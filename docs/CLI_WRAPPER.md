# CLI Wrapper Feature Documentation

## Overview
The CLI Wrapper introduces a user-friendly interface that abstracts away the complexity of Python virtual environments and command-line arguments, providing intuitive aliases for common operations.

## Goals
1. **Simplify Usage**: Remove virtual environment management overhead
2. **Intuitive Commands**: Natural language-like aliases
3. **Input Flexibility**: Support multiple URL formats
4. **Cross-Platform**: Work on macOS/Linux with proper shell detection
5. **Backward Compatible**: Maintain existing Python CLI functionality

## Implementation Components

### Core Files

#### 1. `mksynth` (Main Wrapper Script)
- **Location**: Project root
- **Purpose**: Main entry point that handles command translation
- **Features**:
  - Automatic virtual environment activation
  - Smart URL input parsing
  - Command translation to Python CLI
  - Error handling and help display

#### 2. `install.sh` (Installation Script)
- **Location**: Project root
- **Purpose**: Installs system-wide aliases
- **Features**:
  - Auto-detects shell (.zshrc vs .bashrc)
  - Backs up existing config
  - Creates aliases in shell startup files
  - Installation verification

#### 3. `uninstall.sh` (Uninstallation Script)
- **Location**: Project root
- **Purpose**: Removes installed aliases
- **Features**:
  - Clean removal of aliases
  - Backup restoration if needed

### Command Mapping

#### Primary Alias: `mksynth`

**Syntax:** `mksynth [options] <input>`

**Input Formats Supported:**
- **Single URL**: `mksynth "https://youtube.com/watch?v=..."`
- **Space-delimited URLs**: `mksynth "url1 url2 url3"`
- **Comma-delimited URLs**: `mksynth "url1,url2,url3"`
- **Playlist URLs**: `mksynth "https://youtube.com/playlist?list=..."`

**Examples:**
```bash
# Process single YouTube video
mksynth "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Process multiple videos (space-delimited)
mksynth "https://youtube.com/video1 https://youtube.com/video2"

# Process multiple videos (comma-delimited)
mksynth "https://youtube.com/video1,https://youtube.com/video2"

# Process playlist
mksynth "https://youtube.com/playlist?list=PL8dPuuaLjXtOAKed_MxxWBNaPno5h3Zs8"
```

#### Template-Specific Aliases

**Syntax:** `mksynth-<template> [options] <input>`

**Available Templates:**
- `mksynth-summary` - Uses 'basic_summary' template
- `mksynth-meeting` - Uses 'meeting_minutes' template
- `mksynth-lecture` - Uses 'lecture_summary' template
- `mksynth-tutorial` - Uses 'tutorial_guide' template
- `mksynth-project` - Uses 'project_update' template

**Examples:**
```bash
# Process with meeting template
mksynth-meeting "https://youtube.com/watch?v=..."

# Process playlist with lecture template
mksynth-lecture "https://youtube.com/playlist?list=..."
```

#### Advanced Commands

**Batch Processing:**
```bash
# Process URLs from file
mksynth batch --urls urls.txt

# Process with custom output directory
mksynth batch --urls urls.txt --output-dir my_results
```

**File Scanning:**
```bash
# Scan Downloads directory
mksynth scan

# Scan custom directory
mksynth scan --directory ~/Videos

# Scan with auto-processing
mksynth scan --process
```

### Installation Process

#### Automatic Installation
```bash
# Run installation script
./install.sh

# Installation will:
# 1. Detect shell type (bash/zsh)
# 2. Backup existing shell config
# 3. Add aliases to shell startup file
# 4. Verify installation
```

#### Manual Installation (Optional)
```bash
# Add to ~/.zshrc or ~/.bashrc
alias mksynth="/path/to/media-knowledge-pipeline/mksynth"
alias mksynth-summary="/path/to/media-knowledge-pipeline/mksynth summary"
alias mksynth-meeting="/path/to/media-knowledge-pipeline/mksynth meeting"
# ... additional aliases ...
```

### Configuration

#### Environment Variables
The wrapper respects existing `.env` configuration:
- `WHISPER_MODEL_SIZE`
- `OLLAMA_MODEL` 
- `DEFAULT_SYNTHESIS_PROMPT_TEMPLATE`

#### Wrapper-Specific Options
These can be set via command line or environment:
- `MKSYNTH_VERBOSE` - Enable verbose output
- `MKSYNTH_CACHE_DIR` - Custom cache directory
- `MKSYNTH_DEFAULT_PROMPT` - Default prompt template

### Technical Details

#### Virtual Environment Handling
The wrapper automatically:
1. Detects active virtual environment
2. If none active, activates `media_knowledge_env`
3. Runs Python commands within virtual environment
4. Deactivates environment when done

#### Input Parsing Logic
1. **Single URL Detection**: Checks if input matches URL pattern
2. **List Detection**: Splits by spaces/commas and validates each URL
3. **Playlist Detection**: Uses existing `is_youtube_playlist_url()` function
4. **File Detection**: Checks if input is file path

#### Error Handling
- **Invalid URLs**: Clear error messages with suggestions
- **Network Issues**: Retry logic with exponential backoff
- **Missing Dependencies**: Installation guidance
- **Permission Issues**: User-friendly permission error messages

### Usage Examples

#### Quick Start
```bash
# Install (one-time)
./install.sh

# Source your shell config
source ~/.zshrc  # or ~/.bashrc

# Use simplified commands
mksynth "https://youtube.com/watch?v=..."
mksynth "url1 url2 url3"
mksynth-meeting "https://youtube.com/playlist?list=..."
```

#### Advanced Usage
```bash
# Process with cloud Ollama
mksynth --cloud "https://youtube.com/watch?v=..."

# Process with custom output
mksynth --output result.json "https://youtube.com/watch?v=..."

# Process with quiet mode
mksynth --quiet "https://youtube.com/watch?v=..."

# Batch process with parallel processing
mksynth batch --urls urls.txt --parallel 4
```

### Migration from Current CLI

#### Before (Complex)
```bash
source media_knowledge_env/bin/activate
python main.py process --input "https://youtube.com/watch?v=..." --prompt meeting_minutes
```

#### After (Simple)
```bash
mksynth-meeting "https://youtube.com/watch?v=..."
```

### Testing Strategy

#### Manual Testing
- Verify alias installation
- Test various input formats
- Validate virtual environment handling
- Test error conditions

#### Automated Testing
- Unit tests for input parsing
- Integration tests for command translation
- Shell script testing framework

### Implementation Timeline

#### Phase 1: Core Wrapper
- `mksynth` script with basic functionality
- Virtual environment handling
- Basic command translation

#### Phase 2: Smart Parsing 
- URL list detection
- Playlist support
- File input handling

#### Phase 3: Shell Integration
- `install.sh` for alias installation
- Multiple shell support
- Installation verification

#### Phase 4: Enhanced UX
- Template-specific aliases
- Improved error handling
- Progress indicators

---

**Status**: Planned  
**Target Branch**: `feature/cli-wrapper`  
**Depends On**: `feature/youtube-playlist-support`