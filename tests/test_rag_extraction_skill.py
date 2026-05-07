import unittest
from unittest.mock import MagicMock
from backend.skills.rag_extraction_skill import HybridHyperparameterExtractionSkill
from backend.services.pdf_parser import StructuralChunk

class TestRAGExtractionSkill(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.skill = HybridHyperparameterExtractionSkill(llm_client=self.mock_llm)

    def test_prepare_structural_texts(self):
        """Verifica la preparación de textos para vectorización RAG."""
        chunks = [
            StructuralChunk(chunk_type="section", content="Texto 1", section_title="S1"),
            StructuralChunk(chunk_type="table", content="| T | 1 |", section_title="S2", table_caption="Cap")
        ]
        
        texts, metadatas = self.skill._prepare_structural_texts(chunks)
        
        self.assertEqual(len(texts), 2)
        self.assertIn("[SECCIÓN: S1]", texts[0])
        self.assertIn("[TABLA] S2: Cap", texts[1])
        self.assertEqual(metadatas[1]["chunk_type"], "table")
        
    def test_clean_with_regex_normalization(self):
        """Verifica la normalización de LR y Batch Size."""
        data = {
            "learning_rate": "3 x 10^-4",
            "batch_size": "mini-batch of 2048",
            "weight_decay": "0.0001"
        }
        cleaned = self.skill._clean_with_regex(data)
        
        self.assertEqual(cleaned["learning_rate"], 0.0003)
        self.assertEqual(cleaned["batch_size"], 2048)
        self.assertEqual(cleaned["weight_decay"], 0.0001)

if __name__ == "__main__":
    unittest.main()
