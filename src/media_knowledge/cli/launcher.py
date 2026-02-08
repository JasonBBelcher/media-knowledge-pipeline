#!/usr/bin/env python3
"""
Launcher for Media Knowledge Pipeline CLI
This module provides a convenient entry point that displays ASCII art.
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def display_welcome_ascii():
    """Display the welcome ASCII art for the application."""
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


def main():
    """Main launcher function."""
    display_welcome_ascii()
    print("Welcome to Media Knowledge Pipeline!")
    print()
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  WARNING: Virtual environment not activated!")
        print("   For best results, activate the virtual environment first:")
        print("   $ source venv/bin/activate")
        print("   Or if using media_knowledge_env:")
        print("   $ source media_knowledge_env/bin/activate")
        print()
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Exiting...")
            return
    
    print("🚀 Launching Media Knowledge Pipeline Interactive Frontend...")
    print()
    
    # Launch the interactive frontend directly
    try:
        from src.media_knowledge.cli.interactive import run_interactive_frontend
        run_interactive_frontend()
    except ImportError as e:
        print(f"Error importing interactive frontend: {e}")
        print("Please ensure all dependencies are installed.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()