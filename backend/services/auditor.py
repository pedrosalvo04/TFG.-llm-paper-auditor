import re
import time
import copy
from backend.common.llm_client import LLMClient
from backend.common.config import (
    AUDIT_CONFIG, 
    EVALUATION_CONFIG,
    EXTRACTION_MODEL_NAME, 
    EVALUATION_MODEL_NAME,
    MAP_MODEL_NAME,
    REDUCE_MODEL_NAME,
    VERIFICATION_MODEL_NAME
)
from backend.common.logger import get_logger
from backend.skills import (
    InformationExtractionSkill,
    SectionMappingSkill,
    NeurIPSComplianceSkill,
    MetricsCalculationSkill,
    MetadataAggregationSkill
)

logger = get_logger(__name__)


class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos usando arquitectura de skills"""
    
    def __init__(self):
        """Inicializa el auditor con configuración determinista y skills especializados"""
        self._setup_skills()
        
        # Definición del pipeline de auditoría para ejecución secuencial
        self.phases = [
            {
                "index": 1,
                "msg": "🔍 Fase 1: Extracción inicial de información clave...",
                "skill": self.extraction_skill,
                "processor": self._process_extraction_result
            },
            {
                "index": 2,
                "msg": "🗺️ Fase 1.5: Mapeo inteligente de secciones...",
                "skill": self.section_mapping_skill,
                "processor": self._process_default_result
            },
            {
                "index": 3,
                "msg": "⚖️ Fase 2: Evaluación de criterios de cumplimiento NeurIPS 2026...",
                "skill": self.compliance_skill,
                "processor": self._process_evaluation_result
            },
            {
                "index": 4,
                "msg": "📊 Fase 3: Consolidación de métricas y puntuaciones...",
                "skill": self.metrics_skill,
                "processor": self._process_default_result
            },
            {
                "index": 5,
                "msg": "🏁 Fase 4: Generación de informe final y metadatos...",
                "skill": self.metadata_skill,
                "processor": self._process_default_result
            }
        ]
        
        logger.info(f"✅ Auditor inicializado con pipeline de {len(self.phases)} fases.")

    def _setup_skills(self):
        """Centraliza la creación de clientes LLM y skills especializados."""
        # Clientes LLM
        self.extraction_llm = LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        self.section_mapping_llm = LLMClient(model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        self.evaluation_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=EVALUATION_CONFIG)
        self.verification_llm = LLMClient(model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        # Skills
        self.extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm)
        self.section_mapping_skill = SectionMappingSkill(llm_client=self.section_mapping_llm)
        self.compliance_skill = NeurIPSComplianceSkill(llm_client=self.evaluation_llm)
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()
    
    
    

    
    def _process_extraction_result(self, result, context):
        """Procesa el resultado de la extracción, maneja errores y prepara datos para el frontend."""
        if 'extraction_error' in result:
            logger.error(f"❌ Abortando: Error en extracción: {result['extraction_error']}")
            return {'error': result['extraction_error']}
        
        # Enriquecer contexto para el frontend (Map-Reduce + CoT)
        if 'map_steps' in result:
            context['general_analysis_map'] = result['map_steps']
        if 'reduce_step' in result:
            context['general_analysis_reduce'] = result['reduce_step']
        
        # Guardar copia del original para comparativa en el frontend
        if 'extracted_info' in result:
            context['original_extraction_raw'] = copy.deepcopy(result['extracted_info'])
            
        # Verificar si el paper es válido (ML/AI)
        if result.get('invalid_paper', False):
            logger.warning(f"❌ Paper rechazado: {result.get('invalid_reason')}")
            return {
                'error': 'INVALID_PAPER_TYPE',
                'message': result.get('invalid_reason', 'Este sistema solo evalúa papers de ML/AI'),
                'paper_type': result.get('extracted_info', {}).get('paper_type', 'Unknown')
            }
        return None

    def _process_default_result(self, result, context):
        """Procesador por defecto para fases sin lógica UI especial."""
        if result and 'error' in result:
            logger.error(f"❌ Error en fase: {result['error']}")
            return {'error': result['error']}
        return None




    def _process_evaluation_result(self, result, context):
        """Procesa el resultado de la evaluación y prepara señales para el frontend."""
        if 'evaluation_error' in result:
            logger.error(f"❌ Abortando: Error en evaluación: {result['evaluation_error']}")
            return {'error': result['evaluation_error']}
            
        # Guardar ayudas de evaluación para el frontend
        if 'evaluation_helps' in result:
            context['evaluation_helps'] = result['evaluation_helps']
        return None





    def _log_status(self, msg, phase_index=None, status_callback=None):
        """Reporta el progreso tanto al logger como al callback del frontend."""
        logger.info(msg)
        if status_callback:
            try:
                status_callback(msg, phase_index)
            except TypeError:
                status_callback(msg)

    def audit(self, paper_text, status_callback=None):
        """
        Analiza el paper usando arquitectura de skills en un pipeline multimodelo.
        Analiza el paper ejecutando el pipeline de skills definido.
        """
        caracteres = len(paper_text)
        self._log_status(f"🚀 Iniciando auditoría con skills. Tamaño: {caracteres} caracteres.", phase_index=0, status_callback=status_callback)
        start_time = time.time()
        
        try:
            context = {'paper_text': paper_text}
            final_result = {}
            
            for phase in self.phases:
                # 1. Reportar progreso
                self._log_status(phase["msg"], phase_index=phase["index"], status_callback=status_callback)
                
                # 2. Preparar input (Inyectar métricas de tiempo si es la fase de métricas)
                skill_input = context
                if phase["skill"] == self.metrics_skill:
                    execution_time = round(time.time() - start_time, 2)
                    skill_input = {**context, 'execution_time': execution_time, 'caracteres': caracteres}
                
                # 3. Ejecutar Skill
                result = phase["skill"].execute(skill_input)
                
                # 4. Procesar resultado y posibles errores
                error_response = phase["processor"](result, context)
                if error_response:
                    return error_response
                
                # 5. Actualizar contexto
                context.update(result)
                final_result = result # El último skill suele ser el que genera el informe final
            
            # Asegurar que se exponga el resultado original para el frontend
            if 'original_extraction_raw' in context:
                final_result['original_extraction_raw'] = context['original_extraction_raw']
            
            execution_time = round(time.time() - start_time, 2)
            self._log_status(f"✅ Auditoría completada en {execution_time} segundos", phase_index=5, status_callback=status_callback)
            return final_result


        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
