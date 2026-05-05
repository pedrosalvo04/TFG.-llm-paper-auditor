"""Skills específicos para el auditor de papers - Versión refactorizada"""
import json
import re
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.prompts import get_extraction_prompt, get_evaluation_prompt



class InformationExtractionSkill(BaseSkill):
    """Skill para extraer información estructurada del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'extracted_info': {}}
        
        red_flags = context.get('red_flags', {})
        
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
            raw_text = response.text.strip()
            # Limpiar posibles backticks de markdown si el modelo los añade
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\n?|```$', '', raw_text, flags=re.MULTILINE).strip()
                
            try:
                extracted_info = json.loads(raw_text)
            except json.JSONDecodeError as e:
                # Intento básico de reparación (comas al final)
                fixed_text = re.sub(r',\s*([\]}])', r'\1', raw_text)
                try:
                    extracted_info = json.loads(fixed_text)
                    self.log_execution("⚠️ JSON reparado automáticamente (comas extra eliminadas).")
                except:
                    self.log_execution(f"❌ Error parseando JSON: {str(e)}", level="error")
                    return {'extracted_info': {}, 'invalid_paper': False, 'extraction_error': str(e)}
            
            # Si el modelo devuelve una lista, tomamos el primer elemento (aunque no debería)
            if isinstance(extracted_info, list):
                extracted_info = extracted_info[0] if extracted_info else {}
            
            # Validar si el paper es ML/AI
            if extracted_info.get('paper_type', '').startswith('INVALID'):
                self.log_execution("❌ Paper no válido: No es ML/AI", level="error")
                return {
                    'extracted_info': extracted_info,
                    'invalid_paper': True,
                    'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')
                }
            
            self.log_execution("✅ Información extraída correctamente")
            return {'extracted_info': extracted_info, 'invalid_paper': False}
        except Exception as e:
            self.log_execution(f"❌ Error en extracción general: {str(e)}", level="error")
            return {'extracted_info': {}, 'extraction_error': str(e)}


class ReproducibilityEvaluationSkill(BaseSkill):
    """Skill para evaluar la reproducibilidad del paper usando LLM"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['extracted_info']):
            return {'evaluation': {}}
        
        red_flags = context.get('red_flags', {})
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'evaluation': {}}
        
        self.log_execution("📊 Evaluando reproducibilidad...")
        
        try:
            evaluation_prompt = get_evaluation_prompt(
                context['extracted_info'], 
                context['red_flags']
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
            self.log_execution("✅ Evaluación completada")
            return {'evaluation': evaluation}
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
            "metricas": context.get('metrics', {})
        }
        
        self.log_execution("✅ Resultado final construido correctamente")
        return result
