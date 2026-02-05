"""
Unit tests for synthesizer module.

Tests Ollama API integration, prompt formatting, and knowledge synthesis.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import json

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.synthesizer import (
    KnowledgeSynthesizer,
    SynthesizerError,
    OllamaConnectionError,
    OllamaAPIError,
    PromptTemplateError
)


class TestKnowledgeSynthesizerInit:
    """Test KnowledgeSynthesizer initialization."""
    
    @patch('core.synthesizer.get_config')
    def test_init_local_ollama(self, mock_get_config):
        """Test initialization with local Ollama."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.default_synthesis_prompt_template = "basic_summary"
        mock_get_config.return_value = mock_config
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        
        assert synthesizer.use_cloud is False
        assert synthesizer.base_url == "http://localhost:11434"
        assert synthesizer.model == "llama3.1:8b"
        assert synthesizer.api_key is None
    
    @patch('core.synthesizer.get_config')
    def test_init_cloud_ollama(self, mock_get_config):
        """Test initialization with cloud Ollama."""
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-api-key"
        mock_config.default_synthesis_prompt_template = "basic_summary"
        mock_get_config.return_value = mock_config
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        
        assert synthesizer.use_cloud is True
        assert synthesizer.base_url == "https://api.ollama.ai/v1"
        assert synthesizer.model == "llama3.1:8b"
        assert synthesizer.api_key == "test-api-key"


