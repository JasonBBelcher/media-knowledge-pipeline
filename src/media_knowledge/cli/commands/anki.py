"""
Anki Command for Media Knowledge Pipeline CLI

Generate Anki flashcards from pipeline synthesis output.
"""
import sys
from pathlib import Path
from typing import Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import typer
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
except ImportError:
    print("Required packages not found. Please install typer and rich.")
    import sys
    raise typer.Exit(code=1)

try:
    from core.output_adapters.anki_adapter import AnkiAdapter
    from core.anki_generator import AnkiGenerator, AnkiGeneratorError
except ImportError:
    # For when importing from installed package
    try:
        from media_knowledge.core.output_adapters.anki_adapter import AnkiAdapter
        from media_knowledge.core.anki_generator import AnkiGenerator, AnkiGeneratorError
    except ImportError:
        AnkiAdapter = AnkiGenerator = None

try:
    import genanki
except ImportError:
    genanki = None

app = typer.Typer(help="Generate Anki flashcards from synthesis output")

console = Console()


@app.command()
def generate(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Path to synthesis JSON file"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory for .apkg file"
    ),
    deck_name: Optional[str] = typer.Option(
        None, "--deck-name", "-n", help="Custom Anki deck name"
    ),
    preview: bool = typer.Option(
        False, "--preview", "-p", help="Preview flashcards without generating deck"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Suppress detailed output"
    )
):
    """Generate Anki flashcards from pipeline synthesis output."""
    
    if genanki is None:
        console.print("[red]✗[/red] Required package 'genanki' not installed")
        console.print("Please install: pip install genanki")
        raise typer.Exit(code=1)
    
    if AnkiAdapter is None or AnkiGenerator is None:
        console.print("[red]✗[/red] Anki integration components not available")
        raise typer.Exit(code=1)
    
    if not quiet:
        console.print("[bold blue]Media Knowledge Pipeline - Anki Generator[/bold blue]")
        console.print(f"Input JSON: {input_path}")
        if output:
            console.print(f"Output directory: {output}")
        else:
            console.print("Output directory: Default location (next to input)")
        if deck_name:
            console.print(f"Deck name: {deck_name}")
        console.print("")
    
    # Check if input file exists
    if not input_path.exists():
        console.print(f"[red]✗[/red] Input file not found: {input_path}")
        raise typer.Exit(code=1)
    
    try:
        # Import the generator (ensure it's fresh from the root path)
        from core.anki_generator import AnkiGenerator, AnkiGeneratorError
        generator = AnkiGenerator()
        
        if preview:
            # Preview mode - preview without generating
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task("Previewing flashcards...", total=None)
                
                preview_data = generator.preview_deck_from_json(str(input_path))
                
                if preview_data["status"] == "success":
                    console.print("[green]✓[/green] Preview successful")
                    console.print(f"Generated {preview_data['flashcard_count']} flashcards")
                    
                    if not quiet:
                        # Show sample flashcards
                        console.print("\n[bold]Sample Flashcards:[/bold]")
                        for i, card in enumerate(preview_data['sample_cards'][:3], 1):
                            console.print(f"\nCard {i}:")
                            console.print(f"  Front: {card['front'][:80]}...")
                            console.print(f"  Back: {card['back'][:80]}...")
                else:
                    console.print(f"[red]✗[/red] Preview failed: {preview_data['error']}")
                    raise typer.Exit(code=1)
        else:
            # Generate mode - create actual .apkg file
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task("Generating Anki deck...", total=None)
                
                # Determine output path
                if output:
                    output_dir = output
                    output_dir.mkdir(parents=True, exist_ok=True)
                else:
                    output_dir = input_path.parent
                
                # Generate deck
                output_path = generator.generate_deck_from_json(
                    str(input_path), 
                    str(output_dir / f"{input_path.stem}.apkg"),
                    deck_name
                )
                
                console.print(f"[green]✓[/green] Anki deck generated successfully")
                console.print(f"Output: {output_path}")
                
    except Exception as e:
        console.print(f"[red]✗[/red] Error generating Anki deck: {e}")
        raise typer.Exit(code=1)


@app.command()
def templates():
    """Show available Anki flashcard templates."""
    try:
        # Import the generator
        from core.anki_generator import AnkiGenerator
        generator = AnkiGenerator()
        
        templates = generator.get_available_templates()
        
        console.print("[bold blue]Available Anki Flashcard Templates[/bold blue]")
        console.print("")
        
        for template_name, template_info in templates.items():
            console.print(f"[bold]{template_name}[/bold]")
            console.print(f"  Description: {template_info['description']}")
            console.print(f"  Fields: {', '.join(template_info['fields'])}")
            console.print("")
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error retrieving templates: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()