import unittest
from unittest.mock import MagicMock
from backend.skills.auditor_skills import InformationExtractionSkill
from backend.services.pdf_parser import StructuralChunk

class TestAuditorSkills(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.skill = InformationExtractionSkill(llm_client=self.mock_llm)

    def test_group_structural_chunks_merging(self):
        """Verifica que los chunks pequeños se agrupan hasta el target_size."""
        chunks = [
            StructuralChunk(chunk_type="section", content="A" * 100),
            StructuralChunk(chunk_type="section", content="B" * 100),
            StructuralChunk(chunk_type="section", content="C" * 1000),
        ]
        
        # Target size 250 -> A y B deberían agruparse, C iría solo
        batches = self.skill._group_structural_chunks(chunks, target_size=250)
        
        self.assertEqual(len(batches), 2)
        self.assertIn("A" * 100, batches[0])
        self.assertIn("B" * 100, batches[0])
        self.assertEqual(batches[1], "C" * 1000)
        
    def test_group_structural_chunks_limit(self):
        """Verifica que se respeta el límite máximo de 6 batches."""
        chunks = [StructuralChunk(chunk_type="section", content="A") for _ in range(20)]
        batches = self.skill._group_structural_chunks(chunks, target_size=1)
        self.assertEqual(len(batches), 6)

if __name__ == "__main__":
    unittest.main()
