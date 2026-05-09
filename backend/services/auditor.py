import re
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
from backend.skills import (
    InformationExtractionSkill,
    ReproducibilityEvaluationSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill,
    ChecklistVerificationSkill,
    HybridHyperparameterExtractionSkill
)

logger = get_logger(__name__)

# Patrones para pre-procesamiento y señales rápidas
REGEX_PATTERNS = {
    'tiene_github': r"github\.com/[\w.-]+",
    'tiene_zenodo': r"zenodo\.org/record/\d+",
    'tiene_arxiv': r"arxiv\.org/abs/\d+\.\d+",
    'menciona_dataset': r"(dataset|data\s+set|corpus)",
    'menciona_apendice': r"(appendix|supplementary\s+material)",
    'menciona_limitaciones': r"(limitations|weaknesses|future\s+work)",
    'menciona_etica': r"(ethics|ethical\s+considerations|broader\s+impact)",
    'menciona_licencia': r"(license|licence|CC-BY|MIT\s+license|Apache\s+2\.0)",
}

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
    
    
    def _preprocess_paper(self, text):
        """Detecta patrones básicos en el texto del paper para generar señales rápidas"""
        results = {}
        for key, pattern in REGEX_PATTERNS.items():
            results[key] = bool(re.search(pattern, text, re.IGNORECASE))
        return results
    
    
    def audit(self, paper_text, status_callback=None, use_rag=True):
        """
        Analiza el paper usando arquitectura de skills en 3 fases:
        Pre-procesamiento, Extracción y Evaluación
        
        Args:
            paper_text: Texto del paper en formato markdown
            status_callback: Función opcional para reportar el progreso (logs)
            use_rag: Si es True, utiliza extracción híbrida con RAG (Fase 1.5)
            
        Returns:
            Diccionario con resultados de la auditoría
        """
        def log_status(msg, phase_index=None):
            logger.info(msg)
            if status_callback:
                try:
                    status_callback(msg, phase_index)
                except TypeError:
                    # Fallback para callbacks antiguos que solo aceptan un argumento
                    status_callback(msg)

        caracteres = len(paper_text)
        log_status(f"🚀 Iniciando auditoría con skills. Tamaño: {caracteres} caracteres. RAG: {'Activado' if use_rag else 'Desactivado'}", phase_index=0)
        
        start_time = time.time()
        
        try:
            # Preparar contexto inicial con pre-procesamiento
            red_flags = self._preprocess_paper(paper_text)
            context = {'paper_text': paper_text, 'red_flags': red_flags}
            
            # FASE 1: Extracción de información (con LLM general)
            log_status("🔍 Fase 1: Extracción inicial de información clave...", phase_index=1)
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
            if use_rag:
                log_status("🧠 Fase 1.5: Profundización técnica con RAG y Pydantic...", phase_index=2)
                hybrid_hp_result = self.hybrid_hp_skill.execute(context)
                # Si hay error en RAG, loggeamos pero intentamos seguir con la extracción general 
                # a menos que sea un error crítico que no devuelva nada
                if 'error' in hybrid_hp_result and not hybrid_hp_result.get('extracted_hyperparameters_hybrid'):
                    logger.warning(f"⚠️ Error en extracción híbrida RAG: {hybrid_hp_result['error']}")
                
                context.update(hybrid_hp_result)
                
                # Guardar fragmentos de triage para el frontend
                if 'triage_fragments' in hybrid_hp_result:
                    context['hybrid_triage_fragments'] = hybrid_hp_result['triage_fragments']
            else:
                log_status("⏩ Fase 1.5 omitida (RAG desactivado)", phase_index=2)
            
            # Reemplazar hiperparámetros y hardware con los más precisos de la extracción híbrida
            if 'extracted_hyperparameters_hybrid' in context and 'extracted_info' in context:
                hybrid_hps = context['extracted_hyperparameters_hybrid']
                if hybrid_hps:
                    if 'hyperparameters' not in context['extracted_info']:
                        context['extracted_info']['hyperparameters'] = {}
                    # Update standard hyperparameters
                    # Update standard hyperparameters with hybrid results
                    for key in ['optimizer', 'learning_rate', 'batch_size', 'epochs', 'training_steps', 'total_tokens', 'warmup_steps', 'weight_decay', 'betas', 'epsilon', 'random_seed', 'hardware', 'latency_metrics']:
                        if key in hybrid_hps and str(hybrid_hps[key]).strip() and hybrid_hps[key] != 'NOT FOUND':
                            if 'hyperparameters' not in context['extracted_info']:
                                context['extracted_info']['hyperparameters'] = {}
                            context['extracted_info']['hyperparameters'][key] = hybrid_hps[key]
                    
                    # Handle hardware info more robustly
                    hybrid_hw = hybrid_hps.get('hardware')
                    if hybrid_hw and str(hybrid_hw).strip() and hybrid_hw != 'NOT FOUND':
                        # Ensure 'hardware' key exists and is a dictionary
                        if 'hardware' not in context['extracted_info'] or not isinstance(context['extracted_info']['hardware'], dict):
                            # If it was a list or string, preserve it as 'raw_info' before resetting
                            old_hw = context['extracted_info'].get('hardware')
                            context['extracted_info']['hardware'] = {}
                            if old_hw:
                                context['extracted_info']['hardware']['original_info'] = str(old_hw)
                        
                        context['extracted_info']['hardware']['gpu_cpu'] = hybrid_hw
            
            # FASE 2: Evaluación de reproducibilidad (con LLM)
            log_status("⚖️ Fase 2: Evaluación de criterios de reproducibilidad...", phase_index=3)
            evaluation_result = self.evaluation_skill.execute(context)
            if 'evaluation_error' in evaluation_result:
                logger.error(f"❌ Abortando: Error en evaluación: {evaluation_result['evaluation_error']}")
                return {'error': evaluation_result['evaluation_error']}
                
            context.update(evaluation_result)
            
            # Guardar señales de evaluación para el frontend
            if 'evaluation_signals' in evaluation_result:
                context['evaluation_signals'] = evaluation_result['evaluation_signals']
            
            # FASE 2.5: Verificación Estricta (Auditoría de Falsos Negativos)
            log_status("🛡️ Fase 2.5: Verificación estricta de cumplimiento (Auditor 2)...", phase_index=4)
            verification_result = self.verification_skill.execute(context)
            context.update(verification_result)
            
            # FASE 3: Cálculo de métricas
            log_status("📊 Fase 3: Consolidación de métricas y puntuaciones...", phase_index=5)
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
            log_status("🏁 Fase 4: Generación de informe final y metadatos...", phase_index=6)
            final_result = self.metadata_skill.execute(context)
            
            # Asegurar que se exponga el resultado híbrido y el original para el frontend
            if 'extracted_hyperparameters_hybrid' in context:
                final_result['extracted_hyperparameters_hybrid'] = context['extracted_hyperparameters_hybrid']
            if 'original_extraction_raw' in context:
                final_result['original_extraction_raw'] = context['original_extraction_raw']
            
            log_status(f"✅ Auditoría completada en {execution_time} segundos", phase_index=7)
            
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
