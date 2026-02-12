"""
Integration tests for Anki menu option in legacy interactive frontend
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.media_knowledge.cli.frontend.anki_wizard import AnkiWizard

class TestAnkiMenuIntegration:
    """Test Anki menu integration in legacy system."""
    
    def test_anki_wizard_initialization(self):
        """Test that AnkiWizard initializes correctly."""
        wizard = AnkiWizard()
        assert wizard is not None
    
    def test_get_json_source_valid(self):
        """Test valid JSON source input."""
        wizard = AnkiWizard()
        
        # Mock valid JSON file input
        with patch('builtins.input', return_value='/path/to/results.json'):
            with patch('pathlib.Path.exists', return_value=True):
                with patch('pathlib.Path.is_file', return_value=True):
                    result = wizard.get_json_source()
                    assert result == '/path/to/results.json'
    
    def test_get_json_source_invalid_then_valid(self):
        """Test invalid then valid JSON source input."""
        wizard = AnkiWizard()
        
        # Mock invalid then valid input
        with patch('builtins.input', side_effect=['invalid.txt', '/path/to/results.json']):
            with patch('pathlib.Path.exists', side_effect=[False, True]):
                with patch('pathlib.Path.is_file', return_value=True):
                    with patch('builtins.print') as mock_print:
                        result = wizard.get_json_source()
                        assert result == '/path/to/results.json'
    
    def test_get_deck_name_default(self):
        """Test deck name with default (empty input)."""
        wizard = AnkiWizard()
        
        # Mock empty input for deck name
        with patch('builtins.input', return_value=''):
            result = wizard.get_deck_name('/path/to/results.json')
            assert result == 'Results'
    
    def test_get_deck_name_custom(self):
        """Test deck name with custom input."""
        wizard = AnkiWizard()
        
        # Mock custom deck name input
        with patch('builtins.input', return_value='My Custom Deck'):
            result = wizard.get_deck_name('/path/to/results.json')
            assert result == 'My Custom Deck'
    
    def test_preview_or_generate_preview(self):
        """Test preview option selection."""
        wizard = AnkiWizard()
        
        # Mock preview selection
        with patch('builtins.input', return_value='1'):
            result = wizard.preview_or_generate()
            assert result == True  # Preview mode
    
    def test_preview_or_generate_generate(self):
        """Test generate option selection."""
        wizard = AnkiWizard()
        
        # Mock generate selection
        with patch('builtins.input', return_value='2'):
            result = wizard.preview_or_generate()
            assert result == False  # Generate mode
    
    def test_preview_or_generate_cancel(self):
        """Test cancel option selection."""
        wizard = AnkiWizard()
        
        # Mock cancel selection
        with patch('builtins.input', return_value='0'):
            result = wizard.preview_or_generate()
            assert result is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])