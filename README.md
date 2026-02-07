# Media-to-Knowledge Pipeline

**Version: 2.2.0**

A modular Python application that processes video and audio files through transcription and knowledge synthesis using local or cloud Ollama models. Extract actionable insights, summaries, and structured knowledge from your media content.

## 📋 Changelog

### v2.3.0 (February 7, 2026)
- **Token-Based Model Selection**: Intelligent model switching based on content volume to prevent context overflow
- **Intelligent Folder Organization**: Ordered folder structure for playlists and URL lists with systematic naming
- **Essay Synthesis Notifications**: Real-time feedback during essay generation with token count information
- **Create Essays from Existing Docs**: New CLI command to generate essays from previously processed synthesis files
- **Enhanced Error Handling**: Better management of large content with graceful degradation suggestions

### v2.2.0 (February 7, 2026)
- **Enhanced Python CLI**: Replaced bash script wrapper with modern Python CLI using Typer and Rich
- **Improved User Experience**: Enhanced feedback with colorful output, progress indicators, and real-time status updates
- **Better Error Handling**: Clear error messages and graceful failure recovery
- **Cross-Platform Compatibility**: Consistent interface across all operating systems
- **Extensible Architecture**: Modular design for easy feature additions

### v2.1.0 (February 6, 2026)
- **Progress Tracking**: Added visual progress indicators and percentage tracking for batch processing
- **Enhanced Feedback**: Real-time status updates showing current processing phase and ETA
- **Improved User Experience**: Better visibility into processing pipeline with detailed progress information

### v2.0.0 (February 6, 2026)
- **Multi-Source Essay Synthesis**: Generate comprehensive essays from multiple YouTube videos or playlists with content cohesion checking
- **Batch Processing Enhancements**: Added `--essay` and `--force-essay` flags to batch command for automatic essay generation
- **Content Cohesion Assessment**: Smart evaluation to prevent meaningless synthesis by checking thematic connections between sources
- **Graceful Degradation**: Automatically retains individual synthesized knowledge when essay synthesis is not appropriate
- **New Prompt Templates**: Added synthesis_essay and content_cohesion_check templates for advanced knowledge synthesis

### v1.1.0 (February 5, 2026)
- **Test Suite Improvements**: Fixed 29 failing tests, improved coverage from 82% to 99.6%
- **File Scanner Feature**: Added automated file scanning and monitoring capabilities
- **Enhanced Error Handling**: Improved exception handling and error messages
- **Code Quality**: Fixed function parameter mismatches and added missing exception classes
- **Documentation**: Added comprehensive file scanner documentation
- **Performance**: Optimized test execution and mocking

## 🎯 Capabilities

- **Multi-format Support**: Process video (MP4, MOV, AVI) and audio (MP3, WAV, M4A, FLAC) files
- **Automatic Transcription**: Convert speech to text using OpenAI Whisper
- **Knowledge Synthesis**: Extract insights using Ollama models (local or cloud)
- **12 Built-in Prompt Templates**: Meeting minutes, lecture summaries, project updates, and more
- **Custom Prompts**: Use your own synthesis prompts
- **Long File Support**: Automatic chunking for files >25 minutes
- **Flexible Deployment**: Run entirely locally or use cloud Ollama services
- **Structured Output**: Save results as JSON for further processing
- **Markdown Export**: Automatically save synthesized knowledge as markdown files with descriptive filenames
- **User-Friendly CLI**: Modern command-line interface with colorful output and progress indicators
- **YouTube Playlist Support**: Process entire YouTube playlists automatically
- **Multi-Source Essay Synthesis**: Generate comprehensive essays from multiple videos with content cohesion checking
- **Progress Tracking**: Visual progress indicators and percentage tracking during batch processing
- **Enhanced CLI**: Rich terminal interface with autocomplete and detailed help system

## 📋 Project Structure

