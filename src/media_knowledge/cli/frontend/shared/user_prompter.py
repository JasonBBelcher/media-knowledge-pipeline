"""
Standardized user prompting utilities for Media Knowledge Pipeline CLI Wizard System
"""

from typing import List, Optional, Union

def prompt_for_choice(
    prompt_text: str, 
    options: List[str], 
    allow_cancel: bool = True,
    cancel_label: str = "Back to Main Menu"
) -> Optional[int]:
    """
    Prompt user to select from a list of options.
    
    Args:
        prompt_text (str): Text to display before options
        options (List[str]): List of option descriptions
        allow_cancel (bool): Whether to allow cancellation
        cancel_label (str): Label for cancel option
        
    Returns:
        Optional[int]: Selected option index (1-based) or None if cancelled
    """
    print(f"\n{prompt_text}")
    
    # Display options
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    
    # Display cancel option if allowed
    if allow_cancel:
        print(f"[0] {cancel_label}")
    
    while True:
        try:
            choice = input("\nEnter choice: ").strip()
            if not choice:
                print("Please enter a choice.")
                continue
            
            choice_num = int(choice)
            
            # Handle cancellation
            if choice_num == 0 and allow_cancel:
                return None
            
            # Validate choice range
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                print(f"Please enter a number between {'0 and' if allow_cancel else '1 and'} {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            return None

def prompt_for_text(
    prompt_text: str, 
    allow_empty: bool = False,
    default_value: Optional[str] = None
) -> Optional[str]:
    """
    Prompt user for text input.
    
    Args:
        prompt_text (str): Text to display as prompt
        allow_empty (bool): Whether empty input is allowed
        default_value (Optional[str]): Default value if input is empty
        
    Returns:
        Optional[str]: User input or None if cancelled
    """
    print(f"\n{prompt_text}")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            # Handle empty input
            if not user_input:
                if allow_empty:
                    return default_value
                else:
                    print("Input cannot be empty.")
                    continue
            
            return user_input
        except KeyboardInterrupt:
            return None

def prompt_for_confirmation(prompt_text: str) -> Optional[bool]:
    """
    Prompt user for yes/no confirmation.
    
    Args:
        prompt_text (str): Text to display as prompt
        
    Returns:
        Optional[bool]: True for yes, False for no, None if cancelled
    """
    print(f"\n{prompt_text}")
    print("[y] Yes")
    print("[n] No")
    
    while True:
        try:
            choice = input("\nEnter choice (y/n): ").strip().lower()
            
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        except KeyboardInterrupt:
            return None

def prompt_for_number(
    prompt_text: str, 
    min_val: int, 
    max_val: int
) -> Optional[int]:
    """
    Prompt user for a number within a range.
    
    Args:
        prompt_text (str): Text to display as prompt
        min_val (int): Minimum allowed value
        max_val (int): Maximum allowed value
        
    Returns:
        Optional[int]: Number within range or None if cancelled
    """
    print(f"\n{prompt_text}")
    print(f"(Enter a number between {min_val} and {max_val})")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                print("Please enter a number.")
                continue
            
            num = int(user_input)
            
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            return None

# Additional prompting functions can be added here as needed