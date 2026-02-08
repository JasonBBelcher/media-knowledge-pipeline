"""
Batch Processor for Media Knowledge Pipeline CLI
This module handles the core batch processing logic that can be used by both CLI commands and wizards.
"""

import sys
import re
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from urllib.parse import urlparse

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class BatchProcessorError(Exception):
    """Custom exception for batch processor errors."""
    pass


class BatchProcessor:
    """Handles batch processing of YouTube URLs with advanced features."""
    
    def __init__(self):
        """Initialize batch processor."""
        self.valid_urls = []
        self.invalid_urls = []
        self.processed_count = 0
        
    def parse_urls_file(self, urls_file_path: str) -> Tuple[List[str], List[str]]:
        """Parse URLs from file, separating valid from invalid.
        
        Args:
            urls_file_path (str): Path to file containing URLs
            
        Returns:
            Tuple[List[str], List[str]]: (valid_urls, invalid_urls)
            
        Raises:
            BatchProcessorError: If file cannot be read or is empty
        """
        try:
            urls_file = Path(urls_file_path)
            
            # Check if file exists
            if not urls_file.exists():
                raise BatchProcessorError(f"URLs file not found: {urls_file_path}")
            
            # Read file content
            with open(urls_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check if file is empty
            if not lines:
                raise BatchProcessorError(f"URLs file is empty: {urls_file_path}")
            
            # Parse URLs
            valid_urls = []
            invalid_urls = []
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Validate URL
                if self._is_valid_youtube_url(line):
                    valid_urls.append(line)
                else:
                    invalid_urls.append((line_num, line))
            
            self.valid_urls = valid_urls
            self.invalid_urls = invalid_urls
            
            return valid_urls, [url for _, url in invalid_urls]
            
        except IOError as e:
            raise BatchProcessorError(f"Cannot read URLs file: {e}")
        except Exception as e:
            raise BatchProcessorError(f"Error parsing URLs file: {e}")
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Validate YouTube URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid YouTube URL, False otherwise
        """
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            
            # Check if it's a YouTube domain
            if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
                return False
            
            # Check if it has the required path components for YouTube
            if "youtube.com" in parsed.netloc:
                return "watch" in parsed.path or "embed" in parsed.path or "v" in parsed.query
            elif "youtu.be" in parsed.netloc:
                return len(parsed.path) > 1  # Should have a video ID
            
            return True
        except Exception:
            return False
    
    def filter_valid_urls(self, urls: List[str]) -> List[str]:
        """Filter list to only include valid YouTube URLs.
        
        Args:
            urls (List[str]): List of URLs to filter
            
        Returns:
            List[str]: List of valid YouTube URLs
        """
        return [url for url in urls if self._is_valid_youtube_url(url)]
    
    def setup_parallel_processing(self, workers: int) -> bool:
        """Setup parallel processing with specified number of workers.
        
        Args:
            workers (int): Number of parallel workers (1-8)
            
        Returns:
            bool: True if setup successful, False otherwise
            
        Raises:
            BatchProcessorError: If workers count is invalid
        """
        if not isinstance(workers, int):
            raise BatchProcessorError("Workers must be an integer")
        
        if workers < 1 or workers > 8:
            raise BatchProcessorError("Workers must be between 1 and 8")
        
        # In a full implementation, this would setup a worker pool
        # For now, we'll just validate the configuration
        return True
    
    def configure_essay_generation(self, enable: bool, force: bool = False) -> Dict[str, bool]:
        """Configure essay generation options.
        
        Args:
            enable (bool): Whether to enable essay generation
            force (bool): Whether to force essay generation
            
        Returns:
            Dict[str, bool]: Configuration dictionary
        """
        return {
            "enabled": enable,
            "forced": force and enable  # Force only applies if enabled
        }
    
    def process_url(self, url: str, options: Dict = None) -> Dict:
        """Process a single URL with given options.
        
        Args:
            url (str): YouTube URL to process
            options (Dict): Processing options
            
        Returns:
            Dict: Processing result
        """
        # In a full implementation, this would call the actual processing functions
        # For now, we'll simulate the processing
        self.processed_count += 1
        
        return {
            "url": url,
            "status": "processed",
            "result_id": f"result_{self.processed_count}",
            "timestamp": "2026-02-08T14:30:00Z"
        }
    
    def process_batch(self, urls: List[str], parallel_workers: int = 1, options: Dict = None) -> Dict:
        """Process a batch of URLs with parallel processing.
        
        Args:
            urls (List[str]): List of URLs to process
            parallel_workers (int): Number of parallel workers
            options (Dict): Processing options
            
        Returns:
            Dict: Batch processing results
        """
        if options is None:
            options = {}
        
        # Setup parallel processing
        self.setup_parallel_processing(parallel_workers)
        
        # Process URLs
        results = []
        failed_urls = []
        
        for url in urls:
            try:
                result = self.process_url(url, options)
                results.append(result)
            except Exception as e:
                failed_urls.append({"url": url, "error": str(e)})
        
        return {
            "status": "completed",
            "total_processed": len(results),
            "total_failed": len(failed_urls),
            "results": results,
            "failures": failed_urls,
            "parallel_workers": parallel_workers
        }
    
    def get_statistics(self) -> Dict:
        """Get processing statistics.
        
        Returns:
            Dict: Processing statistics
        """
        return {
            "valid_urls_count": len(self.valid_urls),
            "invalid_urls_count": len(self.invalid_urls),
            "processed_count": self.processed_count,
            "success_rate": (self.processed_count / len(self.valid_urls) * 100) if self.valid_urls else 0
        }


def main():
    """Main function for testing the batch processor."""
    print("Batch Processor for Media Knowledge Pipeline")
    processor = BatchProcessor()
    print("Processor initialized successfully!")
    
    # Test URL validation
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/shorturl",
        "https://www.youtube.com/embed/embedded",
        "invalid-url",
        "https://www.google.com"
    ]
    
    print("\nTesting URL validation:")
    for url in test_urls:
        is_valid = processor._is_valid_youtube_url(url)
        print(f"  {url}: {'Valid' if is_valid else 'Invalid'}")


if __name__ == "__main__":
    main()