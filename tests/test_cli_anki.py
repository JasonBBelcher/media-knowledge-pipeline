"""
Test suite for Anki CLI commands.
Following Test-Driven Development (TDD) principles.
"""
import pytest
import subprocess
import sys
from pathlib import Path


class TestAnkiCLI:
    """Test cases for Anki CLI commands."""

    @pytest.fixture
    def sample_json_file(self):
        """Fixture providing path to sample JSON file."""
        return "sample_synthesis.json"
    
    @pytest.fixture
    def cli_command(self):
        """Fixture providing the base CLI command."""
        return [sys.executable, "-m", "src.media_knowledge.cli.app"]

    def test_cli_help(self, cli_command):
        """Test that CLI help command works."""
        # Test anki help
        result = subprocess.run(
            cli_command + ["anki", "--help"],
            capture_output=True,
            text=True,
            cwd=".",
        )
        
        assert result.returncode == 0
        assert "Generate Anki flashcards" in result.stdout
        assert "generate" in result.stdout
        assert "templates" in result.stdout
        assert "preview" in result.stdout

    def test_templates_command(self, cli_command):
        """Test that templates command works."""
        result = subprocess.run(
            cli_command + ["anki", "templates"],
            capture_output=True,
            text=True,
            cwd=".",
        )
        
        assert result.returncode == 0
        assert "Anki Flashcard Templates" in result.stdout
        assert "concept_definition" in result.stdout
        assert "q_a_pair" in result.stdout
        assert "event_date" in result.stdout
        assert "step_in_process" in result.stdout

    def test_preview_command(self, cli_command, sample_json_file):
        """Test that preview command works."""
        result = subprocess.run(
            cli_command + ["anki", "preview", "--input", sample_json_file],
            capture_output=True,
            text=True,
            cwd=".",
        )
        
        assert result.returncode == 0
        assert "Preview:" in result.stdout
        assert "Flashcards" in result.stdout
        # Check that we see flashcard content in preview
        assert "Concept:" in result.stdout or "Question:" in result.stdout

    def test_generate_command_help(self, cli_command):
        """Test that generate command help works."""
        result = subprocess.run(
            cli_command + ["anki", "generate", "--help"],
            capture_output=True,
            text=True,
            cwd=".",
        )
        
        assert result.returncode == 0
        assert "Generate Anki flashcards" in result.stdout
        assert "--input" in result.stdout
        assert "--output" in result.stdout
        assert "--deck-name" in result.stdout

    def test_generate_command_invalid_input(self, cli_command):
        """Test that generate command handles invalid input gracefully."""
        result = subprocess.run(
            cli_command + ["anki", "generate", "--input", "nonexistent.json"],
            capture_output=True,
            text=True,
            cwd=".",
        )
        
        assert result.returncode != 0
        assert "not found" in result.stdout or "not found" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])