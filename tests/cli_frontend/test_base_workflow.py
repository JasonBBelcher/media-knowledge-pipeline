"""
Unit tests for base workflow class
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.media_knowledge.cli.frontend.workflows.base_workflow import BaseWorkflow, WorkflowError

class ConcreteWorkflow(BaseWorkflow):
    """Concrete implementation of BaseWorkflow for testing."""
    
    def __init__(self):
        super().__init__()
        self.workflow_name = "Test Workflow"
        self.execution_result = False
    
    def run(self):
        """Implementation of abstract run method."""
        return True
    
    def execute(self):
        """Implementation of abstract execute method."""
        return self.execution_result

class TestBaseWorkflow:
    """Test base workflow class."""
    
    def test_initialization(self):
        """Test base workflow initialization."""
        workflow = ConcreteWorkflow()
        assert workflow.workflow_name == "Test Workflow"
        assert workflow.config == {}
    
    def test_display_header(self, capsys):
        """Test display header functionality."""
        workflow = ConcreteWorkflow()
        workflow.display_header("Test Header")
        
        captured = capsys.readouterr()
        assert "TEST HEADER" in captured.out
        assert "=" * 60 in captured.out
    
    def test_display_step(self, capsys):
        """Test display step functionality."""
        workflow = ConcreteWorkflow()
        workflow.display_step(1, "Test Step")
        
        captured = capsys.readouterr()
        assert "Step 1: Test Step" in captured.out
    
    def test_collect_and_get_config(self):
        """Test configuration collection and retrieval."""
        workflow = ConcreteWorkflow()
        
        # Collect some config values
        workflow.collect_config("test_key", "test_value")
        workflow.collect_config("number_key", 42)
        
        # Retrieve config values
        assert workflow.get_config("test_key") == "test_value"
        assert workflow.get_config("number_key") == 42
        assert workflow.get_config("nonexistent_key") is None
        assert workflow.get_config("nonexistent_key", "default") == "default"
    
    def test_confirm_and_execute_success(self):
        """Test confirm and execute with positive confirmation."""
        workflow = ConcreteWorkflow()
        workflow.execution_result = True
        
        # Mock user confirmation
        with patch('src.media_knowledge.cli.frontend.shared.user_prompter.prompt_for_confirmation', return_value=True):
            result = workflow.confirm_and_execute()
            assert result == True
    
    def test_confirm_and_execute_cancelled(self):
        """Test confirm and execute with negative confirmation."""
        workflow = ConcreteWorkflow()
        
        # Mock user cancellation
        with patch('src.media_knowledge.cli.frontend.shared.user_prompter.prompt_for_confirmation', return_value=False):
            result = workflow.confirm_and_execute()
            assert result == False
    
    def test_cleanup(self):
        """Test cleanup method."""
        workflow = ConcreteWorkflow()
        # Should not raise any exceptions
        workflow.cleanup()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])