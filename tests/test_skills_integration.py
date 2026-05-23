"""Script de prueba para la integración de skills"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("=" * 70)
print("TEST DE INTEGRACIÓN - ARQUITECTURA BASADA EN SKILLS")
print("=" * 70)

# Test 1: Importar módulos
print("\n1. Probando importaciones...")
try:
    from backend.skills import (
        BaseSkill,
        InformationExtractionSkill,
        NeurIPSComplianceSkill,
        MetricsCalculationSkill,
        MetadataAggregationSkill,
        ThematicCoverageSkill,
        QueryGenerationSkill,
        SemanticScholarSearchSkill,
        CoverageGapAnalysisSkill,
        CrossValidationSkill
    )
    # Importar skills de detección por regex
    from backend.skills.regex_detection_skills import (
        LimitationsQualityDetectionSkill,
        SoftwareVersionDetectionSkill,
        HardwareDetailDetectionSkill
    )
    print("   [OK] Todas las importaciones de skills exitosas")
except Exception as e:
    print(f"   [ERROR] Error en importaciones: {e}")
    sys.exit(1)

# Test 2: Importar servicios refactorizados
print("\n2. Probando servicios refactorizados...")
try:
    from backend.services.auditor import PaperAuditor
    from backend.services.sota_analyzer import SotaAnalyzer
    print("   [OK] Importaciones de servicios exitosas")
except Exception as e:
    print(f"   [ERROR] Error importando servicios: {e}")
    sys.exit(1)

# Test 3: Inicializar servicios
print("\n3. Inicializando servicios...")
try:
    auditor = PaperAuditor()
    print("   [OK] PaperAuditor inicializado con skills")
    
    sota = SotaAnalyzer()
    print("   [OK] SotaAnalyzer inicializado con skills")
except Exception as e:
    print(f"   [ERROR] Error inicializando servicios: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Verificar estructura de skills en PaperAuditor
print("\n4. Verificando estructura de PaperAuditor...")
try:
    assert hasattr(auditor, 'extraction_skill'), "Falta extraction_skill"
    assert hasattr(auditor, 'hybrid_hp_skill'), "Falta hybrid_hp_skill"
    assert hasattr(auditor, 'evaluation_skill'), "Falta evaluation_skill"
    assert hasattr(auditor, 'verification_skill'), "Falta verification_skill"
    assert hasattr(auditor, 'metrics_skill'), "Falta metrics_skill"
    assert hasattr(auditor, 'metadata_skill'), "Falta metadata_skill"
    print("   [OK] Todos los skills del auditor presentes")
except AssertionError as e:
    print(f"   [ERROR] {e}")
    sys.exit(1)

# Test 5: Obsoleto (Chatbot eliminado)
print("\n5. Test de Chatbot omitido (Chatbot eliminado del backend)")

# Test 6: Verificar estructura de skills en SotaAnalyzer
print("\n6. Verificando estructura de SotaAnalyzer...")
try:
    assert hasattr(sota, 'thematic_skill'), "Falta thematic_skill"
    assert hasattr(sota, 'query_skill'), "Falta query_skill"
    assert hasattr(sota, 'search_skill'), "Falta search_skill"
    assert hasattr(sota, 'gap_skill'), "Falta gap_skill"
    assert hasattr(sota, 'validation_skill'), "Falta validation_skill"
    print("   [OK] Todos los skills de SOTA presentes")
except AssertionError as e:
    print(f"   [ERROR] {e}")
    sys.exit(1)

# Test 7: Verificar herencia de BaseSkill
print("\n7. Verificando herencia de BaseSkill...")
try:
    assert isinstance(auditor.extraction_skill, BaseSkill)
    assert isinstance(sota.thematic_skill, BaseSkill)
    print("   [OK] Todos los skills heredan correctamente de BaseSkill")
except AssertionError:
    print("   [ERROR] Error en herencia de BaseSkill")
    sys.exit(1)

# Test 8: Verificar métodos de BaseSkill
print("\n8. Verificando métodos de BaseSkill...")
try:
    skill = auditor.extraction_skill
    assert hasattr(skill, 'execute'), "Falta método execute"
    assert hasattr(skill, 'validate_context'), "Falta método validate_context"
    assert hasattr(skill, 'log_execution'), "Falta método log_execution"
    assert callable(skill.execute), "execute no es callable"
    print("   [OK] Todos los métodos base presentes")
except AssertionError as e:
    print(f"   [ERROR] {e}")
    sys.exit(1)

# Test 9: Test simple de ejecución (sin LLM real)
print("\n9. Probando ejecución de skill simple...")
try:
    # Crear un skill de búsqueda (no requiere LLM)
    from backend.skills.sota_skills import SemanticScholarSearchSkill
    search_skill = SemanticScholarSearchSkill()
    
    # Context vacío, debería retornar lista vacía
    result = search_skill.execute({'search_queries': []})
    assert 'sota_papers' in result
    print("   [OK] Skill ejecutado correctamente")
except Exception as e:
    print(f"   [ERROR] Error ejecutando skill: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 10: Verificar logging
print("\n10. Verificando capacidad de logging...")
try:
    from backend.common.logger import get_logger
    logger = get_logger("test_skill")
    logger.info("Test de logging")
    print("   [OK] Sistema de logging funcional")
except Exception as e:
    print(f"   [ERROR] Error en logging: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("[OK] TODOS LOS TESTS PASARON EXITOSAMENTE")
print("=" * 70)
print("\nArquitectura basada en skills implementada correctamente:")
print("  • BaseSkill: Clase base para todos los skills")
print("  • Auditor: 5 skills especializados")
print("  • SOTA: 5 skills especializados")
print("\nTotal: 10 skills implementados + 1 clase base")
print("=" * 70)
