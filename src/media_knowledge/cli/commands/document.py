"""
CLI Commands for Document Processing

Handles processing of documents (PDF, EPUB, MOBI) for knowledge synthesis.
"""

from pathlib import Path
from typing import Optional
import json

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import core modules dynamically within functions to avoid module not found errors

app = typer.Typer(
    name="document", 
    help="Process documents (PDF, EPUB, MOBI) for knowledge synthesis"
)

console = Console()


@app.command()
def process(
    file_path: Path = typer.Argument(..., help="Path to document file (PDF, EPUB, MOBI)"),
    prompt_template: Optional[str] = typer.Option(None, "--prompt", "-p", help="Prompt template to use"),
    custom_prompt: Optional[str] = typer.Option(None, "--custom-prompt", "-c", help="Custom prompt text"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file for results"),
    cloud: bool = typer.Option(False, "--cloud", help="Use cloud models for synthesis"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output")
):
    """Process a single document file."""
    
    # Import core modules dynamically
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from core.document_processor import DocumentProcessor
    from core.document_readers import DocumentReaderFactory
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Document Processor[/bold blue]")
        console.print(f"Document: {file_path}")
        console.print(f"Using cloud models: {'Yes' if cloud else 'No'}")
        if prompt_template:
            console.print(f"Prompt template: {prompt_template}")
        if custom_prompt:
            console.print("Using custom prompt")
        console.print("")
    
    # Check if file exists
    if not file_path.exists():
        console.print(f"[red]✗[/red] File not found: {file_path}")
        raise typer.Exit(code=1)
    
    # Check if format is supported
    if not DocumentReaderFactory.is_format_supported(file_path):
        supported_formats = DocumentReaderFactory.supported_formats()
        console.print(f"[red]✗[/red] Unsupported document format: {file_path.suffix}")
        console.print(f"Supported formats: {', '.join(supported_formats)}")
        raise typer.Exit(code=1)
    
    # Process the document
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        progress.add_task("Processing document...", total=None)
        
        try:
            processor = DocumentProcessor(use_cloud=cloud)
            result = processor.process_document(
                file_path=file_path,
                prompt_template=prompt_template,
                custom_prompt=custom_prompt
            )
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error processing document: {e}")
            raise typer.Exit(code=1)
    
    # Handle results
    if result["status"] == "success":
        if not quiet:
            console.print("[green]✓[/green] Successfully processed document!")
            
            # Display summary
            stats = result["processing_stats"]
            table = Table(title="Document Processing Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")
            
            table.add_row("File Size", f"{stats['file_size']:,} bytes")
            table.add_row("Extracted Text", f"{stats['extracted_characters']:,} characters")
            table.add_row("Page Count", str(stats.get('page_count', 'N/A')))
            table.add_row("Model Used", stats.get("synthesis_model", "unknown"))
            
            console.print(table)
            
            # Display synthesis summary
            synthesis = result["synthesis"]
            console.print(f"\n[bold]Synthesis Summary:[/bold]")
            console.print(f"  Raw Text Length: {synthesis.get('synthesis_length', 'N/A')} characters")
            console.print(f"  Model Used: {synthesis.get('model_used', 'unknown')}")
        
        # Save to file if requested
        if output:
            try:
                output.parent.mkdir(parents=True, exist_ok=True)
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                console.print(f"[green]✓[/green] Results saved to: {output}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Failed to save results: {e}")
    
    else:
        console.print(f"[red]✗[/red] Failed to process document: {result.get('error', 'Unknown error')}")
        raise typer.Exit(code=1)


@app.command()
def batch(
    directory: Path = typer.Argument(..., help="Directory containing document files"),
    pattern: str = typer.Option("*.*", "--pattern", "-p", help="File pattern to match"),
    prompt_template: Optional[str] = typer.Option(None, "--prompt", "-P", help="Prompt template to use"),
    custom_prompt: Optional[str] = typer.Option(None, "--custom-prompt", "-c", help="Custom prompt text"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file for batch results"),
    cloud: bool = typer.Option(False, "--cloud", help="Use cloud models for synthesis"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output")
):
    """Process multiple documents in batch."""
    
    # Import core modules dynamically
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    from core.document_processor import DocumentProcessor
    from core.document_readers import DocumentReaderFactory
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Batch Document Processor[/bold blue]")
        console.print(f"Directory: {directory}")
        console.print(f"Pattern: {pattern}")
        console.print(f"Using cloud models: {'Yes' if cloud else 'No'}")
        console.print("")
    
    # Check if directory exists
    if not directory.exists() or not directory.is_dir():
        console.print(f"[red]✗[/red] Directory not found: {directory}")
        raise typer.Exit(code=1)
    
    # Find matching files
    file_paths = list(directory.glob(pattern))
    
    if not file_paths:
        console.print(f"[yellow]⚠[/yellow] No files found matching pattern: {pattern}")
        raise typer.Exit(code=1)
    
    # Filter supported formats
    supported_files = []
    unsupported_files = []
    
    for file_path in file_paths:
        if DocumentReaderFactory.is_format_supported(file_path):
            supported_files.append(file_path)
        else:
            unsupported_files.append(file_path.name)
    
    if not supported_files:
        console.print(f"[red]✗[/red] No supported document files found")
        if unsupported_files:
            console.print(f"Unsupported files: {', '.join(unsupported_files)}")
        raise typer.Exit(code=1)
    
    if not quiet:
        console.print(f"Found {len(supported_files)} supported document(s)")
        if unsupported_files:
            console.print(f"Skipping {len(unsupported_files)} unsupported files")
        console.print("")
    
    # Process documents
    results = []
    processor = DocumentProcessor(use_cloud=cloud)
    
    for file_path in supported_files:
        if not quiet:
            console.print(f"Processing: {file_path.name}")
        
        try:
            result = processor.process_document(
                file_path=file_path,
                prompt_template=prompt_template,
                custom_prompt=custom_prompt
            )
            results.append(result)
            
            if result["status"] == "success":
                if not quiet:
                    console.print(f"  [green]✓[/green] Success")
            else:
                if not quiet:
                    console.print(f"  [red]✗[/red] Failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            console.print(f"  [red]✗[/red] Error: {e}")
            results.append({
                "status": "error",
                "original_file": str(file_path),
                "error": str(e)
            })
    
    # Generate batch summary
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    
    if not quiet:
        console.print(f"\n[bold]Batch Processing Complete[/bold]")
        console.print(f"Successful: {len(successful)} documents")
        console.print(f"Failed: {len(failed)} documents")
        
        if successful:
            # Display overall stats
            total_chars = sum(r.get('processing_stats', {}).get('extracted_characters', 0) 
                            for r in successful)
            console.print(f"Total characters extracted: {total_chars:,}")
    
    # Save results if requested
    if output:
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w', encoding='utf-8') as f:
                batch_result = {
                    "status": "complete",
                    "directory": str(directory),
                    "pattern": pattern,
                    "total_files": len(file_paths),
                    "supported_files": len(supported_files),
                    "unsupported_files": len(unsupported_files),
                    "successful": len(successful),
                    "failed": len(failed),
                    "results": results
                }
                json.dump(batch_result, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✓[/green] Batch results saved to: {output}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Failed to save batch results: {e}")


@app.command()
def formats():
    """Show supported document formats."""
    # Import dynamically
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    from core.document_readers import DocumentReaderFactory
    
    supported_formats = DocumentReaderFactory.supported_formats()
    
    console.print(f"[bold blue]Supported Document Formats[/bold blue]")
    
    table = Table(title="Document Format Support")
    table.add_column("Format", style="cyan")
    table.add_column("Extension", style="magenta")
    table.add_column("Library", style="green")
    
    # Map formats to library names
    format_info = {
        "pdf": "PyMuPDF (fitz)",
        "epub": "ebooklib",
        "mobi": "mobi"
    }
    
    for fmt in supported_formats:
        fmt_key = fmt.lstrip('.')
        library = format_info.get(fmt_key, "Unknown")
        table.add_row(fmt_key.upper(), fmt, library)
    
    console.print(table)