"""
Integration tests for all workflow modules
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.media_knowledge.cli.frontend.workflows.media_workflow import MediaWorkflow
from src.media_knowledge.cli.frontend.workflows.batch_workflow import BatchWorkflow
from src.media_knowledge.cli.frontend.workflows.document_workflow import DocumentWorkflow
from src.media_knowledge.cli.frontend.workflows.anki_workflow import AnkiWorkflow

class TestWorkflowIntegration:
    """Test integration of all workflow modules."""
    
    def test_media_workflow_integration(self):
        """Test complete media workflow integration."""
        # This test verifies that the media workflow integrates properly
        # with all its components
        
        workflow = MediaWorkflow()
        
        # Verify initialization
        assert workflow.workflow_name == "Media Processing Workflow"
        assert hasattr(workflow, 'media_types')
        assert hasattr(workflow, 'templates')
        assert hasattr(workflow, 'output_options')
        
        # Verify inheritance from BaseWorkflow
        assert hasattr(workflow, 'run')
        assert hasattr(workflow, 'execute')
        assert hasattr(workflow, 'collect_config')
        assert hasattr(workflow, 'get_config')
        
        # Verify integration with shared utilities
        assert hasattr(workflow, 'select_media_type')
        assert hasattr(workflow, 'get_media_input')
        assert hasattr(workflow, 'select_template')
        
    def test_batch_workflow_integration(self):
        """Test complete batch workflow integration."""
        workflow = BatchWorkflow()
        
        # Verify initialization
        assert workflow.workflow_name == "Batch Processing Workflow"
        
        # Verify integration with shared utilities
        assert hasattr(workflow, 'get_urls_file')
        assert hasattr(workflow, 'get_parallel_workers')
        assert hasattr(workflow, 'get_essay_options')
        assert hasattr(workflow, 'get_output_directory')
        
    def test_document_workflow_integration(self):
        """Test complete document workflow integration."""
        workflow = DocumentWorkflow()
        
        # Verify initialization
        assert workflow.workflow_name == "Document Processing Workflow"
        assert hasattr(workflow, 'allowed_formats')
        
        # Verify integration with shared utilities
        assert hasattr(workflow, 'get_document_file')
        assert hasattr(workflow, 'select_template')
        assert hasattr(workflow, 'get_processing_options')
        assert hasattr(workflow, 'get_output_options')
        
    def test_anki_workflow_integration(self):
        """Test complete Anki workflow integration."""
        workflow = AnkiWorkflow()
        
        # Verify initialization
        assert workflow.workflow_name == "Anki Generation Workflow"
        
        # Verify integration with shared utilities
        assert hasattr(workflow, 'get_json_source')
        assert hasattr(workflow, 'get_deck_name')
        assert hasattr(workflow, 'preview_or_generate')
        assert hasattr(workflow, 'get_output_directory')
        
    def test_workflow_configuration_sharing(self):
        """Test that workflows can share configuration data."""
        workflow = MediaWorkflow()
        
        # Test collecting configuration
        workflow.collect_config("test_key", "test_value")
        workflow.collect_config("number_key", 42)
        
        # Test retrieving configuration
        assert workflow.get_config("test_key") == "test_value"
        assert workflow.get_config("number_key") == 42
        assert workflow.get_config("nonexistent_key") is None
        assert workflow.get_config("nonexistent_key", "default") == "default"
        
        # Verify configuration is stored in the workflow instance
        assert "test_key" in workflow.config
        assert "number_key" in workflow.config

if __name__ == "__main__":
    pytest.main([__file__, "-v"])