"""AnkiPackageService for generating .apkg files using genanki."""
import random
from typing import Optional

import genanki

from src.entities import AnkiDeck, AnkiCard
from src.services.image_loader_service import ImageLoaderService


class AnkiPackageService:
    """Service responsible for generating Anki packages (.apkg) using genanki."""

    # Basic model with optional image support
    MODEL_ID = 1607392319
    
    BASIC_MODEL = genanki.Model(
        MODEL_ID,
        "Basic Model with Images",
        fields=[
            {"name": "Front"},
            {"name": "Back"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
            },
        ],
    )

    def __init__(self, image_loader: Optional[ImageLoaderService] = None):
        """Initialize the AnkiPackageService.
        
        Args:
            image_loader: Optional ImageLoaderService for loading images.
        """
        self.image_loader = image_loader or ImageLoaderService()

    def generate_deck_id(self, title: str) -> int:
        """Generate a consistent deck ID based on the title.
        
        Args:
            title: The deck title.
            
        Returns:
            A deck ID integer.
        """
        # Use a seeded random to generate consistent IDs for the same title
        random.seed(title)
        return random.randrange(1 << 30, 1 << 31)

    def create_note(self, card: AnkiCard) -> genanki.Note:
        """Create a genanki Note from an AnkiCard entity.
        
        Args:
            card: AnkiCard entity.
            
        Returns:
            genanki.Note object.
        """
        front_content = card.front
        back_content = card.back
        
        # Add image tags if images are specified
        if card.front_image:
            front_content = f'<img src="{card.front_image}"><br>{front_content}'
        if card.back_image:
            back_content = f'{back_content}<br><img src="{card.back_image}">'
        
        return genanki.Note(
            model=self.BASIC_MODEL,
            fields=[front_content, back_content]
        )

    def create_package(self, deck: AnkiDeck, output_path: str) -> str:
        """Create an Anki package (.apkg) from an AnkiDeck entity.
        
        Args:
            deck: AnkiDeck entity containing the cards.
            output_path: Path where the .apkg file will be saved.
            
        Returns:
            Path to the created .apkg file.
            
        Raises:
            ValueError: If deck has missing images.
        """
        # Validate images
        missing_images = self.image_loader.validate_deck_images(deck)
        if missing_images:
            raise ValueError(f"Missing images: {', '.join(missing_images)}")
        
        # Create genanki deck
        deck_id = self.generate_deck_id(deck.title)
        genanki_deck = genanki.Deck(deck_id, deck.title)
        
        # Add notes to deck
        for card in deck.cards:
            note = self.create_note(card)
            genanki_deck.add_note(note)
        
        # Collect media files
        media_files = list(self.image_loader.collect_deck_images(deck))
        
        # Create package
        package = genanki.Package(genanki_deck)
        package.media_files = media_files
        
        # Ensure output path ends with .apkg
        if not output_path.endswith(".apkg"):
            output_path = f"{output_path}.apkg"
        
        package.write_to_file(output_path)
        
        return output_path
