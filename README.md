<div align="center">

# Anki Deck Generator

**Turn a Markdown list of terms and definitions into an Anki deck**

[![CI](https://github.com/HuberNicolas/anki-deck-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/HuberNicolas/anki-deck-generator/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Anki](https://img.shields.io/badge/Anki-80C2EE?logo=anki&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-yellow)

[Quick start](#quick-start) · [Markdown format](#markdown-format) · [Usage](#usage)

</div>

A single Python script that reads a Markdown file with lines like `- **Term** - Definition` and writes an `.apkg`
file that you can import into [Anki](https://apps.ankiweb.net/). It uses [genanki](https://github.com/kerrickstaley/genanki).

## Features

- 📝 One card per list item: bold term on the front, definition on the back
- 🔁 `--reverse` creates a second deck with the definition on the front
- ♻️ Re-importing an updated file updates the existing cards instead of creating duplicates
- 🏷️ Notes after the term, such as `(AUS)`, stay part of the term

> [!NOTE]
> Written in February 2024 as a small personal tool for learning vocabulary. The original version is tagged
> [`v1.0.0`](https://github.com/HuberNicolas/anki-deck-generator/tree/v1.0.0). Version 2 fixes two bugs of that
> version (see [Changes since v1.0.0](#changes-since-v100)) and adds tests, but the tool stays a single script.

## Contents

- [Quick start](#quick-start)
- [Markdown format](#markdown-format)
- [Usage](#usage)
- [Repository structure](#repository-structure)
- [Development](#development)
- [Changes since v1.0.0](#changes-since-v100)
- [License](#license)
- [Author](#author)

## Quick start

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and Anki.

1. Clone the repository:

   ```bash
   git clone https://github.com/HuberNicolas/anki-deck-generator.git
   ```

   ```bash
   cd anki-deck-generator
   ```

2. Create a deck from the example file. uv installs Python and genanki on the first run:

   ```bash
   uv run create_anki_deck.py examples/phrasal-verbs.md "Phrasal Verbs"
   ```

3. In Anki, choose **File → Import** and select `Phrasal_Verbs.apkg`.

Without uv, install the dependency with `pip install genanki` and run the script with `python create_anki_deck.py …`.

## Markdown format

Each card is a list item with the term in bold, followed by a dash and the definition:

```markdown
- **Back out of** - To withdraw from a commitment or promise.
- **Bail up** (AUS) - To corner someone and start a conversation; historically, to rob someone.
```

- List markers `-`, `*` and `+` work; the separator can be `-`, `–` or `—` with spaces around it.
- Text between the bold term and the separator, such as `(AUS)`, is added to the term: `Bail up (AUS)`.
- All other lines (headings, text, items without a bold term) are ignored.
- The text is shown as plain text in Anki. Markdown formatting inside the definition is not converted.

See [`examples/phrasal-verbs.md`](examples/phrasal-verbs.md) for a complete file.

## Usage

```bash
uv run create_anki_deck.py <markdown_file> <deck_name> [--reverse] [-o OUTPUT]
```

| Option | Effect |
|---|---|
| `markdown_file` | Path to the Markdown file |
| `deck_name` | Name of the deck in Anki |
| `--reverse` | Definition on the front, term on the back. Adds ` (Reversed)` to the deck name, so both decks can exist side by side |
| `-o`, `--output` | Output file. Default: the deck name with spaces replaced by `_`, plus `.apkg`, in the current folder |

Create the reversed deck:

```bash
uv run create_anki_deck.py examples/phrasal-verbs.md "Phrasal Verbs" --reverse
```

To add or change cards later, edit the Markdown file, run the script again with the same deck name and import the new
file. Anki updates cards with the same term and adds new ones. Cards whose term you removed or renamed stay in Anki
until you delete them there.

## Repository structure

| Path | Content |
|---|---|
| [`create_anki_deck.py`](create_anki_deck.py) | The script: Markdown parser, deck builder and command line interface |
| [`examples/`](examples) | Example word list |
| [`tests/`](tests) | pytest tests |
| [`pyproject.toml`](pyproject.toml), [`uv.lock`](uv.lock) | Dependencies and tool configuration |

## Development

| Task | Command |
|---|---|
| Run the tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |

The [CI workflow](.github/workflows/ci.yml) runs the same checks on Python 3.10 and 3.13 for every push.

## Changes since v1.0.0

- **Fixed:** Lines with text between the term and the dash, such as `- **Bail up** (AUS) - …`, were skipped without
  a message, including two of the three examples in the old README.
- **Fixed:** Each run created a new deck in Anki, because the IDs came from the current time. IDs are now derived from
  the deck name and the term.
- Added `--output`, an error message when no cards are found, HTML escaping of the card text, `pyproject.toml` with
  `uv.lock` (the old README referred to a `requirements.txt` that did not exist), tests and CI.

## License

[MIT](LICENSE) © 2024 Nicolas Huber

## Author

Nicolas Huber · [GitHub](https://github.com/HuberNicolas)
