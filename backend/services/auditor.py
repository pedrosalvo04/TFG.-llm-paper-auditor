"""
Servicio de auditoría refactorizado con AuditState tipado.

Cambios respecto a la versión anterior:
  - El contexto entre skills es ahora un dict normal (compatible con el frontend),
    pero enriquecido con el modelo AuditState que documenta el contrato de datos.
  - Las instancias de LLMClient se inyectan por constructor (Dependency Injection),
    lo que facilita el mocking en tests unitarios sin llamadas reales a la API.
  - La lógica de ensamblaje final usa AuditState.to_frontend_dict() como única
    fuente de verdad para las claves que espera el frontend.
  - Se elimina el import condicional de `copy` dentro del método.
"""
import copy
import time

from backend.common.audit_state import AuditState
from backend.common.llm_client import LLMClient
<<<<<<< Updated upstream
from backend.common.config import AUDIT_CONFIG
=======
from backend.common.config import (
    AUDIT_CONFIG,
    EXTRACTION_MODEL_NAME,
    EVALUATION_MODEL_NAME,
    MAP_MODEL_NAME,
    REDUCE_MODEL_NAME,
    EMBEDDING_MODEL_NAME,
    VERIFICATION_MODEL_NAME,
)
>>>>>>> Stashed changes
from backend.utils.logger import get_logger
from backend.skills.auditor_skills import (
    RedFlagDetectionSkill,
    InformationExtractionSkill,
    ReproducibilityEvaluationSkill,
    MetricsCalculationSkill,
<<<<<<< Updated upstream
    MetadataAggregationSkill
=======
    MetadataAggregationSkill,
    ChecklistVerificationSkill,
>>>>>>> Stashed changes
)
from backend.skills.rag_extraction_skill import HybridHyperparameterExtractionSkill

logger = get_logger(__name__)


class PaperAuditor:
<<<<<<< Updated upstream
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
=======
    """
    Auditor de reproducibilidad en papers científicos.

    Usa una arquitectura de skills con Dependency Injection:
    los clientes LLM se crean en __init__ y se inyectan a cada skill,
    permitiendo mockearlos en tests sin llamadas reales a la API de Google.
    """

    def __init__(
        self,
        extraction_llm: LLMClient | None = None,
        evaluation_llm: LLMClient | None = None,
        rag_map_llm: LLMClient | None = None,
        verification_llm: LLMClient | None = None,
    ) -> None:
        """
        Inicializa el auditor con clientes LLM inyectados o por defecto.

        Parámetros
        ----------
        extraction_llm : LLMClient, opcional
            Cliente para la fase de extracción (MAP-REDUCE general).
        evaluation_llm : LLMClient, opcional
            Cliente para la fase de evaluación NeurIPS.
        rag_map_llm : LLMClient, opcional
            Cliente para el pipeline RAG (MAP de hiperparámetros).
        verification_llm : LLMClient, opcional
            Cliente para la verificación estricta (Auditor 2).
        """
        # Dependency Injection: usar los clientes proporcionados o crear los defaults
        self.extraction_llm = extraction_llm or LLMClient(
            model_name=EXTRACTION_MODEL_NAME, generation_config=AUDIT_CONFIG
        )
        self.evaluation_llm = evaluation_llm or LLMClient(
            model_name=EVALUATION_MODEL_NAME, generation_config=AUDIT_CONFIG
        )
        self.rag_map_llm = rag_map_llm or LLMClient(
            model_name=MAP_MODEL_NAME, generation_config=AUDIT_CONFIG
        )
        self.verification_llm = verification_llm or LLMClient(
            model_name=VERIFICATION_MODEL_NAME, generation_config=AUDIT_CONFIG
        )

        # Skills especializados (reciben el cliente ya construido)
        self.extraction_skill = InformationExtractionSkill(llm_client=self.extraction_llm)
        self.hybrid_hp_skill = HybridHyperparameterExtractionSkill(llm_client=self.rag_map_llm)
        self.evaluation_skill = ReproducibilityEvaluationSkill(llm_client=self.evaluation_llm)
        self.verification_skill = ChecklistVerificationSkill(llm_client=self.verification_llm)
        self.metrics_skill = MetricsCalculationSkill()
        self.metadata_skill = MetadataAggregationSkill()

        logger.info(f"✅ Motor de Embeddings configurado: {EMBEDDING_MODEL_NAME}")
        logger.info("✅ Auditor inicializado con Dependency Injection y AuditState tipado.")

    def audit(self, paper_text: str, structural_chunks: list | None = None) -> dict:
