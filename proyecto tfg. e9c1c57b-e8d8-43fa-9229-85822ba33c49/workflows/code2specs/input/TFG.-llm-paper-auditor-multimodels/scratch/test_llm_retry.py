
import sys
import os
from unittest.mock import MagicMock, patch

# Mocking modules that might not be available or needed for this test
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['streamlit'] = MagicMock()

# Add project root to path
sys.path.append(os.getcwd())

from backend.common.llm_client import LLMClient

def test_retry_logic():
    client = LLMClient(model_name="test-model")
    
    # Mock the internal client's generate_content method
    mock_gen = MagicMock()
    client.client.models.generate_content = mock_gen
    
    # Simulate a 503 error for 2 attempts, then success
    mock_gen.side_effect = [
        Exception("503 UNAVAILABLE: High demand"),
        Exception("503 UNAVAILABLE: High demand"),
        MagicMock(text="Success response")
    ]
    
    print("Testing retry logic (2 failures then success)...")
    with patch('time.sleep') as mock_sleep: # Don't actually sleep
        response = client.generate("test prompt")
        print("Result: Success response")
        assert mock_gen.call_count == 3
        assert mock_sleep.call_count == 2
        print("OK: Retry logic test passed!")

def test_final_failure():
    client = LLMClient(model_name="test-model")
    
    # Mock the internal client's generate_content method
    mock_gen = MagicMock()
    client.client.models.generate_content = mock_gen
    
    # Always fail
    mock_gen.side_effect = Exception("503 UNAVAILABLE: High demand")
    
    print("\nTesting final failure logic (all failures)...")
    with patch('time.sleep') as mock_sleep:
        try:
            client.generate("test prompt")
            assert False, "Should have raised an exception"
        except Exception as e:
            print(f"Caught expected final exception: {e}")
            assert mock_gen.call_count == 6 # 1 original + 5 retries
            print("OK: Final failure test passed!")

if __name__ == "__main__":
    # Mocking config variables
    with patch('backend.common.config.GOOGLE_API_KEY', "test-key"):
        with patch('backend.common.config.MODEL_NAME', "test-model"):
            test_retry_logic()
            test_final_failure()
