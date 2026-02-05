# Video and Audio to Knowledge Synthesis Guide

This guide provides comprehensive instructions for using the Media-to-Knowledge Pipeline to convert video and audio content into structured, actionable knowledge.

## 🎯 Overview

The Media-to-Knowledge Pipeline transforms media content through a three-stage process:

1. **Media Preparation** - Extract audio from video files and convert to compatible formats
2. **Speech-to-Text Transcription** - Convert audio to text using OpenAI Whisper
3. **Knowledge Synthesis** - Extract insights using Ollama models (local or cloud)

## 📁 Supported Media Formats

### Video Formats
- **MP4** - Most common format, widely supported
- **MOV** - Apple QuickTime format
- **AVI** - Audio Video Interleave
- **MKV** - Matroska container
- **WebM** - Web-optimized format

### Audio Formats
- **MP3** - Most common audio format
- **WAV** - Uncompressed audio (best quality)
- **M4A** - Apple audio format
- **FLAC** - Free Lossless Audio Codec
- **AAC** - Advanced Audio Coding
- **OGG** - Open audio format

## 🚀 Quick Start Guide

### Basic Usage

Process a video file with default settings:
```bash
python main.py --input /path/to/video.mp4
```

Process an audio file:
```bash
python main.py --input /path/to/audio.mp3
```

### Save Results to File
```bash
python main.py --input meeting.mp4 --output meeting_summary.json
```

### Save Synthesis to Markdown
```bash
# Save only the synthesized knowledge as markdown
python main.py --input meeting.mp4 --markdown

# Save both JSON results and markdown synthesis
python main.py --input meeting.mp4 --output meeting_summary.json --markdown

# Specify custom markdown output directory
python main.py --input meeting.mp4 --markdown /path/to/markdown/output
```

> **Note**: The markdown output feature automatically generates descriptive filenames based on the content of the synthesis. For detailed information about this feature, see [MARKDOWN_OUTPUT_FEATURE.md](MARKDOWN_OUTPUT_FEATURE.md).

## 🎛️ Advanced Configuration

### Using Built-in Prompt Templates

The pipeline includes 12 built-in prompt templates for different use cases:

```bash
# Meeting minutes
python main.py --input meeting.mp4 --prompt meeting_minutes

# Lecture summary
python main.py --input lecture.mp4 --prompt lecture_summary

# Project update
python main.py --input update.mp4 --prompt project_update

# Customer feedback analysis
python main.py --input feedback.mp3 --prompt customer_feedback

# Research paper summary
python main.py --input paper.mp4 --prompt research_summary

# Interview analysis
python main.py --input interview.mp3 --prompt interview_summary

# Blog post outline
python main.py --input brainstorm.mp4 --prompt blog_post_outline

# Social media content
python main.py --input presentation.mp4 --prompt social_media_content

# Technical documentation
python main.py --input demo.mp4 --prompt technical_documentation

# Bug report summary
python main.py --input debug_session.mp4 --prompt bug_report_summary
```

### Using Custom Prompts

Create your own synthesis prompt:
```bash
python main.py --input interview.mp4 --prompt "Extract the 5 key insights from this discussion: {transcript}"
```

### Using Cloud Ollama

Process with cloud Ollama instead of local:
```bash
python main.py --input /path/to/audio.mp3 --cloud
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

| Template | Description | Best For |
|----------|-------------|----------|
| `basic_summary` | Core thesis, insights, and takeaways | General summaries |
| `meeting_minutes` | Decisions, action items, open questions | Business meetings |
| `lecture_summary` | Key concepts, examples, learning objectives | Educational content |
| `tutorial_guide` | Step-by-step instructions and best practices | How-to guides |
| `project_update` | Progress, blockers, and next steps | Team updates |
| `customer_feedback` | Sentiment analysis and key themes | Feedback analysis |
| `research_summary` | Methodology, findings, and implications | Academic content |
| `interview_summary` | Key quotes, themes, and insights | Interview analysis |
| `blog_post_outline` | Structure for blog content creation | Content creation |
| `social_media_content` | Engaging posts for social platforms | Social media |
| `technical_documentation` | Clear technical explanations | Tech docs |
| `bug_report_summary` | Issue description, reproduction, and solutions | Debug sessions |

## ⚙️ Configuration Options

### Environment Variables

Configure the pipeline through the `.env` file:

```bash
# Whisper Configuration
WHISPER_MODEL_SIZE=small

