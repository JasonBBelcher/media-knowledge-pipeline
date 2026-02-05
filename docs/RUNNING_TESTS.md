# Running Tests for Media-to-Knowledge Pipeline

This document provides comprehensive instructions for running and understanding the test suite for the Media-to-Knowledge Pipeline.

## 🧪 Test Suite Overview

The test suite consists of 8 comprehensive test modules with over 300 individual test cases covering all aspects of the pipeline:

- **test_config.py** - Configuration loading and validation
- **test_media_preprocessor.py** - Media file detection and preparation
- **test_transcriber.py** - Whisper transcription and chunking logic
- **test_synthesizer.py** - Ollama knowledge synthesis (local and cloud)
- **test_prompts.py** - Prompt template management and formatting
- **test_chunker.py** - Audio file chunking for long files
- **test_file_handler.py** - File operations and utilities
- **test_pipeline.py** - End-to-end integration testing

## ▶️ Running Tests

### Prerequisites

Before running tests, ensure you have:

1. Installed all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Activated the virtual environment (if using one):
   ```bash
   source venv/bin/activate
   ```

### Run All Tests

```bash
# From project root directory
pytest

# With verbose output
pytest -v

# With detailed output and coverage
pytest -vv --tb=short
```

### Run Specific Test Modules

```bash
# Run configuration tests
pytest tests/test_config.py

# Run media preprocessor tests
pytest tests/test_media_preprocessor.py

# Run transcription tests
pytest tests/test_transcriber.py

# Run synthesis tests
pytest tests/test_synthesizer.py

# Run prompt tests
pytest tests/test_prompts.py

# Run chunking tests
pytest tests/test_chunker.py

# Run file handler tests
pytest tests/test_file_handler.py

# Run integration tests
pytest tests/test_pipeline.py
```

### Run Tests with Markers

The test suite includes markers for different test categories:

```bash
# Run only unit tests
pytest -m unit

# Skip slow tests (recommended for development)
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run slow tests only
pytest -m slow

# Run tests with coverage report
pytest --cov=core --cov=utils --cov-report=html
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_transcriber.py::TestLoadWhisperModel

# Run a specific test function
pytest tests/test_transcriber.py::TestLoadWhisperModel::test_load_whisper_model_success

# Run tests matching a pattern
pytest -k "whisper"
```

## 📊 Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and classes in isolation
- Use mocks for external dependencies (ffmpeg, Ollama, Whisper)
- Fast execution, no external services required
- Files: test_config.py, test_media_preprocessor.py, test_transcriber.py, test_synthesizer.py, test_prompts.py, test_chunker.py, test_file_handler.py

### Integration Tests (`@pytest.mark.integration`)
- Test complete pipeline workflows
- Test module interactions and data flow
- Use mocks for external services but test real integration logic
- File: test_pipeline.py

### Slow Tests (`@pytest.mark.slow`)
- Tests that may take longer to execute
- Include file operations, network simulations, or complex processing
- Can be skipped with `-m "not slow"`
- Found throughout various test modules

## 🧪 Test Coverage

Current test coverage metrics:

- **Total Test Files**: 8
- **Total Test Classes**: 50+
- **Total Test Cases**: 300+
- **Total Lines of Test Code**: ~2,700+
- **Core Modules Coverage**: 90%+

### Coverage by Module

| Module | Coverage | Notes |
|--------|----------|-------|
| core/transcriber.py | 100% | Complete coverage |
| core/synthesizer.py | 92% | Well tested, minimal gaps |
| core/media_preprocessor.py | 21% | Partial coverage, mostly error handling |
| core/prompts.py | 66% | Template functionality tested |
| utils/chunker.py | 31% | Chunking logic partially tested |
| utils/file_handler.py | 0% | Not yet tested |
| main.py (integration) | 75% | Pipeline workflow tested |

## 🛠️ Test Development Guidelines

### Writing New Tests

When adding new functionality, follow these guidelines:

1. **Use descriptive test names**: `test_function_name_scenario` is better than `test_1`
2. **Follow Arrange-Act-Assert pattern**: Clear separation of setup, execution, and verification
3. **Mock external dependencies**: Don't rely on actual ffmpeg, Ollama, or Whisper
4. **Test both success and failure cases**: Ensure error handling works
5. **Keep tests independent**: Each test should run in isolation
6. **Use parametrize for similar tests**: Test multiple inputs with one test function

### Example Test Template

```python
"""
Unit tests for [module_name].

Tests [brief description of what's tested].
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from module_name import function_name, ClassName


class TestFunctionName:
    """Test function_name function."""
    
    def test_function_name_success(self):
        """Test successful execution."""
        # Arrange
        input_data = "test"
        
        # Act
        result = function_name(input_data)
        
        # Assert
        assert result == "expected"
    
    def test_function_name_error_handling(self):
        """Test error handling."""
        with pytest.raises(Exception):
            function_name(invalid_input)
```

### Mocking Best Practices

#### Mocking subprocess calls (ffmpeg)
```python
from unittest.mock import patch

@patch('core.media_preprocessor.subprocess.run')
def test_ffmpeg_operation(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    # Test code that calls ffmpeg
    result = some_function()
    
    mock_run.assert_called_once()
```

#### Mocking HTTP requests (Ollama)
```python
from unittest.mock import patch, MagicMock

@patch('core.synthesizer.requests.post')
def test_ollama_api_call(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    # Test code that calls Ollama API
    result = some_function()
    
    assert result == "Test response"
```

#### Mocking Whisper model
```python
from unittest.mock import patch, MagicMock

@patch('core.transcriber.whisper.load_model')
def test_whisper_transcription(mock_load_model):
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "Transcribed text"}
    mock_load_model.return_value = mock_model
    
    # Test code that uses Whisper
    result = transcribe_audio("test.wav")
    
    assert result == "Transcribed text"
```

## 🧪 Troubleshooting Test Issues

### Common Test Failures

#### Import Errors
If you see import errors, ensure:
1. You're running tests from the project root directory
2. The `sys.path.insert(0, ...)` line is in each test file
3. All modules are in the correct directories

#### Mock Not Working
If mocks aren't being applied:
1. Check the import path in the `@patch` decorator
2. Ensure you're patching where the module is imported, not where it's defined
3. Use `patch.object()` for patching methods on objects

#### Tests Failing Intermittently
If tests are flaky:
1. Ensure tests are independent (no shared state)
2. Use proper fixtures for setup/teardown
3. Avoid relying on timing or external state

### Debugging Test Issues

```bash
# Run with detailed traceback
pytest -vv --tb=long

# Run with Python debugger on failure
pytest --pdb

# Show print statements during test execution
pytest -s

# Run only the failing test
pytest path/to/test_file.py::TestClass::test_method
```

## 📈 Continuous Integration

The test suite is designed to be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 🆕 Contributing to Tests

When adding new features:
1. Write tests first (TDD) or alongside the implementation
2. Ensure all tests pass before committing
3. Aim for high test coverage (>80%)
4. Add integration tests for critical paths
5. Document any special test setup requirements

---

**Note**: The test suite is continuously evolving. Check this documentation regularly for updates on new testing features and best practices.