>>>>>>> Stashed changes
        """
        Analiza el paper usando arquitectura de skills en 4 fases.

        El estado fluye como dict nativo para compatibilidad con el frontend,
        pero el contrato de datos está documentado en AuditState.

        Parámetros
        ----------
        paper_text : str
            Texto del paper en formato markdown.

        Devuelve
        --------
        dict con los resultados de la auditoría (compatible con el frontend).
        """
        caracteres = len(paper_text)
        logger.info(f"🚀 Iniciando auditoría. Tamaño: {caracteres} caracteres")

        start_time = time.time()

        try:
<<<<<<< Updated upstream
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
=======
            # Contexto inicial — incluye structural_chunks si vienen de Docling
            state = AuditState(paper_text=paper_text)
            context: dict = {
                "paper_text": paper_text,
                "red_flags": {},
                "structural_chunks": structural_chunks or [],  # Chunks estructurales de Docling
            }
            if structural_chunks:
                n_tables = sum(1 for c in structural_chunks if getattr(c, 'chunk_type', '') == 'table')
                n_sections = sum(1 for c in structural_chunks if getattr(c, 'chunk_type', '') == 'section')
                logger.info(
                    f"🏗️ Chunking Estructural activo: {n_sections} secciones, "
                    f"{n_tables} tablas independientes."
                )
            else:
                logger.info("⚠️ Sin structural_chunks — RAG usará chunking por caracteres (fallback).")

            # ------------------------------------------------------------------
            # FASE 1: Extracción general (Map-Reduce + Structured Outputs)
            # ------------------------------------------------------------------
            extraction_result = self.extraction_skill.execute(context)

            if "extraction_error" in extraction_result:
                logger.error(
                    f"❌ Abortando: Error en extracción: {extraction_result['extraction_error']}"
                )
                return {"error": extraction_result["extraction_error"]}

            context.update(extraction_result)
            state.map_steps = extraction_result.get("map_steps", [])
            state.reduce_step = extraction_result.get("reduce_step")

            if extraction_result.get("invalid_paper", False):
                logger.warning(
                    f"❌ Paper rechazado: {extraction_result.get('invalid_reason')}"
                )
>>>>>>> Stashed changes
                return {
                    "error": "INVALID_PAPER_TYPE",
                    "message": extraction_result.get(
                        "invalid_reason", "Este sistema solo evalúa papers de ML/AI"
                    ),
                    "paper_type": extraction_result.get("extracted_info", {}).get(
                        "paper_type", "Unknown"
                    ),
                }

            if "extracted_info" in extraction_result:
                state.extracted_info = extraction_result["extracted_info"]
                state.original_extraction_raw = copy.deepcopy(extraction_result["extracted_info"])
                context["original_extraction_raw"] = state.original_extraction_raw

            # ------------------------------------------------------------------
            # FASE 1.5: Extracción RAG híbrida de hiperparámetros
            # ------------------------------------------------------------------
            hybrid_hp_result = self.hybrid_hp_skill.execute(context)
