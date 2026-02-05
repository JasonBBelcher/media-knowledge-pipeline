"""
Unit tests for file_scanner module.

Tests file scanning, detection, and monitoring functionality.
"""

import pytest
import tempfile
import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.file_scanner import FileScanner, ScanResult, ScanMode, FileScannerError
from utils.file_handler import FileHandlerError


class TestFileScanner:
    """Test FileScanner class functionality."""
    
    def test_initialization_with_defaults(self):
        """Test scanner initialization with default parameters."""
        scanner = FileScanner()
        
        assert scanner.scan_directory == Path("~/Downloads").expanduser()
        assert scanner.audio_directory == Path("data/audio")
        assert scanner.video_directory == Path("data/videos")
        assert scanner.supported_extensions["video"] == [
            ".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv"
        ]
        assert scanner.supported_extensions["audio"] == [
            ".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma"
        ]
    
    def test_initialization_with_custom_params(self, tmp_path):
        """Test scanner initialization with custom parameters."""
        scanner = FileScanner(
            scan_directory=tmp_path / "scan",
            audio_directory=tmp_path / "audio",
            video_directory=tmp_path / "video"
        )
        
        assert scanner.scan_directory == tmp_path / "scan"
        assert scanner.audio_directory == tmp_path / "audio"
        assert scanner.video_directory == tmp_path / "video"
    
    def test_detect_file_type_video(self):
        """Test video file type detection."""
        scanner = FileScanner()
        
        # Test various video extensions
        assert scanner._detect_file_type(Path("video.mp4")) == "video"
        assert scanner._detect_file_type(Path("video.mov")) == "video"
        assert scanner._detect_file_type(Path("video.avi")) == "video"
    
    def test_detect_file_type_audio(self):
        """Test audio file type detection."""
        scanner = FileScanner()
        
        # Test various audio extensions
        assert scanner._detect_file_type(Path("audio.mp3")) == "audio"
        assert scanner._detect_file_type(Path("audio.wav")) == "audio"
        assert scanner._detect_file_type(Path("audio.m4a")) == "audio"
    
    def test_detect_file_type_unsupported(self):
        """Test unsupported file type detection."""
        scanner = FileScanner()
        
        # Test unsupported extensions
        assert scanner._detect_file_type(Path("document.pdf")) is None
        assert scanner._detect_file_type(Path("image.jpg")) is None
        assert scanner._detect_file_type(Path("text.txt")) is None
    
    def test_get_destination_directory(self):
        """Test destination directory selection."""
        scanner = FileScanner()
        
        assert scanner._get_destination_directory("audio") == scanner.audio_directory
        assert scanner._get_destination_directory("video") == scanner.video_directory
    
    def test_get_destination_directory_invalid(self):
        """Test invalid file type handling."""
        scanner = FileScanner()
        
        with pytest.raises(FileScannerError):
            scanner._get_destination_directory("invalid")
    
    def test_copy_media_file_success(self, tmp_path):
        """Test successful file copying."""
        scanner = FileScanner(
            audio_directory=tmp_path / "audio",
            video_directory=tmp_path / "video"
        )
        
        # Create a test file
        source_file = tmp_path / "test.mp3"
        source_file.write_text("test audio content")
        
        result = scanner._copy_media_file(source_file, "audio")
        
        assert result.status == "copied"
        assert result.file_path == source_file
        assert result.file_type == "audio"
        assert result.destination == tmp_path / "audio" / "test.mp3"
        assert result.destination.exists()
        assert result.destination.read_text() == "test audio content"
    
    def test_copy_media_file_already_exists(self, tmp_path):
        """Test file copying when destination already exists."""
        scanner = FileScanner(
            audio_directory=tmp_path / "audio",
            video_directory=tmp_path / "video"
        )
        
        # Create source file
        source_file = tmp_path / "test.mp3"
        source_file.write_text("test audio content")
        
        # Create destination file (already exists)
        dest_dir = tmp_path / "audio"
        dest_dir.mkdir(exist_ok=True)
        dest_file = dest_dir / "test.mp3"
        dest_file.write_text("existing content")
        
        result = scanner._copy_media_file(source_file, "audio")
        
        assert result.status == "skipped"
        assert result.error_message == "File already exists in destination"
        # Ensure original content wasn't overwritten
        assert dest_file.read_text() == "existing content"
    
    def test_copy_media_file_error(self):
        """Test file copying error handling."""
        scanner = FileScanner()
        
        # Non-existent file
        result = scanner._copy_media_file(Path("nonexistent.mp3"), "audio")
        
        assert result.status == "error"
        assert "File not found" in result.error_message
    
    def test_scan_directory_empty(self, tmp_path):
        """Test scanning an empty directory."""
        scanner = FileScanner(scan_directory=tmp_path)
        
        results = scanner.scan_directory_for_media()
        
        assert len(results) == 0
        assert scanner.get_statistics()["total_processed"] == 0
    
    def test_scan_directory_with_media_files(self, tmp_path):
        """Test scanning a directory with media files."""
        scanner = FileScanner(
            scan_directory=tmp_path,
            audio_directory=tmp_path / "audio",
            video_directory=tmp_path / "video"
        )
        
        # Create test files
        (tmp_path / "audio.mp3").write_text("audio content")
        (tmp_path / "video.mp4").write_text("video content")
        (tmp_path / "document.pdf").write_text("document content")  # Should be ignored
        
        results = scanner.scan_directory_for_media()
        
        # Should process only media files (2 files)
        assert len(results) == 2
        
        # Check audio file result
        audio_result = next(r for r in results if r.file_type == "audio")
        assert audio_result.status == "copied"
        assert (tmp_path / "audio" / "audio.mp3").exists()
        
        # Check video file result
        video_result = next(r for r in results if r.file_type == "video")
        assert video_result.status == "copied"
        assert (tmp_path / "video" / "video.mp4").exists()
        
        # Check statistics - should count all processed files (including ignored ones)
        stats = scanner.get_statistics()
        assert stats["total_processed"] == 3  # All files in directory
        assert stats["audio_files_copied"] == 1
        assert stats["video_files_copied"] == 1
    
    def test_scan_directory_nonexistent(self):
        """Test scanning a non-existent directory."""
        scanner = FileScanner(scan_directory="/nonexistent/path")
        
        results = scanner.scan_directory_for_media()
        
        assert len(results) == 0
    
    def test_scan_directory_file_path(self):
        """Test scanning a file path instead of directory."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            scanner = FileScanner(scan_directory=tmp.name)
            
            results = scanner.scan_directory_for_media()
            
            assert len(results) == 0
            
            os.unlink(tmp.name)
    
    @patch('core.file_scanner.time.sleep')
    def test_watch_directory_basic(self, mock_sleep, tmp_path):
        """Test basic watch directory functionality."""
        scanner = FileScanner(
            scan_directory=tmp_path,
            audio_directory=tmp_path / "audio",
            video_directory=tmp_path / "video"
        )
        
        # Mock sleep to break the loop after one iteration
        mock_sleep.side_effect = [None, KeyboardInterrupt]
        
        # Create callback tracker
        callback_calls = []
        
        def callback(result):
            callback_calls.append(result)
        
        # Start watching
        try:
            scanner.watch_directory(callback=callback, poll_interval=1)
        except KeyboardInterrupt:
            pass  # Expected
        
        # Should have called sleep twice (once for initial wait, once interrupted)
        assert mock_sleep.call_count == 2
    
    def test_scan_result_representation(self):
        """Test ScanResult dataclass representation."""
        result = ScanResult(
            file_path=Path("test.mp3"),
            file_type="audio",
            destination=Path("dest/test.mp3"),
            status="copied",
            file_size=1024
        )
        
        assert result.file_path.name == "test.mp3"
        assert result.file_type == "audio"
        assert result.status == "copied"
        assert result.file_size == 1024
        assert result.error_message is None
    
    def test_scan_mode_enum(self):
        """Test ScanMode enum values."""
        assert ScanMode.SCAN.value == "scan"
        assert ScanMode.WATCH.value == "watch"


class TestIntegration:
    """Integration tests for file scanner functionality."""
    
    def test_scanner_with_real_files(self, tmp_path):
        """Test scanner with real file operations."""
        # Create test directory structure
        scan_dir = tmp_path / "scan"
        audio_dir = tmp_path / "audio"
        video_dir = tmp_path / "video"
        
        scan_dir.mkdir()
        
        # Create test media files
        (scan_dir / "test_audio.mp3").write_bytes(b"fake audio data")
        (scan_dir / "test_video.mp4").write_bytes(b"fake video data")
        (scan_dir / "ignore_me.txt").write_bytes(b"text data")  # Should be ignored
        
        scanner = FileScanner(
            scan_directory=scan_dir,
            audio_directory=audio_dir,
            video_directory=video_dir
        )
        
        results = scanner.scan_directory_for_media()
        
        # Verify results
        assert len(results) == 2
        
        # Verify files were copied
        assert (audio_dir / "test_audio.mp3").exists()
        assert (video_dir / "test_video.mp4").exists()
        
        # Verify ignored file wasn't copied
        assert not (audio_dir / "ignore_me.txt").exists()
        assert not (video_dir / "ignore_me.txt").exists()
        
        # Verify file contents
        assert (audio_dir / "test_audio.mp3").read_bytes() == b"fake audio data"
        assert (video_dir / "test_video.mp4").read_bytes() == b"fake video data"


if __name__ == "__main__":
    pytest.main([__file__])