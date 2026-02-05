"""
Chunker Utility Module

Provides audio file chunking logic for processing long files.
Handles segment processing and result concatenation.

This module is used to split long audio files into smaller segments
that can be processed more efficiently by Whisper, avoiding memory
issues and timeout errors with very long recordings.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple


class AudioChunkerError(Exception):
    """Custom exception for audio chunking errors."""
    pass


def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file in seconds using ffprobe.
    
    Args:
        audio_path: Path to the audio file.
    
    Returns:
        Duration in seconds.
    
    Raises:
        AudioChunkerError: If ffprobe is not available or fails.
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        duration = float(result.stdout.strip())
        return duration
        
    except subprocess.CalledProcessError as e:
        raise AudioChunkerError(
            f"Failed to get audio duration: {e.stderr}"
        ) from e
    except ValueError as e:
        raise AudioChunkerError(
            f"Invalid duration value: {e}"
        ) from e


def calculate_chunk_count(duration: float, chunk_duration: float = 600) -> int:
    """
    Calculate the number of chunks needed for an audio file.
    
    Args:
        duration: Total duration in seconds.
        chunk_duration: Duration of each chunk in seconds (default: 600 = 10 minutes).
    
    Returns:
        Number of chunks needed.
    """
    return int((duration + chunk_duration - 1) // chunk_duration)


def split_audio_into_chunks(
    audio_path: str,
    output_dir: str,
    chunk_duration: float = 600
) -> List[str]:
    """
    Split an audio file into multiple chunks using ffmpeg.
    
    Args:
        audio_path: Path to the input audio file.
        output_dir: Directory to save the chunk files.
        chunk_duration: Duration of each chunk in seconds (default: 600 = 10 minutes).
    
    Returns:
        List of paths to the chunk files in order.
    
    Raises:
        AudioChunkerError: If splitting fails.
    """
    try:
        # Get audio duration
        duration = get_audio_duration(audio_path)
        num_chunks = calculate_chunk_count(duration, chunk_duration)
        
        print(f"Audio duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
        print(f"Splitting into {num_chunks} chunks of {chunk_duration/60:.1f} minutes each...")
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate output filename base
        audio_name = Path(audio_path).stem
        chunk_paths = []
        
        # Split audio into chunks
        for i in range(num_chunks):
            start_time = i * chunk_duration
            output_path = Path(output_dir) / f"{audio_name}_chunk_{i:03d}.wav"
            
            # Use ffmpeg to extract chunk
            # -ss: start time
            # -t: duration
            # -c copy: copy codec without re-encoding (faster)
            cmd = [
                "ffmpeg",
                "-ss", str(start_time),
                "-t", str(chunk_duration),
                "-i", audio_path,
                "-c", "copy",
                "-y",
                str(output_path)
            ]
            
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            chunk_paths.append(str(output_path))
            print(f"Created chunk {i+1}/{num_chunks}: {output_path.name}")
        
        return chunk_paths
        
    except subprocess.CalledProcessError as e:
        raise AudioChunkerError(
            f"Failed to split audio into chunks: {e.stderr}"
        ) from e


def concatenate_transcripts(transcripts: List[str]) -> str:
    """
    Concatenate multiple transcript segments into a single transcript.
    
    Args:
        transcripts: List of transcript segments in order.
    
    Returns:
        Concatenated transcript as a single string.
    """
    # Join transcripts with appropriate spacing
    # Add a space between segments if they don't already end with punctuation
    result = []
    for i, transcript in enumerate(transcripts):
        if i > 0 and result and not result[-1].strip().endswith(('.', '!', '?', '\n')):
            result.append(' ')
        result.append(transcript)
    
    return ''.join(result)


def should_chunk_audio(audio_path: str, threshold_minutes: float = 25) -> bool:
    """
    Determine if an audio file should be chunked based on its duration.
    
    Args:
        audio_path: Path to the audio file.
        threshold_minutes: Duration threshold in minutes (default: 25).
    
    Returns:
        True if the audio should be chunked, False otherwise.
    """
    try:
        duration = get_audio_duration(audio_path)
        duration_minutes = duration / 60
        return duration_minutes > threshold_minutes
    except AudioChunkerError:
        # If we can't get duration, assume it's short enough
        return False