# File Scanner Feature Documentation

## Overview

The File Scanner feature provides automated scanning and monitoring capabilities for the Media Knowledge Pipeline. It enables users to automatically detect, categorize, and copy media files from specified directories to the appropriate data directories for processing.

## Features

### 1. Directory Scanning
- **One-time scanning**: Scan a directory for existing media files
- **File type detection**: Automatically detect audio and video files by extension
- **Automatic copying**: Copy files to appropriate data directories
- **Duplicate handling**: Skip files that already exist in destination

### 2. Directory Monitoring (Watch Mode)
- **Continuous monitoring**: Watch directories for new media files
- **Configurable polling**: Adjustable interval for checking new files
- **Real-time processing**: Process files as they appear
- **Auto-processing**: Optionally run full pipeline (transcription + synthesis) on copied files
- **Graceful interruption**: Stop monitoring with Ctrl+C

### 3. File Type Support

**Video Formats**:
- `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, `.wmv`

**Audio Formats**:
- `.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`, `.ogg`, `.wma`

## Architecture

### Core Components

#### FileScanner Class
Located in `core/file_scanner.py`, this is the main class that provides:
- File type detection by extension
- Directory scanning and monitoring
- File copying with error handling
- Statistics tracking

#### CLI Integration
Integrated into `main.py` with three commands:
- `process`: Original single-file processing
- `scan`: One-time directory scanning
- `watch`: Continuous directory monitoring

#### Configuration
Scanner settings are integrated into `config.py` with environment variable support:
- `SCAN_DIRECTORY`: Default directory to scan (default: `~/Downloads`)
- `AUDIO_DIRECTORY`: Audio file destination (default: `data/audio`)
- `VIDEO_DIRECTORY`: Video file destination (default: `data/videos`)
- `WATCH_POLL_INTERVAL`: Poll interval for watch mode (default: `5` seconds)

## Usage Examples

### Basic Scanning
```bash
# Scan default Downloads directory
python main.py scan

# Scan custom directory
python main.py scan --directory /path/to/media

# Scan with custom destinations
python main.py scan --audio-dir /custom/audio --video-dir /custom/video

# Quiet mode (suppress detailed output)
python main.py scan --quiet
```

### Watch Mode
```bash
# Watch default Downloads directory
python main.py watch

# Watch with custom interval
python main.py watch --interval 10

# Watch custom directory
python main.py watch --directory /path/to/watch

# Quiet watch mode
python main.py watch --quiet
```

### Environment Configuration
```bash
# Set custom directories via environment variables
export SCAN_DIRECTORY="/Users/username/Media"
export AUDIO_DIRECTORY="data/processed/audio"
export VIDEO_DIRECTORY="data/processed/video"
export WATCH_POLL_INTERVAL="10"

# Then run normally
python main.py scan
```

## Error Handling

The scanner includes comprehensive error handling:

### File Operations
- **Missing files**: Gracefully handle non-existent files
- **Permission errors**: Report permission issues clearly
- **Copy failures**: Handle disk space and I/O errors- **Zero-byte files**: Skip files with 0 bytes (incomplete downloads)
- **Partial downloads**: Skip files with `.part`, `.tmp` extensions
### Directory Operations
- **Missing directories**: Warn about non-existent scan directories
- **Invalid paths**: Handle file paths that aren't directories
- **Permission issues**: Report directory access problems

### Watch Mode
- **Interrupt handling**: Clean shutdown on Ctrl+C
- **Network drives**: Handle temporary disconnections
- **File system events**: Robust handling of file system changes

## Testing

Comprehensive unit tests are available in `tests/test_file_scanner.py`:

```bash
# Run all scanner tests
python -m pytest tests/test_file_scanner.py -v

# Run specific test categories
python -m pytest tests/test_file_scanner.py::TestFileScanner -v
python -m pytest tests/test_file_scanner.py::TestIntegration -v
```

## Integration with Existing Pipeline

The file scanner integrates seamlessly with the existing Media Knowledge Pipeline:

1. **Files are copied** to the standard data directories (`data/audio/` and `data/videos/`)
2. **Existing processing workflow** remains unchanged
3. **Configuration system** is extended to support scanner settings
4. **Error handling patterns** follow existing conventions

## Platform Compatibility

- **macOS**: Fully supported (primary development platform)
- **Linux**: Fully supported
- **Windows**: Supported with proper path handling

## Performance Considerations

### Scanning Performance
- **Lightweight**: Minimal resource usage during scanning
- **Efficient**: Only processes media files, ignores others
- **Fast**: Quick file type detection by extension

### Watch Mode Performance
- **Configurable polling**: Adjust interval based on needs
- **Low overhead**: Minimal impact on system performance
- **Smart tracking**: Only processes new files

## Security Considerations

- **File permissions**: Respects existing file permissions
- **Path validation**: Validates all file paths before operations
- **No automatic deletion**: Only copies files, never deletes originals
- **Safe defaults**: Conservative default settings

## Troubleshooting

### Common Issues

**Files not being detected:**
- Check file extensions match supported formats
- Verify scan directory exists and is accessible
- Check file permissions

**Watch mode not detecting new files:**
- Ensure poll interval is appropriate for your use case
- Check if files are being created with correct extensions
- Verify directory permissions

**Permission errors:**
- Ensure write access to destination directories
- Check read access to scan directory
- Verify file ownership and permissions

### Debug Mode

Enable verbose logging by modifying the scanner's log level:

```python
import logging
logging.getLogger("file_scanner").setLevel(logging.DEBUG)
```

## Future Enhancements

Potential improvements for future versions:

1. **MIME type detection**: More accurate file type detection
2. **File system events**: Use native file system monitoring instead of polling
3. **Batch processing**: Process multiple files in parallel
4. **Custom file types**: Support for additional media formats
5. **Cloud integration**: Direct integration with cloud storage
6. **Web interface**: GUI for monitoring and configuration

## API Reference

### FileScanner Class

```python
class FileScanner:
    def __init__(scan_directory="~/Downloads", audio_directory="data/audio", 
                 video_directory="data/videos", supported_extensions=None, 
                 logger=None)
    
    def scan_directory_for_media() -> List[ScanResult]
    def watch_directory(callback=None, poll_interval=5) -> None
    def get_statistics() -> Dict[str, int]
```

### ScanResult Dataclass

```python
@dataclass
class ScanResult:
    file_path: Path
    file_type: str  # "audio" or "video"
    destination: Path
    status: str  # "copied", "skipped", "error"
    error_message: Optional[str] = None
    file_size: int = 0
```

## Output Management

### Directory Structure

The file scanner and pipeline use a consolidated output structure:

```
media-knowledge-pipeline/
├── outputs/                    # Consolidated output directory
│   ├── {filename}_results.json  # JSON processing results
│   └── markdown/               # Markdown output directory
│       └── {filename}.md       # Generated markdown files
├── data/                       # Input media storage
│   ├── audio/                  # Audio files for processing
│   └── videos/                 # Video files for processing
└── ...
```

### File Organization

- **JSON outputs**: Saved to `outputs/{filename}_results.json`
- **Markdown outputs**: Saved to `outputs/markdown/{filename}.md`
- **Media files**: Copied to `data/audio/` and `data/videos/`
- **Consolidated structure**: All outputs stored in root `outputs/` directory

### Auto-processing Outputs

When using the `--process` flag with scan or watch commands, the pipeline automatically:
1. Copies media files to appropriate data directories
2. Processes files through transcription and synthesis pipeline
3. Saves both JSON and Markdown outputs to the consolidated `outputs/` directory