# Media Knowledge Pipeline CLI Wizard Redesign

## Overview

This directory contains the implementation of the redesigned CLI Wizard System for the Media Knowledge Pipeline. The new system replaces the complex, tightly-coupled legacy wizard architecture with a modular, maintainable design while preserving all existing functionality.

## Key Features

1. **Modular Architecture**: Each workflow is an independent module that can be developed and tested separately
2. **Shared Utilities**: Common functionality reused across all workflows
3. **Consistent User Experience**: Uniform interface across all processing types
4. **Backward Compatibility**: All existing CLI commands continue to work unchanged
5. **Easy Extension**: New features follow established patterns

## Directory Structure

```
src/media_knowledge/cli/frontend/
├── main_menu_v2.py              # Central menu router (new)
├── launcher_v2.py               # Entry point for new system (new)
├── command_executor.py          # Existing command executor (preserved)
├── shared/                      # Reusable utilities (new)
│   ├── input_validator.py       # Input validation functions
│   └── user_prompter.py         # Standardized user prompts
└── workflows/                   # Modular workflow plugins (new)
    ├── base_workflow.py         # Common workflow patterns
    ├── media_workflow.py        # Media processing workflow
    ├── batch_workflow.py        # Batch processing workflow
    ├── document_workflow.py     # Document processing workflow
    └── anki_workflow.py         # Anki generation workflow
```

## Components

### Shared Utilities

- **input_validator.py**: Validates YouTube URLs, file paths, numbers, and file formats
- **user_prompter.py**: Provides standardized user input prompts with consistent error handling

### Base Workflow

- **base_workflow.py**: Abstract base class that provides common functionality for all workflows including configuration management, execution flow, and cleanup

### Workflow Modules

1. **Media Processing** (`media_workflow.py`): Handles YouTube videos and local audio/video files
2. **Batch Processing** (`batch_workflow.py`): Processes multiple URLs from a file
3. **Document Processing** (`document_workflow.py`): Processes PDF, EPUB, and MOBI documents
4. **Anki Generation** (`anki_workflow.py`): Creates flashcards from JSON results

### Main Menu System

- **main_menu_v2.py**: Central routing system that connects users to appropriate workflows
- **launcher_v2.py**: Entry point for the new wizard system

## Usage

To launch the new wizard system:

```bash
python -m src.media_knowledge.cli.frontend.launcher_v2
```

Or if integrated into the main CLI:

```bash
media-knowledge-launch-v2
```

## Backward Compatibility

All existing CLI commands remain fully functional:

- `media-knowledge process media --input URL --prompt TEMPLATE`
- `media-knowledge batch process-urls --urls file.txt --parallel N`
- `media-knowledge document process file.pdf --prompt TEMPLATE`
- `media-knowledge anki generate --input results.json --deck-name NAME`

## Migration Strategy

During the transition period:
1. Both old and new systems operate simultaneously
2. Users can choose which system to use
3. New system gradually becomes default
4. Legacy system available via explicit opt-in during transition

## Testing

All components include comprehensive unit tests:
- Shared utilities: input validation and user prompting
- Base workflow class: configuration management and execution flow
- Individual workflows: specific functionality for each processing type
- Integration tests: backward compatibility with CLI commands
- Workflow integration: end-to-end workflow testing

Run all tests with:

```bash
cd tests/cli_frontend
python -m pytest *.py -v
```

## Future Extensibility

Adding new workflows follows the established pattern:
1. Create new workflow module inheriting from BaseWorkflow
2. Implement required methods (run, execute)
3. Register with main menu
4. Add any new shared utilities if needed
5. Test thoroughly

This approach ensures clean separation of concerns while maintaining the flexibility to extend functionality as needed.