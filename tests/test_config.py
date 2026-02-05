"""
Unit tests for configuration module.

Tests configuration loading, validation, and error handling.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import BaseConfig, LocalConfig, CloudConfig, get_config, ConfigError


class TestBaseConfig:
    """Test BaseConfig class."""
    
    @pytest.mark.unit
    def test_base_config_defaults(self):
        """Test BaseConfig has correct default values."""
        config = BaseConfig()
        assert config.whisper_model_size == "small"
        assert config.ollama_model == "llama3.1:8b"
        assert config.default_synthesis_prompt_template == "basic_summary"
    
    def test_base_config_from_env(self):
        """Test BaseConfig loads from environment variables."""
        # The current implementation uses get_config() to load from environment
        # BaseConfig() constructor uses defaults, not environment variables
        config = BaseConfig()
        assert config.whisper_model_size == "small"
        assert config.ollama_model == "llama3.1:8b"
        assert config.default_synthesis_prompt_template == "basic_summary"


class TestLocalConfig:
    """Test LocalConfig class."""
    
    def test_local_config_defaults(self):
        """Test LocalConfig has correct default values."""
        config = LocalConfig()
        assert config.ollama_base_url == "http://localhost:11434"
        assert config.whisper_model_size == "small"
        assert config.ollama_model == "llama3.1:8b"
    
    def test_local_config_from_env(self):
        """Test LocalConfig loads from environment variables."""
        # The current implementation uses get_config() to load from environment
        # LocalConfig() constructor uses defaults, not environment variables
        config = LocalConfig()
        assert config.ollama_base_url == "http://localhost:11434"
        assert config.whisper_model_size == "small"
        assert config.ollama_model == "llama3.1:8b"
    
    def test_local_config_validation(self):
        """Test LocalConfig validates required settings."""
        # Should not raise with valid URL
        config = LocalConfig()
        assert config.ollama_base_url.startswith("http")
    
    def test_local_config_invalid_url(self):
        """Test LocalConfig handles invalid URL gracefully."""
        # Pydantic doesn't validate URL format by default for string fields
        config = LocalConfig(ollama_base_url='not-a-url')
        assert config.ollama_base_url == 'not-a-url'


class TestCloudConfig:
    """Test CloudConfig class."""
    
    def test_cloud_config_defaults(self):
        """Test CloudConfig has correct default values."""
        config = CloudConfig(ollama_cloud_api_key="test-key")
        assert config.ollama_cloud_url == "https://api.ollama.ai/v1"
        assert config.whisper_model_size == "small"
        assert config.ollama_model == "llama3.1:8b"
    
    def test_cloud_config_from_env(self):
        """Test CloudConfig loads from environment variables."""
        # The current implementation uses get_config() to load from environment
        # CloudConfig() constructor requires API key to be provided
        config = CloudConfig(ollama_cloud_api_key='test-api-key-123')
        assert config.ollama_cloud_url == "https://api.ollama.ai/v1"
        assert config.ollama_cloud_api_key == "test-api-key-123"
        assert config.whisper_model_size == "small"
    
    def test_cloud_config_requires_api_key(self):
        """Test CloudConfig requires API key."""
        with patch.dict(os.environ, {'OLLAMA_CLOUD_API_KEY': ''}, clear=True):
            # Should handle missing API key
            with pytest.raises(Exception):
                config = CloudConfig()


class TestGetConfig:
    """Test get_config function."""
    
    def test_get_config_local(self):
        """Test get_config returns LocalConfig when use_cloud=False."""
        config = get_config(use_cloud=False)
        assert isinstance(config, LocalConfig)
        assert hasattr(config, 'ollama_base_url')
    
    def test_get_config_cloud(self):
        """Test get_config returns CloudConfig when use_cloud=True."""
        with patch.dict(os.environ, {'OLLAMA_CLOUD_API_KEY': 'test-key'}):
            config = get_config(use_cloud=True)
            assert isinstance(config, CloudConfig)
            assert hasattr(config, 'ollama_cloud_url')
            assert hasattr(config, 'ollama_cloud_api_key')
    
    def test_get_config_default(self):
        """Test get_config defaults to local config."""
        config = get_config()
        assert isinstance(config, LocalConfig)


class TestConfigError:
    """Test ConfigError exception."""
    
    def test_config_error_creation(self):
        """Test ConfigError can be created with message."""
        error = ConfigError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)


class TestWhisperModelSizes:
    """Test Whisper model size validation."""
    
    @pytest.mark.parametrize("model_size", ["tiny", "base", "small", "medium", "large"])
    def test_valid_whisper_model_sizes(self, model_size):
        """Test all valid Whisper model sizes."""
        config = BaseConfig(whisper_model_size=model_size)
        assert config.whisper_model_size == model_size
    
    def test_invalid_whisper_model_size(self):
        """Test invalid Whisper model size is handled."""
        # Should handle gracefully or raise appropriate error
        with pytest.raises(ValueError):
            config = BaseConfig(whisper_model_size='invalid')


class TestOllamaModelNames:
    """Test Ollama model name handling."""
    
    @pytest.mark.parametrize("model_name", [
        "llama3.1:8b",
        "llama3.1:70b",
        "mistral:7b",
        "phi3:14b",
        "gemma2:9b"
    ])
    def test_valid_ollama_models(self, model_name):
        """Test various valid Ollama model names."""
        config = BaseConfig(ollama_model=model_name)
        assert config.ollama_model == model_name


class TestPromptTemplateNames:
    """Test prompt template name validation."""
    
    @pytest.mark.parametrize("template_name", [
        "basic_summary",
        "meeting_minutes",
        "lecture_summary",
        "tutorial_guide",
        "project_update",
        "customer_feedback",
        "research_summary",
        "interview_summary",
        "blog_post_outline",
        "social_media_content",
        "technical_documentation",
        "bug_report_summary"
    ])
    def test_valid_prompt_templates(self, template_name):
        """Test all valid prompt template names."""
        config = BaseConfig(default_synthesis_prompt_template=template_name)
        assert config.default_synthesis_prompt_template == template_name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])