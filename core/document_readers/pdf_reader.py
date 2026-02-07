"""
PDF Document Reader using PyMuPDF (fitz)

Extracts text content and metadata from PDF files.
"""

from pathlib import Path
from typing import Dict, List

from .base import DocumentReader, DocumentReaderError


try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


class PDFReader(DocumentReader):
    """PDF document reader using PyMuPDF."""
    
    def __init__(self, file_path: Path):
        """Initialize PDF reader.
        
        Args:
            file_path: Path to PDF file
        """
        super().__init__(file_path)
        
        if not HAS_PYMUPDF:
            raise DocumentReaderError(
                "PyMuPDF (fitz) is not installed. Please install it with: pip install PyMuPDF"
            )
        
        self._doc = None
    
    def _open_document(self):
        """Open the PDF document."""
        if self._doc is None:
            try:
                self._doc = fitz.open(str(self.file_path))
            except Exception as e:
                raise DocumentReaderError(f"Failed to open PDF file: {e}")
    
    def read_text(self) -> str:
        """Extract text content from PDF.
        
        Returns:
            Extracted text content
        """
        self.validate_file()
        self._open_document()
        
        try:
            text_parts = []
            
            for page_num in range(len(self._doc)):
                page = self._doc.load_page(page_num)
                text = page.get_text("text")
                
                if text:
                    # Clean up extracted text
                    text = text.strip()
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            raise DocumentReaderError(f"Failed to extract text from PDF: {e}")
    
    def get_metadata(self) -> Dict[str, str]:
        """Extract PDF metadata.
        
        Returns:
            Dictionary containing PDF metadata
        """
        self.validate_file()
        self._open_document()
        
        try:
            metadata = self._doc.metadata
            
            # Convert metadata to string values and clean up
            result = {}
            for key, value in metadata.items():
                if value:
                    result[key] = str(value).strip()
            
            # Add additional useful information
            result["page_count"] = str(len(self._doc))
            result["file_size"] = str(self.file_path.stat().st_size)
            
            return result
            
        except Exception as e:
            self.logger.warning(f"Failed to extract PDF metadata: {e}")
            return {}
    
    def get_page_count(self) -> int:
        """Get the number of pages in the PDF.
        
        Returns:
            Page count
        """
        self.validate_file()
        self._open_document()
        
        return len(self._doc)
    
    def __del__(self):
        """Clean up document resources."""
        if self._doc:
            self._doc.close()
    
    def get_toc(self) -> List[Dict]:
        """Get table of contents.
        
        Returns:
            List of table of contents entries
        """
        self.validate_file()
        self._open_document()
        
        try:
            toc = self._doc.get_toc()
            return [{"level": item[0], "title": item[1], "page": item[2]} for item in toc]
        except Exception as e:
            self.logger.warning(f"Failed to extract TOC: {e}")
            return []
    
    def extract_images(self) -> List[Dict]:
        """Extract images from PDF.
        
        Returns:
            List of image information dictionaries
        """
        self.validate_file()
        self._open_document()
        
        try:
            images = []
            
            for page_num in range(len(self._doc)):
                page = self._doc.load_page(page_num)
                image_list = page.get_images()
                
                for img in image_list:
                    images.append({
                        "page": page_num + 1,
                        "xref": img[0],
                        "smask": img[1],
                        "width": img[2],
                        "height": img[3],
                        "bpc": img[4],
                        "colorspace": img[5],
                        "alt": img[6] if len(img) > 6 else "",
                        "name": img[7] if len(img) > 7 else ""
                    })
            
            return images
            
        except Exception as e:
            self.logger.warning(f"Failed to extract images: {e}")
            return []