#!/usr/bin/env python3
"""
Interactive Frontend for Media Knowledge Pipeline CLI
This module provides a friendly menu-driven interface for the CLI.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.media_knowledge.cli.frontend.main_menu import MainMenu
from src.media_knowledge.cli.frontend.document_wizard import DocumentWizard
from src.media_knowledge.cli.frontend.media_wizard import MediaWizard
from src.media_knowledge.cli.frontend.batch_wizard import BatchWizard
from src.media_knowledge.cli.frontend.command_executor import CommandExecutor


def run_interactive_frontend():
    """Run the interactive frontend with menu and wizards."""
    print("Starting Media Knowledge Pipeline Interactive Frontend...")
    executor = CommandExecutor()
    
    while True:
        # Display main menu
        menu = MainMenu()
        choice = menu.run()
        
        # Handle menu choices
        if choice == 0:  # Exit
            print("Thank you for using Media Knowledge Pipeline!")
            break
        elif choice == 1:  # Process Media Content
            print("\nMedia Processing Selected")
            media_wizard = MediaWizard()
            config = media_wizard.process_media_interactive()
            if config:
                print("\nExecuting media processing with the following configuration:")
                for key, value in config.items():
                    print(f"  {key}: {value}")
                
                # Ask user if they want to execute
                confirm = input("\nDo you want to execute this processing? [y/N]: ").strip().lower()
                if confirm in ['y', 'yes']:
                    success = executor.execute_media_processing(config)
                    if success:
                        print("Media processing completed successfully!")
                    else:
                        print("Media processing failed. Check the error messages above.")
                else:
                    print("Media processing cancelled.")
            print("\nReturning to main menu...\n")
        elif choice == 2:  # Batch Process Multiple Items
            print("\nBatch Processing Selected")
            batch_wizard = BatchWizard()
            config = batch_wizard.process_batch_interactive()
            if config:
                print("\nExecuting batch processing with the following configuration:")
                for key, value in config.items():
                    print(f"  {key}: {value}")
                
                # Ask user if they want to execute
                confirm = input("\nDo you want to execute this batch processing? [y/N]: ").strip().lower()
                if confirm in ['y', 'yes']:
                    success = executor.execute_batch_processing(config)
                    if success:
                        print("Batch processing completed successfully!")
                    else:
                        print("Batch processing failed. Check the error messages above.")
                else:
                    print("Batch processing cancelled.")
            print("\nReturning to main menu...\n")
        elif choice == 3:  # Create Essay from Existing Results
            print("\nCreate Essay from Existing Results Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
        elif choice == 4:  # Scan Directory for Media Files
            print("\nScan Directory for Media Files Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
        elif choice == 5:  # Watch Directory for New Files
            print("\nWatch Directory for New Files Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
        elif choice == 6:  # System Status and Requirements
            print("\nSystem Status and Requirements Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
        elif choice == 7:  # Show Pipeline Architecture
            print("\nShow Pipeline Architecture Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")


def main():
    """Main entry point for interactive frontend."""
    try:
        run_interactive_frontend()
    except KeyboardInterrupt:
        print("\n\nInteractive frontend interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Exiting interactive frontend.")


if __name__ == "__main__":
    main()