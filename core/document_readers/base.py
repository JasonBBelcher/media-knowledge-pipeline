"""
Base Document Reader Interface and Factory

Provides the foundation for all document readers in the system.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type
import logging


class DocumentReaderError(Exception):
    """Custom exception for document reader errors."""
    pass


class DocumentReader(ABC):
    """Abstract base class for document readers."""
    
    def __init__(self, file_path: Path):
        """Initialize document reader with file path.
        
        Args:
            file_path: Path to the document file
        """
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    @abstractmethod
    def read_text(self) -> str:
        """Read and extract text content from the document.
        
        Returns:
            Extracted text content
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, str]:
        """Extract document metadata.
        
        Returns:
            Dictionary containing document metadata
        """
        pass
    
    @abstractmethod
    def get_page_count(self) -> int:
        """Get the number of pages in the document.
        
        Returns:
            Page count
        """
        pass
    
    def validate_file(self) -> bool:
        """Validate that the file exists and is readable.
        
        Returns:
            True if file is valid
        """
        if not self.file_path.exists():
            raise DocumentReaderError(f"File does not exist: {self.file_path}")
        
        if not self.file_path.is_file():
            raise DocumentReaderError(f"Path is not a file: {self.file_path}")
        
        try:
            self.file_path.resolve(strict=True)
            return True
        except (OSError, ValueError) as e:
            raise DocumentReaderError(f"File path is invalid: {e}")


class DocumentReaderFactory:
    """Factory class for creating appropriate document readers."""
    
    # Map file extensions to reader classes
    _readers: Dict[str, Type[DocumentReader]] = {}
    
    @classmethod
    def register_reader(cls, extension: str, reader_class: Type[DocumentReader]):
        """Register a document reader for a specific file extension.
        
        Args:
            extension: File extension (e.g., '.pdf', '.epub')
            reader_class: Document reader class
        """
        cls._readers[extension.lower()] = reader_class
    
    @classmethod
    def get_reader(cls, file_path: Path) -> DocumentReader:
        """Get appropriate reader for the given file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            DocumentReader instance
            
        Raises:
            DocumentReaderError: If no reader supports the file format
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Remove leading dot from extension for lookup
        if extension.startswith('.'):
            extension = extension[1:]
        
        reader_class = cls._readers.get(extension)
        if reader_class is None:
            # Try with dot prefix
            reader_class = cls._readers.get(f".{extension}")
        
        if reader_class is None:
            supported_formats = list(cls._readers.keys())
            raise DocumentReaderError(
                f"No document reader available for '{extension}' format. "
                f"Supported formats: {supported_formats}"
            )
        
        return reader_class(file_path)
    
    @classmethod
    def supported_formats(cls) -> List[str]:
        """Get list of supported document formats.
        
        Returns:
            List of supported file extensions
        """
        return list(cls._readers.keys())
    
    @classmethod
    def is_format_supported(cls, file_path: Path) -> bool:
        """Check if the file format is supported.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            True if format is supported
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension.startswith('.'):
            extension = extension[1:]
        
        return extension in cls._readers or f".{extension}" in cls._readers