#!/usr/bin/env python3
"""
Media-to-Knowledge Pipeline - Main Orchestrator

This script processes video or audio files through a pipeline:
1. Extract/prepare audio from media file
2. Transcribe audio to text using Whisper
3. Synthesize knowledge from transcript using Ollama

Usage:
    python main.py --input /path/to/media.mp4
    python main.py --input /path/to/audio.mp3 --cloud
    python main.py --input /path/to/video.mov --prompt meeting_minutes
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from core.media_preprocessor import prepare_audio, MediaPreprocessorError
from core.transcriber import transcribe_audio, TranscriberError
from core.synthesizer import KnowledgeSynthesizer, SynthesizerError
from config import get_config


def print_separator(char: str = "=", length: int = 80) -> None:
    """Print a separator line."""
    print(char * length)


def print_section(title: str) -> None:
    """Print a section header."""
    print_separator()
    print(f"\n{title}\n")
    print_separator()


def save_results_to_file(results: Dict[str, Any], output_path: str) -> None:
    """
    Save results to a JSON file.
    
    Args:
        results: Dictionary containing pipeline results.
        output_path: Path to the output file.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {output_path}")


def generate_intelligent_json_filename(results: Dict[str, Any], base_dir: str = "outputs") -> str:
    """
    Generate an intelligent filename for JSON output based on synthesis content.
    
    Args:
        results: Dictionary containing pipeline results.
        base_dir: Base directory for output files (default: "outputs").
        
    Returns:
        Path to the JSON output file with intelligent filename.
    """
    # Use the same LLM-based approach as markdown generation
    if results["status"] != "success" or not results["synthesis"]:
        # Fallback to timestamp-based naming if synthesis failed
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_dir}/results_{timestamp}.json"
    
    # Extract synthesis text
    synthesis_text = results["synthesis"]["raw_text"]
    
    # Generate descriptive filename using LLM based on the synthesis content
    try:
        # Initialize synthesizer to get model connection
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        
        # Check if we can connect to the model
        if synthesizer.test_connection():
            # Create a custom prompt for filename generation
            filename_prompt = f"""Based on the synthesized content below, provide a short, descriptive subject line that would be suitable as a filename (3-5 words maximum). Focus on the core topic or main concept discussed:

{synthesis_text}

Examples of good subjects:
- "second_brain_productivity"
- "ai_meeting_summarization"
- "cognitive_offloading_systems"
- "productivity_workflow_optimization"

Respond with ONLY the subject, no other text."""
            
            # Generate filename subject using the model with a direct prompt (bypass templates)
            filename_result = synthesizer.synthesize(
                transcript=synthesis_text,
                custom_prompt=filename_prompt
            )
            
            # Extract filename from response
            if filename_result and "raw_text" in filename_result:
                generated_subject = filename_result["raw_text"].split('\n')[0].strip()
                # Clean for filename safety
                filename = "".join(c for c in generated_subject if c.isalnum() or c in ('_', '-')).lower()
                if filename and len(filename) >= 3:
                    return f"{base_dir}/{filename}_results.json"
                else:
                    raise ValueError("Generated filename too short")
            else:
                raise ValueError("No response from model")
        else:
            raise ConnectionError("Cannot connect to model")
    except Exception as e:
        # Fallback to source-based naming with timestamp
        print(f"Warning: Could not generate JSON filename with LLM ({e}), using source-based naming")
        source_file = Path(results.get('media_file', 'unknown_source'))
        if source_file.name != 'unknown_source':
            base_name = source_file.stem
            # Extract meaningful part from source filename
            source_parts = [part for part in base_name.split('-') if len(part) > 2][:2]
            if source_parts:
                filename = f"{'_'.join(source_parts)}"
            else:
                filename = base_name[:20]
        else:
            # For YouTube or other sources, use timestamp
            filename = "youtube_results" if "youtube" in str(source_file).lower() else "results"
        
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_dir}/{filename}_{timestamp}.json"