```
media_knowledge_pipeline/
├── main.py                 # Main orchestration script with CLI
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── VERSION                # Current version number
├── outputs/               # Generated outputs (JSON and Markdown)
│   └── markdown/          # Knowledge synthesis in markdown format
├── data/                  # Media file storage
│   ├── audio/             # Audio files destination
│   └── videos/            # Video files destination
├── core/                  # Core pipeline modules
│   ├── __init__.py
│   ├── media_preprocessor.py  # Video/audio detection and preparation
│   ├── transcriber.py          # Whisper-based transcription
│   ├── synthesizer.py          # Ollama knowledge synthesis
│   ├── prompts.py              # Reusable prompt templates
│   └── file_scanner.py         # Automated file scanning and monitoring
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── file_handler.py         # File validation and operations
│   ├── chunker.py              # Audio chunking for long files
│   ├── token_counter.py        # Token counting for model selection
│   ├── folder_organizer.py     # Intelligent folder organization
│   └── essay_from_existing.py  # Essay generation from existing docs
└── src/                   # Enhanced CLI package
    └── media_knowledge/        # Python CLI modules
        ├── __init__.py
        └── cli/               # CLI command structure
            ├── __init__.py
            ├── app.py         # Main CLI application
            └── commands/      # Individual CLI commands
                ├── __init__.py
                ├── process.py
                ├── batch.py
                ├── playlist.py
                ├── scan.py
                ├── watch.py
                └── create_essay.py  # Create essays from existing docs
```

## 🚀 Installation

