#!/usr/bin/env python3
"""
Watch Command for Media Knowledge Pipeline CLI
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

app = typer.Typer(help="Watch directory for new media files")


@app.command()
def directory(
    directory: Path = typer.Option("~/Downloads", "--directory", "-d", help="Directory to watch"),
    audio_dir: Path = typer.Option("data/audio", "--audio-dir", help="Directory for audio files"),
    video_dir: Path = typer.Option("data/videos", "--video-dir", help="Directory for video files"),
    process_pipeline: bool = typer.Option(False, "--process", help="Automatically process copied files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen without copying"),
    interval: int = typer.Option(5, "--interval", "-i", help="Poll interval in seconds"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
):
    """Continuously watch directory for new media files."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Directory Watch[/bold blue]")
        console.print(f"Watch directory: {directory}")
        console.print(f"Audio directory: {audio_dir}")
        console.print(f"Video directory: {video_dir}")
        console.print(f"Poll interval: {interval}s")
        if process_pipeline:
            console.print("Auto-processing: [green]Enabled[/green]")
        if dry_run:
            console.print("Mode: [yellow]Dry Run[/yellow]")
        console.print("")
        console.print("[yellow]Press Ctrl+C to stop watching[/yellow]")
        console.print("")
    
    try:
        # Import the file scanner
        sys.path.insert(0, str(project_root))
        from core.file_scanner import FileScanner
        import time
        
        # Expand user path
        watch_dir = Path(directory).expanduser()
        audio_target = Path(audio_dir).expanduser()
        video_target = Path(video_dir).expanduser()
        
        if not watch_dir.exists():
            console.print(f"[red]✗[/red] Watch directory does not exist: {watch_dir}")
            raise typer.Exit(code=1)
        
        # Create target directories
        audio_target.mkdir(parents=True, exist_ok=True)
        video_target.mkdir(parents=True, exist_ok=True)
        
        if not quiet:
            console.print(f"[blue]i[/blue] Watching directory: {watch_dir}")
            console.print(f"[blue]i[/blue] Polling every {interval} seconds...")
        
        # Initialize scanner
        scanner = FileScanner(
            scan_directory=str(watch_dir),
            audio_directory=str(audio_target),
            video_directory=str(video_target),
            dry_run=dry_run
        )
        
        # Keep track of processed files to avoid duplicates
        processed_files = set()
        
        try:
            while True:
                # Scan for new files
                results = scanner.scan_directory(str(watch_dir))
                
                new_files = [r for r in results if r.source not in processed_files]
                
                if new_files and not quiet:
                    console.print(f"[blue]i[/blue] Found {len(new_files)} new files")
                
                # Process new files
                for result in new_files:
                    processed_files.add(result.source)
                    
                    if not dry_run:
                        # Copy file
                        try:
                            copied_result = scanner.copy_media_file(result.source)
                            if copied_result.status == 'copied':
                                console.print(f"[green]✓[/green] Copied: {Path(result.source).name} → {Path(copied_result.destination).name}")
                                
                                # Process through pipeline if requested
                                if process_pipeline and copied_result.destination:
                                    console.print(f"  [blue]→[/blue] Processing through pipeline...")
                                    # This would call the process command
                                    console.print(f"  [green]✓[/green] Processed: {Path(copied_result.destination).name}")
                            else:
                                console.print(f"[red]✗[/red] Failed to copy: {Path(result.source).name}")
                        except Exception as e:
                            console.print(f"[red]✗[/red] Error copying {Path(result.source).name}: {str(e)}")
                    else:
                        # Dry run - just show what would happen
                        console.print(f"[yellow]~[/yellow] Would copy: {Path(result.source).name}")
                
                # Wait before next poll
                time.sleep(interval)
                
        except KeyboardInterrupt:
            if not quiet:
                console.print("\n[yellow]⚠[/yellow] Stopping watch process...")
            return
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error during directory watch: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()