def save_synthesis_to_markdown(results: Dict[str, Any], output_dir: str = "outputs/markdown") -> None:
    """
    Save synthesized text to a markdown file with subject as filename.
    
    Args:
        results: Dictionary containing pipeline results.
        output_dir: Directory to save markdown files (default: "outputs/markdown").
    """
    if results["status"] != "success" or not results["synthesis"]:
        return
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Extract synthesis text
    synthesis_text = results["synthesis"]["raw_text"]
    
    # Generate descriptive filename using LLM based on the synthesis content
    try:
        # Initialize synthesizer to get model connection
        synthesizer = KnowledgeSynthesizer(use_cloud=False)
        
        # Check if we can connect to the model
        if synthesizer.test_connection():
            # Create a custom prompt for filename generation
            filename_prompt = f"""Based on the synthesized content below, provide a short, descriptive subject line that would be suitable as a filename (3-5 words maximum). Focus on the core topic or main concept discussed:

{synthesis_text}

Examples of good subjects:
- "second_brain_productivity"
- "ai_meeting_summarization"
- "cognitive_offloading_systems"
- "productivity_workflow_optimization"

Respond with ONLY the subject, no other text."""
            
            # Generate filename subject using the model with a direct prompt (bypass templates)
            # We'll create a minimal synthesis result for just the filename
            filename_result = synthesizer.synthesize(
                transcript=synthesis_text,
                custom_prompt=filename_prompt
            )
            
            # Extract filename from response
            if filename_result and "raw_text" in filename_result:
                generated_subject = filename_result["raw_text"].split('\n')[0].strip()
                # Clean for filename safety
                filename = "".join(c for c in generated_subject if c.isalnum() or c in ('_', '-')).lower()
                if filename and len(filename) >= 3:
                    print(f"✓ Generated descriptive filename with LLM: {filename}")
                else:
                    raise ValueError("Generated filename too short")
            else:
                raise ValueError("No response from model")
        else:
            raise ConnectionError("Cannot connect to model")
    except Exception as e:
        # Fallback to our improved heuristic approach
        print(f"Warning: Could not generate filename with LLM ({e}), using heuristic approach")
        
        # Our improved logic from before
        lines = synthesis_text.split('\n')
        subject = "knowledge_synthesis"  # default fallback
        
        for i, line in enumerate(lines):
            # Found the Core Thesis section header
            if "**Core Thesis**" in line.strip():
                # Look at the next line for the actual thesis content
                if i + 1 < len(lines):
                    thesis_content = lines[i + 1].strip()
                    if thesis_content and not thesis_content.startswith(('-', '*', '#')):
                        # Clean the thesis content for use as filename subject
                        clean_content = thesis_content.replace('*', '').replace('"', '').strip()
                        if clean_content:
                            subject = clean_content[:60].strip()  # Take first 60 chars
                            break
        
        # Additional enhancement - if we have a generic subject, make it more specific
        if subject == "knowledge_synthesis" or len(subject) < 10:
            # Try a more general approach by looking for the first substantial sentence
            for line in lines:
                clean_line = line.strip().replace('*', '').replace('#', '').replace('"', '')
                if (clean_line and 
                    len(clean_line) > 30 and
                    not clean_line.startswith(('-', '##', '**')) and
                    any(word in clean_line.lower() for word in ["argue", "explain", "suggest", "describe", "focus", "system", "approach"])):
                    subject = clean_line[:60].strip()
                    break
        
        # Final fallback to original logic
        if subject == "knowledge_synthesis":
            first_line = synthesis_text.split('\n')[0].strip('#* ')
            subject = first_line[:60].strip() if first_line else "knowledge_synthesis"
        
        # Enhanced cleaning for better filename generation
        # Focus on key concepts from the thesis
        key_concepts = []
        if "second brain" in subject.lower():
            key_concepts.append("second_brain")
        elif "ai" in subject.lower() or "artificial intelligence" in subject.lower():
            key_concepts.append("ai_systems")
        elif "productivity" in subject.lower() or "cognitive" in subject.lower():
            key_concepts.append("productivity")
        elif "system" in subject.lower():
            key_concepts.append("systems")
        
        # If we found key concepts, use them for filename
        if key_concepts:
            filename = "_".join(key_concepts)
        else:
            # Original cleaning approach as fallback
            filename = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = filename.replace(' ', '_').lower()
            
            # Limit length but ensure we get meaningful content
            if len(filename) > 30:
                # Try to preserve important words at beginning and end
                parts = filename.split('_')
                if len(parts) > 3:
                    # Take first 2 and last 1 parts
                    filename = "_".join(parts[:2] + [parts[-1]])[:30]
                else:
                    filename = filename[:30].rstrip('_')
        
        # Ensure filename isn't too generic
        if filename in ["knowledge_synthesis", "core_thesis", ""] or len(filename) < 3:
            # Append source identifier if available
            import os
            source_file = results.get('media_file', 'unknown_source')
            if source_file != 'unknown_source':
                base_name = os.path.splitext(os.path.basename(source_file))[0]
                # Extract meaningful part from source filename
                source_parts = [part for part in base_name.split('-') if len(part) > 2][:2]
                if source_parts:
                    filename = f"{'_'.join(source_parts)}_synthesis"[:40]
                else:
                    filename = base_name[:20] + "_synthesis"
            else:
                filename = "knowledge_synthesis"
        
        # Final safety check to ensure valid filename
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-')).lower()
        if not filename or filename == "":
            filename = "knowledge_synthesis"
    
    # Ensure we have a valid filename with meaningful length
    if not filename or len(filename) < 3:
        filename = "knowledge_synthesis"
    
    # Use refined subject for main heading with fallback to original logic
    main_heading = synthesis_text.split('\n')[0].strip('#* ')
    if not main_heading or main_heading.strip() == "":
        main_heading = "Knowledge Synthesis Results"
    
    # Create markdown content
    md_content = f"""# {main_heading}

## Source
- File: {results.get('media_file', 'Unknown')}
- Processing Time: {results.get('processing_time', 0):.2f} seconds
- Transcript Length: {results.get('transcript_length', 0):,} characters
- Model Used: {results.get('model_used', 'Unknown')}

## Synthesized Knowledge

{synthesis_text}

---
*Generated by Media-to-Knowledge Pipeline*
"""
    
    # Handle duplicate filenames by adding timestamp
    md_file_path = output_path / f"{filename}.md"
    if md_file_path.exists():
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_file_path = output_path / f"{filename}_{timestamp}.md"
    
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ Synthesis saved to markdown: {md_file_path}")




