"""
Media Preprocessor Module

Handles detection and preparation of video/audio files for transcription.
Extracts audio from video files and converts audio formats as needed.
Also supports streaming YouTube videos directly for processing.

Supported formats:
- Video: .mp4, .mov, .avi, .mkv, .webm, .flv, .wmv
- Audio: .mp3, .wav, .m4a, .flac, .aac, .ogg, .wma
- YouTube: Direct streaming from YouTube URLs
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional, Union
import filetype

# Import yt-dlp for YouTube streaming support
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class MediaPreprocessorError(Exception):
    """Custom exception for media preprocessing errors."""
    pass


class YouTubeStreamingError(MediaPreprocessorError):
    """Raised when YouTube streaming fails."""
    pass


class UnsupportedMediaTypeError(MediaPreprocessorError):
    """Raised when the media type is not supported."""
    pass


class FFmpegNotFoundError(MediaPreprocessorError):
    """Raised when ffmpeg is not available."""
    pass


def is_youtube_url(url: str) -> bool:
    """
    Check if a URL is a YouTube URL.
    
    Args:
        url: The URL to check.
        
    Returns:
        True if the URL is a YouTube URL, False otherwise.
    """
    if not isinstance(url, str):
        return False
    
    youtube_domains = [
        'youtube.com',
        'youtu.be',
        'youtube-nocookie.com'
    ]
    
    return any(domain in url.lower() for domain in youtube_domains)


def is_youtube_playlist_url(url: str) -> bool:
    """
    Check if a YouTube URL is a playlist URL.
    
    Args:
        url: The YouTube URL to check.
        
    Returns:
        True if the URL is a YouTube playlist URL, False otherwise.
    """
    if not is_youtube_url(url):
        return False
    
    # Check for playlist parameter in URL
    return 'list=' in url.lower() or '/playlist' in url.lower()


def extract_youtube_playlist_videos(playlist_url: str) -> List[str]:
    """
    Extract video URLs from a YouTube playlist.
    
    Args:
        playlist_url: YouTube playlist URL.
        
    Returns:
        List of individual video URLs from the playlist.
        
    Raises:
        YouTubeStreamingError: If playlist extraction fails.
    """
    if not YT_DLP_AVAILABLE:
        raise YouTubeStreamingError(
            "yt-dlp is not installed. Install it using: pip install yt-dlp"
        )
    
    if not is_youtube_playlist_url(playlist_url):
        raise YouTubeStreamingError(f"Not a valid YouTube playlist URL: {playlist_url}")
    
    try:
        ydl_opts: Dict[str, Any] = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Only extract metadata, don't download
            'playliststart': 1,    # Start from first video
            'playlistend': None,   # No limit (process all videos)
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            info = ydl.extract_info(playlist_url, download=False)  # type: ignore
            
        if info.get('_type') != 'playlist':
            raise YouTubeStreamingError(f"URL is not a playlist: {playlist_url}")
        
        entries = info.get('entries')
        if not entries:
            raise YouTubeStreamingError(f"Playlist contains no videos: {playlist_url}")
        
        # Extract individual video URLs
        video_urls: List[str] = []
        for entry in entries:  # type: ignore
            if entry.get('url'):
                video_urls.append(entry['url'])  # type: ignore
            elif entry.get('id'):
                # Fallback: construct URL from video ID
                video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")  # type: ignore
        
        print(f"Extracted {len(video_urls)} videos from playlist: {info.get('title', 'Unknown')}")
        return video_urls
            
    except Exception as e:
        raise YouTubeStreamingError(f"Failed to extract playlist videos: {str(e)}")


def stream_youtube_playlist_audio(playlist_url: str, output_dir: str) -> List[str]:
    """
    Process all videos in a YouTube playlist and return list of audio files.
    
    Args:
        playlist_url: YouTube playlist URL.
        output_dir: Directory to save the extracted audio files.
        
    Returns:
        List of paths to the extracted .wav files.
        
    Raises:
        YouTubeStreamingError: If playlist processing fails.
    """
    # First extract video URLs from playlist
    video_urls = extract_youtube_playlist_videos(playlist_url)
    
    # Process each video individually
    audio_files: List[str] = []
    for i, video_url in enumerate(video_urls, 1):
        print(f"Processing playlist video {i}/{len(video_urls)}: {video_url}")
        try:
            audio_file = stream_youtube_audio(video_url, output_dir)
            audio_files.append(audio_file)
        except Exception as e:
            print(f"Warning: Failed to process video {i}: {video_url} - {e}")
            continue
    
    if not audio_files:
        raise YouTubeStreamingError(f"No videos were successfully processed from playlist: {playlist_url}")
    
    print(f"Successfully processed {len(audio_files)} videos from playlist")
    return audio_files


def stream_youtube_audio(youtube_url: str, output_dir: str) -> str:
    """
    Stream YouTube video audio directly to a WAV file for transcription.
    
    This function uses yt-dlp to extract the audio stream from a YouTube video
    and pipes it directly to ffmpeg for conversion to WAV format, avoiding
    the need to download the full video file.
    
    Args:
        youtube_url: YouTube video URL.
        output_dir: Directory to save the extracted audio file.
        
    Returns:
        Path to the extracted .wav file.
        
    Raises:
        YouTubeStreamingError: If streaming fails.
        FFmpegNotFoundError: If ffmpeg is not available.
    """
    if not YT_DLP_AVAILABLE:
        raise YouTubeStreamingError(
            "yt-dlp is not installed. Install it using: pip install yt-dlp"
        )
    
    if not check_ffmpeg_available():
        raise FFmpegNotFoundError(
            "ffmpeg is not installed or not available in PATH. "
            "Install it using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        )
    
    # Validate YouTube URL
    if not is_youtube_url(youtube_url):
        raise YouTubeStreamingError(f"Invalid YouTube URL: {youtube_url}")
    
    print(f"Streaming audio from YouTube URL: {youtube_url}")
    
    try:
        # Use yt-dlp to extract video info and get direct audio stream URL
        ydl_opts: Dict[str, Any] = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            info = ydl.extract_info(youtube_url, download=False)  # type: ignore
            video_title_raw = info.get('title', 'youtube_video')
            video_title = str(video_title_raw).replace('/', '_').replace('\\', '_') if video_title_raw else 'youtube_video'
            direct_url = info.get('url')  # Get the direct stream URL
            print(f"Video title: {video_title}")
            
            if not direct_url:
                raise YouTubeStreamingError("Could not extract direct audio stream URL")
    
        # Generate output filename based on video title
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
        output_path = Path(output_dir) / f"{safe_title}_youtube.wav"
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Stream directly from YouTube to WAV using ffmpeg
        # Use the direct URL that yt-dlp provided
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", direct_url,   # Input from direct stream URL
            "-vn",              # No video
            "-acodec", "pcm_s16le",  # WAV codec
            "-ar", "16000",     # 16kHz sample rate (good for Whisper)
            "-ac", "1",         # Mono
            "-y",               # Overwrite output file
            str(output_path)
        ]
        
        print("Streaming and converting audio...")
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise YouTubeStreamingError(
                f"Failed to stream YouTube audio: {result.stderr}"
            )
        
        if not output_path.exists():
            raise YouTubeStreamingError(
                "Failed to create output file - streaming may have failed"
            )
        
        print(f"Audio streamed successfully: {output_path}")
        return str(output_path)
        
    except Exception as e:
        raise YouTubeStreamingError(f"YouTube streaming failed: {str(e)}")


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


def prepare_audio(input_media_path: str, output_dir: str) -> Union[str, List[str]]:
    """
    Prepare audio from a video or audio file for transcription.
    
    This function detects the input file type and processes it accordingly:
    - Video files: Extract audio track to WAV format
    - Audio files: Convert to WAV if needed, or copy if already WAV
    - YouTube URLs: Stream audio directly from YouTube
    - YouTube Playlists: Stream audio from all videos in playlist
    
    Args:
        input_media_path: Path to the input video or audio file, or YouTube URL.
        output_dir: Directory to save the prepared audio file(s).
        
    Returns:
        Path to the prepared .wav audio file ready for transcription.
        For playlists, returns a list of paths.
        
    Raises:
        FileNotFoundError: If the input file does not exist.
        UnsupportedMediaTypeError: If the file type is not supported.
        FFmpegNotFoundError: If ffmpeg is not available.
        MediaPreprocessorError: If processing fails.
        YouTubeStreamingError: If YouTube streaming fails.
        
    Example:
        >>> audio_path = prepare_audio("video.mp4", "./output")
        >>> print(audio_path)
        ./output/video_extracted.wav
        
        >>> audio_path = prepare_audio("https://youtube.com/watch?v=...", "./output")
        >>> print(audio_path)
        ./output/video_title_youtube.wav
        
        >>> audio_paths = prepare_audio("https://youtube.com/playlist?list=...", "./output")
        >>> print(audio_paths)
        ['./output/video1_youtube.wav', './output/video2_youtube.wav', ...]
    """
    # Handle YouTube URLs specially
    if is_youtube_url(input_media_path):
        if not YT_DLP_AVAILABLE:
            raise YouTubeStreamingError(
                "yt-dlp is required for YouTube streaming. Install with: pip install yt-dlp"
            )
        
        # Check if it's a playlist
        if is_youtube_playlist_url(input_media_path):
            print("Detected YouTube playlist, streaming audio from all videos...")
            return stream_youtube_playlist_audio(input_media_path, output_dir)
        else:
            print("Detected YouTube URL, streaming audio directly...")
            return stream_youtube_audio(input_media_path, output_dir)
    
    # Validate input file exists (for local files)
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
            f"Unsupported media type: {media_type} ({mime_type})"
        )
    
    print("Audio prepared successfully:", output_path)
    return output_path