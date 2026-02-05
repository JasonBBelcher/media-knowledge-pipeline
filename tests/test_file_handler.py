"""
Unit tests for file_handler module.

Tests file validation, directory creation, and path manipulation utilities.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.file_handler import (
    validate_file_exists,
    ensure_directory_exists,
    copy_file,
    format_file_size,
    get_file_extension,
    is_audio_file,
    is_video_file,
    is_media_file,
    sanitize_filename,
    get_unique_filename,
    FileHandlerError,
    FileNotFoundError as CustomFileNotFoundError,
    DirectoryCreationError
)


class TestValidateFileExists:
    """Test validate_file_exists function."""
    
    def test_validate_file_exists_success(self):
        """Test validating an existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = validate_file_exists(tmp_path)
            assert result is True
        finally:
            os.unlink(tmp_path)
    
    def test_validate_file_exists_nonexistent(self):
        """Test validating a nonexistent file."""
        with pytest.raises(CustomFileNotFoundError):
            validate_file_exists("/nonexistent/file.txt")
    
    def test_validate_file_exists_directory(self):
        """Test validating a directory instead of file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(CustomFileNotFoundError):
                validate_file_exists(tmp_dir)
    
    def test_validate_file_exists_empty_path(self):
        """Test validating an empty path."""
        with pytest.raises(CustomFileNotFoundError):
            validate_file_exists("")
    
    def test_validate_file_exists_none(self):
        """Test validating None as path."""
        with pytest.raises((CustomFileNotFoundError, TypeError)):
            validate_file_exists(None)


class TestEnsureDirectoryExists:
    """Test ensure_directory_exists function."""
    
    def test_ensure_directory_exists_existing(self):
        """Test ensuring an existing directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = ensure_directory_exists(tmp_dir)
            assert result is True
    
    def test_ensure_directory_exists_new(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = os.path.join(tmp_dir, "new_directory")
            
            result = ensure_directory_exists(new_dir)
            
            assert result is True
            assert os.path.exists(new_dir)
            assert os.path.isdir(new_dir)
    
    def test_ensure_directory_exists_nested(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_dir = os.path.join(tmp_dir, "level1", "level2", "level3")
            
            result = ensure_directory_exists(nested_dir)
            
            assert result is True
            assert os.path.exists(nested_dir)
            assert os.path.isdir(nested_dir)
    
    def test_ensure_directory_exists_permission_error(self):
        """Test handling of permission errors."""
        # Try to create directory in a location that requires permissions
        with pytest.raises(DirectoryCreationError):
            ensure_directory_exists("/root/test_directory")
    
    def test_ensure_directory_exists_empty_path(self):
        """Test ensuring directory with empty path."""
        with pytest.raises(DirectoryCreationError):
            ensure_directory_exists("")


class TestCopyFile:
    """Test copy_file function."""
    
    @pytest.mark.slow
    def test_copy_file_success(self):
        """Test successful file copy."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create source file
            src_file = os.path.join(tmp_dir, "source.txt")
            with open(src_file, "w") as f:
                f.write("Test content")
            
            # Copy file
            dst_file = os.path.join(tmp_dir, "destination.txt")
            result = copy_file(src_file, dst_file)
            
            assert result is True
            assert os.path.exists(dst_file)
            
            # Verify content
            with open(dst_file, "r") as f:
                assert f.read() == "Test content"
    
    def test_copy_file_to_new_directory(self):
        """Test copying file to a new directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create source file
            src_file = os.path.join(tmp_dir, "source.txt")
            with open(src_file, "w") as f:
                f.write("Test content")
            
            # Copy to new directory
            new_dir = os.path.join(tmp_dir, "new_dir")
            dst_file = os.path.join(new_dir, "destination.txt")
            result = copy_file(src_file, dst_file)
            
            assert result is True
            assert os.path.exists(dst_file)
            assert os.path.exists(new_dir)
    
    def test_copy_file_nonexistent_source(self):
        """Test copying nonexistent source file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            src_file = os.path.join(tmp_dir, "nonexistent.txt")
            dst_file = os.path.join(tmp_dir, "destination.txt")
            
            with pytest.raises(CustomFileNotFoundError):
                copy_file(src_file, dst_file)
    
    def test_copy_file_overwrite(self):
        """Test overwriting existing destination file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create source file
            src_file = os.path.join(tmp_dir, "source.txt")
            with open(src_file, "w") as f:
                f.write("New content")
            
            # Create destination file with different content
            dst_file = os.path.join(tmp_dir, "destination.txt")
            with open(dst_file, "w") as f:
                f.write("Old content")
            
            # Copy file (should overwrite)
            result = copy_file(src_file, dst_file)
            
            assert result is True
            
            # Verify new content
            with open(dst_file, "r") as f:
                assert f.read() == "New content"


class TestFormatFileSize:
    """Test format_file_size function."""
    
    def test_format_file_size_bytes(self):
        """Test formatting size in bytes."""
        result = format_file_size(500)
        assert "500" in result
        assert "B" in result
    
    def test_format_file_size_kilobytes(self):
        """Test formatting size in kilobytes."""
        result = format_file_size(2048)
        assert "2.0" in result or "2" in result
        assert "KB" in result
    
    def test_format_file_size_megabytes(self):
        """Test formatting size in megabytes."""
        result = format_file_size(2 * 1024 * 1024)
        assert "2.0" in result or "2" in result
        assert "MB" in result
    
    def test_format_file_size_gigabytes(self):
        """Test formatting size in gigabytes."""
        result = format_file_size(2 * 1024 * 1024 * 1024)
        assert "2.0" in result or "2" in result
        assert "GB" in result
    
    def test_format_file_size_zero(self):
        """Test formatting zero size."""
        result = format_file_size(0)
        assert "0" in result
    
    def test_format_file_size_large(self):
        """Test formatting very large size."""
        result = format_file_size(10 * 1024 * 1024 * 1024)
        assert "10" in result
        assert "GB" in result
    
    def test_format_file_size_decimal(self):
        """Test formatting size with decimal."""
        result = format_file_size(1536)  # 1.5 KB
        assert "1.5" in result or "1" in result


class TestGetFileExtension:
    """Test get_file_extension function."""
    
    def test_get_file_extension_basic(self):
        """Test getting basic file extension."""
        result = get_file_extension("test.txt")
        assert result == ".txt"
    
    def test_get_file_extension_multiple_dots(self):
        """Test getting extension with multiple dots."""
        result = get_file_extension("test.file.txt")
        assert result == ".txt"
    
    def test_get_file_extension_no_extension(self):
        """Test getting extension when none exists."""
        result = get_file_extension("testfile")
        assert result == ""
    
    def test_get_file_extension_path(self):
        """Test getting extension from full path."""
        result = get_file_extension("/path/to/test.txt")
        assert result == ".txt"
    
    def test_get_file_extension_uppercase(self):
        """Test getting uppercase extension."""
        result = get_file_extension("test.TXT")
        assert result == ".TXT" or result == ".txt"
    
    def test_get_file_extension_hidden_file(self):
        """Test getting extension from hidden file."""
        result = get_file_extension(".hidden")
        assert result == ""


class TestIsAudioFile:
    """Test is_audio_file function."""
    
    def test_is_audio_file_mp3(self):
        """Test identifying MP3 audio file."""
        assert is_audio_file("test.mp3") is True
    
    def test_is_audio_file_wav(self):
        """Test identifying WAV audio file."""
        assert is_audio_file("test.wav") is True
    
    def test_is_audio_file_m4a(self):
        """Test identifying M4A audio file."""
        assert is_audio_file("test.m4a") is True
    
    def test_is_audio_file_flac(self):
        """Test identifying FLAC audio file."""
        assert is_audio_file("test.flac") is True
    
    def test_is_audio_file_ogg(self):
        """Test identifying OGG audio file."""
        assert is_audio_file("test.ogg") is True
    
    def test_is_audio_file_not_audio(self):
        """Test identifying non-audio file."""
        assert is_audio_file("test.txt") is False
    
    def test_is_audio_file_video(self):
        """Test identifying video file as not audio."""
        assert is_audio_file("test.mp4") is False
    
    def test_is_audio_file_case_insensitive(self):
        """Test case-insensitive audio file detection."""
        assert is_audio_file("test.MP3") is True
        assert is_audio_file("test.Wav") is True


class TestIsVideoFile:
    """Test is_video_file function."""
    
    def test_is_video_file_mp4(self):
        """Test identifying MP4 video file."""
        assert is_video_file("test.mp4") is True
    
    def test_is_video_file_mov(self):
        """Test identifying MOV video file."""
        assert is_video_file("test.mov") is True
    
    def test_is_video_file_avi(self):
        """Test identifying AVI video file."""
        assert is_video_file("test.avi") is True
    
    def test_is_video_file_mkv(self):
        """Test identifying MKV video file."""
        assert is_video_file("test.mkv") is True
    
    def test_is_video_file_webm(self):
        """Test identifying WebM video file."""
        assert is_video_file("test.webm") is True
    
    def test_is_video_file_not_video(self):
        """Test identifying non-video file."""
        assert is_video_file("test.txt") is False
    
    def test_is_video_file_audio(self):
        """Test identifying audio file as not video."""
        assert is_video_file("test.mp3") is False
    
    def test_is_video_file_case_insensitive(self):
        """Test case-insensitive video file detection."""
        assert is_video_file("test.MP4") is True
        assert is_video_file("test.Mov") is True


class TestIsMediaFile:
    """Test is_media_file function."""
    
    def test_is_media_file_audio(self):
        """Test identifying audio file as media."""
        assert is_media_file("test.mp3") is True
    
    def test_is_media_file_video(self):
        """Test identifying video file as media."""
        assert is_media_file("test.mp4") is True
    
    def test_is_media_file_not_media(self):
        """Test identifying non-media file."""
        assert is_media_file("test.txt") is False
    
    def test_is_media_file_various_audio(self):
        """Test identifying various audio formats."""
        audio_formats = ["mp3", "wav", "m4a", "flac", "ogg", "aac"]
        for fmt in audio_formats:
            assert is_media_file(f"test.{fmt}") is True
    
    def test_is_media_file_various_video(self):
        """Test identifying various video formats."""
        video_formats = ["mp4", "mov", "avi", "mkv", "webm", "flv"]
        for fmt in video_formats:
            assert is_media_file(f"test.{fmt}") is True


class TestSanitizeFilename:
    """Test sanitize_filename function."""
    
    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization."""
        result = sanitize_filename("test file.txt")
        assert "test_file.txt" in result or "test-file.txt" in result
    
    def test_sanitize_filename_special_chars(self):
        """Test sanitizing special characters."""
        result = sanitize_filename("test@#$%^&*file.txt")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
        assert "%" not in result
    
    def test_sanitize_filename_spaces(self):
        """Test sanitizing spaces."""
        result = sanitize_filename("my test file.txt")
        assert " " not in result
    
    def test_sanitize_filename_path_separators(self):
        """Test sanitizing path separators."""
        result = sanitize_filename("test/file.txt")
        assert "/" not in result
    
    def test_sanitize_filename_unicode(self):
        """Test sanitizing unicode characters."""
        result = sanitize_filename("test文件.txt")
        assert "文件" in result or len(result) > 0
    
    def test_sanitize_filename_empty(self):
        """Test sanitizing empty filename."""
        result = sanitize_filename("")
        assert result == "" or result == "unnamed"
    
    def test_sanitize_filename_dots(self):
        """Test sanitizing multiple dots."""
        result = sanitize_filename("test...file.txt")
        assert result.endswith(".txt")


class TestGetUniqueFilename:
    """Test get_unique_filename function."""
    
    def test_get_unique_filename_new(self):
        """Test getting unique filename for new file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = "test.txt"
            result = get_unique_filename(tmp_dir, filename)
            
            assert result == "test.txt"
    
    def test_get_unique_filename_existing(self):
        """Test getting unique filename when file exists."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create existing file
            existing_file = os.path.join(tmp_dir, "test.txt")
            with open(existing_file, "w") as f:
                f.write("content")
            
            result = get_unique_filename(tmp_dir, "test.txt")
            
            assert result != "test.txt"
            assert "test" in result
            assert ".txt" in result
    
    def test_get_unique_filename_multiple_existing(self):
        """Test getting unique filename with multiple existing files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create multiple existing files
            for i in range(3):
                filename = f"test_{i}.txt" if i > 0 else "test.txt"
                filepath = os.path.join(tmp_dir, filename)
                with open(filepath, "w") as f:
                    f.write("content")
            
            result = get_unique_filename(tmp_dir, "test.txt")
            
            assert result != "test.txt"
            assert result != "test_1.txt"
            assert result != "test_2.txt"
    
    def test_get_unique_filename_custom_separator(self):
        """Test getting unique filename with custom separator."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create existing file
            existing_file = os.path.join(tmp_dir, "test.txt")
            with open(existing_file, "w") as f:
                f.write("content")
            
            result = get_unique_filename(tmp_dir, "test.txt", separator="-")
            
            assert "-" in result
            assert ".txt" in result


class TestFileHandlerError:
    """Test FileHandlerError exception."""
    
    def test_file_handler_error_creation(self):
        """Test FileHandlerError can be created."""
        error = FileHandlerError("File handler error")
        
        assert str(error) == "File handler error"
        assert isinstance(error, Exception)
    
    def test_file_handler_error_inheritance(self):
        """Test FileHandlerError inherits from Exception."""
        error = FileHandlerError("Test error")
        
        assert isinstance(error, Exception)
        assert isinstance(error, BaseException)


class TestCustomFileNotFoundError:
    """Test custom FileNotFoundError exception."""
    
    def test_custom_file_not_found_error_creation(self):
        """Test custom FileNotFoundError can be created."""
        error = CustomFileNotFoundError("File not found")
        
        assert str(error) == "File not found"
        assert isinstance(error, Exception)
    
    def test_custom_file_not_found_error_inheritance(self):
        """Test custom FileNotFoundError inherits from FileHandlerError."""
        error = CustomFileNotFoundError("Test error")
        
        assert isinstance(error, FileHandlerError)
        assert isinstance(error, Exception)


class TestDirectoryCreationError:
    """Test DirectoryCreationError exception."""
    
    def test_directory_creation_error_creation(self):
        """Test DirectoryCreationError can be created."""
        error = DirectoryCreationError("Directory creation failed")
        
        assert str(error) == "Directory creation failed"
        assert isinstance(error, Exception)
    
    def test_directory_creation_error_inheritance(self):
        """Test DirectoryCreationError inherits from FileHandlerError."""
        error = DirectoryCreationError("Test error")
        
        assert isinstance(error, FileHandlerError)
        assert isinstance(error, Exception)


class TestFileHandlerIntegration:
    """Test file handler integration scenarios."""
    
    def test_validate_and_copy_workflow(self):
        """Test workflow of validating and copying a file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create source file
            src_file = os.path.join(tmp_dir, "source.txt")
            with open(src_file, "w") as f:
                f.write("Test content")
            
            # Validate source
            assert validate_file_exists(src_file) is True
            
            # Ensure destination directory exists
            dst_dir = os.path.join(tmp_dir, "output")
            assert ensure_directory_exists(dst_dir) is True
            
            # Copy file
            dst_file = os.path.join(dst_dir, "destination.txt")
            assert copy_file(src_file, dst_file) is True
            
            # Verify destination exists
            assert validate_file_exists(dst_file) is True
    
    def test_media_file_detection_workflow(self):
        """Test workflow of detecting media files."""
        media_files = [
            ("audio.mp3", True, False),
            ("video.mp4", False, True),
            ("document.pdf", False, False)
        ]
        
        for filename, is_audio, is_video in media_files:
            assert is_audio_file(filename) == is_audio
            assert is_video_file(filename) == is_video
            assert is_media_file(filename) == (is_audio or is_video)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])