def process_media(
    media_path: str,
    use_cloud_synth: bool = False,
    prompt_template: Optional[str] = None,
    custom_prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a media file through the complete pipeline.
    
    This function orchestrates the entire media-to-knowledge pipeline:
    1. Prepare audio from media file (extract or convert)
    2. Transcribe audio to text using Whisper
    3. Synthesize knowledge from transcript using Ollama
    
    Args:
        media_path: Path to video or audio file.
        use_cloud_synth: Whether to use Ollama Cloud for synthesis.
        prompt_template: Optional prompt template key (e.g., 'meeting_minutes').
        custom_prompt: Optional custom prompt text (overrides prompt_template).
    
    Returns:
        Dictionary containing:
            - status: 'success' or 'error'
            - media_file: Path to input media file
            - audio_file: Path to prepared audio file
            - transcript: Transcribed text
            - transcript_length: Length of transcript
            - synthesis: Synthesized knowledge
            - model_used: Ollama model used
            - template_used: Prompt template used
            - processing_time: Total processing time in seconds
            - error: Error message if status is 'error'
    
    Raises:
        MediaPreprocessorError: If media preprocessing fails.
        TranscriberError: If transcription fails.
        SynthesizerError: If synthesis fails.
    
    Example:
        >>> results = process_media("video.mp4", use_cloud_synth=False)
        >>> print(results["synthesis"]["raw_text"])
    """
    start_time = datetime.now()
    results = {
        "status": "success",
        "media_file": media_path,
        "audio_file": None,
        "transcript": None,
        "transcript_length": 0,
        "synthesis": None,
        "model_used": None,
        "template_used": None,
        "processing_time": 0,
        "error": None
    }
    
    # Create temporary directory for intermediate files
    with tempfile.TemporaryDirectory(prefix="media_knowledge_") as temp_dir:
        try:
            # Step 1: Prepare audio from media file
            print_section("STEP 1: Media Preprocessing")
            print(f"Input file: {media_path}")
            
            audio_path = prepare_audio(media_path, temp_dir)
            results["audio_file"] = audio_path
            print(f"✓ Audio prepared: {audio_path}")
            
            # Step 2: Transcribe audio to text
            print_section("STEP 2: Speech-to-Text Transcription")
            
            config = get_config(use_cloud=False)
            transcript = transcribe_audio(
                audio_path,
                model_size=config.whisper_model_size
            )
            results["transcript"] = transcript
            results["transcript_length"] = len(transcript)
            print(f"✓ Transcription complete: {len(transcript)} characters")
            
            # Step 3: Synthesize knowledge from transcript
            print_section("STEP 3: Knowledge Synthesis")
            
            synthesizer = KnowledgeSynthesizer(use_cloud=use_cloud_synth)
            
            # Test connection before synthesis
            if not synthesizer.test_connection():
                raise SynthesizerError(
                    f"Cannot connect to Ollama. "
                    f"Ensure Ollama is running: 'ollama serve'"
                )
            
            synthesis_result = synthesizer.synthesize(
                transcript=transcript,
                prompt_template=prompt_template,
                custom_prompt=custom_prompt
            )
            
            results["synthesis"] = synthesis_result
            results["model_used"] = synthesis_result["model_used"]
            results["template_used"] = synthesis_result["template_used"]
            
            print(f"✓ Synthesis complete: {synthesis_result['synthesis_length']} characters")
            
        except (MediaPreprocessorError, TranscriberError, SynthesizerError) as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"\n✗ Error: {e}")
            return results
    
    # Calculate total processing time
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    results["processing_time"] = processing_time
    
    return results


def display_results(results: Dict[str, Any]) -> None:
    """
    Display pipeline results in a readable format.
    
    Args:
        results: Dictionary containing pipeline results.
    """
    print_section("PIPELINE RESULTS")
    
    if results["status"] == "error":
        print(f"Status: ✗ Failed")
        print(f"Error: {results['error']}")
        return
    
    print(f"Status: ✓ Success")
    print(f"Processing Time: {results['processing_time']:.2f} seconds")
    print(f"\nInput File: {results['media_file']}")
    print(f"Audio File: {results['audio_file']}")
    print(f"Transcript Length: {results['transcript_length']:,} characters")
    print(f"Model Used: {results['model_used']}")
    print(f"Template Used: {results['template_used']}")
    
    if results["synthesis"]:
        print_section("SYNTHESIZED KNOWLEDGE")
        print(results["synthesis"]["raw_text"])
    
    print_separator()


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Media-to-Knowledge Pipeline: Extract and synthesize knowledge from video/audio files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
 Examples:
  # Process a video file with local Ollama
  python main.py --input video.mp4
  
  # Process an audio file with cloud Ollama
  python main.py --input audio.mp3 --cloud
  
  # Process a YouTube video directly
  python main.py --input "https://www.youtube.com/watch?v=..."
  
  # Use a specific prompt template
  python main.py --input meeting.mp4 --prompt meeting_minutes
  
  # Save results to a JSON file
  python main.py --input lecture.mp4 --output results.json
  
  # Save synthesis to markdown file
  python main.py --input lecture.mp4 --markdown outputs/markdown
  
  # Save both JSON and markdown
  python main.py --input lecture.mp4 --output results.json --markdown outputs/markdown
  
  # Use a custom prompt
  python main.py --input interview.mp4 --prompt "Summarize the key points: {transcript}"
  
  # Scan Downloads directory for media files
  python main.py scan
  
  # Watch Downloads directory for new media files
  python main.py watch
  
  # Scan a custom directory
  python main.py scan --directory /path/to/media
  
   # Watch with custom poll interval
  python main.py watch --interval 10
  
  # Process multiple YouTube URLs from a file
  python main.py batch --urls youtube_urls.txt --markdown outputs/markdown

 Available prompt templates:
  basic_summary, meeting_minutes, lecture_summary, tutorial_guide,
  project_update, customer_feedback, research_summary, interview_summary,
  blog_post_outline, social_media_content, technical_documentation, bug_report_summary
        """
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to execute"
    )
    
    # Process command (original functionality)
    process_parser = subparsers.add_parser(
        "process",
        help="Process a single media file"
    )
    process_parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to video or audio file to process, or YouTube URL"
    )
    process_parser.add_argument(
        "--cloud",
        action="store_true",
        help="Use Ollama Cloud for knowledge synthesis (default: local)"
    )
    process_parser.add_argument(
        "--prompt", "-p",
        help="Prompt template key (e.g., 'meeting_minutes') or custom prompt text"
    )
    process_parser.add_argument(
        "--output", "-o",
        help="Optional output file path for results (JSON format)"
    )
    process_parser.add_argument(
        "--markdown", "-m",
        help="Optional directory path for markdown output (default: outputs/markdown)"
    )
    process_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress detailed output, only show final results"
    )
    
    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan directory for media files and copy to data directories"
    )
    scan_parser.add_argument(
        "--directory", "-d",
        default="~/Downloads",
        help="Directory to scan (default: ~/Downloads)"
    )
    scan_parser.add_argument(
        "--audio-dir",
        default="data/audio",
        help="Directory for audio files (default: data/audio)"
    )
    scan_parser.add_argument(
        "--video-dir",
        default="data/videos",
        help="Directory for video files (default: data/videos)"
    )
    scan_parser.add_argument(
        "--process",
        action="store_true",
        help="Automatically process copied files through the pipeline"
    )
    scan_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without actually copying files"
    )
    scan_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress detailed output"
    )
    
    # Watch command
    watch_parser = subparsers.add_parser(
        "watch",
        help="Continuously watch directory for new media files"
    )
    watch_parser.add_argument(
        "--directory", "-d",
        default="~/Downloads",
        help="Directory to watch (default: ~/Downloads)"
    )
    watch_parser.add_argument(
        "--audio-dir",
        default="data/audio",
        help="Directory for audio files (default: data/audio)"
    )
    watch_parser.add_argument(
        "--video-dir",
        default="data/videos",
        help="Directory for video files (default: data/videos)"
    )
    watch_parser.add_argument(
        "--process",
        action="store_true",
        help="Automatically process copied files through the pipeline"
    )
    watch_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without actually copying files"
    )
    watch_parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Poll interval in seconds (default: 5)"
    )
    watch_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress detailed output"
    )
    
    # Batch command for processing multiple YouTube URLs
    batch_parser = subparsers.add_parser(
        "batch",
        help="Process multiple YouTube URLs from a file"
    )
    batch_parser.add_argument(
        "--urls", "-u",
        required=True,
        help="Path to file containing YouTube URLs (one per line)"
    )
    batch_parser.add_argument(
        "--output-dir", "-o",
        default="outputs",
        help="Directory for output files (default: outputs)"
    )
    batch_parser.add_argument(
        "--cloud",
        action="store_true",
        help="Use Ollama Cloud for knowledge synthesis (default: local)"
    )
    batch_parser.add_argument(
        "--prompt", "-p",
        help="Prompt template key (e.g., 'meeting_minutes') or custom prompt text"
    )
    batch_parser.add_argument(
        "--markdown", "-m",
        help="Optional directory path for markdown outputs (default: outputs/markdown)"
    )
    batch_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress detailed output, only show final results"
    )
    batch_parser.add_argument(
        "--parallel", "-j",
        type=int,
        default=1,
        help="Number of parallel processes (default: 1, sequential processing)"
    )
    
    args = parser.parse_args()
    
    # Handle different commands
    if args.command == "process":
        # Original processing functionality
        _handle_process_command(args)
    elif args.command == "scan":
        # Scan directory for media files
        _handle_scan_command(args)
    elif args.command == "watch":
        # Watch directory for new media files
        _handle_watch_command(args)
    elif args.command == "batch":
        # Process multiple YouTube URLs
        _handle_batch_command(args)
    else:
        # Default to process command for backward compatibility
        _handle_process_command(args)