class TestCallLocalOllama:
    """Test local Ollama API calls."""
    
    @pytest.mark.slow
    @patch('core.synthesizer.requests.post')
    def test_call_local_ollama_success(self, mock_post):
        """Test successful local Ollama API call."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Synthesized text"}
        mock_post.return_value = mock_response
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        synthesizer.base_url = "http://localhost:11434"
        synthesizer.model = "llama3.1:8b"
        
        result = synthesizer._call_local_ollama("Test prompt")
        
        assert result == "Synthesized text"
        mock_post.assert_called_once()
        
        # Verify the call arguments
        call_args = mock_post.call_args
        assert call_args[0][0] == "http://localhost:11434/api/generate"
        assert call_args[1]["json"]["model"] == "llama3.1:8b"
        assert call_args[1]["json"]["prompt"] == "Test prompt"
        assert call_args[1]["json"]["stream"] is False
    
    @patch('core.synthesizer.requests.post')
    def test_call_local_ollama_connection_error(self, mock_post):
        """Test handling of connection errors."""
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        synthesizer.base_url = "http://localhost:11434"
        synthesizer.model = "llama3.1:8b"
        
        with pytest.raises(OllamaConnectionError):
            synthesizer._call_local_ollama("Test prompt")
    
    @patch('core.synthesizer.requests.post')
    def test_call_local_ollama_timeout(self, mock_post):
        """Test handling of timeout errors."""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        synthesizer.base_url = "http://localhost:11434"
        synthesizer.model = "llama3.1:8b"
        
        with pytest.raises(OllamaConnectionError):
            synthesizer._call_local_ollama("Test prompt")
    
    @patch('core.synthesizer.requests.post')
    def test_call_local_ollama_http_error(self, mock_post):
        """Test handling of HTTP errors."""
        import requests
        # Create a proper HTTPError with response attributes
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        
        http_error = requests.exceptions.HTTPError("404 Not Found")
        http_error.response = mock_response
        
        mock_post.return_value = mock_response
        mock_response.raise_for_status.side_effect = http_error
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        synthesizer.base_url = "http://localhost:11434"
        synthesizer.model = "llama3.1:8b"
        
        with pytest.raises(OllamaAPIError):
            synthesizer._call_local_ollama("Test prompt")
    
    @patch('core.synthesizer.requests.post')
    def test_call_local_ollama_empty_response(self, mock_post):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": ""}
        mock_post.return_value = mock_response
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        synthesizer.base_url = "http://localhost:11434"
        synthesizer.model = "llama3.1:8b"
        
        with pytest.raises(OllamaAPIError):
            synthesizer._call_local_ollama("Test prompt")


class TestCallCloudOllama:
    """Test cloud Ollama API calls."""
    
    @patch('core.synthesizer.get_config')
    @patch('core.synthesizer.requests.post')
    def test_call_cloud_ollama_success(self, mock_post, mock_get_config):
        """Test successful cloud Ollama API call."""
        # Mock the config to avoid validation errors
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-api-key"
        mock_get_config.return_value = mock_config
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Cloud synthesized text"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        synthesizer.base_url = "https://api.ollama.ai/v1"
        synthesizer.model = "llama3.1:8b"
        synthesizer.api_key = "test-api-key"
        
        result = synthesizer._call_cloud_ollama("Test prompt")
        
        assert result == "Cloud synthesized text"
        mock_post.assert_called_once()
        
        # Verify the call arguments
        call_args = mock_post.call_args
        assert call_args[0][0] == "https://api.ollama.ai/v1/chat/completions"
        assert call_args[1]["json"]["model"] == "llama3.1:8b"
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-api-key"
    
    @patch('core.synthesizer.get_config')
    @patch('core.synthesizer.requests.post')
    def test_call_cloud_ollama_alternative_response_format(self, mock_post, mock_get_config):
        """Test cloud Ollama with alternative response format."""
        # Mock the config to avoid validation errors
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-api-key"
        mock_get_config.return_value = mock_config
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Alternative format response"}
        mock_post.return_value = mock_response
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        synthesizer.base_url = "https://api.ollama.ai/v1"
        synthesizer.model = "llama3.1:8b"
        synthesizer.api_key = "test-api-key"
        
        result = synthesizer._call_cloud_ollama("Test prompt")
        
        assert result == "Alternative format response"
    
    @patch('core.synthesizer.get_config')
    @patch('core.synthesizer.requests.post')
    def test_call_cloud_ollama_connection_error(self, mock_post, mock_get_config):
        """Test handling of cloud connection errors."""
        # Mock the config to avoid validation errors
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-api-key"
        mock_get_config.return_value = mock_config
        
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Cloud connection failed")
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        synthesizer.base_url = "https://api.ollama.ai/v1"
        synthesizer.model = "llama3.1:8b"
        synthesizer.api_key = "test-api-key"
        
        with pytest.raises(OllamaConnectionError):
            synthesizer._call_cloud_ollama("Test prompt")


class TestSynthesize:
    """Test main synthesize method."""
    
    @patch('core.synthesizer.format_template')
    @patch('core.synthesizer.KnowledgeSynthesizer._call_local_ollama')
    @patch('core.synthesizer.get_config')
    def test_synthesize_with_default_template(self, mock_get_config, mock_call, mock_format):
        """Test synthesis with default template."""
        mock_config = MagicMock()
        mock_config.default_synthesis_prompt_template = "basic_summary"
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_format.return_value = "Formatted prompt with transcript"
        mock_call.return_value = "Synthesized result"
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.synthesize("Test transcript")
        
        assert result["raw_text"] == "Synthesized result"
        assert result["model_used"] == "llama3.1:8b"
        assert result["template_used"] == "basic_summary"
        assert result["transcript_length"] == 15
        assert result["synthesis_length"] == 18
        assert result["use_cloud"] is False
    
    @patch('core.synthesizer.format_template')
    @patch('core.synthesizer.KnowledgeSynthesizer._call_local_ollama')
    @patch('core.synthesizer.get_config')
    def test_synthesize_with_custom_template(self, mock_get_config, mock_call, mock_format):
        """Test synthesis with custom template."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_format.return_value = "Meeting minutes formatted prompt"
        mock_call.return_value = "Meeting minutes result"
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.synthesize("Test transcript", prompt_template="meeting_minutes")
        
        assert result["raw_text"] == "Meeting minutes result"
        assert result["template_used"] == "meeting_minutes"
        mock_format.assert_called_once_with("meeting_minutes", "Test transcript")
    
    @patch('core.synthesizer.KnowledgeSynthesizer._call_local_ollama')
    @patch('core.synthesizer.get_config')
    def test_synthesize_with_custom_prompt(self, mock_get_config, mock_call):
        """Test synthesis with custom prompt text."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_call.return_value = "Custom prompt result"
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.synthesize("Test transcript", custom_prompt="Custom prompt: {transcript}")
        
        assert result["raw_text"] == "Custom prompt result"
        assert result["template_used"] == "custom"
        mock_call.assert_called_once_with("Custom prompt: {transcript}")
    
    @patch('core.synthesizer.get_config')
    def test_synthesize_empty_transcript(self, mock_get_config):
        """Test handling of empty transcript."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        
        with pytest.raises(SynthesizerError):
            synthesizer.synthesize("")
    
    @patch('core.synthesizer.format_template')
    @patch('core.synthesizer.KnowledgeSynthesizer._call_cloud_ollama')
    @patch('core.synthesizer.get_config')
    def test_synthesize_with_cloud(self, mock_get_config, mock_call, mock_format):
        """Test synthesis with cloud Ollama."""
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-key"
        mock_config.default_synthesis_prompt_template = "basic_summary"
        mock_get_config.return_value = mock_config
        
        mock_format.return_value = "Formatted prompt"
        mock_call.return_value = "Cloud result"
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        result = synthesizer.synthesize("Test transcript")
        
        assert result["raw_text"] == "Cloud result"
        assert result["use_cloud"] is True


