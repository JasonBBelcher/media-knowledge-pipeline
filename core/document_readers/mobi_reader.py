"""
MOBI Document Reader

Extracts text content and metadata from MOBI files.
"""

from pathlib import Path
from typing import Dict, List
import tempfile
import os

from .base import DocumentReader, DocumentReaderError


try:
    import mobi
    HAS_MOBI = True
except ImportError:
    HAS_MOBI = False


class MOBIReader(DocumentReader):
    """MOBI document reader."""
    
    def __init__(self, file_path: Path):
        """Initialize MOBI reader.
        
        Args:
            file_path: Path to MOBI file
        """
        super().__init__(file_path)
        
        if not HAS_MOBI:
            raise DocumentReaderError(
                "mobi library is not installed. Please install it with: pip install mobi"
            )
        
        self._temp_dir = None
    
    def read_text(self) -> str:
        """Extract text content from MOBI.
        
        Returns:
            Extracted text content
        """
        self.validate_file()
        
        try:
            # Extract MOBI content to temporary directory
            self._temp_dir = tempfile.mkdtemp()
            
            # Use mobi.extract to unpack the file
            temp_dir, filepath = mobi.extract(str(self.file_path))
            
            # Look for HTML content in the extracted files
            text_content = ""
            
            # Search for HTML files in the extracted directory
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.html') or file.endswith('.htm'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                html_content = f.read()
                                # Extract text from HTML (simple approach)
                                import re
                                text = re.sub(r'<[^>]+>', ' ', html_content)
                                text = re.sub(r'\s+', ' ', text).strip()
                                text_content += text + "\n\n"
                        except Exception as e:
                            self.logger.warning(f"Failed to read {file_path}: {e}")
            
            # Clean up temporary directory
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            if not text_content:
                # If no HTML found, try to read the file directly
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text_content = f.read()
                except:
                    # Last resort: read as binary and decode
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        try:
                            text_content = content.decode('utf-8')
                        except UnicodeDecodeError:
                            text_content = content.decode('latin-1', errors='ignore')
            
            return text_content.strip()
            
        except Exception as e:
            # Clean up on error
            if self._temp_dir and os.path.exists(self._temp_dir):
                import shutil
                shutil.rmtree(self._temp_dir, ignore_errors=True)
            raise DocumentReaderError(f"Failed to extract text from MOBI: {e}")
    
    def get_metadata(self) -> Dict[str, str]:
        """Extract MOBI metadata.
        
        Returns:
            Dictionary containing MOBI metadata
        """
        self.validate_file()
        
        try:
            metadata = {}
            
            # Extract basic file metadata
            metadata["file_size"] = str(self.file_path.stat().st_size)
            metadata["file_name"] = self.file_path.name
            
            # Try to get page count estimate from text content
            try:
                text = self.read_text()
                words = len(text.split())
                metadata["estimated_pages"] = str(max(1, words // 250))
                metadata["word_count"] = str(words)
                metadata["character_count"] = str(len(text))
            except:
                metadata["estimated_pages"] = "Unknown"
            
            # Clean up metadata values
            for key in metadata:
                metadata[key] = metadata[key].strip() if metadata[key] else ""
            
            return metadata
            
        except Exception as e:
            self.logger.warning(f"Failed to extract MOBI metadata: {e}")
            return {}
    
    def get_page_count(self) -> int:
        """Get approximate page count for MOBI (estimated).
        
        Returns:
            Estimated page count based on character count
        """
        self.validate_file()
        
        try:
            # Estimate pages based on text length (rough estimate)
            text = self.read_text()
            
            # Rough estimate: 250 words per page
            words = len(text.split())
            estimated_pages = max(1, words // 250)
            
            return estimated_pages
            
        except Exception as e:
            self.logger.warning(f"Failed to estimate MOBI page count: {e}")
            return 1