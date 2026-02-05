"""
File Handler Utility Module

Provides file validation, directory creation, and path manipulation utilities.

This module contains helper functions for common file system operations
used throughout the Media-to-Knowledge Pipeline.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Union


class FileHandlerError(Exception):
    """Custom exception for file handler errors."""
    pass


class FileNotFoundError(FileHandlerError):
    """Raised when a file is not found."""
    pass


class DirectoryCreationError(FileHandlerError):
    """Raised when directory creation fails."""
    pass


class FileValidationError(FileHandlerError):
    """Raised when file validation fails."""
    pass


def validate_file_exists(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file exists and return its Path object.
    
    Args:
        file_path: Path to the file (string or Path object).
    
    Returns:
        Path object for the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
    
    Example:
        >>> path = validate_file_exists("audio.wav")
        >>> print(path)
        PosixPath('audio.wav')
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )
    if not path.is_file():
        raise FileValidationError(
            f"Path is not a file: {file_path}"
        )
    return path


def validate_file_readable(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file exists and is readable.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        Path object for the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        FileValidationError: If the file is not readable.
    """
    path = validate_file_exists(file_path)
    if not os.access(path, os.R_OK):
        raise FileValidationError(
            f"File is not readable: {file_path}"
        )
    return path


def validate_file_writable(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file can be written (either exists and is writable, or parent directory is writable).
    
    Args:
        file_path: Path to the file.
    
    Returns:
        Path object for the file.
    
    Raises:
        FileValidationError: If the file cannot be written.
    """
    path = Path(file_path)
    
    if path.exists():
        # File exists, check if writable
        if not os.access(path, os.W_OK):
            raise FileValidationError(
                f"File is not writable: {file_path}"
            )
    else:
        # File doesn't exist, check if parent directory is writable
        parent = path.parent
        if not parent.exists():
            raise FileValidationError(
                f"Parent directory does not exist: {parent}"
            )
        if not os.access(parent, os.W_OK):
            raise FileValidationError(
                f"Parent directory is not writable: {parent}"
            )
    
    return path


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        File size in bytes.
    
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = validate_file_exists(file_path)
    return path.stat().st_size


def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get the file extension (including the dot).
    
    Args:
        file_path: Path to the file.
    
    Returns:
        File extension (e.g., ".wav", ".mp4").
    
    Example:
        >>> ext = get_file_extension("audio.wav")
        >>> print(ext)
        .wav
    """
    return Path(file_path).suffix.lower()


def get_file_name_without_extension(file_path: Union[str, Path]) -> str:
    """
    Get the file name without the extension.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        File name without extension.
    
    Example:
        >>> name = get_file_name_without_extension("audio.wav")
        >>> print(name)
        audio
    """
    return Path(file_path).stem


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory.
    
    Returns:
        Path object for the directory.
    
    Raises:
        DirectoryCreationError: If directory creation fails.
    
    Example:
        >>> dir_path = ensure_directory_exists("./output")
        >>> print(dir_path)
        PosixPath('output')
    """
    path = Path(directory)
    
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise DirectoryCreationError(
            f"Failed to create directory '{directory}': {e}"
        ) from e


def create_temp_directory(prefix: str = "media_knowledge_") -> Path:
    """
    Create a temporary directory with a given prefix.
    
    Args:
        prefix: Prefix for the temporary directory name.
    
    Returns:
        Path object for the temporary directory.
    
    Example:
        >>> temp_dir = create_temp_directory("transcription_")
        >>> print(temp_dir)
        PosixPath('/tmp/transcription_abc123')
    """
    import tempfile
    temp_path = Path(tempfile.mkdtemp(prefix=prefix))
    return temp_path


def list_files_in_directory(
    directory: Union[str, Path],
    pattern: Optional[str] = None,
    recursive: bool = False
) -> List[Path]:
    """
    List files in a directory, optionally matching a pattern.
    
    Args:
        directory: Path to the directory.
        pattern: Optional glob pattern (e.g., "*.wav", "*.mp4").
        recursive: Whether to search recursively in subdirectories.
    
    Returns:
        List of Path objects for matching files.
    
    Example:
        >>> wav_files = list_files_in_directory("./audio", "*.wav")
        >>> print(len(wav_files))
        5
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )
    
    if not dir_path.is_dir():
        raise FileValidationError(
            f"Path is not a directory: {directory}"
        )
    
    if recursive:
        files = list(dir_path.rglob(pattern if pattern else "*"))
    else:
        files = list(dir_path.glob(pattern if pattern else "*"))
    
    # Filter to only include files (not directories)
    return [f for f in files if f.is_file()]


