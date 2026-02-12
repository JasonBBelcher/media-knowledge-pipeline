"""
Base workflow class for Media Knowledge Pipeline CLI Wizard System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import sys

class WorkflowError(Exception):
    """Custom exception for workflow errors."""
    pass

class BaseWorkflow(ABC):
    """Base class for all wizard workflows."""
    
    def __init__(self):
        """Initialize base workflow."""
        self.workflow_name = "Base Workflow"
        self.config = {}
    
    @abstractmethod
    def run(self) -> bool:
        """
        Run the workflow.
        
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        pass
    
    def display_header(self, title: str) -> None:
        """
        Display workflow header.
        
        Args:
            title (str): Title to display
        """
        print("\n" + "=" * 60)
        print(f"        {title.upper()}")
        print("=" * 60)
    
    def display_step(self, step_num: int, step_title: str) -> None:
        """
        Display current step in workflow.
        
        Args:
            step_num (int): Step number
            step_title (str): Step title
        """
        print(f"\nStep {step_num}: {step_title}")
    
    def collect_config(self, key: str, value: Any) -> None:
        """
        Collect configuration value.
        
        Args:
            key (str): Configuration key
            value (Any): Configuration value
        """
        self.config[key] = value
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key (str): Configuration key
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value or default
        """
        return self.config.get(key, default)
    
    def confirm_and_execute(self) -> bool:
        """
        Confirm configuration and execute workflow.
        
        Returns:
            bool: True if user confirms and executes, False if cancelled
        """
        from ..shared.user_prompter import prompt_for_confirmation
        
        print("\nConfiguration Summary:")
        print("-" * 30)
        for key, value in self.config.items():
            print(f"{key}: {value}")
        
        # Ask for confirmation
        confirm = prompt_for_confirmation("\nDo you want to proceed with these settings?")
        
        if confirm:
            return self.execute()
        else:
            print("Operation cancelled.")
            return False
    
    @abstractmethod
    def execute(self) -> bool:
        """
        Execute the workflow with current configuration.
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        pass
    
    def cleanup(self) -> None:
        """
        Cleanup resources after workflow completion.
        Override this method in subclasses if cleanup is needed.
        """
        pass