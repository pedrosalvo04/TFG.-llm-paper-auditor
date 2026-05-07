import unittest
from backend.common.audit_state import AuditState, ExtractedInfo, ChecklistItem

class TestAuditState(unittest.TestCase):
    def test_initialization(self):
        """Verifica que el estado se inicializa con valores por defecto correctos."""
        state = AuditState(paper_text="Test content")
        self.assertEqual(state.paper_text, "Test content")
        self.assertFalse(state.invalid_paper)
        self.assertEqual(state.execution_time, 0.0)
        
    def test_to_frontend_dict(self):
        """Verifica que la conversión a dict mantiene las claves requeridas por el frontend."""
        state = AuditState(paper_text="Test", evaluation={"claims": {"answer": "Yes"}})
        d = state.to_frontend_dict()
        self.assertEqual(d["claims"]["answer"], "Yes")
        self.assertIn("informacion_extraida", d)
        self.assertIn("metricas", d)
        
    def test_extracted_info_nesting(self):
        """Verifica que los submodelos de ExtractedInfo funcionan."""
        info = ExtractedInfo()
        self.assertEqual(info.code.repository_url, "NOT FOUND")
        self.assertEqual(info.hyperparameters.optimizer, "NOT FOUND")

if __name__ == "__main__":
    unittest.main()
