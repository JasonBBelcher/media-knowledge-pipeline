# Media Knowledge Pipeline CLI Wizard Architecture

## Overview

This document describes the proposed architecture for the redesigned CLI wizard system, providing detailed specifications for each component.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                         │
├─────────────────────────────────────────────────────────────┤
│                    main_menu.py                             │
│              (Central Menu Router)                          │
├─────────────────────────────────────────────────────────────┤
│  Workflows          │  Shared Utilities    │  Executors     │
│                     │                      │                │
│  media_workflow.py  │  input_validator.py  │ command_       │
│  batch_workflow.py  │  user_prompter.py    │ executor.py    │
│  document_workflow.py │ config_manager.py  │                │
│  anki_workflow.py   │  error_handler.py    │                │
└─────────────────────────────────────────────────────────────┘
```

## Component Specifications

### Main Menu System (`main_menu.py`)

**Responsibility**: Central routing and navigation

**Functions**:
- Display main menu options
- Route user to appropriate workflow modules
- Handle application exit and navigation
- Provide help and guidance

**Interface**:
```python
class MainMenu:
    def display_menu(self) -> None:
        """Display the main menu options"""
    
    def get_user_choice(self) -> int:
        """Get and validate user menu choice"""
    
    def route_to_workflow(self, choice: int) -> None:
        """Route user to selected workflow"""
```

### Base Workflow Class (`base_workflow.py`)

**Responsibility**: Common functionality for all workflows

**Features**:
- Standardized workflow lifecycle
- Shared utility integration
- Common state management
- Error handling patterns

### Workflow Modules

#### Media Processing Workflow (`media_workflow.py`)

**Steps**:
1. Input Selection (YouTube URL or local file)
2. Template Selection (dynamic from available prompts)
3. Processing Options (cloud, quiet, organize)
4. Output Options (JSON, markdown, both, none)
5. Review & Confirm
6. Execute

**Key Methods**:
```python
class MediaWorkflow(BaseWorkflow):
    def select_input_type(self) -> str:
        """Select YouTube or local file input"""
    
    def get_media_input(self) -> str:
        """Get and validate media input"""
    
    def select_template(self) -> str:
        """Select processing template"""
    
    def get_processing_options(self) -> Dict:
        """Get processing options"""
    
    def get_output_options(self) -> Dict:
        """Get output options"""
    
    def confirm_and_execute(self) -> bool:
        """Review configuration and execute"""
```

#### Batch Processing Workflow (`batch_workflow.py`)

**Steps**:
1. URLs File Selection (validate file exists)
2. Parallel Workers Configuration (1-8 range)
3. Template Selection (dynamic)
4. Essay Generation Options
5. Processing Options (cloud, quiet, organize)
6. Output Directory Selection
7. Review & Confirm
8. Execute

#### Document Processing Workflow (`document_workflow.py`)

**Steps**:
1. Document File Selection (PDF/EPUB/MOBI)
2. Template Selection (dynamic)
3. Processing Options (cloud, quiet, organize)
4. Output Options
5. Review & Confirm
6. Execute

#### Anki Generation Workflow (`anki_workflow.py`)

**Steps**:
1. JSON Source Selection
2. Deck Name Configuration
3. Preview vs Generate Decision
4. Output Directory Selection
5. Review & Confirm
6. Execute

### Shared Utilities

#### Input Validator (`input_validator.py`)

**Functions**:
- URL validation (YouTube, generic)
- File path validation  
- Number range validation
- File format validation

#### User Prompter (`user_prompter.py`)

**Functions**:
- Standardized input prompts
- Retry and cancellation handling
- Help and guidance delivery
- Consistent error messaging

#### Configuration Manager (`config_manager.py`)

**Functions**:
- State persistence between workflow steps
- Session management
- Default value handling
- User preference storage

#### Error Handler (`error_handler.py`)

**Functions**:
- Consistent error messaging
- Recovery suggestions
- Logging integration
- User-friendly error display

## Integration Points

### Command Executor Integration

All workflows integrate with the existing `command_executor.py` to maintain CLI compatibility:

```python
# Example integration pattern
executor = CommandExecutor()
success = executor.execute_media_processing(config)
```

### Template Discovery Integration

Workflows use dynamic template discovery:

```python
from shared.template_discovery import get_available_templates

templates = get_available_templates()
# Display templates to user
```

## Data Flow

```
User Input → Workflow Module → Configuration Builder → 
Command Executor → CLI Command → Processing Pipeline → 
Output Files
```

## Error Handling Strategy

1. **Validation Errors**: Caught at input collection stage
2. **Execution Errors**: Handled by command executor  
3. **System Errors**: Managed by centralized error handler
4. **User Cancellation**: Graceful workflow termination

## Testing Strategy

### Unit Tests
- Each workflow module independently testable
- Shared utilities fully unit tested
- Input validators exhaustively tested

### Integration Tests  
- CLI command equivalence testing
- End-to-end workflow testing
- Error condition testing

### User Acceptance Tests
- Complete user journey validation
- UX consistency verification
- Performance benchmarking

## Migration Strategy

### Backward Compatibility
- Existing CLI commands unchanged
- All current functionality preserved
- No breaking changes to user experience

### Transition Phases
1. **Parallel Operation**: New and old systems coexist
2. **Gradual Migration**: Users migrate naturally
3. **Complete Replacement**: Old system deprecated

## Future Extensibility

### New Workflows
Adding new workflows follows established pattern:
1. Create new workflow module
2. Register with main menu
3. Integrate with shared utilities
4. Test and deploy

### Feature Extensions
Adding features to existing workflows:
1. Extend base workflow if applicable
2. Add to specific workflow module
3. Utilize shared utilities
4. Maintain consistency patterns