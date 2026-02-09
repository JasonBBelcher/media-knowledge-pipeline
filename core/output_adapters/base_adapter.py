"""
Base Adapter for Output Transformation

Defines the abstract base class for all output adapters.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class OutputAdapter(ABC):
    """
    Abstract base class for output adapters.
    
    Adapters transform pipeline output to specific formats for different targets
    (Anki, Notion, Obsidian, etc.).
    """
    
    @abstractmethod
    def transform(self, pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform pipeline output to target format.
        
        Args:
            pipeline_output: Dictionary containing pipeline results
            
        Returns:
            Dictionary in target format
        """
        pass
        
    @abstractmethod
    def validate(self, transformed_output: Dict[str, Any]) -> bool:
        """
        Validate transformed output structure.
        
        Args:
            transformed_output: Dictionary in target format
            
        Returns:
            True if valid, False otherwise
        """
        pass