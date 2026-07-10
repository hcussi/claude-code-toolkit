#!/usr/bin/env python3
"""Render every ```mermaid fenced block in a Markdown file to an image file and
rewrite the fence as a Markdown image reference.

For each mermaid block the script writes an image into a sibling folder
(default: "<md-stem>-diagrams/") and replaces the fenced block in place with:

    ![<alt>](<md-stem>-diagrams/diagram-N.png)

The alt text comes from an optional "%% alt: <text>" comment inside the block
(mermaid ignores "%%" comments, so the diagram is unaffected); without one it
falls back to "Diagram N". Output is always PNG named diagram-N; the script never
emits .svg, .mmd, or config files.

Rendering backends (choose with --renderer):
  * mmdc  - the local mermaid-cli binary (offline, no network). Requires
            "mmdc" on PATH (npm i -g @mermaid-js/mermaid-cli).
  * ink   - the hosted mermaid.ink renderer (needs network access).
  * auto  - use mmdc if it is installed, otherwise fall back to ink (default).

The Markdown file is edited in place. Pass --backup for a transient "<file>.bak"
safety net: it is written before the overwrite and removed once the write
succeeds, so no backup file is left behind (it survives only if the write fails).
Re-running is safe: once fences are replaced by images there is nothing left to
convert.

Snippet mode (--snippet OUT): read a single mermaid diagram from stdin and render
it to OUT without touching any Markdown file. Use this to preview a diagram (for
example an ASCII diagram just translated to mermaid) before committing it into a
document.
"""

from __future__ import annotations

import argparse
import base64
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

# Matches a fenced mermaid block, preserving any leading indentation so the
# replacement lands in the same spot. Non-greedy body stops at the first closing
# fence.
FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)```[ \t]*mermaid[ \t]*\r?\n"
    r"(?P<code>.*?)\r?\n"
    r"(?P=indent)?```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)

# An optional "%% alt: ..." mermaid comment inside a block supplies the image's
# alt text. Mermaid ignores "%%" comment lines when rendering, so the diagram is
# unaffected; the script reads it to make the replacement's alt text descriptive
# instead of a generic "Diagram N". Authoring the alt text in the source keeps
# the whole conversion deterministic.
ALT_RE = re.compile(r"^[ \t]*%%[ \t]*alt:[ \t]*(?P<alt>.+?)[ \t]*$", re.IGNORECASE | re.MULTILINE)


def extract_alt(code: str) -> str | None:
    """Return the alt text from a '%% alt: ...' comment in the block, if present.

    The result is sanitized for use inside Markdown image alt text: newlines are
    collapsed and ']' (which would close the alt) is neutralized.
    """
    match = ALT_RE.search(code)
    if not match:
        return None
    alt = " ".join(match.group("alt").split()).replace("]", ")")
    return alt or None


def have_mmdc() -> bool:
    return shutil.which("mmdc") is not None


def render_failure_hint(renderer: str) -> str:
    """Actionable remediation printed when rendering fails.

    The point is to make *stopping and fixing the environment* the obvious next
    step, so a caller is not tempted to invent an alternative renderer.
    """
    common = (
        "\nThis script is the ONLY supported way to produce the images. Do NOT\n"
        "substitute another renderer: no browser/Playwright screenshots, no local\n"
        "HTTP server, no SVG-to-PNG rasterization, no hand-drawn images. Fix the\n"
        "environment (see above) and re-run, or stop and report this to the user."
    )
    if renderer == "ink":
        return (
            "The mermaid.ink renderer needs network access to https://mermaid.ink.\n"
            "Do ONE of these, then re-run:\n"
            "  - enable outbound network for this command, or\n"
            "  - install mermaid-cli for offline rendering, then re-run (auto-used):\n"
            "      npm install -g @mermaid-js/mermaid-cli" + common
        )
    return "The mermaid-cli (mmdc) renderer failed; see the error above." + common


