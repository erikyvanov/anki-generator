"""AnkiCard entity representing a single Anki flashcard."""
from dataclasses import dataclass


@dataclass
class AnkiCard:
    """Represents a single Anki flashcard.
    
    Attributes:
        front: The front content of the card (question).
        back: The back content of the card (answer).
        front_image: Optional path to an image for the front of the card.
        back_image: Optional path to an image for the back of the card.
    """
    front: str
    back: str
    front_image: str | None = None
    back_image: str | None = None

    def has_front_image(self) -> bool:
        """Check if the card has a front image."""
        return self.front_image is not None

    def has_back_image(self) -> bool:
        """Check if the card has a back image."""
        return self.back_image is not None
