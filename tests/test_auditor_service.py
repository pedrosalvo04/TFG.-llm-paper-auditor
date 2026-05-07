import unittest
from unittest.mock import MagicMock
from backend.services.auditor import PaperAuditor
from backend.common.llm_client import LLMClient

class TestAuditorService(unittest.TestCase):
    def test_dependency_injection(self):
        """Verifica que el servicio inyecta correctamente los clientes en los skills."""
        mock_llm = MagicMock(spec=LLMClient)
        auditor = PaperAuditor(extraction_llm=mock_llm)
        
        # El skill de extracción debería tener el mock inyectado
        self.assertEqual(auditor.extraction_skill.llm_client, mock_llm)
        # El skill de métricas no usa LLM, debería ser independiente
        self.assertIsNone(getattr(auditor.metrics_skill, 'llm_client', None))

    def test_audit_error_handling(self):
        """Verifica que los errores en los skills se propagan correctamente."""
        mock_llm = MagicMock()
        auditor = PaperAuditor(extraction_llm=mock_llm)
        
        # Simular fallo en el primer skill
        auditor.extraction_skill.execute = MagicMock(return_value={"extraction_error": "API Key Expired"})
        
        result = auditor.audit("Paper text")
        self.assertEqual(result["error"], "API Key Expired")

if __name__ == "__main__":
    unittest.main()
