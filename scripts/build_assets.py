"""Generate the original SVG artwork used in the profile README.

All artwork is drawn from scratch by this script. Run: python scripts/build_assets.py
Outputs into assets/. Standard library only.
"""
import os
import random

HERE = os.path.join(os.path.dirname(__file__), "..", "assets")
random.seed(42)

BG = "#0d1117"
BG2 = "#141b26"
PANEL = "#161b22"
PANEL_SOFT = "#21262d"
BORDER = "#30363d"
GRID = "#1c2430"
FG = "#e6edf3"
MUTED = "#8b949e"
STRONG = "#f0f6fc"
GREEN = "#39d353"
GREEN_DIM = "#26a641"
ORANGE = "#ff9e64"
BLUE = "#58a6ff"
YELLOW = "#d29922"
PURPLE = "#bc8cff"
RED = "#f85149"
FONT = "'JetBrains Mono', 'Consolas', monospace"
SANS = "'Segoe UI', 'Arial', sans-serif"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n{body}\n</svg>\n'
    )


def stars(n, width, height, ymax):
    parts = []
    for _ in range(n):
        x = random.uniform(20, width - 20)
        y = random.uniform(10, ymax)
        r = random.uniform(0.8, 2.2)
        delay = random.uniform(0, 4)
        dur = random.uniform(1.6, 4.5)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{STRONG}">'
            f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{dur:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return "".join(parts)


def skyline(width, base_y, color, seed):
    rng = random.Random(seed)
    parts = []
    x = -20
    while x < width + 40:
        w = rng.choice([60, 70, 90, 110, 130])
        h = rng.choice([60, 90, 120, 150, 190, 230])
        parts.append(f'<rect x="{x}" y="{base_y - h}" width="{w}" height="{h}" fill="{color}"/>')
        for wy in range(base_y - h + 14, base_y - 12, 22):
            for wx in range(x + 10, x + w - 10, 16):
                if rng.random() < 0.22:
                    fill = YELLOW if rng.random() < 0.8 else "#ffe9a8"
                    parts.append(f'<rect x="{wx}" y="{wy}" width="6" height="8" fill="{fill}" opacity="0.85"/>')
        x += w + rng.choice([8, 14, 22])
    return "".join(parts)


def moon_and_stars():
    return f"""
<circle cx="1045" cy="105" r="130" fill="#f0f6fc" opacity="0.07">
  <animate attributeName="opacity" values="0.05;0.11;0.05" dur="6s" repeatCount="indefinite"/>
</circle>
<circle cx="1045" cy="105" r="74" fill="#1c2430" stroke="{STRONG}" stroke-opacity="0.9" stroke-width="2"/>
<circle cx="1045" cy="105" r="60" fill="#161d28"/>
<circle cx="1024" cy="92" r="7" fill="#232c3a"/>
<circle cx="1068" cy="118" r="5" fill="#232c3a"/>
<circle cx="1052" cy="80" r="4" fill="#232c3a"/>
"""


def shooting_star():
    return f"""
<g opacity="0">
  <path d="M0 0 L90 -26" stroke="{STRONG}" stroke-width="2.5" stroke-linecap="round"/>
  <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.62;0.66;0.74;1" dur="9s" repeatCount="indefinite"/>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 0;760 130;820 152;820 152" keyTimes="0;0.62;0.74;0.8;1" dur="9s" repeatCount="indefinite"/>
</g>
"""


def cat_glow():
    return f"""
<g transform="translate(1005, 160)">
  <g stroke="{GREEN}" stroke-width="4" stroke-linejoin="round" fill="#05070c" stroke-linecap="round">
    <animate attributeName="stroke-opacity" values="0.7;1;0.7" dur="3.2s" repeatCount="indefinite"/>
    <path d="M-6 70 L12 0 L34 56 Z"/>
    <path d="M76 56 L98 0 L116 70 Z"/>
    <rect x="0" y="52" width="110" height="86" rx="22"/>
    <path d="M10 132 L10 232 L100 232 L100 132 Z"/>
    <path d="M100 160 Q150 190 142 232 L100 232"/>
  </g>
  <circle cx="32" cy="92" r="5.5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.3;1" dur="3.2s" repeatCount="indefinite"/></circle>
  <circle cx="78" cy="92" r="5.5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.3;1" dur="3.2s" begin="-1.6s" repeatCount="indefinite"/></circle>
  <path d="M55 106 L55 114" stroke="{GREEN}" stroke-width="3"/>
</g>
"""


def hero():
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0d1117"/>
    <stop offset="0.55" stop-color="#111a26"/>
    <stop offset="1" stop-color="#1a2433"/>
  </linearGradient>
  <linearGradient id="glowline" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{GREEN}"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="frame"><rect x="26" y="26" width="1148" height="388" rx="18"/></clipPath>
</defs>
<rect width="1200" height="440" fill="{BG}"/>
<g clip-path="url(#frame)">
  <rect x="26" y="26" width="1148" height="388" fill="url(#sky)"/>
  {stars(70, 1200, 1200, 200)}
  {moon_and_stars()}
  {shooting_star()}
  {skyline(1200, 350, "#141b26", 7)}
  {skyline(1200, 395, "#0d121b", 21)}
  {cat_glow()}
  <rect x="26" y="395" width="1148" height="20" fill="#0a0e14"/>
</g>
<rect x="26" y="26" width="1148" height="388" rx="18" fill="none" stroke="{BORDER}" stroke-width="2"/>
<rect x="26" y="298" width="520" height="70" fill="{BG}" opacity="0.55"/>
<text x="60" y="92" font-family="{FONT}" font-size="17" fill="{GREEN}" letter-spacing="6">G I T H U B</text>
<text x="58" y="150" font-family="{SANS}" font-size="56" font-weight="800" fill="{STRONG}">Nicolas Dwi Dharma</text>
<text x="58" y="192" font-family="{FONT}" font-size="19" fill="{MUTED}">@nekonaru // explorer</text>
<g font-family="{FONT}" font-size="14">
  <rect x="56" y="222" width="172" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="142" y="242" fill="{FG}" text-anchor="middle">offline-first tools</text>
  <rect x="238" y="222" width="140" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="308" y="242" fill="{FG}" text-anchor="middle">web and game</text>
  <rect x="388" y="222" width="158" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="467" y="242" fill="{FG}" text-anchor="middle">open source</text>
</g>
<rect x="56" y="272" width="470" height="3" fill="url(#glowline)"/>
<text x="56" y="308" font-family="{FONT}" font-size="13" fill="{MUTED}">build in the open, ship what works</text>
<rect x="26" y="26" width="1148" height="3" fill="url(#glowline)" opacity="0.8"/>
"""
    return svg(1200, 440, body)


def ticker():
    items = ["SWARA", "TALOS", "MORFA", "GETTA", "NIUSIC", "LEKAS", "WEBSITEKWU", "GAMETECH26", "STASHIFY", "RENTRA"]
    half = "  //  ".join(items) + "  //  "
    span = 10 * 46
    body = f"""
<clipPath id="clip"><rect x="0" y="0" width="1200" height="46"/></clipPath>
<rect width="1200" height="46" fill="{PANEL}"/>
<rect x="0" y="0" width="1200" height="2" fill="{BORDER}" opacity="0.4"/>
<rect x="0" y="44" width="1200" height="2" fill="{BORDER}" opacity="0.4"/>
<g clip-path="url(#clip)" font-family="{FONT}" font-size="15" fill="{MUTED}" letter-spacing="2">
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0;-{span * 2} 0" dur="60s" repeatCount="indefinite"/>
    <text x="0" y="29" xml:space="preserve">{esc(half * 2)}</text>
  </g>
</g>
"""
    return svg(1200, 46, body)


def section(label, accent=GREEN):
    return svg(1200, 104, f"""
<rect width="1200" height="104" fill="{BG}"/>
<line x1="40" y1="52" x2="340" y2="52" stroke="{BORDER}" stroke-width="2"/>
<line x1="860" y1="52" x2="1160" y2="52" stroke="{BORDER}" stroke-width="2"/>
<circle cx="356" cy="52" r="4" fill="{accent}"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="844" cy="52" r="4" fill="{accent}"><animate attributeName="r" values="4;7;4" dur="2s" begin="-1s" repeatCount="indefinite"/></circle>
<rect x="330" y="18" width="540" height="68" rx="16" fill="{PANEL}" stroke="{accent}" stroke-width="2"/>
<text x="600" y="62" font-family="{FONT}" font-size="23" font-weight="700" letter-spacing="8" fill="{STRONG}" text-anchor="middle">{esc(label)}</text>
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
    y = 124
    for key, value in lines:
        rows.append(f'<text x="470" y="{y}" font-family="{FONT}" font-size="20" fill="{BLUE}">{esc(key):<9}</text>')
        rows.append(f'<text x="632" y="{y}" font-family="{FONT}" font-size="20" fill="{FG}">{esc(value)}</text>')
        y += 33
    cat_rows = []
    cy = 132
    for line in cat:
        cat_rows.append(f'<text x="120" y="{cy}" font-family="{FONT}" font-size="26" fill="{GREEN}" xml:space="preserve">{esc(line)}</text>')
        cy += 31
    body = f"""
<rect width="1200" height="430" fill="{BG}"/>
<rect x="20" y="18" width="1160" height="394" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
<circle cx="58" cy="62" r="8" fill="{RED}"/>
<circle cx="86" cy="62" r="8" fill="{YELLOW}"/>
<circle cx="114" cy="62" r="8" fill="{GREEN}"/>
<text x="600" y="70" font-family="{FONT}" font-size="16" fill="{MUTED}" text-anchor="middle">guest@nekonaru — neofetch</text>
<line x1="20" y1="84" x2="1180" y2="84" stroke="{BORDER}" stroke-width="2"/>
{''.join(cat_rows)}
{''.join(rows)}
<rect x="632" y="384" width="13" height="24" fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
"""
    return svg(1200, 430, body)


def timeline():
    events = [
        ("Sep 2025", "Joined GitHub", "started building in the open", ORANGE),
        ("Jun 2026", "rynnbot", "first repo: a self-hosted WhatsApp bot", BLUE),
        ("Aug 2026", "wattpdl, swara, lumenfetch, boredom", "media and everyday web tools", BLUE),
        ("Oct 2026", "lekas and gametech26", "task tracker and a 3D narrative horror game", BLUE),
        ("Nov 2026", "morfa, getta, talos", "file converter and web downloaders", BLUE),
        ("Nov 2026", "Julia, Haskell, Zig, Ruby", "pushing into new languages", GREEN),
    ]
    y0 = 74
    step = 54
    parts = [f'<rect width="1200" height="430" fill="{BG}"/>']
    parts.append(f'<line x1="238" y1="{y0}" x2="238" y2="{y0 + step * (len(events) - 1) + 6}" stroke="{BORDER}" stroke-width="3"/>')
    for i, (date, title, desc, dot) in enumerate(events):
        yy = y0 + i * step
        parts.append(f'<circle cx="238" cy="{yy}" r="9" fill="{BG}" stroke="{dot}" stroke-width="3"><animate attributeName="r" values="9;12;9" dur="2.4s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<text x="196" y="{yy + 5}" font-family="{FONT}" font-size="13" fill="{MUTED}" text-anchor="end">{esc(date)}</text>')
        parts.append(f'<text x="282" y="{yy - 3}" font-family="{SANS}" font-size="19" font-weight="700" fill="{STRONG}">{esc(title)}</text>')
        parts.append(f'<text x="282" y="{yy + 16}" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(desc)}</text>')
    return svg(1200, 430, "".join(parts))


def footer_art():
    return svg(1200, 150, f"""
<rect width="1200" height="150" fill="{BG}"/>
<rect x="440" y="40" width="320" height="3" fill="{GREEN}" opacity="0.8"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" repeatCount="indefinite"/></rect>
<text x="600" y="86" font-family="{SANS}" font-size="33" font-weight="800" fill="{STRONG}" text-anchor="middle">Thanks for stopping by</text>
<text x="600" y="124" font-family="{FONT}" font-size="15" fill="{MUTED}" text-anchor="middle">built with code and coffee by nekonaru</text>
""")


def main():
    os.makedirs(HERE, exist_ok=True)
    assets = {
        "hero.svg": hero(),
        "ticker.svg": ticker(),
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
