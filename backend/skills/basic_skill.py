import json
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill
from backend.common.prompt_engine import get_basic_audit_prompt
from backend.common.neurips_criteria import NEURIPS_CRITERIA_LITERAL
import os

class SinglePromptSkill(BaseSkill):
    """Skill para ejecutar la auditoría completa en un solo prompt (Modo Básico)"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_context(context, ['paper_text']):
            return {'error': 'paper_text missing'}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'error': 'No LLM client'}
        
        self.log_execution("🔍 Iniciando Análisis Básico (Single Prompt)...")
        paper_text = context['paper_text']
        criteria_mode = context.get('criteria_mode', 'neurips')
        custom_criteria = context.get('custom_criteria', {})
        
        # Construir el texto de las reglas
        criteria_literal_list = []
        if criteria_mode == 'free' and custom_criteria:
            for item, desc in custom_criteria.items():
                criteria_literal_list.append(f"CRITERION '{item}': {desc}")
        else:
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
            for item in all_items:
                if item in NEURIPS_CRITERIA_LITERAL:
                    criteria_literal_list.append(NEURIPS_CRITERIA_LITERAL[item])
                
                # Inyectar el texto completo del Código de Ética si corresponde
                if item == "code_of_ethics":
                    ethics_path = os.path.join(os.path.dirname(__file__), '..', '..', 'code of ethics.md')
                    try:
                        with open(ethics_path, 'r', encoding='utf-8') as f:
                            ethics_text = f.read()
                            criteria_literal_list.append("--- NEURIPS FULL CODE OF ETHICS ---\n" + ethics_text)
                            self.log_execution("📜 Código de Ética completo añadido a las instrucciones.")
                    except Exception as e:
                        self.log_execution(f"⚠️ No se pudo leer 'code of ethics.md': {e}", level="warning")

        criteria_literal_text = "\n\n".join(criteria_literal_list)
        
        prompt = get_basic_audit_prompt(paper_text, criteria_mode, criteria_literal_text)
        
        try:
            self.log_execution(f"🧠 Enviando paper completo al modelo en un solo prompt...")
            # Usamos el método generate genérico
            response = self.llm_client.generate(prompt)
            raw_text = response.text.strip()
            
            try:
                result_json = self.parse_json_response(raw_text)
            except Exception as e:
                self.log_execution(f"❌ Error parseando la respuesta JSON: {str(e)}", level="error")
                return {'error': f"JSON parse error: {str(e)}"}
            
            # Verificar si se devolvió info de extracción
            extracted_info = result_json.get('extracted_info', {})
            if extracted_info.get('paper_type', '').startswith('INVALID'):
                self.log_execution("❌ Paper no válido: No es ML/AI", level="error")
                return {
                    'extracted_info': extracted_info,
                    'invalid_paper': True,
                    'invalid_reason': extracted_info.get('invalid_reason', 'Not ML/AI paper')
                }
            
            self.log_execution("✅ Análisis Básico completado exitosamente.")
            
            # Devolver el resultado de manera que BasicAuditor lo pueda recoger
            # Incluimos extracted_info y luego todos los ítems de evaluación
            return {
                'extracted_info': extracted_info,
                'evaluation': {k: v for k, v in result_json.items() if k != 'extracted_info'},
                'invalid_paper': False
            }
            
        except Exception as e:
            self.log_execution(f"❌ Error crítico en ejecución del prompt único: {str(e)}", level="error")
            return {'error': str(e)}
