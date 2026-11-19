"""Generate the original SVG artwork used in the profile README.

Everything here is drawn from scratch. Run: python scripts/build_assets.py
Outputs into assets/. Standard library only.
"""
import os

HERE = os.path.join(os.path.dirname(__file__), "..", "assets")

BG = "#0d1117"
PANEL = "#161b22"
PANEL_SOFT = "#21262d"
BORDER = "#30363d"
GRID = "#21262d"
FG = "#e6edf3"
MUTED = "#8b949e"
STRONG = "#f0f6fc"
GREEN = "#39d353"
ORANGE = "#ff9e64"
BLUE = "#58a6ff"
YELLOW = "#d29922"
PURPLE = "#bc8cff"
RED = "#f85149"
FONT = "'JetBrains Mono', 'Consolas', monospace"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n{body}\n</svg>\n'
    )


def dots_grid(w, h, step=60):
    parts = []
    for x in range(step // 2, w, step):
        for y in range(step // 2, h, step):
            parts.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GRID}"/>')
    return "".join(parts)


def hero():
    cat = f"""
    <g stroke="{GREEN}" stroke-width="4" stroke-linejoin="round" fill="{PANEL}">
      <path d="M890 205 L872 112 L960 158 Z"/>
      <path d="M1030 158 L1118 112 L1100 205 Z"/>
      <rect x="880" y="160" width="230" height="180" rx="44"/>
      <path d="M880 320 Q880 400 770 400 L1130 400 Q1020 400 1020 320" fill="{PANEL}"/>
      <path d="M770 400 L770 430 M1130 400 L1130 430" stroke-width="4" stroke="{GREEN}"/>
    </g>
    <rect x="925" y="238" width="26" height="36" rx="9" fill="{GREEN}"/>
    <rect x="1040" y="238" width="26" height="36" rx="9" fill="{GREEN}"/>
    <path d="M982 300 L1008 300 L995 314 Z" fill="{ORANGE}"/>
    <path d="M995 318 L995 330" stroke="{ORANGE}" stroke-width="3"/>
    <path d="M940 300 L862 285 M940 320 L862 322" stroke="{MUTED}" stroke-width="3" stroke-linecap="round"/>
    <path d="M1050 300 L1128 285 M1050 320 L1128 322" stroke="{MUTED}" stroke-width="3" stroke-linecap="round"/>
    """
    body = f"""
<rect width="1200" height="440" fill="{BG}"/>
{dots_grid(1200, 440, 60)}
<rect x="30" y="30" width="1140" height="380" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
<path d="M30 90 L32 48 L48 32 L1170 32 L1186 48 L1188 90 L1188 90 L1198 90 L1198 350 L1186 366 L1182 400 L48 400 L30 366 Z" fill="none" stroke="{BORDER}" stroke-width="1.6" opacity="0.6"/>
<text x="70" y="120" font-family="{FONT}" font-size="20" fill="{GREEN}" letter-spacing="6">G I T H U B</text>
<text x="68" y="215" font-family="'Segoe UI', 'Arial', sans-serif" font-size="62" font-weight="800" fill="{STRONG}">Nicolas Dwi Dharma</text>
<text x="70" y="272" font-family="{FONT}" font-size="22" fill="{MTuchel if False else MUTED}">@nekonaru</text>
<g font-family="{FONT}" font-size="16">
  <rect x="68" y="318" width="230" height="34" rx="17" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="183" y="341" fill="{FG}" text-anchor="middle">offline-first tools</text>
  <rect x="316" y="318" width="190" height="34" rx="17" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="411" y="341" fill="{FG}" text-anchor="middle">web and game</text>
  <rect x="524" y="318" width="216" height="34" rx="17" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="632" y="341" fill="{FG}" text-anchor="middle">open source</text>
</g>
{cat}
"""
    body = body.replace("MTuchel if False else MUTED", "MUTED")
    return svg(1200, 440, body)


def section(label, accent=GREEN):
    line_x = 400
    return svg(1200, 104, f"""
<rect width="1200" height="104" fill="{BG}"/>
<line x1="40" y1="52" x2="360" y2="52" stroke="{BORDER}" stroke-width="2"/>
<line x1="840" y1="52" x2="1160" y2="52" stroke="{BORDER}" stroke-width="2"/>
<circle cx="370" cy="52" r="4" fill="{accent}"/>
<circle cx="400" cy="52" r="4" fill="{BORDER}"/>
<circle cx="830" cy="52" r="4" fill="{BORDER}"/>
<circle cx="860" cy="52" r="4" fill="{accent}"/>
<rect x="330" y="20" width="540" height="64" rx="14" fill="{PANEL}" stroke="{accent}" stroke-width="2"/>
<text x="600" y="62" font-family="{FONT}" font-size="24" font-weight="700" letter-spacing="8" fill="{STRONG}" text-anchor="middle">{esc(label)}</text>
""")


def neofetch():
    lines = [
        ("handle", "@nekonaru"),
        ("name", "Nicolas Dwi Dharma"),
        ("bio", "Explorer"),
        ("joined", "Sep 2025"),
        ("repos", "32 public"),
        ("stars", "2"),
        ("top lang", "C# by bytes"),
        ("focus", "media and web tools"),
    ]
    cat = [
        "  /\\_/\\  ",
        " ( o.o ) ",
        "  > ^ <  ",
        " /|   |\\ ",
        "(_|   |_) ",
    ]
    rows = []
    y = 118
    for key, value in lines:
        rows.append(f'<text x="480" y="{y}" font-family="{FONT}" font-size="20" fill="{BLUE}">{esc(key):<9}</text>')
        rows.append(f'<text x="640" y="{y}" font-family="{FONT}" font-size="20" fill="{FG}">{esc(value)}</text>')
        y += 34
    cat_rows = []
    cy = 130
    for line in cat:
        cat_rows.append(f'<text x="150" y="{cy}" font-family="{FONT}" font-size="26" fill="{GREEN}" xml:space="preserve">{esc(line)}</text>')
        cy += 32
    body = f"""
<rect width="1200" height="430" fill="{BG}"/>
<rect x="20" y="20" width="1160" height="390" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
<circle cx="60" cy="62" r="8" fill="{RED}"/>
<circle cx="88" cy="62" r="8" fill="{YELLOW}"/>
<circle cx="116" cy="62" r="8" fill="{GREEN}"/>
<text x="600" y="70" font-family="{FONT}" font-size="17" fill="{MUTED}" text-anchor="middle">guest@nekonaru — neofetch</text>
<line x1="20" y1="84" x2="1180" y2="84" stroke="{BORDER}" stroke-width="2"/>
{''.join(cat_rows)}
<text x="150" y="330" font-family="{FONT}" font-size="18" fill="{MUTED}">just shipping</text>
{''.join(rows)}
"""
    return svg(1200, 430, body)


def timeline():
    events = [
        ("Sep 2025", "Joined GitHub", "started building in the open"),
        ("Jun 2026", "rynnbot", "first repo: a self-hosted WhatsApp bot"),
        ("Aug 2026", "wattpdl, swara, lumenfetch, boredom", "media and everyday web tools"),
        ("Oct 2026", "lekas and gametech26", "task tracker and a 3D narrative horror game"),
        ("Nov 2026", "morfa, getta, talos", "file converter and web downloaders"),
        ("Nov 2026", "Julia, Haskell, Zig, Ruby", "pushing into new languages"),
    ]
    rows = []
    y = 92
    line_y = [y + i * 52 for i in range(len(events))]
    parts = [f'<rect width="1200" height="430" fill="{BG}"/>']
    parts.append(f'<line x1="240" y1="70" x2="240" y2="{y + 5 * 52 + 20}" stroke="{BORDER}" stroke-width="3"/>')
    for i, (date, title, desc) in enumerate(events):
        yy = y + i * 52
        color = GREEN if i == len(events) - 1 else (ORANGE if i == 0 else BLUE)
        parts.append(f'<circle cx="240" cy="{yy}" r="8" fill="{BG}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="200" y="{yy + 5}" font-family="{FONT}" font-size="13" fill="{MUTED}" text-anchor="end">{esc(date)}</text>')
        parts.append(f'<text x="285" y="{yy - 2}" font-family="' + "'Segoe UI', 'Arial', sans-serif" + f'" font-size="19" font-weight="700" fill="{STRONG}">{esc(title)}</text>')
        parts.append(f'<text x="285" y="{yy + 17}" font-family="' + "'Segoe UI', 'Arial', sans-serif" + f'" font-size="13" fill="{MUTED}">{esc(desc)}</text>')
    return svg(1200, 430, "".join(parts))


def footer_art():
    return svg(1200, 150, f"""
<rect width="1200" height="150" fill="{BG}"/>
<path d="M0 150 L1200 150" stroke="{BORDER}" stroke-width="2"/>
<text x="600" y="72" font-family="'Segoe UI', 'Arial', sans-serif" font-size="34" font-weight="800" fill="{STRONG}" text-anchor="middle">Thanks for stopping by</text>
<text x="600" y="112" font-family="{FONT}" font-size="16" fill="{MUTED}" text-anchor="middle">built with code and coffee by nekonaru</text>
""")


def main():
    os.makedirs(HERE, exist_ok=True)
    assets = {
        "hero.svg": hero(),
        "neofetch.svg": neofetch(),
        "timeline.svg": timeline(),
        "footer.svg": footer_art(),
        "section-projects.svg": section("PROJECTS", GREEN),
        "section-stack.svg": section("TECH STACK", BLUE),
        "section-stats.svg": section("GITHUB STATS", ORANGE),
        "section-journey.svg": section("JOURNEY", PURPLE),
        "section-connect.svg": section("CONNECT", YELLOW),
    }
    for name, content in assets.items():
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
