"""
Document Readers Package

Contains format-specific readers for various document types.
"""

from .base import DocumentReaderFactory, DocumentReaderError
from .pdf_reader import PDFReader
from .epub_reader import EPUBReader
from .mobi_reader import MOBIReader

# Register all document readers
DocumentReaderFactory.register_reader("pdf", PDFReader)
DocumentReaderFactory.register_reader("epub", EPUBReader)
DocumentReaderFactory.register_reader("mobi", MOBIReader)

__all__ = [
    "DocumentReaderFactory",
    "DocumentReaderError", 
    "PDFReader",
    "EPUBReader",
    "MOBIReader"
]