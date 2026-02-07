"""
Timeout Manager Utilities

Provides timeout handling for long-running subprocess operations,
particularly useful for ffmpeg operations that can hang.
"""

import subprocess
import threading
import time
from typing import List, Optional, Dict, Any
from pathlib import Path


class ProcessTimeoutError(Exception):
    """Raised when a subprocess exceeds its timeout limit."""
    pass


class ProcessManager:
    """Manages subprocess operations with timeout and progress monitoring."""
    
    def __init__(self, timeout: int = 300, verbose: bool = True):
        """
        Initialize ProcessManager.
        
        Args:
            timeout: Maximum time in seconds to allow process to run
            verbose: Whether to print progress information
        """
        self.timeout = timeout
        self.verbose = verbose
        self.process = None
        self.is_finished = False
        self.result = None
        self.error = None
        
    def _run_subprocess(self, cmd: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Run subprocess with timeout protection.
        
        Args:
            cmd: Command to execute as list of strings
            cwd: Working directory for the process
            
        Returns:
            Dictionary with keys: returncode, stdout, stderr, duration
            
        Raises:
            ProcessTimeoutError: If process exceeds timeout
            subprocess.CalledProcessError: If process exits with error
        """
        if self.verbose:
            print(f"Executing: {' '.join(cmd)}")
            
        start_time = time.time()
        
        try:
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Monitor progress in a separate thread
            if self.verbose:
                monitor_thread = threading.Thread(target=self._monitor_progress)
                monitor_thread.daemon = True
                monitor_thread.start()
            
            # Wait for completion with timeout
            try:
                stdout, stderr = self.process.communicate(timeout=self.timeout)
                duration = time.time() - start_time
                
                result = {
                    'returncode': self.process.returncode,
                    'stdout': stdout,
                    'stderr': stderr,
                    'duration': duration
                }
                
                # Check if this is a legitimate processing error (not timeout)
                if self.process.returncode != 0:
                    # Don't raise timeout error for ffmpeg processing errors
                    raise subprocess.CalledProcessError(
                        self.process.returncode, 
                        cmd, 
                        stderr
                    )
                    
                return result
                
            except subprocess.TimeoutExpired:
                # Terminate the process if it exceeds timeout
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)  # Give 5 seconds to terminate gracefully
                except subprocess.TimeoutExpired:
                    self.process.kill()  # Force kill if still running
                    
                raise ProcessTimeoutError(
                    f"Process exceeded timeout of {self.timeout} seconds: {' '.join(cmd)}"
                )
                
        except Exception as e:
            duration = time.time() - start_time
            if self.verbose:
                print(f"Process failed after {duration:.1f}s: {str(e)}")
            raise
            
    def _monitor_progress(self) -> None:
        """Monitor process output and display progress updates."""
        if not self.process or not self.process.stderr:
            return
            
        try:
            # Read stderr for progress information
            while self.process.poll() is None:
                if self.process.stderr:
                    # Read available output (non-blocking)
                    import select
                    import sys
                    
                    # Check if data is available to read
                    if hasattr(select, 'select'):  # Unix-like systems
                        ready, _, _ = select.select([self.process.stderr], [], [], 0.1)
                        if ready:
                            line = self.process.stderr.readline()
                            if line and self.verbose:
                                line = line.strip()
                                # Filter out repetitive progress lines
                                if not any(skip in line for skip in ['size=', 'time=', 'bitrate=', 'speed=']):
                                    print(f"  → {line}")
                    else:
                        # Windows - just let it run without monitoring
                        time.sleep(1)
                        
        except Exception:
            # Don't let monitoring errors crash the main process
            pass

    def run_with_retry(self, cmd: List[str], cwd: Optional[str] = None, 
                      max_retries: int = 3) -> Dict[str, Any]:
        """
        Run subprocess with retry logic on failure.
        
        Args:
            cmd: Command to execute as list of strings
            cwd: Working directory for the process
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary with execution results
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0 and self.verbose:
                    print(f"Retry attempt {attempt}/{max_retries}")
                    
                result = self._run_subprocess(cmd, cwd)
                return result
                
            except (ProcessTimeoutError, subprocess.CalledProcessError) as e:
                last_exception = e
                if attempt < max_retries:
                    if self.verbose:
                        print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    if self.verbose:
                        print(f"All {max_retries + 1} attempts failed")
                    break  # Exit the loop so we can raise the exception
            except Exception:
                # Handle any other exceptions
                if attempt < max_retries:
                    if self.verbose:
                        print(f"Attempt {attempt + 1} failed with exception, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    if self.verbose:
                        print(f"All {max_retries + 1} attempts failed")
                    break  # Exit the loop so we can raise the exception
                    
        # If we get here, all retries failed - raise the last exception
        if last_exception:
            raise last_exception
        else:
            # This shouldn't happen, but just in case
            raise Exception("Process failed for unknown reasons")


def run_ffmpeg_with_timeout(cmd: List[str], timeout: int = 300, 
                           max_retries: int = 3, verbose: bool = True) -> Dict[str, Any]:
    """
    Convenience function to run ffmpeg with timeout and retry.
    
    Args:
        cmd: ffmpeg command as list of strings
        timeout: Maximum execution time in seconds
        max_retries: Maximum retry attempts
        verbose: Whether to show progress information
        
    Returns:
        Dictionary with execution results
    """
    manager = ProcessManager(timeout=timeout, verbose=verbose)
    return manager.run_with_retry(cmd, max_retries=max_retries)


def test_ffmpeg_availability() -> bool:
    """
    Test if ffmpeg is available and responsive.
    
    Returns:
        True if ffmpeg is available, False otherwise
    """
    try:
        result = run_ffmpeg_with_timeout(
            ["ffmpeg", "-version"], 
            timeout=10, 
            verbose=False
        )
        return result['returncode'] == 0
    except Exception:
        return False