"""
Anki Generator Module

Generates Anki flashcards from pipeline JSON output using the genanki library.
"""
import json
import hashlib
from typing import Dict, Any, List
from pathlib import Path

# Try to import genanki, but allow module to be imported even if not available
try:
    import genanki
    GENANKI_AVAILABLE = True
except ImportError:
    GENANKI_AVAILABLE = False
    genanki = None


class AnkiGeneratorError(Exception):
    """Custom exception for Anki generator errors."""
    pass


class AnkiNoteModel:
    """Anki note models for different flashcard types."""
    
    # Model IDs (should be consistent across installations)
    CONCEPT_DEFINITION_ID = 1607392319
    Q_A_PAIR_ID = 1607392320
    EVENT_DATE_ID = 1607392321
    STEP_IN_PROCESS_ID = 1607392322
    
    @staticmethod
    def get_concept_definition_model():
        """Get the concept definition note model."""
        return genanki.Model(
            AnkiNoteModel.CONCEPT_DEFINITION_ID,
            'Concept Definition Model',
            fields=[
                {'name': 'Concept'},
                {'name': 'Definition'},
                {'name': 'Context'},
                {'name': 'Examples'},
                {'name': 'Tags'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Concept}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}<br><br>{{#Context}}<div class="context">Context: {{Context}}</div>{{/Context}}{{#Examples}}<div class="examples">Examples: {{Examples}}</div>{{/Examples}}',
                },
            ],
            css='''.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 18px;
  text-align: left;
  color: #333;
  background-color: #f9f9f9;
  padding: 20px;
}

.context, .explanation, .figures, .examples {
  font-size: 14px;
  color: #666;
  margin-top: 10px;
  padding: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  border-left: 3px solid #4CAF50;
}

hr#answer {
  border: none;
  border-top: 1px solid #ddd;
  margin: 15px 0;
}

.tags {
  font-size: 12px;
  color: #777;
  margin-top: 15px;
}
'''
        )
        
    @staticmethod
    def get_q_a_pair_model():
        """Get the Q&A pair note model."""
        return genanki.Model(
            AnkiNoteModel.Q_A_PAIR_ID,
            'Q&A Pair Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Explanation'},
                {'name': 'Source'},
                {'name': 'Tags'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{#Explanation}}<br><br><div class="explanation">Why: {{Explanation}}</div>{{/Explanation}}',
                },
            ],
            css='.card {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;font-size: 18px;text-align: left;color: #333;background-color: #f9f9f9;padding: 20px;}.explanation {font-size: 14px;color: #666;margin-top: 10px;padding: 8px;background-color: #f0f0f0;border-radius: 4px;border-left: 3px solid #4CAF50;}hr#answer {border: none;border-top: 1px solid #ddd;margin: 15px 0;}.tags {font-size: 12px;color: #777;margin-top: 15px;}'
        )
        
    @staticmethod
    def get_event_date_model():
        """Get the event/date note model."""
        return genanki.Model(
            AnkiNoteModel.EVENT_DATE_ID,
            'Timeline/Event Model',
            fields=[
                {'name': 'Event'},
                {'name': 'Date'},
                {'name': 'Significance'},
                {'name': 'KeyFigures'},
                {'name': 'Tags'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Event}} ({{Date}})',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Significance}}{{#KeyFigures}}<br><br><div class="figures">Key Figures: {{KeyFigures}}</div>{{/KeyFigures}}',
                },
            ],
            css='.card {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;font-size: 18px;text-align: left;color: #333;background-color: #f9f9f9;padding: 20px;}.figures {font-size: 14px;color: #666;margin-top: 10px;padding: 8px;background-color: #f0f0f0;border-radius: 4px;border-left: 3px solid #4CAF50;}hr#answer {border: none;border-top: 1px solid #ddd;margin: 15px 0;}.tags {font-size: 12px;color: #777;margin-top: 15px;}'
        )
        
    @staticmethod
    def get_step_in_process_model():
        """Get the process step note model."""
        return genanki.Model(
            AnkiNoteModel.STEP_IN_PROCESS_ID,
            'Process Step Model',
            fields=[
                {'name': 'Process'},
                {'name': 'StepNumber'},
                {'name': 'Step'},
                {'name': 'Detail'},
                {'name': 'Tags'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': 'Step {{StepNumber}} of {{Process}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Step}}<br><br>{{Detail}}',
                },
            ],
            css='.card {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;font-size: 18px;text-align: left;color: #333;background-color: #f9f9f9;padding: 20px;}hr#answer {border: none;border-top: 1px solid #ddd;margin: 15px 0;}.tags {font-size: 12px;color: #777;margin-top: 15px;}'
        )


