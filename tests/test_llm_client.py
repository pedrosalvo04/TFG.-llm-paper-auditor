import unittest
from unittest.mock import MagicMock, patch
from backend.common.llm_client import LLMClient, _is_retryable_error

class TestLLMClient(unittest.TestCase):
    def test_retryable_errors(self):
        """Verifica que solo los errores 503/429 sean reintentables."""
        self.assertTrue(_is_retryable_error(Exception("503 Service Unavailable")))
        self.assertTrue(_is_retryable_error(Exception("429 Resource Exhausted")))
        self.assertFalse(_is_retryable_error(Exception("400 Bad Request")))
        
    @patch("google.genai.Client")
    def test_generate_call(self, mock_genai):
        """Verifica que la llamada generate usa el modelo y config correctos."""
        client = LLMClient(model_name="test-model", generation_config={"temp": 0.5})
        mock_response = MagicMock()
        client.client.models.generate_content.return_value = mock_response
        
        res = client.generate("Hello")
        self.assertEqual(res, mock_response)
        client.client.models.generate_content.assert_called_with(
            model="test-model",
            contents="Hello",
            config={"temp": 0.5}
        )

if __name__ == "__main__":
    unittest.main()
