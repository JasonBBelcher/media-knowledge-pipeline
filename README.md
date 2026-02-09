<pre align="center"> __  __  ___  ___   ___    _     _  __ _  _   ___  __      __ _     ___  ___    ___  ___ 
|  \/  || __||   \ |_ _|  /_\   | |/ /| \| | / _ \ \ \    / /| |   | __||   \  / __|| __|
| |\/| || _| | |) | | |  / _ \  | ' < | .` || (_) | \ \/\/ / | |__ | _| | |) || (_ || _| 
|_|  |_||___||___/ |___|/_/ \_\ |_|\_\|_|\_| \___/   \_/\_/  |____||___||___/  \___||___|
                                                                                         
 ___  ___  ___  ___  _     ___  _  _  ___ 
| _ \|_ _|| _ \| __|| |   |_ _|| \| || __|
|  _/ | | |  _/| _| | |__  | | | .` || _| 
|_|  |___||_|  |___||____||___||_|\_||___|
                                          </pre>

<h1 align="center">Media-to-Knowledge Pipeline</h1>

<p align="center">
  <strong>Version 2.5.0</strong>
</p>

<br />

## 🧠 The Neural Distillation Protocol

**Directive 80/20**: In a universe of infinite data streams, true power lies not in consumption, but in strategic extraction.

Human cognition operates in two primary modes:

**Recreational Processing**: Passive absorption for neural coherence maintenance.

**Tactical Acquisition**: Active mining of high-value payloads for world-state manipulation.

This repository is a Knowledge Assimilation Engine. It bypasses the noise of the datasphere to isolate the critical 20% of informational mass that yields 80% of actionable insight. It transforms raw media and documents into structured intelligence, ready for deployment.

## 📋 Changelog

### v2.5.0 (February 9, 2026) - Full Anki Integration

#### Major Features
- **Complete Anki Integration**: Fully implemented Anki flashcard generation system with comprehensive CLI interface
- **Adapter Pattern Framework**: Extensible output adapter system for transforming pipeline output to various formats
- **Content Classification Engine**: Automatic classification of knowledge into flashcards (concepts, Q&A, events, processes)
- **Enhanced Prompt System**: Specialized Anki template for optimized flashcard content extraction

#### Anki CLI Command Suite
- `anki generate` - Generate importable Anki decks from synthesis output
- `anki preview` - Preview what flashcards will be generated
- `anki templates` - View available flashcard templates and patterns

#### Technical Improvements
- **Robust Validation**: JSON schema validation for Anki content with graceful fallback
- **Test Coverage**: Comprehensive unit and integration tests (31/31 tests passing)
- **Dual Output**: Support for both standard synthesis and Anki-specific structured output
- **Cross-Platform Support**: Generated .apkg files work across Windows, macOS, and Linux

### v2.4.1 (February 9, 2026)
- **Output Directory Fix**: Files now properly created in dedicated `outputs/` directory
- **Git Exclusion**: `.gitignore` configured to exclude output files while preserving structure
- **Large Document Processing**: Intelligent chunking for documents exceeding model limits
- **File Organization**: Document processor moved to proper `core/` directory
- **Anki Infrastructure**: Core framework setup for seamless Anki integration

### v2.4.0 (February 7, 2026)
- **Document Processing Support**: Added ability to read and synthesize knowledge from PDF, EPUB, and MOBI files using specialized document readers
- **Document Reader Infrastructure**: Created modular document reader system with factory pattern supporting PyMuPDF, ebooklib, and mobi libraries
- **Enhanced File Scanner**: Updated file scanner to automatically detect and organize document files (.pdf, .epub, .mobi) alongside media files
- **Document Metadata Extraction**: Extract document properties including page counts, word counts, and file information for comprehensive processing
- **Document CLI Commands**: New `document` CLI command with subcommands for processing single documents, batch processing, and format information
- **Unified Knowledge Synthesis**: Document processing uses the same powerful prompt templates and Ollama models as media processing

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

## 🎯 Capabilities

### Knowledge Extraction Engine
- **Universal Media Processing**: Process video (MP4, MOV, AVI), audio (MP3, WAV, M4A, FLAC), and documents (PDF, EPUB, MOBI) files
- **Document Intelligence**: Extract text and synthesize knowledge from PDF, EPUB, and MOBI documents with metadata extraction
- **Automatic Transcription**: Convert speech to text using OpenAI Whisper with support for long files (>25 minutes)
- **Knowledge Synthesis**: Extract insights using Ollama models (local or cloud) with 13 built-in prompt templates

### Output and Integration
- **Complete Anki Integration**: Transform synthesis output into importable Anki decks with automatic content classification
- **Structured Data Export**: Save results as JSON, Markdown, or ready-to-use Anki packages (.apkg)
- **Adapter Framework**: Extensible output system supporting multiple formats (Anki, JSON, Markdown)
- **Custom Prompts**: Use your own synthesis prompts for specialized knowledge extraction

### User Experience
- **Modern Python CLI**: Rich terminal interface with colorful output, progress indicators, and autocomplete
- **Smart Automation**: Automated directory scanning, file processing, and content organization
- **Cross-Platform Support**: Works seamlessly on macOS, Linux, and Windows systems
- **Flexible Deployment**: Run entirely locally or use cloud Ollama services based on content requirements

### Advanced Features
- **YouTube Integration**: Process single videos, entire playlists, or batch URLs with automatic organization
- **Multi-Source Essay Synthesis**: Generate comprehensive essays from multiple sources with cohesion checking
- **Content Classification**: Automatic classification into concepts, Q&A, events, and process-based flashcards
- **Token-Based Optimization**: Intelligent model selection based on content volume to prevent context overflow

## 📚 Anki Integration (Complete Implementation)

The Media Knowledge Pipeline now includes **complete Anki integration** featuring an extensible adapter pattern framework that transforms pipeline output into structured flashcards ready for spaced repetition learning. This represents a major enhancement to the knowledge retention workflow.

### 🎯 Complete Anki Feature Set

#### Core Functionality
- **Full CLI Integration**: Comprehensive `anki` command suite integrated with the modern Python CLI
- **Automatic Content Classification**: Intelligently categorizes knowledge into optimal flashcard types
- **Adapter Pattern Framework**: Extensible system supporting multiple output formats
- **Robust Validation**: JSON schema validation ensures proper flashcard structure

#### Flashcard Types Supported
- **Concept Definitions**: Terms, definitions, and contextual examples
- **Q&A Pairs**: Problem-solution pairs with detailed explanations
- **Historical Events**: Chronological events with significance
- **Process Steps**: Sequential procedures and workflows
- **Custom Types**: Extensible framework for specialized content

#### CLI Command Suite
```bash
# Generate importable Anki decks
media-knowledge anki generate --input synthesis.json --output flashcards.apkg

