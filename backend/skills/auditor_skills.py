<<<<<<< Updated upstream
"""Skills específicos para el auditor de papers - Versión refactorizada"""
=======
"""
Skills del pipeline de auditoría refactorizados con LLMOps best practices:

  1. Structured Outputs: todas las llamadas LLM usan `response_schema` de Pydantic.
     Elimina completamente el parsing manual con regex, json.loads() y el loop de
     stack de llaves `{`. La garantía de JSON válido la asume el proveedor del modelo.

  2. AuditState: el contexto entre skills es el dict nativo para compatibilidad
     con el frontend, pero las llamadas al LLM usan schemas Pydantic tipados.

  3. Sin time.sleep() manuales: los reintentos los gestiona tenacity en LLMClient.
"""
>>>>>>> Stashed changes
import json
from typing import Any, Dict

from backend.skills.base_skill import BaseSkill
<<<<<<< Updated upstream
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
=======
from backend.common.config import REDUCE_MODEL_NAME
from backend.common.schemas import (
    MapFragmentResult,
    ReduceExtractionResult,
    EvaluationResultSchema,
    VerificationResultSchema,
)
from backend.common.prompts import (
    get_evaluation_prompt,
    get_verification_prompt,
    get_map_extraction_prompt,
    get_reduce_extraction_prompt,
    get_evaluation_signals,
>>>>>>> Stashed changes
)


<<<<<<< Updated upstream
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


