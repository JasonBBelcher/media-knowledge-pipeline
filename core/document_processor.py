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
                        custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Process a document file and synthesize knowledge from its content.
        
        Args:
            file_path: Path to document file (PDF, EPUB, MOBI)
            prompt_template: Template key for synthesis
            custom_prompt: Custom prompt for synthesis
            
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
            
            # Extract metadata
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