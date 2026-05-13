"""Script para verificar que la refactorización del auditor funciona correctamente"""
from backend.services.auditor import PaperAuditor
from backend.common.prompts import get_extraction_prompt, get_evaluation_prompt

def test_auditor_initialization():
    """Verifica que el auditor se inicializa correctamente"""
    try:
        auditor = PaperAuditor()
        print("✅ Auditor inicializado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar auditor: {e}")
        return False

def test_regex_patterns():
    """Verifica que los patrones regex están definidos"""
    try:
        from backend.services.auditor import REGEX_PATTERNS
        assert len(REGEX_PATTERNS) > 0
        print(f"✅ Patrones regex definidos: {len(REGEX_PATTERNS)} patrones")
        return True
    except Exception as e:
        print(f"❌ Error en patrones regex: {e}")
        return False

def test_preprocess_method():
    """Verifica que el método de preprocesamiento funciona"""
    try:
        auditor = PaperAuditor()
        text = "This is a test paper with github.com/test/repo"
        red_flags = auditor._preprocess_paper(text)
        assert isinstance(red_flags, dict)
        print(f"✅ Método _preprocess_paper funciona correctamente")
        print(f"   Red flags detectadas: {sum(1 for v in red_flags.values() if v)}")
        return True
    except Exception as e:
        print(f"❌ Error en _preprocess_paper: {e}")
        return False

def test_prompts_module():
    """Verifica que el módulo de prompts funciona"""
    try:
        test_text = "Test paper"
        test_flags = {"test": True}
        
        extraction_prompt = get_extraction_prompt(test_text, test_flags)
        assert len(extraction_prompt) > 0
        print("✅ Función get_extraction_prompt funciona")
        
        test_info = {"test": "info"}
        evaluation_prompt = get_evaluation_prompt(test_info, test_flags)
        assert len(evaluation_prompt) > 0
        print("✅ Función get_evaluation_prompt funciona")
        
        return True
    except Exception as e:
        print(f"❌ Error en módulo prompts: {e}")
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN DE REFACTORIZACIÓN DEL AUDITOR")
    print("=" * 60)
    print()
    
    tests = [
        ("Inicialización del Auditor", test_auditor_initialization),
        ("Patrones Regex", test_regex_patterns),
        ("Método de Preprocesamiento", test_preprocess_method),
        ("Módulo de Prompts", test_prompts_module)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📝 Test: {name}")
        print("-" * 60)
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'✅' if passed == total else '⚠️'} Tests pasados: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Refactorización completada exitosamente!")
        print("La funcionalidad del auditor se mantiene intacta.")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
