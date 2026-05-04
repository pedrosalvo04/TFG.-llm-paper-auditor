"""Skills específicos para el auditor de papers - Versión refactorizada"""
import json
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.prompts import get_extraction_prompt, get_evaluation_prompt
from backend.skills.regex_detection_skills import (
    HyperparameterDetectionSkill,
    DataAvailabilityDetectionSkill,
    CodeAvailabilityDetectionSkill,
    StatisticsDetectionSkill,
    EnvironmentalImpactDetectionSkill,
    ProblematicPhrasesDetectionSkill,
    LimitationsQualityDetectionSkill,
    SoftwareVersionDetectionSkill,
    HardwareDetailDetectionSkill,
    LlmUsageDetectionSkill,
    CrowdsourcingDetectionSkill,
    LicenseDetectionSkill,
)


class RedFlagDetectionSkill(BaseSkill):
    """Skill coordinador que ejecuta todos los detectores especializados"""
    
    def __init__(self):
        super().__init__()
        self.hyperparameter_skill = HyperparameterDetectionSkill()
        self.data_skill = DataAvailabilityDetectionSkill()
        self.code_skill = CodeAvailabilityDetectionSkill()
        self.statistics_skill = StatisticsDetectionSkill()
        self.environmental_skill = EnvironmentalImpactDetectionSkill()
        self.problematic_skill = ProblematicPhrasesDetectionSkill()
        self.limitations_skill = LimitationsQualityDetectionSkill()
        self.software_skill = SoftwareVersionDetectionSkill()
        self.hardware_detail_skill = HardwareDetailDetectionSkill()
        self.llm_usage_skill = LlmUsageDetectionSkill()
        self.crowdsourcing_skill = CrowdsourcingDetectionSkill()
        self.license_skill = LicenseDetectionSkill()
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'red_flags': {}}
        
        self.log_execution("=== CONSOLIDANDO RED FLAGS ===")
        
        # Ejecutar todos los detectores
        hyper_result = self.hyperparameter_skill.execute(context)
        data_result = self.data_skill.execute(context)
        code_result = self.code_skill.execute(context)
        stats_result = self.statistics_skill.execute(context)
        env_result = self.environmental_skill.execute(context)
        prob_result = self.problematic_skill.execute(context)
        limits_result = self.limitations_skill.execute(context)
        sw_result = self.software_skill.execute(context)
        hw_detail_result = self.hardware_detail_skill.execute(context)
        llm_usage_result = self.llm_usage_skill.execute(context)
        crowdsourcing_result = self.crowdsourcing_skill.execute(context)
        license_result = self.license_skill.execute(context)
        
        # Consolidar resultados
        red_flags = {}
        
        # Hiperparámetros
        hyper_flags = hyper_result.get('hyperparameter_flags', {})
        red_flags['hiperparametros_vacios'] = hyper_flags.get('has_vague', False)
        red_flags['sin_learning_rate'] = not hyper_flags.get('has_learning_rate', False)
        red_flags['sin_batch_size'] = not hyper_flags.get('has_batch_size', False)
        red_flags['sin_optimizer'] = not hyper_flags.get('has_optimizer', False)
        red_flags['sin_weight_decay'] = not hyper_flags.get('has_weight_decay', False)
        # NeurIPS 2026: betas y epsilon se consideran secundarios y no generan red flags
        red_flags['sin_epochs'] = not hyper_flags.get('has_epochs', False)
        red_flags['sin_warmup'] = not hyper_flags.get('has_warmup', False)
        
        # Guardar snippets de hiperparámetros encontrados para validación LLM
        hp_snippets = {}
        for key in ['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup', 'weight_decay']:
            val = hyper_flags.get(f'{key}_value')
            if val:
                hp_snippets[key] = val
        red_flags['_hp_snippets'] = hp_snippets
        
        # Datos, código, estadística, ambiental, tablas, reproducibilidad
        red_flags.update(data_result.get('data_flags', {}))
        red_flags.update(code_result.get('code_flags', {}))
        red_flags.update(stats_result.get('statistics_flags', {}))
        red_flags.update(env_result.get('environmental_flags', {}))
        red_flags.update(prob_result.get('problematic_flags', {}))
        red_flags.update(limits_result.get('limitations_flags', {}))
        red_flags.update(sw_result.get('software_flags', {}))
        red_flags.update(hw_detail_result.get('hardware_detail_flags', {}))
        red_flags.update(llm_usage_result.get('llm_usage_flags', {}))
        red_flags.update(crowdsourcing_result.get('crowdsourcing_flags', {}))
        red_flags.update(license_result.get('license_flags', {}))
        
        critical_flags = [
            k for k, v in red_flags.items() 
            if v and not k.startswith("tiene_") and not k.startswith("menciona_") 
            and not k.startswith("_") and not k.startswith("cantidad_")
            and not k.startswith("puntos_")
        ]
        
        self.log_execution("\n" + "="*60)
        self.log_execution(f"🚩 RED FLAGS FINALES: {len(critical_flags)} detectadas")
        if critical_flags:
            for flag in critical_flags:
                self.log_execution(f"  ⚠️ {flag}")
        else:
            self.log_execution("✅ No se detectaron red flags críticas")
        self.log_execution("="*60 + "\n")
        
        return {'red_flags': red_flags}


