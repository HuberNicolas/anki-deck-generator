"""Create an Anki deck from a Markdown list of terms and definitions.

Each card comes from a list item like ``- **Term** - Definition``.
"""

import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

import genanki

# "- **Term** (note) - Definition": the optional note after the bold term stays part of the term.
# The separator is a hyphen, en dash or em dash surrounded by spaces.
LINE_PATTERN = re.compile(r"^\s*[-*+]\s+\*\*(?P<term>.+?)\*\*(?P<note>.*?)\s+[-–—]\s+(?P<definition>.+?)\s*$")


def stable_id(name: str) -> int:
    """Derive a deterministic 31-bit ID from a name.

    Anki identifies decks and note types by ID. A stable ID lets a re-import update the existing deck
    instead of creating a second one.
    """
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:8], 16) >> 1


def parse_markdown(text: str) -> list[tuple[str, str]]:
    """Return (term, definition) pairs for all list items that match LINE_PATTERN."""
    notes = []
    for line in text.splitlines():
        match = LINE_PATTERN.match(line)
        if match:
            term = (match["term"] + match["note"]).strip()
            notes.append((term, match["definition"]))
    return notes


def build_deck(notes: list[tuple[str, str]], deck_name: str, reverse: bool = False) -> genanki.Deck:
    """Build a deck with one card per note; with reverse=True the definition is the question."""
    model_name = "Anki Deck Generator (Reversed)" if reverse else "Anki Deck Generator"
    model = genanki.Model(
        model_id=stable_id(model_name),
        name=model_name,
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )
    deck = genanki.Deck(deck_id=stable_id(f"deck:{deck_name}"), name=deck_name)

    for term, definition in notes:
        question, answer = (definition, term) if reverse else (term, definition)
        deck.add_note(
            genanki.Note(
                model=model,
                fields=[html.escape(question), html.escape(answer)],
                # Keyed on the term, so editing a definition updates the card instead of adding a new one.
                guid=genanki.guid_for(deck_name, term, reverse),
            )
        )
    return deck


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an Anki deck from a Markdown file.")
    parser.add_argument("md_file_path", type=Path, help="path to the Markdown file")
    parser.add_argument("deck_name", help="name of the Anki deck")
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="generate reversed cards (definition as question, term as answer)",
    )
    parser.add_argument("-o", "--output", type=Path, help="output file (default: <deck_name>.apkg)")
    args = parser.parse_args(argv)

    notes = parse_markdown(args.md_file_path.read_text(encoding="utf-8"))
    if not notes:
        print(f"No cards found in {args.md_file_path}. Expected lines like: - **Term** - Definition", file=sys.stderr)
        return 1

    deck_name = f"{args.deck_name} (Reversed)" if args.reverse else args.deck_name
    output = args.output or Path(f"{deck_name.replace(' ', '_')}.apkg")
    genanki.Package(build_deck(notes, deck_name, args.reverse)).write_to_file(output)
    print(f"Deck '{deck_name}' with {len(notes)} cards saved to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
