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

## LaTeX Support

The generator supports LaTeX equations using Anki's built-in MathJax rendering. You can include mathematical equations in your cards using the following syntax:

### Inline Math

Use `\(` and `\)` for inline math:

```json
{
    "front": "What is the quadratic formula?",
    "back": "The quadratic formula is \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\)"
}
```

### Display Math

Use `\[` and `\]` for display (centered) math:

```json
{
    "front": "Pythagorean theorem",
    "back": "\\[a^2 + b^2 = c^2\\]"
}
```

### Alternative Syntax

You can also use `$$` for display math (though `\[` and `\]` are preferred):

```json
{
    "front": "Einstein's mass-energy equivalence",
    "back": "$$E = mc^2$$"
}
```

### LaTeX Example

```json
{
    "title": "Mathematics",
    "cards": [
        {
            "front": "What is the integral of \\(x^2\\)?",
            "back": "\\[\\int x^2 dx = \\frac{x^3}{3} + C\\]"
        },
        {
            "front": "What is Euler's identity?",
            "back": "\\[e^{i\\pi} + 1 = 0\\]"
        }
    ]
}
```

**Note:** Remember to escape backslashes in JSON by using `\\` instead of `\`.

## Images

Images should be placed in the `./data` directory (or specify a custom directory with `-d`). The image filenames in the JSON should match the files in the data directory.

## Examples

### Basic Example

See `example.json` for a sample input file with basic cards and images.

```bash
# Create data directory and add images
mkdir -p data

# Generate the Anki package
anki-generator example.json -o my_deck.apkg
```

### LaTeX Example

See `example_latex.json` for a sample input file with mathematical equations.

```bash
# Generate the Anki package with LaTeX equations
anki-generator example_latex.json -o math_deck.apkg
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