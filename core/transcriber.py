"""
Transcriber Module

Handles speech-to-text transcription using OpenAI Whisper.
Supports chunking for long audio files (>25 minutes).

This module provides automatic handling of both short and long audio files,
with intelligent chunking for files that exceed the threshold duration.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional
import whisper

from config import get_config
from utils.chunker import (
    should_chunk_audio,
    split_audio_into_chunks,
    concatenate_transcripts,
    AudioChunkerError
)


class TranscriberError(Exception):
    """Custom exception for transcription errors."""
    pass


class AudioFileNotFoundError(TranscriberError):
    """Raised when the audio file is not found."""
    pass


class TranscriptionFailedError(TranscriberError):
    """Raised when transcription fails."""
    pass


def load_whisper_model(model_size: str = "small"):
    """
    Load the Whisper model with the specified size.
    
    Args:
        model_size: Model size (tiny, base, small, medium, large).
    
    Returns:
        Loaded Whisper model.
    
    Raises:
        TranscriberError: If model loading fails.
    """
    try:
        print(f"Loading Whisper model: {model_size}...")
        model = whisper.load_model(model_size)
        print(f"Whisper model loaded successfully: {model_size}")
        return model
    except Exception as e:
        raise TranscriberError(
            f"Failed to load Whisper model '{model_size}': {e}"
        ) from e


def transcribe_audio_segment(
    model,
    audio_path: str,
    language: Optional[str] = None
) -> str:
    """
    Transcribe a single audio segment using Whisper.
    
    Args:
        model: Loaded Whisper model.
        audio_path: Path to the audio file.
        language: Optional language code (e.g., 'en', 'es'). If None, auto-detect.
    
    Returns:
        Transcribed text as a string.
    
    Raises:
        TranscriptionFailedError: If transcription fails.
    """
    try:
        print(f"Transcribing: {Path(audio_path).name}...")
        
        # Transcribe audio
        result = model.transcribe(
            audio_path,
            language=language,
            fp16=False  # Disable FP16 for better compatibility
        )
        
        transcript = result["text"].strip()
        print(f"Transcription complete: {len(transcript)} characters")
        
        return transcript
        
    except Exception as e:
        raise TranscriptionFailedError(
            f"Failed to transcribe audio file '{audio_path}': {e}"
        ) from e


def transcribe_audio(
    audio_path: str,
    model_size: Optional[str] = None,
    language: Optional[str] = None,
    chunk_threshold_minutes: float = 25
) -> str:
    """
    Transcribe an audio file to text using OpenAI Whisper.
    
    This function automatically handles both short and long audio files:
    - Short files (≤25 minutes): Transcribed directly
    - Long files (>25 minutes): Split into chunks and transcribed separately
    
    Args:
        audio_path: Path to the audio file (WAV format recommended).
        model_size: Whisper model size (tiny, base, small, medium, large).
                   If None, uses value from config (default: "small").
        language: Optional language code (e.g., 'en', 'es'). If None, auto-detect.
        chunk_threshold_minutes: Duration threshold in minutes for chunking.
    
    Returns:
        Full transcript as a string.
    
    Raises:
        AudioFileNotFoundError: If the audio file does not exist.
        TranscriberError: If model loading fails.
        TranscriptionFailedError: If transcription fails.
    
    Example:
        >>> transcript = transcribe_audio("audio.wav")
        >>> print(transcript)
        "This is the transcribed text..."
    """
    # Validate audio file exists
    if not os.path.exists(audio_path):
        raise AudioFileNotFoundError(
            f"Audio file not found: {audio_path}"
        )
    
    # Get model size from config if not specified
    if model_size is None:
        config = get_config(use_cloud=False)
        model_size = config.whisper_model_size
    
    # Load Whisper model
    model = load_whisper_model(model_size)
    
    # Check if audio should be chunked
    if should_chunk_audio(audio_path, chunk_threshold_minutes):
        print(f"Audio file exceeds {chunk_threshold_minutes} minutes, using chunked transcription...")
        return transcribe_long_audio(model, audio_path, language)
    else:
        print("Transcribing audio file directly...")
        return transcribe_audio_segment(model, audio_path, language)


def transcribe_long_audio(
    model,
    audio_path: str,
    language: Optional[str] = None,
    chunk_duration: float = 600
) -> str:
    """
    Transcribe a long audio file by splitting it into chunks.
    
    Args:
        model: Loaded Whisper model.
        audio_path: Path to the audio file.
        language: Optional language code.
        chunk_duration: Duration of each chunk in seconds (default: 600 = 10 minutes).
    
    Returns:
        Concatenated transcript as a string.
    
    Raises:
        TranscriptionFailedError: If transcription fails.
    """
    # Create temporary directory for chunks
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Split audio into chunks
            chunk_paths = split_audio_into_chunks(
                audio_path,
                temp_dir,
                chunk_duration
            )
            
            # Transcribe each chunk
            transcripts = []
            for i, chunk_path in enumerate(chunk_paths):
                print(f"\nProcessing chunk {i+1}/{len(chunk_paths)}...")
                transcript = transcribe_audio_segment(model, chunk_path, language)
                transcripts.append(transcript)
            
            # Concatenate transcripts
            print("\nConcatenating transcripts...")
            full_transcript = concatenate_transcripts(transcripts)
            
            print(f"\nTranscription complete: {len(full_transcript)} characters total")
            return full_transcript
            
        except AudioChunkerError as e:
            raise TranscriptionFailedError(
                f"Failed to process long audio: {e}"
            ) from e