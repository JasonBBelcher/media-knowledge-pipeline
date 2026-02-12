"""
Main Menu System for Media Knowledge Pipeline CLI Wizard System (v2)
"""

from typing import Optional
from .shared.user_prompter import prompt_for_choice
from .workflows.media_workflow import MediaWorkflow
from .workflows.batch_workflow import BatchWorkflow
from .workflows.document_workflow import DocumentWorkflow
from .workflows.anki_workflow import AnkiWorkflow

class MainMenuError(Exception):
    """Custom exception for main menu errors."""
    pass

class MainMenuV2:
    """Main menu system for interactive CLI frontend (v2)."""
    
    def __init__(self):
        """Initialize main menu system."""
        self.menu_options = [
            "Process Media Content  (Video/Audio)",
            "Batch Process Multiple Items",
            "Process Document (PDF/EPUB/MOBI)",
            "Generate Anki Flashcards",
            "Exit"
        ]
    
    def display_title(self):
        """Display the title for the application."""
        print("=" * 60)
        print("           MEDIA KNOWLEDGE PIPELINE")
        print("                Wizard System v2")
        print("=" * 60)
        print()
    
    def display_menu(self):
        """Display the main menu options."""
        self.display_title()
        print("What would you like to do?")
        print()
    
    def get_user_choice(self) -> Optional[int]:
        """
        Get and validate user input.
        
        Returns:
            Optional[int]: Valid user choice or None if cancelled
        """
        return prompt_for_choice(
            "What would you like to do?",
            self.menu_options,
            allow_cancel=True,
            cancel_label="Exit"
        )
    
    def route_to_workflow(self, choice: int) -> bool:
        """
        Route user to selected workflow.
        
        Args:
            choice (int): User's menu choice
            
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        try:
            if choice == 1:
                workflow = MediaWorkflow()
                return workflow.run()
            elif choice == 2:
                workflow = BatchWorkflow()
                return workflow.run()
            elif choice == 3:
                workflow = DocumentWorkflow()
                return workflow.run()
            elif choice == 4:
                workflow = AnkiWorkflow()
                return workflow.run()
            else:
                print("Invalid choice.")
                return False
        except Exception as e:
            print(f"Error running workflow: {e}")
            return False
    
    def run(self) -> bool:
        """
        Run the main menu loop.
        
        Returns:
            bool: True if exited normally, False if error occurred
        """
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                # Handle exit
                if choice is None:  # User chose to exit
                    print("Goodbye!")
                    return True
                
                # Route to workflow
                if choice > 0:  # Valid choice
                    success = self.route_to_workflow(choice)
                    if not success:
                        print("Workflow completed with issues.")
                    
                    # Pause before showing menu again
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                return True
            except Exception as e:
                print(f"Error in main menu: {e}")
                return False

def main():
    """Main function for testing the menu system."""
    menu = MainMenuV2()
    menu.run()

if __name__ == "__main__":
    main()