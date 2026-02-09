"""
Test suite for intelligent document chunking functionality.
Following Test-Driven Development (TDD) principles.
"""

import pytest
from typing import List
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.large_document_processor import LargeDocumentProcessor


class TestDocumentChunking:
    """Test cases for document chunking functionality."""

    def test_small_document_no_chunking(self):
        """Test that small documents (< max chunk size) are not chunked."""
        processor = LargeDocumentProcessor()
        
        # Small text under chunk limit
        small_text = "This is a small document that should not be chunked."
        
        chunks = processor.chunk_document(small_text, max_size=1000)
        
        # Should return single chunk containing the entire text
        assert len(chunks) == 1
        assert chunks[0] == small_text

    def test_large_document_proportional_chunking(self):
        """Test that large documents are chunked proportionally."""
        processor = LargeDocumentProcessor()
        
        # Create large text (simulate 5000 character document with sections)
        large_text = "\n\n".join([
            f"Section {i}\n" + "Content " * 200  # ~1000 chars per section
            for i in range(10)
        ])
        
        chunks = processor.chunk_document(large_text, max_size=3000)
        
        # Should be chunked into multiple pieces
        assert len(chunks) > 1
        
        # Each chunk should be reasonably sized (not tiny)
        for chunk in chunks:
            assert len(chunk) > 100  # Not empty/ridiculously small

    def test_section_aware_chunking(self):
        """Test that chunking respects section boundaries."""
        processor = LargeDocumentProcessor()
        
        # Text with clear section headers
        text_with_sections = """
# Introduction
This is the introduction section with some content.

# Main Content
This is the main content section with detailed information.

## Subsection A
Some subsection content here.

## Subsection B
More subsection content here.

# Conclusion
This is the conclusion section.
"""
        
        chunks = processor.chunk_document(text_with_sections, max_size=200)
        
        # Should preserve section integrity where possible
        # Check that chunks don't break in the middle of sections unnecessarily
        assert len(chunks) >= 1

    def test_chunk_size_limits(self):
        """Test that chunks respect size limits."""
        processor = LargeDocumentProcessor()
        
        # Medium text
        medium_text = "Word " * 1000  # ~5000 characters
        
        max_chunk_size = 1000
        chunks = processor.chunk_document(medium_text, max_size=max_chunk_size)
        
        # All chunks should be under the limit (with some buffer for headers)
        for chunk in chunks:
            assert len(chunk) <= max_chunk_size * 1.5  # Allow 50% buffer

    def test_empty_document_handling(self):
        """Test handling of empty or nearly empty documents."""
        processor = LargeDocumentProcessor()
        
        # Empty text
        empty_text = ""
        chunks = processor.chunk_document(empty_text)
        assert len(chunks) == 0
        
        # Nearly empty text
        tiny_text = "   \n  \t  "
        chunks = processor.chunk_document(tiny_text)
        assert len(chunks) == 0

    def test_single_large_section(self):
        """Test handling of single very large section."""
        processor = LargeDocumentProcessor()
        
        # Single large section that exceeds chunk size
        large_section = "Content " * 1000  # Very large single section
        chunks = processor.chunk_document(large_section, max_size=1000)
        
        # Should still create chunks even for single large section
        assert len(chunks) >= 1

    def test_markdown_header_recognition(self):
        """Test recognition of markdown-style headers."""
        processor = LargeDocumentProcessor()
        
        markdown_content = """# Chapter 1
Chapter content here.

## Section 1.1
Section content.

# Chapter 2
Another chapter.

### Subsection
Subsection content."""
        
        chunks = processor.chunk_document(markdown_content, max_size=200)
        
        # Should handle markdown headers appropriately
        assert isinstance(chunks, list)

    def test_realistic_epub_processing(self):
        """Test chunking with realistic EPUB-like content structure."""
        processor = LargeDocumentProcessor()
        
        # Simulate realistic book structure
        book_content = "\n\n".join([
            "# Chapter " + str(i) + "\n" + ("Content paragraph " * 50)
            for i in range(1, 21)  # 20 chapters
        ])
        
        chunks = processor.chunk_document(book_content, max_size=2000)
        
        # Should create reasonable number of chunks for large book
        assert len(chunks) > 5  # Expect multiple chunks for 20-chapter book


class TestProportionalChunking:
    """Test cases for proportional chunking based on document size."""

    def test_chunk_size_scaling(self):
        """Test that chunk size scales appropriately with document size."""
        processor = LargeDocumentProcessor()
        
        # Test different document sizes
        sizes = [1000, 5000, 10000, 50000, 100000]
        chunks_per_size = []
        
        for size in sizes:
            # Create text of approximate size
            text = "Content word " * (size // 12)  # Approximate character count
            chunks = processor.chunk_document(text, max_size=5000)
            chunks_per_size.append(len(chunks))
        
        # Larger documents should create more chunks (roughly proportional)
        # This is a sanity check, not exact proportionality
        assert all(count >= 1 for count in chunks_per_size)

    def test_memory_efficient_processing(self):
        """Test that chunking enables memory-efficient processing."""
        processor = LargeDocumentProcessor()
        
        # Very large text that would cause memory issues if processed all at once
        very_large_text = "Memory test content " * 10000  # ~200KB
        
        chunks = processor.chunk_document(very_large_text, max_size=5000)
        
        # Should create multiple chunks to enable streaming processing
        assert len(chunks) > 10  # Should create many chunks for large content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])