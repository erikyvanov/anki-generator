# Anki Generator

Generate Anki packages (.apkg) from JSON files using [genanki](https://github.com/kerrickstaley/genanki).

## Installation

```bash
pip install -e .
```

## Usage

```bash
anki-generator input.json -o output.apkg
```

### Command Line Options

- `input`: Path to the input JSON file (required)
- `-o, --output`: Path for the output .apkg file (default: same name as input)
- `-d, --data-dir`: Directory containing images (default: `./data`)

## JSON Input Format

The input JSON file should have the following structure:

```json
{
    "title": "Deck Title",
    "cards": [
        {
            "front": "Question text",
            "back": "Answer text",
            "front_image": "optional_front_image.png",
            "back_image": "optional_back_image.png"
        }
    ]
}
```

### Fields

- `title` (required): The name of the Anki deck
- `cards` (required): Array of card objects
  - `front` (required): The front side content (question)
  - `back` (required): The back side content (answer)
  - `front_image` (optional): Filename of an image to display on the front
  - `back_image` (optional): Filename of an image to display on the back

## Images

Images should be placed in the `./data` directory (or specify a custom directory with `-d`). The image filenames in the JSON should match the files in the data directory.

## Example

See `example.json` for a sample input file.

```bash
# Create data directory and add images
mkdir -p data

# Generate the Anki package
anki-generator example.json -o my_deck.apkg
```

## Project Structure

The project follows the Single Responsibility Principle with separate entities and services:

### Entities

- `AnkiCard`: Represents a single flashcard with front/back content and optional images
- `AnkiDeck`: Represents a deck containing a title and list of cards

### Services

- `JsonReaderService`: Reads and parses JSON input files into entities
- `ImageLoaderService`: Manages image loading and validation from the data directory
- `AnkiPackageService`: Generates .apkg files using genanki

## License

MIT