<<<<<<< Updated upstream
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
=======

            if (
                "error" in hybrid_hp_result
                and not hybrid_hp_result.get("extracted_hyperparameters_hybrid")
            ):
                logger.warning(
                    f"⚠️ Error en extracción híbrida RAG: {hybrid_hp_result.get('error')}"
                )

            context.update(hybrid_hp_result)
            state.extracted_hyperparameters_hybrid = hybrid_hp_result.get(
                "extracted_hyperparameters_hybrid"
            )
            state.triage_fragments = hybrid_hp_result.get("triage_fragments", [])
            context["hybrid_triage_fragments"] = state.triage_fragments

            # Enriquecer los hiperparámetros de extracted_info con los valores RAG más precisos
            self._merge_hybrid_hyperparameters(context, state)

            # ------------------------------------------------------------------
            # FASE 2: Evaluación de reproducibilidad
            # ------------------------------------------------------------------
            evaluation_result = self.evaluation_skill.execute(context)

            if "evaluation_error" in evaluation_result:
                logger.error(
                    f"❌ Abortando: Error en evaluación: {evaluation_result['evaluation_error']}"
                )
                return {"error": evaluation_result["evaluation_error"]}

            context.update(evaluation_result)
            state.evaluation = evaluation_result.get("evaluation")
            state.evaluation_signals = evaluation_result.get("evaluation_signals")

            if "evaluation_signals" in evaluation_result:
                context["evaluation_signals"] = evaluation_result["evaluation_signals"]

            # ------------------------------------------------------------------
            # FASE 2.5: Verificación estricta (Auditor 2 / Self-Correction)
            # ------------------------------------------------------------------
            verification_result = self.verification_skill.execute(context)
            context.update(verification_result)
            if "evaluation" in verification_result:
                state.evaluation = verification_result["evaluation"]

            # ------------------------------------------------------------------
            # FASE 3: Métricas
            # ------------------------------------------------------------------
>>>>>>> Stashed changes
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            state.execution_time = execution_time
            state.caracteres = caracteres

            metrics_context = {**context, "execution_time": execution_time, "caracteres": caracteres}
            metrics_result = self.metrics_skill.execute(metrics_context)
            context.update(metrics_result)
            state.metrics = metrics_result.get("metrics")

            # ------------------------------------------------------------------
            # FASE 4: Agregación final → dict compatible con el frontend
            # ------------------------------------------------------------------
            final_result = self.metadata_skill.execute(context)
<<<<<<< Updated upstream
            
            # Asegurar que se exponga el resultado híbrido para el frontend
            if 'extracted_hyperparameters_hybrid' in context:
                final_result['extracted_hyperparameters_hybrid'] = context['extracted_hyperparameters_hybrid']
            
=======

            # Añadir campos extra que el frontend necesita y no pasan por MetadataAggregationSkill
            if state.extracted_hyperparameters_hybrid:
                final_result["extracted_hyperparameters_hybrid"] = (
                    state.extracted_hyperparameters_hybrid
                )
            if state.original_extraction_raw:
                final_result["original_extraction_raw"] = state.original_extraction_raw

>>>>>>> Stashed changes
            logger.info(f"✅ Auditoría completada en {execution_time} segundos")
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(
                f"❌ Error durante la auditoría tras "
                f"{round(end_time - start_time, 2)}s: {str(e)}"
            )
            return {"error": str(e)}

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    @staticmethod
    def _merge_hybrid_hyperparameters(context: dict, state: AuditState) -> None:
        """
        Actualiza los hiperparámetros de extracted_info con los valores más
        precisos obtenidos por el pipeline RAG híbrido.

        Mantiene la misma lógica de la versión anterior pero centralizada aquí.
        """
        hybrid_hps = state.extracted_hyperparameters_hybrid
        if not hybrid_hps or not context.get("extracted_info"):
            return

        if "hyperparameters" not in context["extracted_info"]:
            context["extracted_info"]["hyperparameters"] = {}

        key_map = {
            "optimizer": "optimizer",
            "learning_rate": "learning_rate",
            "batch_size": "batch_size",
            "epochs": "epochs",
            "warmup": "warmup_steps",   # alias: prompts usa 'warmup', RAG usa 'warmup_steps'
            "weight_decay": "weight_decay",
            "betas": "betas",
            "epsilon": "epsilon",
        }

        for dest_key, src_key in key_map.items():
            value = hybrid_hps.get(src_key)
            if value and str(value).strip() and str(value) != "NOT FOUND":
                context["extracted_info"]["hyperparameters"][dest_key] = value

        hw_value = hybrid_hps.get("hardware")
        if hw_value and str(hw_value).strip() and str(hw_value) != "NOT FOUND":
            if "hardware" not in context["extracted_info"]:
                context["extracted_info"]["hardware"] = {}
            context["extracted_info"]["hardware"]["gpu_cpu"] = hw_value