def render_with_mmdc(code: str, out_path: Path, theme: str, background: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(code)
        tmp_path = Path(tmp.name)
    try:
        cmd = [
            "mmdc",
            "-i",
            str(tmp_path),
            "-o",
            str(out_path),
            "-t",
            theme,
            "-b",
            background,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(
                f"mmdc failed ({proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
            )
    finally:
        tmp_path.unlink(missing_ok=True)


def ink_bgcolor(background: str) -> str | None:
    """Translate a --background value into a mermaid.ink bgColor query value.

    Returns None for a transparent background (omit the param). mermaid.ink wants
    a bare hex code (e.g. "ffffff") or a CSS color name prefixed with "!"
    (e.g. "!white").
    """
    bg = background.strip().lstrip("#")
    if bg.lower() == "transparent":
        return None
    is_hex = len(bg) in (3, 6, 8) and all(c in "0123456789abcdefABCDEF" for c in bg)
    return bg if is_hex else f"!{bg}"


def render_with_ink(
    code: str, out_path: Path, fmt: str, theme: str, background: str, retries: int = 3
) -> None:
    encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
    kind = "svg" if fmt == "svg" else "img"
    url = f"https://mermaid.ink/{kind}/{encoded}?theme={theme}"
    if fmt == "png":
        url += "&type=png"
    bgcolor = ink_bgcolor(background)
    if bgcolor is not None:
        url += f"&bgColor={bgcolor}"
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mermaid-to-images"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if not data:
                raise RuntimeError("empty response from mermaid.ink")
            out_path.write_bytes(data)
            return
        except (urllib.error.URLError, RuntimeError) as err:
            last_err = err
            if attempt < retries:
                time.sleep(1.5 * attempt)
    raise RuntimeError(f"mermaid.ink request failed: {last_err}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "md_file",
        type=Path,
        nargs="?",
        help="Markdown file to process (edited in place). Omit when using --snippet.",
    )
    parser.add_argument(
        "--snippet",
        type=Path,
        default=None,
        metavar="OUT",
        help="Render a single mermaid diagram read from stdin to OUT, then exit "
        "(no Markdown file is touched). Use it to preview a translation.",
    )
    parser.add_argument(
        "--renderer",
        choices=["auto", "mmdc", "ink"],
        default="auto",
        help="Rendering backend (default: auto)",
    )
    parser.add_argument(
        "--format",
        choices=["png", "svg"],
        default="png",
        help="Image format (default: png)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output folder for images (default: <md-stem>-diagrams next to the file)",
    )
    parser.add_argument("--theme", default="default", help="Mermaid theme (default: default)")
    parser.add_argument(
        "--background",
        default="white",
        help="Image background color, e.g. white, #ffffff, or transparent "
        "(default: white). An opaque background keeps mermaid's gray message "
        "labels readable; transparent can make them vanish on dark surfaces.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Write a transient <file>.bak before overwriting and remove it once "
        "the write succeeds (kept only if the write fails, for recovery)",
    )
    args = parser.parse_args()

    renderer = args.renderer
    if renderer == "auto":
        renderer = "mmdc" if have_mmdc() else "ink"
    if renderer == "mmdc" and not have_mmdc():
        print(
            "error: --renderer mmdc requested but 'mmdc' is not on PATH.\n"
            "Install it with: npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        return 1

    def render(code: str, out_path: Path) -> None:
        if renderer == "mmdc":
            render_with_mmdc(code, out_path, args.theme, args.background)
        else:
            render_with_ink(code, out_path, args.format, args.theme, args.background)

    # Snippet mode: render one diagram from stdin and exit, no Markdown involved.
    if args.snippet is not None:
        code = sys.stdin.read().strip()
        if not code:
            print("error: --snippet expects a mermaid diagram on stdin", file=sys.stderr)
            return 1
        out_path: Path = args.snippet
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            render(code, out_path)
        except Exception as err:  # noqa: BLE001 - surface any backend failure clearly
            print(
                f"error rendering snippet: {err}\n\n{render_failure_hint(renderer)}",
                file=sys.stderr,
            )
            return 1
        print(f"Rendered snippet with '{renderer}' -> {out_path}")
        return 0

    if args.md_file is None:
        print("error: a Markdown file is required (or use --snippet)", file=sys.stderr)
        return 1
    md_path: Path = args.md_file
    if not md_path.is_file():
        print(f"error: not a file: {md_path}", file=sys.stderr)
        return 1

    text = md_path.read_text(encoding="utf-8")
    blocks = list(FENCE_RE.finditer(text))
    if not blocks:
        print(f"No ```mermaid blocks found in {md_path}. Nothing to do.")
        return 0

    out_dir = args.out or md_path.parent / f"{md_path.stem}-diagrams"
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "svg" if args.format == "svg" else "png"

    print(f"Found {len(blocks)} mermaid block(s). Rendering with '{renderer}' -> {out_dir}/")

    # Build the replacements first (rendering may fail), then rewrite the text in a
    # single pass so earlier match offsets stay valid.
    replacements: list[tuple[int, int, str]] = []
    for i, match in enumerate(blocks, start=1):
        code = match.group("code")
        indent = match.group("indent")
        img_path = out_dir / f"diagram-{i}.{ext}"
        try:
            render(code, img_path)
        except Exception as err:  # noqa: BLE001 - surface any backend failure clearly
            print(
                f"error rendering block {i}: {err}\n\n{render_failure_hint(renderer)}",
                file=sys.stderr,
            )
            return 1
        rel = img_path.relative_to(md_path.parent).as_posix()
        alt = extract_alt(code) or f"Diagram {i}"
        replacements.append((match.start(), match.end(), f"{indent}![{alt}]({rel})"))
        print(f"  block {i} -> {img_path}  (alt: {alt!r})")

    new_parts: list[str] = []
    cursor = 0
    for start, end, repl in replacements:
        new_parts.append(text[cursor:start])
        new_parts.append(repl)
        cursor = end
    new_parts.append(text[cursor:])
    new_text = "".join(new_parts)

    # The backup is a transient safety net: written before the overwrite so the
    # original survives a failed write, then removed once the write succeeds so no
    # .bak clutter is left behind.
    backup: Path | None = None
    if args.backup:
        backup = md_path.with_suffix(md_path.suffix + ".bak")
        backup.write_text(text, encoding="utf-8")

    try:
        md_path.write_text(new_text, encoding="utf-8")
    except OSError as err:
        if backup is not None:
            print(
                f"error writing {md_path}: {err}\noriginal preserved at {backup}",
                file=sys.stderr,
            )
        else:
            print(f"error writing {md_path}: {err}", file=sys.stderr)
        return 1

    if backup is not None:
        backup.unlink(missing_ok=True)

    print(f"Updated {md_path}: replaced {len(replacements)} block(s) with image references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
