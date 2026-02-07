#!/usr/bin/env python3
"""
Batch Command for Media Knowledge Pipeline CLI
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
    from rich.table import Table
except ImportError:
    print("Required packages not found. Please install typer and rich.")
    sys.exit(1)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

app = typer.Typer(help="Process multiple YouTube URLs from file")


@app.command()
def process_urls(
    urls_file: Path = typer.Option(..., "--urls", "-u", help="Path to file containing YouTube URLs"),
    output_dir: Path = typer.Option("outputs", "--output-dir", "-o", help="Output directory"),
    cloud: bool = typer.Option(False, "--cloud", help="Use Ollama Cloud for knowledge synthesis"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Prompt template or custom prompt"),
    markdown: Optional[Path] = typer.Option(None, "--markdown", "-m", help="Markdown output directory"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
    parallel: int = typer.Option(1, "--parallel", "-j", help="Number of parallel processes"),
    essay: bool = typer.Option(False, "--essay", "-e", help="Generate comprehensive essay from multiple sources"),
    force_essay: bool = typer.Option(False, "--force-essay", help="Force essay generation even if content cohesion is questionable"),
    organize: bool = typer.Option(True, "--organize/--no-organize", help="Organize output in folders"),
    folder_name: Optional[str] = typer.Option(None, "--folder-name", help="Custom name for batch folder"),
):
    """Process multiple YouTube URLs from a file with enhanced features."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Batch Processing[/bold blue]")
        console.print(f"URLs file: {urls_file}")
        console.print(f"Output directory: {output_dir}")
        if cloud:
            console.print("Using: [green]Ollama Cloud[/green]")
        if parallel > 1:
            console.print(f"Parallel processing: {parallel} workers")
        if essay:
            console.print("Essay synthesis: [green]Enabled[/green]")
        if force_essay:
            console.print("Force essay: [yellow]Yes[/yellow]")
        console.print("")
    
    try:
        # Read URLs from file
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            console.print("[red]✗[/red] No valid URLs found in the file.")
            raise typer.Exit(code=1)
        
        if not quiet:
            console.print(f"[blue]i[/blue] Found {len(urls)} URLs to process")
            for i, url in enumerate(urls, 1):
                console.print(f"  {i}. {url}")
            console.print("")
        
        # Import the main pipeline batch function
        sys.path.insert(0, str(project_root))
        from main import _handle_batch_command
        import argparse
        
        # Create args object to mimic command line arguments
        class BatchArgs:
            def __init__(self):
                self.urls = str(urls_file)
                self.output_dir = str(output_dir)
                self.cloud = cloud
                self.prompt = prompt
                self.markdown = str(markdown) if markdown else None
                self.quiet = quiet
                self.parallel = parallel
                self.essay = essay
                self.force_essay = force_essay
        
        args = BatchArgs()
        
        # Process batch (this will call the existing batch handler)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=False,
        ) as progress:
            task_id = progress.add_task("Processing URLs...", total=len(urls))
            
            # For now, we'll call the existing batch handler but we should
            # eventually reimplement this with better progress tracking
            if not quiet:
                console.print("[blue]i[/blue] Starting batch processing...")
            
            # Call the existing handler
            _handle_batch_command(args)
            
            # Update progress
            progress.update(task_id, completed=len(urls))
        
        if not quiet:
            console.print("[green]✓[/green] Batch processing completed!")
            
    except FileNotFoundError:
        console.print(f"[red]✗[/red] URLs file not found: {urls_file}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]✗[/red] Error during batch processing: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()