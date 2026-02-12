"""
Main Menu System for Media Knowledge Pipeline CLI Frontend
"""

from pathlib import Path

class MainMenuError(Exception):
    """Custom exception for main menu errors."""
    pass


class MainMenu:
    """Main menu system for interactive CLI frontend."""
    
    def __init__(self):
        """Initialize main menu system."""
        self.menu_options = [
            "Process Media Content  (Video/Audio/Document)",
            "Batch Process Multiple Items",
            "Create Essay from Existing Results",
            "Generate Anki Flashcards",
            "Scan Directory for Media Files",
            "Watch Directory for New Files", 
            "System Status and Requirements",
            "Show Pipeline Architecture",
            "Exit"
        ]
    
    def display_ascii_art_title(self):
        """Display the ASCII art title for the application."""
        try:
            # Use the art library to generate clean ASCII art
            from art import text2art
            media_art = text2art("MEDIA", font="standard")
            knowledge_art = text2art("KNOWLEDGE", font="standard")
            pipeline_art = text2art("PIPELINE", font="standard")
            
            print(media_art)
            print(knowledge_art)
            print(pipeline_art)
            print()
        except ImportError:
            # Fallback to simple header if art library not available
            print("=" * 60)
            print("           MEDIA KNOWLEDGE PIPELINE")
            print("=" * 60)
            print()
    
    def display_menu(self):
        """Display the main menu options."""
        # ASCII art is now displayed by the launcher, so we just show the menu
        print("=" * 80)
        print("                        MEDIA KNOWLEDGE PIPELINE")
        
        # Read version from VERSION file
        try:
            version_path = Path(__file__).parent.parent.parent.parent.parent / "VERSION"
            with open(version_path, 'r') as f:
                version = f.read().strip()
        except:
            version = "2.5.2"
        
        print(f"                          v{version} - Enhanced")
        print("=" * 80)
        print()
        print("=" * 80)
        print()
        print(" What would you like to do?")
        print()
        
        # Display menu options with numbers
        for i, option in enumerate(self.menu_options, 1):
            if option == "Exit":
                print(f" [0] {option}")
            else:
                print(f" [{i}] {option}")
        
        print()
        print(" Enter your choice (0-7): ", end="")
    
    def get_user_choice(self):
        """Get and validate user input.
        
        Returns:
            int: Valid user choice (0-7)
            
        Raises:
            MainMenuError: If user input is invalid
        """
        try:
            choice = input().strip()
            if not choice:
                raise MainMenuError("No input provided")
            
            choice_num = int(choice)
            
            # Validate choice range
            if choice_num == 0:
                return 0  # Exit
            elif 1 <= choice_num <= 7:
                return choice_num
            else:
                raise MainMenuError(f"Choice must be between 0 and 7, got {choice_num}")
                
        except ValueError:
            raise MainMenuError(f"Invalid input: '{choice}' is not a number")
    
    def run(self):
        """Run the main menu loop.
        
        Returns:
            int: User's menu choice
        """
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                return choice
            except MainMenuError as e:
                print(f"Error: {e}")
                print("Please try again.\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                return 0
            except EOFError:
                print("\nExiting...")
                return 0


def main():
    """Main function for testing the menu system."""
    menu = MainMenu()
    choice = menu.run()
    print(f"Selected option: {choice}")
    return choice


if __name__ == "__main__":
    main()