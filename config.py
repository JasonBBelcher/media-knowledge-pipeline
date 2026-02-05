"""
Configuration Management for Media-to-Knowledge Pipeline

This module handles loading and validating configuration from environment variables.
Supports both local and cloud Ollama configurations.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


# Load environment variables from .env file
load_dotenv()


class BaseConfig(BaseModel):
    """Base configuration with common settings."""
    
    # Whisper Model Configuration
    whisper_model_size: str = Field(
        default="small",
        description="Whisper model size: tiny, base, small, medium, large"
    )
    
    # Ollama Model Configuration
    ollama_model: str = Field(
        default="llama3.1:8b",
        description="Ollama model name for knowledge synthesis"
    )
    
    # Default Prompt Template
    default_synthesis_prompt_template: str = Field(
        default="basic_summary",
        description="Default prompt template key"
    )
    
    # File Scanner Configuration
    scan_directory: str = Field(
        default="~/Downloads",
        description="Default directory to scan for media files"
    )
    
    audio_directory: str = Field(
        default="data/audio",
        description="Directory to copy audio files to"
    )
    
    video_directory: str = Field(
        default="data/videos",
        description="Directory to copy video files to"
    )
    
    watch_poll_interval: int = Field(
        default=5,
        description="Poll interval for watch mode in seconds"
    )
    
    auto_process: bool = Field(
        default=False,
        description="Automatically process files after copying"
    )
    
    skip_existing: bool = Field(
        default=True,
        description="Skip files that already exist in destination"
    )
    
    @field_validator("whisper_model_size")
    @classmethod
    def validate_whisper_model(cls, v: str) -> str:
        """Validate Whisper model size."""
        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        if v not in valid_sizes:
            raise ValueError(f"Invalid Whisper model size: {v}. Must be one of {valid_sizes}")
        return v


class LocalConfig(BaseConfig):
    """Configuration for local Ollama instance."""
    
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Local Ollama API endpoint"
    )
    
    use_cloud: bool = Field(
        default=False,
        description="Whether to use cloud Ollama"
    )


class CloudConfig(BaseConfig):
    """Configuration for Ollama Cloud instance."""
    
    # NOTE: This URL is a PLACEHOLDER - verify from official Ollama Cloud documentation
    ollama_cloud_url: str = Field(
        default="https://api.ollama.ai/v1",
        description="Ollama Cloud API endpoint (PLACEHOLDER - verify from docs)"
    )
    
    ollama_cloud_api_key: str = Field(
        ...,
        description="API key for Ollama Cloud authentication"
    )
    
    use_cloud: bool = Field(
        default=True,
        description="Whether to use cloud Ollama"
    )
    
    @field_validator("ollama_cloud_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that API key is provided."""
        if not v or v == "your_api_key_here":
            raise ValueError(
                "OLLAMA_CLOUD_API_KEY must be set in .env file. "
                "Get your API key from Ollama Cloud documentation."
            )
        return v


def get_config(use_cloud: bool = False) -> BaseConfig:
    """
    Get the appropriate configuration based on cloud flag.
    
    Args:
        use_cloud: Whether to use cloud Ollama configuration
    
    Returns:
        Configuration object (LocalConfig or CloudConfig)
    """
    if use_cloud:
        return CloudConfig(
            whisper_model_size=os.getenv("WHISPER_MODEL_SIZE", "small"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            default_synthesis_prompt_template=os.getenv("DEFAULT_SYNTHESIS_PROMPT_TEMPLATE", "basic_summary"),
            scan_directory=os.getenv("MKD_DOWNLOAD_DIR", os.getenv("SCAN_DIRECTORY", "~/Downloads")),
            audio_directory=os.getenv("AUDIO_DIRECTORY", "data/audio"),
            video_directory=os.getenv("VIDEO_DIRECTORY", "data/videos"),
            watch_poll_interval=int(os.getenv("MKD_SCAN_INTERVAL", os.getenv("WATCH_POLL_INTERVAL", "5"))),
            auto_process=os.getenv("MKD_AUTO_PROCESS", "false").lower() == "true",
            skip_existing=os.getenv("MKD_SKIP_EXISTING", "true").lower() == "true",
            ollama_cloud_url=os.getenv("OLLAMA_CLOUD_URL", "https://api.ollama.ai/v1"),
            ollama_cloud_api_key=os.getenv("OLLAMA_CLOUD_API_KEY", "")
        )
    else:
        return LocalConfig(
            whisper_model_size=os.getenv("WHISPER_MODEL_SIZE", "small"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            default_synthesis_prompt_template=os.getenv("DEFAULT_SYNTHESIS_PROMPT_TEMPLATE", "basic_summary"),
            scan_directory=os.getenv("MKD_DOWNLOAD_DIR", os.getenv("SCAN_DIRECTORY", "~/Downloads")),
            audio_directory=os.getenv("AUDIO_DIRECTORY", "data/audio"),
            video_directory=os.getenv("VIDEO_DIRECTORY", "data/videos"),
            watch_poll_interval=int(os.getenv("MKD_SCAN_INTERVAL", os.getenv("WATCH_POLL_INTERVAL", "5"))),
            auto_process=os.getenv("MKD_AUTO_PROCESS", "false").lower() == "true",
            skip_existing=os.getenv("MKD_SKIP_EXISTING", "true").lower() == "true",
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )


# Export configuration instances
config = get_config(use_cloud=False)