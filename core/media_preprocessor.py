"""
Media Preprocessor Module

Handles detection and preparation of video/audio files for transcription.
Extracts audio from video files and converts audio formats as needed.

Supported formats:
- Video: .mp4, .mov, .avi, .mkv, .webm, .flv, .wmv
- Audio: .mp3, .wav, .m4a, .flac, .aac, .ogg, .wma
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple
import filetype


class MediaPreprocessorError(Exception):
    """Custom exception for media preprocessing errors."""
    pass


class UnsupportedMediaTypeError(MediaPreprocessorError):
    """Raised when the media type is not supported."""
    pass


class FFmpegNotFoundError(MediaPreprocessorError):
    """Raised when ffmpeg is not available."""
    pass


def check_ffmpeg_available() -> bool:
    """
    Check if ffmpeg is available on the system.
    
    Returns:
        True if ffmpeg is available, False otherwise.
    """
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def detect_media_type(file_path: str) -> Tuple[str, str]:
    """
    Detect the type of media file (video or audio).
    
    Args:
        file_path: Path to the media file.
    
    Returns:
        Tuple of (media_type, mime_type) where media_type is 'video' or 'audio'.
    
    Raises:
        UnsupportedMediaTypeError: If the file type is not supported.
    """
    kind = filetype.guess(file_path)
    
    if kind is None:
        # Fallback to extension-based detection
        ext = Path(file_path).suffix.lower()
        video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv'}
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
        
        if ext in video_extensions:
            return 'video', f'video/{ext[1:]}'
        elif ext in audio_extensions:
            return 'audio', f'audio/{ext[1:]}'
        else:
            raise UnsupportedMediaTypeError(
                f"Unsupported file extension: {ext}. "
                f"Supported video formats: {', '.join(video_extensions)}. "
                f"Supported audio formats: {', '.join(audio_extensions)}."
            )
    
    mime_type = kind.mime
    if mime_type.startswith('video/'):
        return 'video', mime_type
    elif mime_type.startswith('audio/'):
        return 'audio', mime_type
    else:
        raise UnsupportedMediaTypeError(
            f"Unsupported MIME type: {mime_type}. "
            "Only video and audio files are supported."
        )


def extract_audio_from_video(video_path: str, output_dir: str) -> str:
    """
    Extract audio track from a video file using ffmpeg.
    
    Args:
        video_path: Path to the video file.
        output_dir: Directory to save the extracted audio.
    
    Returns:
        Path to the extracted .wav file.
    
    Raises:
        FFmpegNotFoundError: If ffmpeg is not available.
        MediaPreprocessorError: If extraction fails.
    """
    if not check_ffmpeg_available():
        raise FFmpegNotFoundError(
            "ffmpeg is not installed or not available in PATH. "
            "Install it using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        )
    
    # Generate output filename
    video_name = Path(video_path).stem
    output_path = Path(output_dir) / f"{video_name}_extracted.wav"
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Use ffmpeg to extract audio
        # -i: input file
        # -vn: no video
        # -acodec pcm_s16le: 16-bit PCM audio codec (WAV compatible)
        # -ar 16000: sample rate 16kHz (good for Whisper)
        # -ac 1: mono channel
        # -y: overwrite output file if exists
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            str(output_path)
        ]
        
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return str(output_path)
        
    except subprocess.CalledProcessError as e:
        raise MediaPreprocessorError(
            f"Failed to extract audio from video: {e.stderr}"
        ) from e


def convert_audio_to_wav(audio_path: str, output_dir: str) -> str:
    """
    Convert audio file to WAV format using ffmpeg.
    
    Args:
        audio_path: Path to the audio file.
        output_dir: Directory to save the converted audio.
    
    Returns:
        Path to the converted .wav file.
    
    Raises:
        FFmpegNotFoundError: If ffmpeg is not available.
        MediaPreprocessorError: If conversion fails.
    """
    if not check_ffmpeg_available():
        raise FFmpegNotFoundError(
            "ffmpeg is not installed or not available in PATH. "
            "Install it using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        )
    
    # Generate output filename
    audio_name = Path(audio_path).stem
    output_path = Path(output_dir) / f"{audio_name}_converted.wav"
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Use ffmpeg to convert to WAV
        # -i: input file
        # -acodec pcm_s16le: 16-bit PCM audio codec (WAV compatible)
        # -ar 16000: sample rate 16kHz (good for Whisper)
        # -ac 1: mono channel
        # -y: overwrite output file if exists
        cmd = [
            "ffmpeg",
            "-i", audio_path,
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            str(output_path)
        ]
        
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return str(output_path)
        
    except subprocess.CalledProcessError as e:
        raise MediaPreprocessorError(
            f"Failed to convert audio to WAV: {e.stderr}"
        ) from e


def copy_wav_file(wav_path: str, output_dir: str) -> str:
    """
    Copy a WAV file to the output directory.
    
    Args:
        wav_path: Path to the WAV file.
        output_dir: Directory to copy the file to.
    
    Returns:
        Path to the copied .wav file.
    
    Raises:
        MediaPreprocessorError: If copy fails.
    """
    try:
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        wav_name = Path(wav_path).name
        output_path = Path(output_dir) / wav_name
        
        # Copy file
        shutil.copy2(wav_path, output_path)
        
        return str(output_path)
        
    except Exception as e:
        raise MediaPreprocessorError(
            f"Failed to copy WAV file: {e}"
        ) from e


def prepare_audio(input_media_path: str, output_dir: str) -> str:
    """
    Prepare audio from a video or audio file for transcription.
    
    This function detects the input file type and processes it accordingly:
    - Video files: Extract audio track to WAV format
    - Audio files: Convert to WAV if needed, or copy if already WAV
    
    Args:
        input_media_path: Path to the input video or audio file.
        output_dir: Directory to save the prepared audio file.
    
    Returns:
        Path to the prepared .wav audio file ready for transcription.
    
    Raises:
        FileNotFoundError: If the input file does not exist.
        UnsupportedMediaTypeError: If the file type is not supported.
        FFmpegNotFoundError: If ffmpeg is not available.
        MediaPreprocessorError: If processing fails.
    
    Example:
        >>> audio_path = prepare_audio("video.mp4", "./output")
        >>> print(audio_path)
        ./output/video_extracted.wav
    """
    # Validate input file exists
    if not os.path.exists(input_media_path):
        raise FileNotFoundError(
            f"Input file not found: {input_media_path}"
        )
    
    # Detect media type
    media_type, mime_type = detect_media_type(input_media_path)
    print(f"Detected media type: {media_type} ({mime_type})")
    
    # Process based on media type
    if media_type == 'video':
        print("Extracting audio from video file...")
        output_path = extract_audio_from_video(input_media_path, output_dir)
    elif media_type == 'audio':
        # Check if already WAV
        if input_media_path.lower().endswith('.wav'):
            print("Audio file is already in WAV format, copying...")
            output_path = copy_wav_file(input_media_path, output_dir)
        else:
            print(f"Converting audio file to WAV format...")
            output_path = convert_audio_to_wav(input_media_path, output_dir)
    else:
        raise UnsupportedMediaTypeError(
            f"Unsupported media type: {media_type}"
        )
    
    print(f"Audio prepared successfully: {output_path}")
    return output_path