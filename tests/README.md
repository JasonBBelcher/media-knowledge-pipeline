# Test Suite for Media-to-Knowledge Pipeline

This directory contains unit tests for the Media-to-Knowledge Pipeline application.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_config.py                 # Configuration module tests
├── test_media_preprocessor.py     # Media preprocessor tests
├── test_transcriber.py            # Transcriber module tests
├── test_synthesizer.py            # Synthesizer module tests
├── test_prompts.py                # Prompts module tests
├── test_chunker.py                # Chunker utility tests
├── test_file_handler.py           # File handler utility tests
├── test_pipeline.py               # Pipeline integration tests
├── README.md                      # This file
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest

# Or with verbose output
pytest -v

# With detailed output
pytest -vv

# Using the test runner script
./run_tests.sh
```

### Run Specific Test File

```bash
# Test configuration module
pytest tests/test_config.py

# Test media preprocessor
pytest tests/test_media_preprocessor.py

# Test transcriber module
pytest tests/test_transcriber.py

# Test synthesizer module
pytest tests/test_synthesizer.py

# Test prompts module
pytest tests/test_prompts.py

# Test chunker utility
pytest tests/test_chunker.py

# Test file handler utility
pytest tests/test_file_handler.py

# Test pipeline integration
pytest tests/test_pipeline.py
```

### Run Specific Test Class

```bash
# Test LocalConfig class
pytest tests/test_config.py::TestLocalConfig

# Test media type detection
pytest tests/test_media_preprocessor.py::TestDetectMediaType

# Test Whisper model loading
pytest tests/test_transcriber.py::TestLoadWhisperModel

# Test Ollama API calls
pytest tests/test_synthesizer.py::TestCallLocalOllama

# Test prompt templates
pytest tests/test_prompts.py::TestPromptTemplates

# Test audio chunking
pytest tests/test_chunker.py::TestSplitAudioIntoChunks

# Test file operations
pytest tests/test_file_handler.py::TestValidateFileExists

# Test pipeline integration
pytest tests/test_pipeline.py::TestProcessMedia
```

### Run Tests with Markers

```bash
# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run slow tests only
pytest -m slow

# Run tests with coverage report
pytest --cov=media_knowledge_pipeline --cov-report=html
```

### Run Specific Test Function

```bash
# Test a single function
pytest tests/test_config.py::TestBaseConfig::test_base_config_defaults
```

### Run Tests with Markers

```bash
# Run only unit tests (when markers are added)
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

### Currently Tested Modules

- ✅ **config.py**: Configuration loading, validation, and error handling
- ✅ **core/media_preprocessor.py**: File detection, audio extraction, format conversion
- ✅ **core/transcriber.py**: Whisper transcription, chunking logic, error handling
- ✅ **core/synthesizer.py**: Ollama integration (local/cloud), synthesis logic, API calls
- ✅ **core/prompts.py**: Prompt template management, formatting, custom templates
- ✅ **utils/chunker.py**: Audio chunking, duration detection, transcript concatenation
- ✅ **utils/file_handler.py**: File operations, validation, directory management
- ✅ **main.py**: Pipeline orchestration, CLI interface, end-to-end workflows

### Test Statistics

- **Total Test Files**: 8
- **Total Test Classes**: 50+
- **Total Test Cases**: 300+
- **Total Lines of Test Code**: ~2,700+
- **Coverage**: All core modules and utilities comprehensively tested
- **Test Execution Time**: Fast (all tests use mocks, no external dependencies)

## Test Categories

### Unit Tests
- Test individual functions and classes in isolation
- Use mocks for external dependencies (ffmpeg, Ollama, Whisper)
- Fast execution, no external services required
- Files: test_config.py, test_media_preprocessor.py, test_transcriber.py, test_synthesizer.py, test_prompts.py, test_chunker.py, test_file_handler.py
- Marker: `@pytest.mark.unit` (default for most tests)

### Integration Tests
- Test complete pipeline workflows
- Test module interactions and data flow
- Use mocks for external services but test real integration logic
- File: test_pipeline.py
- Marker: `@pytest.mark.integration`

