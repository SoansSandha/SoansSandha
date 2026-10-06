"""Neofetch-style card. Edit CONTENT, run, commit the SVG."""
import os
from theme import *

ANIMATED = os.environ.get("STATIC") != "1"
USER = "SoansSandha"

# (key, [lines]) -- lines are pre-wrapped to ~84 chars; key "" continues the block above
CONTENT = [
    ("Now", ["Building small web apps: a Spotify playlist sorter and a multiplayer browser game"]),
    ("Stack", ["Remix, React and Tailwind"]),
    ("Content", ["Sanity"]),
    ("Infra", ["Terraform"]),
    ("Also", ["JavaScript, TypeScript, Vite, Supabase, Framer Motion"]),
    None,
    ("Highlights", [
        ("hi", "running-order"),
        "Sorts a Spotify playlist for good without resetting date-added. It moves only",
        "the tracks that have to move, shows a preview first, and has 291 tests.",
        ("hi", "placeless"),
        "A Spyfall-style multiplayer game in the browser. The secrets never reach the",
        "client: Postgres row-level security and server-side roles keep it fair.",
    ]),
]

W, X_KEY, X_VAL, LH = 860, 40, 150, 22
MAX_CHARS = 82  # ~7.8px per mono char; keeps lines inside the card
rows, y, n = [], 86, 0

def line(cls, x, y, text, n):
    d = f' style="animation-delay:{0.25 + n * 0.1:.2f}s"' if ANIMATED else ""
    return f'<text class="ln {cls}" x="{x}" y="{y}"{d}>{esc(text)}</text>'

rows.append(line("hi", X_KEY, 62, "soans@github", 0)); n += 1
for item in CONTENT:
    if item is None:
        y += 10; continue
    key, lines = item
    rows.append(line("key", X_KEY, y, key, n))
    for ln in lines:
        if isinstance(ln, tuple):
            rows.append(line("hi", X_VAL, y, ln[1], n))
        else:
            rows.append(line("", X_VAL, y, ln, n))
        y += LH; n += 1

for item in CONTENT:
    for ln in (item[1] if item else []):
        t = ln[1] if isinstance(ln, tuple) else ln
        assert len(t) <= MAX_CHARS, f"line too long ({len(t)}): {t}"
H = y + 14
css = style_block(ANIMATED, ".ln{opacity:0;animation:in .45s ease-out both}@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}" if ANIMATED else ".ln{opacity:1}")
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="About {USER}">
<style>{css}</style>
<rect width="{W}" height="{H}" rx="10" fill="{INK}" stroke="{EDGE}"/>
<text class="dim sm" x="{X_KEY}" y="22">~/{USER}/whoami</text>
<line x1="0" x2="{W}" y1="32" y2="32" stroke="{EDGE}"/>
<line x1="{X_KEY}" x2="{W - X_KEY}" y1="70" y2="70" stroke="{EDGE}"/>
{"".join(rows)}
</svg>'''
open("info-card.svg", "w").write(svg)
print("wrote info-card.svg", H, "px tall")
