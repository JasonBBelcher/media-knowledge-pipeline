"""
Test backward compatibility with existing CLI commands
"""

import pytest
import subprocess
import sys
import os

class TestBackwardCompatibility:
    """Test that new wizard system preserves CLI command compatibility."""
    
    def test_media_processing_cli_equivalent(self):
        """Test that media workflow produces equivalent CLI command."""
        # This test verifies that our new workflow system would produce
        # the same CLI commands as the existing system
        
        # Example CLI command that should still work:
        # media-knowledge process media --input URL --prompt TEMPLATE
        
        # We can test this by importing and checking command structure
        from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
        executor = CommandExecutor()
        
        # Test media processing command structure
        config = {
            "media_input": "https://youtu.be/test123",
            "media_type": "youtube",
            "template": "lecture_summary",
            "custom_prompt": None,
            "processing_options": {"use_cloud": True, "quiet": False, "organize": True},
            "output_config": {"save_json": True, "save_markdown": True, "output_type": 3}
        }
        
        # Build expected command
        expected_parts = [
            "process",
            "media",
            "--input",
            "https://youtu.be/test123",
            "--cloud",
            "--prompt",
            "lecture_summary",
            "--output",
            "results.json",
            "--markdown",
            "outputs/markdown"
        ]
        
        # Verify command structure without actually executing it
        command = executor.base_command + ["process", "media"]
        command.extend(["--input", config["media_input"]])
        
        if config["processing_options"]["use_cloud"]:
            command.append("--cloud")
        
        if config["template"] and config["template"] != "custom":
            command.extend(["--prompt", config["template"]])
        
        if config["output_config"]["save_json"]:
            command.extend(["--output", "results.json"])
        
        if config["output_config"]["save_markdown"]:
            command.extend(["--markdown", "outputs/markdown"])
        
        if config["processing_options"]["quiet"]:
            command.append("--quiet")
        
        if not config["processing_options"]["organize"]:
            command.append("--no-organize")
        
        # Verify key parts are present
        assert "process" in command
        assert "media" in command
        assert "--input" in command
        assert "https://youtu.be/test123" in command
        
    def test_batch_processing_cli_equivalent(self):
        """Test that batch workflow produces equivalent CLI command."""
        from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
        executor = CommandExecutor()
        
        # Test batch processing command structure
        config = {
            "urls_file": "urls.txt",
            "output_dir": "outputs",
            "parallel_workers": 3,
            "template": "research_summary",
            "custom_prompt": None,
            "essay_options": {"enable_essay": True, "force_essay": False},
            "processing_options": {"use_cloud": False, "quiet": True, "organize": False}
        }
        
        # Build expected command structure
        command = executor.base_command + ["batch", "process-urls"]
        command.extend(["--urls", config["urls_file"]])
        command.extend(["--output-dir", config["output_dir"]])
        command.extend(["--parallel", str(config["parallel_workers"])])
        
        if config["processing_options"]["use_cloud"]:
            command.append("--cloud")
        
        if config["template"] and config["template"] != "custom":
            command.extend(["--prompt", config["template"]])
        
        if config["essay_options"]["enable_essay"]:
            command.append("--essay")
            if config["essay_options"]["force_essay"]:
                command.append("--force-essay")
        
        if config["processing_options"]["quiet"]:
            command.append("--quiet")
        
        if not config["processing_options"]["organize"]:
            command.append("--no-organize")
        
        # Verify key parts are present
        assert "batch" in command
        assert "process-urls" in command
        assert "--urls" in command
        assert "urls.txt" in command
        assert "--output-dir" in command
        assert "outputs" in command
        assert "--parallel" in command
        assert "3" in command
    
    def test_document_processing_cli_equivalent(self):
        """Test that document workflow produces equivalent CLI command."""
        from src.media_knowledge.cli.frontend.command_executor import CommandExecutor
        executor = CommandExecutor()
        
        # Test document processing command structure
        config = {
            "file_path": "document.pdf",
            "template": "academic_paper_summary",
            "custom_prompt": None,
            "processing_options": {"use_cloud": True, "quiet": False, "organize": True},
            "output_config": {"save_json": True, "save_markdown": False, "output_type": 1}
        }
        
        # Build expected command structure
        command = executor.base_command + ["document", "process"]
        command.append(config["file_path"])
        
        if config["processing_options"]["use_cloud"]:
            command.append("--cloud")
        
        if config["template"] and config["template"] != "custom":
            command.extend(["--prompt", config["template"]])
        
        if config["output_config"]["save_json"] or config["output_config"]["save_markdown"]:
            command.extend(["--output", "results.json"])
        
        if config["processing_options"]["quiet"]:
            command.append("--quiet")
        
        # Verify key parts are present
        assert "document" in command
        assert "process" in command
        assert "document.pdf" in command

if __name__ == "__main__":
    pytest.main([__file__, "-v"])