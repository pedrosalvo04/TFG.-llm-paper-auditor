import json
import re
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.config import REDUCE_MODEL_NAME
from backend.common.prompts import (
    get_extraction_prompt, 
    get_evaluation_prompt,
    get_verification_prompt,
    get_map_extraction_prompt,
    get_reduce_extraction_prompt,
    get_evaluation_signals
)
from langchain_text_splitters import RecursiveCharacterTextSplitter



class InformationExtractionSkill(BaseSkill):
    """Skill para extraer información estructurada del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'extracted_info': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'extracted_info': {}}
        
        self.log_execution("🔍 Iniciando Análisis General (Map-Reduce + CoT + Context Mapping)...")
        paper_text = context['paper_text']
        
        try:
            # 1. Fase MAP (Extracción Segmentada)
            self.log_execution("🧠 [Fase MAP] Segmentando paper en bloques...")
            # Chunks más manejables para asegurar que el modelo no se pierda y respete el JSON
            splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
            fragments = splitter.split_text(paper_text)
            
            # Ampliamos a 5 bloques para mayor cobertura (100k caracteres aprox)
            fragments = fragments[:5]
            self.log_execution(f"📄 Paper dividido en {len(fragments)} bloques para análisis profundo.")
            
            map_results = []
            import time
            for i, fragment in enumerate(fragments):
                self.log_execution(f"⚙️ Procesando Bloque {i+1}...")
                prompt = get_map_extraction_prompt(fragment)
                
                try:
                    # Usar el método generate que ya tiene lógica de reintento para 503
                    response = self.llm_client.generate(prompt)
                    raw_text = response.text.strip()
                    
                    # Extracción balanceada de JSON (evita el error "Extra data")
                    start_idx = raw_text.find('{')
                    if start_idx != -1:
                        stack = 0
                        for i_char in range(start_idx, len(raw_text)):
                            if raw_text[i_char] == '{': stack += 1
                            elif raw_text[i_char] == '}':
                                stack -= 1
                                if stack == 0:
                                    raw_text = raw_text[start_idx:i_char+1]
                                    break
                    
                    fragment_data = json.loads(raw_text)
                    map_results.append(fragment_data)
                    
                    # Pequeña pausa para no saturar la cuota RPM
                    if i < len(fragments) - 1:
                        time.sleep(2)
                except Exception as e:
                    self.log_execution(f"⚠️ Error en fragmento {i+1}: {str(e)}", level="warning")
            
            if not map_results:
                self.log_execution("❌ No se pudo extraer información de ningún fragmento.", level="error")
                return {'extracted_info': {}, 'extraction_error': "Map phase produced no results"}

            # 2. Fase REDUCE (Consolidación)
            self.log_execution(f"🧠 [Fase REDUCE] Consolidando {len(map_results)} extracciones con {REDUCE_MODEL_NAME}...")

            reduce_prompt = get_reduce_extraction_prompt(map_results)
            
            try:
                # Usar el método generate para reintentos automáticos
                response = self.llm_client.generate(reduce_prompt)
                raw_text = response.text.strip()
            except Exception as e:
                self.log_execution(f"⚠️ Error en fase REDUCE: {str(e)}. Reintentando...", level="warning")
                # Fallback manual con configuración JSON si falla el general
                response = self.llm_client.client.models.generate_content(
                    model=REDUCE_MODEL_NAME,
                    contents=reduce_prompt,
                    config={"response_mime_type": "application/json", "temperature": 0.0}
                )
                raw_text = response.text.strip()

            # Extracción balanceada de JSON final
            start_idx = raw_text.find('{')
            if start_idx != -1:
                stack = 0
                for i in range(start_idx, len(raw_text)):
                    if raw_text[i] == '{': stack += 1
                    elif raw_text[i] == '}':
                        stack -= 1
                        if stack == 0:
                            raw_text = raw_text[start_idx:i+1]
                            break
                
            try:
                extracted_info = json.loads(raw_text)
            except json.JSONDecodeError as e:
                # Intento básico de reparación
                fixed_text = re.sub(r',\s*([\]}])', r'\1', raw_text)
                extracted_info = json.loads(fixed_text)
            
            # Validar si el paper es ML/AI
            if extracted_info.get('paper_type', '').startswith('INVALID'):
                self.log_execution("❌ Paper no válido: No es ML/AI", level="error")
                return {
                    'extracted_info': extracted_info,
                    'invalid_paper': True,
                    'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')
                }
            
            # Asegurar que campos críticos existan para el frontend
            if 'thought_process' not in extracted_info:
                extracted_info['thought_process'] = "Resumen de consolidación no generado por el modelo."
            if 'context_mapping' not in extracted_info:
                # Reconstrucción manual si el modelo falló pero tenemos los MAP
                all_sections = []
                for m in map_results:
                    sections = m.get('context_mapping', [])
                    if isinstance(sections, list):
                        all_sections.extend(sections)
                extracted_info['context_mapping'] = list(set(all_sections)) if all_sections else ["General Context"]

            self.log_execution("✅ Análisis general completado con Map-Reduce")
            return {
                'extracted_info': extracted_info, 
                'invalid_paper': False,
                'map_steps': map_results,
                'reduce_step': extracted_info
            }
        except Exception as e:
            self.log_execution(f"❌ Error crítico en extracción general Map-Reduce: {str(e)}", level="error")
            return {'extracted_info': {}, 'extraction_error': str(e)}


class ReproducibilityEvaluationSkill(BaseSkill):
    """Skill para evaluar la reproducibilidad del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        extracted_info = context.get('extracted_info') or {}
        
        # Asegurar que extracted_info es un diccionario
        if not isinstance(extracted_info, dict):
            self.log_execution(f"⚠️ extracted_info no es un diccionario (es {type(extracted_info)}), ignorando.", level="warning")
            extracted_info = {}
            
        if not extracted_info:
            return {'evaluation': {}}
        
        red_flags = context.get('red_flags', {})
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'evaluation': {}}
        
        self.log_execution("📊 Evaluando reproducibilidad...")
        
        try:
            # Calcular señales para el frontend y para el prompt
            signals = get_evaluation_signals(extracted_info)
            
            evaluation_prompt = get_evaluation_prompt(
                extracted_info, 
                red_flags
            )
            response = self.llm_client.generate(evaluation_prompt)
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()
                
            try:
                evaluation = json.loads(raw_text)
            except json.JSONDecodeError as e:
                fixed_text = re.sub(r',\s*([\]}])', r'\1', raw_text)
                try:
                    evaluation = json.loads(fixed_text)
                    self.log_execution("⚠️ JSON de evaluación reparado automáticamente.")
                except Exception as ex:
                    self.log_execution(f"❌ Error parseando JSON de evaluación: {str(e)}", level="error")
                    return {'evaluation': {}, 'evaluation_error': f'JSON parse error: {str(e)}'}
            
            if isinstance(evaluation, list):
                evaluation = evaluation[0] if evaluation else {}
            
            # Asegurar que evaluation es un diccionario (por si acaso el LLM devolvió algo raro)
            if not isinstance(evaluation, dict):
                self.log_execution(f"⚠️ La evaluación no es un diccionario ({type(evaluation)}), reseteando.", level="warning")
                evaluation = {}

            self.log_execution("✅ Evaluación completada")
            return {
                'evaluation': evaluation,
                'evaluation_signals': signals # Para visualización en el frontend
            }
        except Exception as e:
            error_msg = str(e)
            self.log_execution(f"❌ Error general en evaluación: {error_msg}", level="error")
            
            if '503' in error_msg or 'UNAVAILABLE' in error_msg:
                return {'evaluation': {}, 'evaluation_error': 'El modelo LLM está experimentando alta demanda. Intenta nuevamente en unos momentos.'}
            
            return {'evaluation': {}, 'evaluation_error': error_msg}