=======
>>>>>>> Stashed changes
class InformationExtractionSkill(BaseSkill):
    """
    Extrae información estructurada del paper mediante Map-Reduce.

    Fase MAP: divide el paper en fragmentos y extrae de cada uno usando
              MapFragmentResult como response_schema (Structured Output).
    Fase REDUCE: consolida todos los fragmentos con ReduceExtractionResult
                 como response_schema.

    Al usar response_schema, el proveedor garantiza JSON válido. No se necesita:
      - json.loads() con try/except
      - re.sub() para reparar comas
      - el loop de stack de llaves
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
<<<<<<< Updated upstream
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
            
=======
        if not self.validate_context(context, ["paper_text"]):
            return {"extracted_info": {}}

        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {"extracted_info": {}}

        self.log_execution("🔍 Iniciando Análisis General (Map-Reduce + Structured Outputs)...")
        paper_text = context["paper_text"]
        structural_chunks = context.get("structural_chunks", [])

        try:
            # ----------------------------------------------------------------
            # Fase MAP: Segmentación Estructural vs Aleatoria
            # ----------------------------------------------------------------
            if structural_chunks:
                self.log_execution("🧠 [Fase MAP] Usando Agrupación Estructural de Docling...")
                # Agrupamos chunks estructurales en batches de ~25k caracteres
                batches = self._group_structural_chunks(structural_chunks, target_size=25000)
                self.log_execution(f"📄 Paper organizado en {len(batches)} bloques lógicos (secciones/tablas).")
            else:
                self.log_execution("⚠️ [Fase MAP] Fallback: Segmentando paper por cantidad de caracteres...")
                splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
                batches = splitter.split_text(paper_text)[:5]
                self.log_execution(f"📄 Paper dividido en {len(batches)} bloques por caracteres.")

            map_results = []
            for i, fragment in enumerate(batches):
                self.log_execution(f"⚙️ Procesando Bloque {i + 1}/{len(batches)}...")
                prompt = get_map_extraction_prompt(fragment)
                try:
                    # Structured Output: response_schema garantiza JSON válido
                    response = self.llm_client.generate(
                        prompt, response_schema=MapFragmentResult
                    )
                    # Con Structured Outputs, response.text es JSON válido garantizado
                    fragment_data = json.loads(response.text)
                    map_results.append(fragment_data)
                except Exception as e:
                    self.log_execution(
                        f"⚠️ Error en fragmento {i + 1}: {str(e)}", level="warning"
                    )

            if not map_results:
                self.log_execution(
                    "❌ No se pudo extraer información de ningún fragmento.", level="error"
                )
                return {
                    "extracted_info": {},
                    "extraction_error": "Map phase produced no results",
                }

            # ----------------------------------------------------------------
            # Fase REDUCE
            # ----------------------------------------------------------------
            self.log_execution(
                f"🧠 [Fase REDUCE] Consolidando {len(map_results)} extracciones "
                f"con {REDUCE_MODEL_NAME}..."
            )
            reduce_prompt = get_reduce_extraction_prompt(map_results)

            # Structured Output: elimina toda la sanitización de JSON posterior
            response = self.llm_client.generate(
                reduce_prompt, response_schema=ReduceExtractionResult
            )
            extracted_info = json.loads(response.text)

>>>>>>> Stashed changes
            # Validar si el paper es ML/AI
            if extracted_info.get("paper_type", "").startswith("INVALID"):
                self.log_execution("❌ Paper no válido: No es ML/AI", level="error")
                return {
                    "extracted_info": extracted_info,
                    "invalid_paper": True,
                    "invalid_reason": extracted_info.get("invalid_reason", "Not ML/AI paper"),
                }
<<<<<<< Updated upstream
            
            self.log_execution("✅ Información extraída correctamente")
            return {'extracted_info': extracted_info, 'invalid_paper': False}
        except Exception as e:
            self.log_execution(f"❌ Error en extracción: {str(e)}", level="error")
            return {'extracted_info': {}, 'extraction_error': str(e)}
=======

            # Asegurar campos críticos (el schema ya los garantiza con defaults)
            if "thought_process" not in extracted_info:
                extracted_info["thought_process"] = "Resumen de consolidación no generado."
            if "context_mapping" not in extracted_info or not extracted_info["context_mapping"]:
                all_sections = []
                for m in map_results:
                    sections = m.get("context_mapping", [])
                    if isinstance(sections, list):
                        all_sections.extend(sections)
                extracted_info["context_mapping"] = (
                    list(set(all_sections)) if all_sections else ["General Context"]
                )

            self.log_execution("✅ Análisis general completado con Map-Reduce + Structured Outputs")
            return {
                "extracted_info": extracted_info,
                "invalid_paper": False,
                "map_steps": map_results,
                "reduce_step": extracted_info,
            }

        except Exception as e:
            self.log_execution(
                f"❌ Error crítico en extracción general Map-Reduce: {str(e)}", level="error"
            )
            return {"extracted_info": {}, "extraction_error": str(e)}

    def _group_structural_chunks(self, chunks: list, target_size: int = 25000) -> list[str]:
        """
        Agrupa los StructuralChunks de Docling en strings de tamaño óptimo.
        
        Garantiza que ninguna tabla o sección se corte a la mitad, 
        manteniendo la coherencia semántica en cada llamada al LLM.
        """
        batches = []
        current_batch = []
        current_size = 0
        
        for chunk in chunks:
            # Si el chunk ya es de por sí más grande que el target, lo añadimos solo
            chunk_text = getattr(chunk, 'content', str(chunk))
            chunk_len = len(chunk_text)
            
            if current_size + chunk_len > target_size and current_batch:
                # Flush del batch actual
                batches.append("\n\n---\n\n".join(current_batch))
                current_batch = []
                current_size = 0
            
            current_batch.append(chunk_text)
            current_size += chunk_len
            
        # Añadir el último batch si quedó algo
        if current_batch:
            batches.append("\n\n---\n\n".join(current_batch))
            
        return batches[:6] # Límite de 6 bloques para evitar costes infinitos y latencia alta

>>>>>>> Stashed changes


class ReproducibilityEvaluationSkill(BaseSkill):
    """
    Evalúa la reproducibilidad del paper según el checklist NeurIPS 2026.

    Usa EvaluationResultSchema como response_schema (Structured Output),
    lo que elimina el parsing manual y la reparación de JSON con regex.
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
<<<<<<< Updated upstream
        if not self.validate_context(context, ['extracted_info', 'red_flags']):
            return {'evaluation': {}}
        
=======
        extracted_info = context.get("extracted_info") or {}

        if not isinstance(extracted_info, dict):
            self.log_execution(
                f"⚠️ extracted_info no es un dict (es {type(extracted_info)}), ignorando.",
                level="warning",
            )
            extracted_info = {}

        if not extracted_info:
            return {"evaluation": {}}

