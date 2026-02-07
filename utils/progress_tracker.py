"""
Progress tracking utilities for the media knowledge pipeline.
"""

import sys
import time
from typing import Optional
from datetime import datetime


class ProgressTracker:
    """A simple progress tracker for the media knowledge pipeline."""
    
    def __init__(self, total_items: int = 0, quiet: bool = False):
        """
        Initialize progress tracker.
        
        Args:
            total_items: Total number of items to process
            quiet: Whether to suppress detailed output
        """
        self.total_items = total_items
        self.processed_items = 0
        self.current_item = 0
        self.start_time = time.time()
        self.quiet = quiet
        self.current_phase = ""
        self.item_start_time = None
        
    def start_processing(self, item_name: str = "") -> None:
        """Start processing an item."""
        self.current_item += 1
        self.item_start_time = time.time()
        if not self.quiet:
            if self.total_items > 0:
                percentage = (self.current_item / self.total_items) * 100
                print(f"\n[{self.current_item}/{self.total_items} {percentage:.1f}%] Processing: {item_name}")
            else:
                print(f"\n[{self.current_item}] Processing: {item_name}")
            sys.stdout.flush()
    
    def update_phase(self, phase: str) -> None:
        """Update the current processing phase."""
        self.current_phase = phase
        if not self.quiet:
            print(f"  → {phase}...")
            sys.stdout.flush()
    
    def complete_item(self, item_name: str = "", success: bool = True) -> None:
        """Mark an item as completed."""
        self.processed_items += 1
        item_time = time.time() - self.item_start_time if self.item_start_time else 0
        
        if not self.quiet:
            status = "✓" if success else "✗"
            time_str = f" ({item_time:.1f}s)" if item_time > 0 else ""
            print(f"  {status} Completed{time_str}: {item_name}")
            sys.stdout.flush()
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since tracker was initialized."""
        return time.time() - self.start_time
    
    def get_eta(self) -> str:
        """Get estimated time of arrival."""
        if self.total_items <= 0 or self.processed_items <= 0:
            return "Unknown"
            
        elapsed = self.get_elapsed_time()
        avg_time_per_item = elapsed / self.processed_items
        remaining_items = self.total_items - self.processed_items
        eta_seconds = avg_time_per_item * remaining_items
        
        if eta_seconds < 60:
            return f"{eta_seconds:.0f}s"
        elif eta_seconds < 3600:
            return f"{eta_seconds/60:.1f}m"
        else:
            return f"{eta_seconds/3600:.1f}h"


class ProgressBar:
    """A text-based progress bar for visual progress indication."""
    
    def __init__(self, total: int, width: int = 50):
        """
        Initialize progress bar.
        
        Args:
            total: Total number of items
            width: Width of the progress bar in characters
        """
        self.total = total
        self.width = width
        self.current = 0
        self.start_time = time.time()
        
    def update(self, current: Optional[int] = None, message: str = "") -> None:
        """Update the progress bar."""
        if current is not None:
            self.current = current
        else:
            self.current += 1
            
        # Calculate percentage
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        
        # Create progress bar
        filled_width = int(self.width * self.current // self.total) if self.total > 0 else 0
        bar = "█" * filled_width + "░" * (self.width - filled_width)
        
        # Calculate ETA
        elapsed = time.time() - self.start_time
        if self.current > 0 and elapsed > 0:
            avg_time_per_item = elapsed / self.current
            remaining_items = self.total - self.current
            eta_seconds = avg_time_per_item * remaining_items
            if eta_seconds < 60:
                eta = f"{eta_seconds:.0f}s"
            elif eta_seconds < 3600:
                eta = f"{eta_seconds/60:.1f}m"
            else:
                eta = f"{eta_seconds/3600:.1f}h"
        else:
            eta = "∞"
        
        # Print progress bar
        sys.stdout.write(f"\r[{bar}] {self.current}/{self.total} ({percentage:.1f}%) ETA: {eta} {message}")
        sys.stdout.flush()
        
    def finish(self, message: str = "Done!") -> None:
        """Finish the progress bar."""
        sys.stdout.write(f"\r{' ' * 100}\r{message}\n")
        sys.stdout.flush()


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


# Global progress tracker instance
_global_tracker: Optional[ProgressTracker] = None


def init_progress_tracker(total_items: int = 0, quiet: bool = False) -> ProgressTracker:
    """Initialize global progress tracker."""
    global _global_tracker
    _global_tracker = ProgressTracker(total_items, quiet)
    return _global_tracker


def get_progress_tracker() -> Optional[ProgressTracker]:
    """Get the global progress tracker."""
    global _global_tracker
    return _global_tracker


def start_item_processing(item_name: str = "") -> None:
    """Start processing an item using the global tracker."""
    if _global_tracker:
        _global_tracker.start_processing(item_name)


def update_processing_phase(phase: str) -> None:
    """Update processing phase using the global tracker."""
    if _global_tracker:
        _global_tracker.update_phase(phase)


def complete_item_processing(item_name: str = "", success: bool = True) -> None:
    """Complete item processing using the global tracker."""
    if _global_tracker:
        _global_tracker.complete_item(item_name, success)