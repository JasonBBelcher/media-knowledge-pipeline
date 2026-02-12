# Anki Menu Enhancement Plan

## Overview
Plan to add Anki flashcard generation option to the interactive menu system in the legacy wizard interface.

## Current State
The new modular CLI wizard system (v2.6.0) already includes full Anki generation capabilities in `src/media_knowledge/cli/frontend/workflows/anki_workflow.py`. However, the legacy interactive menu system still needs the Anki option added.

## Goal
Add "Generate Anki Flashcards" as an option in the main interactive menu of the legacy system.

## Implementation Plan

### 1. Update Main Menu Options
**File**: `src/media_knowledge/cli/frontend/main_menu.py`
- Add "Generate Anki Flashcards" to the menu options array
- Update menu display to accommodate the new option
- Adjust numbering scheme for subsequent options

### 2. Add AnkiWizard Class
**File**: `src/media_knowledge/cli/frontend/anki_wizard.py`
- Create `AnkiWizard` class if it doesn't exist
- Implement `process_anki_interactive()` method
- Include:
  - JSON source file selection prompt
  - Deck name configuration prompt  
  - Preview vs generate decision prompt
  - Output directory selection prompt
  - Configuration building and validation

### 3. Integrate Anki Option in Interactive Frontend
**File**: `src/media_knowledge/cli/interactive.py`
- Import `AnkiWizard` class
- Add new elif clause for Anki menu option (likely choice #4)
- Implement interactive workflow:
  - Instantiate AnkiWizard
  - Call `process_anki_interactive()` method
  - Display configuration summary
  - Prompt for execution confirmation
  - Execute using command executor

### 4. Update Template Selection
**Files**: `src/media_knowledge/cli/frontend/media_wizard.py` and `src/media_knowledge/cli/frontend/batch_wizard.py`
- Add "Anki Flashcards (Generate study cards)" to template options
- Update numbering and mapping logic accordingly

## Implementation Steps

### Step 1: Create/Update AnkiWizard
```python
# In src/media_knowledge/cli/frontend/anki_wizard.py
class AnkiWizardError(Exception):
    pass

class AnkiWizard:
    def process_anki_interactive(self):
        # Implementation for interactive Anki generation
        pass
```

### Step 2: Update Main Menu
```python
# In src/media_knowledge/cli/frontend/main_menu.py
self.menu_options = [
    "Process Media Content  (Video/Audio/Document)",
    "Batch Process Multiple Items",
    "Create Essay from Existing Results",
    "Generate Anki Flashcards",  # New option
    "Scan Directory for Media Files",
    "Watch Directory for New Files", 
    "System Status and Requirements",
    "Show Pipeline Architecture",
    "Exit"
]
```

### Step 3: Update Interactive Frontend
```python
# In src/media_knowledge/cli/interactive.py
elif choice == 4:  # Generate Anki Flashcards
    print("\nGenerate Anki Flashcards Selected")
    anki_wizard = AnkiWizard()
    config = anki_wizard.process_anki_interactive()
    if config:
        # Display config and execute
```

## Testing Requirements

1. **Menu Navigation**: Verify Anki option appears correctly in menu
2. **Input Validation**: Test various JSON source file inputs
3. **Configuration Building**: Confirm proper config object creation
4. **Execution Flow**: Validate command executor integration
5. **Edge Cases**: Test cancellation, invalid inputs, missing files

## Backward Compatibility

- ✅ All existing menu options remain functional
- ✅ Existing CLI commands unchanged
- ✅ No breaking changes to current workflows
- ✅ Graceful handling of missing dependencies

## Timeline

- **Estimated Implementation**: 2-3 hours
- **Testing**: 1-2 hours
- **Documentation**: 30 minutes

## Success Criteria

1. Anki option appears in interactive menu as choice #4
2. Users can successfully navigate through Anki workflow
3. JSON files can be processed into Anki decks
4. Both preview and generate modes work correctly
5. All existing functionality remains intact
6. Proper error handling and user guidance provided
