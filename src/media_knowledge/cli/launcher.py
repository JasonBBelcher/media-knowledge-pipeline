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
    
    # Skip environment check since it's already done by the shell script
    print("🚀 Launching Media Knowledge Pipeline Interactive Frontend...")
    print()
    
    # Launch the interactive frontend directly
    try:
        # Try relative import first (package context)
        from .interactive import run_interactive_frontend
        run_interactive_frontend()
    except ImportError as e:
        # If relative import fails, try absolute import (direct execution)
        try:
            import sys
            import os
            # Add project root to path for imports
            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(__file__)
                        )
                    )
                )
            )
            sys.path.insert(0, project_root)
            from media_knowledge.cli.interactive import run_interactive_frontend
            run_interactive_frontend()
        except ImportError as e2:
            print(f"Error importing interactive frontend: {e}")
            print(f"Alternative import attempt failed: {e2}")
            print("Please ensure all dependencies are installed.")


if __name__ == "__main__":
    main()