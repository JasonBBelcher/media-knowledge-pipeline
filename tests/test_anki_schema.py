"""
Test suite for Anki schema validation.
Following Test-Driven Development (TDD) principles.
"""
import pytest
from core.output_adapters.anki_schema import validate_anki_content, ANKI_FLASHCARD_SCHEMA


class TestAnkiSchema:
    """Test cases for Anki schema validation."""

    def test_valid_anki_content(self):
        """Test that valid Anki content passes validation."""
        valid_data = {
            "metadata": {
                "source_title": "Test Video"
            },
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "concept_definition",
                    "priority": "high",
                    "tags": ["test"],
                    "concept": "Test Concept",
                    "definition": "A test definition"
                }
            ]
        }
        
        is_valid = validate_anki_content(valid_data)
        assert is_valid is True

    def test_invalid_missing_metadata(self):
        """Test that content missing metadata fails validation."""
        invalid_data = {
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "concept_definition",
                    "priority": "high",
                    "tags": ["test"],
                    "concept": "Test Concept",
                    "definition": "A test definition"
                }
            ]
        }
        
        is_valid = validate_anki_content(invalid_data)
        assert is_valid is False

    def test_invalid_wrong_card_type(self):
        """Test that content with invalid card type fails validation."""
        invalid_data = {
            "metadata": {
                "source_title": "Test Video"
            },
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "invalid_type",  # Invalid type
                    "priority": "high",
                    "tags": ["test"],
                    "concept": "Test Concept",
                    "definition": "A test definition"
                }
            ]
        }
        
        is_valid = validate_anki_content(invalid_data)
        assert is_valid is False

    def test_valid_qa_pair(self):
        """Test that valid Q&A pair passes validation."""
        valid_data = {
            "metadata": {
                "source_title": "Test Lecture"
            },
            "flashcard_content": [
                {
                    "id": "fc_002",
                    "type": "q_a_pair",
                    "priority": "medium",
                    "tags": ["ML", "supervised"],
                    "question": "What is supervised learning?",
                    "answer": "Learning with labeled training data."
                }
            ]
        }
        
        is_valid = validate_anki_content(valid_data)
        assert is_valid is True

    def test_invalid_priority_value(self):
        """Test that invalid priority value fails validation."""
        invalid_data = {
            "metadata": {
                "source_title": "Test Video"
            },
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "concept_definition",
                    "priority": "invalid",  # Invalid priority
                    "tags": ["test"],
                    "concept": "Test Concept",
                    "definition": "A test definition"
                }
            ]
        }
        
        is_valid = validate_anki_content(invalid_data)
        assert is_valid is False

    def test_empty_flashcard_content(self):
        """Test that empty flashcard content still passes validation."""
        valid_data = {
            "metadata": {
                "source_title": "Test Video"
            },
            "flashcard_content": []  # Empty but valid
        }
        
        is_valid = validate_anki_content(valid_data)
        assert is_valid is True

    def test_schema_structure(self):
        """Test that the schema itself has the expected structure."""
        # Check top-level properties
        assert "type" in ANKI_FLASHCARD_SCHEMA
        assert "properties" in ANKI_FLASHCARD_SCHEMA
        
        # Check required fields
        assert "metadata" in ANKI_FLASHCARD_SCHEMA["properties"]
        assert "flashcard_content" in ANKI_FLASHCARD_SCHEMA["properties"]
        
        # Check flashcard item schema
        flashcard_schema = ANKI_FLASHCARD_SCHEMA["properties"]["flashcard_content"]["items"]
        assert "oneOf" in flashcard_schema
        assert len(flashcard_schema["oneOf"]) == 4  # Four card types


if __name__ == "__main__":
    pytest.main([__file__, "-v"])