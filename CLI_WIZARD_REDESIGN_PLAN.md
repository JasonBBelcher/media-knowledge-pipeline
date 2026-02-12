# Media Knowledge Pipeline CLI Wizard Redesign Plan

## Executive Summary

Based on comprehensive analysis, this document outlines a modern, modular replacement for the current CLI wizard system that solves all existing issues while preserving all functionality.

## Current Issues Identified

1. **Complexity Overload**: Multiple tightly-coupled wizard classes with duplicated logic
2. **Inconsistent UX**: Different workflows have different user experiences  
3. **Hardcoded Options**: Template lists aren't dynamically discovered
4. **Maintenance Nightmare**: Changes require touching multiple files
5. **Extensibility Challenges**: Adding features requires duplicating patterns
6. **Error Handling Gaps**: Inconsistent error messaging and recovery

## Current Functionality to Preserve

### CLI Commands Equivalents
- `media-knowledge process media --input URL --prompt TEMPLATE`
- `media-knowledge batch process-urls --urls file.txt --parallel N`  
- `media-knowledge document process file.pdf --prompt TEMPLATE`
- `media-knowledge anki generate --input results.json --deck-name NAME`
- `media-knowledge status`

### Processing Options
- Cloud/local processing selection
- Prompt template system (dynamic discovery)
- Output formats (JSON, markdown, both)
- Processing options (quiet, organize, etc.)
- Parallel processing for batch jobs

## Proposed Next-Gen Architecture

```
src/media_knowledge/cli/frontend/
├── main_menu.py              # Central menu router
├── command_executor.py       # Keep existing executor
├── shared/                   # Reusable utilities  
│   ├── input_validator.py    # Consistent validation
│   ├── user_prompter.py      # Standardized prompts
│   └── ...                   # Other shared components
└── workflows/                # Modular workflow plugins
    ├── base_workflow.py      # Common workflow patterns
    ├── media_workflow.py     # Media processing workflow
    ├── batch_workflow.py     # Batch processing workflow
    ├── document_workflow.py  # Document processing workflow
    └── anki_workflow.py      # Anki generation workflow
```

## Benefits of Redesign

- **Modularity**: Each workflow is independent, isolated component
- **Maintainability**: Changes to one workflow don't break others  
- **Extensibility**: New features follow established patterns
- **Consistency**: Unified UX across all workflows
- **Testability**: Each component can be unit tested independently
- **Reliability**: Centralized error handling and validation

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- Create shared utility modules
- Design central menu system with plugin architecture
- Establish base workflow class

### Phase 2: Core Workflows (Week 2)  
- Implement 4 core workflows (media, batch, document, anki)
- Ensure consistency with existing CLI flag equivalents
- Integrate with current command executor

### Phase 3: Integration (Week 3)
- Connect all components
- Comprehensive testing
- Performance optimization

## Key Architectural Principles

1. **Plugin Architecture**: Workflows plug into central system
2. **Shared Utilities**: Eliminate code duplication  
3. **Consistent Patterns**: Same UX everywhere
4. **Clear Boundaries**: Separate concerns clearly
5. **Easy Extension**: New features follow same patterns

This approach gives us a clean slate to build a robust, maintainable wizard system that solves all current issues while ensuring we can easily add new features in the future.