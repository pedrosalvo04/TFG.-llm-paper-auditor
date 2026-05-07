import unittest
from backend.services.pdf_parser import StructuralChunk

class TestPDFParser(unittest.TestCase):
    def test_structural_chunk_embedding_text(self):
        """Verifica que el texto de embedding para tablas es descriptivo."""
        # Chunk tipo sección
        s = StructuralChunk(chunk_type="section", content="Context", section_title="Intro")
        self.assertIn("[SECCIÓN: Intro]", s.to_embed_text())
        
        # Chunk tipo tabla
        t = StructuralChunk(
            chunk_type="table", 
            content="| a | b |", 
            section_title="Results",
            table_caption="Main metrics"
        )
        self.assertIn("[TABLA] Results: Main metrics", t.to_embed_text())
        
    def test_structural_chunk_with_description(self):
        """Verifica que si hay descripción LLM, se usa en el embedding."""
        t = StructuralChunk(
            chunk_type="table", 
            content="| a | b |", 
            table_description="Resumen de hiperparámetros"
        )
        self.assertIn("Resumen de hiperparámetros", t.to_embed_text())

if __name__ == "__main__":
    unittest.main()
