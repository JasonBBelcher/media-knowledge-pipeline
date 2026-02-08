"""
Document Processing Wizard for Media Knowledge Pipeline CLI Frontend
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.media_knowledge.cli.frontend.main_menu import MainMenuError


class DocumentWizardError(Exception):
    """Custom exception for document wizard errors."""
    pass


class DocumentWizard:
    """Wizard for processing documents interactively."""
    
    def __init__(self):
        """Initialize document wizard."""
        self.document_types = [
            "PDF Document",
            "EPUB Book/Ebook",
            "MOBI Book/Ebook"
        ]
        
        self.templates = [
            "Lecture Summary (Educational content)",
            "Technical Documentation",
            "Research Summary",
            "Tutorial Guide",
            "Basic Summary",
            "Custom Prompt"
        ]
        
        self.output_options = [
            "Save detailed JSON results",
            "Save Markdown summary",
            "Save both formats",
            "No file output (display only)"
        ]
    
    def select_document_type(self):
        """Guide user through document type selection.
        
        Returns:
            str: Selected document type extension
            
        Raises:
            DocumentWizardError: If user cancels or invalid input
        """
        print("\nStep 1: Select Document Type")
        for i, doc_type in enumerate(self.document_types, 1):
            print(f"[{i}] {doc_type}")
        print("[0] Back to Main Menu")
        
        while True:
            try:
                choice = input("\nEnter choice (0-3): ").strip()
                if not choice:
                    print("Please enter a choice.")
                    continue
                
                choice_num = int(choice)
                if choice_num == 0:
                    raise DocumentWizardError("User cancelled")
                elif 1 <= choice_num <= 3:
                    # Return file extension
                    extensions = ["pdf", "epub", "mobi"]
                    return extensions[choice_num - 1]
                else:
                    print("Please enter a number between 0 and 3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_file_path(self, extension):
        """Get and validate file path from user.
        
        Args:
            extension (str): Expected file extension
            
        Returns:
            str: Validated file path
            
        Raises:
            DocumentWizardError: If file doesn't exist or invalid
        """
        print(f"\nStep 2: Enter Document Path")
        print(f"Please provide the full path to your .{extension} file:")
        print("(Default: current directory)")
        
        while True:
            try:
                file_path = input("> ").strip()
                
                if not file_path:
                    # Default to current directory with sample name
                    file_path = f"./sample.{extension}"
                    print(f"Using default: {file_path}")
                
                # Validate file exists
                path_obj = Path(file_path)
                if not path_obj.exists():
                    print(f"File not found: {file_path}")
                    print("Please check the path and try again.")
                    continue
                
                # Validate extension matches
                if path_obj.suffix.lower() != f".{extension}":
                    print(f"File must have .{extension} extension, got {path_obj.suffix}")
                    continue
                
                return str(path_obj)
                
            except KeyboardInterrupt:
                raise DocumentWizardError("User cancelled")
            except Exception as e:
                print(f"Error reading file path: {e}")
                print("Please try again.")
    
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
                    raise DocumentWizardError("User cancelled")
                elif 1 <= choice_num <= 5:
                    # Map to template keys
                    template_keys = [
                        "lecture_summary",
                        "technical_documentation", 
                        "research_summary",
                        "tutorial_guide",
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
        print("Enter your custom prompt for processing this document:")
        
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
                    raise DocumentWizardError("User cancelled")
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
            "quiet": quiet_mode
        }
    
    def confirm_and_execute(self, file_path, template, output_config, processing_options, custom_prompt=None):
        """Confirm settings and show what would be executed.
        
        Args:
            file_path (str): Document file path
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
        print(f"Document: {file_path}")
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
        
        print("\nReady to process! Press ENTER to begin or 'q' to cancel:")
        choice = input("> ").strip().lower()
        
        return choice != 'q'
    
    def process_document_interactive(self):
        """Main interactive document processing flow.
        
        Returns:
            dict: Processing configuration or None if cancelled
        """
        try:
            print("\n" + "=" * 50)
            print("PROCESS DOCUMENT WIZARD")
            print("=" * 50)
            
            # Step 1: Select document type
            extension = self.select_document_type()
            
            # Step 2: Get file path
            file_path = self.get_file_path(extension)
            
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
                file_path, template, output_config, processing_options, custom_prompt
            )
            
            if confirmed:
                return {
                    "file_path": file_path,
                    "template": template,
                    "custom_prompt": custom_prompt,
                    "output_config": output_config,
                    "processing_options": processing_options
                }
            else:
                print("Document processing cancelled.")
                return None
                
        except DocumentWizardError as e:
            print(f"Wizard cancelled: {e}")
            return None
        except KeyboardInterrupt:
            print("\nDocument processing cancelled by user.")
            return None


def main():
    """Main function for testing the document wizard."""
    wizard = DocumentWizard()
    result = wizard.process_document_interactive()
    if result:
        print("\nConfiguration created:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    return result


if __name__ == "__main__":
    main()