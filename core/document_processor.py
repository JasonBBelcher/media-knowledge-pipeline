"""
Document Processor Module

Handles processing of various document formats (PDF, EPUB, MOBI) for knowledge synthesis.
This module integrates document reading capabilities with the existing knowledge synthesis pipeline.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from core.document_readers import DocumentReaderFactory, DocumentReaderError
from core.synthesizer import KnowledgeSynthesizer


class DocumentProcessorError(Exception):
    """Custom exception for document processor errors."""
    pass


class DocumentProcessor:
    """Processes documents and synthesizes knowledge from their content."""
    
    def __init__(self, use_cloud: bool = False):
        """Initialize document processor.
        
        Args:
            use_cloud: Whether to use cloud Ollama models
        """
        self.logger = logging.getLogger("DocumentProcessor")
        self.synthesizer = KnowledgeSynthesizer(use_cloud=use_cloud)
    
    def process_document(self, 
                        file_path: Path,
                        prompt_template: Optional[str] = None,
                        custom_prompt: Optional[str] = None,
                        max_chunk_size: int = 15000) -> Dict[str, Any]:
        """Process a document file and synthesize knowledge from its content.
        
        Args:
            file_path: Path to document file (PDF, EPUB, MOBI)
            prompt_template: Template key for synthesis
            custom_prompt: Custom prompt for synthesis
            max_chunk_size: Maximum characters per chunk for large documents
            
        Returns:
            Dictionary containing:
                - original_file: Path to source document
                - extracted_text: Raw text extracted from document
                - synthesis: The synthesized knowledge
                - metadata: Document metadata
                - processing_stats: Processing statistics
                
        Raises:
            DocumentProcessorError: If processing fails
        """
        try:
            # Validate file exists
            if not file_path.exists():
                raise DocumentProcessorError(f"Document file not found: {file_path}")
            
            file_size = file_path.stat().st_size
            self.logger.info(f"Processing document: {file_path.name} ({file_size:,} bytes)")
            
            # Get appropriate document reader
            try:
                reader = DocumentReaderFactory.get_reader(file_path)
            except DocumentReaderError as e:
                raise DocumentProcessorError(f"Unsupported document format: {e}")
            
            # Extract text content from document
            try:
                extracted_text = reader.read_text()
                self.logger.info(f"Extracted {len(extracted_text):,} characters from document")
            except Exception as e:
                raise DocumentProcessorError(f"Failed to extract text from document: {e}")
            
            # For very large documents, use chunking strategy to avoid token limits
            LARGE_DOCUMENT_THRESHOLD = 50000  # 50K characters threshold
            if len(extracted_text) > LARGE_DOCUMENT_THRESHOLD:
                self.logger.info(f"Large document detected ({len(extracted_text):,} chars), using chunking strategy")
                return self._process_large_document(
                    file_path, extracted_text, prompt_template, custom_prompt, max_chunk_size
                )
            
            # Extract metadata
            page_count = 0
            try:
                metadata = reader.get_metadata()
                page_count = reader.get_page_count()
                metadata["page_count"] = str(page_count)
            except Exception as e:
                self.logger.warning(f"Failed to extract metadata: {e}")
                metadata = {}
            
            # Synthesize knowledge from extracted text
            try:
                synthesis_result = self.synthesizer.synthesize(
                    transcript=extracted_text,
                    prompt_template=prompt_template,
                    custom_prompt=custom_prompt
                )
            except Exception as e:
                raise DocumentProcessorError(f"Synthesis failed: {e}")
            
            # Compile results
            result = {
                "status": "success",
                "original_file": str(file_path),
                "extracted_text": extracted_text,
                "synthesis": synthesis_result,
                "metadata": metadata,
                "processing_stats": {
                    "file_size": file_size,
                    "extracted_characters": len(extracted_text),
                    "synthesis_model": synthesis_result.get("model_used", "unknown"),
                    "page_count": page_count
                }
            }
            
            self.logger.info(f"Successfully processed document: {file_path.name}")
            return result
            
        except Exception as e:
            error_msg = f"Document processing failed for {file_path}: {e}"
            self.logger.error(error_msg)
            return {
                "status": "error",
                "original_file": str(file_path),
                "error": str(e),
                "processing_stats": {
                    "file_size": file_path.stat().st_size if file_path.exists() else 0
                }
            }
    
    def _process_large_document(self,
                               file_path: Path,
                               text: str,
                               prompt_template: Optional[str],
                               custom_prompt: Optional[str],
                               max_chunk_size: int) -> Dict[str, Any]:
        """Process large document using intelligent chunking strategy.
        
        Args:
            file_path: Path to document file
            text: Extracted document text
            prompt_template: Template key for synthesis
            custom_prompt: Custom prompt for synthesis
            max_chunk_size: Maximum characters per chunk
            
        Returns:
            Dictionary containing processing results with combined synthesis
        """
        # Import chunking processor (avoiding circular imports)
        import sys
        from pathlib import Path as PPath
        
        # Dynamically import the large document processor
        project_root = PPath(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        try:
            from core.large_document_processor import LargeDocumentProcessor
        except ImportError:
            # Fallback if direct import fails
            sys.path.insert(0, str(project_root))
            from core.large_document_processor import LargeDocumentProcessor
        
        self.logger.info(f"Processing large document with chunking strategy: {len(text):,} characters")
        
        # Use our intelligent chunking processor
        chunk_processor = LargeDocumentProcessor(use_cloud=getattr(self.synthesizer, 'use_cloud', False))
        
        # Chunk the document intelligently
        chunks = chunk_processor.chunk_document(text, max_size=max_chunk_size)
        self.logger.info(f"Split document into {len(chunks)} chunks for processing")
        
        # Process chunks individually and collect results
        chunk_results = []
        successful_chunks = 0
        
        for i, chunk in enumerate(chunks):
            self.logger.debug(f"Processing chunk {i+1}/{len(chunks)} ({len(chunk):,} chars)")
            try:
                # Process each chunk with synthesis
                chunk_result = chunk_processor.synthesize_chunk(chunk, i, len(chunks))
                chunk_results.append(chunk_result)
                
                if chunk_result['status'] == 'success':
                    successful_chunks += 1
                    self.logger.debug(f"Chunk {i+1} processed successfully with {chunk_result['model_used']}")
                else:
                    self.logger.warning(f"Chunk {i+1} failed: {chunk_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                self.logger.error(f"Error processing chunk {i+1}: {e}")
                chunk_results.append({
                    'status': 'error',
                    'chunk_index': i,
                    'error': str(e),
                    'chunk_size': len(chunk)
                })
        
        # Combine successful chunk syntheses
        try:
            combined_content = chunk_processor.combine_syntheses(chunk_results)
            self.logger.info(f"Combined {successful_chunks}/{len(chunks)} chunk syntheses successfully")
        except Exception as e:
            self.logger.error(f"Failed to combine chunk syntheses: {e}")
            combined_content = f"# Large Document Processing Results\\n\\nProcessed {len(chunks)} chunks with {successful_chunks} successful syntheses.\\n\\nError combining results: {e}"
        
        # Create synthesis-like result structure
        synthesis_result = {
            "raw_text": combined_content,
            "model_used": "chunked_processing",
            "synthesis_length": len(combined_content),
            "template_used": prompt_template or "large_document_default"
        }
        
        # Return results in same format as regular processing
        return {
            "status": "success",
            "original_file": str(file_path),
            "extracted_text": text[:1000] + f"... (truncated, full text: {len(text):,} chars in {len(chunks)} chunks)",
            "synthesis": synthesis_result,
            "metadata": {
                "page_count": "Multiple chunks",
                "chunk_count": len(chunks),
                "successful_chunks": successful_chunks,
                "failed_chunks": len(chunks) - successful_chunks
            },
            "processing_stats": {
                "file_size": file_path.stat().st_size,
                "extracted_characters": len(text),
                "chunks_processed": len(chunks),
                "successful_chunks": successful_chunks,
                "synthesis_model": "chunked_processing"
            }
        }
    
    def batch_process_documents(self, 
                               file_paths: list[Path],
                               prompt_template: Optional[str] = None,
                               custom_prompt: Optional[str] = None) -> list[Dict[str, Any]]:
        """Process multiple documents in batch.
        
        Args:
            file_paths: List of paths to document files
            prompt_template: Template key for synthesis
            custom_prompt: Custom prompt for synthesis
            
        Returns:
            List of processing results
        """
        results = []
        
        for file_path in file_paths:
            result = self.process_document(file_path, prompt_template, custom_prompt)
            results.append(result)
        
        # Generate batch summary
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]
        
        self.logger.info(f"Batch processing complete: {len(successful)} successful, {len(failed)} failed")
        
        return results
    
    def get_supported_formats(self) -> list[str]:
        """Get list of supported document formats.
        
        Returns:
            List of supported file extensions
        """
        return DocumentReaderFactory.supported_formats()
    
    def is_format_supported(self, file_path: Path) -> bool:
        """Check if a document format is supported.
        
        Args:
            file_path: Path to document file
            
        Returns:
            True if format is supported
        """
        return DocumentReaderFactory.is_format_supported(file_path)


def test_document_processor():
    """Test the document processor with different formats."""
    processor = DocumentProcessor()
    
    print("Supported formats:", processor.get_supported_formats())
    
    # Test with a sample document
    # This would need actual documents to test properly
    print("Document processor test completed - requires actual documents for full testing")
    

if __name__ == "__main__":
    test_document_processor()