class AnkiGenerator:
    """Main Anki generator class."""
    
    def __init__(self, deck_name: str = "Media Knowledge Deck"):
        """
        Initialize the Anki generator.
        
        Args:
            deck_name: Name for the Anki deck
        """
        if not GENANKI_AVAILABLE:
            raise AnkiGeneratorError("genanki library not available. Please install with: pip install genanki")
            
        self.deck_name = deck_name
        self.models = {
            "concept_definition": AnkiNoteModel.get_concept_definition_model(),
            "q_a_pair": AnkiNoteModel.get_q_a_pair_model(),
            "event_date": AnkiNoteModel.get_event_date_model(),
            "step_in_process": AnkiNoteModel.get_step_in_process_model()
        }
        
    def generate_deck_from_json(self, json_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate Anki deck from JSON data.
        
        Args:
            json_data: Dictionary containing flashcard content
            output_path: Path to save .apkg file (default: auto-generated)
            
        Returns:
            Path to generated .apkg file
        """
        # Create deck with hash-based ID for consistency
        deck_id = self._generate_deck_id(self.deck_name)
        deck = genanki.Deck(deck_id, self.deck_name)
        
        # Add notes to deck
        flashcard_content = json_data.get("flashcard_content", [])
        for item in flashcard_content:
            note = self._create_note_for_item(item)
            if note:
                deck.add_note(note)
        
        # Generate default output path if not provided
        if output_path is None:
            source_title = json_data.get("metadata", {}).get("source_title", "knowledge_cards")
            # Sanitize filename
            safe_title = "".join(c for c in source_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(" ", "_")
            output_path = f"outputs/{safe_title}_anki.apkg"
            
        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write deck to file
        genanki.Package(deck).write_to_file(str(output_file))
        
        return str(output_file)
        
    def _create_note_for_item(self, item: Dict[str, Any]) -> genanki.Note:
        """
        Create genanki.Note from flashcard item.
        
        Args:
            item: Flashcard item dictionary
            
        Returns:
            genanki.Note object or None if invalid
        """
        item_type = item.get("type")
        if item_type not in self.models:
            # Default to concept definition for unknown types
            item_type = "concept_definition"
            
        model = self.models[item_type]
        
        # Prepare fields based on item type
        fields = self._prepare_fields_for_item(item, item_type)
        
        # Create note
        note = genanki.Note(
            model=model,
            fields=fields
        )
        
        return note
        
    def _prepare_fields_for_item(self, item: Dict[str, Any], item_type: str) -> List[str]:
        """
        Prepare field values for a flashcard item.
        
        Args:
            item: Flashcard item dictionary
            item_type: Type of flashcard
            
        Returns:
            List of field values
        """
        if item_type == "concept_definition":
            return [
                item.get("concept", ""),
                item.get("definition", ""),
                item.get("context", ""),
                ", ".join(item.get("examples", [])),
                ", ".join(item.get("tags", []))
            ]
        elif item_type == "q_a_pair":
            return [
                item.get("question", ""),
                item.get("answer", ""),
                item.get("explanation", ""),
                item.get("source_timestamp", ""),
                ", ".join(item.get("tags", []))
            ]
        elif item_type == "event_date":
            return [
                item.get("event", ""),
                item.get("date", ""),
                item.get("significance", ""),
                ", ".join(item.get("key_figures", [])),
                ", ".join(item.get("tags", []))
            ]
        elif item_type == "step_in_process":
            return [
                item.get("process", ""),
                str(item.get("step_number", "")),
                item.get("step", ""),
                item.get("detail", ""),
                ", ".join(item.get("tags", []))
            ]
        else:
            # Default fields
            return ["", "", "", "", ""]
            
    def _generate_deck_id(self, deck_name: str) -> int:
        """
        Generate consistent deck ID based on deck name.
        
        Args:
            deck_name: Name of the deck
            
        Returns:
            Integer deck ID
        """
        # Create hash of deck name for consistent IDs
        hash_object = hashlib.md5(deck_name.encode())
        hex_dig = hash_object.hexdigest()
        # Convert to integer and ensure it's positive
        return int(hex_dig[:8], 16) % (2**31)


def test_anki_generator():
    """Test the Anki generator with sample data."""
    if not GENANKI_AVAILABLE:
        print("genanki not available, skipping test")
        return
        
    # Sample data for testing
    sample_data = {
        "metadata": {
            "source_title": "Test Lecture"
        },
        "flashcard_content": [
            {
                "type": "concept_definition",
                "concept": "Machine Learning",
                "definition": "A method of data analysis that automates analytical model building.",
                "tags": ["AI", "algorithms"]
            },
            {
                "type": "q_a_pair",
                "question": "What is supervised learning?",
                "answer": "Learning with labeled training data.",
                "tags": ["ML", "supervised"]
            }
        ]
    }
    
    try:
        generator = AnkiGenerator("Test Deck")
        output_path = generator.generate_deck_from_json(sample_data, "outputs/test_deck.apkg")
        print(f"✓ Anki deck generated successfully: {output_path}")
    except Exception as e:
        print(f"✗ Error generating Anki deck: {e}")


if __name__ == "__main__":
    test_anki_generator()