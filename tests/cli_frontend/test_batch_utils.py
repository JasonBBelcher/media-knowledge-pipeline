"""
Test suite for Batch Processing Utilities
Following Test-Driven Development (TDD) principles
"""
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.frontend.batch_utils import BatchUtilities, BatchUtilsError


class TestBatchUtilities:
    """Test cases for batch utilities."""
    
    def test_utilities_initialization(self):
        """Test that batch utilities initialize correctly."""
        utils = BatchUtilities()
        assert utils is not None
        assert hasattr(utils, 'processor')
    
    def test_urls_file_validation(self):
        """Test URLs file validation functionality."""
        utils = BatchUtilities()
        
        # Test with mock file content
        test_content = """
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/shorturl
# This is a comment

invalid-url
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                result = utils.validate_urls_file('/tmp/test_urls.txt')
                assert result['valid_count'] == 2
                assert result['invalid_count'] == 1
                assert result['is_valid'] == True
    
    def test_sample_urls_file_creation(self):
        """Test creation of sample URLs file."""
        utils = BatchUtilities()
        
        # Test successful creation
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', mock_open()):
                result = utils.create_sample_urls_file('/tmp/sample_urls.txt')
                assert result == True
    
    def test_processing_time_estimation(self):
        """Test processing time estimation."""
        utils = BatchUtilities()
        
        # Test time estimation for different scenarios
        estimate1 = utils.estimate_processing_time(1, 1)
        assert estimate1['minutes'] == 0.8
        
        estimate2 = utils.estimate_processing_time(10, 2)
        assert estimate2['minutes'] == 3.8
        
        # Test that more workers reduce time
        estimate3 = utils.estimate_processing_time(10, 1)
        estimate4 = utils.estimate_processing_time(10, 5)
        assert estimate3['seconds'] > estimate4['seconds']


class TestUrlsFileValidation:
    """Test cases for URLs file validation."""
    
    def test_valid_urls_file_validation(self):
        """Test validation of valid URLs file."""
        utils = BatchUtilities()
        
        test_content = """
https://www.youtube.com/watch?v=valid1
https://youtu.be/valid2
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                result = utils.validate_urls_file('/tmp/valid_urls.txt')
                assert result['valid_count'] == 2
                assert result['invalid_count'] == 0
                assert result['is_valid'] == True
    
    def test_empty_urls_file_validation(self):
        """Test validation of empty URLs file."""
        utils = BatchUtilities()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='')):
                with pytest.raises(BatchUtilsError):
                    utils.validate_urls_file('/tmp/empty.txt')
    
    def test_malformed_urls_file_validation(self):
        """Test validation of malformed URLs file."""
        utils = BatchUtilities()
        
        test_content = """
not-a-url
https://www.google.com
ftp://invalid.com
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                result = utils.validate_urls_file('/tmp/malformed_urls.txt')
                assert result['valid_count'] == 0
                assert result['invalid_count'] == 3
                assert result['is_valid'] == False


class TestTimeEstimation:
    """Test cases for time estimation functionality."""
    
    def test_single_video_estimation(self):
        """Test time estimation for single video."""
        utils = BatchUtilities()
        
        estimate = utils.estimate_processing_time(1, 1)
        assert isinstance(estimate['seconds'], int)
        assert isinstance(estimate['minutes'], float)
        assert isinstance(estimate['hours'], float)
        assert estimate['seconds'] > 0
    
    def test_multiple_videos_estimation(self):
        """Test time estimation for multiple videos."""
        utils = BatchUtilities()
        
        # More videos should take more time (with same workers)
        estimate1 = utils.estimate_processing_time(1, 1)
        estimate2 = utils.estimate_processing_time(5, 1)
        assert estimate2['seconds'] > estimate1['seconds']
    
    def test_parallel_processing_effect(self):
        """Test that parallel processing reduces estimated time."""
        utils = BatchUtilities()
        
        # Same number of videos, more workers should reduce time
        estimate1 = utils.estimate_processing_time(10, 1)
        estimate2 = utils.estimate_processing_time(10, 2)
        assert estimate2['seconds'] < estimate1['seconds']


class TestSummaryFormatting:
    """Test cases for summary formatting."""
    
    def test_batch_summary_formatting(self):
        """Test formatting of batch summary."""
        utils = BatchUtilities()
        
        config = {
            "urls_file": "/tmp/urls.txt",
            "output_dir": "/tmp/output",
            "parallel_workers": 4,
            "template": "lecture_summary",
            "essay_options": {
                "enable_essay": True,
                "force_essay": False
            },
            "processing_options": {
                "use_cloud": True,
                "quiet": False,
                "organize": True
            }
        }
        
        summary = utils.format_batch_summary(config)
        assert "BATCH PROCESSING SUMMARY" in summary
        assert "URLs File: /tmp/urls.txt" in summary
        assert "Parallel Workers: 4" in summary
        assert "Essay Generation: Enabled" in summary
    
    def test_custom_prompt_summary(self):
        """Test summary formatting with custom prompt."""
        utils = BatchUtilities()
        
        config = {
            "template": "custom",
            "custom_prompt": "This is a very long custom prompt that should be truncated in the summary"
        }
        
        summary = utils.format_batch_summary(config)
        assert "Custom" in summary


# Test data for batch utilities
SAMPLE_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/shorturl",
    "https://www.youtube.com/embed/embedded"
]

INVALID_URLS = [
    "not-a-url",
    "https://www.google.com",
    "ftp://invalid-protocol.com"
]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])