class TestTestConnection:
    """Test connection testing functionality."""
    
    @patch('core.synthesizer.requests.get')
    @patch('core.synthesizer.get_config')
    def test_test_connection_local_success(self, mock_get_config, mock_get):
        """Test successful local connection test."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.test_connection()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=10)
    
    @patch('core.synthesizer.requests.get')
    @patch('core.synthesizer.get_config')
    def test_test_connection_local_failure(self, mock_get_config, mock_get):
        """Test failed local connection test."""
        mock_config = MagicMock()
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_get.side_effect = Exception("Connection failed")
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.test_connection()
        
        assert result is False
    
    @patch('core.synthesizer.get_config')
    def test_test_connection_cloud_with_api_key(self, mock_get_config):
        """Test cloud connection test with API key."""
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = "test-key"
        mock_get_config.return_value = mock_config
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        result = synthesizer.test_connection()
        
        assert result is True
    
    @patch('core.synthesizer.get_config')
    def test_test_connection_cloud_without_api_key(self, mock_get_config):
        """Test cloud connection test without API key."""
        mock_config = MagicMock()
        mock_config.ollama_cloud_url = "https://api.ollama.ai/v1"
        mock_config.ollama_model = "llama3.1:8b"
        mock_config.ollama_cloud_api_key = ""
        mock_get_config.return_value = mock_config
        
        synthesizer = KnowledgeSynthesizer(use_cloud=True)
        result = synthesizer.test_connection()
        
        assert result is False


class TestSynthesizerExceptions:
    """Test synthesizer exception classes."""
    
    def test_synthesizer_error_creation(self):
        """Test SynthesizerError can be created."""
        error = SynthesizerError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)
    
    def test_ollama_connection_error_creation(self):
        """Test OllamaConnectionError can be created."""
        error = OllamaConnectionError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, SynthesizerError)
    
    def test_ollama_api_error_creation(self):
        """Test OllamaAPIError can be created."""
        error = OllamaAPIError("API error")
        assert str(error) == "API error"
        assert isinstance(error, SynthesizerError)
    
    def test_prompt_template_error_creation(self):
        """Test PromptTemplateError can be created."""
        error = PromptTemplateError("Invalid template")
        assert str(error) == "Invalid template"
        assert isinstance(error, SynthesizerError)


class TestSynthesisResultStructure:
    """Test synthesis result structure."""
    
    @patch('core.synthesizer.format_template')
    @patch('core.synthesizer.KnowledgeSynthesizer._call_local_ollama')
    @patch('core.synthesizer.get_config')
    def test_synthesis_result_structure(self, mock_get_config, mock_call, mock_format):
        """Test that synthesis result has correct structure."""
        mock_config = MagicMock()
        mock_config.default_synthesis_prompt_template = "basic_summary"
        mock_config.ollama_base_url = "http://localhost:11434"
        mock_config.ollama_model = "llama3.1:8b"
        mock_get_config.return_value = mock_config
        
        mock_format.return_value = "Formatted prompt"
        mock_call.return_value = "Synthesized text"
        
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        result = synthesizer.synthesize("Test transcript")
        
        # Verify all expected keys are present
        expected_keys = [
            "raw_text",
            "model_used",
            "template_used",
            "transcript_length",
            "synthesis_length",
            "use_cloud"
        ]
        
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])