"""
Test suite for Command Executor
Following Test-Driven Development (TDD) principles
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.frontend.command_executor import CommandExecutor


class TestCommandExecutor:
    """Test cases for command executor."""
    
    def test_executor_initialization(self):
        """Test that command executor initializes correctly."""
        executor = CommandExecutor()
        assert executor is not None
        assert hasattr(executor, 'base_command')
        assert isinstance(executor.base_command, list)
        
    def test_execute_media_processing_with_youtube_url(self):
        """Test media processing with YouTube URL configuration."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test123",
            "media_type": "youtube",
            "template": "lecture_summary",
            "custom_prompt": None,
            "output_config": {
                "save_json": True,
                "save_markdown": True,
                "output_type": 3
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_media_processing(config)
            
            assert result == True
            mock_run.assert_called_once()
            
            # Check command construction
            call_args = mock_run.call_args[0][0]
            assert "process" in call_args
            assert "media" in call_args
            assert "--input" in call_args
            assert "outputs/markdown" in call_args
            
    def test_execute_media_processing_with_local_file(self):
        """Test media processing with local file configuration."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "/path/to/video.mp4",
            "media_type": "local",
            "template": "technical_tutorial",
            "custom_prompt": None,
            "output_config": {
                "save_json": False,
                "save_markdown": True,
                "output_type": 2
            },
            "processing_options": {
                "use_cloud": True,
                "quiet": True,
                "organize": False
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_media_processing(config)
            
            assert result == True
            mock_run.assert_called_once()
            
            # Check command construction
            call_args = mock_run.call_args[0][0]
            assert "process" in call_args
            assert "media" in call_args
            assert "--input" in call_args
            assert "--cloud" in call_args
            assert "--quiet" in call_args
            assert "--no-organize" in call_args
            
    def test_execute_media_processing_with_custom_prompt(self):
        """Test media processing with custom prompt."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test456",
            "media_type": "youtube",
            "template": "custom",
            "custom_prompt": "Summarize this video focusing on key insights",
            "output_config": {
                "save_json": True,
                "save_markdown": False,
                "output_type": 1
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_media_processing(config)
            
            assert result == True
            mock_run.assert_called_once()
            
            # Check custom prompt is included
            call_args = mock_run.call_args[0][0]
            assert "Summarize" in " ".join(call_args)
            
    def test_execute_media_processing_failure(self):
        """Test media processing when command fails."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test123",
            "media_type": "youtube",
            "template": "lecture_summary",
            "custom_prompt": None,
            "output_config": {
                "save_json": True,
                "save_markdown": True,
                "output_type": 3
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            
            result = executor.execute_media_processing(config)
            
            assert result == False
            mock_run.assert_called_once()
            
    def test_execute_batch_processing(self):
        """Test batch processing execution."""
        executor = CommandExecutor()
        
        config = {
            "urls_file": "/tmp/urls.txt",
            "output_dir": "/tmp/outputs",
            "parallel_workers": 4,
            "template": "research_presentation",
            "custom_prompt": None,
            "essay_options": {
                "enable_essay": True,
                "force_essay": False
            },
            "processing_options": {
                "use_cloud": True,
                "quiet": True,
                "organize": False
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_batch_processing(config)
            
            assert result == True
            mock_run.assert_called_once()
            
            # Check command construction
            call_args = mock_run.call_args[0][0]
            assert "batch" in call_args
            assert "process-urls" in call_args
            assert "--urls" in call_args
            assert "--parallel" in call_args
            assert "4" in call_args
            assert "--essay" in call_args
            assert "--cloud" in call_args
            assert "--quiet" in call_args
            assert "--no-organize" in call_args
            
    def test_execute_document_processing(self):
        """Test document processing execution."""
        executor = CommandExecutor()
        
        config = {
            "file_path": "/tmp/document.pdf",
            "template": "research_summary",
            "custom_prompt": None,
            "output_config": {
                "save_json": True,
                "save_markdown": False,
                "output_type": 1
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_document_processing(config)
            
            assert result == True
            mock_run.assert_called_once()
            
            # Check command construction
            call_args = mock_run.call_args[0][0]
            assert "document" in call_args
            assert "process" in call_args
            assert "/tmp/document.pdf" in call_args
            assert "--output" in call_args
            
    def test_markdown_directory_parameter_correct(self):
        """Test that markdown directory parameter is correctly set to outputs/markdown."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test123",
            "media_type": "youtube",
            "template": "lecture_summary",
            "custom_prompt": None,
            "output_config": {
                "save_json": False,
                "save_markdown": True,
                "output_type": 2
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_media_processing(config)
            
            assert result == True
            
            # Verify markdown directory is correctly set
            call_args = mock_run.call_args[0][0]
            markdown_index = call_args.index("--markdown")
            markdown_path = call_args[markdown_index + 1]
            assert markdown_path == "outputs/markdown"


class TestCommandConstruction:
    """Test command construction logic."""
    
    def test_base_command_format(self):
        """Test that base command uses correct format."""
        executor = CommandExecutor()
        
        # Base command should be structured for CLI module execution
        assert len(executor.base_command) >= 3
        assert executor.base_command[0] == sys.executable
        assert executor.base_command[1] == "-m"
        assert "media_knowledge" in executor.base_command[2]
        
    def test_command_with_all_options(self):
        """Test command construction with all options enabled."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test123",
            "media_type": "youtube",
            "template": "custom",
            "custom_prompt": "Analyze this content",
            "output_config": {
                "save_json": True,
                "save_markdown": True,
                "output_type": 3
            },
            "processing_options": {
                "use_cloud": True,
                "quiet": True,
                "organize": False
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = executor.execute_media_processing(config)
            
            assert result == True
            mock_run.assert_called_once()


class TestErrorHandling:
    """Test error handling in command executor."""
    
    def test_exception_handling(self):
        """Test handling of exceptions during command execution."""
        executor = CommandExecutor()
        
        config = {
            "media_input": "https://youtube.com/watch?v=test123",
            "media_type": "youtube",
            "template": "lecture_summary",
            "custom_prompt": None,
            "output_config": {
                "save_json": True,
                "save_markdown": True,
                "output_type": 3
            },
            "processing_options": {
                "use_cloud": False,
                "quiet": False,
                "organize": True
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Subprocess failed")
            
            result = executor.execute_media_processing(config)
            
            assert result == False
            mock_run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])