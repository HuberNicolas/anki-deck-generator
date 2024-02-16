import genanki
import re
import argparse
import hashlib
import time

# Setup command line argument parsing
parser = argparse.ArgumentParser(description='Create an Anki deck from a Markdown file.')
parser.add_argument('md_file_path', type=str, help='Path to the Markdown file')
parser.add_argument('deck_name', type=str, help='Name of the Anki deck')
parser.add_argument('--reverse', action='store_true', help='Generate reversed cards (definition as question, term as answer)')

args = parser.parse_args()

# Function to generate a unique ID based on the deck name
def generate_id(name):
    hash_input = (name + str(time.time())).encode('utf-8')
    hash_output = hashlib.sha256(hash_input).hexdigest()
    return int(hash_output[:8], 16)

# Function to parse the Markdown file
def parse_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    notes = []
    for line in lines:
        match = re.match(r'- \*\*(.*)\*\* - (.*)', line)
        if match:
            term, definition = match.groups()
            notes.append((term, definition))
    return notes

# Function to create an Anki deck and add notes
def create_anki_deck(notes, deck_name, reverse=False):
    if reverse:
        deck_name += " (Reversed)"
        model_name = 'Simple Model (Reversed)'
    else:
        model_name = 'Simple Model'

    deck_id = generate_id(deck_name + 'deck')
    model_id = generate_id(deck_name + 'model')

    my_deck = genanki.Deck(
        deck_id=deck_id,
        name=deck_name,
    )

    my_model = genanki.Model(
        model_id=model_id,
        name=model_name,
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',  # Front of the card
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',  # Back of the card
            },
        ],
    )

    for term, definition in notes:
        if reverse:
            term, definition = definition, term  # Flip term and definition
        note = genanki.Note(
            model=my_model,
            fields=[term, definition]
        )
        my_deck.add_note(note)

    # Save the deck to a file
    output_file_name = f"{deck_name.replace(' ', '_')}.apkg"
    genanki.Package(my_deck).write_to_file(output_file_name)
    print(f"Deck '{deck_name}' created successfully and saved to {output_file_name}")

# Main process
if __name__ == "__main__":
    notes = parse_md_file(args.md_file_path)
    create_anki_deck(notes, args.deck_name, args.reverse)