### Prerequisites
- **Python 3.9 or higher**
- **Homebrew** (for macOS users)
- **Ollama** (for local processing) - [Install Ollama](https://ollama.ai/download)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install ffmpeg (macOS)

ffmpeg is required for audio/video processing:

```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Step 3: Install Ollama (for Local Processing)

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., llama3.1:8b)
ollama pull llama3.1:8b
```

### Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

### Step 5: Verify Installation

```bash
# Check Python version
python --version

# Check ffmpeg
ffmpeg -version

# Check Ollama (if using local)
ollama list
```

## 💻 Usage

### Modern Python CLI (Recommended)

The enhanced Python CLI provides a rich terminal experience with colorful output, progress indicators, and comprehensive help:

```bash
# Show available commands
media-knowledge --help

# Show system status
media-knowledge status

# Process a single YouTube video or local file
media-knowledge process media --input "https://youtube.com/watch?v=..."

# Process multiple YouTube URLs from a file
media-knowledge batch process-urls --urls youtube_urls.txt

# Process YouTube playlist with organized output
media-knowledge playlist process-playlist "https://youtube.com/playlist?list=..."

# Scan directory for media files
media-knowledge scan directory --directory ~/Downloads

# Watch directory for new media files
media-knowledge watch directory --directory ~/Downloads --process

# Create essay from existing synthesized documents
media-knowledge create-essay --directory outputs --pattern "*.json"
```

### Enhanced Capabilities

#### Token-Based Model Selection
The system automatically selects appropriate models based on content volume:
- **≤ 8K tokens**: Local llama3.1:8b model
- **8K-12K tokens**: Cloud mistral:7b model  
- **12K-32K tokens**: Cloud llama3.1:70b model
- **32K-65K tokens**: Cloud deepseek-v3.1:671b model
- **> 65K tokens**: Content too large, manual batching recommended

#### Intelligent Folder Organization
All outputs are organized in logical folder structures:
```
outputs/
├── playlist_AI_Learning_Series/
│   ├── 001_Introduction_to_AI/
│   │   ├── video.mp4
│   │   ├── transcript.json
│   │   └── synthesis.md
│   └── 002_Machine_Learning_Basics/
│       ├── video.mp4
│       ├── transcript.json
│       └── synthesis.md
├── batch_20260207_153045/
│   ├── 001_First_Video_Title/
│   │   ├── video.mp4
│   │   ├── transcript.json
│   │   └── synthesis.md
│   └── comprehensive_analysis_3_sources_20260207_153045.md
└── comprehensive_analysis_from_existing_docs.md
```

#### Essay Synthesis Notifications
Real-time feedback during essay generation:
```
✓ Batch processing complete: 8/8 videos processed successfully
→ Aggregating content: 18.4K tokens detected
→ Using model: llama3.1:70b for optimal processing
→ Synthesizing comprehensive essay from aggregated content...
✓ Essay synthesis complete: 2,847 words
```

### CLI Commands

#### Process Single Media
```bash
# Process a video file with default settings
media-knowledge process media --input /path/to/video.mp4

# Process with cloud Ollama
media-knowledge process media --input /path/to/audio.mp3 --cloud

# Use a specific prompt template
media-knowledge process media --input meeting.mp4 --prompt meeting_minutes

# Save results to file
media-knowledge process media --input lecture.mp4 --output results.json

# Save synthesis to markdown
media-knowledge process media --input lecture.mp4 --markdown outputs/markdown

# Combine multiple options
media-knowledge process media \
  --input "https://www.youtube.com/watch?v=..." \
  --prompt meeting_minutes \
  --output meeting_summary.json \
  --markdown outputs/markdown \
  --cloud
```

#### Batch Processing
```bash
# Process multiple YouTube URLs
media-knowledge batch process-urls --urls youtube_urls.txt

# Parallel processing with essay synthesis
media-knowledge batch process-urls --urls youtube_urls.txt --parallel 3 --essay

# Custom output and markdown directory
media-knowledge batch process-urls \
  --urls urls.txt \
  --output-dir results \
  --markdown outputs/markdown \
  --quiet
```

#### Playlist Processing
```bash
# Process a YouTube playlist
media-knowledge playlist process-playlist "https://youtube.com/playlist?list=..."

# Playlist with custom folder name
media-knowledge playlist process-playlist \
  "https://youtube.com/playlist?list=..." \
  --folder-name "AI_Learning_Series"
```

#### Directory Scanning
```bash
# Scan Downloads directory
media-knowledge scan directory

# Scan custom directory
media-knowledge scan directory --directory /path/to/media

# Auto-process copied files
media-knowledge scan directory --directory ~/Downloads --process

# Dry run to see what would happen
media-knowledge scan directory --directory ~/Downloads --dry-run
```

#### Directory Watching
```bash
# Watch Downloads directory
media-knowledge watch directory

# Watch with custom poll interval
media-knowledge watch directory --interval 10

# Auto-process new files
media-knowledge watch directory --directory ~/Downloads --process
```

### CLI Features

- **Colorful Output**: Red errors, green successes, blue information
- **Progress Indicators**: Real-time progress bars and spinners
- **Autocomplete**: Tab completion for commands and options
- **Help System**: Context-sensitive help for all commands
- **Rich Formatting**: Tables, lists, and formatted output
- **Verbose Logging**: Detailed operation information when needed

### Legacy CLI Compatibility

The original CLI interface still works for backward compatibility:

```bash
# Original interface still supported
python main.py --input video.mp4
python main.py batch --urls youtube_urls.txt
python main.py scan
python main.py watch
```

## 🚀 Simplified CLI Wrapper

The CLI wrapper provides user-friendly aliases that abstract away Python virtual environment complexity:

### Quick Installation

```bash
# Install aliases to your shell
./install.sh

# Source your shell config
source ~/.zshrc  # or ~/.bashrc
```

### Usage Examples

```bash
# Process single YouTube video
mksynth "https://youtube.com/watch?v=..."

# Process multiple videos
mksynth "https://youtube.com/video1 https://youtube.com/video2"
mksynth "https://youtube.com/video1,https://youtube.com/video2"

# Process playlist
mksynth "https://youtube.com/playlist?list=..."

# Template-specific commands
mksynth-meeting "https://youtube.com/watch?v=..."
mksynth-lecture "https://youtube.com/playlist?list=..."

# Batch processing
mksynth batch --urls urls.txt

# Batch processing with essay synthesis
mksynth batch --urls urls.txt --essay

# Force essay generation
mksynth batch --urls urls.txt --essay --force-essay
```

### Available Commands

**Primary Commands:**
- `mksynth <url>` - Process YouTube URL(s)
- `mksynth batch --urls <file>` - Batch process URLs file
- `mksynth batch --urls <file> --essay` - Batch process URLs and generate comprehensive essay
- `mksynth scan` - Scan directories for media files
- `mksynth watch` - Continuous directory monitoring

**Template-Specific Commands:**
- `mksynth-summary` - Basic summary template
- `mksynth-meeting` - Meeting minutes template
- `mksynth-lecture` - Lecture summary template
- `mksynth-tutorial` - Tutorial guide template
- `mksynth-project` - Project update template
- `mksynth-customer` - Customer feedback template

### Input Formats Supported
- **Single URL**: Standard YouTube video or playlist URL
- **Space-delimited**: "url1 url2 url3"
- **Comma-delimited**: "url1,url2,url3"
- **File**: Path to file containing URLs (one per line)

### Features
- **Automatic Virtual Environment**: No need to activate manually
- **Smart URL Detection**: Handles multiple input formats
- **Template Shortcuts**: Pre-configured prompt aliases
- **Cross-Platform**: Works on macOS/Linux
- **Backward Compatible**: Original Python CLI still works

## 🔍 File Scanner Feature

The file scanner provides automated scanning and monitoring of directories for media files, automatically copying them to the appropriate data directories with optional auto-processing through the full pipeline.

### Quick Start

```bash
# One-time scan of Downloads directory
python main.py scan

# Continuous monitoring of Downloads directory
python main.py watch

# Scan and auto-process files through pipeline
python main.py scan --process --prompt meeting_minutes

# Watch with auto-processing enabled
python main.py watch --process

# Watch with custom interval and auto-processing
python main.py watch --interval 10 --process

# Scan custom directory
python main.py scan --directory /path/to/media

# Dry run (show what would happen without copying)
python main.py scan --dry-run
```

### Configuration

Set environment variables in `.env`:

```bash
# File Scanner Configuration
MKD_DOWNLOAD_DIR=/custom/path
MKD_SCAN_INTERVAL=60
MKD_AUTO_PROCESS=true
MKD_SKIP_EXISTING=true
```

### Supported File Formats

**Video**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, `.wmv` → `data/videos/`

**Audio**: `.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`, `.ogg`, `.wma` → `data/audio/`

### Features

- **Automatic File Detection**: Identifies media files by extension
- **Smart Organization**: Copies files to appropriate directories
- **Duplicate Handling**: Skips files that already exist in destination
- **Auto-processing**: Optionally process files through full pipeline (transcription + synthesis) after copying using `--process` flag
- **Dry-run Mode**: Preview operations without actual file copying
- **Continuous Monitoring**: Watch directories for new files in real-time
- **Cross-platform**: Works on macOS, Linux, and Windows
- **File Validation**: Skips zero-byte files and partially downloaded files

## 📝 Available Prompt Templates

| Template | Description |
|----------|-------------|
| `basic_summary` | Extract core thesis, insights, and takeaways |
| `meeting_minutes` | Decisions, action items, and open questions |
| `lecture_summary` | Key concepts, examples, and learning objectives |
| `tutorial_guide` | Step-by-step instructions and best practices |
| `project_update` | Progress, blockers, and next steps |
| `customer_feedback` | Sentiment analysis and key themes |
| `research_summary` | Methodology, findings, and implications |
| `interview_summary` | Key quotes, themes, and insights |
| `blog_post_outline` | Structure for blog content creation |
| `social_media_content` | Engaging posts for social platforms |
| `technical_documentation` | Clear technical explanations |
| `bug_report_summary` | Issue description, reproduction, and solutions |

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with these variables:

```bash
# Whisper Configuration
WHISPER_MODEL_SIZE=small

# Local Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Cloud Ollama Configuration (PLACEHOLDER - verify from official docs)
OLLAMA_CLOUD_URL=https://api.ollama.ai/v1
OLLAMA_CLOUD_API_KEY=your_api_key_here

# Default Synthesis Settings
DEFAULT_SYNTHESIS_PROMPT_TEMPLATE=basic_summary

# File Scanner Configuration
MKD_DOWNLOAD_DIR=~/Downloads
MKD_SCAN_INTERVAL=5
MKD_AUTO_PROCESS=false
MKD_SKIP_EXISTING=true
```

### Whisper Model Sizes

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | ~39MB | Fastest | Lowest | Quick drafts, testing |
| `base` | ~74MB | Fast | Good | General use |
| `small` | ~244MB | Medium | Better | **Recommended for M3 Mac** |
| `medium` | ~769MB | Slow | High | High-quality transcripts |
| `large` | ~1550MB | Slowest | Best | Critical content |

### Ollama Model Selection

Recommended models for knowledge synthesis:

- `llama3.1:8b` - Good balance of speed and quality (default)
- `llama3.1:70b` - Higher quality, slower
- `mistral:7b` - Fast, good for summaries
- `phi3:14b` - Efficient, good for structured outputs

## 🔧 Pipeline Architecture

```
┌─────────────────┐
│  Media Input    │
│  (Video/Audio)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessor   │
│  - Detect type  │
│  - Extract audio│
│  - Convert to WAV│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Transcriber   │
│  - Whisper model│
│  - Auto-chunking│
│  (if >25 min)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Synthesizer   │
│  - Ollama local │
│  - Ollama cloud │
│  - Prompt templates│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Output        │
│  - Console      │
│  - JSON file    │
└─────────────────┘
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "ffmpeg not found"
**Solution:** Install ffmpeg using Homebrew (macOS) or apt (Linux):
```bash
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

#### 2. "Ollama connection refused"
**Solution:** Ensure Ollama is running:
```bash
# Start Ollama service
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

#### 3. "Whisper model not found"
**Solution:** The model will download automatically on first run. Ensure you have internet connection and sufficient disk space.

#### 4. "Out of memory" during transcription
**Solution:** Use a smaller Whisper model:
```bash
# In .env file
WHISPER_MODEL_SIZE=tiny  # or base
```

#### 5. "Long file processing is slow"
**Solution:** This is expected for files >25 minutes. The system automatically chunks them. Consider using a smaller model for faster processing.

#### 6. "Cloud Ollama authentication failed"
**Solution:** Verify your API key and endpoint URL in `.env`. Note: The cloud endpoint is a placeholder and may need verification from official Ollama Cloud documentation.

#### 7. "Module not found" errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

#### 8. "Files not being processed after copying"
**Solution:** Use the `--process` flag to enable auto-processing:
```bash
python main.py scan --process
python main.py watch --process
```

#### 9. "Zero-byte files being skipped"
**Solution:** This is intentional - the system skips incomplete downloads. Wait for files to finish downloading before processing.

#### 10. "Watch mode not detecting new files"
**Solution:** Ensure files have completed downloading and are not zero bytes. Use `--interval` to adjust polling frequency.

### Debug Mode

For detailed error messages, run with verbose output:

```bash
python main.py --input video.mp4 --verbose
```

## 📊 Output Format

### Console Output
```
═══════════════════════════════════════════════════════════════
Media-to-Knowledge Pipeline
═══════════════════════════════════════════════════════════════
Started at: 2026-02-04 14:30:00
═══════════════════════════════════════════════════════════════

✓ Status: Success
📁 File: video.mp4 (125.4 MB)
🎬 Type: Video
📝 Transcript: [First 500 characters...]
🧠 Synthesis: [Full synthesis result...]

✓ Pipeline completed successfully!
Total processing time: 45.23 seconds
```

### JSON Output
```json
{
  "status": "success",
  "file_info": {
    "name": "video.mp4",
    "size": 125400000,
    "size_formatted": "125.4 MB",
    "type": "video"
  },
  "transcript": "Full transcript text...",
  "synthesis": "Synthesized knowledge...",
  "processing_time": 45.23,
  "timestamp": "2026-02-04T14:30:00"
}
```

## 🔐 Security Notes

- **API Keys**: Never commit `.env` files to version control
- **Local Processing**: All processing happens locally by default - no data leaves your machine
- **Cloud Processing**: When using `--cloud`, your transcript is sent to the cloud endpoint
- **Temporary Files**: Audio files are stored in `temp/` directory and can be deleted after processing

## 📚 Advanced Usage

### Processing Multiple Files

Create a shell script to batch process files:

```bash
#!/bin/bash
for file in /path/to/media/*.mp4; do
    python main.py --input "$file" --output "results/$(basename "$file" .mp4).json"
done
```

### Custom Prompt Templates

Add your own templates in `core/prompts.py`:

```python
CUSTOM_TEMPLATE = """
Your custom prompt here: {transcript}
"""
```

### Integration with Other Tools

The JSON output can be easily integrated with:
- Notion API
- Obsidian plugins
- Database systems
- Web applications

## 📖 Documentation

For more detailed information, see our comprehensive documentation:

- [Running Tests Guide](docs/RUNNING_TESTS.md) - Complete guide to testing the pipeline
- [Video/Audio to Knowledge Synthesis](docs/VIDEO_AUDIO_TO_KNOWLEDGE.md) - Advanced usage patterns and optimization

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional prompt templates
- Support for more media formats
- Web interface
- Real-time processing
- Multi-language support

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text
- [Ollama](https://ollama.ai) for local LLM inference
- [ffmpeg](https://ffmpeg.org) for media processing

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Configuration](#-configuration) guide
3. Open an issue on GitHub

---

**Note about Ollama Cloud**: The `OLLAMA_CLOUD_URL` endpoint is a placeholder. Please verify the correct endpoint from official Ollama Cloud documentation before using cloud features. The local Ollama integration is fully tested and recommended for most use cases.