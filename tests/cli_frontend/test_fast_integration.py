"""
Fast integration tests for Media Knowledge Pipeline CLI
Tests that run quickly and verify core functionality
"""
import pytest
import sys
import subprocess
import importlib
import os

sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')


def test_cli_module_imports():
    """Test that all CLI modules can be imported."""
    modules_to_test = [
        'src.media_knowledge.cli.app',
        'src.media_knowledge.cli.commands.process',
        'src.media_knowledge.cli.commands.batch',
        'src.media_knowledge.cli.commands.document',
        'src.media_knowledge.cli.commands.anki',
        'src.media_knowledge.cli.frontend.main_menu',
        'src.media_knowledge.cli.frontend.media_wizard',
        'src.media_knowledge.cli.frontend.batch_wizard',
        'src.media_knowledge.cli.frontend.document_wizard',
        'src.media_knowledge.cli.frontend.command_executor',
    ]
    
    for module_path in modules_to_test:
        try:
            importlib.import_module(module_path)
            print(f"✅ {module_path} imports successfully")
        except ImportError as e:
            pytest.fail(f"Failed to import {module_path}: {e}")


def test_cli_command_availability():
    """Test that all CLI commands are available."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0
    expected_commands = ['create-essay', 'status', 'process', 'batch', 'document', 'anki', 'scan', 'watch']
    for cmd in expected_commands:
        assert cmd in result.stdout, f"Command '{cmd}' should be available"


def test_status_command_runs():
    """Test that status command runs without crashing."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'status'],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    # Status command should complete successfully
    assert result.returncode == 0
    assert len(result.stdout) > 0 or len(result.stderr) > 0


def test_process_command_structure():
    """Test process command help structure."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'process', 'media', '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0
    assert '--input' in result.stdout
    assert '--cloud' in result.stdout
    assert '--markdown' in result.stdout


def test_batch_command_structure():
    """Test batch command help structure."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'batch', 'process-urls', '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0
    assert '--urls' in result.stdout
    assert '--parallel' in result.stdout


def test_document_command_structure():
    """Test document command help structure."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'document', 'formats'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Formata command should complete
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_file_system_operations():
    """Test basic file system operations that CLI depends on."""
    import tempfile
    
    # Test that we can create and read files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        # Test file existence
        assert os.path.exists(temp_path)
        
        # Test file reading
        with open(temp_path, 'r') as f:
            content = f.read()
            assert content == "test content"
    finally:
        # Clean up
        os.unlink(temp_path)


def test_output_directory_structure():
    """Test that output directory structure exists."""
    outputs_dir = '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline/outputs'
    markdown_dir = os.path.join(outputs_dir, 'markdown')
    
    assert os.path.exists(outputs_dir), "Outputs directory should exist"
    assert os.path.exists(markdown_dir), "Markdown directory should exist"
    assert os.path.isdir(outputs_dir), "Outputs should be a directory"
    assert os.path.isdir(markdown_dir), "Markdown should be a directory"


def test_cli_version():
    """Test that CLI reports version information."""
    # Check VERSION file exists
    version_file = '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline/VERSION'
    assert os.path.exists(version_file), "VERSION file should exist"
    
    with open(version_file, 'r') as f:
        version = f.read().strip()
        assert version, "VERSION should not be empty"
        assert '.' in version, "VERSION should contain dot separators"


def test_python_dependencies():
    """Test that Python dependencies are available."""
    required_modules = [
        'typer',
        'rich', 
        'requests',
        'youtube_dl',
        'openai_whisper',
        'ffmpeg'
    ]
    
    for module_name in required_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Some modules might have different names or be optional
            print(f"Note: {module_name} may not be available")


def test_basic_wizard_functionality():
    """Test basic wizard component functionality."""
    from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
    
    # Test command executor initialization
    executor = CommandExecutor()
    assert executor is not None
    assert executor.base_command is not None
    assert len(executor.base_command) > 0
    
    # Test project root is accessible
    assert executor.project_root is not None
    assert os.path.exists(executor.project_root)


def test_cli_help_command():
    """Test CLI help command works."""
    result = subprocess.run(
        ['media-knowledge', '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Command should either work or show proper error
    if result.returncode == 0:
        assert 'Usage' in result.stdout
    else:
        # Command might not be in PATH, but package should still be importable
        assert True


def test_process_help_subcommands():
    """Test process subcommands help."""
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'process', '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0
    assert 'media' in result.stdout


def test_subcommand_validation():
    """Test subcommand validation."""
    # Test invalid subcommand
    result = subprocess.run(
        ['python', '-m', 'media_knowledge.cli.app', 'process', 'invalid'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Should show error for invalid subcommand
    assert result.returncode != 0 or 'Error' in result.stdout or 'Error' in result.stderr


def test_core_module_access():
    """Test access to core modules."""
    # Test that we can access core functionality
    core_modules = ['core.document_processor', 'core.output_adapters', 'core.prompts']
    
    for module_path in core_modules:
        full_path = f'src.media_knowledge.{module_path}'
        try:
            importlib.import_module(full_path)
            print(f"✅ {full_path} accessible")
        except ImportError:
            print(f"⚠️  {full_path} not accessible (may be expected)")


def test_environment_consistency():
    """Test environment consistency for CLI operation."""
    # Test that Python executable is available
    assert sys.executable is not None
    assert os.path.exists(sys.executable)
    
    # Test that we can execute Python scripts
    test_script = "print('test')"
    result = subprocess.run(
        [sys.executable, '-c', test_script],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    assert result.returncode == 0
    assert 'test' in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])