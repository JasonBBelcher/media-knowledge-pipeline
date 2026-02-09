"""
Integration test for Anki adapter and generator working together.
Following Test-Driven Development (TDD) principles.
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from core.output_adapters.anki_adapter import AnkiAdapter
from core.anki_generator import AnkiGenerator, AnkiGeneratorError


class TestAnkiIntegration:
    """Test cases for Anki adapter and generator integration."""

    def test_adapter_to_generator_flow(self):
        """Test the complete flow from adapter to generator."""
        # Sample pipeline output
        pipeline_output = {
            "metadata": {
                "source_title": "Test Video Lecture",
                "source_type": "video"
            },
            "synthesis": {
                "raw_text": "Machine learning is a method of data analysis. What is supervised learning: Learning with labeled data.",
                "flashcard_content": [
                    {
                        "id": "fc_001",
                        "type": "concept_definition",
                        "priority": "high",
                        "tags": ["ML", "basics"],
                        "concept": "Machine Learning",
                        "definition": "A method of data analysis that automates analytical model building."
                    },
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
        }
        
        # Test adapter transformation
        adapter = AnkiAdapter()
        anki_ready_data = adapter.transform(pipeline_output)
        
        # Verify adapter output
        assert "metadata" in anki_ready_data
        assert "flashcard_content" in anki_ready_data
        assert len(anki_ready_data["flashcard_content"]) == 2
        
        # Test generator with mocked genanki
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki") as mock_genanki:
                # Mock the required genanki classes
                mock_deck = Mock()
                mock_package = Mock()
                
                mock_genanki.Deck.return_value = mock_deck
                mock_genanki.Package.return_value = mock_package
                
                # Create generator and generate deck
                generator = AnkiGenerator("Test Integration Deck")
                output_path = generator.generate_deck_from_json(anki_ready_data)
                
                # Verify genanki was called correctly
                mock_genanki.Deck.assert_called_once()
                mock_genanki.Package.assert_called_once_with(mock_deck)
                mock_package.write_to_file.assert_called_once()

    def test_full_flow_without_structured_content(self):
        """Test full flow when pipeline output lacks structured flashcard content."""
        # Sample pipeline output without flashcard structure
        pipeline_output = {
            "metadata": {
                "source_title": "Test Video"
            },
            "synthesis": {
                "raw_text": "What is machine learning: A method of data analysis.\n\nSupervised learning means using labeled data."
            }
        }
        
        # Test adapter transformation (will use heuristic classification)
        adapter = AnkiAdapter()
        anki_ready_data = adapter.transform(pipeline_output)
        
        # Verify adapter created flashcard content through classification
        assert "flashcard_content" in anki_ready_data
        assert len(anki_ready_data["flashcard_content"]) > 0
        
        # Verify content was classified
        flashcard = anki_ready_data["flashcard_content"][0]
        assert "id" in flashcard
        assert "type" in flashcard
        assert "tags" in flashcard

    def test_integration_validation(self):
        """Test that integrated output passes validation."""
        # Sample pipeline output
        pipeline_output = {
            "metadata": {
                "source_title": "Validation Test"
            },
            "synthesis": {
                "raw_text": "Test content",
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
        }
        
        # Test adapter transformation
        adapter = AnkiAdapter()
        anki_ready_data = adapter.transform(pipeline_output)
        
        # Verify adapter validation
        is_valid = adapter.validate(anki_ready_data)
        assert is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])