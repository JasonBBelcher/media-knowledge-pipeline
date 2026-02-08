"""
Test suite for Batch Processing Commands
Following Test-Driven Development (TDD) principles
"""
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.batch_processor import BatchProcessor, BatchProcessorError


class TestBatchCommands:
    """Test cases for batch processing commands."""
    
    def test_batch_command_initialization(self):
        """Test that batch command initializes correctly."""
        processor = BatchProcessor()
        assert processor is not None
        assert hasattr(processor, 'valid_urls')
        assert hasattr(processor, 'invalid_urls')
        assert hasattr(processor, 'processed_count')
    
    def test_urls_file_parsing(self):
        """Test parsing of URLs from file."""
        processor = BatchProcessor()
        
        # Test with mock file content
        test_content = """
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/shorturl
# This is a comment
https://www.youtube.com/embed/embedded

invalid-url
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                valid_urls, invalid_urls = processor.parse_urls_file('/tmp/test_urls.txt')
                assert len(valid_urls) == 3
                assert len(invalid_urls) == 1
                assert "dQw4w9WgXcQ" in valid_urls[0]
    
    def test_parallel_processing_setup(self):
        """Test parallel processing configuration."""
        processor = BatchProcessor()
        
        # Test valid worker counts
        assert processor.setup_parallel_processing(1) == True
        assert processor.setup_parallel_processing(4) == True
        assert processor.setup_parallel_processing(8) == True
    
    def test_essay_generation_options(self):
        """Test essay generation options configuration."""
        processor = BatchProcessor()
        
        # Test essay generation configuration
        config = processor.configure_essay_generation(True, False)
        assert config['enabled'] == True
        assert config['forced'] == False
        
        config = processor.configure_essay_generation(True, True)
        assert config['enabled'] == True
        assert config['forced'] == True
        
        config = processor.configure_essay_generation(False, True)
        assert config['enabled'] == False
        assert config['forced'] == False


class TestUrlsParsing:
    """Test cases for URLs file parsing."""
    
    def test_valid_urls_file_parsing(self):
        """Test parsing of valid URLs file."""
        processor = BatchProcessor()
        
        # Test with valid URLs only
        test_content = """
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/shorturl
https://www.youtube.com/embed/embedded
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                valid_urls, invalid_urls = processor.parse_urls_file('/tmp/test_urls.txt')
                assert len(valid_urls) == 3
                assert len(invalid_urls) == 0
    
    def test_empty_urls_file_handling(self):
        """Test handling of empty URLs file."""
        processor = BatchProcessor()
        
        # Test with empty file
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='')):
                with pytest.raises(BatchProcessorError, match="URLs file is empty"):
                    processor.parse_urls_file('/tmp/empty.txt')
    
    def test_malformed_urls_filtering(self):
        """Test filtering of malformed URLs."""
        processor = BatchProcessor()
        
        # Test with mix of valid and invalid URLs
        test_content = """
https://www.youtube.com/watch?v=valid1
not-a-url
https://www.google.com
https://youtu.be/valid2
ftp://invalid-protocol.com
        """
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=test_content)):
                valid_urls, invalid_urls = processor.parse_urls_file('/tmp/mixed_urls.txt')
                assert len(valid_urls) == 2
                assert len(invalid_urls) == 3
                assert "youtube.com/watch?v=valid1" in valid_urls[0]
                assert "youtu.be/valid2" in valid_urls[1]


class TestParallelProcessing:
    """Test cases for parallel processing functionality."""
    
    def test_parallel_workers_configuration(self):
        """Test parallel workers configuration."""
        processor = BatchProcessor()
        
        # Test valid worker counts
        valid_workers = [1, 2, 4, 8]
        for workers in valid_workers:
            assert processor.setup_parallel_processing(workers) == True
        
        # Test invalid worker counts
        invalid_workers = [0, -1, 9, 100]
        for workers in invalid_workers:
            with pytest.raises(BatchProcessorError):
                processor.setup_parallel_processing(workers)
    
    def test_worker_pool_creation(self):
        """Test creation of worker pool."""
        processor = BatchProcessor()
        
        # Test that parallel processing setup works
        assert processor.setup_parallel_processing(4) == True


class TestEssayGeneration:
    """Test cases for essay generation functionality."""
    
    def test_essay_generation_enable(self):
        """Test enabling essay generation."""
        processor = BatchProcessor()
        
        config = processor.configure_essay_generation(True, False)
        assert config['enabled'] == True
        assert config['forced'] == False
    
    def test_force_essay_generation(self):
        """Test force essay generation option."""
        processor = BatchProcessor()
        
        # Force only applies when enabled
        config = processor.configure_essay_generation(True, True)
        assert config['enabled'] == True
        assert config['forced'] == True
        
        # Force ignored when disabled
        config = processor.configure_essay_generation(False, True)
        assert config['enabled'] == False
        assert config['forced'] == False


# Test data for batch processing
TEST_URLS_CONTENT = """
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=video2
https://youtu.be/shorturl
# This is a comment
https://www.youtube.com/embed/embedded

"""

TEST_EMPTY_CONTENT = ""

TEST_MALFORMED_CONTENT = """
not-a-url
https://www.youtube.com/watch?v=valid
ftp://invalid-protocol.com
"""

if __name__ == "__main__":
    pytest.main([__file__, "-v"])