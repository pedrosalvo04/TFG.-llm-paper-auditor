import time
from backend.common.llm_client import LLMClient
from backend.common.config import EVALUATION_MODEL_NAME, EVALUATION_CONFIG, AUDIT_CONFIG
from backend.common.logger import get_logger
from backend.skills.auditor_skills import CriteriaExtractionSkill, MetricsCalculationSkill, MetadataAggregationSkill
from backend.skills.basic_skill import SinglePromptSkill

logger = get_logger(__name__)

class BasicAuditor:
    """Auditor simplificado que ejecuta toda la evaluación en un solo prompt"""
    
    def __init__(self):
        """Inicializa el auditor básico con configuración de skills"""
        self._setup_skills()
        
        self.phases = [
            {
                "index": 0,
                "msg": "📑 Fase 0: Extracción de criterios personalizados...",
                "skill": self.criteria_extraction_skill,
                "processor": self._process_default_result
            },
            {
                "index": 1,
                "msg": "🔍 Fase 1: Análisis Básico y Evaluación Completa...",
                "skill": self.single_prompt_skill,
                "processor": self._process_single_prompt_result
            },
            {
                "index": 2,
                "msg": "📊 Fase 2: Consolidación de métricas y puntuaciones...",
                "skill": self.metrics_skill,
                "processor": self._process_default_result
            },
            {
                "index": 3,
                "msg": "🏁 Fase 3: Generación de informe final y metadatos...",
                "skill": self.metadata_skill,
                "processor": self._process_default_result
            }
        ]
        logger.info(f"✅ BasicAuditor inicializado con pipeline de {len(self.phases)} fases.")

    def _setup_skills(self):
        """Centraliza la creación de clientes LLM y skills especializados."""
        # Usamos el modelo de evaluación (con su configuración) ya que se necesita capacidad de razonamiento
        self.basic_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=EVALUATION_CONFIG)
        self.criteria_extraction_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG)
        
        self.criteria_extraction_skill = CriteriaExtractionSkill(llm_client=self.criteria_extraction_llm)
        self.single_prompt_skill = SinglePromptSkill(llm_client=self.basic_llm)
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()
        
    def _process_default_result(self, result, context):
        if result and 'error' in result:
            logger.error(f"❌ Error en fase: {result['error']}")
            return {'error': result['error']}
        return None

    def _process_single_prompt_result(self, result, context):
        if 'error' in result:
            logger.error(f"❌ Abortando: Error en extracción básica: {result['error']}")
            return {'error': result['error']}
            
        if result.get('invalid_paper', False):
            logger.warning(f"❌ Paper rechazado: {result.get('invalid_reason')}")
            return {
                'error': 'INVALID_PAPER_TYPE',
                'message': result.get('invalid_reason', 'Este sistema solo evalúa papers de ML/AI'),
                'paper_type': result.get('extracted_info', {}).get('paper_type', 'Unknown')
            }
        return None

    def _log_status(self, msg, phase_index=None, status_callback=None):
        """Reporta el progreso tanto al logger como al callback del frontend."""
        logger.info(msg)
        if status_callback:
            try:
                status_callback(msg, phase_index)
            except TypeError:
                status_callback(msg)

    def audit(self, paper_text, status_callback=None, criteria_mode="neurips", criteria_text=None):
        """
        Analiza el paper usando un solo prompt
        """
        caracteres = len(paper_text)
        self._log_status(f"🚀 Iniciando auditoría BÁSICA. Tamaño: {caracteres} caracteres. Modo: {criteria_mode}", phase_index=0, status_callback=status_callback)
        start_time = time.time()
        
        try:
            context = {
                'paper_text': paper_text,
                'criteria_mode': criteria_mode,
                'criteria_text': criteria_text
            }
            final_result = {}
            
            for phase in self.phases:
                if phase["skill"] == self.criteria_extraction_skill and criteria_mode != "free":
                    continue
                    
                self._log_status(phase["msg"], phase_index=phase["index"], status_callback=status_callback)
                
                skill_input = context
                if phase["skill"] == self.metrics_skill:
                    execution_time = round(time.time() - start_time, 2)
                    skill_input = {**context, 'execution_time': execution_time, 'caracteres': caracteres}
                
                result = phase["skill"].execute(skill_input)
                
                error_response = phase["processor"](result, context)
                if error_response:
                    return error_response
                
                context.update(result)
                final_result = result
            
            execution_time = round(time.time() - start_time, 2)
            self._log_status(f"✅ Auditoría BÁSICA completada en {execution_time} segundos", phase_index=3, status_callback=status_callback)
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}
