"""Servicio de auditoría de papers refactorizado con arquitectura de skills"""
import time
from backend.common.llm_client import LLMClient
from backend.common.config import (
    AUDIT_CONFIG, 
    EXTRACTION_MODEL_NAME, 
    EVALUATION_MODEL_NAME,
    MAP_MODEL_NAME,
    REDUCE_MODEL_NAME,
    EMBEDDING_MODEL_NAME,
    VERIFICATION_MODEL_NAME
)
from backend.utils.logger import get_logger
from backend.skills.auditor_skills import (
    InformationExtractionSkill,
    ReproducibilityEvaluationSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill,
    ChecklistVerificationSkill
)
from backend.skills.rag_extraction_skill import HybridHyperparameterExtractionSkill

logger = get_logger(__name__)

class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos usando arquitectura de skills"""
    
    def __init__(self):
        """Inicializa el auditor con configuración determinista y skills especializados"""
        # Cliente para extracción inicial
        self.extraction_llm = LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Cliente para evaluación final
        self.evaluation_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Cliente para RAG/Triage (Fase Map)
        self.rag_map_llm = LLMClient(model_name=MAP_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Cliente para RAG/Reduce (Gemma 4)
        self.rag_reduce_llm = LLMClient(model_name=REDUCE_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Cliente para Verificación Estricta (Auditor 2)
        self.verification_llm = LLMClient(model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Inicializar skills especializados
        self.extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm)
        self.hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm)
        self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm)
        
        # Para la verificación estricta usamos el cliente específico (Auditor 2)
        self.verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm)
        
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()
        
        logger.info(f"✅ Motor de Embeddings inicializado: {EMBEDDING_MODEL_NAME}")
        logger.info(f"✅ Auditor inicializado respetando la configuración técnica.")
    
    
    def audit(self, paper_text):
        """
        Analiza el paper usando arquitectura de skills en 3 fases:
        Pre-procesamiento, Extracción y Evaluación
        
        Args:
            paper_text: Texto del paper en formato markdown
            
        Returns:
            Diccionario con resultados de la auditoría
        """
        caracteres = len(paper_text)
        logger.info(f"🚀 Iniciando auditoría con skills. Tamaño: {caracteres} caracteres")
        
        start_time = time.time()
        
        try:
            # Preparar contexto inicial
            context = {'paper_text': paper_text, 'red_flags': {}} # Mantenemos red_flags vacío por compatibilidad interna momentánea
            
            # FASE 1: Extracción de información (con LLM general)
            extraction_result = self.extraction_skill.execute(context)
            if 'extraction_error' in extraction_result:
                logger.error(f"❌ Abortando: Error en extracción: {extraction_result['extraction_error']}")
                return {'error': extraction_result['extraction_error']}
            
            context.update(extraction_result)
            
            # Guardar pasos intermedios para el frontend (Map-Reduce + CoT)
            if 'map_steps' in extraction_result:
                context['general_analysis_map'] = extraction_result['map_steps']
            if 'reduce_step' in extraction_result:
                context['general_analysis_reduce'] = extraction_result['reduce_step']
            
            # Guardar copia del original para comparativa en el frontend
            if 'extracted_info' in extraction_result:
                import copy
                context['original_extraction_raw'] = copy.deepcopy(extraction_result['extracted_info'])
            
            # Verificar si el paper es válido (ML/AI)
            if extraction_result.get('invalid_paper', False):
                logger.warning(f"❌ Paper rechazado: {extraction_result.get('invalid_reason')}")
                return {
                    'error': 'INVALID_PAPER_TYPE',
                    'message': extraction_result.get('invalid_reason', 'Este sistema solo evalúa papers de ML/AI'),
                    'paper_type': extraction_result.get('extracted_info', {}).get('paper_type', 'Unknown')
                }
            
            # FASE 1.5: Extracción estructurada híbrida (RAG + Pydantic)
            hybrid_hp_result = self.hybrid_hp_skill.execute(context)
            # Si hay error en RAG, loggeamos pero intentamos seguir con la extracción general 
            # a menos que sea un error crítico que no devuelva nada
            if 'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid'):
                logger.warning(f"⚠️ Error en extracción híbrida RAG: {hybrid_hp_result['error']}")
            
            context.update(hybrid_hp_result)
            
            # Guardar fragmentos de triage para el frontend
            if 'triage_fragments' in hybrid_hp_result:
                context['hybrid_triage_fragments'] = hybrid_hp_result['triage_fragments']
            
            # Reemplazar hiperparámetros y hardware con los más precisos de la extracción híbrida
            if 'extracted_hyperparameters_hybrid' in context and 'extracted_info' in context:
                hybrid_hps = context['extracted_hyperparameters_hybrid']
                if hybrid_hps:
                    if 'hyperparameters' not in context['extracted_info']:
                        context['extracted_info']['hyperparameters'] = {}
                    # Update standard hyperparameters
                    for key in ['optimizer', 'learning_rate', 'batch_size', 'epochs', 'warmup', 'weight_decay', 'betas', 'epsilon']:
                        # Map keys between Pydantic schema and prompts.py schema if necessary
                        if key == 'warmup': mapped_key = 'warmup_steps'
                        else: mapped_key = key
                        if mapped_key in hybrid_hps and str(hybrid_hps[mapped_key]).strip() and hybrid_hps[mapped_key] != 'NOT FOUND':
                            context['extracted_info']['hyperparameters'][key] = hybrid_hps[mapped_key]
                    
                    if 'hardware' in hybrid_hps and str(hybrid_hps['hardware']).strip() and hybrid_hps['hardware'] != 'NOT FOUND':
                        if 'hardware' not in context['extracted_info']:
                            context['extracted_info']['hardware'] = {}
                        context['extracted_info']['hardware']['gpu_cpu'] = hybrid_hps['hardware']
            
            # FASE 2: Evaluación de reproducibilidad (con LLM)
            evaluation_result = self.evaluation_skill.execute(context)
            if 'evaluation_error' in evaluation_result:
                logger.error(f"❌ Abortando: Error en evaluación: {evaluation_result['evaluation_error']}")
                return {'error': evaluation_result['evaluation_error']}
                
            context.update(evaluation_result)
            
            # Guardar señales de evaluación para el frontend
            if 'evaluation_signals' in evaluation_result:
                context['evaluation_signals'] = evaluation_result['evaluation_signals']
            
            # FASE 2.5: Verificación Estricta (Auditoría de Falsos Negativos)
            verification_result = self.verification_skill.execute(context)
            context.update(verification_result)
            
            # FASE 3: Cálculo de métricas
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            
            metrics_context = {
                **context,
                'execution_time': execution_time,
                'caracteres': caracteres
            }
            metrics_result = self.metrics_skill.execute(metrics_context)
            context.update(metrics_result)
            
            # FASE 4: Agregación de metadatos
            final_result = self.metadata_skill.execute(context)
            
            # Asegurar que se exponga el resultado híbrido y el original para el frontend
            if 'extracted_hyperparameters_hybrid' in context:
                final_result['extracted_hyperparameters_hybrid'] = context['extracted_hyperparameters_hybrid']
            if 'original_extraction_raw' in context:
                final_result['original_extraction_raw'] = context['original_extraction_raw']
            
            logger.info(f"✅ Auditoría completada en {execution_time} segundos")
            
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
