import json
import re
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.config import REDUCE_MODEL_NAME
from backend.common.prompt_engine import (
    get_extraction_prompt, 
    get_section_mapping_prompt,
    get_evaluation_high_context_prompt,
    get_map_extraction_prompt,
    get_reduce_extraction_prompt,
    get_extraction_assistance_helps
)
from backend.common.neurips_criteria import NEURIPS_CRITERIA_LITERAL
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
            
            # NUEVO: Guardar las secciones como diccionario para la Fase 1.5
            paper_sections_dict = {}
            for s in sections:
                lines = s.split('\n')
                if lines:
                    title = lines[0].strip()
                    # El contenido es todo lo que hay DESPUÉS de la primera línea (el título)
                    content = '\n'.join(lines[1:]).strip()
                    
                    if not title.startswith('#'):
                        # Si no hay un encabezado claro (ej. primer fragmento sin #), le asignamos uno por defecto
                        # y el contenido es el bloque entero
                        title = "General Context / Abstract"
                        content = s.strip()
                    
                    # Manejar posibles títulos duplicados (ej. varios "Conclusion" en distintas partes)
                    if title in paper_sections_dict:
                        paper_sections_dict[title] += "\n\n" + content
                    else:
                        paper_sections_dict[title] = content
            context['paper_sections'] = paper_sections_dict

            
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


class SectionMappingSkill(BaseSkill):
    """Skill para mapear los títulos de docling a los items de alto contexto."""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        paper_sections_dict = context.get('paper_sections', {})
        if not paper_sections_dict:
            self.log_execution("No hay secciones detectadas para mapear.", level="warning")
            return {'section_mapping': {}}
            
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado para SectionMappingSkill", level="error")
            return {'section_mapping': {}}
            
        self.log_execution("🗺️ [Fase 1.5] Mapeando títulos de Docling con items de alto contexto...")
        
        section_titles = list(paper_sections_dict.keys())
        prompt = get_section_mapping_prompt(section_titles)
        
        try:
            response = self.llm_client.generate(prompt)
            raw_text = response.text.strip()
            
            try:
                mapping = self.parse_json_response(raw_text)
                self.log_execution("✅ Mapeo de secciones completado")
                return {'section_mapping': mapping}
            except Exception as e:
                self.log_execution(f"❌ Error parseando JSON de mapeo: {str(e)}", level="error")
                return {'section_mapping': {}}
                
        except Exception as e:
            self.log_execution(f"❌ Error general en mapeo: {str(e)}", level="error")
            return {'section_mapping': {}}

class NeurIPSComplianceSkill(BaseSkill):
    """Skill para evaluar el cumplimiento del checklist NeurIPS 2026 usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        extracted_info = context.get('extracted_info') or {}
        section_mapping = context.get('section_mapping') or {}
        paper_sections = context.get('paper_sections') or {}
        
        if not extracted_info:
            return {'evaluation': {}}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'evaluation': {}}
            
        final_evaluation = {}
        helps = get_extraction_assistance_helps(extracted_info)
        
        # EVALUACIÓN HIGH CONTEXT EN PAREJAS (16 Items)
        all_items = [
            'claims', 'limitations', 
            'theory_assumptions_proofs', 'experimental_result_reproducibility',
            'open_access_data_code', 'experimental_setting_details',
            'experiment_statistical_significance', 'experiments_compute_resource',
            'code_of_ethics', 'broader_impacts',
            'safeguards', 'licenses',
            'assets', 'crowdsourcing_human_subjects',
            'irb_approvals', 'declaration_llm_usage'
        ]
        
        groups = [all_items[i:i + 2] for i in range(0, len(all_items), 2)]
        
        for i, group in enumerate(groups):
            self.log_execution(f"📊 Evaluando grupo {i+1}/{len(groups)} de items en alto contexto...")
            
            # Recopilar secciones relevantes sin duplicados
            relevant_titles = set()
            for item in group:
                titles = section_mapping.get(item, [])
                if isinstance(titles, list):
                    relevant_titles.update(titles)
            
            # Construir texto inyectado
            injected_text = ""
            for title in relevant_titles:
                if title in paper_sections:
                    injected_text += f"\n\n=== {title} ===\n{paper_sections[title]}"
            
            if not injected_text.strip():
                injected_text = "No se encontraron secciones específicas mapeadas para estos items. Revisa el resumen general."
                
            # Extraer textos literales de NeurIPS para los items a evaluar
            criteria_literal_list = []
            for item in group:
                if item in NEURIPS_CRITERIA_LITERAL:
                    criteria_literal_list.append(NEURIPS_CRITERIA_LITERAL[item])
                
                # Inyectar el texto completo del Código de Ética si corresponde
                if item == "code_of_ethics":
                    import os
                    ethics_path = os.path.join(os.path.dirname(__file__), '..', '..', 'code of ethics.md')
                    try:
                        with open(ethics_path, 'r', encoding='utf-8') as f:
                            ethics_text = f.read()
                            criteria_literal_list.append("--- NEURIPS FULL CODE OF ETHICS ---\n" + ethics_text)
                            self.log_execution("📜 Código de Ética completo inyectado en el prompt.")
                    except Exception as e:
                        self.log_execution(f"⚠️ No se pudo leer 'code of ethics.md': {e}", level="warning")
            
            criteria_literal_text = "\n\n".join(criteria_literal_list)
            
            self.log_execution(f"🔍 Items {group}: Inyectando {len(criteria_literal_list)} descripciones literales de NeurIPS.")
                
            prompt = get_evaluation_high_context_prompt(extracted_info, group, injected_text, criteria_literal_text)
            try:
                response = self.llm_client.generate(prompt)
                raw_text = response.text.strip()
                group_eval = self.parse_json_response(raw_text)
                
                # Normalización robusta para grupos
                normalized = {}
                if isinstance(group_eval, dict):
                    # Verificar si las claves del grupo están en el primer nivel
                    if any(k in group_eval for k in group):
                        normalized = group_eval
                    else:
                        # Buscar en niveles anidados
                        for val in group_eval.values():
                            if isinstance(val, dict) and any(k in val for k in group):
                                normalized = val
                                break
                elif isinstance(group_eval, list):
                    for item in group_eval:
                        if isinstance(item, dict):
                            # Si es un dict con claves de items
                            if any(k in item for k in group):
                                normalized.update(item)
                            # Si es un dict tipo {"item": "claims", "answer": "Yes"}
                            elif "item" in item and item["item"] in group:
                                normalized[item["item"]] = item
                
                if normalized:
                    final_evaluation.update(normalized)
                    self.log_execution(f"✅ Grupo {i+1} completado: {len(normalized)} ítems recuperados.")
                else:
                    self.log_execution(f"⚠️ Grupo {i+1} no devolvió ítems válidos en el formato esperado.", level="warning")
                    self.log_execution(f"🔍 Raw LLM Output (Grupo {i+1}): {raw_text[:500]}...", level="warning")
            except Exception as e:
                self.log_execution(f"❌ Error en evaluación grupo {i+1}: {str(e)}", level="error")

        self.log_execution("✅ Evaluación completada")
        return {
            'evaluation': final_evaluation,
            'evaluation_helps': helps # Para visualización en el frontend
        }

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


