"""
Test suite for Anki adapter functionality.
Following Test-Driven Development (TDD) principles.
"""
import pytest
from typing import Dict, Any
from core.output_adapters.anki_adapter import AnkiAdapter


class TestAnkiAdapter:
    """Test cases for Anki adapter functionality."""

    def test_adapter_initialization(self):
        """Test that AnkiAdapter can be instantiated."""
        adapter = AnkiAdapter()
        assert isinstance(adapter, AnkiAdapter)
        
    def test_transform_with_structured_content(self):
        """Test transformation of pipeline output with structured flashcard content."""
        adapter = AnkiAdapter()
        
        # Sample pipeline output with structured content
        pipeline_output = {
            "metadata": {
                "source_title": "Test Video",
                "source_type": "video"
            },
            "synthesis": {
                "raw_text": "Sample synthesis content",
                "flashcard_content": [
                    {
                        "id": "fc_001",
                        "type": "concept_definition",
                        "priority": "high",
                        "tags": ["test"],
                        "concept": "Test Concept",
                        "definition": "A test concept definition"
                    }
                ]
            }
        }
        
        result = adapter.transform(pipeline_output)
        
        # Verify result structure
        assert "metadata" in result
        assert "flashcard_content" in result
        assert len(result["flashcard_content"]) == 1
        
        # Verify flashcard content
        flashcard = result["flashcard_content"][0]
        assert flashcard["id"] == "fc_001"
        assert flashcard["type"] == "concept_definition"
        assert flashcard["concept"] == "Test Concept"
        
    def test_transform_with_raw_text_classification(self):
        """Test transformation with automatic classification from raw text."""
        adapter = AnkiAdapter()
        
        # Sample pipeline output without structured content
        pipeline_output = {
            "metadata": {
                "source_title": "Test Video"
            },
            "synthesis": {
                "raw_text": "What is machine learning: A method of data analysis.\n\nSupervised learning means using labeled data."
            }
        }
        
        result = adapter.transform(pipeline_output)
        
        # Verify result structure
        assert "metadata" in result
        assert "flashcard_content" in result
        assert len(result["flashcard_content"]) > 0
        
    def test_validation_success(self):
        """Test validation of correctly structured Anki output."""
        adapter = AnkiAdapter()
        
        valid_output = {
            "metadata": {
                "source_title": "Test Source"
            },
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "concept_definition",
                    "priority": "high",
                    "tags": ["test"],
                    "concept": "Test Concept",
                    "definition": "Test definition"
                }
            ]
        }
        
        is_valid = adapter.validate(valid_output)
        assert is_valid is True
        
    def test_validation_failure_missing_keys(self):
        """Test validation failure with missing required keys."""
        adapter = AnkiAdapter()
        
        invalid_output = {
            "flashcard_content": []  # Missing metadata
        }
        
        is_valid = adapter.validate(invalid_output)
        assert is_valid is False
        
    def test_validation_failure_invalid_type(self):
        """Test validation failure with invalid flashcard type."""
        adapter = AnkiAdapter()
        
        invalid_output = {
            "metadata": {},
            "flashcard_content": [
                {
                    "id": "fc_001",
                    "type": "invalid_type",  # Invalid type
                    "priority": "high"
                }
            ]
        }
        
        is_valid = adapter.validate(invalid_output)
        assert is_valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])