class MetricsCalculationSkill(BaseSkill):
    """Skill para calcular métricas de la auditoría"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'metrics': {}}
        
        self.log_execution("Calculando métricas...")
        
        paper_text = context['paper_text']
        red_flags = context.get('red_flags', {})
        
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
            "red_flags": context.get('red_flags', {}),
            "metricas": context.get('metrics', {}),
            "general_analysis_map": context.get('general_analysis_map', []),
            "general_analysis_reduce": context.get('general_analysis_reduce', {}),
            "hybrid_triage_fragments": context.get('hybrid_triage_fragments', []),
            "evaluation_signals": context.get('evaluation_signals', {})
        }
        
        self.log_execution("✅ Resultado final construido correctamente")
        return result

class ChecklistVerificationSkill(BaseSkill):
    """
    Skill de Auditoría Estricta (Self-Correction).
    Revisa los ítems críticos (Yes/No/N/A) para detectar falsos positivos y falsos negativos.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        evaluation = context.get('evaluation') or {}
        paper_text = context.get('paper_text') or ''
        
        # Asegurar que evaluation es un diccionario
        if not isinstance(evaluation, dict):
            self.log_execution(f"⚠️ evaluation no es un diccionario (es {type(evaluation)}), ignorando.", level="warning")
            evaluation = {}
            
        if not evaluation:
            self.log_execution("⚠️ No hay datos de evaluación para verificar.", level="warning")
            return {'evaluation': {}}
        
        # Seleccionar ítems para verificación
        # Damos prioridad a los ítems técnicos críticos independientemente de su respuesta inicial
        priority_items = [
            'claims', 'experimental_result_reproducibility', 'open_access_data_code', 
            'experimental_setting_details', 'experiments_compute_resource',
            'experiment_statistical_significance', 'licenses', 'declaration_llm_usage'
        ]
        
        # Filtramos solo los que existen en la evaluación y son diccionarios
        to_check = [item for item in priority_items if item in evaluation and isinstance(evaluation[item], dict)]

        
        # Si sobran huecos, añadimos los que tengan respuestas negativas que no estén en la lista de prioridad
        if len(to_check) < 8:
            other_negatives = [
                k for k, v in evaluation.items() 
                if k not in to_check and isinstance(v, dict) and v.get('answer') in ['No', 'N/A']
            ]
            to_check.extend(other_negatives[:(8 - len(to_check))])
            
        self.log_execution(f"🔍 Iniciando Auditoría Estricta Universal sobre {len(to_check)} ítems clave...")
        
        corrections_made = 0
        
        for item_key in to_check:
            item_data = evaluation[item_key]
            status_type = "Verificación de cumplimiento" if item_data.get('answer') == 'Yes' else "Búsqueda de omisión"
            self.log_execution(f"🛡️ {status_type}: {item_key} (Inicial: {item_data.get('answer')})")
            
            # Contexto amplio (60k chars totales)
            context_snippet = paper_text[:30000] + "\n[...]\n" + paper_text[-30000:]
            
            prompt = get_verification_prompt(item_key, item_data, context_snippet)
            
            try:
                response = self.llm_client.generate(prompt)
                raw_text = response.text.strip()
                if raw_text.startswith("```"):
                    raw_text = re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()
                
                verification_result = json.loads(raw_text)
                
                # Actualizar si hay corrección O si la nueva justificación es más técnica/detallada
                if verification_result.get('was_corrected', False):
                    self.log_execution(f"✨ ¡CAMBIO DETECTADO! {item_key}: {item_data.get('answer')} -> {verification_result.get('answer')}")
                    corrections_made += 1
                
                # Siempre actualizamos para beneficiarnos del refinamiento de la justificación y evidencia
                evaluation[item_key] = {
                    "answer": verification_result.get('answer'),
                    "evidence": verification_result.get('evidence'),
                    "justification": verification_result.get('justification'),
                    "is_no_justified": verification_result.get('is_no_justified', False),
                    "verified": True,
                    "was_refined": not verification_result.get('was_corrected', False)
                }
                    
            except Exception as e:
                self.log_execution(f"⚠️ Error verificando {item_key}: {str(e)}", level="warning")
                
        self.log_execution(f"✅ Auditoría Estricta finalizada. Cambios de estado: {corrections_made}")
        return {'evaluation': evaluation}