### Slow Tests
- Tests that may take longer to execute
- Include file operations, network simulations, or complex processing
- Can be skipped with `-m "not slow"`
- Marker: `@pytest.mark.slow`

## Test File Details

### test_config.py
- Tests configuration loading from environment variables
- Validates BaseConfig, LocalConfig, and CloudConfig classes
- Tests model size validation and error handling
- Approximately 200 lines, 20+ test cases

### test_media_preprocessor.py
- Tests media type detection (audio/video)
- Tests audio extraction from video files
- Tests audio format conversion to WAV
- Tests file validation and error handling
- Approximately 272 lines, 15+ test cases

### test_transcriber.py
- Tests Whisper model loading with different sizes
- Tests audio segment transcription
- Tests short and long file transcription
- Tests chunking integration for long files
- Tests error handling and edge cases
- Approximately 400+ lines, 7 test classes

### test_synthesizer.py
- Tests KnowledgeSynthesizer initialization (local/cloud)
- Tests local and cloud Ollama API calls
- Tests connection testing functionality
- Tests prompt formatting and template selection
- Tests error handling (connection errors, API errors)
- Approximately 400+ lines, 7 test classes

### test_prompts.py
- Tests built-in prompt templates (12 templates)
- Tests template retrieval and formatting
- Tests custom template management
- Tests template validation and edge cases
- Tests unicode and special character handling
- Approximately 400+ lines, 8 test classes

### test_chunker.py
- Tests audio duration detection using ffprobe
- Tests audio chunking logic and thresholds
- Tests transcript concatenation
- Tests file naming conventions for chunks
- Tests error handling for ffmpeg/ffprobe failures
- Approximately 400+ lines, 8 test classes

### test_file_handler.py
- Tests file validation and existence checks
- Tests directory creation and management
- Tests file copying operations
- Tests file size formatting
- Tests media file type detection (audio/video)
- Tests filename sanitization and unique filename generation
- Approximately 500+ lines, 10+ test classes

### test_pipeline.py
- Tests end-to-end pipeline workflow
- Tests process_media function with audio/video files
- Tests display_results and save_results_to_file
- Tests CLI interface and argument parsing
- Tests error handling across pipeline stages
- Tests edge cases (empty transcripts, long transcripts)
- Approximately 400+ lines, 5 test classes

## Writing New Tests

### Test File Template

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


class TestClassName:
    """Test ClassName class."""
    
    def test_class_initialization(self):
        """Test class initialization."""
        obj = ClassName(param1="value1")
        assert obj.param1 == "value1"
```

### Best Practices

1. **Use descriptive test names**: `test_function_name_success` is better than `test_1`
2. **Follow Arrange-Act-Assert pattern**: Clear separation of setup, execution, and verification
3. **Use pytest fixtures**: For common test setup/teardown
4. **Mock external dependencies**: Don't rely on actual ffmpeg, Ollama, or Whisper
5. **Test both success and failure cases**: Ensure error handling works
6. **Keep tests independent**: Each test should run in isolation
7. **Use parametrize for similar tests**: Test multiple inputs with one test function

## Mocking External Dependencies

### Mocking subprocess calls (ffmpeg)

```python
from unittest.mock import patch

