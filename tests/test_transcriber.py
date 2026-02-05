"""
Unit tests for transcriber module.

Tests Whisper integration, chunking logic, and transcription functionality.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, ANY
import tempfile

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.transcriber import (
    load_whisper_model,
    transcribe_audio_segment,
    transcribe_audio,
    transcribe_long_audio,
    TranscriberError,
    AudioFileNotFoundError,
    TranscriptionFailedError
)


class TestLoadWhisperModel:
    """Test Whisper model loading."""
    
    @patch('core.transcriber.whisper.load_model')
    def test_load_whisper_model_success(self, mock_load):
        """Test successful Whisper model loading."""
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        
        model = load_whisper_model("small")
        
        assert model == mock_model
        mock_load.assert_called_once_with("small")
    
    @patch('core.transcriber.whisper.load_model')
    def test_load_whisper_model_different_sizes(self, mock_load):
        """Test loading different Whisper model sizes."""
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        
        for size in ["tiny", "base", "small", "medium", "large"]:
            model = load_whisper_model(size)
            assert model == mock_model
    
    @patch('core.transcriber.whisper.load_model')
    def test_load_whisper_model_failure(self, mock_load):
        """Test Whisper model loading failure."""
        mock_load.side_effect = Exception("Model not found")
        
        with pytest.raises(TranscriberError):
            load_whisper_model("small")


class TestTranscribeAudioSegment:
    """Test single audio segment transcription."""
    
    @patch('core.transcriber.whisper.load_model')
    def test_transcribe_audio_segment_success(self, mock_load):
        """Test successful audio segment transcription."""
        # Mock the model
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "This is a test transcript."
        }
        mock_load.return_value = mock_model
        
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio_segment(mock_model, temp_path)
            
            assert transcript == "This is a test transcript."
            mock_model.transcribe.assert_called_once()
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.whisper.load_model')
    def test_transcribe_audio_segment_with_language(self, mock_load):
        """Test transcription with specified language."""
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Test transcript"}
        mock_load.return_value = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio_segment(mock_model, temp_path, language="en")
            
            assert transcript == "Test transcript"
            mock_model.transcribe.assert_called_once_with(
                temp_path,
                language="en",
                fp16=False
            )
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.whisper.load_model')
    def test_transcribe_audio_segment_failure(self, mock_load):
        """Test transcription failure handling."""
        mock_model = MagicMock()
        mock_model.transcribe.side_effect = Exception("Transcription failed")
        mock_load.return_value = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            with pytest.raises(TranscriptionFailedError):
                transcribe_audio_segment(mock_model, temp_path)
        finally:
            os.unlink(temp_path)


class TestTranscribeAudio:
    """Test main transcribe_audio function."""
    
    @patch('core.transcriber.transcribe_audio_segment')
    @patch('core.transcriber.load_whisper_model')
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_short_file(self, mock_should_chunk, mock_load, mock_transcribe):
        """Test transcription of short audio file (no chunking)."""
        mock_should_chunk.return_value = False
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        mock_transcribe.return_value = "Short transcript"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio(temp_path)
            
            assert transcript == "Short transcript"
            mock_should_chunk.assert_called_once()
            mock_load.assert_called_once()
            mock_transcribe.assert_called_once()
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.transcribe_long_audio')
    @patch('core.transcriber.load_whisper_model')
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_long_file(self, mock_should_chunk, mock_load, mock_transcribe_long):
        """Test transcription of long audio file (with chunking)."""
        mock_should_chunk.return_value = True
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        mock_transcribe_long.return_value = "Long transcript from chunks"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio(temp_path)
            
            assert transcript == "Long transcript from chunks"
            mock_should_chunk.assert_called_once()
            mock_load.assert_called_once()
            mock_transcribe_long.assert_called_once()
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_file_not_found(self, mock_should_chunk):
        """Test handling of non-existent audio file."""
        mock_should_chunk.return_value = False
        
        with pytest.raises(AudioFileNotFoundError):
            transcribe_audio("/nonexistent/audio.wav")
    
    @patch('core.transcriber.load_whisper_model')
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_custom_model_size(self, mock_should_chunk, mock_load):
        """Test transcription with custom model size."""
        mock_should_chunk.return_value = False
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcribe_audio(temp_path, model_size="medium")
            
            mock_load.assert_called_once_with("medium")
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.transcribe_audio_segment')
    @patch('core.transcriber.load_whisper_model')
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_custom_threshold(self, mock_should_chunk, mock_load, mock_transcribe):
        """Test transcription with custom chunking threshold."""
        mock_should_chunk.return_value = False
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        mock_transcribe.return_value = "Transcript"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcribe_audio(temp_path, chunk_threshold_minutes=30)
            
            mock_should_chunk.assert_called_once_with(temp_path, 30)
        finally:
            os.unlink(temp_path)


class TestTranscribeLongAudio:
    """Test long audio file transcription with chunking."""
    
    @pytest.mark.slow
    @patch('core.transcriber.concatenate_transcripts')
    @patch('core.transcriber.split_audio_into_chunks')
    @patch('core.transcriber.transcribe_audio_segment')
    def test_transcribe_long_audio_success(self, mock_transcribe, mock_split, mock_concat):
        """Test successful long audio transcription."""
        # Mock chunk splitting
        mock_split.return_value = ["/tmp/chunk1.wav", "/tmp/chunk2.wav"]
        
        # Mock transcription of each chunk
        mock_transcribe.side_effect = [
            "First chunk transcript",
            "Second chunk transcript"
        ]
        
        # Mock concatenation
        mock_concat.return_value = "First chunk transcript Second chunk transcript"
        
        mock_model = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_long_audio(mock_model, temp_path)
            
            assert transcript == "First chunk transcript Second chunk transcript"
            assert mock_transcribe.call_count == 2
            mock_concat.assert_called_once()
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.split_audio_into_chunks')
    @patch('core.transcriber.transcribe_audio_segment')
    def test_transcribe_long_audio_custom_chunk_duration(self, mock_transcribe, mock_split):
        """Test long audio transcription with custom chunk duration."""
        mock_split.return_value = ["/tmp/chunk1.wav"]
        mock_transcribe.return_value = "Chunk transcript"
        
        mock_model = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcribe_long_audio(mock_model, temp_path, chunk_duration=300)
            
            mock_split.assert_called_once_with(temp_path, ANY, 300)
        finally:
            os.unlink(temp_path)
    
    @patch('core.transcriber.split_audio_into_chunks')
    def test_transcribe_long_audio_chunking_failure(self, mock_split):
        """Test handling of chunking failure."""
        from utils.chunker import AudioChunkerError
        mock_split.side_effect = AudioChunkerError("Chunking failed")
        
        mock_model = MagicMock()
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            with pytest.raises(TranscriptionFailedError):
                transcribe_long_audio(mock_model, temp_path)
        finally:
            os.unlink(temp_path)


class TestTranscriberExceptions:
    """Test transcriber exception classes."""
    
    def test_transcriber_error_creation(self):
        """Test TranscriberError can be created with message."""
        error = TranscriberError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_audio_file_not_found_error_creation(self):
        """Test AudioFileNotFoundError can be created."""
        error = AudioFileNotFoundError("File not found")
        assert str(error) == "File not found"
        assert isinstance(error, TranscriberError)
    
    def test_transcription_failed_error_creation(self):
        """Test TranscriptionFailedError can be created."""
        error = TranscriptionFailedError("Transcription failed")
        assert str(error) == "Transcription failed"
        assert isinstance(error, TranscriberError)


class TestTranscriptionOutput:
    """Test transcription output formatting."""
    
    @patch('core.transcriber.whisper.load_model')
    def test_transcription_output_format(self, mock_load):
        """Test that transcription returns properly formatted text."""
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "  Test transcript with spaces  "
        }
        mock_load.return_value = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio_segment(mock_model, temp_path)
            
            # Whisper should strip whitespace
            assert transcript == "Test transcript with spaces"
        finally:
            os.unlink(temp_path)


class TestTranscriptionWithLanguage:
    """Test transcription with language specification."""
    
    @patch('core.transcriber.transcribe_audio_segment')
    @patch('core.transcriber.load_whisper_model')
    @patch('core.transcriber.should_chunk_audio')
    def test_transcribe_audio_with_language(self, mock_should_chunk, mock_load, mock_transcribe):
        """Test transcription with language parameter."""
        mock_should_chunk.return_value = False
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        mock_transcribe.return_value = "Spanish transcript"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            transcript = transcribe_audio(temp_path, language="es")
            
            assert transcript == "Spanish transcript"
            mock_transcribe.assert_called_once_with(mock_model, temp_path, "es")
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])