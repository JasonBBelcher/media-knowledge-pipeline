#!/usr/bin/env python3
"""
Anki Command for Media Knowledge Pipeline CLI

Generate Anki flashcards from pipeline synthesis output.
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

from core.output_adapters.anki_adapter import AnkiAdapter
from core.anki_generator import AnkiGenerator, AnkiGeneratorError

app = typer.Typer(help="Generate Anki flashcards from synthesis output")


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
    ),
):
    """Generate Anki flashcards from pipeline JSON output."""
    console = Console()
    
    if not quiet:
        console.print("[bold blue]Media Knowledge Pipeline - Anki Generation[/bold blue]")
        console.print(f"Input: {input_path}")
        if output:
            console.print(f"Output directory: {output}")
        if deck_name:
            console.print(f"Deck name: {deck_name}")
        if preview:
            console.print("Mode: Preview only")
        console.print("")
    
    # Validate input file exists
    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input file not found: {input_path}")
        sys.exit(1)
        
    if not input_path.suffix.lower() == '.json':
        console.print(f"[red]Error:[/red] Input must be a JSON file")
        sys.exit(1)
    
    try:
        # Load JSON data
        import json
        with open(input_path, 'r', encoding='utf-8') as f:
            pipeline_output = json.load(f)
            
        if not quiet:
            console.print("[green]✓[/green] Loaded synthesis data")
            
        # Transform with Anki adapter
        adapter = AnkiAdapter()
        anki_data = adapter.transform(pipeline_output)
        
        if not quiet:
            console.print(f"[green]✓[/green] Transformed to Anki format ({len(anki_data['flashcard_content'])} flashcards)")
            
        # Validate transformed data
        is_valid = adapter.validate(anki_data)
        if not is_valid:
            console.print("[yellow]Warning:[/yellow] Anki data validation failed")
        elif not quiet:
            console.print("[green]✓[/green] Data validation passed")
            
        # Preview mode - show sample flashcards
        if preview:
            _show_preview(console, anki_data, quiet)
            return
            
        # Generate Anki deck
        if deck_name is None:
            source_title = anki_data.get("metadata", {}).get("source_title", "Knowledge Cards")
            deck_name = f"{source_title} Flashcards"
            
        generator = AnkiGenerator(deck_name)
        apkg_path = generator.generate_deck_from_json(anki_data, str(output) if output else None)
        
        if not quiet:
            console.print(f"[green]✓[/green] Generated Anki deck: {apkg_path}")
            console.print("[bold green]Success![/bold green] Anki deck ready for import.")
            
    except json.JSONDecodeError as e:
        console.print(f"[red]Error:[/red] Invalid JSON in input file: {e}")
        sys.exit(1)
    except AnkiGeneratorError as e:
        console.print(f"[red]Error:[/red] Anki generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Unexpected error: {e}")
        sys.exit(1)


@app.command()
def templates():
    """List available flashcard templates and their structure."""
    console = Console()
    
    console.print("[bold blue]Anki Flashcard Templates[/bold blue]")
    console.print("")
    
    templates_info = {
        "concept_definition": {
            "description": "Terms, concepts, and definitions",
            "fields": ["concept", "definition", "context (optional)", "examples (optional)"],
            "example": "Machine Learning → A method of data analysis..."
        },
        "q_a_pair": {
            "description": "Questions and answers, problem/solution",
            "fields": ["question", "answer", "explanation (optional)", "source_timestamp (optional)"],
            "example": "What is supervised learning? → Learning with labeled data..."
        },
        "event_date": {
            "description": "Historical events, milestones, dates",
            "fields": ["event", "date", "significance", "key_figures (optional)"],
            "example": "Backpropagation introduction → 1986 → Enabled deep network training..."
        },
        "step_in_process": {
            "description": "Procedural steps, sequences, workflows",
            "fields": ["process", "step_number", "step", "detail"],
            "example": "Data preprocessing → Step 2 → Normalize features → Scale to 0-1 range..."
        }
    }
    
    for template_type, info in templates_info.items():
        console.print(f"[bold]{template_type}[/bold]: {info['description']}")
        console.print(f"  Fields: {', '.join(info['fields'])}")
        console.print(f"  Example: {info['example']}")
        console.print("")


@app.command() 
def preview(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Path to synthesis JSON file"
    ),
    count: int = typer.Option(
        5, "--count", "-c", help="Number of flashcards to preview"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Suppress detailed output"
    ),
):
    """Preview flashcards that would be generated from JSON input."""
    # This is essentially the same as generate with preview=True
    generate(input_path=input_path, preview=True, quiet=quiet)


def _show_preview(console: Console, anki_data: dict, quiet: bool):
    """Show preview of generated flashcards."""
    flashcards = anki_data.get("flashcard_content", [])
    
    if not flashcards:
        console.print("[yellow]No flashcards found in data.[/yellow]")
        return
        
    console.print(f"[bold blue]Preview: {len(flashcards)} Flashcards[/bold blue]")
    console.print("")
    
    # Show first few flashcards
    for i, card in enumerate(flashcards[:5]):
        console.print(f"[bold]Flashcard {i+1}[/bold] ([cyan]{card['type']}[/cyan])")
        console.print(f"  ID: {card['id']}")
        console.print(f"  Priority: {card['priority']}")
        console.print(f"  Tags: {', '.join(card['tags'])}")
        
        # Show type-specific fields
        if card['type'] == 'concept_definition':
            console.print(f"  Concept: {card.get('concept', 'N/A')}")
            console.print(f"  Definition: {card.get('definition', 'N/A')}")
        elif card['type'] == 'q_a_pair':
            console.print(f"  Question: {card.get('question', 'N/A')}")
            console.print(f"  Answer: {card.get('answer', 'N/A')}")
        elif card['type'] == 'event_date':
            console.print(f"  Event: {card.get('event', 'N/A')}")
            console.print(f"  Date: {card.get('date', 'N/A')}")
        elif card['type'] == 'step_in_process':
            console.print(f"  Process: {card.get('process', 'N/A')}")
            console.print(f"  Step: {card.get('step', 'N/A')}")
            
        console.print("")


if __name__ == "__main__":
    app()