"""Download brand icons and generate the illustrated stack, marquee and AI orbit panels.

Standard library only. Run: python scripts/build_icon_panels.py
Outputs into assets/. Icons are inlined so the SVGs stay self-contained.
"""
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


def fetch_simpleicon(slug):
    url = f"https://cdn.simpleicons.org/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "nekonaru-profile-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def fetch_octicon(name):
    url = f"https://raw.githubusercontent.com/primer/octicons/main/icons/{name}-16.svg"
    req = urllib.request.Request(url, headers={"User-Agent": "nekonaru-profile-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def icon_body(svg_text):
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg_text, re.S)
    return m.group(1) if m else svg_text


def recolor(icon_svg, color):
    svg = icon_svg
    if "fill=" in svg:
        svg = re.sub(r'fill="[^"]*"', f'fill="{color}"', svg, count=1)
        return svg
    return re.sub(r"<path", f'<g fill="{color}"><path', svg) + "</g>"


ICONS = {}
SIMPLE = {
    "dart": ("dart", "#00B4AB"),
    "rust": ("rust", "#DEA584"),
    "cs": ("dotnet", "#512BD4"),
    "ts": ("typescript", "#3178C6"),
    "js": ("javascript", "#F7DF1E"),
    "python": ("python", "#3572A5"),
    "go": ("go", "#00ADD8"),
    "lua": ("lua", "#7F7FFF"),
    "kotlin": ("kotlin", "#7F52FF"),
    "php": ("php", "#4F5D95"),
    "cpp": ("cplusplus", "#F34B7D"),
    "c": ("c", "#A8B9CC"),
    "julia": ("julia", "#A270BA"),
    "ruby": ("ruby", "#CC342D"),
    "haskell": ("haskell", "#5E5086"),
    "zig": ("zig", "#F7A41D"),
    "java": ("openjdk", "#B07219"),
    "swift": ("swift", "#F05138"),
    "flutter": ("flutter", "#54C5F8"),
    "nextjs": ("nextdotjs", "#EDEDED"),
    "svelte": ("svelte", "#FF3E00"),
    "laravel": ("laravel", "#FF2D20"),
    "git": ("git", "#F05033"),
    "github": ("githubactions", "#58A6FF"),
    "docker": ("docker", "#2496ED"),
    "ytdlp": ("youtube", "#FF0000"),
    "opencode": ("opencode", "#39D353"),
    "anthropic": ("anthropic", "#D4A373"),
    "claude": ("claude", "#D97757"),
    "cursor": ("cursor", "#EDEDED"),
    "copilot": ("githubcopilot", "#6E7681"),
    "ollama": ("ollama", "#EDEDED"),
    "huggingface": ("huggingface", "#FFD21E"),
}
OCTICONS = {
    "bash": ("terminal", "#4EAA25"),
    "powershell": ("terminal", "#5391FE"),
    "vscode": ("code", "#007ACC"),
}


def load_icons():
    for key, (slug, color) in SIMPLE.items():
        try:
            svg = fetch_simpleicon(slug)
            ICONS[key] = recolor(svg, color)
            print("icon", key, "ok")
        except Exception as e:
            print("icon", key, "MISSING", e)
    for key, (name, color) in OCTICONS.items():
        try:
            svg = fetch_octicon(name)
            body = icon_body(recolor(svg, color))
            ICONS[key] = f'<g fill="{color}">{body}</g>'
            print("icon", key, "ok")
        except Exception as e:
            print("icon", key, "MISSING", e)


def icon_fragment(key, x, y, size):
    if key not in ICONS:
        return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="none"/>'
    frag = ICONS[key]
    scale = size / 24.0
    return f'<g transform="translate({x}, {y}) scale({scale:.3f})" fill="inherit">{frag}</g>'


def chip(x, y, key, name, width, accent):
    parts = []
    w = width
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="{PANEL_SOFT}" stroke="{BORDER}" stroke-width="1.5"/>')
    parts.append(icon_fragment(key, x + 8, y + 4, 26))
    parts.append(f'<text x="{x + 42}" y="{y + 22}" font-family="{FONT}" font-size="13.5" fill="{STRONG}">{esc(name)}</text>')
    return "".join(parts), w + 10


def stack():
    groups = [
        ("LANGUAGES", [
            ("dart", "Dart", 90), ("cs", "C#", 80), ("rust", "Rust", 84), ("ts", "TypeScript", 148),
            ("js", "JavaScript", 152), ("python", "Python", 108), ("go", "Go", 64), ("lua", "Lua", 68),
            ("kotlin", "Kotlin", 94), ("php", "PHP", 76), ("cpp", "C++", 74), ("c", "C", 52),
            ("julia", "Julia", 78), ("ruby", "Ruby", 80), ("haskell", "Haskell", 108), ("zig", "Zig", 66),
            ("java", "Java", 72), ("swift", "Swift", 82),
        ], GREEN),
        ("FRAMEWORKS", [
            ("flutter", "Flutter", 112), ("nextjs", "Next.js", 100), ("svelte", "Svelte", 82), ("laravel", "Laravel", 94),
        ], BLUE),
        ("TOOLS", [
            ("git", "Git", 62), ("github", "Actions", 116), ("docker", "Docker", 96), ("vscode", "VS Code", 96),
            ("powershell", "PowerShell", 136), ("bash", "Bash", 78), ("ytdlp", "yt-dlp", 92),
        ], ORANGE),
        ("AI", [
            ("opencode", "OpenCode", 112), ("anthropic", "Anthropic", 122), ("claude", "Claude", 92),
            ("cursor", "Cursor", 84), ("copilot", "Copilot", 104), ("ollama", "Ollama", 92), ("huggingface", "Hugging Face", 154),
        ], PURPLE),
    ]
    body = [f'<rect width="1200" height="505" fill="{BG}"/>']
    body.append(f'<rect x="22" y="16" width="1156" height="472" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>')
    body.append(f'<text x="56" y="64" font-family="{FONT}" font-size="17" fill="{MUTED}" letter-spacing="5">STACK</text>')
    body.append(f'<line x1="56" y1="76" x2="1144" y2="76" stroke="{BORDER}"/>')
    y = 100
    for title, items, accent in groups:
        body.append(f'<rect x="48" y="{y}" width="106" height="32" rx="16" fill="{PANEL_SOFT}" stroke="{accent}"/>')
        body.append(f'<text x="101" y="{y + 21}" font-family="{FONT}" font-size="12" letter-spacing="1.5" fill="{accent}" text-anchor="middle">{title}</text>')
        x = 172
        row_y = y
        for key, name, w in items:
            frag, dx = chip(x, row_y, key, name, w, accent)
            body.append(frag)
            x += dx
            if x > 1130:
                x = 172
                row_y += 44
        y = max(y + 50, row_y + 54) + 14
    return svg_doc(1200, 505, "".join(body), f"nekonaru stack: languages, frameworks, tools, AI")


def svg_doc(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">\n'
        f'<title>{esc(title)}</title>\n{body}\n</svg>\n'
    )


def marquee():
    icons = ["dart", "cs", "rust", "ts", "js", "python", "go", "lua", "kotlin", "php",
             "flutter", "nextjs", "svelte", "laravel", "git", "github", "docker", "opencode"]
    size = 34
    gap = 46
    items = []
    width = 0
    for key in icons:
        frag = icon_fragment(key, 0, 0, size)
        items.append((frag, gap))
        width += gap
    loop = width * 2
    body = [f'<defs><clipPath id="mq"><rect x="0" y="0" width="1200" height="76"/></clipPath></defs>']
    body.append(f'<rect width="1200" height="76" fill="{PANEL}"/>')
    body.append(f'<rect x="0" y="0" width="1200" height="1" fill="{BORDER}" opacity="0.7"/>')
    body.append(f'<rect x="0" y="75" width="1200" height="1" fill="{BORDER}" opacity="0.7"/>')
    body.append(f'<g clip-path="url(#mq)"><g><animateTransform attributeName="transform" type="translate" values="0 0;-{loop} 0" dur="42s" repeatCount="indefinite"/>')
    x = 0
    for _ in range(2):
        for frag, gap in items:
            body.append(f'<g transform="translate({x}, 21) scale(1.0)">{frag}</g>')
            x += gap
    body.append('</g></g>')
    return svg_doc(1200, 76, "".join(body), "Technology marquee")


def ai_orbit():
    body = [f'<rect width="1200" height="430" fill="{BG}"/>']
    body.append(f'<rect x="22" y="16" width="1156" height="398" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>')
    cx, cy = 600, 215
    for r, op in ((70, 0.5), (125, 0.35), (180, 0.22)):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PURPLE}" stroke-width="1.5" stroke-opacity="{op}" stroke-dasharray="4 7"><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="40s" repeatCount="indefinite"/></circle>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="#1c2430" stroke="{PURPLE}" stroke-width="2.5"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{PURPLE}" opacity="0.12"><animate attributeName="opacity" values="0.06;0.2;0.06" dur="3.6s" repeatCount="indefinite"/></circle>')
    body.append(f'<text x="{cx}" y="{cy + 8}" font-family="{FONT}" font-size="26" font-weight="700" fill="{STRONG}" text-anchor="middle" letter-spacing="2">AI</text>')
    satellites = [
        (0, "opencode", "OpenCode"),
        (60, "anthropic", "Anthropic"),
        (120, "ollama", "Ollama"),
        (180, "huggingface", "Hugging Face"),
        (240, "copilot", "Copilot"),
        (300, "claude", "Claude"),
    ]
    import math
    import math as _m
    for angle, key, label in satellites:
        rad = _m.radians(angle)
        r = 150
        x = cx + r * _m.cos(rad)
        y = cy + r * _m.sin(rad)
        frag = icon_fragment(key, -18, -18, 36)
        body.append(
            f'<g transform="translate({x:.0f}, {y:.0f})">'
            f'<circle r="27" fill="{PANEL_SOFT}" stroke="{PURPLE}" stroke-width="2"/>'
            f'{frag}'
            f'<text y="48" font-family="{FONT}" font-size="11" fill="{MUTED}" text-anchor="middle" letter-spacing="1">{esc(label)}</text>'
            f"</g>"
        )
    body.append(f'<text x="56" y="64" font-family="{FONT}" font-size="17" fill="{MUTED}" letter-spacing="5">AI TOOLBOX</text>')
    body.append(f'<text x="56" y="88" font-family="{FONT}" font-size="12" fill="{MUTED}">agents, automation, open models</text>')
    return svg_doc(1200, 430, "".join(body), "AI toolbox orbit")


def main():
    os.makedirs(HERE, exist_ok=True)
    load_icons()
    assets = {
        "stack.svg": stack(),
        "marquee.svg": marquee(),
        "ai-orbit.svg": ai_orbit(),
    }
    for name, content in assets.items():
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