def _handle_process_command(args):
    """Handle the process command (original functionality)."""
    # Validate input file exists (unless it's a YouTube URL)
    from core.media_preprocessor import is_youtube_url
    if not is_youtube_url(args.input) and not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Print header
    if not args.quiet:
        print_separator()
        print("Media-to-Knowledge Pipeline")
        print_separator()
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_separator()
    
    # Process the media file
    try:
        results = process_media(
            media_path=args.input,
            use_cloud_synth=args.cloud,
            prompt_template=args.prompt if args.prompt and not args.prompt.startswith("Summarize") else None,
            custom_prompt=args.prompt if args.prompt and args.prompt.startswith("Summarize") else None
        )
        
        # Display or save results
        if args.output:
            save_results_to_file(results, args.output)
        elif args.markdown:
            # Save to markdown only - but still create JSON for consistency
            json_output_path = generate_intelligent_json_filename(results)
            save_results_to_file(results, json_output_path)
            # Save to markdown
            save_synthesis_to_markdown(results, args.markdown)
            if not args.quiet:
                display_results(results)
                print(f"✓ JSON results also saved to: {json_output_path}")
        else:
            # No explicit output specified, generate intelligent filename
            json_output_path = generate_intelligent_json_filename(results)
            save_results_to_file(results, json_output_path)
            if not args.quiet:
                display_results(results)
                print(f"✓ Results saved to: {json_output_path}")
        
        # Save to markdown if requested (in addition to JSON)
        if args.markdown and args.output:
            save_synthesis_to_markdown(results, args.markdown)
        
        # Exit with appropriate code
        if results["status"] == "error":
            sys.exit(1)
        else:
            if not args.quiet:
                print(f"\n✓ Pipeline completed successfully!")
                print(f"Total processing time: {results['processing_time']:.2f} seconds")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def _handle_scan_command(args):
    """Handle the scan command."""
    try:
        from core.file_scanner import FileScanner
        
        # Print header
        if not args.quiet:
            print_separator()
            print("Media-to-Knowledge Pipeline - File Scanner")
            print_separator()
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Scanning directory: {args.directory}")
            print(f"Audio destination: {args.audio_dir}")
            print(f"Video destination: {args.video_dir}")
            if args.process:
                print("Auto-processing: ENABLED")
            if args.dry_run:
                print("Dry run: ENABLED (no files will be copied)")
            print_separator()
        
        # Define processing callback if auto-process is enabled
        process_callback = None
        if args.process:
            def process_file(file_path):
                if not args.quiet:
                    print(f"Processing file: {file_path.name}")
                
                # Use the existing process_media function
                results = process_media(
                    media_path=str(file_path),
                    use_cloud_synth=False,  # Use local by default
                    prompt_template=None
                )
                
                if results["status"] == "success":
                    # Generate intelligent JSON filename
                    json_output = generate_intelligent_json_filename(results)
                    markdown_dir = "outputs/markdown"
                    
                    # Save JSON results
                    save_results_to_file(results, json_output)
                    
                    # Save markdown synthesis
                    save_synthesis_to_markdown(results, markdown_dir)
                    
                    if not args.quiet:
                        print(f"✓ Processing completed: {file_path.name}")
                        print(f"  JSON output: {json_output}")
                        print(f"  Markdown output: {markdown_dir}/")
                else:
                    print(f"✗ Processing failed: {file_path.name} - {results['error']}")
            
            process_callback = process_file
        
        # Create scanner instance
        scanner = FileScanner(
            scan_directory=args.directory,
            audio_directory=args.audio_dir,
            video_directory=args.video_dir,
            auto_process=args.process,
            process_callback=process_callback,
            dry_run=args.dry_run
        )
        
        # Perform scan
        results = scanner.scan_directory_for_media()
        
        # Display summary
        if not args.quiet:
            print_separator()
            print("SCAN SUMMARY")
            print_separator()
            
            copied_files = [r for r in results if r.status == "copied"]
            dry_run_files = [r for r in results if r.status == "dry_run"]
            skipped_files = [r for r in results if r.status == "skipped"]
            error_files = [r for r in results if r.status == "error"]
            
            print(f"Files processed: {len(results)}")
            if args.dry_run:
                print(f"Files that would be copied: {len(dry_run_files)}")
            else:
                print(f"Files copied: {len(copied_files)}")
            print(f"Files skipped: {len(skipped_files)}")
            print(f"Files with errors: {len(error_files)}")
            
            if copied_files:
                print("\nCopied files:")
                for result in copied_files:
                    print(f"  ✓ {result.file_path.name} -> {result.destination}")
            
            if dry_run_files:
                print("\nFiles that would be copied (dry run):")
                for result in dry_run_files:
                    print(f"  📋 {result.file_path.name} -> {result.destination}")
            
            if skipped_files:
                print("\nSkipped files (already exist):")
                for result in skipped_files:
                    print(f"  ⚠ {result.file_path.name}")
            
            if error_files:
                print("\nFiles with errors:")
                for result in error_files:
                    print(f"  ✗ {result.file_path.name}: {result.error_message}")
            
            print_separator()
            if args.dry_run:
                print("✓ Dry run completed successfully!")
            else:
                print("✓ Scan completed successfully!")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n✗ Scan interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error during scan: {e}", file=sys.stderr)
        sys.exit(1)

 