>>>>>>> Stashed changes
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {"evaluation": {}}

        self.log_execution("📊 Evaluando reproducibilidad con Structured Outputs...")
        red_flags = context.get("red_flags", {})

        try:
<<<<<<< Updated upstream
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
=======
            signals = get_evaluation_signals(extracted_info)
            evaluation_prompt = get_evaluation_prompt(extracted_info, red_flags)

            # Structured Output: garantiza un JSON con los 16 ítems del checklist
            response = self.llm_client.generate(
                evaluation_prompt, response_schema=EvaluationResultSchema
            )
            evaluation = json.loads(response.text)

            # Normalizar: si el LLM devuelve una lista (caso raro), tomar el primer elemento
            if isinstance(evaluation, list):
                evaluation = evaluation[0] if evaluation else {}

            if not isinstance(evaluation, dict):
                self.log_execution(
                    f"⚠️ La evaluación no es un dict ({type(evaluation)}), reseteando.",
                    level="warning",
                )
                evaluation = {}

            self.log_execution("✅ Evaluación completada con Structured Outputs")
            return {
                "evaluation": evaluation,
                "evaluation_signals": signals,
            }

        except Exception as e:
            error_msg = str(e)
            self.log_execution(f"❌ Error en evaluación: {error_msg}", level="error")

            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                return {
                    "evaluation": {},
                    "evaluation_error": (
                        "El modelo LLM está experimentando alta demanda. "
                        "Intenta nuevamente en unos momentos."
                    ),
                }
            return {"evaluation": {}, "evaluation_error": error_msg}
>>>>>>> Stashed changes


class MetricsCalculationSkill(BaseSkill):
    """Skill para calcular métricas de la auditoría (sin LLM)."""

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
<<<<<<< Updated upstream
        if not self.validate_context(context, ['paper_text', 'red_flags']):
            return {'metrics': {}}
        
        self.log_execution("Calculando métricas...")
        
        paper_text = context['paper_text']
        red_flags = context['red_flags']
        
=======
        if not self.validate_context(context, ["paper_text"]):
            return {"metrics": {}}

        self.log_execution("Calculando métricas...")

        paper_text = context["paper_text"]
        red_flags = context.get("red_flags", {})

>>>>>>> Stashed changes
        critical_flags = [
            k
            for k, v in red_flags.items()
            if v
            and not k.startswith("tiene_")
            and not k.startswith("menciona_")
            and not k.startswith("_")
            and not k.startswith("cantidad_")
            and not k.startswith("puntos_")
        ]

        metrics = {
            "tiempo_segundos": context.get("execution_time", 0),
            "caracteres_leidos": len(paper_text),
            "red_flags_detectadas": len(critical_flags),
        }

        self.log_execution(f"✅ Métricas calculadas: {metrics['red_flags_detectadas']} red flags")
        return {"metrics": metrics}


class MetadataAggregationSkill(BaseSkill):
    """Agrega los resultados de todas las fases en el dict final del frontend."""

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['red_flags']):
            return {'error': 'Contexto inválido'}
        
        self.log_execution("Agregando metadatos y construyendo resultado final...")

        evaluation = context.get("evaluation", {})

        result = {
<<<<<<< Updated upstream
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
=======
            "claims": evaluation.get("claims", {}),
            "limitations": evaluation.get("limitations", {}),
            "theory_assumptions_proofs": evaluation.get("theory_assumptions_proofs", {}),
            "experimental_result_reproducibility": evaluation.get(
                "experimental_result_reproducibility", {}
            ),
            "open_access_data_code": evaluation.get("open_access_data_code", {}),
            "experimental_setting_details": evaluation.get("experimental_setting_details", {}),
            "experiment_statistical_significance": evaluation.get(
                "experiment_statistical_significance", {}
            ),
            "experiments_compute_resource": evaluation.get("experiments_compute_resource", {}),
            "code_of_ethics": evaluation.get("code_of_ethics", {}),
            "broader_impacts": evaluation.get("broader_impacts", {}),
            "safeguards": evaluation.get("safeguards", {}),
            "licenses": evaluation.get("licenses", {}),
            "assets": evaluation.get("assets", {}),
            "crowdsourcing_human_subjects": evaluation.get("crowdsourcing_human_subjects", {}),
            "irb_approvals": evaluation.get("irb_approvals", {}),
            "declaration_llm_usage": evaluation.get("declaration_llm_usage", {}),
            "informacion_extraida": context.get("extracted_info", {}),
            "red_flags": context.get("red_flags", {}),
            "metricas": context.get("metrics", {}),
            "general_analysis_map": context.get("general_analysis_map", []),
            "general_analysis_reduce": context.get("general_analysis_reduce", {}),
            "hybrid_triage_fragments": context.get("hybrid_triage_fragments", []),
            "evaluation_signals": context.get("evaluation_signals", {}),
>>>>>>> Stashed changes
        }

        self.log_execution("✅ Resultado final construido correctamente")
        return result
