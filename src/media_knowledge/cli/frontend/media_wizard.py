"""
Media Processing Wizard for Media Knowledge Pipeline CLI Frontend
"""

import os
import sys
import re
from pathlib import Path
from urllib.parse import urlparse

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.media_knowledge.cli.frontend.main_menu import MainMenuError


class MediaWizardError(Exception):
    """Custom exception for media wizard errors."""
    pass


class MediaWizard:
    """Wizard for processing media (YouTube videos, local audio/video files) interactively."""
    
    def __init__(self):
        """Initialize media wizard."""
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
            "Custom Prompt"
        ]
        
        self.output_options = [
            "Save detailed JSON results",
            "Save Markdown summary",
            "Save both formats",
            "No file output (display only)"
        ]
    
    def select_media_type(self):
        """Guide user through media type selection.
        
        Returns:
            str: Selected media type ('youtube' or 'local')
            
        Raises:
            MediaWizardError: If user cancels or invalid input
        """
        print("\nStep 1: Select Media Type")
        for i, media_type in enumerate(self.media_types, 1):
            print(f"[{i}] {media_type}")
        print("[0] Back to Main Menu")
        
        while True:
            try:
                choice = input("\nEnter choice (0-2): ").strip()
                if not choice:
                    print("Please enter a choice.")
                    continue
                
                choice_num = int(choice)
                if choice_num == 0:
                    raise MediaWizardError("User cancelled")
                elif choice_num == 1:
                    return "youtube"
                elif choice_num == 2:
                    return "local"
                else:
                    print("Please enter a number between 0 and 2.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_media_input(self, media_type):
        """Get and validate media input (URL or file path) from user.
        
        Args:
            media_type (str): 'youtube' or 'local'
            
        Returns:
            str: Validated media input (URL or file path)
            
        Raises:
            MediaWizardError: If input is invalid or user cancels
        """
        if media_type == "youtube":
            print("\nStep 2: Enter YouTube Video URL")
            print("Please provide the full YouTube URL:")
            print("(Example: https://www.youtube.com/watch?v=...)")
            
            while True:
                try:
                    url = input("> ").strip()
                    
                    if not url:
                        print("URL cannot be empty.")
                        continue
                    
                    # Validate URL format
                    if self._is_valid_youtube_url(url):
                        return url
                    else:
                        print("Please enter a valid YouTube URL.")
                        print("Example: https://www.youtube.com/watch?v=...")
                        continue
                        
                except KeyboardInterrupt:
                    raise MediaWizardError("User cancelled")
                except Exception as e:
                    print(f"Error reading URL: {e}")
                    print("Please try again.")
        else:  # local file
            print("\nStep 2: Enter Media File Path")
            print("Please provide the full path to your media file:")
            print("(Supported: MP4, MOV, AVI, MKV, MP3, WAV, etc.)")
            print("(Default: current directory)")
            
            while True:
                try:
                    file_path = input("> ").strip()
                    
                    if not file_path:
                        # Default to current directory with sample name
                        file_path = "./sample.mp4"
                        print(f"Using default: {file_path}")
                    
                    # Validate file exists
                    path_obj = Path(file_path)
                    if not path_obj.exists():
                        print(f"File not found: {file_path}")
                        print("Please check the path and try again.")
                        continue
                    
                    # Validate it's a file (not directory)
                    if not path_obj.is_file():
                        print(f"Path is not a file: {file_path}")
                        continue
                    
                    return str(path_obj)
                    
                except KeyboardInterrupt:
                    raise MediaWizardError("User cancelled")
                except Exception as e:
                    print(f"Error reading file path: {e}")
                    print("Please try again.")
    
    def _is_valid_youtube_url(self, url):
        """Validate YouTube URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid YouTube URL, False otherwise
        """
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            
            # Check if it's a YouTube domain
            if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
                return False
            
            # Check if it has the required path components for YouTube
            if "youtube.com" in parsed.netloc:
                return "watch" in parsed.path or "embed" in parsed.path
            elif "youtu.be" in parsed.netloc:
                return len(parsed.path) > 1  # Should have a video ID
            
            return True
        except Exception:
            return False
    
    def select_template(self):
        """Guide user through template selection.
        
        Returns:
            str: Selected template key or 'custom'
        """
        print("\nStep 3: Select Processing Template")
        print("Available Templates:")
        for i, template in enumerate(self.templates, 1):
            marker = " ← DEFAULT" if i == 1 else ""
            print(f"[{i}] {template}{marker}")
        print("[0] Back to Main Menu")
        
        while True:
            try:
                choice = input("\nEnter choice (0-6): ").strip()
                if not choice:
                    print("Using default template: lecture_summary")
                    return "lecture_summary"
                
                choice_num = int(choice)
                if choice_num == 0:
                    raise MediaWizardError("User cancelled")
                elif 1 <= choice_num <= 5:
                    # Map to template keys
                    template_keys = [
                        "lecture_summary",
                        "technical_tutorial", 
                        "research_presentation",
                        "podcast_summary",
                        "basic_summary"
                    ]
                    return template_keys[choice_num - 1]
                elif choice_num == 6:
                    return "custom"
                else:
                    print("Please enter a number between 0 and 6.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_custom_prompt(self):
        """Get custom prompt from user if selected.
        
        Returns:
            str: Custom prompt text
        """
        print("\nStep 3b: Enter Custom Prompt")
        print("Enter your custom prompt for processing this media:")
        
        while True:
            try:
                prompt = input("> ").strip()
                if prompt:
                    return prompt
                else:
                    print("Custom prompt cannot be empty. Using default behavior.")
                    return None
            except KeyboardInterrupt:
                return None
    
    def select_output_options(self):
        """Guide user through output options selection.
        
        Returns:
            dict: Output configuration
        """
        print("\nStep 4: Output Options")
        for i, option in enumerate(self.output_options, 1):
            print(f"[{i}] {option}")
        print("[0] Back to Main Menu")
        
        while True:
            try:
                choice = input("\nEnter choice (0-4): ").strip()
                if not choice:
                    print("Using default: Save both formats")
                    choice_num = 3
                else:
                    choice_num = int(choice)
                
                if choice_num == 0:
                    raise MediaWizardError("User cancelled")
                elif 1 <= choice_num <= 4:
                    return {
                        "save_json": choice_num in [1, 3],
                        "save_markdown": choice_num in [2, 3],
                        "output_type": choice_num
                    }
                else:
                    print("Please enter a number between 0 and 4.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_processing_options(self):
        """Get additional processing options.
        
        Returns:
            dict: Processing options
        """
        print("\nStep 5: Processing Options")
        
        # Cloud processing option
        cloud_choice = input("Use cloud models for processing? (Requires internet) [y/N]: ").strip().lower()
        use_cloud = cloud_choice in ['y', 'yes']
        
        # Quiet mode option
        quiet_choice = input("Run in quiet mode? (Less verbose output) [y/N]: ").strip().lower()
        quiet_mode = quiet_choice in ['y', 'yes']
        
        return {
            "use_cloud": use_cloud,
            "quiet": quiet_mode,
            "organize": True  # Always organize by default
        }
    
    def confirm_and_execute(self, media_input, media_type, template, output_config, processing_options, custom_prompt=None):
        """Confirm settings and show what would be executed.
        
        Args:
            media_input (str): URL or file path
            media_type (str): 'youtube' or 'local'
            template (str): Template to use
            output_config (dict): Output configuration
            processing_options (dict): Processing options
            custom_prompt (str): Custom prompt if provided
            
        Returns:
            bool: True if user confirms, False if cancelled
        """
        print("\n" + "=" * 50)
        print("CONFIRMATION")
        print("=" * 50)
        
        media_label = "YouTube URL" if media_type == "youtube" else "Local File"
        print(f"Media: {media_label}")
        print(f"Input: {media_input}")
        print(f"Template: {template}")
        if custom_prompt:
            print(f"Custom Prompt: {custom_prompt[:50]}...")
        
        print("\nOutput Options:")
        if output_config["save_json"]:
            print("  - Save detailed JSON results")
        if output_config["save_markdown"]:
            print("  - Save Markdown summary")
        if not (output_config["save_json"] or output_config["save_markdown"]):
            print("  - Display results only (no files saved)")
        
        print(f"\nProcessing Options:")
        print(f"  - Cloud models: {'Yes' if processing_options['use_cloud'] else 'No'}")
        print(f"  - Quiet mode: {'Yes' if processing_options['quiet'] else 'No'}")
        print(f"  - Organize output: {'Yes' if processing_options['organize'] else 'No'}")
        
        print("\nReady to process! Press ENTER to begin or 'q' to cancel:")
        choice = input("> ").strip().lower()
        
        return choice != 'q'
    
    def process_media_interactive(self):
        """Main interactive media processing flow.
        
        Returns:
            dict: Processing configuration or None if cancelled
        """
        try:
            print("\n" + "=" * 50)
            print("PROCESS MEDIA WIZARD")
            print("=" * 50)
            
            # Step 1: Select media type
            media_type = self.select_media_type()
            
            # Step 2: Get media input
            media_input = self.get_media_input(media_type)
            
            # Step 3: Select template
            template = self.select_template()
            custom_prompt = None
            if template == "custom":
                custom_prompt = self.get_custom_prompt()
                template = "custom"
            
            # Step 4: Output options
            output_config = self.select_output_options()
            
            # Step 5: Processing options
            processing_options = self.get_processing_options()
            
            # Confirmation
            confirmed = self.confirm_and_execute(
                media_input, media_type, template, output_config, processing_options, custom_prompt
            )
            
            if confirmed:
                return {
                    "media_input": media_input,
                    "media_type": media_type,
                    "template": template,
                    "custom_prompt": custom_prompt,
                    "output_config": output_config,
                    "processing_options": processing_options
                }
            else:
                print("Media processing cancelled.")
                return None
                
        except MediaWizardError as e:
            print(f"Wizard cancelled: {e}")
            return None
        except KeyboardInterrupt:
            print("\nMedia processing cancelled by user.")
            return None


def main():
    """Main function for testing the media wizard."""
    wizard = MediaWizard()
    result = wizard.process_media_interactive()
    if result:
        print("\nConfiguration created:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    return result


if __name__ == "__main__":
    main()