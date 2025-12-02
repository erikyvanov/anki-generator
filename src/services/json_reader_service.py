"""JsonReaderService for reading and parsing JSON input files."""
import json
from pathlib import Path

from src.entities import AnkiCard, AnkiDeck


class JsonReaderService:
    """Service responsible for reading and parsing JSON files into AnkiDeck entities."""

    def read_deck_from_file(self, file_path: str) -> AnkiDeck:
        """Read a JSON file and convert it to an AnkiDeck entity.
        
        Args:
            file_path: Path to the JSON file.
            
        Returns:
            AnkiDeck entity populated with data from the JSON file.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            json.JSONDecodeError: If the JSON is invalid.
            KeyError: If required fields are missing.
        """
        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return self._parse_deck_data(data)

    def read_deck_from_string(self, json_string: str) -> AnkiDeck:
        """Parse a JSON string and convert it to an AnkiDeck entity.
        
        Args:
            json_string: JSON string containing deck data.
            
        Returns:
            AnkiDeck entity populated with data from the JSON string.
            
        Raises:
            json.JSONDecodeError: If the JSON is invalid.
            KeyError: If required fields are missing.
        """
        data = json.loads(json_string)
        return self._parse_deck_data(data)

    def _parse_deck_data(self, data: dict) -> AnkiDeck:
        """Parse dictionary data into an AnkiDeck entity.
        
        Args:
            data: Dictionary containing deck data.
            
        Returns:
            AnkiDeck entity.
            
        Raises:
            KeyError: If required fields are missing.
        """
        title = data["title"]
        cards_data = data.get("cards", [])
        
        cards = [self._parse_card_data(card_data) for card_data in cards_data]
        
        return AnkiDeck(title=title, cards=cards)

    def _parse_card_data(self, card_data: dict) -> AnkiCard:
        """Parse dictionary data into an AnkiCard entity.
        
        Args:
            card_data: Dictionary containing card data.
            
        Returns:
            AnkiCard entity.
            
        Raises:
            KeyError: If required fields are missing.
        """
        return AnkiCard(
            front=card_data["front"],
            back=card_data["back"],
            front_image=card_data.get("front_image"),
            back_image=card_data.get("back_image")
        )
