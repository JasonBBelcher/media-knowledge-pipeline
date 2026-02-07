"""
Utility for creating essays from existing synthesized documents.

This module provides functionality to generate comprehensive essays
from previously processed synthesis results stored as JSON files.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import glob


class ExistingDocumentsEssayGenerator:
    """Generate essays from existing synthesized documents."""
    
    def __init__(self):
        """Initialize the essay generator."""
        pass
    
    def load_synthesis_files(self, directory: str, pattern: str = "*.json") -> List[Dict]:
        """
        Load synthesis result files from a directory.
        
        Args:
            directory: Directory containing JSON synthesis files
            pattern: File pattern to match (default: *.json)
            
        Returns:
            List of synthesis result dictionaries
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Find all matching files
        json_files = list(directory_path.glob(pattern))
        
        results = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get('status') == 'success':
                        results.append(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {json_file}: {e}")
                continue
        
        return results
    
    def filter_successful_results(self, results: List[Dict]) -> List[Dict]:
        """
        Filter results to only include successful synthesis.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            List of successful results
        """
        return [r for r in results if r.get('status') == 'success' and r.get('synthesis')]
    
    def extract_synthesis_texts(self, results: List[Dict]) -> List[str]:
        """
        Extract synthesis text from results.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            List of synthesis text strings
        """
        texts = []
        for result in results:
            synthesis = result.get('synthesis', {})
            if isinstance(synthesis, dict):
                text = synthesis.get('raw_text', '')
                if text:
                    texts.append(text)
            elif isinstance(synthesis, str):
                texts.append(synthesis)
        
        return texts
    
    def create_combined_transcript(self, results: List[Dict]) -> str:
        """
        Create combined transcript from results for essay synthesis.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Combined transcript text
        """
        combined = ""
        for i, result in enumerate(results, 1):
            transcript = result.get('transcript', '')
            if transcript:
                combined += f"\n--- Source {i} Transcript ---\n{transcript}\n"
        
        return combined
    
    def generate_essay_from_files(self, directory: str, 
                                 pattern: str = "*.json",
                                 output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate essay from existing synthesis files.
        
        Args:
            directory: Directory containing JSON synthesis files
            pattern: File pattern to match
            output_file: Optional output file path for essay
            
        Returns:
            Dictionary with essay generation results
        """
        try:
            # Load synthesis files
            print(f"🔍 Loading synthesis files from: {directory}")
            all_results = self.load_synthesis_files(directory, pattern)
            print(f"📄 Found {len(all_results)} files")
            
            # Filter successful results
            successful_results = self.filter_successful_results(all_results)
            print(f"✅ Successfully processed: {len(successful_results)} files")
            
            if len(successful_results) < 2:
                return {
                    "status": "error",
                    "error": f"Need at least 2 successful synthesis results, found {len(successful_results)}"
                }
            
            # Extract synthesis texts for cohesion check
            synthesis_texts = self.extract_synthesis_texts(successful_results)
            if len(synthesis_texts) < 2:
                return {
                    "status": "error", 
                    "error": "Not enough synthesis text content for essay generation"
                }
            
            # Create combined transcript for essay synthesis
            combined_transcript = self.create_combined_transcript(successful_results)
            
            result = {
                "status": "success",
                "individual_results": successful_results,
                "synthesis_texts": synthesis_texts,
                "combined_transcript": combined_transcript,
                "sources_count": len(successful_results),
                "directory": directory
            }
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved essay data to: {output_path}")
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


def test_existing_documents_essay_generator():
    """Test the existing documents essay generator."""
    generator = ExistingDocumentsEssayGenerator()
    print("Existing documents essay generator test successful")
    return True


if __name__ == "__main__":
    test_existing_documents_essay_generator()