"""
Test custom filename functionality in workflows
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.media_knowledge.cli.frontend.workflows.media_workflow import MediaWorkflow
from src.media_knowledge.cli.frontend.workflows.document_workflow import DocumentWorkflow

class TestCustomFilenames:
    """Test custom filename functionality in workflows."""
    
    def test_media_workflow_custom_filename(self):
        """Test media workflow with custom filename."""
        workflow = MediaWorkflow()
        
        # Mock both prompt_for_choice and prompt_for_text using direct input mocking
        with patch('builtins.input') as mock_input:
            # First call returns '1' (Save detailed JSON results)
            # Second call returns 'my_custom_file' (custom filename)
            mock_input.side_effect = ['1', 'my_custom_file']
            
            config = workflow.get_output_options()
            
            assert config is not None
            assert config["save_json"] == True
            assert config["save_markdown"] == False
            assert "output_path" in config
            assert config["output_path"] == "outputs/my_custom_file.json"
    
    def test_media_workflow_auto_naming(self):
        """Test media workflow with auto naming."""
        workflow = MediaWorkflow()
        
        # Mock both prompt_for_choice and prompt_for_text using direct input mocking
        with patch('builtins.input') as mock_input:
            # First call returns '1' (Save detailed JSON results)
            # Second call returns '' (empty for auto naming)
            mock_input.side_effect = ['1', '']
            
            config = workflow.get_output_options()
            
            # Now the function should NOT return None - it should return valid config with auto naming
            assert config is not None
            assert config["save_json"] == True
            assert config["save_markdown"] == False
            assert "output_path" in config
            assert config["output_path"] == "outputs/auto_named_results.json"
    
    def test_document_workflow_custom_filename(self):
        """Test document workflow with custom filename."""
        workflow = DocumentWorkflow()
        
        # Mock both prompt_for_choice and prompt_for_text using direct input mocking
        with patch('builtins.input') as mock_input:
            # First call returns '1' (Save detailed JSON results)
            # Second call returns 'document_summary' (custom filename)
            mock_input.side_effect = ['1', 'document_summary']
            
            config = workflow.get_output_options()
            
            assert config is not None
            assert config["save_json"] == True
            assert config["save_markdown"] == False
            assert "output_path" in config
            assert config["output_path"] == "outputs/document_summary.json"
    
    def test_both_outputs_custom_filename(self):
        """Test workflow with both outputs and custom filename."""
        workflow = MediaWorkflow()
        
        # Mock both prompt_for_choice and prompt_for_text using direct input mocking
        with patch('builtins.input') as mock_input:
            # First call returns '3' (Save both formats)
            # Second call returns 'complete_analysis' (custom filename)
            mock_input.side_effect = ['3', 'complete_analysis']
            
            config = workflow.get_output_options()
            
            assert config is not None
            assert config["save_json"] == True
            assert config["save_markdown"] == True
            assert "output_path" in config
            assert config["output_path"] == "outputs/complete_analysis.json"
            assert "markdown_path" in config
            assert config["markdown_path"] == "outputs/markdown"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])