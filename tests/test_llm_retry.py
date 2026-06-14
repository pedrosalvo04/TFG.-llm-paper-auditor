import sys
import os
from unittest.mock import MagicMock, patch

# Mocking modules
sys.modules['streamlit'] = MagicMock()

# Add project root to path
sys.path.append(os.getcwd())

from backend.common.llm_client import LLMClient
import requests

def test_generate_success():
    client = LLMClient(model_name="qwen2.5")
    
    # Mock requests.post
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Success response"}
    
    with patch('requests.post', return_value=mock_response) as mock_post:
        print("Testing successful generation...")
        response = client.generate("test prompt")
        print(f"Result: {response.text}")
        assert response.text == "Success response"
        assert mock_post.call_count == 1
        print("OK: Success logic test passed!")

def test_connection_failure():
    client = LLMClient(model_name="qwen2.5")
    
    # Mock requests.post to raise ConnectionError
    with patch('requests.post', side_effect=requests.exceptions.ConnectionError("Connection Refused")) as mock_post:
        print("\nTesting connection failure logic...")
        try:
            client.generate("test prompt")
            assert False, "Should have raised a ConnectionError"
        except ConnectionError as e:
            print(f"Caught expected connection exception: {e}")
            assert mock_post.call_count == 1
            print("OK: Connection failure test passed!")

if __name__ == "__main__":
    test_generate_success()
    test_connection_failure()
