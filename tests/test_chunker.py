"""
Unit tests for chunker module.

Tests audio chunking functionality for long audio files.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import tempfile
import json

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.chunker import (
    split_audio_into_chunks,
    concatenate_transcripts,
    should_chunk_audio,
    get_audio_duration,
    AudioChunkerError
)


class TestGetAudioDuration:
    """Test get_audio_duration function."""
    
    @patch('utils.chunker.subprocess.run')
    def test_get_audio_duration_success(self, mock_run):
        """Test successful audio duration retrieval."""
        mock_result = MagicMock()
        mock_result.stdout = json.dumps({
            "format": {
                "duration": "300.5"
            }
        })
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        duration = get_audio_duration("test_audio.wav")
        
        assert duration == 300.5
        mock_run.assert_called_once()
        
        # Verify ffprobe command
        call_args = mock_run.call_args
        assert "ffprobe" in call_args[0][0]
        assert "-v" in call_args[0][0]
        assert "-print_format" in call_args[0][0]
        assert "json" in call_args[0][0]
    
    @patch('utils.chunker.subprocess.run')
    def test_get_audio_duration_integer(self, mock_run):
        """Test audio duration with integer value."""
        mock_result = MagicMock()
        mock_result.stdout = json.dumps({
            "format": {
                "duration": "600"
            }
        })
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        duration = get_audio_duration("test_audio.wav")
        
        assert duration == 600.0
    
    @patch('utils.chunker.subprocess.run')
    def test_get_audio_duration_file_not_found(self, mock_run):
        """Test handling of file not found error."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "No such file or directory"
        mock_run.return_value = mock_result
        
        with pytest.raises(AudioProcessingError):
            get_audio_duration("nonexistent.wav")
    
    @patch('utils.chunker.subprocess.run')
    def test_get_audio_duration_invalid_json(self, mock_run):
        """Test handling of invalid JSON output."""
        mock_result = MagicMock()
        mock_result.stdout = "Invalid JSON output"
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        with pytest.raises(AudioProcessingError):
            get_audio_duration("test_audio.wav")
    
    @patch('utils.chunker.subprocess.run')
    def test_get_audio_duration_missing_duration(self, mock_run):
        """Test handling of missing duration in JSON."""
        mock_result = MagicMock()
        mock_result.stdout = json.dumps({
            "format": {
                "other_field": "value"
            }
        })
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        with pytest.raises(AudioProcessingError):
            get_audio_duration("test_audio.wav")


class TestShouldChunkAudio:
    """Test should_chunk_audio function."""
    
    @patch('utils.chunker.get_audio_duration')
    def test_should_chunk_audio_long_file(self, mock_duration):
        """Test that long files should be chunked."""
        mock_duration.return_value = 1800.0  # 30 minutes
        
        result = should_chunk_audio("long_audio.wav")
        
        assert result is True
    
    @patch('utils.chunker.get_audio_duration')
    def test_should_chunk_audio_short_file(self, mock_duration):
        """Test that short files should not be chunked."""
        mock_duration.return_value = 600.0  # 10 minutes
        
        result = should_chunk_audio("short_audio.wav")
        
        assert result is False
    
    @patch('utils.chunker.get_audio_duration')
    def test_should_chunk_audio_boundary(self, mock_duration):
        """Test boundary case at chunk threshold."""
        mock_duration.return_value = 1500.0  # 25 minutes (default threshold)
        
        result = should_chunk_audio("boundary_audio.wav")
        
        assert result is True
    
    @patch('utils.chunker.get_audio_duration')
    def test_should_chunk_audio_custom_threshold(self, mock_duration):
        """Test with custom chunk threshold."""
        mock_duration.return_value = 1200.0  # 20 minutes
        
        result = should_chunk_audio("custom_audio.wav", chunk_threshold_minutes=15)
        
        assert result is True
    
    @patch('utils.chunker.get_audio_duration')
    def test_should_chunk_audio_below_custom_threshold(self, mock_duration):
        """Test below custom chunk threshold."""
        mock_duration.return_value = 600.0  # 10 minutes
        
        result = should_chunk_audio("custom_audio.wav", chunk_threshold_minutes=15)
        
        assert result is False


