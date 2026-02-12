"""
Input validation utilities for Media Knowledge Pipeline CLI Wizard System
"""

import re
from pathlib import Path
from typing import Union

def validate_youtube_url(url: str) -> bool:
    """
    Validate YouTube URL format.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid YouTube URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    # Regular expression for YouTube URLs
    youtube_regex = (
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/)|'
        r'youtu\.be/)([a-zA-Z0-9_-]{11})'
    )
    
    return bool(re.match(youtube_regex, url))

def validate_file_path(file_path: str) -> bool:
    """
    Validate that a file path exists and is a file (not directory).
    
    Args:
        file_path (str): File path to validate
        
    Returns:
        bool: True if file exists and is a file, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    try:
        path_obj = Path(file_path)
        return path_obj.exists() and path_obj.is_file()
    except Exception:
        return False

def validate_number_range(value: Union[str, int], min_val: int, max_val: int) -> bool:
    """
    Validate that a number is within a specified range.
    
    Args:
        value (Union[str, int]): Number to validate
        min_val (int): Minimum allowed value
        max_val (int): Maximum allowed value
        
    Returns:
        bool: True if number is within range, False otherwise
    """
    try:
        num = int(value)
        return min_val <= num <= max_val
    except (ValueError, TypeError):
        return False

def validate_file_format(file_path: str, allowed_extensions: list) -> bool:
    """
    Validate that a file has an allowed extension.
    
    Args:
        file_path (str): File path to validate
        allowed_extensions (list): List of allowed extensions (e.g., ['.pdf', '.epub'])
        
    Returns:
        bool: True if file has allowed extension, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    try:
        path_obj = Path(file_path)
        return path_obj.suffix.lower() in allowed_extensions
    except Exception:
        return False

# Additional validators can be added here as needed