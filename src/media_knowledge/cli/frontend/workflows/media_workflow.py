"""
Media Processing Workflow for Media Knowledge Pipeline CLI Wizard System
"""

from typing import Dict, Any, Optional
from .base_workflow import BaseWorkflow
from ..shared.input_validator import validate_youtube_url, validate_file_path
from ..shared.user_prompter import prompt_for_choice, prompt_for_text, prompt_for_confirmation

class MediaWorkflowError(Exception):
    """Custom exception for media workflow errors."""
    pass

class MediaWorkflow(BaseWorkflow):
    """Workflow for processing media (YouTube videos, local audio/video files)."""
    
    def __init__(self):
        """Initialize media workflow."""
        super().__init__()
        self.workflow_name = "Media Processing Workflow"
        
        self.media_types = [
            "YouTube Video URL",
            "Local Media File (Video/Audio)"
        ]
        
        self.templates = [
            "Lecture Summary (Educational content)",
            "Technical Tutorial", 
            "Research Presentation",
            "Podcast Summary",
            "Basic Summary",
            "Anki Flashcards (Generate study cards)",
            "Custom Prompt"
        ]
        
        self.output_options = [
            "Save detailed JSON results",
            "Save Markdown summary",
            "Save both formats",
            "No file output (display only)"
        ]

    def run(self) -> bool:
        """
        Run the media processing workflow.
        
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        try:
            self.display_header("Media Processing Wizard")
            
            # Step 1: Select media type
            self.display_step(1, "Select Media Type")
            media_type = self.select_media_type()
            if media_type is None:
                return False
            
            # Step 2: Get media input
            self.display_step(2, "Enter Media Input")
            media_input = self.get_media_input(media_type)
            if media_input is None:
                return False
            
            # Step 3: Select template
            self.display_step(3, "Select Processing Template")
            template = self.select_template()
            if template is None:
                return False
            
            # Step 4: Get processing options
            self.display_step(4, "Processing Options")
            processing_options = self.get_processing_options()
            if processing_options is None:
                return False
            
            # Step 5: Get output options
            self.display_step(5, "Output Options")
            output_options = self.get_output_options()
            if output_options is None:
                return False
            
            # Step 6: Confirm and execute
            self.display_step(6, "Review & Execute")
            return self.confirm_and_execute()
            
        except Exception as e:
            print(f"Error in media workflow: {e}")
            return False

    def select_media_type(self) -> Optional[str]:
        """
        Guide user through media type selection.
        
        Returns:
            Optional[str]: Selected media type ('youtube' or 'local') or None if cancelled
        """
        choice = prompt_for_choice(
            "Select media type:",
            self.media_types,
            allow_cancel=True
        )
        
        if choice is None:
            return None
        elif choice == 1:
            return "youtube"
        elif choice == 2:
            return "local"
        else:
            return None

    def get_media_input(self, media_type: str) -> Optional[str]:
        """
        Get and validate media input (URL or file path) from user.
        
        Args:
            media_type (str): 'youtube' or 'local'
            
        Returns:
            Optional[str]: Validated media input or None if cancelled
        """
        if media_type == "youtube":
            print("Please provide the full YouTube URL:")
            print("(Example: https://www.youtube.com/watch?v=...)")
            
            while True:
                url = prompt_for_text("Enter YouTube URL:")
                if url is None:  # User cancelled
                    return None
                
                if validate_youtube_url(url):
                    self.collect_config("media_input", url)
                    self.collect_config("media_type", "youtube")
                    return url
                else:
                    print("Please enter a valid YouTube URL.")
        else:  # local file
            print("Please provide the full path to your media file:")
            print("(Supported: MP4, MOV, AVI, MKV, MP3, WAV, etc.)")
            
            while True:
                file_path = prompt_for_text("Enter file path:")
                if file_path is None:  # User cancelled
                    return None
                
                if validate_file_path(file_path):
                    self.collect_config("media_input", file_path)
                    self.collect_config("media_type", "local")
                    return file_path
                else:
                    print("File not found. Please check the path and try again.")

    def select_template(self) -> Optional[str]:
        """
        Guide user through template selection.
        
        Returns:
            Optional[str]: Selected template or None if cancelled
        """
        choice = prompt_for_choice(
            "Select processing template:",
            self.templates,
            allow_cancel=True
        )
        
        if choice is None:
            return None
        elif 1 <= choice <= len(self.templates):
            template_map = {
                1: "lecture_summary",
                2: "technical_tutorial",
                3: "research_presentation",
                4: "podcast_summary",
                5: "basic_summary",
                6: "anki_flashcards",
                7: "custom"
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
        choice = prompt_for_choice(
            "Select output options:",
            self.output_options,
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
        Execute the media processing workflow with current configuration.
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            print("\nExecuting media processing...")
            
            # Import and use the existing command executor
            from ..command_executor import CommandExecutor
            executor = CommandExecutor()
            
            # Prepare configuration for the executor
            config = {
                "media_input": self.get_config("media_input"),
                "media_type": self.get_config("media_type"),
                "template": self.get_config("template"),
                "custom_prompt": self.get_config("custom_prompt"),
                "processing_options": self.get_config("processing_options", {}),
                "output_config": self.get_config("output_config", {})
            }
            
            # Execute media processing
            success = executor.execute_media_processing(config)
            
            return success
        except Exception as e:
            print(f"Error during media processing: {e}")
            return False