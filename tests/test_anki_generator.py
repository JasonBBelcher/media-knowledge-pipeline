"""
Test suite for Anki generator functionality.
Following Test-Driven Development (TDD) principles.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from core.anki_generator import AnkiGenerator, AnkiGeneratorError, AnkiNoteModel


class TestAnkiNoteModel:
    """Test cases for Anki note models."""

    def test_model_creation(self):
        """Test that all note models can be created."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki") as mock_genanki:
                # Mock the Model class
                mock_model = Mock()
                mock_model.name = "Concept Definition Model"
                mock_model.fields = [{"name": "field1"}] * 5
                mock_genanki.Model.return_value = mock_model
                
                # Test concept definition model
                concept_model = AnkiNoteModel.get_concept_definition_model()
                assert concept_model.name == "Concept Definition Model"
                
                # Test Q&A pair model
                mock_model.name = "Q&A Pair Model"
                qa_model = AnkiNoteModel.get_q_a_pair_model()
                assert qa_model.name == "Q&A Pair Model"
                
                # Test event date model
                mock_model.name = "Timeline/Event Model"
                event_model = AnkiNoteModel.get_event_date_model()
                assert event_model.name == "Timeline/Event Model"
                
                # Test step in process model
                mock_model.name = "Process Step Model"
                step_model = AnkiNoteModel.get_step_in_process_model()
                assert step_model.name == "Process Step Model"


class TestAnkiGenerator:
    """Test cases for Anki generator functionality."""

    def test_generator_initialization(self):
        """Test that AnkiGenerator can be instantiated."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki"):
                generator = AnkiGenerator("Test Deck")
                assert isinstance(generator, AnkiGenerator)
                assert generator.deck_name == "Test Deck"

    def test_generator_without_genanki(self):
        """Test that AnkiGenerator raises error when genanki is not available."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", False):
            with pytest.raises(AnkiGeneratorError, match="genanki library not available"):
                AnkiGenerator("Test Deck")

    def test_prepare_fields_for_concept_definition(self):
        """Test field preparation for concept definition items."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki"):
                generator = AnkiGenerator("Test Deck")
                
                item = {
                    "concept": "Machine Learning",
                    "definition": "A method of data analysis",
                    "context": "Chapter 3 discussion",
                    "examples": ["Email spam detection", "Image recognition"],
                    "tags": ["AI", "algorithms"]
                }
                
                fields = generator._prepare_fields_for_item(item, "concept_definition")
                assert fields[0] == "Machine Learning"
                assert fields[1] == "A method of data analysis"
                assert fields[2] == "Chapter 3 discussion"
                assert "Email spam detection" in fields[3]
                assert "AI" in fields[4]

    def test_prepare_fields_for_qa_pair(self):
        """Test field preparation for Q&A pair items."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki"):
                generator = AnkiGenerator("Test Deck")
                
                item = {
                    "question": "What is supervised learning?",
                    "answer": "Learning with labeled data",
                    "explanation": "Uses input-output pairs",
                    "source_timestamp": "00:15:23",
                    "tags": ["ML", "supervised"]
                }
                
                fields = generator._prepare_fields_for_item(item, "q_a_pair")
                assert fields[0] == "What is supervised learning?"
                assert fields[1] == "Learning with labeled data"
                assert fields[2] == "Uses input-output pairs"
                assert fields[3] == "00:15:23"
                assert fields[4] == "ML, supervised"

    def test_generate_deck_id_consistency(self):
        """Test that deck ID generation is consistent."""
        with patch("core.anki_generator.GENANKI_AVAILABLE", True):
            with patch("core.anki_generator.genanki"):
                generator = AnkiGenerator("Test Deck")
                
                id1 = generator._generate_deck_id("Same Deck Name")
                id2 = generator._generate_deck_id("Same Deck Name")
                
                # Should be the same for the same name
                assert id1 == id2
                
                id3 = generator._generate_deck_id("Different Deck Name")
                
                # Should be different for different names
                assert id1 != id3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])