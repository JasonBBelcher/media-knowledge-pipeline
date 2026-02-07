"""
Folder Organizer Utilities

Provides intelligent folder organization for media processing outputs.
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re


class FolderOrganizer:
    """Organizes output files into logical folder structures."""
    
    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize folder organizer.
        
        Args:
            base_output_dir: Base directory for organized output
        """
        self.base_output_dir = Path(base_output_dir)
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_safe_folder_name(self, title: str, max_length: int = 50) -> str:
        """
        Create a safe folder name from a title.
        
        Args:
            title: Title to convert to folder name
            max_length: Maximum length of folder name
            
        Returns:
            Safe folder name
        """
        if not title:
            return "untitled"
        
        # Remove or replace unsafe characters
        safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title)
        
        # Remove extra whitespace and limit length
        safe_title = re.sub(r'\s+', '_', safe_title.strip())
        safe_title = safe_title[:max_length]
        
        # Ensure it's not empty
        if not safe_title:
            return "untitled"
        
        return safe_title
    
    def organize_playlist(self, playlist_videos: List[Dict], 
                         playlist_title: Optional[str] = None) -> Path:
        """
        Create organized folder structure for playlist processing.
        
        Args:
            playlist_videos: List of video dictionaries with metadata
            playlist_title: Optional playlist title for folder name
            
        Returns:
            Path to playlist output directory
        """
        # Create playlist folder name
        if playlist_title:
            playlist_folder_name = f"playlist_{self.create_safe_folder_name(playlist_title)}"
        else:
            playlist_folder_name = f"playlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        playlist_dir = self.base_output_dir / playlist_folder_name
        playlist_dir.mkdir(parents=True, exist_ok=True)
        
        # Create individual video folders
        for i, video in enumerate(playlist_videos, 1):
            video_title = video.get('title', f'video_{i}')
            video_folder_name = f"{i:03d}_{self.create_safe_folder_name(video_title)}"
            video_dir = playlist_dir / video_folder_name
            video_dir.mkdir(parents=True, exist_ok=True)
        
        return playlist_dir
    
    def organize_batch(self, urls: List[str], 
                      batch_name: Optional[str] = None) -> Path:
        """
        Create organized folder structure for batch processing.
        
        Args:
            urls: List of URLs being processed
            batch_name: Optional custom batch name
            
        Returns:
            Path to batch output directory
        """
        # Create batch folder name
        if batch_name:
            batch_folder_name = f"batch_{self.create_safe_folder_name(batch_name)}"
        else:
            batch_folder_name = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        batch_dir = self.base_output_dir / batch_folder_name
        batch_dir.mkdir(parents=True, exist_ok=True)
        
        # Create individual URL folders (we'll name them as we process)
        return batch_dir
    
    def create_ordered_video_folder(self, batch_dir: Path, order: int, 
                                  video_title: str) -> Path:
        """
        Create an ordered folder for a specific video in a batch.
        
        Args:
            batch_dir: Parent batch directory
            order: Order number (1-based)
            video_title: Video title for folder name
            
        Returns:
            Path to video output directory
        """
        video_folder_name = f"{order:03d}_{self.create_safe_folder_name(video_title)}"
        video_dir = batch_dir / video_folder_name
        video_dir.mkdir(parents=True, exist_ok=True)
        return video_dir
    
    def get_essay_output_path(self, parent_dir: Path, 
                             source_count: int) -> Path:
        """
        Get standardized path for essay output.
        
        Args:
            parent_dir: Parent directory for essay
            source_count: Number of sources in essay
            
        Returns:
            Path for essay file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        essay_filename = f"comprehensive_analysis_{source_count}_sources_{timestamp}.md"
        return parent_dir / essay_filename


def test_folder_organizer():
    """Test folder organizer functionality."""
    organizer = FolderOrganizer("test_outputs")
    
    # Test safe folder name creation
    safe_name = organizer.create_safe_folder_name("Test/Title: With Special Characters!")
    print(f"Safe folder name: {safe_name}")
    
    # Test playlist organization
    playlist_videos = [
        {"title": "Introduction to AI"},
        {"title": "Machine Learning Basics"},
        {"title": "Deep Learning Applications"}
    ]
    
    playlist_dir = organizer.organize_playlist(playlist_videos, "AI_Learning_Series")
    print(f"Playlist directory: {playlist_dir}")
    
    # Test batch organization
    urls = ["https://youtube.com/watch?v=1", "https://youtube.com/watch?v=2"]
    batch_dir = organizer.organize_batch(urls, "Learning_Batch")
    print(f"Batch directory: {batch_dir}")
    
    # Test ordered video folder creation
    video_dir = organizer.create_ordered_video_folder(batch_dir, 1, "First Video")
    print(f"Video directory: {video_dir}")
    
    return True


if __name__ == "__main__":
    test_folder_organizer()