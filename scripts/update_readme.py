"""Update the automated sections in the profile README (latest repos as visual cards).

Standard library only. Run by GitHub Actions, or locally: python scripts/update_readme.py
"""
import json
import os
import re
import urllib.request
from datetime import datetime
from urllib.parse import quote

USER = os.environ.get("GH_USER", "nekonaru")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = os.path.join(os.path.dirname(__file__), "..", "README.md")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# shields.io badge style for each language: hex color, simple-icons slug, text color
LANG_BADGES = {
    "Dart": ("0175C2", "dart", "white"),
    "C#": ("512BD4", "csharp", "white"),
    "Rust": ("000000", "rust", "white"),
    "Python": ("3776AB", "python", "white"),
    "TypeScript": ("3178C6", "typescript", "white"),
    "JavaScript": ("F7DF1E", "javascript", "black"),
    "HTML": ("E34F26", "html5", "white"),
    "CSS": ("1572B6", "css3", "white"),
    "Flutter": ("02569B", "flutter", "white"),
    "Kotlin": ("7F52FF", "kotlin", "white"),
    "Go": ("00ADD8", "go", "white"),
    "Java": ("E76F00", "openjdk", "white"),
    "C++": ("00599C", "cplusplus", "white"),
    "PHP": ("777BB4", "php", "white"),
    "Ruby": ("CC342D", "ruby", "white"),
    "Swift": ("F05138", "swift", "white"),
    "Shell": ("4EAA25", "gnubash", "white"),
    "Vue": ("4FC08D", "vuedotjs", "white"),
    "Svelte": ("FF3E00", "svelte", "white"),
}


def api(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme-updater",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def format_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def clean(text, limit=90):
    text = (text or "").replace("|", "/").replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lang_badge(language):
    if not language:
        return '<img src="https://img.shields.io/badge/language-unknown-24283b?style=flat-square" alt="Unknown language" />'
    color, logo, logo_color = LANG_BADGES.get(language, ("24283b", None, "white"))
    label = quote(language, safe="")
    src = f"https://img.shields.io/badge/{label}-{color}?style=flat-square&logoColor={logo_color}"
    if logo:
        src += f"&logo={logo}"
    return f'<img src="{src}" alt="{esc(language)}" />'


def stars_badge(repo_name):
    src = f"https://img.shields.io/github/stars/{USER}/{repo_name}?style=flat-square&color=c792ea"
    return f'<img src="{src}" alt="Stars" />'


def repo_languages():
    repos = api(f"/users/{USER}/repos?sort=pushed&per_page=100&type=owner")
    repos = [r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() != USER.lower()]
    totals = {}
    for r in repos:
        try:
            langs = api(f"/repos/{USER}/{r['name']}/languages")
        except Exception:
            continue
        for lang, size in langs.items():
            totals[lang] = totals.get(lang, 0) + size
    return totals


def top_language_badge():
    totals = repo_languages()
    if not totals:
        return '![Top Language](https://img.shields.io/badge/Top%20Lang-unknown-24283b?style=flat-square)'
    language = max(totals, key=totals.get)
    color, logo, logo_color = LANG_BADGES.get(language, ("24283b", None, "white"))
    src = f"https://img.shields.io/badge/Top%20Lang-{quote(language, safe='')}-{color}?style=flat-square&logoColor={logo_color}"
    if logo:
        src += f"&logo={logo}"
    return f"![Top Language]({src})"


def repo_cards():
    repos = api(f"/users/{USER}/repos?sort=pushed&per_page=100&type=owner")
    repos = [r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() != USER.lower()]
    repos = repos[:3]
    if not repos:
        return "_No public repositories yet._"
    cells = []
    for r in repos:
        name = esc(r["name"])
        url = r["html_url"]
        desc = esc(clean(r["description"], 90)) or "No description yet."
        date = format_date(r["pushed_at"])
        cells.append(
            "\n".join(
                [
                    '<td align="center" width="33%">',
                    f'<b><a href="{url}">{name}</a></b><br/>',
                    f'<sub>{desc}</sub><br/><br/>',
                    f"{lang_badge(r['language'])} {stars_badge(r['name'])}<br/>",
                    f'<sub>Updated {date}</sub>',
                    "</td>",
                ]
            )
        )
    return "<table>\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"


def replace_block(text, name, body, inline=False):
    pattern = re.compile(rf"(<!--START_SECTION:{name}-->)(.*?)(<!--END_SECTION:{name}-->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"Marker {name} not found in README")
    if inline:
        return pattern.sub(lambda m: f"{m.group(1)}{body}{m.group(3)}", text)
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main():
    with open(README, encoding="utf-8") as f:
        text = f.read()
    text = replace_block(text, "repos", repo_cards())
    text = replace_block(text, "toplang", top_language_badge(), inline=True)
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)
    print("README updated")


if __name__ == "__main__":
    main()
