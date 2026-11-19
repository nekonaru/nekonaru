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


def gpt_badge():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40">'
        '<rect width="24" height="24" rx="5" fill="#19C37D"/>'
        '<path d="M8.6 7.2v9.6h2V9.4l2 5.6h1.8l2-5.6v7.4h2V7.2h-2.4l-2.4 6.4L9.7 7.2z" fill="#0d1117"/>'
        '</svg>'
    )
    return base64.b64encode(svg.encode()).decode("ascii")


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
        "claude": ("https://cdn.simpleicons.org/claude", "claude"),
        "gemini": ("https://cdn.simpleicons.org/googlegemini", "gemini"),
        "hermes": ("https://cdn.simpleicons.org/hermes", "hermes"),
        "deepseek": ("https://cdn.simpleicons.org/deepseek", "deepseek"),
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
        ("AI", [("opencode", "OpenCode"), ("claude", "Claude"), ("gpt", "GPT"), ("gemini", "Gemini"), ("hermes", "Hermes"), ("deepseek", "DeepSeek")], PURPLE),
    ]
    used = {icon for _, items, _ in groups for icon, _ in items}
    defs = []
    for key, payload in ICONS.items():
        if key in used:
            defs.append(f'<image id="icon-{key}" href="data:image/svg+xml;base64,{payload}" width="24" height="24"/>')

    COLS = 6
    CELL_W, CELL_H, GAP = 176, 44, 14
    X0 = 168
    y = 84
    body = [f'<defs>{"".join(defs)}</defs>']
    body.append(f'<rect width="1200" height="640" fill="{BG}"/>')
    body.append(f'<rect x="22" y="16" width="1156" height="608" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>')
    body.append(f'<text x="56" y="60" font-family="{FONT}" font-size="17" fill="{MUTED}" letter-spacing="5">STACK</text>')
    body.append(f'<line x1="56" y1="72" x2="1144" y2="72" stroke="{BORDER}"/>')
    for title, items, accent in groups:
        nrows = (len(items) + COLS - 1) // COLS
        row_h = nrows * CELL_H + (nrows - 1) * GAP
        cy = y + row_h // 2
        body.append(f'<rect x="40" y="{cy - 16}" width="100" height="32" rx="16" fill="{PANEL_SOFT}" stroke="{accent}"/>')
        body.append(f'<text x="90" y="{cy + 5}" font-family="{FONT}" font-size="11" letter-spacing="1" fill="{accent}" text-anchor="middle">{title}</text>')
        for i, (icon, name) in enumerate(items):
            col = i % COLS
            row = i // COLS
            x = X0 + col * CELL_W
            ry = y + row * (CELL_H + GAP)
            body.append(
                f'<g transform="translate({x}, {ry})">'
                f'<rect width="{CELL_W - 12}" height="{CELL_H}" rx="12" fill="{PANEL_SOFT}" stroke="{BORDER}"/>'
                f'<use href="#icon-{icon}" x="10" y="10" width="24" height="24"/>'
                f'<text x="44" y="29" font-family="{FONT}" font-size="13" fill="{STRONG}">{esc(name)}</text>'
                f'</g>'
            )
        y += row_h + 18
    return svg_doc(1200, y + 4, "".join(body), "nekonaru tech stack")


def ai_orbit():
    defs = []
    for key, payload in ICONS.items():
        defs.append(f'<image id="icon-{key}" href="data:image/svg+xml;base64,{payload}" width="40" height="40"/>')
    gpt_icon = gpt_badge()
    defs.append(f'<image id="icon-gpt" href="data:image/svg+xml;base64,{gpt_icon}" width="40" height="40"/>')
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
        (0, "opencode", "OpenCode"),
        (60, "claude", "Claude"),
        (120, "gpt", "GPT"),
        (180, "gemini", "Gemini"),
        (240, "hermes", "Hermes"),
        (300, "deepseek", "DeepSeek"),
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
    ICONS["gpt"] = gpt_badge()
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
