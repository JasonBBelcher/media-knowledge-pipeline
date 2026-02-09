#!/usr/bin/env python3
"""
Enhanced CLI Application for Media Knowledge Pipeline
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
except ImportError:
    print("Required packages not found. Please install:")
    print("pip install typer rich")
    sys.exit(1)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from media_knowledge.cli.commands import process, batch, playlist, scan, watch, document, anki

# Import the existing documents essay generator
try:
    from utils.essay_from_existing import ExistingDocumentsEssayGenerator
    EXISTING_DOCS_AVAILABLE = True
except ImportError:
    EXISTING_DOCS_AVAILABLE = False
    class ExistingDocumentsEssayGenerator:
        def __init__(self):
            pass
        def generate_essay_from_files(self, directory, pattern="*.json", output_file=None):
            return {"status": "error", "error": "Feature not available"}

app = typer.Typer(
    name="media-knowledge",
    help="Extract and synthesize knowledge from video/audio content",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(process.app, name="process", help="Process single media file or YouTube URL")
app.add_typer(batch.app, name="batch", help="Process multiple YouTube URLs from file")
app.add_typer(playlist.app, name="playlist", help="Process YouTube playlist")
app.add_typer(scan.app, name="scan", help="Scan directory for media files")
app.add_typer(watch.app, name="watch", help="Watch directory for new media files")
app.add_typer(document.app, name="document", help="Process documents (PDF, EPUB, MOBI)")
app.add_typer(anki.app, name="anki", help="Generate Anki flashcards from synthesis output")


@app.command()
def create_essay(
    directory: Path = typer.Option(..., "--directory", "-d", help="Directory containing JSON synthesis files"),
    pattern: str = typer.Option("*.json", "--pattern", "-p", help="File pattern to match"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file for essay data"),
    cloud: bool = typer.Option(False, "--cloud", help="Use cloud models for essay synthesis"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
):
    """Create essay from existing synthesized documents."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Essay from Existing Documents[/bold blue]")
        console.print(f"Directory: {directory}")
        console.print(f"Pattern: {pattern}")
        if output:
            console.print(f"Output: {output}")
        console.print("")
    
    try:
        # Initialize generator
        generator = ExistingDocumentsEssayGenerator()
        
        # Generate essay data
        result = generator.generate_essay_from_files(
            directory=str(directory),
            pattern=pattern,
            output_file=str(output) if output else None
        )
        
        if result["status"] == "success":
            if not quiet:
                console.print("[green]✓[/green] Successfully loaded existing documents!")
                console.print(f"  Sources found: {result['sources_count']}")
                
                # Show summary
                table = Table(title="Document Summary")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="magenta")
                
                table.add_row("Sources Loaded", str(result['sources_count']))
                table.add_row("Directory", result['directory'])
                
                console.print(table)
                
                console.print("[blue]i[/blue] Use the batch command with --essay to generate final essay")
        
        else:
            console.print(f"[red]✗[/red] Failed to load documents: {result['error']}")
            raise typer.Exit(code=1)
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error creating essay from existing documents: {str(e)}")
        raise typer.Exit(code=1)


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", 
        help="Show version and exit",
        is_eager=True,
    ),
):
    """Media Knowledge Pipeline CLI - Enhanced version"""
    if version:
        from media_knowledge import __version__
        typer.echo(f"Media Knowledge Pipeline v{__version__}")
        raise typer.Exit()


@app.command()
def status():
    """Show system status and requirements check."""
    console = Console()
    
    table = Table(title="System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    # Check ffmpeg
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            table.add_row("ffmpeg", "✓ Available", "Ready for media processing")
        else:
            table.add_row("ffmpeg", "✗ Not Found", "Required for audio/video conversion")
    except FileNotFoundError:
        table.add_row("ffmpeg", "✗ Not Found", "Required for audio/video conversion")
    
    # Check Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            table.add_row("Ollama", "✓ Running", "Local models available")
        else:
            table.add_row("Ollama", "⚠ Not Responding", "Check Ollama service")
    except Exception:
        table.add_row("Ollama", "⚠ Not Running", "Required for knowledge synthesis")
    
    # Check Whisper
    try:
        import whisper
        table.add_row("Whisper", "✓ Available", "Speech-to-text ready")
    except ImportError:
        table.add_row("Whisper", "⚠ Not Installed", "Required for transcription")
    
    console.print(table)


if __name__ == "__main__":
    app()