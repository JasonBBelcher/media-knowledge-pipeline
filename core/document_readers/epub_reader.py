"""
EPUB Document Reader using ebooklib

Extracts text content and metadata from EPUB files.
"""

from pathlib import Path
from typing import Dict, List
import html
import re

from .base import DocumentReader, DocumentReaderError


try:
    import ebooklib
    from ebooklib import epub
    from ebooklib.utils import debug
    HAS_EBOOKLIB = True
except ImportError:
    HAS_EBOOKLIB = False


class EPUBReader(DocumentReader):
    """EPUB document reader using ebooklib."""
    
    def __init__(self, file_path: Path):
        """Initialize EPUB reader.
        
        Args:
            file_path: Path to EPUB file
        """
        super().__init__(file_path)
        
        if not HAS_EBOOKLIB:
            raise DocumentReaderError(
                "ebooklib is not installed. Please install it with: pip install ebooklib"
            )
        
        self._book = None
    
    def _open_book(self):
        """Open the EPUB book."""
        if self._book is None:
            try:
                self._book = epub.read_epub(str(self.file_path))
            except Exception as e:
                raise DocumentReaderError(f"Failed to open EPUB file: {e}")
    
    def _clean_html_text(self, html_content: str) -> str:
        """Clean HTML content and extract text.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Cleaned text content
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def read_text(self) -> str:
        """Extract text content from EPUB.
        
        Returns:
            Extracted text content
        """
        self.validate_file()
        self._open_book()
        
        try:
            text_parts = []
            
            # Get all items that are text content
            for item in self._book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Extract content as bytes
                    content_bytes = item.get_content()
                    try:
                        # Try to decode as UTF-8
                        content = content_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Fallback to latin-1
                        content = content_bytes.decode('latin-1', errors='ignore')
                    
                    # Clean the HTML content
                    cleaned_text = self._clean_html_text(content)
                    
                    if cleaned_text:
                        text_parts.append(cleaned_text)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            raise DocumentReaderError(f"Failed to extract text from EPUB: {e}")
    
    def get_metadata(self) -> Dict[str, str]:
        """Extract EPUB metadata.
        
        Returns:
            Dictionary containing EPUB metadata
        """
        self.validate_file()
        self._open_book()
        
        try:
            metadata = {}
            
            # Extract metadata from EPUB metadata object
            for key, value in self._book.get_metadata("DC", None).items():
                if isinstance(value, (list, tuple)):
                    metadata[str(key)] = ", ".join(str(v) for v in value if v)
                elif value:
                    metadata[str(key)] = str(value)
            
            # Add additional useful information
            metadata["page_count"] = "Variable"  # EPUB doesn't have fixed page count
            metadata["file_size"] = str(self.file_path.stat().st_size)
            metadata["language"] = self._book.get_metadata("DC", "language")[0][0] if self._book.get_metadata("DC", "language") else "unknown"
            
            # Extract title
            titles = self._book.get_metadata("DC", "title")
            if titles:
                metadata["title"] = titles[0][0]
            
            # Extract author
            authors = self._book.get_metadata("DC", "creator")
            if authors:
                metadata["author"] = authors[0][0]
            
            # Clean up metadata values
            for key in metadata:
                metadata[key] = metadata[key].strip() if metadata[key] else ""
            
            return metadata
            
        except Exception as e:
            self.logger.warning(f"Failed to extract EPUB metadata: {e}")
            return {}
    
    def get_page_count(self) -> int:
        """Get approximate page count for EPUB (estimated).
        
        Returns:
            Estimated page count based on character count
        """
        self.validate_file()
        self._open_book()
        
        try:
            # Estimate pages based on text length (rough estimate)
            text = self.read_text()
            
            # Rough estimate: 250 words per page
            words = len(text.split())
            estimated_pages = max(1, words // 250)
            
            return estimated_pages
            
        except Exception as e:
            self.logger.warning(f"Failed to estimate EPUB page count: {e}")
            return 1
    
    def get_chapters(self) -> List[Dict]:
        """Get EPUB chapters/structure.
        
        Returns:
            List of chapter information
        """
        self.validate_file()
        self._open_book()
        
        try:
            chapters = []
            spine_items = self._book.spine
            
            for spine_ref in spine_items:
                if hasattr(spine_ref, 'id') and spine_ref.id:
                    item = self._book.get_item_by_id(spine_ref.id)
                    
                    if item:
                        # Extract chapter title from item content
                        content_bytes = item.get_content()
                        try:
                            content = content_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            content = content_bytes.decode('latin-1', errors='ignore')
                        
                        # Extract title from HTML
                        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
                        title = title_match.group(1) if title_match else "Chapter"
                        
                        chapters.append({
                            "id": spine_ref.id,
                            "title": html.unescape(title),
                            "file": item.get_name()
                        })
            
            return chapters
            
        except Exception as e:
            self.logger.warning(f"Failed to extract chapters: {e}")
            return []