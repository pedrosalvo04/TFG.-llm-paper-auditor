"""Servicio de auditoría de papers refactorizado con arquitectura de skills"""
import time
from backend.common.llm_client import LLMClient
from backend.common.config import AUDIT_CONFIG
from backend.utils.logger import get_logger
from backend.skills.auditor_skills import (
    RedFlagDetectionSkill,
    InformationExtractionSkill,
    ReproducibilityEvaluationSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill
)
from backend.skills.rag_extraction_skill import HybridHyperparameterExtractionSkill

logger = get_logger(__name__)

class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos usando arquitectura de skills"""
    
    def __init__(self):
        """Inicializa el auditor con configuración determinista y skills especializados"""
        self.llm_client = LLMClient(generation_config=AUDIT_CONFIG)
        
        # Inicializar skills especializados
        self.red_flag_skill = RedFlagDetectionSkill()
        self.extraction_skill = InformationExtractionSkill(llm_client=self.llm_client)
        self.hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.llm_client)
        self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.llm_client)
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()
        
        logger.info("✅ Auditor de papers inicializado correctamente")
    
    
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
            context = {'paper_text': paper_text}
            
            # FASE 0: Detección de red flags (sin LLM)
            red_flags_result = self.red_flag_skill.execute(context)
            context.update(red_flags_result)
            
            # FASE 1: Extracción de información (con LLM general)
            extraction_result = self.extraction_skill.execute(context)
            context.update(extraction_result)
            
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
            context.update(hybrid_hp_result)
            
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
                    
                    # --- SINCRONIZACIÓN DE RED FLAGS ---
                    # Si el experto (RAG) encontró el dato, desactivamos la Red Flag preliminar del Regex
                    if 'red_flags' in context:
                        current_flags = context['red_flags']
                        if hybrid_hps.get('learning_rate') != 'NOT FOUND':
                            current_flags['sin_learning_rate'] = False
                        if hybrid_hps.get('epochs') != 'NOT FOUND':
                            current_flags['sin_epochs'] = False
                        if hybrid_hps.get('batch_size') != 'NOT FOUND':
                            current_flags['sin_batch_size'] = False
                        if hybrid_hps.get('optimizer') != 'NOT FOUND':
                            current_flags['sin_optimizer'] = False
                        if hybrid_hps.get('warmup_steps') != 'NOT FOUND':
                            current_flags['sin_warmup'] = False
                        if hybrid_hps.get('weight_decay') != 'NOT FOUND':
                            current_flags['sin_weight_decay'] = False
                        if hybrid_hps.get('betas') != 'NOT FOUND':
                            current_flags['sin_betas'] = False
                        if hybrid_hps.get('epsilon') != 'NOT FOUND':
                            current_flags['sin_epsilon'] = False
            
            # FASE 2: Evaluación de reproducibilidad (con LLM)
            evaluation_result = self.evaluation_skill.execute(context)
            context.update(evaluation_result)
            
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
            
            # Asegurar que se exponga el resultado híbrido para el frontend
            if 'extracted_hyperparameters_hybrid' in context:
                final_result['extracted_hyperparameters_hybrid'] = context['extracted_hyperparameters_hybrid']
            
            logger.info(f"✅ Auditoría completada en {execution_time} segundos")
            
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