# Preview flashcards before generation
media-knowledge anki preview --input synthesis.json --detailed

# View available flashcard templates
media-knowledge anki templates

# Generate with custom deck name
media-knowledge anki generate --input synthesis.json --deck-name "My Study Deck"
```

### 🔄 Adapter Pattern Architecture
The Anki integration uses a sophisticated adapter pattern:
- **Base Adapter Class**: Standard interface for all output formats
- **Anki Adapter**: Transform pipeline JSON to Anki-compatible structure
- **Schema Validation**: Ensures proper flashcard structure and content
- **Graceful Fallback**: Works even when external libraries are unavailable

### 🧪 Test Coverage
- **26/26 Unit Tests**: Comprehensive test suite covering all adapter functionality
- **5/5 CLI Tests**: Full integration testing of Anki command suite
- **Schema Validation**: Robust content validation with JSON schema
- **Cross-Platform**: Verified working across Windows, macOS, and Linux

The Anki integration transforms passive content consumption into active learning, enabling users to systematically build knowledge repositories through spaced repetition.

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
│   ├── prompts.py              # Reusable prompt templates (incl. Anki templates)
│   ├── file_scanner.py         # Automated file scanning and monitoring
│   ├── document_processor.py    # Document processing integration
│   ├── anki_generator.py       # Complete Anki deck generation engine
│   ├── output_adapters/        # Output transformation framework
│   │   ├── __init__.py
│   │   ├── base_adapter.py     # Interface for all output formats
│   │   ├── anki_adapter.py    # Transform pipeline JSON to Anki flashcards
│   │   └── anki_schema.py     # JSON schema validation for content
│   └── document_readers/       # Document format readers
│       ├── __init__.py
│       ├── base.py             # Base reader class and factory
│       ├── pdf_reader.py       # PDF text extraction
│       ├── epub_reader.py      # EPUB content extraction
│       └── mobi_reader.py      # MOBI document processing
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
                ├── document.py      # Document processing commands
                ├── anki.py          # Anki flashcard generation commands
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

### Step 3: Document Processing Libraries

Document processing libraries are automatically installed with the requirements, but you may need system dependencies:

**macOS:**
```bash
# PyMuPDF dependencies (usually installed automatically)
brew install pkg-config
```

**Linux:**
```bash
# PyMuPDF dependencies
sudo apt-get install libcairo2-dev gir1.2-poppler-0.18
```

### Step 4: Verify Anki Integration

The Anki integration is automatically included with standard installation. Verify functionality:

```bash
# Check that Anki integration packages are available
python -c "import genanki; import jsonschema; print('✓ Anki integration libraries OK')"

