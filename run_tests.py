import unittest
import sys
import os

# Asegurar que el directorio raíz esté en el path para los imports de backend
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_all_tests():
    print("--- Iniciando Suite de Pruebas Unitarias del Auditor ---")
    print("-" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n[OK] TODOS LOS TESTS HAN PASADO! El pipeline es robusto.")
        sys.exit(0)
    else:
        print("\n[FAIL] ALGUNOS TESTS HAN FALLADO. Revisa los logs arriba.")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
