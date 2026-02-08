"""
Test suite for CLI Frontend Main Menu System
Following Test-Driven Development (TDD) principles
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.frontend.main_menu import MainMenu, MainMenuError


class TestMainMenuSystem:
    """Test cases for the main menu system."""
    
    def test_ascii_art_display(self):
        """Test that ASCII art title is displayed correctly."""
        menu = MainMenu()
        
        # Capture stdout to test output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            menu.display_ascii_art_title()
            output = fake_out.getvalue()
            
            # Check that clean ASCII art was printed by looking for key patterns
            assert "____" in output  # Underscores are common in ASCII art
            assert "|" in output     # Pipe characters are common in ASCII art
            assert len(output) > 100  # Should be substantial output
    
    def test_menu_options_display(self):
        """Test that all menu options are displayed."""
        menu = MainMenu()
        
        # Capture stdout to test output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            menu.display_menu()
            output = fake_out.getvalue()
            
            # Check that key elements are displayed
            assert "MEDIA KNOWLEDGE PIPELINE" in output
            assert "=" * 80 in output  # Header separator
            
            # Check that all options are displayed
            expected_options = [
                "Process Media Content  (Video/Audio/Document)",
                "Batch Process Multiple Items",
                "Create Essay from Existing Results",
                "Scan Directory for Media Files",
                "Watch Directory for New Files",
                "System Status and Requirements",
                "Show Pipeline Architecture",
                "Exit"
            ]
            
            for option in expected_options:
                assert option in output or option.replace("  ", " ") in output
    
    def test_menu_has_correct_number_of_options(self):
        """Test that menu has the expected number of options."""
        menu = MainMenu()
        assert len(menu.menu_options) == 8  # 7 options + Exit
    
    def test_get_user_choice_valid_input(self):
        """Test getting valid user input."""
        menu = MainMenu()
        
        # Test valid choices
        test_cases = [
            ("1", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
            ("0", 0)
        ]
        
        for input_val, expected in test_cases:
            with patch('builtins.input', return_value=input_val):
                result = menu.get_user_choice()
                assert result == expected
    
    def test_get_user_choice_invalid_input(self):
        """Test handling of invalid user input."""
        menu = MainMenu()
        
        # Test invalid inputs
        invalid_inputs = ["8", "9", "-1", "abc", ""]
        
        for invalid_input in invalid_inputs:
            with patch('builtins.input', return_value=invalid_input):
                with pytest.raises(MainMenuError):
                    menu.get_user_choice()
    
    def test_get_user_choice_non_numeric(self):
        """Test handling of non-numeric input."""
        menu = MainMenu()
        
        with patch('builtins.input', return_value="hello"):
            with pytest.raises(MainMenuError) as excinfo:
                menu.get_user_choice()
            assert "not a number" in str(excinfo.value)
    
    def test_get_user_choice_empty_input(self):
        """Test handling of empty input."""
        menu = MainMenu()
        
        with patch('builtins.input', return_value=""):
            with pytest.raises(MainMenuError) as excinfo:
                menu.get_user_choice()
            assert "No input provided" in str(excinfo.value)


class TestMainMenuIntegration:
    """Integration tests for main menu system."""
    
    def test_main_menu_initialization(self):
        """Test that main menu initializes correctly."""
        menu = MainMenu()
        assert menu is not None
        assert hasattr(menu, 'menu_options')
        assert hasattr(menu, 'display_ascii_art_title')
        assert hasattr(menu, 'display_menu')
        assert hasattr(menu, 'get_user_choice')
    
    def test_menu_options_content(self):
        """Test that menu options contain expected content."""
        menu = MainMenu()
        
        # Check that Exit is the last option
        assert menu.menu_options[-1] == "Exit"
        
        # Check that key options are present
        assert any("Process Media Content" in opt for opt in menu.menu_options)
        assert any("Batch Process" in opt for opt in menu.menu_options)
        assert any("Create Essay" in opt for opt in menu.menu_options)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])