class TestSplitAudioIntoChunks:
    """Test split_audio_into_chunks function."""
    
    @pytest.mark.slow
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_success(self, mock_makedirs, mock_duration, mock_run):
        """Test successful audio splitting."""
        mock_duration.return_value = 1800.0  # 30 minutes
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=10
            )
            
            assert len(chunk_files) == 3
            assert all(f.startswith(temp_dir) for f in chunk_files)
            assert all(f.endswith(".wav") for f in chunk_files)
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_partial_chunk(self, mock_makedirs, mock_duration, mock_run):
        """Test splitting with partial final chunk."""
        mock_duration.return_value = 1650.0  # 27.5 minutes
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=10
            )
            
            assert len(chunk_files) == 3  # 10 + 10 + 7.5
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_single_chunk(self, mock_makedirs, mock_duration, mock_run):
        """Test splitting when only one chunk is needed."""
        mock_duration.return_value = 600.0  # 10 minutes
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=10
            )
            
            assert len(chunk_files) == 1
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_ffmpeg_error(self, mock_makedirs, mock_duration, mock_run):
        """Test handling of ffmpeg errors."""
        mock_duration.return_value = 1800.0
        mock_run.return_value = MagicMock(returncode=1, stderr="ffmpeg error")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(AudioProcessingError):
                split_audio_into_chunks(
                    "test_audio.wav",
                    temp_dir,
                    chunk_duration_minutes=10
                )
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_custom_duration(self, mock_makedirs, mock_duration, mock_run):
        """Test splitting with custom chunk duration."""
        mock_duration.return_value = 1800.0  # 30 minutes
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=5
            )
            
            assert len(chunk_files) == 6  # 30 / 5 = 6 chunks
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_split_audio_into_chunks_output_prefix(self, mock_makedirs, mock_duration, mock_run):
        """Test splitting with custom output prefix."""
        mock_duration.return_value = 1200.0  # 20 minutes
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=10,
                output_prefix="custom_"
            )
            
            assert len(chunk_files) == 2
            assert all("custom_" in Path(f).name for f in chunk_files)


class TestConcatenateTranscripts:
    """Test concatenate_transcripts function."""
    
    def test_concatenate_transcripts_basic(self):
        """Test basic transcript concatenation."""
        transcripts = [
            "This is the first segment.",
            "This is the second segment.",
            "This is the third segment."
        ]
        
        result = concatenate_transcripts(transcripts)
        
        assert "This is the first segment." in result
        assert "This is the second segment." in result
        assert "This is the third segment." in result
    
    def test_concatenate_transcripts_with_timestamps(self):
        """Test concatenating transcripts with timestamps."""
        transcripts = [
            "[00:00:00] First segment",
            "[00:05:00] Second segment",
            "[00:10:00] Third segment"
        ]
        
        result = concatenate_transcripts(transcripts)
        
        assert "[00:00:00] First segment" in result
        assert "[00:05:00] Second segment" in result
        assert "[00:10:00] Third segment" in result
    
    def test_concatenate_transcripts_empty_list(self):
        """Test concatenating empty list."""
        result = concatenate_transcripts([])
        
        assert result == ""
    
    def test_concatenate_transcripts_single_item(self):
        """Test concatenating single transcript."""
        transcripts = ["Single transcript"]
        
        result = concatenate_transcripts(transcripts)
        
        assert result == "Single transcript"
    
    def test_concatenate_transcripts_with_newlines(self):
        """Test concatenating with custom separator."""
        transcripts = ["First", "Second", "Third"]
        
        result = concatenate_transcripts(transcripts, separator="\n\n")
        
        assert result == "First\n\nSecond\n\nThird"
    
    def test_concatenate_transcripts_with_prefix(self):
        """Test concatenating with prefix for each segment."""
        transcripts = ["First", "Second", "Third"]
        
        result = concatenate_transcripts(transcripts, segment_prefix="Segment: ")
        
        assert "Segment: First" in result
        assert "Segment: Second" in result
        assert "Segment: Third" in result
    
    def test_concatenate_transcripts_preserves_whitespace(self):
        """Test that concatenation preserves whitespace."""
        transcripts = [
            "  First with spaces  ",
            "  Second with spaces  ",
            "  Third with spaces  "
        ]
        
        result = concatenate_transcripts(transcripts)
        
        assert "  First with spaces  " in result
        assert "  Second with spaces  " in result
        assert "  Third with spaces  " in result
    
    def test_concatenate_transcripts_unicode(self):
        """Test concatenating unicode transcripts."""
        transcripts = [
            "English text",
            "中文文本",
            "日本語テキスト"
        ]
        
        result = concatenate_transcripts(transcripts)
        
        assert "English text" in result
        assert "中文文本" in result
        assert "日本語テキスト" in result


