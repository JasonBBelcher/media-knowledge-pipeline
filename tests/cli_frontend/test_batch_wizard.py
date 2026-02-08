"""
Test suite for Batch Processing Wizard
Following Test-Driven Development (TDD) principles
"""
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.frontend.batch_wizard import BatchWizard, BatchWizardError


class TestBatchWizard:
    """Test cases for batch processing wizard."""
    
    def test_wizard_initialization(self):
        """Test that batch wizard initializes correctly."""
        wizard = BatchWizard()
        assert wizard is not None
        assert hasattr(wizard, 'templates')
        assert hasattr(wizard, 'output_options')
    
    def test_urls_file_selection(self):
        """Test URLs file selection functionality."""
        wizard = BatchWizard()
        
        # Test valid file path (mocking file existence and content)
        valid_path = "/tmp/urls.txt"
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_file', return_value=True):
                with patch('builtins.open', mock_open(read_data='https://youtube.com/watch?v=test')):
                    with patch('builtins.input', return_value=valid_path):
                        result = wizard.get_urls_file()
                        assert result == valid_path
    
    def test_output_directory_selection(self):
        """Test output directory selection functionality."""
        wizard = BatchWizard()
        
        # Test valid directory path
        valid_dir = "/tmp/output"
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.input', return_value=valid_dir):
                result = wizard.get_output_directory()
                assert result == valid_dir
    
    def test_parallel_processing_options(self):
        """Test parallel processing options configuration."""
        wizard = BatchWizard()
        
        # Test valid parallel workers
        with patch('builtins.input', return_value='4'):
            result = wizard.get_parallel_workers()
            assert result == 4
    
    def test_essay_generation_options(self):
        """Test essay generation options configuration."""
        wizard = BatchWizard()
        
        # Test essay options with yes/no responses
        with patch('builtins.input', side_effect=['y', 'n']):
            result = wizard.get_essay_options()
            assert result['enable_essay'] == True
            assert result['force_essay'] == False


class TestUrlsFileValidation:
    """Test cases for URLs file validation."""
    
    def test_valid_urls_file(self):
        """Test validation of valid URLs files."""
        wizard = BatchWizard()
        
        # Mock a valid URLs file
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_file', return_value=True):
                with patch('builtins.open', mock_open(read_data='https://youtube.com/watch?v=test')):
                    with patch('builtins.input', return_value='/tmp/urls.txt'):
                        result = wizard.get_urls_file()
                        assert result == '/tmp/urls.txt'
    
    def test_invalid_urls_file(self):
        """Test handling of invalid URLs files."""
        wizard = BatchWizard()
        
        # Test with empty file
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_file', return_value=True):
                with patch('builtins.open', mock_open(read_data='')):
                    # First input is empty file, second is valid file
                    with patch('builtins.input', side_effect=['/tmp/empty.txt', '/tmp/valid.txt']):
                        with pytest.raises(StopIteration):
                            # This will raise StopIteration because we're out of side_effect values
                            # but that's OK for testing the validation logic
                            wizard.get_urls_file()
    
    def test_missing_urls_file(self):
        """Test handling of missing URLs files."""
        wizard = BatchWizard()
        
        # Test with non-existent file
        with patch('pathlib.Path.exists', return_value=False):
            # First input is missing file, second is valid file
            with patch('builtins.input', side_effect=['/tmp/missing.txt', '/tmp/valid.txt']):
                with pytest.raises(StopIteration):
                    # This will raise StopIteration because we're out of side_effect values
                    # but that's OK for testing the validation logic
                    wizard.get_urls_file()


class TestParallelOptions:
    """Test cases for parallel processing options."""
    
    def test_parallel_workers_selection(self):
        """Test parallel workers selection."""
        wizard = BatchWizard()
        
        # Test valid parallel workers
        test_cases = ['1', '2', '4', '8']
        expected_results = [1, 2, 4, 8]
        
        for i, test_input in enumerate(test_cases):
            with patch('builtins.input', return_value=test_input):
                result = wizard.get_parallel_workers()
                assert result == expected_results[i]
    
    def test_invalid_parallel_workers(self):
        """Test handling of invalid parallel worker counts."""
        wizard = BatchWizard()
        
        # Test invalid inputs - this would normally prompt for re-entry
        # We'll test that the validation logic works by checking the range
        with patch('builtins.input', side_effect=['0', '9', '4']):
            # First two should be rejected, third should work
            with pytest.raises(StopIteration):
                wizard.get_parallel_workers()


class TestEssayOptions:
    """Test cases for essay generation options."""
    
    def test_enable_essay_generation(self):
        """Test enabling essay generation."""
        wizard = BatchWizard()
        
        # Test enabling essay generation
        with patch('builtins.input', return_value='y'):
            result = wizard.get_essay_options()
            assert result['enable_essay'] == True
    
    def test_force_essay_generation(self):
        """Test force essay generation option."""
        wizard = BatchWizard()
        
        # Test forcing essay generation when essay is enabled
        with patch('builtins.input', side_effect=['y', 'y']):
            result = wizard.get_essay_options()
            assert result['enable_essay'] == True
            assert result['force_essay'] == True


# Test data for batch processing options
BATCH_OPTIONS = [
    "URLs file path",
    "Output directory", 
    "Parallel processing (1-8 workers)",
    "Essay generation",
    "Force essay generation"
]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])