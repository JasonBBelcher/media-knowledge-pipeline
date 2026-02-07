# Batch YouTube URL Processing Feature

## Overview
This feature adds support for processing multiple YouTube URLs in batch mode, allowing users to efficiently process large collections of videos through the media-to-knowledge pipeline.

## New Command
```bash
python main.py batch --urls youtube_urls.txt --markdown outputs/markdown
```

## Features

### 1. Multiple Input Sources
- Process YouTube URLs from a text file (one URL per line)
- Automatically filters for valid YouTube URLs
- Ignores blank lines and comments (lines starting with #)

### 2. Processing Modes
- **Sequential Processing**: Process URLs one at a time (default)
- **Parallel Processing**: Process multiple URLs simultaneously using `--parallel N`

### 3. Intelligent Output Naming
- All outputs use the same LLM-based intelligent naming system
- JSON and markdown files get descriptive, content-based names
- Automatic deduplication with timestamp suffixes when needed

### 4. Comprehensive Monitoring
- Progress tracking for each URL
- Detailed success/failure reporting
- Overall statistics and success rates
- Quiet mode for minimal output (`--quiet`)

## Usage Examples

### Basic Batch Processing
```bash
# Create a file with YouTube URLs (one per line)
echo -e "https://youtu.be/video1\nhttps://www.youtube.com/watch?v=video2" > urls.txt

# Process all URLs
python main.py batch --urls urls.txt
```

### Advanced Options
```bash
# Parallel processing with 3 workers
python main.py batch --urls urls.txt --parallel 3

# Save outputs to custom directories
python main.py batch --urls urls.txt --output-dir results --markdown markdown_output

# Use cloud Ollama and custom prompt
python main.py batch --urls urls.txt --cloud --prompt meeting_minutes

# Minimal output
python main.py batch --urls urls.txt --quiet
```

## File Format
Create a text file with YouTube URLs:

```
# My YouTube Collection
https://www.youtube.com/watch?v=video1
https://youtu.be/video2
https://www.youtube.com/watch?v=video3

# More videos to process later
# https://www.youtube.com/watch?v=skipped_video
```

## Output Structure
- **JSON Results**: `outputs/{intelligent_name}_results.json`
- **Markdown Synthesis**: `outputs/markdown/{intelligent_name}.md`

## Error Handling
- Individual URL failures don't stop the entire batch
- Clear error messages for each failed URL
- Summary report showing success/failure counts
- Exit codes indicate overall success (0) or partial failure (1)

## Performance Benefits
- Process large collections without manual intervention
- Parallel processing speeds up throughput
- Consistent output naming for easy organization
- Progress tracking for long-running operations

## Integration
This feature builds on existing YouTube streaming capabilities:
- Direct audio streaming (no full video downloads)
- Seamless integration with existing pipeline
- Same quality intelligent naming system
- Compatible with all existing prompt templates

The batch processing feature enables users to efficiently process YouTube playlists, channels, or curated collections of videos with minimal effort.