class TestChunkerError:
    """Test ChunkerError exception."""
    
    def test_chunker_error_creation(self):
        """Test ChunkerError can be created."""
        error = ChunkerError("Chunking failed")
        
        assert str(error) == "Chunking failed"
        assert isinstance(error, Exception)
    
    def test_chunker_error_inheritance(self):
        """Test ChunkerError inherits from Exception."""
        error = ChunkerError("Test error")
        
        assert isinstance(error, Exception)
        assert isinstance(error, BaseException)


class TestAudioProcessingError:
    """Test AudioProcessingError exception."""
    
    def test_audio_processing_error_creation(self):
        """Test AudioProcessingError can be created."""
        error = AudioProcessingError("Audio processing failed")
        
        assert str(error) == "Audio processing failed"
        assert isinstance(error, Exception)
    
    def test_audio_processing_error_inheritance(self):
        """Test AudioProcessingError inherits from ChunkerError."""
        error = AudioProcessingError("Test error")
        
        assert isinstance(error, ChunkerError)
        assert isinstance(error, Exception)


class TestChunkingWorkflow:
    """Test complete chunking workflow."""
    
    @patch('utils.chunker.split_audio_into_chunks')
    @patch('utils.chunker.should_chunk_audio')
    def test_chunking_workflow_with_chunking(self, mock_should_chunk, mock_split):
        """Test workflow when chunking is needed."""
        mock_should_chunk.return_value = True
        mock_split.return_value = [
            "/tmp/chunk_001.wav",
            "/tmp/chunk_002.wav",
            "/tmp/chunk_003.wav"
        ]
        
        # Simulate the workflow
        audio_file = "long_audio.wav"
        output_dir = "/tmp/chunks"
        
        if should_chunk_audio(audio_file):
            chunks = split_audio_into_chunks(audio_file, output_dir)
            assert len(chunks) == 3
            mock_split.assert_called_once_with(audio_file, output_dir)
    
    @patch('utils.chunker.should_chunk_audio')
    def test_chunking_workflow_without_chunking(self, mock_should_chunk):
        """Test workflow when chunking is not needed."""
        mock_should_chunk.return_value = False
        
        audio_file = "short_audio.wav"
        
        if should_chunk_audio(audio_file):
            assert False, "Should not reach here"
        else:
            assert True


class TestChunkFileNaming:
    """Test chunk file naming conventions."""
    
    @patch('utils.chunker.subprocess.run')
    @patch('utils.chunker.get_audio_duration')
    @patch('utils.chunker.os.makedirs')
    def test_chunk_file_naming_pattern(self, mock_makedirs, mock_duration, mock_run):
        """Test that chunk files follow naming pattern."""
        mock_duration.return_value = 1800.0
        mock_run.return_value = MagicMock(returncode=0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_files = split_audio_into_chunks(
                "test_audio.wav",
                temp_dir,
                chunk_duration_minutes=10
            )
            
            # Check that files are named with sequential numbers
            for i, chunk_file in enumerate(chunk_files, 1):
                filename = Path(chunk_file).name
                assert str(i).zfill(3) in filename or str(i) in filename


if __name__ == "__main__":
    pytest.main([__file__, "-v"])