class InformationExtractionSkill(BaseSkill):
    """Skill para extraer información estructurada del paper usando Context Mapping (Agentic RAG)"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text', 'red_flags']):
            return {'extracted_info': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'extracted_info': {}}
        
        self.log_execution("🔍 Extrayendo información estructurada usando Context Mapping...")
        
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from sentence_transformers import SentenceTransformer
            import chromadb
            
            # 1. Chunking
            self.log_execution("Fragmentando texto para Context Mapping...")
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=300)
            chunks = splitter.split_text(context['paper_text'])
            
            # 2. Embedding
            self.log_execution("Generando embeddings locales para 15 agentes virtuales...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(chunks).tolist()
            
            chroma_client = chromadb.Client()
            try:
                chroma_client.delete_collection("context_mapping_chunks")
            except:
                pass
            collection = chroma_client.create_collection(name="context_mapping_chunks")
            
            ids = [str(i) for i in range(len(chunks))]
            collection.add(embeddings=embeddings, documents=chunks, ids=ids)
            
            # 3. Consultas específicas por dominio (Los 15 'Agentes')
            queries_map = {
                'code': ["github repository url", "source code open source", "code is available at"],
                'data': ["dataset availability", "data download link", "dataset can be found"],
                'hyperparameters': ["hyperparameters training details", "learning rate optimizer batch size epochs"],
                'hardware': ["hardware gpu tpu cpu memory", "compute resources time hours days"],
                'statistics': ["confidence intervals error bars", "statistical significance p-value multiple runs"],
                'architecture': ["model architecture layers", "transformer backbone dimensions parameters"],
                'baseline_comparison': ["baselines compared against", "state-of-the-art benchmark results"],
                'software': ["pytorch tensorflow jax version", "software environment dependencies"],
                'limitations': ["limitations weakness failure cases", "future work negative results"],
                'problematic_phrases': ["proprietary confidential", "cannot release restricted non-public"],
                'theory_and_proofs': ["theorem proof lemma assumption", "mathematical derivation appendix"],
                'broader_impacts': ["broader societal impact", "ethical considerations negative impact"],
                'llm_usage': ["language model generated by chatgpt", "annotated by llm automatic evaluation"],
                'human_subjects': ["human subjects crowdsourcing mturk", "human evaluators IRB approval"],
                'licenses': ["license MIT apache cc-by", "licensed under terms of use dataset license"]
            }
            
            context_mapping = {}
            for key, queries in queries_map.items():
                query_embeddings = model.encode(queries).tolist()
                results = collection.query(query_embeddings=query_embeddings, n_results=15)
                
                relevant_chunks = set()
                for doc_list in results['documents']:
                    for doc in doc_list:
                        relevant_chunks.add(doc)
                
                context_mapping[key] = "\n\n...\n\n".join(relevant_chunks)
                
            self.log_execution("✅ Context Mapping completado. Generando prompt maestro...")
            
            extraction_prompt = get_extraction_prompt(
                context_mapping, 
                context['red_flags']
            )
            response = self.llm_client.generate(extraction_prompt)
            extracted_info = json.loads(response.text)
            
            # Validar si el paper es ML/AI
            if extracted_info.get('paper_type', '').startswith('INVALID'):
                self.log_execution("❌ Paper no válido: No es ML/AI", level="error")
                return {
                    'extracted_info': extracted_info,
                    'invalid_paper': True,
                    'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')
                }
            
            self.log_execution("✅ Información extraída correctamente")
            return {'extracted_info': extracted_info, 'invalid_paper': False}
        except Exception as e:
            self.log_execution(f"❌ Error en extracción: {str(e)}", level="error")
            return {'extracted_info': {}, 'extraction_error': str(e)}


class ReproducibilityEvaluationSkill(BaseSkill):
    """Skill para evaluar la reproducibilidad del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['extracted_info', 'red_flags']):
            return {'evaluation': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'evaluation': {}}
        
        self.log_execution("📊 Evaluando reproducibilidad...")
        
        try:
            evaluation_prompt = get_evaluation_prompt(
                context['extracted_info'], 
                context['red_flags']
            )
            response = self.llm_client.generate(evaluation_prompt)
            evaluation = json.loads(response.text)
            self.log_execution("✅ Evaluación completada")
            return {'evaluation': evaluation}
        except json.JSONDecodeError as e:
            self.log_execution(f"❌ Error parseando JSON: {str(e)}", level="error")
            return {'evaluation': {}, 'evaluation_error': f'JSON parse error: {str(e)}'}
        except Exception as e:
            error_msg = str(e)
            self.log_execution(f"❌ Error en evaluación: {error_msg}", level="error")
            
            if '503' in error_msg or 'UNAVAILABLE' in error_msg:
                return {'evaluation': {}, 'evaluation_error': 'El modelo LLM está experimentando alta demanda. Intenta nuevamente en unos momentos.'}
            
            return {'evaluation': {}, 'evaluation_error': error_msg}


