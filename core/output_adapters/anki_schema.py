"""
JSON Schema for Anki flashcard content validation.
"""
from typing import Dict, Any


# JSON Schema for Anki flashcard content validation
ANKI_FLASHCARD_SCHEMA = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "object",
            "properties": {
                "source_title": {"type": "string"},
                "source_type": {"type": "string"},
                "processing_date": {"type": "string"}
            },
            "required": ["source_title"]
        },
        "flashcard_content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["concept_definition", "q_a_pair", "event_date", "step_in_process"]
                    },
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["id", "type", "priority", "tags"],
                "oneOf": [
                    {
                        "properties": {
                            "type": {"const": "concept_definition"},
                            "concept": {"type": "string"},
                            "definition": {"type": "string"},
                            "context": {"type": "string"},
                            "examples": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["concept", "definition"]
                    },
                    {
                        "properties": {
                            "type": {"const": "q_a_pair"},
                            "question": {"type": "string"},
                            "answer": {"type": "string"},
                            "explanation": {"type": "string"},
                            "source_timestamp": {"type": "string"}
                        },
                        "required": ["question", "answer"]
                    },
                    {
                        "properties": {
                            "type": {"const": "event_date"},
                            "event": {"type": "string"},
                            "date": {"type": "string"},
                            "significance": {"type": "string"},
                            "key_figures": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["event", "date", "significance"]
                    },
                    {
                        "properties": {
                            "type": {"const": "step_in_process"},
                            "process": {"type": "string"},
                            "step_number": {"type": "integer"},
                            "step": {"type": "string"},
                            "detail": {"type": "string"}
                        },
                        "required": ["process", "step_number", "step"]
                    }
                ]
            }
        }
    },
    "required": ["metadata", "flashcard_content"]
}


def validate_anki_content(data: Dict[str, Any]) -> bool:
    """
    Validate Anki content against schema.
    
    Args:
        data: Dictionary containing Anki flashcard content
        
    Returns:
        True if valid, False otherwise
    """
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=ANKI_FLASHCARD_SCHEMA)
        return True
    except ImportError:
        # If jsonschema not available, do basic validation
        return _basic_validation(data)
    except jsonschema.ValidationError:
        return False


def _basic_validation(data: Dict[str, Any]) -> bool:
    """
    Basic validation when jsonschema is not available.
    
    Args:
        data: Dictionary containing Anki flashcard content
        
    Returns:
        True if valid, False otherwise
    """
    # Check required top-level keys
    if "metadata" not in data or "flashcard_content" not in data:
        return False
        
    # Check metadata
    metadata = data["metadata"]
    if "source_title" not in metadata:
        return False
        
    # Check flashcard content array
    flashcards = data["flashcard_content"]
    if not isinstance(flashcards, list):
        return False
        
    # Check each flashcard
    valid_types = {"concept_definition", "q_a_pair", "event_date", "step_in_process"}
    for card in flashcards:
        # Check required fields
        required_fields = {"id", "type", "priority", "tags"}
        if not all(field in card for field in required_fields):
            return False
            
        # Check valid type
        if card["type"] not in valid_types:
            return False
            
        # Check priority
        if card["priority"] not in {"high", "medium", "low"}:
            return False
            
        # Check tags
        if not isinstance(card["tags"], list):
            return False
            
    return True