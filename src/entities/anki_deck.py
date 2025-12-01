"""AnkiDeck entity representing an Anki deck with cards."""
from dataclasses import dataclass, field
from typing import List

from .anki_card import AnkiCard


@dataclass
class AnkiDeck:
    """Represents an Anki deck containing multiple flashcards.
    
    Attributes:
        title: The title/name of the deck.
        cards: List of AnkiCard objects in the deck.
    """
    title: str
    cards: List[AnkiCard] = field(default_factory=list)

    def add_card(self, card: AnkiCard) -> None:
        """Add a card to the deck."""
        self.cards.append(card)

    def card_count(self) -> int:
        """Return the number of cards in the deck."""
        return len(self.cards)