class MetricsCalculationSkill(BaseSkill):
    """Skill para calcular métricas de la auditoría"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text', 'red_flags']):
            return {'metrics': {}}
        
        self.log_execution("Calculando métricas...")
        
        paper_text = context['paper_text']
        red_flags = context['red_flags']
        
        critical_flags = [
            k for k, v in red_flags.items() 
            if v and not k.startswith("tiene_") and not k.startswith("menciona_") 
            and not k.startswith("_") and not k.startswith("cantidad_")
            and not k.startswith("puntos_")
        ]
        
        metrics = {
            "tiempo_segundos": context.get('execution_time', 0),
            "caracteres_leidos": len(paper_text),
            "red_flags_detectadas": len(critical_flags)
        }
        
        self.log_execution(f"✅ Métricas calculadas: {metrics['red_flags_detectadas']} red flags")
        return {'metrics': metrics}


class MetadataAggregationSkill(BaseSkill):
    """Skill para agregar metadatos de la auditoría"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['red_flags']):
            return {'error': 'Contexto inválido'}
        
        self.log_execution("Agregando metadatos y construyendo resultado final...")
        
        evaluation = context.get('evaluation', {})
        
        result = {
            "claims": evaluation.get('claims', {}),
            "limitations": evaluation.get('limitations', {}),
            "theory_assumptions_proofs": evaluation.get('theory_assumptions_proofs', {}),
            "experimental_result_reproducibility": evaluation.get('experimental_result_reproducibility', {}),
            "open_access_data_code": evaluation.get('open_access_data_code', {}),
            "experimental_setting_details": evaluation.get('experimental_setting_details', {}),
            "experiment_statistical_significance": evaluation.get('experiment_statistical_significance', {}),
            "experiments_compute_resource": evaluation.get('experiments_compute_resource', {}),
            "code_of_ethics": evaluation.get('code_of_ethics', {}),
            "broader_impacts": evaluation.get('broader_impacts', {}),
            "safeguards": evaluation.get('safeguards', {}),
            "licenses": evaluation.get('licenses', {}),
            "assets": evaluation.get('assets', {}),
            "crowdsourcing_human_subjects": evaluation.get('crowdsourcing_human_subjects', {}),
            "irb_approvals": evaluation.get('irb_approvals', {}),
            "declaration_llm_usage": evaluation.get('declaration_llm_usage', {}),
            "informacion_extraida": context.get('extracted_info', {}),
            "red_flags": context['red_flags'],
            "metricas": context.get('metrics', {})
        }
        
        self.log_execution("✅ Resultado final construido correctamente")
        return result
