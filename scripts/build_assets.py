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
    rng = random.Random(7)
    rain = []
    for _ in range(36):
        x = rng.uniform(30, 1170)
        delay = rng.uniform(0, 3.5)
        dur = rng.uniform(1.5, 2.7)
        ln = rng.uniform(30, 62)
        rain.append(
            f'<line x1="{x:.0f}" y1="0" x2="{x + 9:.0f}" y2="{ln:.0f}" stroke="{STRONG}" stroke-width="1.6" opacity="0" stroke-linecap="round">'
            f'<animate attributeName="opacity" values="0;0.5;0" dur="{dur:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y1" values="-80;470" dur="{dur:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{-80 + ln:.0f};470" dur="{dur:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/>'
            f"</line>"
        )
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0b1018"><animate attributeName="stop-color" values="#0b1018;#0e1620;#0b1018" dur="11s" repeatCount="indefinite"/></stop>
    <stop offset="0.55" stop-color="#101a28"/>
    <stop offset="1" stop-color="#1b2637"/>
  </linearGradient>
  <radialGradient id="moonGlow" cx="0.84" cy="0.22" r="0.3">
    <stop offset="0" stop-color="#f0f6fc" stop-opacity="0.35"><animate attributeName="stop-opacity" values="0.25;0.42;0.25" dur="5s" repeatCount="indefinite"/></stop>
    <stop offset="0.55" stop-color="#f0f6fc" stop-opacity="0.06"/>
    <stop offset="1" stop-color="#f0f6fc" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="glowline" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{GREEN}"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="neonGround" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0.05"/>
    <stop offset="0.45" stop-color="{GREEN}" stop-opacity="0.9"/>
    <stop offset="0.55" stop-color="{GREEN}" stop-opacity="0.9"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0.05"/>
  </linearGradient>
  <clipPath id="frame"><rect x="26" y="26" width="1148" height="388" rx="18"/></clipPath>
</defs>
<rect width="1200" height="440" fill="{BG}"/>
<g clip-path="url(#frame)">
  <rect x="26" y="26" width="1148" height="388" fill="url(#sky)"/>
  {stars(70, 1200, 1200, 200)}
  <rect x="26" y="26" width="1148" height="388" fill="url(#moonGlow)"/>
  <circle cx="1008" cy="96" r="52" fill="#e8eef7"><animate attributeName="r" values="52;53.5;52" dur="5s" repeatCount="indefinite"/></circle>
  <circle cx="988" cy="82" r="8" fill="#c9d3e2" opacity="0.55"/>
  <circle cx="1032" cy="110" r="5" fill="#c9d3e2" opacity="0.5"/>
  <circle cx="1014" cy="72" r="4" fill="#c9d3e2" opacity="0.45"/>
  <g stroke="{STRONG}" stroke-width="2" stroke-linecap="round" fill="none">
    <path d="M0 0 L74 -22"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.55;0.58;0.72;1" dur="8s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="180 40;180 40;830 172;880 190;880 190" keyTimes="0;0.55;0.72;0.78;1" dur="8s" repeatCount="indefinite"/></path>
  </g>
  {skyline(1200, 350, "#131c28", 7)}
  {skyline(1200, 395, "#0c1119", 21)}
  {''.join(rain)}
  <rect x="26" y="395" width="1148" height="19" fill="#0a0e14"/>
  <rect x="26" y="392" width="1148" height="4" fill="url(#neonGround)"><animate attributeName="opacity" values="0.55;1;0.55" dur="3.4s" repeatCount="indefinite"/></rect>
  <g transform="translate(975, 138)">
    <g stroke="{GREEN}" stroke-width="4.5" stroke-linejoin="round" fill="#04070d" stroke-linecap="round">
      <path d="M-8 66 L10 0 L33 52 Z"/>
      <path d="M73 52 L96 0 L114 66 Z"/>
      <rect x="0" y="48" width="106" height="80" rx="20"/>
      <path d="M10 122 L10 238 L98 238 L98 122 Z"/>
      <rect x="-6" y="238" width="122" height="10" rx="4" fill="#04070d"><animate attributeName="y" values="238;229;238" dur="3.4s" repeatCount="indefinite"/></rect>
    </g>
    <g transform="translate(92, 150)">
      <path d="M0 0 Q46 12 42 74" stroke="{GREEN}" stroke-width="7" fill="none" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" values="0 0 0;-16 0 0;0 0 0" dur="3.1s" repeatCount="indefinite"/>
      </path>
    </g>
    <rect x="28" y="88" width="14" height="10" rx="5" fill="{GREEN}"><animate attributeName="height" values="10;10;1.2;10;10" keyTimes="0;0.42;0.48;0.55;1" dur="4.6s" repeatCount="indefinite"/></rect>
    <rect x="64" y="88" width="14" height="10" rx="5" fill="{GREEN}"><animate attributeName="height" values="10;10;1.2;10;10" keyTimes="0;0.42;0.48;0.55;1" dur="4.6s" begin="-0.2s" repeatCount="indefinite"/></rect>
    <path d="M53 108 L53 116" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</g>
<rect x="26" y="26" width="1148" height="388" rx="18" fill="none" stroke="{BORDER}" stroke-width="2"/>
<rect x="26" y="288" width="540" height="92" fill="{BG}" opacity="0.62"/>
<g font-family="{FONT}" opacity="0">
  <animate attributeName="opacity" values="0;1" dur="0.6s" begin="0.1s" fill="freeze"/>
  <text x="56" y="84" font-size="16" fill="{GREEN}" letter-spacing="6">G I T H U B</text>
