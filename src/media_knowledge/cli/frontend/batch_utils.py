"""
Batch Processing Utilities for Media Knowledge Pipeline CLI Frontend
This module provides helper functions for batch processing wizards.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.media_knowledge.cli.batch_processor import BatchProcessor, BatchProcessorError


class BatchUtilsError(Exception):
    """Custom exception for batch utilities errors."""
    pass


class BatchUtilities:
    """Utility functions for batch processing wizards."""
    
    def __init__(self):
        """Initialize batch utilities."""
        self.processor = BatchProcessor()
    
    def validate_urls_file(self, file_path: str) -> dict:
        """Validate URLs file and return statistics.
        
        Args:
            file_path (str): Path to URLs file
            
        Returns:
            dict: Validation results including counts and samples
            
        Raises:
            BatchUtilsError: If file cannot be validated
        """
        try:
            valid_urls, invalid_urls = self.processor.parse_urls_file(file_path)
            
            return {
                "valid_count": len(valid_urls),
                "invalid_count": len(invalid_urls),
                "total_count": len(valid_urls) + len(invalid_urls),
                "valid_urls": valid_urls[:5],  # Sample of valid URLs
                "invalid_urls": invalid_urls[:5] if invalid_urls else [],  # Sample of invalid URLs
                "is_valid": len(valid_urls) > 0
            }
        except BatchProcessorError as e:
            raise BatchUtilsError(f"URLs file validation failed: {e}")
        except Exception as e:
            raise BatchUtilsError(f"Unexpected error validating URLs file: {e}")
    
    def create_sample_urls_file(self, file_path: str) -> bool:
        """Create a sample URLs file for testing.
        
        Args:
            file_path (str): Path where sample file should be created
            
        Returns:
            bool: True if file created successfully, False otherwise
        """
        try:
            sample_content = """# Sample YouTube URLs for Media Knowledge Pipeline
# Add one YouTube URL per line
# Lines starting with # are treated as comments

https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/DLzxrzFCyOs
https://www.youtube.com/watch?v= video_with_spaces (remove spaces)
# Add your own URLs below this line

"""
            
            # Create parent directories if needed
            path_obj = Path(file_path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Write sample content
            with open(path_obj, 'w', encoding='utf-8') as f:
                f.write(sample_content)
            
            return True
        except Exception as e:
            raise BatchUtilsError(f"Failed to create sample URLs file: {e}")
    
    def estimate_processing_time(self, url_count: int, parallel_workers: int = 1) -> dict:
        """Estimate processing time based on URL count and parallel workers.
        
        Args:
            url_count (int): Number of URLs to process
            parallel_workers (int): Number of parallel workers
            
        Returns:
            dict: Time estimates in different units
        """
        # Rough estimate: 30-60 seconds per video (includes download, transcribe, synthesize)
        base_time_per_video = 45  # seconds
        estimated_seconds = (url_count * base_time_per_video) / parallel_workers
        
        return {
            "seconds": round(estimated_seconds),
            "minutes": round(estimated_seconds / 60, 1),
            "hours": round(estimated_seconds / 3600, 2)
        }
    
    def format_batch_summary(self, config: dict) -> str:
        """Format a summary of batch processing configuration.
        
        Args:
            config (dict): Batch processing configuration
            
        Returns:
            str: Formatted summary string
        """
        summary = []
        summary.append("BATCH PROCESSING SUMMARY")
        summary.append("=" * 30)
        summary.append(f"URLs File: {config.get('urls_file', 'Not specified')}")
        summary.append(f"Output Directory: {config.get('output_dir', 'Not specified')}")
        summary.append(f"Parallel Workers: {config.get('parallel_workers', 1)}")
        
        template = config.get('template', 'None')
        if template == 'custom' and config.get('custom_prompt'):
            summary.append(f"Template: Custom ({config['custom_prompt'][:30]}...)")
        elif template:
            summary.append(f"Template: {template}")
        else:
            summary.append("Template: Default")
        
        essay_options = config.get('essay_options', {})
        if essay_options.get('enable_essay'):
            summary.append("Essay Generation: Enabled")
            if essay_options.get('force_essay'):
                summary.append("  Force Essay: Yes")
        else:
            summary.append("Essay Generation: Disabled")
        
        processing_options = config.get('processing_options', {})
        options_summary = []
        if processing_options.get('use_cloud'):
            options_summary.append("Cloud Processing")
        if processing_options.get('quiet'):
            options_summary.append("Quiet Mode")
        if not processing_options.get('organize', True):
            options_summary.append("No Organization")
        
        if options_summary:
            summary.append("Options: " + ", ".join(options_summary))
        
        # Add time estimate
        urls_file = config.get('urls_file')
        if urls_file:
            try:
                validation_result = self.validate_urls_file(urls_file)
                url_count = validation_result['valid_count']
                time_estimate = self.estimate_processing_time(
                    url_count, config.get('parallel_workers', 1)
                )
                summary.append(f"Estimated Time: {time_estimate['minutes']} minutes ({url_count} videos)")
            except:
                pass  # If we can't estimate, just skip this line
        
        return "\n".join(summary)


def main():
    """Main function for testing the batch utilities."""
    print("Batch Utilities for Media Knowledge Pipeline")
    utils = BatchUtilities()
    print("Utilities initialized successfully!")
    
    # Test time estimation
    print("\nTesting time estimation:")
    for count in [1, 5, 10, 20]:
        estimate = utils.estimate_processing_time(count, 2)
        print(f"  {count} videos with 2 workers: {estimate['minutes']} minutes")


if __name__ == "__main__":
    main()