def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path]
) -> Path:
    """
    Copy a file from source to destination.
    
    Args:
        source: Path to the source file.
        destination: Path to the destination (file or directory).
    
    Returns:
        Path object for the copied file.
    
    Raises:
        FileNotFoundError: If source file does not exist.
        FileHandlerError: If copy operation fails.
    
    Example:
        >>> copied = copy_file("audio.wav", "./backup/audio.wav")
        >>> print(copied)
        PosixPath('backup/audio.wav')
    """
    source_path = validate_file_exists(source)
    dest_path = Path(destination)
    
    try:
        # If destination is a directory, copy file into it
        if dest_path.is_dir():
            dest_path = dest_path / source_path.name
        
        # Ensure parent directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        return dest_path
        
    except Exception as e:
        raise FileHandlerError(
            f"Failed to copy file from '{source}' to '{destination}': {e}"
        ) from e


def move_file(
    source: Union[str, Path],
    destination: Union[str, Path]
) -> Path:
    """
    Move a file from source to destination.
    
    Args:
        source: Path to the source file.
        destination: Path to the destination (file or directory).
    
    Returns:
        Path object for the moved file.
    
    Raises:
        FileNotFoundError: If source file does not exist.
        FileHandlerError: If move operation fails.
    
    Example:
        >>> moved = move_file("audio.wav", "./processed/audio.wav")
        >>> print(moved)
        PosixPath('processed/audio.wav')
    """
    source_path = validate_file_exists(source)
    dest_path = Path(destination)
    
    try:
        # If destination is a directory, move file into it
        if dest_path.is_dir():
            dest_path = dest_path / source_path.name
        
        # Ensure parent directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(source_path), str(dest_path))
        return dest_path
        
    except Exception as e:
        raise FileHandlerError(
            f"Failed to move file from '{source}' to '{destination}': {e}"
        ) from e


def delete_file(file_path: Union[str, Path]) -> None:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file to delete.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        FileHandlerError: If deletion fails.
    
    Example:
        >>> delete_file("temp.wav")
    """
    path = validate_file_exists(file_path)
    
    try:
        path.unlink()
    except Exception as e:
        raise FileHandlerError(
            f"Failed to delete file '{file_path}': {e}"
        ) from e


def clean_directory(
    directory: Union[str, Path],
    pattern: Optional[str] = None
) -> int:
    """
    Delete all files in a directory, optionally matching a pattern.
    
    Args:
        directory: Path to the directory.
        pattern: Optional glob pattern for files to delete.
    
    Returns:
        Number of files deleted.
    
    Raises:
        FileHandlerError: If cleaning fails.
    
    Example:
        >>> count = clean_directory("./temp", "*.wav")
        >>> print(f"Deleted {count} files")
        Deleted 5 files
    """
    try:
        files = list_files_in_directory(directory, pattern, recursive=False)
        deleted_count = 0
        
        for file_path in files:
            file_path.unlink()
            deleted_count += 1
        
        return deleted_count
        
    except Exception as e:
        raise FileHandlerError(
            f"Failed to clean directory '{directory}': {e}"
        ) from e


def format_file_size(size_bytes: int) -> str:
    """
    Format a file size in bytes to a human-readable string.
    
    Args:
        size_bytes: File size in bytes.
    
    Returns:
        Human-readable file size string.
    
    Example:
        >>> size = format_file_size(1048576)
        >>> print(size)
        1.00 MB
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def is_audio_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is an audio file based on its extension.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        True if the file is an audio file, False otherwise.
    
    Example:
        >>> is_audio_file("audio.mp3")
        True
        >>> is_audio_file("video.mp4")
        False
    """
    path = Path(file_path)
    audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma"}
    return path.suffix.lower() in audio_extensions


def is_video_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a video file based on its extension.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        True if the file is a video file, False otherwise.
    
    Example:
        >>> is_video_file("video.mp4")
        True
        >>> is_video_file("audio.mp3")
        False
    """
    path = Path(file_path)
    video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv"}
    return path.suffix.lower() in video_extensions


def is_media_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a media file (audio or video) based on its extension.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        True if the file is a media file, False otherwise.
    
    Example:
        >>> is_media_file("video.mp4")
        True
        >>> is_media_file("audio.mp3")
        True
        >>> is_media_file("document.pdf")
        False
    """
    return is_audio_file(file_path) or is_video_file(file_path)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename: Original filename.
    
    Returns:
        Sanitized filename with invalid characters replaced.
    
    Example:
        >>> sanitize_filename("file/with\"invalid*chars?.txt")
        'file_with_invalid_chars_.txt'
    """
    import re
    # Replace invalid characters with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    return sanitized


def get_unique_filename(file_path: Union[str, Path]) -> Path:
    """
    Get a unique filename by appending a counter if the file already exists.
    
    Args:
        file_path: Original file path.
    
    Returns:
        Path object with a unique filename.
    
    Example:
        >>> get_unique_filename("file.txt")
        Path('file.txt')
        >>> # If file.txt exists, returns Path('file_1.txt')
    """
    path = Path(file_path)
    if not path.exists():
        return path
    
    stem = path.stem
    suffix = path.suffix
    directory = path.parent
    
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = directory / new_name
        if not new_path.exists():
            return new_path
        counter += 1