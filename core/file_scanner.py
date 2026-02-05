"""
File Scanner Module for Media Knowledge Pipeline

Provides automated scanning and monitoring of directories for media files.
Supports both one-time scanning and continuous watching modes.
"""

import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set, Callable
from dataclasses import dataclass
from enum import Enum

from utils.file_handler import (
    validate_file_exists,
    copy_file,
    is_audio_file,
    is_video_file,
    FileHandlerError
)

# Optional watchdog import for efficient file watching
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class ScanMode(Enum):
    """Scan operation modes."""
    SCAN = "scan"
    WATCH = "watch"


@dataclass
class ScanResult:
    """Result of a file scanning operation."""
    file_path: Path
    file_type: str  # "audio" or "video"
    destination: Path
    status: str  # "copied", "skipped", "error"
    error_message: Optional[str] = None
    file_size: int = 0


class FileScannerError(Exception):
    """Custom exception for file scanner errors."""
    pass


if WATCHDOG_AVAILABLE:
    class MediaFileEventHandler(FileSystemEventHandler):
        """Watchdog event handler for media file creation events."""
        
        def __init__(self, scanner, callback=None):
            self.scanner = scanner
            self.callback = callback
        
        def on_created(self, event):
            """Handle file creation events."""
            if not event.is_directory:
                file_path = Path(event.src_path)
                
                # Skip partially downloaded files (common pattern)
                if file_path.name.startswith('.') or file_path.name.endswith('.part') or file_path.name.endswith('.tmp'):
                    return
                
                # Wait a moment for file to be fully written
                time.sleep(0.5)
                
                # Process the file
                file_type = self.scanner._detect_file_type(file_path)
                
                if file_type:
                    result = self.scanner._copy_media_file(file_path, file_type)
                    
                    # Call callback if provided
                    if self.callback:
                        self.callback(result)
                    
                    # Track processed files
                    self.scanner.processed_files.add(file_path)


