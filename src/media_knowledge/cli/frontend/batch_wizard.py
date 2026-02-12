"""
Batch Processing Wizard for Media Knowledge Pipeline CLI Frontend
"""

import os
import sys
from pathlib import Path

from .main_menu import MainMenuError


class BatchWizardError(Exception):
    """Custom exception for batch wizard errors."""
    pass


class BatchWizard:
    """Wizard for processing multiple YouTube URLs from a file."""
    
    def __init__(self):
        """Initialize batch wizard."""
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
    
    def get_urls_file(self):
        """Get and validate URLs file path from user.
        
        Returns:
            str: Validated URLs file path
            
        Raises:
            BatchWizardError: If file is invalid or user cancels
        """
        print("\nStep 1: Enter URLs File Path")
        print("Please provide the path to a text file containing YouTube URLs (one per line):")
        print("(Default: current directory)")
        
        while True:
            try:
                file_path = input("> ").strip()
                
                if not file_path:
                    # Default to current directory with sample name
                    file_path = "./urls.txt"
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
                
                # Validate file has content
                try:
                    with open(path_obj, 'r') as f:
                        content = f.read().strip()
                        if not content:
                            print(f"File is empty: {file_path}")
                            continue
                except Exception as e:
                    print(f"Cannot read file: {e}")
                    continue
                
                return str(path_obj)
                
            except KeyboardInterrupt:
                raise BatchWizardError("User cancelled")
            except Exception as e:
                print(f"Error reading file path: {e}")
                print("Please try again.")
    
    def get_output_directory(self):
        """Get output directory path from user.
        
        Returns:
            str: Output directory path
        """
        print("\nStep 2: Enter Output Directory")
        print("Please provide the directory where results should be saved:")
        print("(Default: ./outputs)")
        
        while True:
            try:
                dir_path = input("> ").strip()
                
                if not dir_path:
                    dir_path = "./outputs"
                    print(f"Using default: {dir_path}")
                
                # Create directory if it doesn't exist
                path_obj = Path(dir_path)
                path_obj.mkdir(parents=True, exist_ok=True)
                
                return str(path_obj)
                
            except KeyboardInterrupt:
                raise BatchWizardError("User cancelled")
            except Exception as e:
                print(f"Error creating directory: {e}")
                print("Please try again.")
    
    def get_parallel_workers(self):
        """Get number of parallel workers from user.
        
        Returns:
            int: Number of parallel workers (1-8)
        """
        print("\nStep 3: Parallel Processing")
        print("How many parallel workers do you want to use? (1-8)")
        print("(More workers = faster processing, but higher resource usage)")
        print("(Default: 1)")
        
        while True:
            try:
                workers_input = input("> ").strip()
                
                if not workers_input:
                    print("Using default: 1 worker")
                    return 1
                
                workers = int(workers_input)
                
                if 1 <= workers <= 8:
                    return workers
                else:
                    print("Please enter a number between 1 and 8.")
                    
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                raise BatchWizardError("User cancelled")
    
    def select_template(self):
        """Guide user through template selection.
        
        Returns:
            str: Selected template key or 'custom'
        """
        print("\nStep 4: Select Processing Template")
        print("Available Templates:")
        for i, template in enumerate(self.templates, 1):
            marker = " ← DEFAULT" if i == 1 else ""
            print(f"[{i}] {template}{marker}")
        print("[0] Back to Main Menu")
        
        while True:
            try:
                choice = input("\nEnter choice (0-7): ").strip()
                if not choice:
                    print("Using default template: lecture_summary")
                    return "lecture_summary"
                
                choice_num = int(choice)
                if choice_num == 0:
                    raise BatchWizardError("User cancelled")
                elif 1 <= choice_num <= 6:
                    # Map to template keys
                    template_keys = [
                        "lecture_summary",
                        "technical_tutorial", 
                        "research_presentation",
                        "podcast_summary",
                        "basic_summary",
                        "anki_flashcards"
                    ]
                    return template_keys[choice_num - 1]
                elif choice_num == 7:
                    return "custom"
                else:
                    print("Please enter a number between 0 and 7.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_custom_prompt(self):
        """Get custom prompt from user if selected.
        
        Returns:
            str: Custom prompt text
        """
        print("\nStep 4b: Enter Custom Prompt")
        print("Enter your custom prompt for processing these URLs:")
        
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
    
    def get_essay_options(self):
        """Get essay generation options.
        
        Returns:
            dict: Essay generation options
        """
        print("\nStep 5: Essay Generation")
        
        # Enable essay generation
        essay_choice = input("Generate comprehensive essay from multiple sources? [y/N]: ").strip().lower()
        enable_essay = essay_choice in ['y', 'yes']
        
        # Force essay generation
        force_essay = False
        if enable_essay:
            force_choice = input("Force essay generation even if content cohesion is questionable? [y/N]: ").strip().lower()
            force_essay = force_choice in ['y', 'yes']
        
        return {
            "enable_essay": enable_essay,
            "force_essay": force_essay
        }
    
    def get_processing_options(self):
        """Get additional processing options.
        
        Returns:
            dict: Processing options
        """
        print("\nStep 6: Processing Options")
        
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
    
    def confirm_and_execute(self, urls_file, output_dir, parallel_workers, template, essay_options, processing_options, custom_prompt=None):
        """Confirm settings and show what would be executed.
        
        Args:
            urls_file (str): Path to URLs file
            output_dir (str): Output directory
            parallel_workers (int): Number of parallel workers
            template (str): Template to use
            essay_options (dict): Essay generation options
            processing_options (dict): Processing options
            custom_prompt (str): Custom prompt if provided
            
        Returns:
            bool: True if user confirms, False if cancelled
        """
        print("\n" + "=" * 50)
        print("CONFIRMATION")
        print("=" * 50)
        print(f"URLs File: {urls_file}")
        print(f"Output Directory: {output_dir}")
        print(f"Parallel Workers: {parallel_workers}")
        print(f"Template: {template}")
        if custom_prompt:
            print(f"Custom Prompt: {custom_prompt[:50]}...")
        
        print("\nEssay Options:")
        print(f"  - Generate essay: {'Yes' if essay_options['enable_essay'] else 'No'}")
        if essay_options['enable_essay']:
            print(f"  - Force essay: {'Yes' if essay_options['force_essay'] else 'No'}")
        
        print(f"\nProcessing Options:")
        print(f"  - Cloud models: {'Yes' if processing_options['use_cloud'] else 'No'}")
        print(f"  - Quiet mode: {'Yes' if processing_options['quiet'] else 'No'}")
        print(f"  - Organize output: {'Yes' if processing_options['organize'] else 'No'}")
        
        print("\nReady to process! Press ENTER to begin or 'q' to cancel:")
        choice = input("> ").strip().lower()
        
        return choice != 'q'
    
    def process_batch_interactive(self):
        """Main interactive batch processing flow.
        
        Returns:
            dict: Processing configuration or None if cancelled
        """
        try:
            print("\n" + "=" * 50)
            print("BATCH PROCESSING WIZARD")
            print("=" * 50)
            
            # Step 1: Get URLs file
            urls_file = self.get_urls_file()
            
            # Step 2: Get output directory
            output_dir = self.get_output_directory()
            
            # Step 3: Get parallel workers
            parallel_workers = self.get_parallel_workers()
            
            # Step 4: Select template
            template = self.select_template()
            custom_prompt = None
            if template == "custom":
                custom_prompt = self.get_custom_prompt()
                template = "custom"
            
            # Step 5: Essay options
            essay_options = self.get_essay_options()
            
            # Step 6: Processing options
            processing_options = self.get_processing_options()
            
            # Confirmation
            confirmed = self.confirm_and_execute(
                urls_file, output_dir, parallel_workers, template, essay_options, processing_options, custom_prompt
            )
            
            if confirmed:
                return {
                    "urls_file": urls_file,
                    "output_dir": output_dir,
                    "parallel_workers": parallel_workers,
                    "template": template,
                    "custom_prompt": custom_prompt,
                    "essay_options": essay_options,
                    "processing_options": processing_options
                }
            else:
                print("Batch processing cancelled.")
                return None
                
        except BatchWizardError as e:
            print(f"Wizard cancelled: {e}")
            return None
        except KeyboardInterrupt:
            print("\nBatch processing cancelled by user.")
            return None


def main():
    """Main function for testing the batch wizard."""
    wizard = BatchWizard()
    result = wizard.process_batch_interactive()
    if result:
        print("\nConfiguration created:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    return result


if __name__ == "__main__":
    main()