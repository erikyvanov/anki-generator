"""ImageLoaderService for loading images from the data directory."""
from pathlib import Path
from typing import List, Set

from src.entities import AnkiDeck


class ImageLoaderService:
    """Service responsible for loading and validating images from the data directory."""

    def __init__(self, data_directory: str = "./data"):
        """Initialize the ImageLoaderService.
        
        Args:
            data_directory: Path to the directory containing images.
        """
        self.data_directory = Path(data_directory)

    def get_image_path(self, image_name: str) -> Path:
        """Get the full path to an image file.
        
        Args:
            image_name: Name of the image file.
            
        Returns:
            Full path to the image file.
        """
        return self.data_directory / image_name

    def image_exists(self, image_name: str) -> bool:
        """Check if an image exists in the data directory.
        
        Args:
            image_name: Name of the image file.
            
        Returns:
            True if the image exists, False otherwise.
        """
        return self.get_image_path(image_name).exists()

    def validate_deck_images(self, deck: AnkiDeck) -> List[str]:
        """Validate that all images referenced in the deck exist.
        
        Args:
            deck: AnkiDeck entity to validate.
            
        Returns:
            List of missing image file names.
        """
        missing_images = []
        
        for card in deck.cards:
            if card.front_image and not self.image_exists(card.front_image):
                missing_images.append(card.front_image)
            if card.back_image and not self.image_exists(card.back_image):
                missing_images.append(card.back_image)
        
        return missing_images

    def collect_deck_images(self, deck: AnkiDeck) -> Set[str]:
        """Collect all unique image paths from a deck.
        
        Args:
            deck: AnkiDeck entity.
            
        Returns:
            Set of unique image paths that exist.
        """
        images = set()
        
        for card in deck.cards:
            if card.front_image:
                path = self.get_image_path(card.front_image)
                if path.exists():
                    images.add(str(path))
            if card.back_image:
                path = self.get_image_path(card.back_image)
                if path.exists():
                    images.add(str(path))
        
        return images
