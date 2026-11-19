"""Generate the illustrated stack and AI toolbox panels for the profile README.

Standard library only. Run: python scripts/build_icon_panels.py
Outputs into assets/. Icons are inlined as base64 <image> elements so the SVGs
stay self-contained and render on GitHub.
"""
import base64
import os
import re
import urllib.request

HERE = os.path.join(os.path.dirname(__file__), "..", "assets")

BG = "#0d1117"
PANEL = "#161b22"
PANEL_SOFT = "#21262d"
BORDER = "#30363d"
FG = "#e6edf3"
MUTED = "#8b949e"
STRONG = "#f0f6fc"
GREEN = "#39d353"
ORANGE = "#ff9e64"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
FONT = "'JetBrains Mono', 'Consolas', monospace"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_doc(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">\n'
        f'<title>{esc(title)}</title>\n{body}\n</svg>\n'
    )


def b64(url):
    req = urllib.request.Request(url, headers={"User-Agent": "nekonaru-profile-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return base64.b64encode(resp.read()).decode("ascii")


def icon_ref(name):
    icons = {
        "dart": ("https://cdn.simpleicons.org/dart", "dart"),
        "cs": ("https://cdn.simpleicons.org/dotnet", "cs"),
        "rust": ("https://cdn.simpleicons.org/rust", "rust"),
        "ts": ("https://cdn.simpleicons.org/typescript", "ts"),
        "js": ("https://cdn.simpleicons.org/javascript", "js"),
        "python": ("https://cdn.simpleicons.org/python", "python"),
        "go": ("https://cdn.simpleicons.org/go", "go"),
        "lua": ("https://cdn.simpleicons.org/lua", "lua"),
        "kotlin": ("https://cdn.simpleicons.org/kotlin", "kotlin"),
        "php": ("https://cdn.simpleicons.org/php", "php"),
        "cpp": ("https://cdn.simpleicons.org/cplusplus", "cpp"),
        "c": ("https://cdn.simpleicons.org/c", "c"),
        "julia": ("https://cdn.simpleicons.org/julia", "julia"),
        "ruby": ("https://cdn.simpleicons.org/ruby", "ruby"),
        "haskell": ("https://cdn.simpleicons.org/haskell", "haskell"),
        "zig": ("https://cdn.simpleicons.org/zig", "zig"),
        "java": ("https://cdn.simpleicons.org/openjdk", "java"),
        "swift": ("https://cdn.simpleicons.org/swift", "swift"),
        "flutter": ("https://cdn.simpleicons.org/flutter", "flutter"),
        "nextjs": ("https://cdn.simpleicons.org/nextdotjs", "nextjs"),
        "svelte": ("https://cdn.simpleicons.org/svelte", "svelte"),
        "laravel": ("https://cdn.simpleicons.org/laravel", "laravel"),
        "git": ("https://cdn.simpleicons.org/git", "git"),
        "github": ("https://cdn.simpleicons.org/githubactions", "github"),
        "docker": ("https://cdn.simpleicons.org/docker", "docker"),
        "ytdlp": ("https://cdn.simpleicons.org/youtube", "ytdlp"),
        "opencode": ("https://cdn.simpleicons.org/opencode", "opencode"),
        "anthropic": ("https://cdn.simpleicons.org/anthropic", "anthropic"),
        "claude": ("https://cdn.simpleicons.org/claude", "claude"),
        "cursor": ("https://cdn.simpleicons.org/cursor", "cursor"),
        "copilot": ("https://cdn.simpleicons.org/githubcopilot", "copilot"),
        "ollama": ("https://cdn.simpleicons.org/ollama", "ollama"),
        "huggingface": ("https://cdn.simpleicons.org/huggingface", "huggingface"),
        "bash": ("https://raw.githubusercontent.com/primer/octicons/main/icons/terminal-16.svg", "bash"),
        "powershell": ("https://raw.githubusercontent.com/primer/octicons/main/icons/terminal-16.svg", "powershell"),
        "vscode": ("https://raw.githubusercontent.com/primer/octicons/main/icons/code-16.svg", "vscode"),
    }
    ICONS = {}
    for key, (url, _) in icons.items():
        try:
            ICONS[key] = b64(url)
            print("icon", key, "ok", len(ICONS[key]))
        except Exception as e:
            print("icon", key, "MISSING", e)
    return ICONS


ICONS = icon_ref(None) if False else None


def image(name, size=40):
    return f'<image href="data:image/svg+xml;base64,{ICONS[name]}" width="{size}" height="{size}"/>'


def chip(x, y, name, icon, fill=PANEL_SOFT, stroke=BORDER, text=STRONG):
    return (
        f'<rect x="{x}" y="{y}" width="150" height="40" rx="20" fill="{fill}" stroke="{stroke}"/>'
        f'<g transform="translate({x + 12}, {y + 7})"><g transform="scale({26 / 24:.3f})">{image(icon, 24)}</g></g>'
        f'<text x="{x + 50}" y="{y + 27}" font-family="{FONT}" font-size="14" fill="{text}">{esc(name)}</text>'
    )


def stack():
    groups = [
        ("LANGUAGES", [
            ("dart", "Dart"), ("cs", "C#"), ("ts", "TypeScript"), ("js", "JavaScript"), ("python", "Python"),
            ("rust", "Rust"), ("go", "Go"), ("lua", "Lua"), ("kotlin", "Kotlin"), ("php", "PHP"),
            ("cpp", "C++"), ("c", "C"), ("julia", "Julia"), ("ruby", "Ruby"), ("haskell", "Haskell"),
            ("zig", "Zig"), ("java", "Java"), ("swift", "Swift"),
        ], GREEN),
        ("FRAMEWORKS", [("flutter", "Flutter"), ("nextjs", "Next.js"), ("svelte", "Svelte"), ("laravel", "Laravel")], BLUE),
        ("TOOLS", [("git", "Git"), ("github", "Actions"), ("docker", "Docker"), ("vscode", "VS Code"), ("powershell", "PowerShell"), ("bash", "Bash"), ("ytdlp", "yt-dlp")], ORANGE),
        ("AI", [("opencode", "OpenCode"), ("anthropic", "Anthropic"), ("claude", "Claude"), ("cursor", "Cursor"), ("copilot", "Copilot"), ("ollama", "Ollama"), ("huggingface", "Hugging Face")], PURPLE),
    ]
    defs = []
    for key, payload in ICONS.items():
        defs.append(f'<image id="icon-{key}" href="data:image/svg+xml;base64,{payload}" width="30" height="30"/>')
    body = [f'<defs>{"".join(defs)}</defs>']
    body.append(f'<rect width="1200" height="560" fill="{BG}"/>')
    body.append(f'<rect x="22" y="16" width="1156" height="528" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>')
    body.append(f'<text x="56" y="64" font-family="{FONT}" font-size="17" fill="{MUTED}" letter-spacing="5">STACK</text>')
    body.append(f'<line x1="56" y1="76" x2="1144" y2="76" stroke="{BORDER}"/>')
    cols = 6
    cell_w, cell_h = 176, 54
    x0 = 48
    y = 88
    for title, items, accent in groups:
        body.append(f'<rect x="40" y="{y}" width="92" height="26" rx="13" fill="{PANEL_SOFT}" stroke="{accent}"/>')
        body.append(f'<text x="86" y="{y + 17}" font-family="{FONT}" font-size="11" letter-spacing="1" fill="{accent}" text-anchor="middle">{title}</text>')
        for i, (icon, name) in enumerate(items):
            col = i % cols
            row = i // cols
            x = x0 + 110 + col * cell_w
            ry = y + row * cell_h
            body.append(f'<g transform="translate({x}, {ry})"><use href="#icon-{icon}" x="0" y="-15"/><text x="40" y="7" font-family="{FONT}" font-size="12.5" fill="{STRONG}">{esc(name)}</text></g>')
        row_count = (len(items) + cols - 1) // cols
        y += 30 + row_count * cell_h + 12
    height = y + 16
    return svg_doc(1200, height, "".join(body), f"nekonaru tech stack")


def ai_orbit():
    defs = []
    for key, payload in ICONS.items():
        defs.append(f'<image id="icon-{key}" href="data:image/svg+xml;base64,{payload}" width="40" height="40"/>')
    body = [f'<defs>{"".join(defs)}</defs>']
    body.append(f'<rect width="1200" height="430" fill="{BG}"/>')
    body.append(f'<rect x="22" y="16" width="1156" height="398" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>')
    cx, cy = 600, 215
    for r, op in ((56, 0.5), (112, 0.32), (172, 0.2)):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PURPLE}" stroke-width="1.5" stroke-opacity="{op}" stroke-dasharray="4 7"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="#1c2430" stroke="{PURPLE}" stroke-width="2.5"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{PURPLE}" opacity="0.12"><animate attributeName="opacity" values="0.06;0.2;0.06" dur="3.6s" repeatCount="indefinite"/></circle>')
    body.append(f'<text x="{cx}" y="{cy + 7}" font-family="{FONT}" font-size="25" font-weight="700" fill="{STRONG}" text-anchor="middle" letter-spacing="2">AI</text>')
    import math
    satellites = [
        (90, "opencode", "OpenCode"),
        (150, "anthropic", "Anthropic"),
        (210, "ollama", "Ollama"),
        (270, "huggingface", "Hugging Face"),
        (330, "copilot", "Copilot"),
        (30, "claude", "Claude"),
    ]
    import math as _m
    for angle, key, label in satellites:
        rad = _m.radians(angle)
        r = 150
        x = cx + r * _m.cos(rad)
        y = cy + r * _m.sin(rad)
        body.append(
            f'<g transform="translate({x:.0f}, {y:.0f})">'
            f'<circle r="26" fill="{PANEL_SOFT}" stroke="{PURPLE}" stroke-width="2"/>'
            f'<use href="#icon-{key}" x="-18" y="-18" width="36" height="36"/>'
            f'<text y="44" font-family="{FONT}" font-size="11" fill="{MUTED}" text-anchor="middle" letter-spacing="1">{esc(label)}</text>'
            f'</g>'
        )
    body.append(f'<text x="48" y="66" font-family="{FONT}" font-size="17" fill="{MUTED}" letter-spacing="5">AI TOOLBOX</text>')
    body.append(f'<text x="48" y="88" font-family="{FONT}" font-size="12" fill="{MUTED}">agents, automation, open models</text>')
    return svg_doc(1200, 430, "".join(body), "AI toolbox orbit")


def main():
    os.makedirs(HERE, exist_ok=True)
    global ICONS
    ICONS = icon_ref(None)
    assets = {
        "stack.svg": stack(),
        "ai-orbit.svg": ai_orbit(),
    }
    for name, content in assets.items():
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
