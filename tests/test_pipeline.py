"""
Integration tests for the Media-to-Knowledge Pipeline.

Tests end-to-end workflow from media file to knowledge synthesis.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import tempfile
import os
import json

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import (
    process_media,
    display_results,
    save_results_to_file,
    main
)


class TestProcessMedia:
    """Test process_media function (main pipeline orchestrator)."""
    
    @pytest.mark.integration
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_process_media_audio_file_success(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test successful processing of audio file."""
        # Setup mocks
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/prepared_audio.wav"
        mock_transcribe.return_value = "This is a test transcript."
        mock_synthesize.return_value = {
            "raw_text": "Synthesized knowledge",
            "model_used": "llama3.1:8b",
            "template_used": "basic_summary",
            "transcript_length": 24,
            "synthesis_length": 20,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = process_media(
                tmp_path,
                prompt_template="basic_summary",
                use_cloud=False
            )
            
            assert result["transcript"] == "This is a test transcript."
            assert result["synthesis"]["raw_text"] == "Synthesized knowledge"
            assert result["synthesis"]["model_used"] == "llama3.1:8b"
            assert result["audio_file"] == tmp_path
            
            # Verify all pipeline steps were called
            mock_validate.assert_called_once_with(tmp_path)
            mock_prepare.assert_called_once()
            mock_transcribe.assert_called_once()
            mock_synthesize.assert_called_once()
        finally:
            os.unlink(tmp_path)
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_process_media_video_file_success(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test successful processing of video file."""
        # Setup mocks
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/extracted_audio.wav"
        mock_transcribe.return_value = "Video transcript content."
        mock_synthesize.return_value = {
            "raw_text": "Video knowledge synthesis",
            "model_used": "llama3.1:8b",
            "template_used": "meeting_minutes",
            "transcript_length": 22,
            "synthesis_length": 23,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = process_media(
                tmp_path,
                prompt_template="meeting_minutes",
                use_cloud=False
            )
            
            assert result["transcript"] == "Video transcript content."
            assert result["synthesis"]["raw_text"] == "Video knowledge synthesis"
            assert result["synthesis"]["template_used"] == "meeting_minutes"
        finally:
            os.unlink(tmp_path)
    
    @patch('main.validate_file_exists')
    def test_process_media_file_not_found(self, mock_validate):
        """Test handling of file not found error."""
        mock_validate.side_effect = Exception("File not found")
        
        with pytest.raises(Exception):
            process_media("/nonexistent/file.mp3")
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_process_media_with_custom_prompt(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test processing with custom prompt."""
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        mock_transcribe.return_value = "Test transcript"
        mock_synthesize.return_value = {
            "raw_text": "Custom synthesis",
            "model_used": "llama3.1:8b",
            "template_used": "custom",
            "transcript_length": 13,
            "synthesis_length": 15,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = process_media(
                tmp_path,
                custom_prompt="Custom: {transcript}",
                use_cloud=False
            )
            
            assert result["synthesis"]["raw_text"] == "Custom synthesis"
            assert result["synthesis"]["template_used"] == "custom"
        finally:
            os.unlink(tmp_path)
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_process_media_with_cloud(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test processing with cloud Ollama."""
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        mock_transcribe.return_value = "Test transcript"
        mock_synthesize.return_value = {
            "raw_text": "Cloud synthesis",
            "model_used": "llama3.1:8b",
            "template_used": "basic_summary",
            "transcript_length": 13,
            "synthesis_length": 14,
            "use_cloud": True
        }
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = process_media(
                tmp_path,
                prompt_template="basic_summary",
                use_cloud=True
            )
            
            assert result["synthesis"]["use_cloud"] is True
        finally:
            os.unlink(tmp_path)


class TestDisplayResults:
    """Test display_results function."""
    
    def test_display_results_basic(self, capsys):
        """Test basic results display."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        display_results(results)
        
        captured = capsys.readouterr()
        assert "Test transcript" in captured.out
        assert "Synthesized text" in captured.out
        assert "llama3.1:8b" in captured.out
    
    def test_display_results_with_metadata(self, capsys):
        """Test results display with metadata."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "meeting_minutes",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        display_results(results)
        
        captured = capsys.readouterr()
        assert "meeting_minutes" in captured.out
        assert "13" in captured.out  # transcript length
        assert "15" in captured.out  # synthesis length
    
    def test_display_results_cloud(self, capsys):
        """Test results display with cloud synthesis."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Cloud synthesis",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 14,
                "use_cloud": True
            },
            "audio_file": "test.mp3"
        }
        
        display_results(results)
        
        captured = capsys.readouterr()
        assert "Cloud" in captured.out or "cloud" in captured.out.lower()


class TestSaveResultsToFile:
    """Test save_results_to_file function."""
    
    def test_save_results_to_file_json(self):
        """Test saving results to JSON file."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            save_results_to_file(results, tmp_path, format='json')
            
            # Verify file was created and contains correct data
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r') as f:
                loaded_data = json.load(f)
            
            assert loaded_data["transcript"] == "Test transcript"
            assert loaded_data["synthesis"]["raw_text"] == "Synthesized text"
        finally:
            os.unlink(tmp_path)
    
    def test_save_results_to_file_txt(self):
        """Test saving results to text file."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            save_results_to_file(results, tmp_path, format='txt')
            
            # Verify file was created
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r') as f:
                content = f.read()
            
            assert "Test transcript" in content
            assert "Synthesized text" in content
        finally:
            os.unlink(tmp_path)
    
    def test_save_results_to_file_creates_directory(self):
        """Test that save_results_to_file creates directory if needed."""
        results = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "subdir", "output.json")
            
            save_results_to_file(results, output_path, format='json')
            
            # Verify file was created in new directory
            assert os.path.exists(output_path)


class TestMainCLI:
    """Test main CLI function."""
    
    @patch('main.save_results_to_file')
    @patch('main.display_results')
    @patch('main.process_media')
    @patch('sys.argv', ['main.py', 'test.mp3', '--template', 'basic_summary'])
    def test_main_cli_basic(self, mock_process, mock_display, mock_save):
        """Test basic CLI execution."""
        mock_process.return_value = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        try:
            main()
        except SystemExit:
            pass  # argparse calls sys.exit
        
        mock_process.assert_called_once()
        mock_display.assert_called_once()
    
    @patch('main.save_results_to_file')
    @patch('main.display_results')
    @patch('main.process_media')
    @patch('sys.argv', ['main.py', 'test.mp3', '--output', 'output.json'])
    def test_main_cli_with_output(self, mock_process, mock_display, mock_save):
        """Test CLI with output file."""
        mock_process.return_value = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Synthesized text",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 15,
                "use_cloud": False
            },
            "audio_file": "test.mp3"
        }
        
        try:
            main()
        except SystemExit:
            pass
        
        mock_save.assert_called_once()
    
    @patch('main.process_media')
    @patch('sys.argv', ['main.py', 'test.mp3', '--cloud'])
    def test_main_cli_with_cloud(self, mock_process):
        """Test CLI with cloud flag."""
        mock_process.return_value = {
            "transcript": "Test transcript",
            "synthesis": {
                "raw_text": "Cloud synthesis",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 13,
                "synthesis_length": 14,
                "use_cloud": True
            },
            "audio_file": "test.mp3"
        }
        
        try:
            main()
        except SystemExit:
            pass
        
        # Verify that process_media was called with use_cloud=True
        call_kwargs = mock_process.call_args[1]
        assert call_kwargs['use_cloud'] is True