class FileScanner:
    """
    Scanner for detecting and processing media files in directories.
    
    This class provides functionality to:
    - Scan directories for media files
    - Copy files to appropriate data directories
    - Monitor directories for new files (watch mode)
    - Handle file type detection and validation
    - Auto-process files through the pipeline
    """
    
    def __init__(
        self,
        scan_directory: str = "~/Downloads",
        audio_directory: str = "data/audio",
        video_directory: str = "data/videos",
        supported_extensions: Optional[Dict[str, List[str]]] = None,
        logger: Optional[logging.Logger] = None,
        auto_process: bool = False,
        process_callback: Optional[Callable[[Path], None]] = None,
        dry_run: bool = False
    ):
        """
        Initialize the file scanner.
        
        Args:
            scan_directory: Directory to scan for media files
            audio_directory: Directory to copy audio files to
            video_directory: Directory to copy video files to
            supported_extensions: Dictionary mapping file types to extensions
            logger: Optional logger instance
            auto_process: Whether to automatically process files after copying
            process_callback: Callback function for processing files
            dry_run: Whether to simulate operations without actual copying
        """
        # Expand user directory paths
        self.scan_directory = Path(scan_directory).expanduser()
        self.audio_directory = Path(audio_directory)
        self.video_directory = Path(video_directory)
        
        # Ensure data directories exist (unless dry run)
        if not dry_run:
            self.audio_directory.mkdir(parents=True, exist_ok=True)
            self.video_directory.mkdir(parents=True, exist_ok=True)
        
        # Default supported extensions
        self.supported_extensions = supported_extensions or {
            "video": [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv"],
            "audio": [".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma"]
        }
        
        # Set up logging
        self.logger = logger or self._setup_default_logger()
        
        # Auto-processing settings
        self.auto_process = auto_process
        self.process_callback = process_callback
        self.dry_run = dry_run
        
        # Track processed files to avoid duplicates
        self.processed_files: Set[Path] = set()
    
    def _setup_default_logger(self) -> logging.Logger:
        """Set up a default logger for the scanner."""
        logger = logging.getLogger("file_scanner")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _detect_file_type(self, file_path: Path) -> Optional[str]:
        """
        Detect the type of a media file by extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            "audio", "video", or None if not a supported media file
        """
        file_extension = file_path.suffix.lower()
        
        if file_extension in self.supported_extensions["video"]:
            return "video"
        elif file_extension in self.supported_extensions["audio"]:
            return "audio"
        
        return None
    
    def _get_destination_directory(self, file_type: str) -> Path:
        """Get the destination directory for a file type."""
        if file_type == "audio":
            return self.audio_directory
        elif file_type == "video":
            return self.video_directory
        else:
            raise FileScannerError(f"Unsupported file type: {file_type}")
    
    def _copy_media_file(self, file_path: Path, file_type: str) -> ScanResult:
        """
        Copy a media file to the appropriate data directory.
        
        Args:
            file_path: Path to the source file
            file_type: Type of media file ("audio" or "video")
            
        Returns:
            ScanResult with operation status
        """
        try:
            # Validate source file
            validate_file_exists(file_path)
            
            # Skip zero-byte files (incomplete downloads)
            file_size = file_path.stat().st_size
            if file_size == 0:
                return ScanResult(
                    file_path=file_path,
                    file_type=file_type,
                    destination=Path(),
                    status="skipped",
                    error_message="File is zero bytes (likely incomplete download)"
                )
            
            # Get destination directory
            dest_dir = self._get_destination_directory(file_type)
            
            # Create destination filename
            dest_file = dest_dir / file_path.name
            
            # Check if file already exists in destination
            if dest_file.exists():
                return ScanResult(
                    file_path=file_path,
                    file_type=file_type,
                    destination=dest_file,
                    status="skipped",
                    error_message="File already exists in destination"
                )
            
            # Handle dry-run mode
            if self.dry_run:
                return ScanResult(
                    file_path=file_path,
                    file_type=file_type,
                    destination=dest_file,
                    status="dry_run",
                    file_size=file_size
                )
            
            # Copy the file
            copy_file(file_path, dest_file)
            
            # Auto-process if enabled
            if self.auto_process and self.process_callback:
                try:
                    self.process_callback(dest_file)
                except Exception as e:
                    self.logger.warning(f"Auto-processing failed for {dest_file}: {e}")
            
            return ScanResult(
                file_path=file_path,
                file_type=file_type,
                destination=dest_file,
                status="copied",
                file_size=file_size
            )
            
        except FileHandlerError as e:
            return ScanResult(
                file_path=file_path,
                file_type=file_type,
                destination=Path(),
                status="error",
                error_message=str(e)
            )
    
    def scan_directory_for_media(self) -> List[ScanResult]:
        """
        Scan the configured directory for media files.
        
        Returns:
            List of ScanResult objects for each processed file
        """
        results = []
        
        # Check if scan directory exists
        if not self.scan_directory.exists():
            self.logger.warning(f"Scan directory does not exist: {self.scan_directory}")
            return results
        
        if not self.scan_directory.is_dir():
            self.logger.warning(f"Scan path is not a directory: {self.scan_directory}")
            return results
        
        self.logger.info(f"Scanning directory: {self.scan_directory}")
        
        # Scan all files in directory
        for file_path in self.scan_directory.iterdir():
            if file_path.is_file():
                file_type = self._detect_file_type(file_path)
                
                if file_type:
                    result = self._copy_media_file(file_path, file_type)
                    results.append(result)
                    
                    # Log the result
                    if result.status == "copied":
                        self.logger.info(
                            f"Copied {file_type} file: {file_path.name} "
                            f"({result.file_size:,} bytes) -> {result.destination}"
                        )
                    elif result.status == "skipped":
                        self.logger.info(
                            f"Skipped {file_type} file: {file_path.name} "
                            f"({result.error_message})"
                        )
                    else:
                        self.logger.error(
                            f"Error processing {file_type} file: {file_path.name} - "
                            f"{result.error_message}"
                        )
                
                # Track processed files
                self.processed_files.add(file_path)
        
        return results
    
    def watch_directory(
        self,
        callback: Optional[Callable[[ScanResult], None]] = None,
        poll_interval: int = 5,
        use_watchdog: bool = True
    ) -> None:
        """
        Continuously monitor the directory for new media files.
        
        Args:
            callback: Optional callback function to call when a file is processed
            poll_interval: Interval between scans in seconds (fallback if watchdog not available)
            use_watchdog: Whether to use watchdog library for efficient monitoring
        """
        # Use watchdog if available and requested
        if use_watchdog and WATCHDOG_AVAILABLE:
            self._watch_with_watchdog(callback)
        else:
            self._watch_with_polling(callback, poll_interval)
    
    def _watch_with_watchdog(self, callback: Optional[Callable[[ScanResult], None]] = None) -> None:
        """Watch directory using watchdog library for efficient file system events."""
        self.logger.info(f"Starting watchdog watch mode on directory: {self.scan_directory}")
        self.logger.info("Press Ctrl+C to stop watching")
        
        observer = Observer()
        event_handler = MediaFileEventHandler(self, callback)
        
        try:
            observer.schedule(event_handler, str(self.scan_directory), recursive=False)
            observer.start()
            
            # Keep the main thread alive
            while observer.is_alive():
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Watch mode stopped by user")
        except Exception as e:
            self.logger.error(f"Error in watchdog watch mode: {e}")
            raise
        finally:
            observer.stop()
            observer.join()
    
    def _watch_with_polling(
        self,
        callback: Optional[Callable[[ScanResult], None]] = None,
        poll_interval: int = 5
    ) -> None:
        """Watch directory using polling (fallback method)."""
        self.logger.info(f"Starting polling watch mode on directory: {self.scan_directory}")
        self.logger.info(f"Poll interval: {poll_interval} seconds")
        self.logger.info("Press Ctrl+C to stop watching")
        
        try:
            while True:
                # Get current files in directory
                current_files = set()
                if self.scan_directory.exists() and self.scan_directory.is_dir():
                    current_files = {
                        file_path for file_path in self.scan_directory.iterdir() 
                        if file_path.is_file()
                    }
                
                # Find new files
                new_files = current_files - self.processed_files
                
                if new_files:
                    self.logger.info(f"Found {len(new_files)} new file(s)")
                    
                    for file_path in new_files:
                        file_type = self._detect_file_type(file_path)
                        
                        if file_type:
                            result = self._copy_media_file(file_path, file_type)
                            
                            # Log the result
                            if result.status == "copied":
                                self.logger.info(
                                    f"Copied {file_type} file: {file_path.name} "
                                    f"({result.file_size:,} bytes) -> {result.destination}"
                                )
                            elif result.status == "skipped":
                                self.logger.info(
                                    f"Skipped {file_type} file: {file_path.name} "
                                    f"(already exists in destination)"
                                )
                            else:
                                self.logger.error(
                                    f"Error processing {file_type} file: {file_path.name} - "
                                    f"{result.error_message}"
                                )
                            
                            # Call callback if provided
                            if callback:
                                callback(result)
                        
                        # Track processed files
                        self.processed_files.add(file_path)
                
                # Wait for next scan
                time.sleep(poll_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Watch mode stopped by user")
        except Exception as e:
            self.logger.error(f"Error in watch mode: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about processed files."""
        return {
            "total_processed": len(self.processed_files),
            "audio_files_copied": len([f for f in self.processed_files 
                                      if self._detect_file_type(f) == "audio"]),
            "video_files_copied": len([f for f in self.processed_files 
                                      if self._detect_file_type(f) == "video"])
        }