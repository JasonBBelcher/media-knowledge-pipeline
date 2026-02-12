"""
Launcher for Media Knowledge Pipeline CLI Wizard System (v2)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from .main_menu_v2 import MainMenuV2

def launch_v2():
    """Launch the new wizard system."""
    try:
        print("Launching Media Knowledge Pipeline Wizard System v2...")
        menu = MainMenuV2()
        menu.run()
    except KeyboardInterrupt:
        print("\n\nExiting wizard system...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError launching wizard system: {e}")
        sys.exit(1)

def main():
    """Main entry point for the new wizard system."""
    launch_v2()

if __name__ == "__main__":
    main()