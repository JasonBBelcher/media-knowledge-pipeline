"""
Unit tests for user prompter utility module
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.media_knowledge.cli.frontend.shared.user_prompter import (
    prompt_for_choice,
    prompt_for_text,
    prompt_for_confirmation,
    prompt_for_number
)

class TestUserPrompter:
    """Test user prompting functions."""
    
    def test_prompt_for_choice_valid(self):
        """Test valid user choice input."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='2'):
            result = prompt_for_choice("Select an option:", options)
            assert result == 2
    
    def test_prompt_for_choice_invalid_then_valid(self):
        """Test invalid then valid user choice input."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', side_effect=['invalid', '5', '2']):
            with patch('builtins.print') as mock_print:
                result = prompt_for_choice("Select an option:", options)
                assert result == 2
    
    def test_prompt_for_choice_cancel(self):
        """Test user cancelling choice input."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='0'):
            result = prompt_for_choice("Select an option:", options)
            assert result is None
    
    def test_prompt_for_choice_no_cancel(self):
        """Test user choice input without cancel option."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='2'):
            result = prompt_for_choice("Select an option:", options, allow_cancel=False)
            assert result == 2
    
    def test_prompt_for_text_input(self):
        """Test text input prompting."""
        with patch('builtins.input', return_value='test input'):
            result = prompt_for_text("Enter text:")
            assert result == 'test input'
    
    def test_prompt_for_text_input_empty_not_allowed(self):
        """Test text input prompting with empty input not allowed."""
        with patch('builtins.input', side_effect=['', 'valid input']):
            with patch('builtins.print') as mock_print:
                result = prompt_for_text("Enter text:")
                assert result == 'valid input'
    
    def test_prompt_for_text_input_empty_allowed(self):
        """Test text input prompting with empty input allowed."""
        with patch('builtins.input', return_value=''):
            result = prompt_for_text("Enter text:", allow_empty=True, default_value="default")
            assert result == 'default'
    
    def test_prompt_for_confirmation_yes(self):
        """Test confirmation prompt with 'yes' response."""
        with patch('builtins.input', return_value='y'):
            result = prompt_for_confirmation("Confirm?")
            assert result == True
    
    def test_prompt_for_confirmation_no(self):
        """Test confirmation prompt with 'no' response."""
        with patch('builtins.input', return_value='n'):
            result = prompt_for_confirmation("Confirm?")
            assert result == False
    
    def test_prompt_for_confirmation_invalid_then_valid(self):
        """Test invalid then valid confirmation input."""
        with patch('builtins.input', side_effect=['invalid', 'maybe', 'y']):
            with patch('builtins.print') as mock_print:
                result = prompt_for_confirmation("Confirm?")
                assert result == True
    
    def test_prompt_for_number_valid(self):
        """Test valid number input."""
        with patch('builtins.input', return_value='5'):
            result = prompt_for_number("Enter number:", 1, 10)
            assert result == 5
    
    def test_prompt_for_number_invalid_then_valid(self):
        """Test invalid then valid number input."""
        with patch('builtins.input', side_effect=['invalid', '15', '5']):
            with patch('builtins.print') as mock_print:
                result = prompt_for_number("Enter number:", 1, 10)
                assert result == 5
    
    def test_prompt_for_number_out_of_range(self):
        """Test number input outside valid range."""
        with patch('builtins.input', side_effect=['15', '0', '5']):
            with patch('builtins.print') as mock_print:
                result = prompt_for_number("Enter number:", 1, 10)
                assert result == 5

if __name__ == "__main__":
    pytest.main([__file__, "-v"])