"""
Command Executor for Media Knowledge Pipeline CLI Frontend
This module executes the actual CLI commands based on wizard configurations.
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class CommandExecutor:
    """Execute CLI commands based on wizard configurations."""
    
    def __init__(self):
        """Initialize command executor."""
        self.base_command = [sys.executable, "-m", "media_knowledge"]
    
    def execute_media_processing(self, config):
        """Execute media processing based on configuration.
        
        Args:
            config (dict): Media processing configuration from wizard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build command based on configuration
            command = self.base_command + ["process", "media"]
            
            # Add input (URL or file path)
            command.extend(["--input", config["media_input"]])
            
            # Add cloud option if enabled
            if config["processing_options"]["use_cloud"]:
                command.append("--cloud")
            
            # Add template or custom prompt
            if config["template"] and config["template"] != "custom":
                command.extend(["--prompt", config["template"]])
            elif config["custom_prompt"]:
                command.extend(["--prompt", config["custom_prompt"]])
            
            # Add output options
            if config["output_config"]["save_json"]:
                command.extend(["--output", "results.json"])
            
            if config["output_config"]["save_markdown"]:
                command.extend(["--markdown", "output"])
            
            # Add quiet option
            if config["processing_options"]["quiet"]:
                command.append("--quiet")
            
            # Add organize option
            if not config["processing_options"]["organize"]:
                command.append("--no-organize")
            
            print(f"\nExecuting command: {' '.join(command)}")
            
            # Execute command
            result = subprocess.run(command, cwd=str(project_root))
            
            if result.returncode == 0:
                print("\n✅ Media processing completed successfully!")
                return True
            else:
                print(f"\n❌ Media processing failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error executing media processing: {e}")
            return False
    
    def execute_document_processing(self, config):
        """Execute document processing based on configuration.
        
        Args:
            config (dict): Document processing configuration from wizard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build command based on configuration
            command = self.base_command + ["document", "process"]
            
            # Add file path
            command.append(config["file_path"])
            
            # Add cloud option if enabled
            if config["processing_options"]["use_cloud"]:
                command.append("--cloud")
            
            # Add template or custom prompt
            if config["template"] and config["template"] != "custom":
                command.extend(["--prompt", config["template"]])
            elif config["custom_prompt"]:
                command.extend(["--custom-prompt", config["custom_prompt"]])
            
            # Add output options
            if config["output_config"]["save_json"] or config["output_config"]["save_markdown"]:
                command.extend(["--output", "results.json"])
            
            # Add quiet option
            if config["processing_options"]["quiet"]:
                command.append("--quiet")
            
            print(f"\nExecuting command: {' '.join(command)}")
            
            # Execute command
            result = subprocess.run(command, cwd=str(project_root))
            
            if result.returncode == 0:
                print("\n✅ Document processing completed successfully!")
                return True
            else:
                print(f"\n❌ Document processing failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error executing document processing: {e}")
            return False
    
    def execute_batch_processing(self, config):
        """Execute batch processing based on configuration.
        
        Args:
            config (dict): Batch processing configuration from wizard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build command based on configuration
            command = self.base_command + ["batch", "process-urls"]
            
            # Add URLs file
            command.extend(["--urls", config["urls_file"]])
            
            # Add output directory
            command.extend(["--output-dir", config["output_dir"]])
            
            # Add cloud option if enabled
            if config["processing_options"]["use_cloud"]:
                command.append("--cloud")
            
            # Add template or custom prompt
            if config["template"] and config["template"] != "custom":
                command.extend(["--prompt", config["template"]])
            elif config["custom_prompt"]:
                command.extend(["--prompt", config["custom_prompt"]])
            
            # Add parallel processing
            if config["parallel_workers"] > 1:
                command.extend(["--parallel", str(config["parallel_workers"])])
            
            # Add essay options
            if config["essay_options"]["enable_essay"]:
                command.append("--essay")
                if config["essay_options"]["force_essay"]:
                    command.append("--force-essay")
            
            # Add quiet option
            if config["processing_options"]["quiet"]:
                command.append("--quiet")
            
            # Add organize option
            if not config["processing_options"]["organize"]:
                command.append("--no-organize")
            
            print(f"\nExecuting command: {' '.join(command)}")
            
            # Execute command
            result = subprocess.run(command, cwd=str(project_root))
            
            if result.returncode == 0:
                print("\n✅ Batch processing completed successfully!")
                return True
            else:
                print(f"\n❌ Batch processing failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error executing batch processing: {e}")
            return False


def main():
    """Main function for testing the command executor."""
    print("Command Executor for Media Knowledge Pipeline")
    executor = CommandExecutor()
    print("Executor initialized successfully!")


if __name__ == "__main__":
    main()