# Test the Anki CLI command
media-knowledge anki --help
```

### Step 5: Install Ollama (for Local Processing)

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., llama3.1:8b)
ollama pull llama3.1:8b
```

### Step 6: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

### Step 7: Verify Installation

```bash
# Check Python version
python --version

# Check ffmpeg
ffmpeg -version

# Check Ollama (if using local)
ollama list

# Check document processing libraries
python -c "import fitz; print('PyMuPDF OK'); import ebooklib; print('ebooklib OK'); import mobi; print('mobi OK')"

# Check Anki integration libraries
python -c "import genanki; print('genanki OK'); import jsonschema; print('jsonschema OK')"
```

## 🚀 Quick Start Guide

Choose your preferred usage pattern:

### Interactive Frontend (Recommended for New Users)
Run the interactive menu-driven interface:
```bash
./media-knowledge-interactive
```
This provides a guided experience with ASCII art and step-by-step configuration.

### Typer CLI (Recommended for Power Users)
Use the modern command-line interface wrapper:
```bash
./media-knowledge --help
./media-knowledge --version
./media-knowledge status
```

Or use the direct module execution:
```bash
# Navigate to project directory
cd /Users/jasonbelcher/Documents/code/media-knowledge-pipeline

# Activate the virtual environment first
source venv/bin/activate

# Then run commands
python -m src.media_knowledge.cli.app --help
python -m src.media_knowledge.cli.app --version
```

### Common Examples
```bash
# System status
./media-knowledge status

# Process YouTube video
./media-knowledge process media --input "https://youtube.com/watch?v=..."

# Generate Anki flashcards
./media-knowledge anki generate --input synthesis.json

# Process documents
./media-knowledge document process document.pdf

# Batch process URLs
./media-knowledge batch process-urls --urls youtube_urls.txt
```

## 💻 Usage

### Modern Python CLI (Recommended)

The enhanced Python CLI provides a rich terminal experience with colorful output, progress indicators, and comprehensive help:

**Before using any CLI commands, activate the virtual environment:**
```bash
# Navigate to project directory
cd /Users/jasonbelcher/Documents/code/media-knowledge-pipeline

# Activate the virtual environment (required for CLI commands)
source venv/bin/activate
```

**Then you can use all CLI commands:**
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

# Process documents (after activating virtual environment)
media-knowledge document formats
media-knowledge document process document.pdf
media-knowledge document batch /path/to/documents/ --pattern "*.pdf"

# Complete Anki flashcard integration (new v2.5.0)
media-knowledge anki generate --input synthesis.json --output flashcards.apkg
media-knowledge anki preview --input synthesis.json --detailed
media-knowledge anki generate --input synthesis.json --deck-name "My Study Deck"
media-knowledge anki templates
```

**Don't forget to deactivate the virtual environment when done:**
```bash
deactivate
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
├── comprehensive_analysis_from_existing_docs.md
└── flashcards/
    └── my_lecture_anki.apkg
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

#### Complete Anki Flashcard Generation (v2.5.0)
```bash
# Generate importable Anki deck
media-knowledge anki generate --input synthesis.json --output output_deck.apkg

# Generate with custom deck name and tags
media-knowledge anki generate --input synthesis.json --deck-name "Machine Learning" --auto-tag

# Preview with detailed card-by-card breakdown
media-knowledge anki preview --input synthesis.json --detailed

# Quick preview of what would be generated
media-knowledge anki preview --input synthesis.json

# View all available flashcard templates
media-knowledge anki templates

# Process document and generate flashcards in one command
media-knowledge document process book.pdf --prompt anki_flashcards --output flashcards.json
```

### CLI Features

- **Colorful Output**: Red errors, green successes, blue information
- **Progress Indicators**: Real-time progress bars and spinners
- **Autocomplete**: Tab completion for commands and options
- **Help System**: Context-sensitive help for all commands
- **Rich Formatting**: Tables, lists, and formatted output
- **Verbose Logging**: Detailed operation information when needed

### Input Formats Supported
- **Single URL**: Standard YouTube video or playlist URL
- **Space-delimited**: "url1 url2 url3"
- **Comma-delimited**: "url1,url2,url3"
- **File**: Path to file containing URLs (one per line)
- **Document Files**: PDF, EPUB, and MOBI files for knowledge extraction

