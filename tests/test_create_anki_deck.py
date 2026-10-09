import sqlite3
import zipfile

from create_anki_deck import build_deck, main, parse_markdown, stable_id


def test_parse_simple_item():
    assert parse_markdown("- **Back out of** - To withdraw.") == [("Back out of", "To withdraw.")]


def test_parse_keeps_note_after_term():
    assert parse_markdown("- **Bail up** (AUS) - To corner someone.") == [("Bail up (AUS)", "To corner someone.")]


def test_parse_keeps_dashes_in_definition():
    assert parse_markdown("* **Term** – A - B") == [("Term", "A - B")]


def test_parse_ignores_other_lines():
    assert parse_markdown("# Title\n\nSome text\n- plain item - no bold term\n") == []


def test_ids_are_stable():
    assert stable_id("Deck") == stable_id("Deck")
    assert stable_id("Deck") != stable_id("Other deck")
    assert 0 < stable_id("Deck") < 2**31


def test_reverse_swaps_fields_and_escapes_html():
    deck = build_deck([("a < b", "Definition")], "Deck", reverse=True)
    assert deck.notes[0].fields == ["Definition", "a &lt; b"]


def test_main_writes_package(tmp_path):
    md = tmp_path / "words.md"
    md.write_text("- **One** - First\n- **Two** (x) - Second\n", encoding="utf-8")
    out = tmp_path / "deck.apkg"

    assert main([str(md), "Test", "-o", str(out)]) == 0

    with zipfile.ZipFile(out) as package:
        package.extract("collection.anki2", tmp_path)
    with sqlite3.connect(tmp_path / "collection.anki2") as db:
        assert db.execute("select count(*) from notes").fetchone()[0] == 2


def test_main_fails_without_cards(tmp_path, capsys):
    md = tmp_path / "empty.md"
    md.write_text("nothing here\n", encoding="utf-8")
    assert main([str(md), "Test"]) == 1
    assert "No cards found" in capsys.readouterr().err
