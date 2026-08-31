# One-shot generators (do not re-run)

These scripts built the twelve `Slides/Unit_*.tex` decks once, by converting and
merging the 15-module draft in `../../Archive_Modules/`. They have done their job.

**The `.tex` files are now the source of truth.** Re-running anything in this folder
would overwrite `Slides/Unit_*.tex` and discard any edits made since.

They are kept only so the conversion is reproducible and auditable. If you ever do want
to regenerate a deck from the archived module, copy your current `.tex` somewhere safe
first.

Safe to re-run at any time (they live in `../`):

- `compile.sh <deck>` rebuilds one PDF from its `.tex`
- `build_unitNN.py` rebuilds a unit's homework and code companion
- `make_module*_slide_figs.py` regenerates the figures
- `polish_decks.py`, `polish_notebooks.py`, `polish_activities.py` re-apply the voice
  and activity conventions in place, and leave your own edits alone