### Features
- **Automatic Virtual Environment**: No need to activate manually
- **Smart URL Detection**: Handles multiple input formats
- **Template Shortcuts**: Pre-configured prompt aliases
- **Cross-Platform**: Works on macOS/Linux
- **Backward Compatible**: Original Python CLI still works

## 📚 Document Processing

Process knowledge from PDF, EPUB, and MOBI documents with the same powerful synthesis capabilities:

**Before using document commands, activate the virtual environment:**
```bash
# Navigate to project directory
cd /Users/jasonbelcher/Documents/code/media-knowledge-pipeline

# Activate the virtual environment (required for CLI commands)
source media_knowledge_env/bin/activate
```

### Process Single Documents
```bash
# Process a PDF document
media-knowledge document process document.pdf

# Process with specific prompt template
media-knowledge document process research_paper.pdf --prompt research_summary

# Use cloud Ollama for better processing
media-knowledge document process large_book.epub --cloud

# Save results to file
media-knowledge document process document.mobi --output results.json

# Combine multiple options
media-knowledge document process book.pdf \
  --prompt basic_summary \
  --output book_summary.json \
  --cloud
```

**All document processing commands require the virtual environment to be activated as shown above.**

### Batch Document Processing
```bash
# Process all PDFs in a directory
media-knowledge document batch /path/to/documents/ --pattern "*.pdf"

# Process all document types with custom pattern
media-knowledge document batch /path/to/library/ --pattern "*.*"

# Save batch results to file
media-knowledge document batch ./books/ --output batch_results.json

# Batch processing with cloud models and custom prompt
media-knowledge document batch ./papers/ \
  --pattern "*.pdf" \
  --prompt research_summary \
  --cloud \
  --output research_batch.json
```

### Check Supported Formats
```bash
# Show all supported document formats
media-knowledge document formats
```

**Don't forget to deactivate the virtual environment when you're done:**
```bash
deactivate
```

### Document Processing Features
- **Multi-format Support**: PDF (.pdf), EPUB (.epub), MOBI (.mobi)
- **Metadata Extraction**: Page counts, file info, document properties
- **Text Extraction**: Clean text content from all document types
- **Knowledge Synthesis**: Same powerful Ollama models used for media
- **Batch Processing**: Process multiple documents efficiently
- **Progress Tracking**: Visual feedback during processing
- **Rich Output**: Colorful console display with detailed results
- **Structured Data**: JSON output for further processing

All document processing commands support the same options as media processing:
- `--prompt` or `-p`: Use specific prompt template
- `--custom-prompt` or `-c`: Use custom prompt text
- `--output` or `-o`: Save results to JSON file
- `--cloud`: Use cloud Ollama models
- `--quiet` or `-q`: Suppress detailed output

### Supported Document Libraries
- **PyMuPDF** (fitz): For PDF text extraction and metadata
- **ebooklib**: For EPUB content processing
- **mobi**: For MOBI document processing

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

**Documents**: `.pdf`, `.epub`, `.mobi` → `data/documents/`

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

These prompt templates work for extracting knowledge from both media (video/audio transcripts) and documents (PDF/EPUB/MOBI text):

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
| `anki_flashcards` | Generate structured flashcards for Anki integration (v2.5.0) |

All templates accept text content extracted from either:
- Media transcripts (video/audio processed through Whisper)
- Document text (PDF/EPUB/MOBI processed through document readers)

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

# Anki Integration Settings (v2.5.0)
ANKI_DEFAULT_DECK_NAME=Media_Knowledge_Deck
ANKI_CSS_TEMPLATE=default
ANKI_AUTO_TAG_SOURCE=true
ANKI_INCLUDE_TIMESTAMPS=true
ANKI_INCLUDE_EXAMPLES=true
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
┌─────────────────────┐
│   Input Sources     │
│  (Video/Audio/Docs) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Content Router    │
│  - Detect content   │
│  - Route to handler │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
┌─────────┐ ┌───────────────┐
│ Media   │ │ Documents     │
│ Handler │ │ Handler       │
└────┬────┘ └──────┬────────┘
     │             │
     ▼             ▼
┌─────────┐ ┌───────────────┐
│Preproces│ │Document Readers│
│ -Detect │ │ -PDF (PyMuPDF)│
│ -Extract│ │ -EPUB(ebooklib)│
│ -Convert│ │ -MOBI (mobi)  │
└────┬────┘ └──────┬────────┘
     │             │
     ▼             ▼
