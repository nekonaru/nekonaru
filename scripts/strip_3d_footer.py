"""Strip the bottom action bar (total contributions, star count, fork count, date range)
from the 3D contribution SVG.

The 3D contribution action always renders this bar. We do not want it because the streak
card already shows the total contributions. This script is run by GitHub Actions after the
SVG is generated, on every run, so the strip survives regeneration.

Usage: python strip_3d_footer.py profile-3d-contrib/profile-night-rainbow.svg
Standard library only.
"""
import sys

FOOTER_MARK = '<g><text style="font-size: 32px; font-weight: bold;"'


def strip_footer(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.strip().endswith("</svg>"):
        raise SystemExit(f"{path} does not look like an SVG (missing closing tag)")
    idx = content.rfind(FOOTER_MARK)
    if idx == -1:
        raise SystemExit(f"Footer marker not found in {path}; the 3D contribution layout may have changed")
    prefix = content[:idx]
    if prefix.count("<g") != prefix.count("</g>"):
        raise SystemExit(f"Unbalanced <g> tags after stripping footer in {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(prefix + "</svg>\n")
    print(f"Stripped footer from {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python strip_3d_footer.py <path-to-night-rainbow.svg>")
    strip_footer(sys.argv[1])
