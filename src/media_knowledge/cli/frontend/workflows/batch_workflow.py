"""
Batch Processing Workflow for Media Knowledge Pipeline CLI Wizard System
"""

from typing import Dict, Any, Optional
from pathlib import Path
from .base_workflow import BaseWorkflow
from ..shared.input_validator import validate_file_path
from ..shared.user_prompter import prompt_for_text, prompt_for_confirmation, prompt_for_number

class BatchWorkflowError(Exception):
    """Custom exception for batch workflow errors."""
    pass

class BatchWorkflow(BaseWorkflow):
    """Workflow for batch processing multiple URLs."""
    
    def __init__(self):
        """Initialize batch workflow."""
        super().__init__()
        self.workflow_name = "Batch Processing Workflow"

    def run(self) -> bool:
        """
        Run the batch processing workflow.
        
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        try:
            self.display_header("Batch Processing Wizard")
            
            # Step 1: Get URLs file
            self.display_step(1, "Select URLs File")
            urls_file = self.get_urls_file()
            if urls_file is None:
                return False
            
            # Step 2: Configure parallel workers
            self.display_step(2, "Configure Parallel Processing")
            parallel_workers = self.get_parallel_workers()
            if parallel_workers is None:
                return False
            
            # Step 3: Select template
            self.display_step(3, "Select Processing Template")
            template = self.select_template()
            if template is None:
                return False
            
            # Step 4: Configure essay options
            self.display_step(4, "Essay Generation Options")
            essay_options = self.get_essay_options()
            if essay_options is None:
                return False
            
            # Step 5: Get processing options
            self.display_step(5, "Processing Options")
            processing_options = self.get_processing_options()
            if processing_options is None:
                return False
            
            # Step 6: Select output directory
            self.display_step(6, "Output Directory")
            output_dir = self.get_output_directory()
            if output_dir is None:
                return False
            
            # Step 7: Confirm and execute
            self.display_step(7, "Review & Execute")
            return self.confirm_and_execute()
            
        except Exception as e:
            print(f"Error in batch workflow: {e}")
            return False

    def get_urls_file(self) -> Optional[str]:
        """
        Get and validate URLs file from user.
        
        Returns:
            Optional[str]: Validated URLs file path or None if cancelled
        """
        print("Please provide the path to your URLs file:")
        print("(One URL per line in the file)")
        
        while True:
            file_path = prompt_for_text("Enter URLs file path:")
            if file_path is None:  # User cancelled
                return None
            
            if validate_file_path(file_path):
                self.collect_config("urls_file", file_path)
                return file_path
            else:
                print("File not found. Please check the path and try again.")

    def get_parallel_workers(self) -> Optional[int]:
        """
        Get number of parallel workers from user.
        
        Returns:
            Optional[int]: Number of parallel workers or None if cancelled
        """
        print("Configure parallel processing:")
        workers = prompt_for_number("Number of parallel workers (1-8):", 1, 8)
        
        if workers is not None:
            self.collect_config("parallel_workers", workers)
        
        return workers

    def select_template(self) -> Optional[str]:
        """
        Guide user through template selection.
        For simplicity, we'll use a fixed set of templates.
        
        Returns:
            Optional[str]: Selected template or None if cancelled
        """
        templates = [
            "Lecture Summary (Educational content)",
            "Technical Tutorial", 
            "Research Presentation",
            "Podcast Summary",
            "Basic Summary",
            "Custom Prompt"
        ]
        
        from ..shared.user_prompter import prompt_for_choice
        
        choice = prompt_for_choice(
            "Select processing template:",
            templates,
            allow_cancel=True
        )
        
        if choice is None:
            return None
        elif 1 <= choice <= len(templates):
            template_map = {
                1: "lecture_summary",
                2: "technical_tutorial",
                3: "research_presentation",
                4: "podcast_summary",
                5: "basic_summary",
                6: "custom"
            }
            
            template_name = template_map.get(choice, "basic_summary")
            self.collect_config("template", template_name)
            
            # Handle custom prompt
            if template_name == "custom":
                custom_prompt = prompt_for_text("Enter your custom prompt:")
                if custom_prompt is None:
                    return None
                self.collect_config("custom_prompt", custom_prompt)
            
            return template_name
        else:
            return None

    def get_essay_options(self) -> Optional[Dict[str, bool]]:
        """
        Get essay generation options from user.
        
        Returns:
            Optional[Dict[str, bool]]: Essay options or None if cancelled
        """
        print("Configure essay generation:")
        
        # Enable essay option
        enable_essay = prompt_for_confirmation("Enable essay generation?")
        if enable_essay is None:
            return None
        
        # Force essay option (only if essay is enabled)
        force_essay = False
        if enable_essay:
            force_essay = prompt_for_confirmation("Force essay generation for all items?")
            if force_essay is None:
                return None
        
        options = {
            "enable_essay": enable_essay,
            "force_essay": force_essay if enable_essay else False
        }
        
        self.collect_config("essay_options", options)
        return options

    def get_processing_options(self) -> Optional[Dict[str, Any]]:
        """
        Get processing options from user.
        
        Returns:
            Optional[Dict[str, Any]]: Processing options or None if cancelled
        """
        print("Configure processing options:")
        
        # Cloud processing option
        use_cloud = prompt_for_confirmation("Use cloud processing? (faster but requires internet)")
        if use_cloud is None:
            return None
        
        # Quiet mode option
        quiet = prompt_for_confirmation("Quiet mode? (minimal output)")
        if quiet is None:
            return None
        
        # Organization option
        organize = prompt_for_confirmation("Organize output files? (create subdirectories)")
        if organize is None:
            return None
        
        options = {
            "use_cloud": use_cloud,
            "quiet": quiet,
            "organize": organize
        }
        
        self.collect_config("processing_options", options)
        return options

    def get_output_directory(self) -> Optional[str]:
        """
        Get output directory from user.
        
        Returns:
            Optional[str]: Output directory path or None if cancelled
        """
        print("Select output directory:")
        print("(Leave empty to use default 'outputs' directory)")
        
        dir_path = prompt_for_text(
            "Enter output directory path:", 
            allow_empty=True, 
            default_value="outputs"
        )
        
        if dir_path is None:  # User cancelled
            return None
            
        # Create directory if it doesn't exist
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            self.collect_config("output_dir", dir_path)
            return dir_path
        except Exception as e:
            print(f"Error creating directory: {e}")
            return None

    def execute(self) -> bool:
        """
        Execute the batch processing workflow with current configuration.
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            print("\nExecuting batch processing...")
            
            # Import and use the existing command executor
            from ..command_executor import CommandExecutor
            executor = CommandExecutor()
            
            # Prepare configuration for the executor
            config = {
                "urls_file": self.get_config("urls_file"),
                "parallel_workers": self.get_config("parallel_workers", 1),
                "template": self.get_config("template"),
                "custom_prompt": self.get_config("custom_prompt"),
                "essay_options": self.get_config("essay_options", {}),
                "processing_options": self.get_config("processing_options", {}),
                "output_dir": self.get_config("output_dir", "outputs")
            }
            
            # Execute batch processing
            success = executor.execute_batch_processing(config)
            
            return success
        except Exception as e:
            print(f"Error during batch processing: {e}")
            return False