# Local Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Cloud Ollama Configuration (verify from official docs)
OLLAMA_CLOUD_URL=https://api.ollama.ai/v1
OLLAMA_CLOUD_API_KEY=your_api_key_here

# Default Synthesis Settings
DEFAULT_SYNTHESIS_PROMPT_TEMPLATE=basic_summary
```

### Whisper Model Selection

Choose the right model based on your needs:

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | ~39MB | Fastest | Lowest | Quick drafts, testing |
| `base` | ~74MB | Fast | Good | General use |
| `small` | ~244MB | Medium | Better | **Recommended for M3 Mac** |
| `medium` | ~769MB | Slow | High | High-quality transcripts |
| `large` | ~1550MB | Slowest | Best | Critical content |

### Ollama Model Recommendations

For knowledge synthesis:

- `llama3.1:8b` - Good balance of speed and quality (default)
- `llama3.1:70b` - Higher quality, slower
- `mistral:7b` - Fast, good for summaries
- `phi3:14b` - Efficient, good for structured outputs

## 📊 Output Formats

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
  "media_file": "/path/to/video.mp4",
  "audio_file": "/tmp/audio.wav",
  "transcript": "Full transcript text...",
  "transcript_length": 12345,
  "synthesis": {
    "raw_text": "Synthesized knowledge...",
    "model_used": "llama3.1:8b",
    "template_used": "meeting_minutes",
    "transcript_length": 12345,
    "synthesis_length": 5432,
    "use_cloud": false
  },
  "model_used": "llama3.1:8b",
  "template_used": "meeting_minutes",
  "processing_time": 45.23,
  "error": null
}
```

## 📁 Organizing Your Media Files

### Recommended Directory Structure

```
media_library/
├── meetings/
│   ├── 2026-01-team-meeting.mp4
│   ├── 2026-01-client-call.mp3
│   └── quarterly_review.mov
├── lectures/
│   ├── machine_learning_basics.mp4
│   ├── python_tutorial.mp4
│   └── research_seminar.mp4
├── interviews/
│   ├── candidate_interview.mp4
│   └── expert_panel.mp3
├── podcasts/
│   ├── tech_podcast_ep1.mp3
│   └── business_insights.mp3
└── outputs/
    ├── summaries/
    ├── transcripts/
    └── json/
```

### Batch Processing Script

Process multiple files with a shell script:

```bash
#!/bin/bash
# batch_process.sh

INPUT_DIR="./media_library/meetings"
OUTPUT_DIR="./outputs/summaries"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Process all MP4 files
for file in "$INPUT_DIR"/*.mp4; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .mp4)
        echo "Processing $filename..."
        python main.py \
            --input "$file" \
            --prompt meeting_minutes \
            --output "$OUTPUT_DIR/${filename}_summary.json"
    fi
done

echo "Batch processing complete!"
```

Make the script executable and run it:
```bash
chmod +x batch_process.sh
./batch_process.sh
```

## ⏱️ Performance Optimization

### Large File Processing

Files longer than 25 minutes are automatically chunked for processing:
- Files are split into 10-minute segments
- Each segment is processed independently
- Results are concatenated for final synthesis

### Memory Management

For systems with limited RAM:
1. Use smaller Whisper models (`tiny` or `base`)
2. Process one file at a time
3. Monitor system resources during processing

### Speed Optimization

To optimize processing speed:
1. Use SSD storage for temporary files
2. Close unnecessary applications during processing
3. Use the `small` Whisper model for good balance of speed/quality
4. Consider using cloud Ollama for faster synthesis

## 🔧 Troubleshooting Common Issues

### Transcription Issues

#### Poor Transcription Quality
- **Solution**: Use a larger Whisper model (`medium` or `large`)
- **Solution**: Ensure audio quality is good (clear speaking, minimal background noise)

#### "Out of Memory" Errors
- **Solution**: Use a smaller Whisper model
- **Solution**: Process shorter segments manually

### Synthesis Issues

#### Slow Synthesis
- **Solution**: Ensure Ollama is running with sufficient resources
- **Solution**: Use a smaller/faster Ollama model
- **Solution**: Consider using cloud Ollama for faster processing

