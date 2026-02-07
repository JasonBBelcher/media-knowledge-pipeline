"""
Unit tests for essay synthesis functionality.

Tests content cohesion assessment and essay synthesis from multiple sources.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.synthesizer import EssaySynthesizer, KnowledgeSynthesizer, SynthesizerError
from core.prompts import format_template


class MockKnowledgeSynthesizer(KnowledgeSynthesizer):
    """Mock KnowledgeSynthesizer for testing."""
    
    def __init__(self, use_cloud=False):
        # Call parent constructor
        super().__init__(use_cloud=use_cloud)
        self.model = "test-model"
        
    def _call_local_ollama(self, prompt):
        """Mock local Ollama call."""
        if "content_cohesion_check" in prompt:
            # Mock cohesion assessment responses
            if "quantum" in prompt.lower() and "computing" in prompt.lower():
                return "YES"
            elif "quantum" in prompt.lower() and "cooking" in prompt.lower():
                return "NO"
            else:
                return "MARGINAL"
        else:
            # Mock essay synthesis response
            return "This is a synthesized essay combining multiple sources on related topics."
    
    def _call_cloud_ollama(self, prompt):
        """Mock cloud Ollama call (same as local for testing)."""
        return self._call_local_ollama(prompt)


class TestEssaySynthesizer:
    """Test EssaySynthesizer class."""
    
    def test_init(self):
        """Test EssaySynthesizer initialization."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        assert essay_synth.synthesizer == mock_synthesizer
        assert hasattr(essay_synth, 'assess_cohesion')
        assert hasattr(essay_synth, 'synthesize_essay')
    
    @patch('core.synthesizer.format_template')
    def test_assess_cohesion_success(self, mock_format_template):
        """Test successful cohesion assessment."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Mock format_template to return a predictable result
        mock_format_template.return_value = "Test prompt with {transcript}"
        
        # Create mock results with related content
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum computing basics"}
            },
            {
                "status": "success", 
                "synthesis": {"raw_text": "Quantum algorithms explained"}
            }
        ]
        
        result = essay_synth.assess_cohesion(mock_results)
        assert result in ["YES", "NO", "MARGINAL"]
    
    def test_assess_cohesion_insufficient_results(self):
        """Test cohesion assessment with insufficient results."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Only one successful result
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum computing basics"}
            }
        ]
        
        result = essay_synth.assess_cohesion(mock_results)
        assert result == "NO"
    
    def test_assess_cohesion_failed_results(self):
        """Test cohesion assessment with failed results."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Failed results shouldn't affect cohesion assessment
        mock_results = [
            {
                "status": "error",
                "error": "Processing failed"
            },
            {
                "status": "error",
                "error": "Processing failed"
            }
        ]
        
        result = essay_synth.assess_cohesion(mock_results)
        assert result == "NO"
    
    @patch('core.synthesizer.format_template')
    def test_synthesize_essay_success(self, mock_format_template):
        """Test successful essay synthesis."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Mock format_template
        mock_format_template.return_value = "Essay prompt with {individual_summaries} and {combined_transcript}"
        
        # Create mock results
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum computing basics"},
                "transcript": "Transcript about quantum computing"
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum algorithms explained"},
                "transcript": "Transcript about quantum algorithms"
            }
        ]
        
        combined_transcript = "Combined transcript content"
        result = essay_synth.synthesize_essay(mock_results, combined_transcript)
        
        assert "raw_text" in result
        assert "model_used" in result
        assert "template_used" in result
        assert result["template_used"] == "synthesis_essay"
    
    def test_synthesize_essay_insufficient_results(self):
        """Test essay synthesis with insufficient results."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Only one successful result
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum computing basics"},
                "transcript": "Transcript about quantum computing"
            }
        ]
        
        combined_transcript = "Combined transcript content"
        
        with pytest.raises(SynthesizerError, match="Need at least 2 successful synthesis results"):
            essay_synth.synthesize_essay(mock_results, combined_transcript)
    
    def test_synthesize_essay_no_transcript(self):
        """Test essay synthesis with no transcript content."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        # Results without transcript
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Content 1"}
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Content 2"}
            }
        ]
        
        combined_transcript = ""  # Empty transcript
        
        # Should still work with empty transcript
        result = essay_synth.synthesize_essay(mock_results, combined_transcript)
        assert "raw_text" in result


class TestContentCohesionScenarios:
    """Test different content cohesion scenarios."""
    
    def test_related_content_high_cohesion(self):
        """Test highly related content."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Introduction to quantum mechanics"}
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum computing applications"}
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Future of quantum technology"}
            }
        ]
        
        # Mock response for related content
        with patch.object(mock_synthesizer, '_call_local_ollama', return_value="YES"):
            result = essay_synth.assess_cohesion(mock_results)
            assert result == "YES"
    
    def test_unrelated_content_low_cohesion(self):
        """Test unrelated content."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Quantum mechanics principles"}
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Mediterranean cooking recipes"}
            }
        ]
        
        # Mock response for unrelated content
        with patch.object(mock_synthesizer, '_call_local_ollama', return_value="NO"):
            result = essay_synth.assess_cohesion(mock_results)
            assert result == "NO"


class TestIntegration:
    """Integration tests for essay synthesis."""
    
    def test_end_to_end_essay_synthesis(self):
        """Test complete essay synthesis workflow."""
        mock_synthesizer = MockKnowledgeSynthesizer()
        essay_synth = EssaySynthesizer(mock_synthesizer)
        
        mock_results = [
            {
                "status": "success",
                "synthesis": {"raw_text": "Source 1 summary"},
                "transcript": "Transcript 1"
            },
            {
                "status": "success",
                "synthesis": {"raw_text": "Source 2 summary"},
                "transcript": "Transcript 2"
            }
        ]
        
        combined_transcript = "Transcript 1\nTranscript 2"
        
        result = essay_synth.synthesize_essay(mock_results, combined_transcript)
        
        assert result["status"] == "success"
        assert "synthesized essay" in result["raw_text"].lower()
        assert result["sources_count"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])