import re
import time
import json
import os
from backend.common.llm_client import LLMClient
from backend.common.config import (
    EVALUATION_CONFIG,
    EVALUATION_MODEL_NAME
)
from backend.common.logger import get_logger

logger = get_logger(__name__)


class PaperAuditor:
    """Auditor de reproducibilidad en papers científicos usando arquitectura baseline (single-prompt)"""
    
    def __init__(self):
        """Inicializa el auditor con un solo cliente LLM y sin skills especializados"""
        self.evaluation_llm = LLMClient(model_name=EVALUATION_MODEL_NAME, generation_config=EVALUATION_CONFIG)
        logger.info(f"✅ Auditor baseline inicializado.")

    def _log_status(self, msg, phase_index=None, status_callback=None):
        """Reporta el progreso tanto al logger como al callback del frontend."""
        logger.info(msg)
        if status_callback:
            try:
                status_callback(msg, phase_index)
            except TypeError:
                status_callback(msg)

    def _read_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error leyendo archivo {filepath}: {e}")
            return ""

    def audit(self, paper_text, status_callback=None, criteria_mode="neurips", criteria_text=None):
        """
        Analiza el paper usando una única llamada masiva al LLM con todo el contexto.
        """
        caracteres = len(paper_text)
        self._log_status(f"🚀 Iniciando auditoría BASELINE (Single-Prompt). Tamaño: {caracteres} caracteres. Modo: {criteria_mode}", phase_index=0, status_callback=status_callback)
        start_time = time.time()
        
        try:
            # 1. Cargar contexto
            self._log_status("📑 Fase Única: Analizando el paper en una sola llamada masiva al LLM...", phase_index=1, status_callback=status_callback)
            
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            if criteria_mode == "neurips":
                neurips_criteria = self._read_file(os.path.join(base_dir, "criterios NeurIPS 2026.md"))
                ethics_code = self._read_file(os.path.join(base_dir, "code of ethics.md"))
            else:
                neurips_criteria = criteria_text or "No se proporcionaron criterios."
                ethics_code = "No aplica en modo libre."

            prompt = f"""
Eres un auditor experto, riguroso y objetivo de machine learning evaluando un paper científico.
Debes evaluar el paper contra los criterios provistos y el código de ética.

¡INSTRUCCIONES DE OBJETIVIDAD Y RIGOR!
Tu objetivo es ser un evaluador justo pero estricto. Evita el sesgo de confirmación (asumir que un paper famoso cumple con todo), pero tampoco penalices injustificadamente.
1. BASADO EN EVIDENCIA: Para responder "Yes", debes ser capaz de extraer una cita exacta ('evidence') del texto que demuestre el cumplimiento de forma inequívoca. Si la información no está o es muy ambigua, responde "No".
2. BÚSQUEDA EXHAUSTIVA: Los papers son largos. No asumas que algo falta solo porque no esté en su propia sección dedicada. Busca en apéndices y a lo largo de todo el texto. Solo responde "No" si, tras evaluar todo el contenido, la información requerida está verdaderamente ausente.
3. PRECISIÓN TÉCNICA: Para métricas, reproducibilidad e infraestructura, exige datos concretos (ej: enlaces reales a código, números exactos de GPUs/TPUs, hiperparámetros específicos). Menciones genéricas como "usamos muchas GPUs" no son suficientes y deben marcarse como "No".
4. EQUILIBRIO: Penaliza las omisiones metodológicas reales ("No"), pero reconoce y premia el cumplimiento cuando los autores proporcionan la información explícitamente ("Yes").

Devuelve tu análisis ÚNICAMENTE en formato JSON, asegurándote de usar las claves que se te indicarán al final del prompt.

Nota: Para 'answer', utiliza obligatoriamente "Yes", "No", o "N/A".
'is_no_justified' debe ser un booleano, true si la respuesta es No pero el autor lo ha justificado adecuadamente en el paper.
'evidence' debe ser un fragmento de texto extraído directamente del paper que demuestre el cumplimiento de este ítem (o guion "-" si no hay evidencia directa).
'justification' debe ser el razonamiento por el cual asignas esa respuesta (o la justificación dada por el autor en caso de responder 'No').

--- CRITERIOS A EVALUAR ---
{neurips_criteria}

--- CÓDIGO DE ÉTICA ---
{ethics_code}

--- PAPER A EVALUAR ---
{paper_text}

--- RECORDATORIO FINAL Y ESTRUCTURA JSON REQUERIDA ---
Tu tarea es auditar el paper anterior y responder **ÚNICAMENTE** con un objeto JSON válido que siga exactamente esta estructura (sin usar markdown, solo el JSON puro):
{{
  "claims": {{"answer": "Yes/No/N/A", "justification": "Razonamiento...", "evidence": "Cita del paper...", "is_no_justified": false}},
  "limitations": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "theory_assumptions_proofs": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "experimental_result_reproducibility": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "open_access_data_code": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "experimental_setting_details": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "experiment_statistical_significance": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "experiments_compute_resource": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "code_of_ethics": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "broader_impacts": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "safeguards": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "licenses": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "assets": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "crowdsourcing_human_subjects": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "irb_approvals": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "declaration_llm_usage": {{"answer": "Yes/No/N/A", "justification": "...", "evidence": "...", "is_no_justified": false}},
  "informacion_extraida": {{
      "hyperparameters": "...",
      "hardware": "...",
      "architecture": "...",
      "data": "...",
      "code": "...",
      "statistics": "...",
      "baseline_comparison": "...",
      "theory_and_proofs": "...",
      "software_versions": "...",
      "limitations_quality": "...",
      "licenses_extraction": "...",
      "broader_impacts_extraction": "...",
      "llm_usage_extraction": "...",
      "human_subjects_extraction": "...",
      "thought_process": "Escribe aquí tu proceso de pensamiento general.",
      "context_mapping": ["Seccion 1", "Seccion 2"]
  }}
}}
"""
            # 2. Llamada LLM
            response = self.evaluation_llm.generate(prompt)
            
            # 3. Procesar y limpiar respuesta
            self._log_status("📊 Procesando resultados y limpiando JSON...", phase_index=2, status_callback=status_callback)
            
            result_text = response.text.strip()
            
            # Limpiar posible markdown json backticks
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            elif result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            result_text = result_text.strip()
            
            try:
                final_result = json.loads(result_text)
            except json.JSONDecodeError as e:
                logger.error(f"Error parseando el JSON devuelto por el LLM: {e}")
                logger.error(f"Texto devuelto: {result_text[:500]}...")
                return {"error": "El LLM no devolvió un JSON válido. Revisa los logs para más detalles."}

            execution_time = round(time.time() - start_time, 2)
            
            # Añadir las métricas que el frontend espera
            final_result["metricas"] = {
                "tiempo_segundos": execution_time,
                "caracteres_leidos": caracteres
            }
            
            self._log_status(f"✅ Auditoría completada en {execution_time} segundos", phase_index=3, status_callback=status_callback)
            return final_result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ Error durante la auditoría tras {round(end_time - start_time, 2)}s: {str(e)}")
            return {"error": str(e)}