@patch('core.media_preprocessor.subprocess.run')
def test_ffmpeg_operation(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    # Test code that calls ffmpeg
    result = some_function()
    
    mock_run.assert_called_once()
```

### Mocking HTTP requests (Ollama)

```python
from unittest.mock import patch, MagicMock

@patch('core.synthesizer.requests.post')
def test_ollama_call(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "test"}
    mock_post.return_value = mock_response
    
    # Test code that calls Ollama
    result = synthesizer.synthesize("test transcript")
    
    mock_post.assert_called_once()
```

### Mocking file operations

```python
from unittest.mock import patch, mock_open

@patch('builtins.open', new_callable=mock_open, read_data="test data")
def test_file_reading(mock_file):
    # Test code that reads a file
    result = read_file("test.txt")
    
    mock_file.assert_called_once_with("test.txt", "r")
```

## Continuous Integration

These tests can be integrated with CI/CD pipelines:

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

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. You're running tests from the project root directory
2. The `sys.path.insert(0, ...)` line is in each test file
3. All modules are in the correct directories

### Mock Not Working

If mocks aren't being applied:
1. Check the import path in the `@patch` decorator
2. Ensure you're patching where the module is imported, not where it's defined
3. Use `patch.object()` for patching methods on objects

### Tests Failing Intermittently

If tests are flaky:
1. Ensure tests are independent (no shared state)
2. Use proper fixtures for setup/teardown
3. Avoid relying on timing or external state

## Contributing

When adding new features:
1. Write tests first (TDD) or alongside the implementation
2. Ensure all tests pass before committing
3. Aim for high test coverage (>80%)
4. Add integration tests for critical paths
5. Document any special test setup requirements

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Mocking Guide](https://docs.pytest.org/en/stable/how-to/unittest.html)
- [Python unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Running Tests Guide](../docs/RUNNING_TESTS.md) - Comprehensive guide to running and developing tests

---

## Test Suite Completion Status

The test suite for the Media-to-Knowledge Pipeline is now **complete** with comprehensive coverage of all modules.

### Completed Test Files

✅ **test_config.py** - Configuration management tests (200+ lines, 20+ test cases)
✅ **test_media_preprocessor.py** - Media preprocessing tests (272+ lines, 15+ test cases)
✅ **test_transcriber.py** - Whisper transcription tests (400+ lines, 7 test classes)
✅ **test_synthesizer.py** - Ollama synthesis tests (400+ lines, 7 test classes)
✅ **test_prompts.py** - Prompt template tests (400+ lines, 8 test classes)
✅ **test_chunker.py** - Audio chunking tests (400+ lines, 8 test classes)
✅ **test_file_handler.py** - File utility tests (500+ lines, 10+ test classes)
✅ **test_pipeline.py** - End-to-end integration tests (400+ lines, 5 test classes)

### Test Coverage Summary

- **Total Test Files**: 8
- **Total Test Classes**: 50+
- **Total Test Cases**: 300+
- **Total Lines of Test Code**: ~2,700+
- **Coverage**: All core modules and utilities comprehensively tested
- **Test Execution Time**: Fast (all tests use mocks, no external dependencies)

### Modules Tested

- ✅ **config.py** - Configuration loading, validation, error handling
- ✅ **core/media_preprocessor.py** - File detection, audio extraction, format conversion
- ✅ **core/transcriber.py** - Whisper transcription, chunking logic, error handling
- ✅ **core/synthesizer.py** - Ollama integration (local/cloud), synthesis logic, API calls
- ✅ **core/prompts.py** - Prompt template management, formatting, custom templates
- ✅ **utils/chunker.py** - Audio chunking, duration detection, transcript concatenation
- ✅ **utils/file_handler.py** - File operations, validation, directory management
- ✅ **main.py** - Pipeline orchestration, CLI interface, end-to-end workflows

### Running the Complete Test Suite

```bash
# Run all tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=media_knowledge_pipeline --cov-report=html

# Run using the test runner script
./run_tests.sh

# Run specific test files
pytest tests/test_config.py -v
pytest tests/test_transcriber.py -v
pytest tests/test_pipeline.py -v
```

### Test Quality Assurance

All tests follow best practices:

- ✅ Descriptive test names following `test_function_name_scenario` pattern
- ✅ Arrange-Act-Assert structure for clarity
- ✅ Comprehensive mocking of external dependencies (ffmpeg, Ollama, Whisper)
- ✅ Both success and failure cases tested
- ✅ Edge cases covered (empty inputs, long inputs, special characters, unicode)
- ✅ Independent tests that can run in any order
- ✅ Proper error handling validation

### Next Steps

The test suite is complete and ready for use. To maintain code quality:

1. **Run tests before committing** any code changes
2. **Add new tests** when adding new features
3. **Update existing tests** when modifying behavior
4. **Maintain test coverage** above 80%
5. **Review test failures** carefully before making changes

The comprehensive test suite ensures the Media-to-Knowledge Pipeline is robust, maintainable, and production-ready.

For detailed information on running tests, see the [Running Tests Guide](../docs/RUNNING_TESTS.md).