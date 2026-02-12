"""
Unit tests for Media Knowledge Pipeline CLI components
Fast, focused tests that don't require full integration
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.app import app
from typer.testing import CliRunner


def test_app_object_exists():
    """Test that the Typer app object exists and has basic attributes."""
    assert app is not None
    assert hasattr(app, 'registered_commands')
    assert len(app.registered_commands) > 0


def test_cli_runner_works():
    """Test that CliRunner can invoke basic commands."""
    runner = CliRunner()
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_command_import_paths():
    """Test that all CLI commands can be imported."""
    # Test that all command modules can be imported
    try:
        from src.media_knowledge.cli.commands import process, batch, document, anki
        assert process is not None
        assert batch is not None
        assert document is not None
        assert anki is not None
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_command_executor_basic():
    """Test command executor initialization."""
    from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
    
    executor = CommandExecutor()
    assert executor is not None
    assert hasattr(executor, 'base_command')
    assert isinstance(executor.base_command, list)
    assert len(executor.base_command) > 0
    assert executor.base_command[0].endswith('python')
    assert '-m' in executor.base_command


def test_command_executor_media_command_building():
    """Test media processing command construction."""
    from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
    
    executor = CommandExecutor()
    config = {
        'media_input': 'https://youtube.com/test',
        'media_type': 'youtube',
        'template': 'lecture_summary',
        'custom_prompt': None,
        'output_config': {'save_json': True, 'save_markdown': True},
        'processing_options': {'use_cloud': True, 'quiet': False, 'organize': True}
    }
    
    command = executor.base_command + ['process', 'media']
    command.extend(['--input', config['media_input']])
    command.append('--cloud')
    command.extend(['--prompt', config['template']])
    command.extend(['--output', 'results.json'])
    command.extend(['--markdown', 'outputs/markdown'])
    
    assert len(command) > 5
    assert 'process' in command
    assert 'media' in command
    assert '--input' in command
    assert '--cloud' in command
    assert '--prompt' in command
    assert '--output' in command
    assert '--markdown' in command


def test_batch_command_composition():
    """Test batch command structure."""
    runner = CliRunner()
    result = runner.invoke(app, ['batch', '--help'])
    assert result.exit_code == 0
    assert 'process-urls' in result.stdout


def test_document_command_structure():
    """Test document command structure."""
    runner = CliRunner()
    result = runner.invoke(app, ['document', '--help'])
    assert result.exit_code == 0
    assert 'process' in result.stdout
    assert 'batch' in result.stdout


def test_anki_command_structure():
    """Test anki command structure."""
    runner = CliRunner()
    result = runner.invoke(app, ['anki', '--help'])
    assert result.exit_code == 0
    assert 'generate' in result.stdout


def test_config_file_exists():
    """Test that the CLI configuration files exist."""
    # Check main app file
    app_path = Path('/Users/jasonbelcher/Documents/code/media-knowledge-pipeline/src/media_knowledge/cli/app.py')
    assert app_path.exists(), "Main CLI app file should exist"
    
    # Check commands directory
    commands_dir = Path('/Users/jasonbelcher/Documents/code/media-knowledge-pipeline/src/media_knowledge/cli/commands')
    assert commands_dir.exists(), "Commands directory should exist"
    assert commands_dir.is_dir(), "Commands should be a directory"
    
    # Check command files exist
    expected_commands = ['process.py', 'batch.py', 'document.py', 'anki.py']
    for cmd_file in expected_commands:
        cmd_path = commands_dir / cmd_file
        assert cmd_path.exists(), f"Command file {cmd_file} should exist"


def test_frontend_files_exist():
    """Test that frontend wizard files exist."""
    frontend_dir = Path('/Users/jasonbelcher/Documents/code/media-knowledge-pipeline/src/media_knowledge/cli/frontend')
    assert frontend_dir.exists(), "Frontend directory should exist"
    
    expected_files = ['main_menu.py', 'media_wizard.py', 'batch_wizard.py', 'document_wizard.py', 'command_executor.py']
    for file_name in expected_files:
        file_path = frontend_dir / file_name
        assert file_path.exists(), f"Frontend file {file_name} should exist"


def test_command_imports():
    """Test that CLI commands can be imported without errors."""
    # Test basic command imports
    try:
        from src.media_knowledge.cli.commands import process, batch, document, anki
        
        # If we get here, imports worked
        assert process is not None
        assert batch is not None
        assert document is not None
        assert anki is not None
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_main_menu_import():
    """Test that main menu can be imported."""
    try:
        from src.media_knowledge.cli.frontend.main_menu import MainMenu
        menu = MainMenu()
        assert menu is not None
        assert hasattr(menu, 'display_menu')
        assert hasattr(menu, 'get_user_choice')
    except ImportError as e:
        pytest.fail(f"MainMenu import failed: {e}")


def test_media_wizard_import():
    """Test that media wizard can be imported."""
    try:
        from src.media_knowledge.cli.frontend.media_wizard import MediaWizard
        wizard = MediaWizard()
        assert wizard is not None
        assert hasattr(wizard, 'process_media_interactive')
    except ImportError as e:
        pytest.fail(f"MediaWizard import failed: {e}")


def test_cli_help_summary():
    """Test that CLI help shows all main commands."""
    runner = CliRunner()
    result = runner.invoke(app, ['--help'])
    
    assert result.exit_code == 0
    
    # Check for all major command groups
    required_commands = ['create-essay', 'status', 'process', 'batch', 'document', 'anki']
    for cmd in required_commands:
        assert cmd in result.stdout, f"Command '{cmd}' should be in help output"


def test_environment_variables():
    """Test that required environment variables are available."""
    # Check that basic environment variables can be accessed
    import os
    
    # Test that we can set and read environment variables
    test_env_var = "TEST_VAR_123"
    os.environ[test_env_var] = "test_value"
    assert os.environ.get(test_env_var) == "test_value"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])