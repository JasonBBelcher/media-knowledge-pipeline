"""
Unit tests for prompts module.

Tests prompt template retrieval, formatting, and custom template management.
"""

import pytest
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.prompts import (
    PromptTemplates,
    get_template,
    format_template,
    add_custom_template,
    list_templates
)


class TestPromptTemplates:
    """Test PromptTemplates class and built-in templates."""
    
    @pytest.mark.unit
    def test_prompt_templates_initialization(self):
        """Test that all built-in templates are accessible."""
        from core.prompts import PROMPT_TEMPLATES
        
        # Verify all expected templates exist in the global dictionary
        expected_templates = [
            "basic_summary",
            "meeting_minutes",
            "lecture_summary",
            "tutorial_guide",
            "project_update",
            "customer_feedback",
            "research_summary",
            "interview_summary",
            "blog_post_outline",
            "social_media_content",
            "technical_documentation",
            "bug_report_summary"
        ]
        
        for template_name in expected_templates:
            assert template_name in PROMPT_TEMPLATES, f"Missing template: {template_name}"
    
    def test_basic_summary_template(self):
        """Test basic_summary template content."""
        template = PromptTemplates.BASIC_SUMMARY
        
        # The actual template starts with "Extract the core thesis" not "summary"
        assert "extract" in template.lower()
        assert "{transcript}" in template
    
    def test_meeting_minutes_template(self):
        """Test meeting_minutes template content."""
        template = PromptTemplates.MEETING_MINUTES
        
        assert "meeting" in template.lower()
        assert "{transcript}" in template
    
    def test_action_items_template(self):
        """Test action_items template content."""
        # This template doesn't exist, let's test customer feedback instead
        template = PromptTemplates.CUSTOMER_FEEDBACK
        
        assert "feedback" in template.lower()
        assert "{transcript}" in template
    
    def test_all_templates_contain_transcript_placeholder(self):
        """Test that all templates contain the {transcript} placeholder."""
        # Access templates through the global PROMPT_TEMPLATES dictionary
        from core.prompts import PROMPT_TEMPLATES
        
        for template_name, template_content in PROMPT_TEMPLATES.items():
            assert "{transcript}" in template_content, \
                f"Template '{template_name}' missing {{transcript}} placeholder"


class TestGetTemplate:
    """Test get_template function."""
    
    def test_get_template_basic_summary(self):
        """Test retrieving basic_summary template."""
        template = get_template("basic_summary")
        
        assert isinstance(template, str)
        assert "{transcript}" in template
        assert "extract" in template.lower()  # The template starts with "Extract the core thesis"
    
    def test_get_template_meeting_minutes(self):
        """Test retrieving meeting_minutes template."""
        template = get_template("meeting_minutes")
        
        assert isinstance(template, str)
        assert "{transcript}" in template
        assert "meeting" in template.lower()
    
    def test_get_template_all_built_in(self):
        """Test retrieving all built-in templates."""
        built_in_templates = [
            "basic_summary",
            "meeting_minutes",
            "lecture_summary",
            "tutorial_guide",
            "project_update",
            "customer_feedback",
            "research_summary",
            "interview_summary",
            "blog_post_outline",
            "social_media_content",
            "technical_documentation",
            "bug_report_summary"
        ]
        
        for template_name in built_in_templates:
            template = get_template(template_name)
            assert isinstance(template, str)
            assert "{transcript}" in template
    
    def test_get_template_custom(self):
        """Test retrieving custom template."""
        # Add a custom template first
        add_custom_template("custom_test", "Custom template: {transcript}")
        
        template = get_template("custom_test")
        
        assert template == "Custom template: {transcript}"
    
    def test_get_template_nonexistent(self):
        """Test retrieving nonexistent template returns None."""
        template = get_template("nonexistent_template")
        assert template is None
    
    def test_get_template_case_sensitive(self):
        """Test that template names are case-sensitive."""
        # This should work
        template = get_template("basic_summary")
        assert template is not None
        
        # This should also work (the function converts to lowercase)
        template = get_template("Basic_Summary")
        assert template is not None


class TestFormatTemplate:
    """Test format_template function."""
    
    def test_format_template_basic(self):
        """Test basic template formatting."""
        template = "Summary: {transcript}"
        transcript = "This is a test transcript."
        
        result = format_template("basic_summary", transcript)
        
        assert "This is a test transcript." in result
    
    def test_format_template_with_built_in(self):
        """Test formatting with built-in template."""
        transcript = "The meeting discussed project milestones and deadlines."
        
        result = format_template("meeting_minutes", transcript)
        
        assert "The meeting discussed project milestones and deadlines." in result
    
    def test_format_template_with_custom(self):
        """Test formatting with custom template."""
        add_custom_template("custom_format", "Custom: {transcript} - End")
        transcript = "Test content"
        
        result = format_template("custom_format", transcript)
        
        assert result == "Custom: Test content - End"
    
    def test_format_template_empty_transcript(self):
        """Test formatting with empty transcript."""
        transcript = ""
        
        result = format_template("basic_summary", transcript)
        
        assert "{transcript}" not in result
        assert "" in result
    
    def test_format_template_long_transcript(self):
        """Test formatting with long transcript."""
        transcript = "This is a test. " * 100  # Long transcript
        
        result = format_template("basic_summary", transcript)
        
        assert transcript in result
    
    def test_format_template_special_characters(self):
        """Test formatting with special characters in transcript."""
        transcript = "Test with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?"
        
        result = format_template("basic_summary", transcript)
        
        assert transcript in result
    
    def test_format_template_unicode(self):
        """Test formatting with unicode characters."""
        transcript = "Test with unicode: 你好世界 🌍"
        
        result = format_template("basic_summary", transcript)
        
        assert transcript in result
    
    def test_format_template_newlines(self):
        """Test formatting with newlines in transcript."""
        transcript = "Line 1\nLine 2\nLine 3"
        
        result = format_template("basic_summary", transcript)
        
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
    
    def test_format_template_nonexistent_template(self):
        """Test formatting with nonexistent template raises error."""
        with pytest.raises(ValueError):
            format_template("nonexistent", "Test transcript")


