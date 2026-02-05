# Media-to-Knowledge Pipeline

A modular Python application that processes video and audio files through transcription and knowledge synthesis using local or cloud Ollama models. Extract actionable insights, summaries, and structured knowledge from your media content.

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

## 📋 Project Structure

```
media_knowledge_pipeline/
├── main.py                 # Main orchestration script with CLI
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── core/                   # Core pipeline modules
│   ├── __init__.py
│   ├── media_preprocessor.py  # Video/audio detection and preparation
│   ├── transcriber.py          # Whisper-based transcription
│   ├── synthesizer.py          # Ollama knowledge synthesis
│   └── prompts.py              # Reusable prompt templates
└── utils/                  # Utility functions
    ├── __init__.py
    ├── file_handler.py         # File validation and operations
    └── chunker.py              # Audio chunking for long files
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

### Basic Usage (Local Ollama)

Process a video file with default settings:

```bash
python main.py --input /path/to/video.mp4
```

### Use Cloud Ollama

Process with cloud Ollama instead of local:

```bash
python main.py --input /path/to/audio.mp3 --cloud
```

### Use Built-in Prompt Templates

```bash
# Meeting minutes
python main.py --input meeting.mp4 --prompt meeting_minutes

# Lecture summary
python main.py --input lecture.mp4 --prompt lecture_summary

# Project update
python main.py --input update.mp4 --prompt project_update

# Customer feedback analysis
python main.py --input feedback.mp3 --prompt customer_feedback
```

### Use Custom Prompt

```bash
python main.py --input interview.mp4 --prompt "Summarize the key points: {transcript}"
```

### Save Results to File

```bash
python main.py --input lecture.mp4 --output results.json
```

### Quiet Mode (Minimal Output)

```bash
python main.py --input video.mp4 --quiet
```

### Full Example with All Options

```bash
python main.py \
  --input /path/to/meeting.mp4 \
  --prompt meeting_minutes \
  --output meeting_summary.json \
  --cloud
```

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