def _handle_watch_command(args):
    """Handle the watch command."""
    try:
        from core.file_scanner import FileScanner
        
        # Print header
        if not args.quiet:
            print_separator()
            print("Media-to-Knowledge Pipeline - File Watcher")
            print_separator()
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Watching directory: {args.directory}")
            print(f"Audio destination: {args.audio_dir}")
            print(f"Video destination: {args.video_dir}")
            print(f"Poll interval: {args.interval} seconds")
            if args.process:
                print("Auto-processing: ENABLED")
            if args.dry_run:
                print("Dry run: ENABLED (no files will be copied)")
            print_separator()
            print("Press Ctrl+C to stop watching")
            print_separator()
        
        # Define processing callback if auto-process is enabled
        process_callback = None
        if args.process:
            def process_file(file_path):
                if not args.quiet:
                    print(f"Processing file: {file_path.name}")
                
                # Use the existing process_media function
                results = process_media(
                    media_path=str(file_path),
                    use_cloud_synth=False,  # Use local by default
                    prompt_template=None
                )
                
                if results["status"] == "success":
                    # Generate intelligent JSON filename
                    json_output = generate_intelligent_json_filename(results)
                    markdown_dir = "outputs/markdown"
                    
                    # Save JSON results
                    save_results_to_file(results, json_output)
                    
                    # Save markdown synthesis
                    save_synthesis_to_markdown(results, markdown_dir)
                    
                    if not args.quiet:
                        print(f"✓ Processing completed: {file_path.name}")
                        print(f"  JSON output: {json_output}")
                        print(f"  Markdown output: {markdown_dir}/")
                else:
                    print(f"✗ Processing failed: {file_path.name} - {results['error']}")
            
            process_callback = process_file
        
        # Create scanner instance
        scanner = FileScanner(
            scan_directory=args.directory,
            audio_directory=args.audio_dir,
            video_directory=args.video_dir,
            auto_process=args.process,
            process_callback=process_callback,
            dry_run=args.dry_run
        )
        
        # Define callback for file processing
        def on_file_processed(result):
            if not args.quiet:
                if result.status == "copied":
                    print(f"✓ Copied {result.file_type} file: {result.file_path.name}")
                elif result.status == "dry_run":
                    print(f"📋 Would copy {result.file_type} file: {result.file_path.name}")
                elif result.status == "skipped":
                    print(f"⚠ Skipped {result.file_type} file: {result.file_path.name}")
                else:
                    print(f"✗ Error processing {result.file_type} file: {result.file_path.name}")
        
        # Start watching
        scanner.watch_directory(
            callback=on_file_processed,
            poll_interval=args.interval
        )
        
    except KeyboardInterrupt:
        print("\n\n✓ Watch mode stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error in watch mode: {e}", file=sys.stderr)
        sys.exit(1)


