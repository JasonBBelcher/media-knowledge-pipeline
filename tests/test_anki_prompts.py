"""
Test suite for Anki prompt templates.
Following Test-Driven Development (TDD) principles.
"""
import pytest
from core.prompts import PromptTemplates, format_template, get_template, list_templates


class TestAnkiPrompts:
    """Test cases for Anki prompt templates."""

    def test_anki_flashcards_template_exists(self):
        """Test that the Anki flashcards template exists."""
        # Check that the template attribute exists
        assert hasattr(PromptTemplates, "ANKI_FLASHCARDS")
        
        # Check that it's in the template dictionary
        template = get_template("anki_flashcards")
        assert template is not None
        assert "knowledge extraction assistant" in template
        assert "flashcard content array" in template
        
    def test_anki_flashcards_in_template_list(self):
        """Test that anki_flashcards is in the list of templates."""
        templates = list_templates()
        assert "anki_flashcards" in templates
        
    def test_anki_flashcards_formatting(self):
        """Test that the Anki flashcards template can be formatted with a transcript."""
        sample_transcript = "Machine learning is a method of data analysis that automates analytical model building."
        
        formatted_prompt = format_template("anki_flashcards", sample_transcript)
        
        # Verify the prompt contains key elements
        assert formatted_prompt is not None
        assert "knowledge extraction assistant" in formatted_prompt
        assert sample_transcript in formatted_prompt
        assert "CATEGORIZE it as exactly one of" in formatted_prompt
        assert "Return ONLY valid JSON" in formatted_prompt
        
    def test_anki_flashcards_template_structure(self):
        """Test that the Anki flashcards template has the required structure."""
        template = get_template("anki_flashcards")
        
        # Check that template exists
        assert template is not None
        
        # Check for key instruction elements
        assert "CATEGORIZE it as exactly one of" in template
        assert "concept_definition" in template
        assert "q_a_pair" in template
        assert "event_date" in template
        assert "step_in_process" in template
        
        # Check for JSON structure requirement
        assert "Return ONLY valid JSON" in template
        assert "flashcard content array" in template
        
        # Check for field requirements
        assert "concept, definition" in template
        assert "question, answer" in template
        assert "event, date" in template
        assert "process, step_number" in template


if __name__ == "__main__":
    pytest.main([__file__, "-v"])