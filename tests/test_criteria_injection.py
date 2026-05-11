import sys
import os
import json

# Añadir el path raíz para importar módulos del backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.common.neurips_criteria import NEURIPS_CRITERIA_LITERAL
from backend.common.prompt_engine import get_evaluation_high_context_prompt

def test_criteria_completeness():
    """Verifica que el diccionario de criterios contiene los 16 ítems."""
    expected_count = 16
    actual_count = len(NEURIPS_CRITERIA_LITERAL)
    
    print(f"Verificando integridad de NEURIPS_CRITERIA_LITERAL...")
    if actual_count == expected_count:
        print(f"PASS: Se encontraron los {expected_count} ítems esperados.")
        return True
    else:
        print(f"FAIL: Se esperaban {expected_count} ítems, pero se encontraron {actual_count}.")
        return False

def test_prompt_rendering_with_criteria():
    """Verifica que el prompt de alto contexto renderiza correctamente el texto literal de los criterios."""
    test_info = {"paper_type": "AI"}
    test_items = ["claims", "limitations"]
    test_mapped_text = "=== Abstract ===\nThis paper claims..."
    
    # Extraer criterios de prueba
    test_criteria_list = [NEURIPS_CRITERIA_LITERAL[item] for item in test_items]
    test_criteria_text = "\n\n".join(test_criteria_list)
    
    print(f"Verificando renderizado del prompt con criterios literales...")
    
    prompt = get_evaluation_high_context_prompt(
        extracted_info=test_info,
        items_to_evaluate=test_items,
        mapped_sections_text=test_mapped_text,
        criteria_literal_text=test_criteria_text
    )
    
    # Verificar que el marcador de posición se ha reemplazado
    if "{criteria_literal_text}" in prompt:
        print(f"FAIL: El marcador {{criteria_literal_text}} no fue reemplazado en el prompt.")
        return False
    
    # Verificar que el contenido de los criterios está presente
    for item_key in test_items:
        literal = NEURIPS_CRITERIA_LITERAL[item_key]
        # Verificar solo el inicio del literal para ser robustos ante cambios de formato
        if literal[:50] not in prompt:
            print(f"FAIL: No se encontró la descripción literal de '{item_key}' en el prompt.")
            return False
            
    print(f"PASS: El prompt contiene los criterios literales inyectados correctamente.")
    return True

def test_auditor_skill_logic():
    """Simula la lógica de NeurIPSComplianceSkill para verificar la agrupación y extracción."""
    all_items = list(NEURIPS_CRITERIA_LITERAL.keys())
    groups = [all_items[i:i + 2] for i in range(0, len(all_items), 2)]
    
    print(f"Verificando lógica de agrupación de items en NeurIPSComplianceSkill...")
    
    if len(groups) != 8:
        print(f"FAIL: Se esperaban 8 grupos de 2, pero se obtuvieron {len(groups)}.")
        return False
        
    for i, group in enumerate(groups):
        criteria_list = []
        for item in group:
            if item in NEURIPS_CRITERIA_LITERAL:
                criteria_list.append(NEURIPS_CRITERIA_LITERAL[item])
        
        if len(criteria_list) != 2:
            print(f"FAIL: Error en Grupo {i+1}: Se esperaban 2 criterios, se obtuvieron {len(criteria_list)}.")
            return False
            
    print(f"PASS: Lógica de agrupación y extracción de criterios validada para los 16 ítems.")
    return True

def main():
    print("=" * 60)
    print("TEST DE INYECCION DE CRITERIOS LITERALES NEURIPS")
    print("=" * 60)
    
    tests = [
        ("Integridad del diccionario de criterios", test_criteria_completeness),
        ("Renderizado de prompt con criterios", test_prompt_rendering_with_criteria),
        ("Logica de agrupacion de la Skill", test_auditor_skill_logic)
    ]
    
    results = []
    for name, func in tests:
        print(f"\n[RUNNING]: {name}")
        success = func()
        results.append((name, success))
        
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} - {name}")
        
    total_passed = sum(1 for _, s in results if s)
    if total_passed == len(tests):
        print("\nAll tests passed successfully.")
        sys.exit(0)
    else:
        print(f"\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
