# Markdown Output Feature

## Overview

The Media-to-Knowledge Pipeline now includes enhanced functionality to export synthesized knowledge as markdown files with descriptive filenames automatically generated from the content.

## Features

1. **Automated Filename Generation**: Creates descriptive filenames based on the first line of the synthesized content
2. **Flexible Output Options**: Save only markdown, only JSON, or both formats simultaneously
3. **Clean File Names**: Automatically sanitizes filenames to remove special characters and ensure compatibility
4. **Rich Metadata**: Includes source information, processing time, transcript length, and model used

## Usage Examples

### Save Only Markdown Output
```bash
python main.py --input meeting.mp4 --markdown
```

### Save Both JSON and Markdown
```bash
python main.py --input meeting.mp4 --output meeting_summary.json --markdown
```

### Specify Custom Markdown Directory
```bash
python main.py --input meeting.mp4 --markdown /path/to/markdown/files
```

## Implementation Details

The markdown export functionality is implemented in the `save_synthesis_to_markdown()` function in `main.py`:

1. Extracts the synthesized text from the results
2. Generates a filename from the first line of the synthesis (limited to 50 characters)
3. Sanitizes the filename to remove special characters
4. Creates a markdown document with:
   - Title based on the synthesis subject
   - Source information section
   - Full synthesized knowledge content
   - Generated-by footer

## Edge Case Handling

The implementation handles several edge cases:

1. Empty or whitespace-only subjects
2. Special characters in filenames
3. Very long subject lines (truncated to 50 characters)
4. Missing synthesis content

## Benefits

1. **Easy Content Organization**: Automatically named files make it easy to organize and find specific syntheses
2. **Human-Readable Format**: Markdown format is ideal for reading, sharing, and further editing
3. **Metadata Preservation**: Important processing information is preserved in the output
4. **Flexible Integration**: Works seamlessly with existing JSON output functionality