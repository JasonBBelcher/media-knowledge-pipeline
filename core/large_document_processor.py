#!/usr/bin/env python3
"""
Large Document Processor for Educational Cliff Notes

This script processes large technical documents by intelligently chunking them,
synthesizing educational content from each chunk, and combining the results
into comprehensive educational cliff notes that actually teach concepts.
"""

import json
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.document_readers import DocumentReaderFactory
from core.synthesizer import KnowledgeSynthesizer


class LargeDocumentProcessor:
    """Process large documents with intelligent chunking and educational synthesis."""
    
    def __init__(self, use_cloud: bool = False):
        """Initialize the processor with synthesis capabilities."""
        self.synthesizer = KnowledgeSynthesizer(use_cloud=use_cloud)
        self.max_chunk_size = 15000  # Characters per chunk to stay within token limits
        
    def read_document(self, file_path: str) -> str:
        """Read document content using appropriate reader."""
        reader = DocumentReaderFactory.get_reader(Path(file_path))
        return reader.read_text()
    
    def chunk_document(self, text: str, max_size: Optional[int] = None) -> List[str]:
        """
        Intelligently chunk document while preserving section boundaries.
        
        Args:
            text: Full document text
            max_size: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        if max_size is None:
            max_size = self.max_chunk_size
            
        # If document is smaller than max size, return as single chunk
        if len(text) <= max_size:
            return [text] if text.strip() else []
            
        # Split by major section breaks first
        sections = re.split(r'(?:\n#{1,3} |\n[A-Z][^.!?]*\n={3,}|\n[A-Z][^.!?]*\n-{3,})', text)
        
        # If splitting by sections doesn't help, split by paragraphs
        if len(sections) <= 1 or any(len(section) > max_size * 0.8 for section in sections if section.strip()):
            # Split by paragraphs instead
            sections = re.split(r'\n\s*\n', text)
        
        chunks = []
        current_chunk = ""
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # If this single section is already too large, we need to split it further
            if len(section) > max_size:
                # Split large section into smaller parts
                words = section.split()
                temp_chunk = ""
                
                for word in words:
                    if len(temp_chunk) + len(word) + 1 <= max_size:
                        temp_chunk += word + " "
                    else:
                        if temp_chunk.strip():
                            chunks.append(temp_chunk.strip())
                        temp_chunk = word + " "
                
                # Don't forget the last part
                if temp_chunk.strip():
                    chunks.append(temp_chunk.strip())
                continue
            
            # If adding this section would exceed chunk size substantially
            if len(current_chunk) + len(section) > max_size and current_chunk:
                # Add current chunk and start new one
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = section
            else:
                # Add to current chunk with separator
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section
        
        # Don't forget the last chunk
        if current_chunk and current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        # Ensure no chunk exceeds max_size (last resort forced splitting)
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_size:
                # Force split by words
                words = chunk.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) + 1 <= max_size:
                        temp_chunk += word + " "
                    else:
                        if temp_chunk.strip():
                            final_chunks.append(temp_chunk.strip())
                        temp_chunk = word + " "
                if temp_chunk.strip():
                    final_chunks.append(temp_chunk.strip())
            else:
                final_chunks.append(chunk)
                
        return final_chunks
    
    def synthesize_chunk(self, chunk: str, chunk_index: int, total_chunks: int) -> Dict[str, Any]:
        """
        Synthesize educational content from a document chunk.
        
        Args:
            chunk: Text chunk to process
            chunk_index: Index of this chunk (0-based)
            total_chunks: Total number of chunks
            
        Returns:
            Dictionary with synthesis results
        """
        print(f"Processing chunk {chunk_index + 1}/{total_chunks} ({len(chunk)} chars)...")
        
        try:
            # Use lecture summary template as default for educational content
            result = self.synthesizer.synthesize(
                transcript=chunk,
                prompt_template='lecture_summary'  # Good for educational content
            )
            
            return {
                'status': 'success',
                'chunk_index': chunk_index,
                'chunk_size': len(chunk),
                'synthesis': result,
                'model_used': result.get('model_used', 'unknown')
            }
        except Exception as e:
            print(f"Error synthesizing chunk {chunk_index + 1}: {e}")
            return {
                'status': 'error',
                'chunk_index': chunk_index,
                'error': str(e),
                'chunk_size': len(chunk)
            }
    
    def combine_syntheses(self, chunk_results: List[Dict]) -> str:
        """
        Combine chunk syntheses into comprehensive educational content.
        
        Args:
            chunk_results: List of synthesis results from chunks
            
        Returns:
            Combined educational content as markdown
        """
        successful_results = [r for r in chunk_results if r['status'] == 'success']
        
        if not successful_results:
            return "# Educational Content Processing Failed\n\nNo successful chunk processing results."
        
        # Create comprehensive educational content
        output_lines = [
            "# Educational Cliff Notes",
            "",
            f"*Generated from {len(chunk_results)} document chunks*",
            f"*Successfully processed {len(successful_results)} chunks*",
            "",
            "## Table of Contents",
            ""
        ]
        
        # Extract key concepts from successful syntheses
        all_concepts = []
        all_takeaways = []
        chunk_summaries = []
        
        for i, result in enumerate(successful_results):
            synthesis_text = result['synthesis'].get('raw_text', '')
            if synthesis_text:
                # Extract headers as concepts
                concepts = re.findall(r'#{1,3}\s+(.+)', synthesis_text)
                all_concepts.extend(concepts)
                
                # Extract key takeaways section
                takeaways_match = re.search(r'[Kk]ey [Tt]akeaways(.+?)(?:\n\n|\Z)', synthesis_text, re.DOTALL)
                if takeaways_match:
                    takeaways = takeaways_match.group(1).strip()
                    all_takeaways.append((i+1, takeaways))
                
                # Extract main summary
                lines = synthesis_text.split('\n')
                if lines:
                    first_line = lines[0].strip('# ')
                    chunk_summaries.append(f"{i+1}. {first_line}")
        
        # Add table of contents
        for i, summary in enumerate(chunk_summaries, 1):
            output_lines.append(f"- {summary}")
        
        output_lines.extend([
            "",
            "## Core Concepts Covered",
            ""
        ])
        
        # Add unique concepts
        unique_concepts = list(dict.fromkeys([c.strip() for c in all_concepts if c.strip()]))
        for concept in unique_concepts[:20]:  # Limit to top 20
            output_lines.append(f"- {concept}")
        
        output_lines.extend([
            "",
            "## Comprehensive Summary",
            ""
        ])
        
        # Add content from each successful chunk
        for i, result in enumerate(successful_results):
            synthesis_text = result['synthesis'].get('raw_text', '')
            if synthesis_text:
                output_lines.extend([
                    f"### Section {i+1} Summary",
                    "",
                    synthesis_text,
                    ""
                ])
        
        if all_takeaways:
            output_lines.extend([
                "## Key Takeaways Across All Sections",
                ""
            ])
            
            for section_num, takeaways in all_takeaways:
                output_lines.extend([
                    f"**From Section {section_num}**:",
                    takeaways,
                    ""
                ])
        
        output_lines.extend([
            "",
            "## Meta Information",
            "",
            f"- **Chunks Processed**: {len(chunk_results)}",
            f"- **Successful Syntheses**: {len(successful_results)}",
            f"- **Processing Method**: Intelligent chunking with educational synthesis",
            "- **Focus**: Core concepts, learning objectives, and practical application"
        ])
        
        return "\n".join(output_lines)
    
    def process_document(self, file_path: str, output_file: Optional[str] = None) -> str:
        """
        Process large document and generate educational cliff notes.
        
        Args:
            file_path: Path to document file
            output_file: Optional path to save results
            
        Returns:
            Generated educational content as string
        """
        print(f"Processing large document: {file_path}")
        
        # Read document
        start_time = time.time()
        document_text = self.read_document(file_path)
        read_time = time.time() - start_time
        
        print(f"✓ Document loaded ({len(document_text):,} characters) in {read_time:.2f}s")
        
        # Chunk document
        print("Intelligently chunking document...")
        chunks = self.chunk_document(document_text)
        print(f"✓ Split into {len(chunks)} chunks for processing")
        
        # Process chunks
        chunk_results = []
        for i, chunk in enumerate(chunks):
            result = self.synthesize_chunk(chunk, i, len(chunks))
            chunk_results.append(result)
            
            # Brief pause to avoid overwhelming the model
            time.sleep(0.5)
        
        # Combine results
        print("Combining chunk syntheses into comprehensive educational content...")
        combined_content = self.combine_syntheses(chunk_results)
        
        # Save if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(combined_content)
            print(f"✓ Educational content saved to: {output_file}")
        
        processing_time = time.time() - start_time
        print(f"✓ Total processing time: {processing_time:.2f} seconds")
        
        return combined_content


def main():
    """Main function to process the large EPUB document."""
    epub_path = '/Users/jasonbelcher/Documents/code/ai-notes/technical-docs/dokumen.pub_agentic-design-patterns-a-hands-on-guide-to-building-intelligent-systems.epub'
    
    print("=" * 70)
    print("LARGE DOCUMENT EDUCATIONAL PROCESSOR")
    print("=" * 70)
    print("Goal: Transform 400+ page technical book into educational cliff notes")
    print("Method: Intelligent chunking + educational synthesis")
    print("=" * 70)
    
    try:
        # Initialize processor
        processor = LargeDocumentProcessor(use_cloud=False)
        
        # Ensure outputs directory exists
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Process document with proper output path
        output_file_path = output_dir / "AGENTIC_DESIGN_PATTERNS_EDUCATIONAL_NOTES.md"
        educational_content = processor.process_document(
            epub_path, 
            output_file=str(output_file_path)
        )
        
        print("\n" + "=" * 70)
        print("GENERATED EDUCATIONAL CONTENT (Preview)")
        print("=" * 70)
        print(educational_content[:2000] + "..." if len(educational_content) > 2000 else educational_content)
        
        print(f"\n✅ SUCCESSFULLY GENERATED EDUCATIONAL CLIFF NOTES!")
        print(f"📝 Full content saved to: {output_file_path}")
        
    except Exception as e:
        print(f"\n❌ Error processing document: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()