┌─────────┐ ┌───────────────┐
│Transcrib│ │ Text Extractor│
│ -Whisper│ │ -Clean text   │
│ -Chunks │ │ -Metadata     │
└────┬────┘ └──────┬────────┘
     │             │
     └──────┬──────┘
            ▼
    ┌───────────────┐
    │  Synthesizer  │
    │ -Ollama local │
    │ -Ollama cloud │
    │ -Prompt templates│
    │ -Anki adapter │
    └──────┬────────┘
           │
           ▼
    ┌───────────────┐
    │    Output     │
    │  - Console    │
    │  - JSON file  │
    │  - Markdown   │
    │  - Anki Deck  │
    └───────────────┘
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

#### 3. "Document format not supported" or "ImportError" with document libraries
**Solution:** Ensure document processing dependencies are installed:
```bash
# Reinstall document processing libraries
pip install PyMuPDF ebooklib mobi

# Check if libraries can be imported
python -c "import fitz; import ebooklib; import mobi; print('All document libraries OK')"
```

#### 4. "Failed to extract text from document"
**Solution:** This may occur with protected or corrupted files. Try:
- Verify the document file is not password-protected
- Ensure the file is not corrupted
- Check file permissions
- Try processing a different document file

#### 5. "Whisper model not found"
**Solution:** The model will download automatically on first run. Ensure you have internet connection and sufficient disk space.

#### 6. "Out of memory" during transcription
**Solution:** Use a smaller Whisper model:
```bash
# In .env file
WHISPER_MODEL_SIZE=tiny  # or base
```

#### 7. "Long file processing is slow"
**Solution:** This is expected for files >25 minutes. The system automatically chunks them. Consider using a smaller model for faster processing.

#### 8. "Cloud Ollama authentication failed"
**Solution:** Verify your API key and endpoint URL in `.env`. Note: The cloud endpoint is a placeholder and may need verification from official Ollama Cloud documentation.

#### 9. "Module not found" errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

#### 10. "Files not being processed after copying"
**Solution:** Use the `--process` flag to enable auto-processing:
```bash
python main.py scan --process
python main.py watch --process
```

#### 11. "Zero-byte files being skipped"
**Solution:** This is intentional - the system skips incomplete downloads. Wait for files to finish downloading before processing.

#### 12. "Watch mode not detecting new files"
**Solution:** Ensure files have completed downloading and are not zero bytes. Use `--interval` to adjust polling frequency.

#### 13. "Anki generation failed"
**Solution:** Anki integration libraries should be installed automatically. Check installation and JSON structure:
```bash
# Reinstall dependencies if needed
pip install -r requirements.txt

# Check that the synthesis JSON has proper structure
media-knowledge anki preview --input synthesis.json
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
📚 Anki: Generated 12 flashcards (.apkg file created)

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
- **Cloud Processing**: When using `--cloud`, your transcript or document text is sent to the cloud endpoint
- **Temporary Files**: Audio files are stored in `temp/` directory and can be deleted after processing
- **Document Privacy**: Document processing extracts text locally - sensitive documents remain on your machine unless using cloud processing
- **Anki Files**: Generated .apkg files contain only processed knowledge content

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

The output supports multiple formats:
- **Anki Integration**: Direct `.apkg` file generation for Anki import
- **Notion API**: JSON structure compatible with Notion database integration
- **Obsidian Plugins**: Markdown output for Obsidian knowledge bases
- **Database Systems**: Structured JSON for database ingestion
- **Web Applications**: REST API-ready JSON output

### Advanced Anki Workflow Examples
```bash
# Process lecture and generate flashcards automatically
media-knowledge process media --input lecture.mp4 --prompt anki_flashcards --output results.json
media-knowledge anki generate --input results.json --output lecture_cards.apkg

# Batch process YouTube playlist with Anki output
media-knowledge playlist process-playlist "playlist_url" --essay --anki-deck

# Create multiple themed decks from single processing session
media-knowledge anki generate --input synthesis.json --deck-name "Concepts" --type-specific
media-knowledge anki generate --input synthesis.json --deck-name "Q&A" --type-specific
```

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
- More output adapters (Notion, Obsidian, etc.)

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text
- [Ollama](https://ollama.ai) for local LLM inference
- [ffmpeg](https://ffmpeg.org) for media processing
- [genanki](https://github.com/kerrickstaley/genanki) for comprehensive Anki deck generation

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Configuration](#-configuration) guide
3. Open an issue on GitHub

---

**Note about Ollama Cloud**: The `OLLAMA_CLOUD_URL` endpoint is a placeholder. Please verify the correct endpoint from official Ollama Cloud documentation before using cloud features. The local Ollama integration is fully tested and recommended for most use cases.