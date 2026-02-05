"""
Knowledge Synthesizer Module

Handles knowledge synthesis from transcripts using Ollama models.
Supports both local and cloud Ollama instances.

This module provides the core synthesis engine that takes a transcript
and uses Ollama models to extract structured knowledge based on
configurable prompt templates.
"""

import requests
from typing import Optional, Dict, Any
from config import get_config
from core.prompts import get_template, format_template


class SynthesizerError(Exception):
    """Custom exception for synthesizer errors."""
    pass


class OllamaConnectionError(SynthesizerError):
    """Raised when connection to Ollama fails."""
    pass


class OllamaAPIError(SynthesizerError):
    """Raised when Ollama API returns an error."""
    pass


class PromptTemplateError(SynthesizerError):
    """Raised when prompt template is invalid."""
    pass


class KnowledgeSynthesizer:
    """
    Knowledge synthesizer using Ollama models.
    
    This class provides methods to synthesize knowledge from transcripts
    using either local or cloud Ollama instances. It supports various
    prompt templates for different synthesis tasks.
    
    Attributes:
        use_cloud: Whether to use cloud Ollama (True) or local (False).
        config: Configuration object with Ollama settings.
        base_url: Base URL for Ollama API endpoint.
        model: Model name to use for synthesis.
        api_key: API key for cloud Ollama (None for local).
    """
    
    def __init__(self, use_cloud: bool = False):
        """
        Initialize the KnowledgeSynthesizer.
        
        Args:
            use_cloud: Whether to use cloud Ollama (default: False).
        
        Raises:
            SynthesizerError: If configuration is invalid.
        
        Example:
            >>> # Use local Ollama
            >>> synthesizer = KnowledgeSynthesizer(use_cloud=False)
            >>> 
            >>> # Use cloud Ollama
            >>> synthesizer = KnowledgeSynthesizer(use_cloud=True)
        """
        self.use_cloud = use_cloud
        self.config = get_config(use_cloud=use_cloud)
        
        if use_cloud:
            # Cloud configuration
            self.base_url = self.config.ollama_cloud_url
            self.model = self.config.ollama_model
            self.api_key = self.config.ollama_cloud_api_key
            print(f"Initialized KnowledgeSynthesizer with Cloud Ollama")
            print(f"  Endpoint: {self.base_url}")
            print(f"  Model: {self.model}")
        else:
            # Local configuration
            self.base_url = self.config.ollama_base_url
            self.model = self.config.ollama_model
            self.api_key = None
            print(f"Initialized KnowledgeSynthesizer with Local Ollama")
            print(f"  Endpoint: {self.base_url}")
            print(f"  Model: {self.model}")
    
    def _call_local_ollama(self, prompt: str) -> str:
        """
        Call local Ollama API for synthesis.
        
        Args:
            prompt: The formatted prompt to send to Ollama.
        
        Returns:
            The synthesized text response.
        
        Raises:
            OllamaConnectionError: If connection fails.
            OllamaAPIError: If API returns an error.
        """
        endpoint = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            print(f"Calling local Ollama at {endpoint}...")
            response = requests.post(
                endpoint,
                json=payload,
                timeout=300  # 5 minute timeout for long responses
            )
            response.raise_for_status()
            
            result = response.json()
            synthesized_text = result.get("response", "")
            
            if not synthesized_text:
                raise OllamaAPIError("Empty response from Ollama")
            
            print(f"Synthesis complete: {len(synthesized_text)} characters")
            return synthesized_text
            
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError(
                f"Failed to connect to local Ollama at {self.base_url}. "
                f"Ensure Ollama is running: 'ollama serve'"
            ) from e
        except requests.exceptions.Timeout as e:
            raise OllamaConnectionError(
                f"Request to Ollama timed out after 300 seconds"
            ) from e
        except requests.exceptions.HTTPError as e:
            raise OllamaAPIError(
                f"Ollama API returned HTTP error: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise OllamaAPIError(
                f"Unexpected error calling Ollama: {e}"
            ) from e
    
    def _call_cloud_ollama(self, prompt: str) -> str:
        """
        Call cloud Ollama API for synthesis.
        
        NOTE: This endpoint is a PLACEHOLDER and needs verification from
        official Ollama Cloud documentation. The actual endpoint and payload
        structure may differ.
        
        Args:
            prompt: The formatted prompt to send to Ollama Cloud.
        
        Returns:
            The synthesized text response.
        
        Raises:
            OllamaConnectionError: If connection fails.
            OllamaAPIError: If API returns an error.
        """
        # NOTE: This URL is a PLACEHOLDER - verify from official Ollama Cloud documentation
        endpoint = f"{self.base_url}/chat/completions"
        
        # NOTE: This payload structure is based on OpenAI-compatible format
        # Verify the exact structure from Ollama Cloud documentation
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"Calling Ollama Cloud at {endpoint}...")
            print("NOTE: Cloud endpoint is a placeholder - verify from official documentation")
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=300  # 5 minute timeout for long responses
            )
            response.raise_for_status()
            
            result = response.json()
            
            # NOTE: Response structure may vary - verify from documentation
            # Assuming OpenAI-compatible format
            if "choices" in result and len(result["choices"]) > 0:
                synthesized_text = result["choices"][0].get("message", {}).get("content", "")
            else:
                synthesized_text = result.get("response", "")
            
            if not synthesized_text:
                raise OllamaAPIError("Empty response from Ollama Cloud")
            
            print(f"Synthesis complete: {len(synthesized_text)} characters")
            return synthesized_text
            
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError(
                f"Failed to connect to Ollama Cloud at {self.base_url}. "
                f"Check your internet connection and API key."
            ) from e
        except requests.exceptions.Timeout as e:
            raise OllamaConnectionError(
                f"Request to Ollama Cloud timed out after 300 seconds"
            ) from e
        except requests.exceptions.HTTPError as e:
            raise OllamaAPIError(
                f"Ollama Cloud API returned HTTP error: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise OllamaAPIError(
                f"Unexpected error calling Ollama Cloud: {e}"
            ) from e
    
    def synthesize(
        self,
        transcript: str,
        prompt_template: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesize knowledge from a transcript.
        
        This method takes a transcript and uses Ollama to extract structured
        knowledge based on a prompt template or custom prompt.
        
        Args:
            transcript: The transcript text to synthesize.
            prompt_template: Optional template key (e.g., "basic_summary", "meeting_minutes").
                           If None, uses default from config.
            custom_prompt: Optional custom prompt text. If provided, overrides prompt_template.
        
        Returns:
            Dictionary containing:
                - raw_text: The synthesized text
                - model_used: The model name used
                - template_used: The template key used (or "custom")
                - transcript_length: Length of input transcript
                - synthesis_length: Length of synthesized output
        
        Raises:
            PromptTemplateError: If prompt template is invalid.
            SynthesizerError: If synthesis fails.
        
        Example:
            >>> synthesizer = KnowledgeSynthesizer(use_cloud=False)
            >>> result = synthesizer.synthesize(transcript, "meeting_minutes")
            >>> print(result["raw_text"])
            Meeting Overview...
        """
        # Validate transcript
        if not transcript or not transcript.strip():
            raise SynthesizerError("Transcript cannot be empty")
        
        transcript_length = len(transcript)
        print(f"\nSynthesizing knowledge from transcript ({transcript_length} characters)...")
        
        # Determine which prompt to use
        if custom_prompt:
            # Use custom prompt directly
            formatted_prompt = custom_prompt
            template_key = "custom"
            print("Using custom prompt")
        elif prompt_template:
            # Use specified template
            formatted_prompt = format_template(prompt_template, transcript)
            template_key = prompt_template
            print(f"Using prompt template: {prompt_template}")
        else:
            # Use default template from config
            default_template = self.config.default_synthesis_prompt_template
            formatted_prompt = format_template(default_template, transcript)
            template_key = default_template
            print(f"Using default prompt template: {default_template}")
        
        # Call appropriate Ollama endpoint
        try:
            if self.use_cloud:
                synthesized_text = self._call_cloud_ollama(formatted_prompt)
            else:
                synthesized_text = self._call_local_ollama(formatted_prompt)
        except (OllamaConnectionError, OllamaAPIError) as e:
            raise SynthesizerError(f"Synthesis failed: {e}") from e
        
        # Return structured result
        result = {
            "raw_text": synthesized_text,
            "model_used": self.model,
            "template_used": template_key,
            "transcript_length": transcript_length,
            "synthesis_length": len(synthesized_text),
            "use_cloud": self.use_cloud
        }
        
        return result
    
    def test_connection(self) -> bool:
        """
        Test the connection to Ollama.
        
        Returns:
            True if connection is successful, False otherwise.
        
        Example:
            >>> synthesizer = KnowledgeSynthesizer(use_cloud=False)
            >>> if synthesizer.test_connection():
            ...     print("Connection successful!")
        """
        try:
            if self.use_cloud:
                # For cloud, we can't easily test without making a real request
                # Just check if we have an API key
                return bool(self.api_key)
            else:
                # For local, check if Ollama is running
                endpoint = f"{self.base_url}/api/tags"
                response = requests.get(endpoint, timeout=10)
                response.raise_for_status()
                return True
        except Exception:
            return False