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
    TableDetectionSkill,
    ReproducibilityDetectionSkill,
    LimitationsQualityDetectionSkill,
    SoftwareVersionDetectionSkill,
    HardwareDetailDetectionSkill,
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
        self.table_skill = TableDetectionSkill()
        self.reproducibility_skill = ReproducibilityDetectionSkill()
        self.limitations_skill = LimitationsQualityDetectionSkill()
        self.software_skill = SoftwareVersionDetectionSkill()
        self.hardware_detail_skill = HardwareDetailDetectionSkill()
    
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
        table_result = self.table_skill.execute(context)
        repro_result = self.reproducibility_skill.execute(context)
        limits_result = self.limitations_skill.execute(context)
        sw_result = self.software_skill.execute(context)
        hw_detail_result = self.hardware_detail_skill.execute(context)
        
        # Consolidar resultados
        red_flags = {}
        
        # Hiperparámetros
        hyper_flags = hyper_result.get('hyperparameter_flags', {})
        red_flags['hiperparametros_vacios'] = hyper_flags.get('has_vague', False)
        red_flags['sin_learning_rate'] = not hyper_flags.get('has_learning_rate', False)
        red_flags['sin_batch_size'] = not hyper_flags.get('has_batch_size', False)
        red_flags['sin_optimizer'] = not hyper_flags.get('has_optimizer', False)
        red_flags['sin_weight_decay'] = not hyper_flags.get('has_weight_decay', False)
        red_flags['sin_betas'] = not hyper_flags.get('has_betas', False)
        red_flags['sin_epsilon'] = not hyper_flags.get('has_epsilon', False)
        red_flags['sin_epochs'] = not hyper_flags.get('has_epochs', False)
        red_flags['sin_warmup'] = not hyper_flags.get('has_warmup', False)
        
        # Guardar snippets de hiperparámetros encontrados para validación LLM
        hp_snippets = {}
        for key in ['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup',
                     'weight_decay', 'betas', 'epsilon']:
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
        red_flags.update(table_result.get('table_flags', {}))
        red_flags.update(repro_result.get('reproducibility_flags', {}))
        red_flags.update(limits_result.get('limitations_flags', {}))
        red_flags.update(sw_result.get('software_flags', {}))
        red_flags.update(hw_detail_result.get('hardware_detail_flags', {}))
        
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
    """Skill para extraer información estructurada del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text', 'red_flags']):
            return {'extracted_info': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'extracted_info': {}}
        
        self.log_execution("🔍 Extrayendo información estructurada...")
        
        try:
            extraction_prompt = get_extraction_prompt(
                context['paper_text'], 
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
        
        metrics = {
            "tiempo_segundos": context.get('execution_time', 0),
            "caracteres_leidos": len(paper_text),
            "red_flags_detectadas": sum(
                1 for k, v in red_flags.items() 
                if v and not k.startswith("tiene_")
            )
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
            "self_written_summary": evaluation.get('self_written_summary', ''),
            "claims_scope_audit": evaluation.get('claims_scope_audit', {}),
            "limitations_impact": evaluation.get('limitations_impact', {}),
            "theoretical_rigor": evaluation.get('theoretical_rigor', {}),
            "reproducibility": evaluation.get('reproducibility', {}),
            "originality_significance": evaluation.get('originality_significance', {}),
            "ethics_flag": evaluation.get('ethics_flag', {}),
            "peer_review_scores": evaluation.get('peer_review_scores', {}),
            "summary_contributions": evaluation.get('summary_contributions', ''),
            "questions_for_authors": evaluation.get('questions_for_authors', []),
            "recommendation": evaluation.get('recommendation', ''),
            "confidence": evaluation.get('confidence', ''),
            "informacion_extraida": context.get('extracted_info', {}),
            "red_flags": context['red_flags'],
            "metricas": context.get('metrics', {})
        }
        
        self.log_execution("✅ Resultado final construido correctamente")
        return result
