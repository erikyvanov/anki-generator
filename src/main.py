"""Main entry point for the Anki Generator."""
import argparse
import sys
from pathlib import Path

from src.services import JsonReaderService, ImageLoaderService, AnkiPackageService


def main() -> int:
    """Main function to generate Anki packages from JSON files.
    
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Generate Anki packages (.apkg) from JSON files."
    )
    parser.add_argument(
        "input",
        help="Path to the input JSON file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path for the output .apkg file (default: same name as input)",
        default=None
    )
    parser.add_argument(
        "-d", "--data-dir",
        help="Directory containing images (default: ./data)",
        default="./data"
    )
    
    args = parser.parse_args()
    
    # Determine output path
    input_path = Path(args.input)
    if args.output:
        output_path = args.output
    else:
        output_path = str(input_path.with_suffix(".apkg"))
    
    # Initialize services
    json_reader = JsonReaderService()
    image_loader = ImageLoaderService(data_directory=args.data_dir)
    package_service = AnkiPackageService(image_loader=image_loader)
    
    try:
        # Read deck from JSON
        print(f"Reading deck from: {args.input}")
        deck = json_reader.read_deck_from_file(args.input)
        print(f"Deck title: {deck.title}")
        print(f"Number of cards: {deck.card_count()}")
        
        # Generate package
        print(f"Generating package: {output_path}")
        result_path = package_service.create_package(deck, output_path)
        print(f"Package created successfully: {result_path}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
