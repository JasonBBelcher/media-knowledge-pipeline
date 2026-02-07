#!/usr/bin/env python3
"""
Test script for progress tracking functionality.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.progress_tracker import ProgressTracker, ProgressBar


def test_progress_tracker():
    """Test the ProgressTracker class."""
    print("Testing ProgressTracker...")
    
    # Create a progress tracker for 5 items
    tracker = ProgressTracker(total_items=5, quiet=False)
    
    # Test starting processing
    tracker.start_processing("Test Item 1")
    
    # Test updating phase
    tracker.update_phase("Downloading")
    
    # Simulate some work
    import time
    time.sleep(0.1)
    
    # Test completing item
    tracker.complete_item("Test Item 1", success=True)
    
    # Test another item
    tracker.start_processing("Test Item 2")
    tracker.update_phase("Processing")
    time.sleep(0.1)
    tracker.complete_item("Test Item 2", success=False)
    
    print(f"Elapsed time: {tracker.get_elapsed_time():.2f}s")
    print(f"ETA: {tracker.get_eta()}")
    
    print("ProgressTracker test completed!")


def test_progress_bar():
    """Test the ProgressBar class."""
    print("\nTesting ProgressBar...")
    
    # Create a progress bar for 10 items
    bar = ProgressBar(total=10)
    
    # Update progress
    for i in range(1, 11):
        bar.update(i, f"Processing item {i}")
        import time
        time.sleep(0.1)
    
    bar.finish("All items processed!")
    
    print("ProgressBar test completed!")


if __name__ == "__main__":
    test_progress_tracker()
    test_progress_bar()