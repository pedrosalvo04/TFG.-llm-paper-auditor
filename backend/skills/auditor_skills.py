import json
import re
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.config import REDUCE_MODEL_NAME
from backend.common.prompt_engine import (
    get_extraction_prompt, 
    get_evaluation_prompt,
    get_verification_prompt,
    get_map_extraction_prompt,
    get_reduce_extraction_prompt,
    get_extraction_assistance_helps
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
            # 1. Fase MAP (Extracción Segmentada por Secciones)
            self.log_execution("🧠 [Fase MAP] Segmentando paper por secciones lógicas...")
            
            # Identificar secciones (líneas que empiezan con #) generadas por Docling
            # Usamos una expresión regular que busque el inicio de línea con #
            import re
            paper_text_norm = paper_text.replace('\r\n', '\n')
            sections = re.split(r'\n(?=#+ )', '\n' + paper_text_norm)
            sections = [s.strip() for s in sections if s.strip()]
            
            if len(sections) > 1:
                total_chars = sum(len(s) for s in sections)
                target = total_chars / 4
                fragments = []
                current_fragment = ""
                
                for section in sections:
                    # Si añadir la siguiente sección supera el objetivo y aún no tenemos 3 fragmentos
                    if len(current_fragment) + len(section) > target and len(fragments) < 3:
                        if current_fragment:
                            fragments.append(current_fragment)
                            current_fragment = section
                        else:
                            # Caso borde: una sola sección es gigante
                            fragments.append(section)
                            current_fragment = ""
                    else:
                        if current_fragment:
                            current_fragment += "\n\n" + section
                        else:
                            current_fragment = section
                            
                if current_fragment:
                    fragments.append(current_fragment)
                
                self.log_execution(f"📄 Paper dividido en {len(fragments)} secciones lógicas (basadas en Docling).")
            else:
                # Fallback: Chunks más manejables si no hay estructura de secciones clara
                self.log_execution("⚠️ No se detectaron secciones claras. Usando fallback de segmentación por caracteres.")
                splitter = RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=2000)
                fragments = splitter.split_text(paper_text)
                fragments = fragments[:4] # Forzar a 4 partes como pide el usuario
                self.log_execution(f"📄 Paper dividido en {len(fragments)} bloques (fallback).")
            
            map_results = []
            import time
            for i, fragment in enumerate(fragments):
                self.log_execution(f"⚙️ Procesando Bloque {i+1}...")
                prompt = get_map_extraction_prompt(fragment)
                
                try:
                    # Usar el método generate que ya tiene lógica de reintento para 503
                    response = self.llm_client.generate(prompt)
                    raw_text = response.text.strip()
                    
                    try:
                        fragment_data = self.parse_json_response(raw_text)
                        map_results.append(fragment_data)
                    except Exception as e:
                        self.log_execution(f"⚠️ Error parseando fragmento {i+1}: {str(e)}", level="warning")
                    
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

            try:
                extracted_info = self.parse_json_response(raw_text)
            except Exception as e:
                self.log_execution(f"❌ Error parseando consolidación final: {str(e)}", level="error")
                return {'extracted_info': {}, 'extraction_error': f"JSON parse error in REDUCE: {str(e)}"}
            
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


class NeurIPSComplianceSkill(BaseSkill):
    """Skill para evaluar el cumplimiento del checklist NeurIPS 2026 usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        extracted_info = context.get('extracted_info') or {}
        
        if not extracted_info:
            return {'evaluation': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'evaluation': {}}
        
        self.log_execution("📊 Evaluando reproducibilidad...")
        
        try:
            # Calcular ayudas (helps) para el evaluador basándose en la extracción de la Fase 1
            helps = get_extraction_assistance_helps(extracted_info)
            
            evaluation_prompt = get_evaluation_prompt(
                extracted_info
            )
            response = self.llm_client.generate(evaluation_prompt)
            raw_text = response.text.strip()
            try:
                evaluation = self.parse_json_response(raw_text)
            except Exception as e:
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
                'evaluation_helps': helps # Para visualización en el frontend
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
        metrics = {
            "tiempo_segundos": context.get('execution_time', 0),
            "caracteres_leidos": len(paper_text)
        }
        
        self.log_execution("✅ Métricas calculadas")
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
            "metricas": context.get('metrics', {}),
            "general_analysis_map": context.get('general_analysis_map', []),
            "general_analysis_reduce": context.get('general_analysis_reduce', {}),
            "hybrid_triage_fragments": context.get('hybrid_triage_fragments', []),
            "evaluation_helps": context.get('evaluation_helps', {})
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
            'experiment_statistical_significance', 'licenses', 'declaration_llm_usage',
            'code_of_ethics'
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
                try:
                    verification_result = self.parse_json_response(raw_text)
                except Exception as e:
                    self.log_execution(f"⚠️ Error parseando verificación de {item_key}: {str(e)}", level="warning")
                    continue
                
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
