#!/usr/bin/env python3
"""
Playlist Command for Media Knowledge Pipeline CLI
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
    raise typer.Exit(code=1)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

app = typer.Typer(help="Process YouTube playlist with enhanced features")


@app.command()
def process_playlist(
    url: str = typer.Argument(..., help="YouTube playlist URL"),
    output_dir: Path = typer.Option("outputs", "--output-dir", "-o", help="Output directory"),
    cloud: bool = typer.Option(False, "--cloud", help="Use Ollama Cloud for knowledge synthesis"),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Prompt template or custom prompt"),
    markdown: Optional[Path] = typer.Option(None, "--markdown", "-m", help="Markdown output directory"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
    essay: bool = typer.Option(True, "--essay/--no-essay", help="Generate playlist summary essay"),
    force_essay: bool = typer.Option(False, "--force-essay", help="Force essay generation even if content cohesion is questionable"),
    organize: bool = typer.Option(True, "--organize/--no-organize", help="Organize output in folders"),
    folder_name: Optional[str] = typer.Option(None, "--folder-name", help="Custom name for playlist folder"),
):
    """Process YouTube playlist with intelligent folder organization."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Playlist Processing[/bold blue]")
        console.print(f"Playlist URL: {url}")
        console.print(f"Output directory: {output_dir}")
        if cloud:
            console.print("Using: [green]Ollama Cloud[/green]")
        if essay:
            console.print("Essay synthesis: [green]Enabled[/green]")
        if force_essay:
            console.print("Force essay: [yellow]Yes[/yellow]")
        console.print("")
    
    try:
        # For now, we'll use the existing functionality but enhance it
        # Eventually we'll implement proper playlist handling with folder organization
        
        # Import necessary modules
        sys.path.insert(0, str(project_root))
        from core.media_preprocessor import is_youtube_playlist_url, extract_youtube_playlist_videos
        import yt_dlp
        
        if not is_youtube_playlist_url(url):
            console.print("[red]✗[/red] Provided URL is not a YouTube playlist URL.")
            raise typer.Exit(code=1)
        
        if not quiet:
            console.print("[blue]i[/blue] Extracting videos from playlist...")
        
        # Extract playlist videos
        try:
            video_urls = extract_youtube_playlist_videos(url)
            if not quiet:
                console.print(f"[blue]i[/blue] Found {len(video_urls)} videos in playlist")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to extract playlist videos: {str(e)}")
            raise typer.Exit(code=1)
        
        # Create a temporary URLs file for batch processing
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            for video_url in video_urls:
                f.write(f"{video_url}\n")
            temp_urls_file = f.name
        
        # Use the batch command for processing
        from media_knowledge.cli.commands.batch import process_urls as batch_process
        import os
        
        # Process the playlist as a batch
        batch_process(
            urls_file=Path(temp_urls_file),
            output_dir=output_dir,
            cloud=cloud,
            prompt=prompt,
            markdown=markdown,
            quiet=quiet,
            parallel=1,  # Sequential for playlist to respect order
            essay=essay,
            force_essay=force_essay,
            organize=organize,
            folder_name=folder_name or f"playlist_{Path(url).name}"
        )
        
        # Clean up temporary file
        os.unlink(temp_urls_file)
        
        if not quiet:
            console.print("[green]✓[/green] Playlist processing completed!")
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error processing playlist: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()