</g>
<g font-family="{SANS}" opacity="0" transform="translate(-34,0)">
  <animate attributeName="opacity" values="0;1" dur="0.7s" begin="0.3s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" values="-34 0;0 0" dur="0.8s" begin="0.3s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
  <text x="54" y="156" font-size="54" font-weight="800" fill="{STRONG}">Nicolas Dwi Dharma</text>
</g>
<g font-family="{FONT}" opacity="0" transform="translate(-20,0)">
  <animate attributeName="opacity" values="0;1" dur="0.6s" begin="0.55s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" values="-20 0;0 0" dur="0.7s" begin="0.55s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
  <text x="54" y="198" font-size="19" fill="{MUTED}">@nekonaru // explorer</text>
</g>
<g font-family="{FONT}" font-size="14" opacity="0">
  <animate attributeName="opacity" values="0;1" dur="0.6s" begin="0.8s" fill="freeze"/>
  <rect x="54" y="224" width="172" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"><animate attributeName="stroke" values="{BORDER};{GREEN};{BORDER}" dur="3.6s" begin="1.5s" repeatCount="indefinite"/></rect>
  <text x="140" y="244" fill="{FG}" text-anchor="middle">offline-first tools</text>
  <rect x="236" y="224" width="140" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="306" y="244" fill="{FG}" text-anchor="middle">web and game</text>
  <rect x="386" y="224" width="158" height="30" rx="15" fill="{PANEL_SOFT}" stroke="{BORDER}"/>
  <text x="465" y="244" fill="{FG}" text-anchor="middle">open source</text>
</g>
<rect x="54" y="276" width="470" height="3" fill="url(#glowline)"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></rect>
<text x="54" y="310" font-family="{FONT}" font-size="13" fill="{MUTED}">build in the open, <tspan fill="{GREEN}">ship what works</tspan><tspan fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>_</tspan></text>
<rect x="26" y="26" width="1148" height="3" fill="url(#neonGround)" opacity="0.9"><animate attributeName="opacity" values="0.5;1;0.5" dur="3.4s" repeatCount="indefinite"/></rect>
"""
    return svg(1200, 440, body)


def ticker():
    items = ["SWARA", "TALOS", "MORFA", "GETTA", "NIUSIC", "LEKAS", "WEBSITEKWU", "GAMETECH26", "STASHIFY", "RENTRA"]
    half = "  //  ".join(items) + "  //  "
    char_w = 13.4
    span = len(half) * char_w
    body = f"""
<clipPath id="clip"><rect x="0" y="0" width="1200" height="46"/></clipPath>
<rect width="1200" height="46" fill="{PANEL}"/>
<polygon points="0,0 1200,0 1152,46 0,46" fill="#1a222e" opacity="0.5"/>
<rect x="0" y="0" width="1200" height="1" fill="{BORDER}" opacity="0.6"/>
<rect x="0" y="45" width="1200" height="1" fill="{BORDER}" opacity="0.6"/>
<g clip-path="url(#clip)" font-family="{FONT}" font-size="15" fill="{MUTED}" letter-spacing="2">
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0;-{span:.0f} 0" dur="46s" repeatCount="indefinite"/>
    <text x="0" y="29" xml:space="preserve">{esc(half * 3)}</text>
  </g>
</g>
"""
    return svg(1200, 46, body)


def section(label, accent=GREEN):
    return svg(1200, 104, f"""
<rect width="1200" height="104" fill="{BG}"/>
<defs>
  <clipPath id="panelClip"><rect x="330" y="18" width="540" height="68" rx="16"/></clipPath>
  <linearGradient id="shimmer" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{accent}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </linearGradient>
</defs>
<line x1="40" y1="52" x2="340" y2="52" stroke="{BORDER}" stroke-width="2"/>
<line x1="860" y1="52" x2="1160" y2="52" stroke="{BORDER}" stroke-width="2"/>
<circle cx="356" cy="52" r="4" fill="{accent}"><animate attributeName="r" values="4;8;4" dur="2.2s" repeatCount="indefinite"/></circle>
<circle cx="844" cy="52" r="4" fill="{accent}"><animate attributeName="r" values="4;8;4" dur="2.2s" begin="-1.1s" repeatCount="indefinite"/></circle>
<rect x="330" y="18" width="540" height="68" rx="16" fill="{PANEL}" stroke="{accent}" stroke-width="2"/>
<rect x="330" y="18" width="130" height="68" fill="url(#shimmer)" clip-path="url(#panelClip)">
  <animate attributeName="x" values="330;870" dur="3.4s" repeatCount="indefinite"/>
</rect>
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
<rect x="20" y="84" width="1160" height="60" fill="{GREEN}" opacity="0.05">
  <animate attributeName="y" values="84;352;84" dur="5.5s" repeatCount="indefinite"/>
</rect>
{''.join(cat_rows)}
{''.join(rows)}
<rect x="632" y="384" width="13" height="24" fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1.05s" repeatCount="indefinite"/></rect>
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
    y0 = 78
    step = 54
    parts = [f'<rect width="1200" height="430" fill="{BG}"/>']
    parts.append(f'<path d="M238 {y0} L238 {y0 + step * (len(events) - 1)}" stroke="{BORDER}" stroke-width="3" stroke-dasharray="8 10" stroke-linecap="round"><animate attributeName="stroke-dashoffset" values="0;-144" dur="6s" repeatCount="indefinite"/></path>')
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