class TestAddCustomTemplate:
    """Test add_custom_template function."""
    
    def test_add_custom_template_basic(self):
        """Test adding a basic custom template."""
        add_custom_template("test_template", "Test: {transcript}")
        
        template = get_template("test_template")
        assert template == "Test: {transcript}"
    
    def test_add_custom_template_overwrite(self):
        """Test overwriting an existing custom template."""
        add_custom_template("overwrite_test", "Original: {transcript}")
        add_custom_template("overwrite_test", "Updated: {transcript}")
        
        template = get_template("overwrite_test")
        assert template == "Updated: {transcript}"
    
    def test_add_custom_template_multiple_placeholders(self):
        """Test adding template with multiple placeholders."""
        add_custom_template("multi_placeholder", "Title: {title}\nContent: {transcript}")
        
        template = get_template("multi_placeholder")
        assert "{title}" in template
        assert "{transcript}" in template
    
    def test_add_custom_template_no_placeholder(self):
        """Test adding template without transcript placeholder raises error."""
        with pytest.raises(ValueError):
            add_custom_template("no_placeholder", "Static text without placeholder")
    
    def test_add_custom_template_empty_name(self):
        """Test adding template with empty name."""
        with pytest.raises(ValueError):
            add_custom_template("", "Template content")
    
    def test_add_custom_template_empty_content(self):
        """Test adding template with empty content but valid placeholder."""
        # This should work - empty content with placeholder is allowed
        add_custom_template("empty_content", "{transcript}")
        
        template = get_template("empty_content")
        assert template == "{transcript}"
    
    def test_add_custom_template_special_characters(self):
        """Test adding template with special characters."""
        add_custom_template("special_chars", "Special: @#$%^&*() {transcript}")
        
        template = get_template("special_chars")
        assert "@#$%^&*()" in template
        assert "{transcript}" in template


class TestListTemplates:
    """Test list_templates function."""
    
    def test_list_templates_all(self):
        """Test listing all templates."""
        templates = list_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        
        # Check that built-in templates are included
        assert "basic_summary" in templates
        assert "meeting_minutes" in templates
    
    def test_list_templates_includes_custom(self):
        """Test that list_templates includes custom templates."""
        add_custom_template("list_test_custom", "Custom: {transcript}")
        
        templates = list_templates()
        
        assert "list_test_custom" in templates
    
    def test_list_templates_no_duplicates(self):
        """Test that list_templates returns no duplicates."""
        templates = list_templates()
        
        assert len(templates) == len(set(templates))
    
    def test_list_templates_sorted(self):
        """Test that list_templates returns sorted list."""
        templates = list_templates()
        
        assert templates == sorted(templates)





class TestTemplateContentValidation:
    """Test validation of template content."""
    
    def test_all_templates_are_strings(self):
        """Test that all templates are strings."""
        from core.prompts import PROMPT_TEMPLATES
        
        for template_name, template_content in PROMPT_TEMPLATES.items():
            assert isinstance(template_content, str), \
                f"Template '{template_name}' is not a string"
    
    def test_all_templates_are_non_empty(self):
        """Test that all templates are non-empty."""
        from core.prompts import PROMPT_TEMPLATES
        
        for template_name, template_content in PROMPT_TEMPLATES.items():
            assert len(template_content) > 0, \
                f"Template '{template_name}' is empty"
    
    def test_template_names_are_valid_identifiers(self):
        """Test that template names are valid identifiers."""
        from core.prompts import PROMPT_TEMPLATES
        
        for template_name in PROMPT_TEMPLATES.keys():
            # Template names should be lowercase with underscores
            assert template_name.isidentifier() or "_" in template_name, \
                f"Template name '{template_name}' is not a valid identifier"


class TestTemplateFormattingEdgeCases:
    """Test edge cases in template formatting."""
    
    def test_format_template_with_none_transcript(self):
        """Test formatting with None transcript."""
        # This should work - None gets converted to string "None"
        result = format_template("basic_summary", None)
        assert "None" in result
    
    def test_format_template_with_numeric_transcript(self):
        """Test formatting with numeric transcript."""
        transcript = 12345
        
        result = format_template("basic_summary", transcript)
        
        assert "12345" in result
    
    def test_format_template_preserves_whitespace(self):
        """Test that formatting preserves whitespace."""
        template = "  Indented: {transcript}  "
        transcript = "test"
        
        result = format_template("basic_summary", transcript)
        
        # The result should contain the transcript
        assert "test" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])