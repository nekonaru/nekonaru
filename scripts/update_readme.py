"""Update the automated sections in the profile README (latest repos and recent activity).

Standard library only. Run by GitHub Actions, or locally: python scripts/update_readme.py
"""
import json
import os
import re
import urllib.request
from datetime import datetime

USER = os.environ.get("GH_USER", "nekonaru")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = os.path.join(os.path.dirname(__file__), "..", "README.md")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


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


def repo_table():
    repos = api(f"/users/{USER}/repos?sort=pushed&per_page=100&type=owner")
    repos = [r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() != USER.lower()]
    repos = repos[:6]
    if not repos:
        return "_No public repositories yet._"
    rows = ["| Project | Description | Language | Stars | Updated |", "| :-- | :-- | :-- | :-: | :-- |"]
    for r in repos:
        rows.append(
            f"| **[{r['name']}]({r['html_url']})** | {clean(r['description']) or '-'} | "
            f"{r['language'] or '-'} | {r['stargazers_count']} | {format_date(r['pushed_at'])} |"
        )
    return "\n".join(rows)


def activity_list():
    try:
        events = api(f"/users/{USER}/events/public?per_page=60")
    except Exception:
        return "_Activity could not be loaded._"
    lines, seen = [], set()
    for e in events:
        repo = e["repo"]["name"]
        url = f"https://github.com/{repo}"
        if e["type"] == "PushEvent":
            commits = e["payload"].get("commits") or []
            msg = clean(commits[-1]["message"].split("\n")[0], 70) if commits else "update"
            line = f"- Push to [{repo}]({url}): `{msg}` ({format_date(e['created_at'])})"
        elif e["type"] == "CreateEvent" and e["payload"].get("ref_type") == "repository":
            line = f"- Created repository [{repo}]({url}) ({format_date(e['created_at'])})"
        elif e["type"] == "ReleaseEvent":
            tag = e["payload"]["release"]["tag_name"]
            line = f"- Released `{tag}` in [{repo}]({url}) ({format_date(e['created_at'])})"
        else:
            continue
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
        if len(lines) >= 5:
            break
    return "\n".join(lines) or "_No recent public activity._"


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!--START_SECTION:{name}-->)(.*?)(<!--END_SECTION:{name}-->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"Marker {name} not found in README")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main():
    with open(README, encoding="utf-8") as f:
        text = f.read()
    text = replace_block(text, "repos", repo_table())
    text = replace_block(text, "activity", activity_list())
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)
    print("README updated")


if __name__ == "__main__":
    main()
