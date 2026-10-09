# TODO

Open tasks for this repository.

## 1. Update to v2

- [x] Tag the original version as `v1.0.0`
- [x] Add `pyproject.toml` and `uv.lock` with genanki, Ruff and pytest
- [x] Fix skipped lines with a note after the term, e.g. `(AUS)`
- [x] Use stable deck, note type and note IDs so re-imports update the deck
- [x] Add tests, an example file and a CI workflow
- [ ] Import a generated deck into Anki once by hand (not tested automatically, to keep the personal collection untouched)

## 2. Before publishing

- [x] Add the MIT license
- [x] Rewrite the old university e-mail address in the commit history
- [ ] Push the rewritten `main` and the tags, check that CI passes
- [ ] Create GitHub releases for `v1.0.0` and `v2.0.0`
- [ ] Add a description and topics on GitHub
