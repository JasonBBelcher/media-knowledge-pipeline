#!/usr/bin/env python3
"""
Process Command for Media Knowledge Pipeline CLI
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
except ImportError:
    print("Required packages not found. Please install typer and rich.")
    sys.exit(1)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

app = typer.Typer(help="Process single media file or YouTube URL")


@app.command()
def media(
    input_path: str = typer.Option(..., "--input", "-i", help="Path to video/audio file or YouTube URL"),
    cloud: bool = typer.Option(False, "--cloud", help="Use Ollama Cloud for knowledge synthesis"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Prompt template or custom prompt"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file path"),
    markdown: Optional[Path] = typer.Option(None, "--markdown", "-m", help="Markdown output directory"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
    organize: bool = typer.Option(True, "--organize/--no-organize", help="Organize output in folders"),
):
    """Process a single media file or YouTube URL."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Processing Media[/bold blue]")
        console.print(f"Input: {input_path}")
        if cloud:
            console.print("Using: [green]Ollama Cloud[/green]")
        if prompt:
            console.print(f"Prompt: {prompt}")
        if output:
            console.print(f"JSON Output: {output}")
        if markdown:
            console.print(f"Markdown Output: {markdown}")
        console.print("")
    
    try:
        # Import the main pipeline
        sys.path.insert(0, str(project_root))
        from main import process_media, save_results_to_file, save_synthesis_to_markdown
        
        # Process the media
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            if not quiet:
                progress.add_task("Processing media...", total=None)
            
            results = process_media(
                media_path=input_path,
                use_cloud_synth=cloud,
                prompt_template=prompt if prompt and not prompt.startswith("Summarize") else None,
                custom_prompt=prompt if prompt and prompt.startswith("Summarize") else None
            )
        
        # Handle results
        if results["status"] == "success":
            if not quiet:
                console.print("[green]✓[/green] Processing completed successfully!")
                
                # Display summary
                table = Table(title="Processing Results")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="magenta")
                
                table.add_row("Processing Time", f"{results['processing_time']:.2f}s")
                table.add_row("Transcript Length", f"{results['transcript_length']} characters")
                table.add_row("Synthesis Length", f"{len(results['synthesis']['raw_text'])} characters")
                table.add_row("Model Used", results['model_used'])
                
                console.print(table)
            
            # Save results
            if output:
                save_results_to_file(results, str(output))
                if not quiet:
                    console.print(f"[blue]i[/blue] Results saved to: {output}")
            
            if markdown:
                save_synthesis_to_markdown(results, str(markdown))
                if not quiet:
                    console.print(f"[blue]i[/blue] Markdown saved to: {markdown}")
                    
        else:
            console.print(f"[red]✗[/red] Processing failed: {results['error']}")
            raise typer.Exit(code=1)
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error processing media: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()