class TestPipelineIntegration:
    """Test complete pipeline integration scenarios."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_full_pipeline_audio_to_knowledge(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test complete pipeline from audio file to knowledge."""
        # Setup mocks
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        mock_transcribe.return_value = "This is a comprehensive audio transcript about machine learning and artificial intelligence."
        mock_synthesize.return_value = {
            "raw_text": "The audio discusses key concepts in machine learning and AI, including neural networks, deep learning, and their applications.",
            "model_used": "llama3.1:8b",
            "template_used": "detailed_summary",
            "transcript_length": 95,
            "synthesis_length": 110,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Process media
            result = process_media(tmp_path, prompt_template="detailed_summary", use_cloud=False)
            
            # Verify pipeline steps
            assert "transcript" in result
            assert "synthesis" in result
            assert result["transcript"] == "This is a comprehensive audio transcript about machine learning and artificial intelligence."
            assert result["synthesis"]["raw_text"] == "The audio discusses key concepts in machine learning and AI, including neural networks, deep learning, and their applications."
            
            # Verify all mocks were called in correct order
            mock_validate.assert_called_once()
            mock_prepare.assert_called_once()
            mock_transcribe.assert_called_once()
            mock_synthesize.assert_called_once()
        finally:
            os.unlink(tmp_path)
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_full_pipeline_with_output_file(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test complete pipeline with output file saving."""
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        mock_transcribe.return_value = "Meeting transcript about project milestones."
        mock_synthesize.return_value = {
            "raw_text": "Project milestones discussed include Q1 deliverables and Q2 planning.",
            "model_used": "llama3.1:8b",
            "template_used": "meeting_minutes",
            "transcript_length": 45,
            "synthesis_length": 70,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_tmp:
            output_path = output_tmp.name
        
        try:
            # Process media
            result = process_media(tmp_path, prompt_template="meeting_minutes", use_cloud=False)
            
            # Save results
            save_results_to_file(result, output_path, format='json')
            
            # Verify output file
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["transcript"] == "Meeting transcript about project milestones."
            assert saved_data["synthesis"]["raw_text"] == "Project milestones discussed include Q1 deliverables and Q2 planning."
        finally:
            os.unlink(tmp_path)
            os.unlink(output_path)
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_full_pipeline_error_handling(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test pipeline error handling."""
        mock_validate.return_value = True
        mock_prepare.side_effect = Exception("Audio preparation failed")
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Process media should raise exception
            with pytest.raises(Exception):
                process_media(tmp_path, use_cloud=False)
            
            # Verify that transcription and synthesis were not called
            mock_transcribe.assert_not_called()
            mock_synthesize.assert_not_called()
        finally:
            os.unlink(tmp_path)


class TestPipelineEdgeCases:
    """Test pipeline edge cases."""
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_pipeline_empty_transcript(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test pipeline with empty transcript."""
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        mock_transcribe.return_value = ""
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Synthesis should handle empty transcript
            mock_synthesize.return_value = {
                "raw_text": "No content to synthesize",
                "model_used": "llama3.1:8b",
                "template_used": "basic_summary",
                "transcript_length": 0,
                "synthesis_length": 25,
                "use_cloud": False
            }
            
            result = process_media(tmp_path, use_cloud=False)
            
            assert result["transcript"] == ""
            assert result["synthesis"]["transcript_length"] == 0
        finally:
            os.unlink(tmp_path)
    
    @patch('main.synthesize')
    @patch('main.transcribe_audio')
    @patch('main.prepare_audio')
    @patch('main.validate_file_exists')
    def test_pipeline_long_transcript(self, mock_validate, mock_prepare, mock_transcribe, mock_synthesize):
        """Test pipeline with very long transcript."""
        mock_validate.return_value = True
        mock_prepare.return_value = "/tmp/audio.wav"
        
        # Create a long transcript
        long_transcript = "This is a sentence. " * 1000
        mock_transcribe.return_value = long_transcript
        
        mock_synthesize.return_value = {
            "raw_text": "Summary of long content",
            "model_used": "llama3.1:8b",
            "template_used": "basic_summary",
            "transcript_length": len(long_transcript),
            "synthesis_length": 23,
            "use_cloud": False
        }
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = process_media(tmp_path, use_cloud=False)
            
            assert len(result["transcript"]) == len(long_transcript)
            assert result["synthesis"]["transcript_length"] == len(long_transcript)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])