# Anki Deck Generator from Markdown

This Python script automatically generates Anki decks from Markdown files. It is designed to create flashcards with a term on the front and its definition on the back. Optionally, it can reverse the cards, placing the definition on the front and the term on the back.

## Features

- **Automatic Deck Generation**: Converts Markdown files into Anki decks.
- **Reversible Cards**: Option to reverse the question and answer on the cards.
- **CLI Support**: Easily use the script from the command line.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later installed on your system.
- Anki installed on your system to import and use the generated decks.
- The `genanki` Python package installed. You can install it using pip:

  ```bash
  pip install genanki
  ```

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/anki-deck-generator.git
   ```

2. Navigate into the cloned repository:

   ```bash
   cd anki-deck-generator
   ```

3. Ensure you have the required Python packages installed:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the script, run it from the command line, providing the path to your Markdown file and the desired name for your Anki deck. Optionally, you can include the `--reverse` flag to reverse the front and back of the cards.

```bash
python create_anki_deck.py <path_to_markdown_file> <deck_name> [--reverse]
```

### Example

To create a deck named "Phrasal Verbs":

```bash
python create_anki_deck.py "Phrasal Verbs.md" "Phrasal Verbs"
```

To create the same deck with reversed cards:

```bash
python create_anki_deck.py "Phrasal Verbs.md" "Phrasal Verbs" --reverse
```

### Markdown File Format

Your Markdown file should follow this format:

``` markdown
- **Term 1** - Definition of term 1.
- **Term 2** - Definition of term 2.
- **Term 3** - Definition of term 3.
```

Each line represents a flashcard, with the term bolded and its definition following the dash.

Example `Phrasal Verbs.md`:

``` markdown
- **Back out of** - To withdraw from a commitment or promise.
- **Bail up** (AUS) - To corner someone and start a conversation; historically, to rob someone.
- **Bang on about** (AUS) - To talk about something for a long time, especially in a way that is boring to others.
```
