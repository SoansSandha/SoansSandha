"""Split-flap name banner. Each tile riffles through a few letters, then lands once."""
import os, random
from theme import *

ANIMATED = os.environ.get("STATIC") != "1"
NAME = "SOANS"
BOARDING = ["running-order", "placeless"]

W, H = 860, 190
TW, TH, GAP = 92, 120, 12
X0 = (W - (len(NAME) * TW + (len(NAME) - 1) * GAP)) // 2
TOP = 22
TILE, SPLIT = "#1e2129", INK
GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
STEP_S = 0.07  # how long each riffle letter shows

rnd = random.Random(7)  # fixed seed so the SVG is stable between runs
tiles = []
for i, ch in enumerate(NAME):
    x = X0 + i * (TW + GAP)
    cx, base = x + TW // 2, TOP + TH // 2 + 30
    parts = [
        f'<rect x="{x}" y="{TOP}" width="{TW}" height="{TH}" rx="8" fill="{TILE}" stroke="{EDGE}"/>',
    ]
    t = 0.3 + i * 0.12
    if ANIMATED:
        for _ in range(6 + i * 2):
            g = rnd.choice(GLYPHS.replace(ch, ""))
            parts.append(f'<text class="big f" x="{cx}" y="{base}" style="animation-delay:{t:.2f}s">{g}</text>')
            t += STEP_S
    d = f' style="animation-delay:{t:.2f}s"' if ANIMATED else ""
    parts.append(f'<text class="big fin" x="{cx}" y="{base}"{d}>{ch}</text>')
    # the hinge line drawn over the letters, like a real flap
    parts.append(f'<rect x="{x}" y="{TOP + TH // 2 - 1}" width="{TW}" height="2" fill="{SPLIT}"/>')
    parts += [f'<circle cx="{x + dx}" cy="{TOP + TH // 2}" r="3" fill="{EDGE}"/>' for dx in (5, TW - 5)]
    tiles.append("".join(parts))

sub_y = TOP + TH + 34
sub = (f'<text class="sub" x="{W // 2}" y="{sub_y}" text-anchor="middle" xml:space="preserve">'
       f'<tspan class="key">NOW BOARDING</tspan>   '
       + '<tspan class="dim">·</tspan>'.join(f' {esc(r)} ' for r in BOARDING) + '</text>')

css = (f"text{{font-family:{MONO};fill:{PAPER}}}.big{{font-size:84px;font-weight:700;fill:{AMBER};text-anchor:middle}}"
       f".sub{{font-size:14px;letter-spacing:1px}}.key{{fill:{AMBER};font-weight:600}}.dim{{fill:{DIM}}}")
if ANIMATED:
    css += (".f{opacity:0;animation:flash .07s steps(1)}@keyframes flash{from,to{opacity:1}}"
            ".fin{opacity:0;animation:land .01s forwards}@keyframes land{to{opacity:1}}"
            "@media (prefers-reduced-motion:reduce){.f{display:none}.fin{opacity:1;animation:none}}")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}">
<style>{css}</style>
<rect width="{W}" height="{H}" rx="10" fill="{INK}" stroke="{EDGE}"/>
{"".join(tiles)}
{sub}
</svg>'''
open("banner.svg", "w").write(svg)
print("wrote banner.svg", len(svg), "bytes")
