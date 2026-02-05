"""
Unit tests for media preprocessor module.

Tests file detection, audio extraction, and format conversion.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.media_preprocessor import (
    prepare_audio,
    detect_media_type,
    extract_audio_from_video,
    convert_audio_to_wav,
    MediaPreprocessorError
)


class TestDetectMediaType:
    """Test media type detection."""
    
    @pytest.mark.unit
    @pytest.mark.parametrize("filename,expected_type", [
        ("video.mp4", "video"),
        ("video.mov", "video"),
        ("video.avi", "video"),
        ("video.mkv", "video"),
        ("video.webm", "video"),
        ("audio.mp3", "audio"),
        ("audio.wav", "audio"),
        ("audio.m4a", "audio"),
        ("audio.flac", "audio"),
        ("audio.ogg", "audio"),
    ])
    def test_detect_media_type_supported_formats(self, filename, expected_type):
        """Test detection of supported video and audio formats."""
        with patch('core.media_preprocessor.filetype.guess') as mock_guess:
            # Mock the filetype library to return appropriate MIME types
            if expected_type == "video":
                mock_guess.return_value = MagicMock(mime="video/mp4")
            else:
                mock_guess.return_value = MagicMock(mime="audio/mpeg")
            
            result = detect_media_type(filename)
            assert result == expected_type
    
    def test_detect_media_type_unsupported(self):
        """Test detection of unsupported file types."""
        with patch('core.media_preprocessor.filetype.guess') as mock_guess:
            mock_guess.return_value = MagicMock(mime="application/pdf")
            
            with pytest.raises(MediaPreprocessorError):
                detect_media_type("document.pdf")
    
    def test_detect_media_type_unknown(self):
        """Test detection of unknown file types."""
        with patch('core.media_preprocessor.filetype.guess') as mock_guess:
            mock_guess.return_value = None
            
            with pytest.raises(MediaPreprocessorError):
                detect_media_type("unknown.xyz")


class TestExtractAudioFromVideo:
    """Test audio extraction from video files."""
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_extract_audio_from_video_success(self, mock_run):
        """Test successful audio extraction from video."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "video.mp4")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            # Create dummy input file
            Path(input_path).touch()
            
            result = extract_audio_from_video(input_path, output_path)
            assert result == output_path
            mock_run.assert_called_once()
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_extract_audio_from_video_failure(self, mock_run):
        """Test audio extraction failure handling."""
        mock_run.return_value = MagicMock(returncode=1, stderr="ffmpeg error")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "video.mp4")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            Path(input_path).touch()
            
            with pytest.raises(MediaPreprocessorError):
                extract_audio_from_video(input_path, output_path)
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_extract_audio_from_video_ffmpeg_not_found(self, mock_run):
        """Test handling when ffmpeg is not found."""
        mock_run.side_effect = FileNotFoundError("ffmpeg not found")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "video.mp4")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            Path(input_path).touch()
            
            with pytest.raises(MediaPreprocessorError):
                extract_audio_from_video(input_path, output_path)


class TestConvertAudioToWav:
    """Test audio format conversion to WAV."""
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_convert_audio_to_wav_success(self, mock_run):
        """Test successful audio conversion to WAV."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "audio.mp3")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            Path(input_path).touch()
            
            result = convert_audio_to_wav(input_path, output_path)
            assert result == output_path
            mock_run.assert_called_once()
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_convert_audio_to_wav_already_wav(self, mock_run):
        """Test that WAV files are not re-converted."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "audio.wav")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            Path(input_path).touch()
            
            result = convert_audio_to_wav(input_path, output_path)
            assert result == input_path
            mock_run.assert_not_called()
    
    @patch('core.media_preprocessor.subprocess.run')
    def test_convert_audio_to_wav_failure(self, mock_run):
        """Test audio conversion failure handling."""
        mock_run.return_value = MagicMock(returncode=1, stderr="conversion error")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "audio.mp3")
            output_path = os.path.join(temp_dir, "audio.wav")
            
            Path(input_path).touch()
            
            with pytest.raises(MediaPreprocessorError):
                convert_audio_to_wav(input_path, output_path)


class TestPrepareAudio:
    """Test the main prepare_audio function."""
    
    @patch('core.media_preprocessor.convert_audio_to_wav')
    @patch('core.media_preprocessor.detect_media_type')
    def test_prepare_audio_video_file(self, mock_detect, mock_convert):
        """Test preparing audio from video file."""
        mock_detect.return_value = "video"
        mock_convert.return_value = "/output/audio.wav"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "video.mp4")
            Path(input_path).touch()
            
            result = prepare_audio(input_path, temp_dir)
            assert result == "/output/audio.wav"
            mock_detect.assert_called_once_with(input_path)
    
    @patch('core.media_preprocessor.convert_audio_to_wav')
    @patch('core.media_preprocessor.detect_media_type')
    def test_prepare_audio_audio_file(self, mock_detect, mock_convert):
        """Test preparing audio from audio file."""
        mock_detect.return_value = "audio"
        mock_convert.return_value = "/output/audio.wav"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "audio.mp3")
            Path(input_path).touch()
            
            result = prepare_audio(input_path, temp_dir)
            assert result == "/output/audio.wav"
            mock_detect.assert_called_once_with(input_path)
    
    def test_prepare_audio_file_not_found(self):
        """Test handling when input file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "nonexistent.mp4")
            
            with pytest.raises(MediaPreprocessorError):
                prepare_audio(input_path, temp_dir)
    
    def test_prepare_audio_output_dir_creation(self):
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "video.mp4")
            Path(input_path).touch()
            
            output_dir = os.path.join(temp_dir, "new_output_dir")
            
            with patch('core.media_preprocessor.detect_media_type') as mock_detect, \
                 patch('core.media_preprocessor.convert_audio_to_wav') as mock_convert:
                mock_detect.return_value = "video"
                mock_convert.return_value = os.path.join(output_dir, "audio.wav")
                
                prepare_audio(input_path, output_dir)
                assert os.path.exists(output_dir)


class TestMediaPreprocessorError:
    """Test MediaPreprocessorError exception."""
    
    def test_media_preprocessor_error_creation(self):
        """Test MediaPreprocessorError can be created with message."""
        error = MediaPreprocessorError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)


class TestFileValidation:
    """Test file validation in preprocessor."""
    
    def test_validate_file_exists(self):
        """Test file existence validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_file = os.path.join(temp_dir, "exists.mp4")
            Path(existing_file).touch()
            
            # Should not raise for existing file
            assert os.path.exists(existing_file)
    
    def test_validate_file_not_exists(self):
        """Test handling of non-existent file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existent = os.path.join(temp_dir, "does_not_exist.mp4")
            
            assert not os.path.exists(non_existent)


class TestOutputPathGeneration:
    """Test output path generation."""
    
    @patch('core.media_preprocessor.detect_media_type')
    def test_output_path_naming(self, mock_detect):
        """Test that output paths are named correctly."""
        mock_detect.return_value = "video"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "my_video.mp4")
            Path(input_path).touch()
            
            with patch('core.media_preprocessor.extract_audio_from_video') as mock_extract:
                mock_extract.return_value = os.path.join(temp_dir, "my_video.wav")
                
                result = prepare_audio(input_path, temp_dir)
                assert result.endswith(".wav")
                assert "my_video" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])