#### Irrelevant Synthesis Results
- **Solution**: Use a more specific prompt template
- **Solution**: Provide a custom prompt with specific instructions
- **Solution**: Use a more capable Ollama model

### File Processing Issues

#### Unsupported File Format
- **Solution**: Convert to supported format using ffmpeg:
  ```bash
  ffmpeg -i input.wmv -c:a mp3 output.mp3
  ```

#### File Not Found Errors
- **Solution**: Verify file path is correct
- **Solution**: Ensure file permissions allow reading

## 🛡️ Privacy and Security

### Data Handling

- **Local Processing**: All processing happens locally by default - no data leaves your machine
- **Cloud Processing**: When using `--cloud`, only the transcript is sent to the cloud endpoint
- **Temporary Files**: Audio files are stored in system temp directories and deleted after processing

### Best Practices

1. **Review content** before processing sensitive material
2. **Use local processing** for confidential content
3. **Verify cloud endpoints** before sending data
4. **Store API keys securely** in `.env` file (never commit to version control)

## 🔄 Integration with Other Tools

### Notion Integration

Export results to Notion using the JSON output:
```python
import json
import requests

# Read the JSON output
with open('meeting_summary.json', 'r') as f:
    data = json.load(f)

# Send to Notion API
notion_data = {
    "parent": {"database_id": "your_database_id"},
    "properties": {
        "Name": {"title": [{"text": {"content": "Meeting Summary"}}]},
        "Summary": {"rich_text": [{"text": {"content": data['synthesis']['raw_text']}}]}
    }
}

requests.post(
    "https://api.notion.com/v1/pages",
    headers={
        "Authorization": "Bearer your_integration_token",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    },
    json=notion_data
)
```

### Obsidian Integration

Save summaries as Markdown files for Obsidian:
```bash
# Convert JSON to Markdown
python -c "
import json
with open('summary.json', 'r') as f:
    data = json.load(f)
with open('summary.md', 'w') as f:
    f.write(f'# {data[\"media_file\"]}\\n\\n')
    f.write(f'## Transcript\\n\\n{data[\"transcript\"]}\\n\\n')
    f.write(f'## Synthesis\\n\\n{data[\"synthesis\"][\"raw_text\"]}\\n')
"
```

## 📈 Advanced Usage Patterns

### Creating Custom Prompt Templates

Add your own templates in `core/prompts.py`:

```python
CUSTOM_EXECUTIVE_BRIEF = """
As a senior executive, provide a concise briefing on this content:

{transcript}

Please structure your response as:
1. Executive Summary (2-3 sentences)
2. Key Metrics/Numbers (if applicable)
3. Strategic Implications (2-3 points)
4. Recommended Actions (2-3 items)
"""
```

Then register it in the `PROMPT_TEMPLATES` dictionary:
```python
PROMPT_TEMPLATES = {
    # ... existing templates ...
    "executive_brief": CUSTOM_EXECUTIVE_BRIEF,
}
```

### Processing Live Streams

For processing live streams, first record them to a file:
```bash
# Record a live stream
ffmpeg -i "https://stream-url/live.m3u8" -c copy recording.mp4

# Then process with the pipeline
python main.py --input recording.mp4 --prompt meeting_minutes
```

### Automated Processing Pipeline

Set up automated processing with cron jobs:
```bash
# Process daily podcast episodes
0 6 * * * cd /path/to/media-pipeline && python main.py --input /podcasts/latest.mp3 --prompt podcast_summary --output /summaries/$(date +\%Y-\%m-\%d).json
```

## 🆕 Future Enhancements

Planned improvements to the pipeline:

1. **Multi-language Support** - Automatic language detection and translation
2. **Real-time Processing** - Stream processing capabilities
3. **Web Interface** - Graphical user interface for easier use
4. **Speaker Diarization** - Identify different speakers in conversations
5. **Emotion Analysis** - Detect sentiment and emotional tone
6. **Keyword Extraction** - Automatically identify key topics and terms

---

**Note about Ollama Cloud**: The `OLLAMA_CLOUD_URL` endpoint is a placeholder. Please verify the correct endpoint from official Ollama Cloud documentation before using cloud features. The local Ollama integration is fully tested and recommended for most use cases.