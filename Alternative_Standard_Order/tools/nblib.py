"""Helpers for building Stat 220 lecture code notebooks and homework notebooks."""
from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
DATA = "https://richardson.byu.edu/220"


class CodeNB:
    """A lecture code companion: markdown narration + runnable cells."""

    def __init__(self, unit, title, blurb):
        self.cells = []
        self.unit = unit
        self.md(f"# Unit {unit} code companion: {title}\n\n{blurb}\n\n"
                "Run the cells in order. Each section matches a moment in the slides. The point is "
                "to see the mechanism move when you change the inputs, so change them.")

    def md(self, t):
        self.cells.append(nbf.v4.new_markdown_cell(t))

    def code(self, t):
        self.cells.append(nbf.v4.new_code_cell(t))

    def section(self, title, text=""):
        self.md(f"## {title}\n\n{text}")

    def write(self, filename, execute=True, timeout=600):
        nb = nbf.v4.new_notebook()
        nb["cells"] = self.cells
        nb["metadata"] = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        }
        out = ROOT / "Notebooks" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        if execute:
            client = NotebookClient(nb, timeout=timeout, kernel_name="python3",
                                    resources={"metadata": {"path": str(out.parent)}})
            client.execute()
        nbf.write(nb, out)
        n_err = sum(1 for c in nb.cells for o in c.get("outputs", [])
                    if o.get("output_type") == "error")
        print(f"wrote {out.name}  ({len(nb.cells)} cells, executed={execute}, errors={n_err})")
        return n_err


AUTOGRADER = Path("/Users/robertrichardson/Library/CloudStorage/"
                  "GoogleDrive-richardson@stat.byu.edu/My Drive/BYU Classes/220/Autograder")

_ANCHOR_RE = None


def _anchor_regex():
    """The autograder's own problem-anchor pattern, so we validate against the real thing."""
    global _ANCHOR_RE
    if _ANCHOR_RE is None:
        import re
        _ANCHOR_RE = re.compile(r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*|__|\*|_)?[ \t]*"
                                r"(?:problem|question|q)[ \t]*([0-9]{1,2})\b")
    return _ANCHOR_RE


class HW:
    """Homework in the autograder's `**Problem N**` / `Part a.` structure.

    The autograder splits on any line that *starts* with "Problem N", so prose like
    "Problem 1 is a simulation lab" at the head of a line silently creates a phantom
    section. `write()` validates against the real splitter and refuses to pass quietly.
    """

    def __init__(self, unit, title, intro):
        self.cells = []
        self.ids = []
        stray = _anchor_regex().findall(intro)
        if stray:
            raise ValueError(
                f"Unit {unit} intro begins a line with 'Problem/Question {stray}'. "
                "The autograder would treat that as a problem heading. Rephrase "
                "(e.g. 'The first problem is...').")
        self.md(f"# Stat 220, Unit {unit} Homework: {title}\n\n{intro}")

    def md(self, t):
        self.cells.append(nbf.v4.new_markdown_cell(t))

    def code(self, t=""):
        self.cells.append(nbf.v4.new_code_cell(t))

    def answer(self):
        self.cells.append(nbf.v4.new_markdown_cell("_Your answer:_\n\n"))

    def problem(self, n, text):
        self.ids.append(n)
        self.md(f"**Problem {n}.** {text}")

    def part(self, letter, text, kind="code"):
        self.md(f"Part {letter}. {text}")
        if kind == "code":
            self.code()
        else:
            self.answer()

    def write(self, filename):
        nb = nbf.v4.new_notebook()
        nb["cells"] = self.cells
        nb["metadata"] = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        }
        out = ROOT / "Homework" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        nbf.write(nb, out)

        # Validate against the autograder's real splitter, not a lookalike.
        import sys
        status = "unchecked"
        if AUTOGRADER.exists():
            sys.path.insert(0, str(AUTOGRADER))
            try:
                from autograder.ingest import split_submission
                found = sorted(split_submission(out).keys())
                if found != sorted(self.ids):
                    raise AssertionError(
                        f"{out.name}: autograder sees problems {found}, expected "
                        f"{sorted(self.ids)}. Check for stray 'Problem N' at a line start.")
                status = f"autograder sees {found}"
            finally:
                sys.path.remove(str(AUTOGRADER))
        print(f"wrote {out.name}  ({len(nb.cells)} cells, {status})")
