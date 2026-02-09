"""
Anki Adapter for Output Transformation

Transforms pipeline output to Anki flashcard format.
"""
from typing import Dict, Any, List
from .base_adapter import OutputAdapter
from .anki_schema import validate_anki_content


class AnkiAdapter(OutputAdapter):
    """
    Adapter for transforming pipeline output to Anki flashcard format.
    
    Maps synthesis content to different flashcard types:
    - Concept definitions
    - Q&A pairs  
    - Event dates
    - Process steps
    """
    
    def __init__(self):
        """Initialize the Anki adapter."""
        self.content_types = {
            "concept_definition",
            "q_a_pair", 
            "event_date",
            "step_in_process"
        }
        
    def transform(self, pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform pipeline output to Anki flashcard structure.
        
        Args:
            pipeline_output: Dictionary containing pipeline results
            
        Returns:
            Dictionary in Anki flashcard format
        """
        # Extract relevant content from pipeline output
        synthesis = pipeline_output.get("synthesis", {})
        raw_text = synthesis.get("raw_text", "")
        
        # Try to extract structured flashcard content first
        flashcard_content = self._extract_structured_content(pipeline_output)
        
        # If no structured content, classify from raw text
        if not flashcard_content:
            flashcard_content = self._classify_content_from_text(raw_text)
            
        return {
            "metadata": self._extract_metadata(pipeline_output),
            "flashcard_content": flashcard_content
        }
        
    def validate(self, transformed_output: Dict[str, Any]) -> bool:
        """
        Validate Anki-specific output structure using JSON schema.
        
        Args:
            transformed_output: Dictionary in Anki format
            
        Returns:
            True if valid, False otherwise
        """
        return validate_anki_content(transformed_output)
        
    def _extract_structured_content(self, pipeline_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract structured flashcard content from pipeline output.
        
        Args:
            pipeline_output: Dictionary containing pipeline results
            
        Returns:
            List of flashcard content dictionaries
        """
        # Check if pipeline output already contains flashcard structure
        if "flashcard_content" in pipeline_output:
            return pipeline_output["flashcard_content"]
            
        # Check if synthesis contains structured content
        synthesis = pipeline_output.get("synthesis", {})
        if "flashcard_content" in synthesis:
            return synthesis["flashcard_content"]
            
        return []
        
    def _classify_content_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Classify content from raw text using heuristic rules.
        
        Args:
            text: Raw synthesis text
            
        Returns:
            List of classified flashcard items
        """
        # This is a simplified implementation
        # In practice, this would use more sophisticated NLP techniques
        flashcards = []
        
        # Split text into paragraphs for basic classification
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            # Simple heuristics for content type classification
            if '?' in paragraph and ':' in paragraph:
                # Likely Q&A pair
                parts = paragraph.split(':', 1)
                if len(parts) == 2:
                    flashcards.append({
                        "id": f"fc_{i:03d}",
                        "type": "q_a_pair",
                        "priority": "medium",
                        "tags": ["auto-generated"],
                        "question": parts[0].strip().rstrip('?'),
                        "answer": parts[1].strip()
                    })
            elif any(keyword in paragraph.lower() for keyword in [" is ", " means ", " refers to "]):
                # Likely concept definition
                flashcards.append({
                    "id": f"fc_{i:03d}",
                    "type": "concept_definition", 
                    "priority": "medium",
                    "tags": ["auto-generated"],
                    "concept": paragraph.split()[0] if paragraph.split() else "Concept",
                    "definition": paragraph
                })
            else:
                # Default to concept definition
                flashcards.append({
                    "id": f"fc_{i:03d}",
                    "type": "concept_definition",
                    "priority": "low", 
                    "tags": ["auto-generated"],
                    "concept": f"Content Point {i+1}",
                    "definition": paragraph
                })
                
        return flashcards
        
    def _extract_metadata(self, pipeline_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata from pipeline output.
        
        Args:
            pipeline_output: Dictionary containing pipeline results
            
        Returns:
            Dictionary of metadata
        """
        metadata = pipeline_output.get("metadata", {})
        
        # Add default metadata if not present
        if "source_title" not in metadata:
            metadata["source_title"] = "Unknown Source"
            
        if "processing_date" not in metadata:
            from datetime import datetime
            metadata["processing_date"] = datetime.now().isoformat()
            
        return metadata
        
    def _validate_flashcard_item(self, item: Dict[str, Any]) -> bool:
        """
        Validate a single flashcard item structure.
        
        Args:
            item: Flashcard item dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["id", "type", "priority"]
        if not all(field in item for field in required_fields):
            return False
            
        if item["type"] not in self.content_types:
            return False
            
        return True