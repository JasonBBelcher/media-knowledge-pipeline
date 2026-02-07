"""
Token Counter Utilities

Provides token counting functionality for text content to enable
intelligent model selection based on content volume.
"""

from typing import List, Dict, Any, Optional
import re


class TokenCounter:
    """Counts tokens in text content for model selection."""
    
    # Approximate token-to-character ratios for different models
    # These are rough estimates since actual tokenization varies by model
    TOKEN_RATIOS = {
        'llama3.1:8b': 4.0,      # ~4 chars per token
        'llama3.1:70b': 4.0,
        'mistral:7b': 4.2,
        'deepseek-v3.1:671b': 3.8,
        'gpt-oss:120b': 4.1,
    }
    
    # Model context window limits (tokens)
    CONTEXT_LIMITS = {
        'llama3.1:8b': 8000,
        'llama3.1:70b': 32000,
        'mistral:7b': 12000,
        'deepseek-v3.1:671b': 65000,
        'gpt-oss:120b': 128000,
    }
    
    def __init__(self):
        """Initialize token counter."""
        pass
    
    def format_token_summary(self, token_count: int) -> str:
        """
        Format token count for display.
        
        Args:
            token_count: Number of tokens
            
        Returns:
            Formatted string representation
        """
        if token_count >= 1000000:
            return f"{token_count/1000000:.1f}M tokens"
        elif token_count >= 1000:
            return f"{token_count/1000:.1f}K tokens"
        else:
            return f"{token_count} tokens"
    
    def estimate_tokens_from_text(self, text: str, model: str = 'llama3.1:8b') -> int:
        """
        Estimate token count from text using character-based approximation.
        
        Args:
            text: Text content to count tokens for
            model: Model name to use for estimation
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Get ratio for model (default to llama3.1:8b if not found)
        ratio = self.TOKEN_RATIOS.get(model, 4.0)
        
        # Estimate tokens based on character count and ratio
        return max(1, int(len(text) / ratio))
    
    def count_tokens_from_results(self, synthesis_results: List[Dict], 
                                model: str = 'llama3.1:8b') -> int:
        """
        Count total tokens from synthesis results.
        
        Args:
            synthesis_results: List of synthesis result dictionaries
            model: Model name to use for estimation
            
        Returns:
            Total estimated token count
        """
        total_tokens = 0
        
        for result in synthesis_results:
            if result.get("status") == "success":
                synthesis_data = result.get("synthesis", {})
                if isinstance(synthesis_data, dict):
                    raw_text = synthesis_data.get("raw_text", "")
                    if raw_text:
                        total_tokens += self.estimate_tokens_from_text(raw_text, model)
                elif isinstance(synthesis_data, str):
                    # If synthesis is directly a string
                    total_tokens += self.estimate_tokens_from_text(synthesis_data, model)
        
        return total_tokens
    
    def recommend_model(self, token_count: int) -> Dict[str, Any]:
        """
        Recommend appropriate model based on token count.
        
        Args:
            token_count: Number of tokens to process
            
        Returns:
            Dictionary with model recommendation and details
        """
        recommendations = [
            # Small models (local)
            {
                'max_tokens': 8000,
                'model': 'llama3.1:8b',
                'type': 'local',
                'warning': None
            },
            # Medium models (cloud)  
            {
                'max_tokens': 12000,
                'model': 'mistral:7b',
                'type': 'cloud',
                'warning': 'Switching to cloud model for extended context'
            },
            # Large models (cloud)
            {
                'max_tokens': 32000,
                'model': 'llama3.1:70b',
                'type': 'cloud',
                'warning': 'Using high-capacity cloud model for large content'
            },
            # Very large models (cloud)
            {
                'max_tokens': 65000,
                'model': 'deepseek-v3.1:671b',
                'type': 'cloud',
                'warning': 'Using ultra-high capacity model for extensive content'
            }
        ]
        
        # Find appropriate recommendation
        for rec in recommendations:
            if token_count <= rec['max_tokens']:
                return rec
        
        # Content too large
        return {
            'model': None,
            'type': 'cloud',
            'warning': 'Content exceeds maximum context window. Consider manual batching.',
            'error': 'CONTENT_TOO_LARGE'
        }


def test_token_counter():
    """Test token counter functionality."""
    counter = TokenCounter()
    
    # Test basic token estimation
    test_text = "This is a sample text for token counting. " * 100
    tokens = counter.estimate_tokens_from_text(test_text)
    print(f"Estimated tokens: {tokens}")
    
    # Test model recommendation
    recommendation = counter.recommend_model(15000)
    print(f"Model recommendation: {recommendation}")
    
    # Test token formatting
    formatted = counter.format_token_summary(25000)
    print(f"Formatted token count: {formatted}")
    
    return True


if __name__ == "__main__":
    test_token_counter()