<<<<<<< Updated upstream
=======


class ChecklistVerificationSkill(BaseSkill):
    """
    Auditoría Estricta (Self-Correction / Auditor 2).

    Revisa los ítems críticos del checklist para detectar falsos positivos
    y falsos negativos. Usa VerificationResultSchema como Structured Output,
    eliminando el parsing manual con json.loads() + regex.
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        evaluation = context.get("evaluation") or {}
        paper_text = context.get("paper_text") or ""

        if not isinstance(evaluation, dict):
            self.log_execution(
                f"⚠️ evaluation no es un dict (es {type(evaluation)}), ignorando.",
                level="warning",
            )
            evaluation = {}

        if not evaluation:
            self.log_execution(
                "⚠️ No hay datos de evaluación para verificar.", level="warning"
            )
            return {"evaluation": {}}

        # Ítems prioritarios (técnicos y críticos)
        priority_items = [
            "claims",
            "experimental_result_reproducibility",
            "open_access_data_code",
            "experimental_setting_details",
            "experiments_compute_resource",
            "experiment_statistical_significance",
            "licenses",
            "declaration_llm_usage",
        ]

        to_check = [
            item
            for item in priority_items
            if item in evaluation and isinstance(evaluation[item], dict)
        ]

        # Completar hasta 8 ítems con negativos no prioritarios
        if len(to_check) < 8:
            other_negatives = [
                k
                for k, v in evaluation.items()
                if k not in to_check
                and isinstance(v, dict)
                and v.get("answer") in ["No", "N/A"]
            ]
            to_check.extend(other_negatives[: (8 - len(to_check))])

        self.log_execution(
            f"🔍 Iniciando Auditoría Estricta sobre {len(to_check)} ítems clave..."
        )

        corrections_made = 0

        for item_key in to_check:
            item_data = evaluation[item_key]
            status_type = (
                "Verificación de cumplimiento"
                if item_data.get("answer") == "Yes"
                else "Búsqueda de omisión"
            )
            self.log_execution(
                f"🛡️ {status_type}: {item_key} (Inicial: {item_data.get('answer')})"
            )

            # Contexto amplio (60k chars)
            context_snippet = paper_text[:30000] + "\n[...]\n" + paper_text[-30000:]
            prompt = get_verification_prompt(item_key, item_data, context_snippet)

            try:
                # Structured Output: elimina json.loads() + strip de markdown
                response = self.llm_client.generate(
                    prompt, response_schema=VerificationResultSchema
                )
                verification_result = json.loads(response.text)

                if verification_result.get("was_corrected", False):
                    self.log_execution(
                        f"✨ ¡CAMBIO DETECTADO! {item_key}: "
                        f"{item_data.get('answer')} → {verification_result.get('answer')}"
                    )
                    corrections_made += 1

                # Actualizar siempre para beneficiarse del refinamiento de justificación
                evaluation[item_key] = {
                    "answer": verification_result.get("answer"),
                    "evidence": verification_result.get("evidence"),
                    "justification": verification_result.get("justification"),
                    "is_no_justified": verification_result.get("is_no_justified", False),
                    "verified": True,
                    "was_refined": not verification_result.get("was_corrected", False),
                }

            except Exception as e:
                self.log_execution(
                    f"⚠️ Error verificando {item_key}: {str(e)}", level="warning"
                )

        self.log_execution(
            f"✅ Auditoría Estricta finalizada. Cambios de estado: {corrections_made}"
        )
        return {"evaluation": evaluation}
>>>>>>> Stashed changes