def _handle_batch_command(args):
    """Handle the batch command for processing multiple YouTube URLs."""
    try:
        from pathlib import Path
        import concurrent.futures
        from core.media_preprocessor import is_youtube_url
        
        # Print header
        if not args.quiet:
            print_separator()
            print("Media-to-Knowledge Pipeline - Batch Processing")
            print_separator()
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"URLs file: {args.urls}")
            print(f"Output directory: {args.output_dir}")
            if args.parallel > 1:
                print(f"Parallel processing: {args.parallel} workers")
            if args.markdown:
                print(f"Markdown output directory: {args.markdown}")
            print_separator()
        
        # Validate URLs file exists
        urls_file = Path(args.urls)
        if not urls_file.exists():
            print(f"Error: URLs file not found: {args.urls}", file=sys.stderr)
            sys.exit(1)
        
        # Read URLs from file
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Filter for valid YouTube URLs
        youtube_urls = [url for url in urls if is_youtube_url(url)]
        
        if not youtube_urls:
            print("No valid YouTube URLs found in the file.", file=sys.stderr)
            sys.exit(1)
        
        print(f"Found {len(youtube_urls)} YouTube URLs to process")
        if not args.quiet:
            for i, url in enumerate(youtube_urls, 1):
                print(f"  {i}. {url}")
        
        # Process URLs
        successful = 0
        failed = 0
        
        if args.parallel > 1:
            # Parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
                # Submit all jobs
                future_to_url = {
                    executor.submit(_process_single_url, url, args): (url,) 
                    for url in youtube_urls
                }
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future][0]
                    try:
                        result = future.result()
                        if result["status"] == "success":
                            successful += 1
                            if not args.quiet:
                                print(f"✓ Completed: {url}")
                        else:
                            failed += 1
                            if not args.quiet:
                                print(f"✗ Failed: {url} - {result['error']}")
                    except Exception as e:
                        failed += 1
                        if not args.quiet:
                            print(f"✗ Error processing: {url} - {e}")
        else:
            # Sequential processing
            for i, url in enumerate(youtube_urls, 1):
                if not args.quiet:
                    print(f"\nProcessing URL {i}/{len(youtube_urls)}: {url}")
                
                try:
                    result = _process_single_url(url, args)
                    if result["status"] == "success":
                        successful += 1
                        if not args.quiet:
                            print(f"✓ Completed {i}: {url}")
                    else:
                        failed += 1
                        if not args.quiet:
                            print(f"✗ Failed {i}: {url} - {result['error']}")
                except Exception as e:
                    failed += 1
                    if not args.quiet:
                        print(f"✗ Error processing {i}: {url} - {e}")
        
        # Print summary
        if not args.quiet:
            print_separator()
            print("BATCH PROCESSING SUMMARY")
            print_separator()
            print(f"Total URLs processed: {len(youtube_urls)}")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            print(f"Success rate: {successful/len(youtube_urls)*100:.1f}%")
            print_separator()
            if failed == 0:
                print("✓ All URLs processed successfully!")
            else:
                print(f"⚠ {failed} URLs failed processing.")
            print_separator()
        
        sys.exit(0 if failed == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n\n✗ Batch processing interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error in batch processing: {e}", file=sys.stderr)
        sys.exit(1)


def _process_single_url(url: str, args) -> dict:
    """
    Process a single YouTube URL with the pipeline.
    
    Args:
        url: YouTube URL to process
        args: Command line arguments
        
    Returns:
        Dictionary with processing results
    """
    try:
        # Process the media file
        results = process_media(
            media_path=url,
            use_cloud_synth=args.cloud,
            prompt_template=args.prompt if args.prompt and not args.prompt.startswith("Summarize") else None,
            custom_prompt=args.prompt if args.prompt and args.prompt.startswith("Summarize") else None
        )
        
        if results["status"] == "success":
            # Save JSON results with intelligent naming
            json_output_path = generate_intelligent_json_filename(results, args.output_dir)
            save_results_to_file(results, json_output_path)
            
            # Save markdown if requested
            if args.markdown:
                save_synthesis_to_markdown(results, args.markdown)
            
            if not args.quiet:
                print(f"  Results saved to: {json_output_path}")
                if args.markdown:
                    print(f"  Markdown saved to: {args.markdown}")
        
        return results
        
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": str(e)
        }


if __name__ == "__main__":
    main()