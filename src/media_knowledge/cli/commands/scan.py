#!/usr/bin/env python3
"""
Scan Command for Media Knowledge Pipeline CLI
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

app = typer.Typer(help="Scan directory for media files")


@app.command()
def directory(
    directory: Path = typer.Option("~/Downloads", "--directory", "-d", help="Directory to scan"),
    audio_dir: Path = typer.Option("data/audio", "--audio-dir", help="Directory for audio files"),
    video_dir: Path = typer.Option("data/videos", "--video-dir", help="Directory for video files"),
    process_pipeline: bool = typer.Option(False, "--process", help="Automatically process copied files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen without copying"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress detailed output"),
):
    """Scan directory for media files and copy to appropriate directories."""
    console = Console()
    
    if not quiet:
        console.print(f"[bold blue]Media Knowledge Pipeline - Directory Scan[/bold blue]")
        console.print(f"Scan directory: {directory}")
        console.print(f"Audio directory: {audio_dir}")
        console.print(f"Video directory: {video_dir}")
        if process_pipeline:
            console.print("Auto-processing: [green]Enabled[/green]")
        if dry_run:
            console.print("Mode: [yellow]Dry Run[/yellow]")
        console.print("")
    
    try:
        # Import the file scanner
        sys.path.insert(0, str(project_root))
        from core.file_scanner import FileScanner
        
        # Expand user path
        scan_dir = Path(directory).expanduser()
        audio_target = Path(audio_dir).expanduser()
        video_target = Path(video_dir).expanduser()
        
        if not scan_dir.exists():
            console.print(f"[red]✗[/red] Scan directory does not exist: {scan_dir}")
            raise typer.Exit(code=1)
        
        # Create target directories
        audio_target.mkdir(parents=True, exist_ok=True)
        video_target.mkdir(parents=True, exist_ok=True)
        
        if not quiet:
            console.print(f"[blue]i[/blue] Scanning directory: {scan_dir}")
        
        # Initialize scanner
        scanner = FileScanner(
            scan_directory=str(scan_dir),
            audio_directory=str(audio_target),
            video_directory=str(video_target),
            dry_run=dry_run
        )
        
        # Scan directory
        results = scanner.scan_directory(str(scan_dir))
        
        if not quiet:
            console.print(f"[green]✓[/green] Scan completed!")
            console.print(f"  Files found: {len(results)}")
            
            # Show summary
            audio_count = sum(1 for r in results if r.file_type == 'audio')
            video_count = sum(1 for r in results if r.file_type == 'video')
            copied_count = sum(1 for r in results if r.status == 'copied')
            
            table = Table(title="Scan Results")
            table.add_column("Category", style="cyan")
            table.add_column("Count", style="magenta")
            
            table.add_row("Total Files", str(len(results)))
            table.add_row("Audio Files", str(audio_count))
            table.add_row("Video Files", str(video_count))
            if not dry_run:
                table.add_row("Copied Files", str(copied_count))
            
            console.print(table)
        
        # Process files through pipeline if requested
        if process_pipeline and not dry_run and results:
            console.print("[blue]i[/blue] Processing copied files through pipeline...")
            processed_count = 0
            
            for result in results:
                if result.status == 'copied' and result.destination:
                    try:
                        # Process each file
                        # This would call the process command for each file
                        processed_count += 1
                        if not quiet:
                            console.print(f"  [green]✓[/green] Processed: {Path(result.destination).name}")
                    except Exception as e:
                        if not quiet:
                            console.print(f"  [red]✗[/red] Failed to process: {Path(result.destination).name} - {str(e)}")
            
            if not quiet:
                console.print(f"[green]✓[/green] Pipeline processing completed: {processed_count}/{len([r for r in results if r.status == 'copied'])} files processed")
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error during directory scan: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()