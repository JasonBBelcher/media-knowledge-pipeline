"""
Document Processing Workflow for Media Knowledge Pipeline CLI Wizard System
"""

from typing import Dict, Any, Optional
from pathlib import Path
from .base_workflow import BaseWorkflow
from ..shared.input_validator import validate_file_path, validate_file_format
from ..shared.user_prompter import prompt_for_text, prompt_for_confirmation

class DocumentWorkflowError(Exception):
    """Custom exception for document workflow errors."""
    pass

class DocumentWorkflow(BaseWorkflow):
    """Workflow for processing documents (PDF, EPUB, MOBI files)."""
    
    def __init__(self):
        """Initialize document workflow."""
        super().__init__()
        self.workflow_name = "Document Processing Workflow"
        self.allowed_formats = ['.pdf', '.epub', '.mobi']

    def run(self) -> bool:
        """
        Run the document processing workflow.
        
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        try:
            self.display_header("Document Processing Wizard")
            
            # Step 1: Get document file
            self.display_step(1, "Select Document File")
            document_file = self.get_document_file()
            if document_file is None:
                return False
            
            # Step 2: Select template
            self.display_step(2, "Select Processing Template")
            template = self.select_template()
            if template is None:
                return False
            
            # Step 3: Get processing options
            self.display_step(3, "Processing Options")
            processing_options = self.get_processing_options()
            if processing_options is None:
                return False
            
            # Step 4: Get output options
            self.display_step(4, "Output Options")
            output_options = self.get_output_options()
            if output_options is None:
                return False
            
            # Step 5: Confirm and execute
            self.display_step(5, "Review & Execute")
            return self.confirm_and_execute()
            
        except Exception as e:
            print(f"Error in document workflow: {e}")
            return False

    def get_document_file(self) -> Optional[str]:
        """
        Get and validate document file from user.
        
        Returns:
            Optional[str]: Validated document file path or None if cancelled
        """
        print("Please provide the path to your document file:")
        print("(Supported formats: PDF, EPUB, MOBI)")
        
        while True:
            file_path = prompt_for_text("Enter document file path:")
            if file_path is None:  # User cancelled
                return None
            
            # Check if file exists
            if not validate_file_path(file_path):
                print("File not found. Please check the path and try again.")
                continue
            
            # Check if file format is supported
            if not validate_file_format(file_path, self.allowed_formats):
                print(f"Unsupported file format. Supported formats: {', '.join(self.allowed_formats)}")
                continue
            
            self.collect_config("document_file", file_path)
            return file_path

    def select_template(self) -> Optional[str]:
        """
        Guide user through template selection.
        
        Returns:
            Optional[str]: Selected template or None if cancelled
        """
        templates = [
            "Academic Paper Summary",
            "Book Chapter Summary",
            "Research Article Analysis",
            "Technical Documentation",
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
                1: "academic_paper_summary",
                2: "book_chapter_summary",
                3: "research_article_analysis",
                4: "technical_documentation",
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

    def get_output_options(self) -> Optional[Dict[str, Any]]:
        """
        Get output options from user.
        
        Returns:
            Optional[Dict[str, Any]]: Output options or None if cancelled
        """
        output_options = [
            "Save detailed JSON results",
            "Save Markdown summary",
            "Save both formats",
            "No file output (display only)"
        ]
        
        from ..shared.user_prompter import prompt_for_choice
        
        choice = prompt_for_choice(
            "Select output options:",
            output_options,
            allow_cancel=True
        )
        
        if choice is None:
            return None
        
        # Map choices to output configuration
        output_config = {
            1: {"save_json": True, "save_markdown": False, "output_type": 1},
            2: {"save_json": False, "save_markdown": True, "output_type": 2},
            3: {"save_json": True, "save_markdown": True, "output_type": 3},
            4: {"save_json": False, "save_markdown": False, "output_type": 0}
        }
        
        config = output_config.get(choice, output_config[3])  # Default to no output
        
        # If user wants to save JSON, ask for custom filename
        if config["save_json"]:
            print("\nCustom filename for JSON output (optional):")
            print("Leave empty to use intelligent auto-naming")
            custom_name = prompt_for_text("Enter filename (without .json extension):", allow_empty=True, default_value="")
            
            if custom_name is None:  # User cancelled (Ctrl+C)
                return None
                
            if custom_name:
                # Use custom filename in outputs directory
                config["output_path"] = f"outputs/{custom_name}.json"
            else:
                # Use intelligent naming - let system decide in outputs directory
                config["output_path"] = "outputs/auto_named_results.json"
        
        # If user wants to save markdown, markdown always goes to organized directory
        if config["save_markdown"]:
            config["markdown_path"] = "outputs/markdown"
            
        self.collect_config("output_config", config)
        return config

    def execute(self) -> bool:
        """
        Execute the document processing workflow with current configuration.
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            print("\nExecuting document processing...")
            
            # Import and use the existing command executor
            from ..command_executor import CommandExecutor
            executor = CommandExecutor()
            
            # Prepare configuration for the executor
            config = {
                "file_path": self.get_config("document_file"),
                "template": self.get_config("template"),
                "custom_prompt": self.get_config("custom_prompt"),
                "processing_options": self.get_config("processing_options", {}),
                "output_config": self.get_config("output_config", {})
            }
            
            # Execute document processing
            success = executor.execute_document_processing(config)
            
            return success
        except Exception as e:
            print(f"Error during document processing: {e}")
            return False