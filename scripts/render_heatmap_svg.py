"""Render data/contributions.json as an animated 53x7 heatmap SVG."""
import json, os
from datetime import date, timedelta
from theme import *

ANIMATED = os.environ.get("STATIC") != "1"
data = json.load(open("data/contributions.json"))
days = data["days"]; st = data["stats"]

CELL, STEP = 12, 15
LEFT, TOP = 44, 62
first = date.fromisoformat(days[0]["date"])
start = first - timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
W, H = 860, 218
best = st["best_day"]["date"] if st["best_day"]["count"] else None

cells, months, last_col, last_month = [], [], -9, None
for d in days:
    dt = date.fromisoformat(d["date"])
    col = (dt - start).days // 7
    row = (dt.weekday() + 1) % 7
    x, y = LEFT + col * STEP, TOP + row * STEP
    cls = "l%d" % min(d["level"], 4)
    if d["date"] == best:
        cls = "best"
    delay = f"{col * 0.011 + row * 0.028:.3f}"
    cells.append(
        f'<rect class="c {cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
        f'style="animation-delay:{delay}s"><title>{esc(d["date"])}: {d["count"]}</title></rect>'
    )
    if row == 0 and dt.month != last_month and col - last_col >= 3:
        months.append(f'<text class="dim sm" x="{x}" y="{TOP - 8}">{dt.strftime("%b")}</text>')
        last_col = col
    if row == 0:
        last_month = dt.month

dow = "".join(
    f'<text class="dim sm" x="{LEFT - 8}" y="{TOP + r * STEP + 10}" text-anchor="end">{n}</text>'
    for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
)

fills = "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(RAMP)) + f".best{{fill:{AMBER_HI}}}"
anim = ".c{opacity:0;animation:pop .5s ease-out both}@keyframes pop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}" if ANIMATED else ".c{opacity:1}"
css = style_block(ANIMATED, fills + anim)

fy = TOP + 7 * STEP + 28
lx = W - 40 - 5 * STEP - 62
legend = (f'<text class="dim sm" x="{lx}" y="{fy}">Less</text>' +
    "".join(f'<rect class="l{i}" x="{lx + 30 + i * STEP}" y="{fy - 10}" width="{CELL}" height="{CELL}" rx="3"/>' for i in range(5)) +
    f'<text class="dim sm" x="{lx + 30 + 5 * STEP + 4}" y="{fy}">More</text>')

bd = date.fromisoformat(st["best_day"]["date"]).strftime("%b %-d")
foot = (f'<text xml:space="preserve" x="{LEFT}" y="{fy}"><tspan class="hi">{st["total"]}</tspan> contributions in the last year'
        f'   streak <tspan class="hi">{st["current_streak"]}</tspan> (longest {st["longest_streak"]})'
        f'   best day <tspan class="hi">{st["best_day"]["count"]}</tspan> on {bd}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{st["total"]} contributions in the last year">
<style>{css}</style>
<rect width="{W}" height="{H}" rx="10" fill="{INK}" stroke="{EDGE}"/>
<text class="dim sm" x="{LEFT - 28}" y="22">~/{esc(data["user"])}/contributions.sh</text>
<line x1="0" x2="{W}" y1="32" y2="32" stroke="{EDGE}"/>
{"".join(months)}{dow}
{"".join(cells)}
{foot}{legend}
</svg>'''
open("contrib-heatmap.svg", "w").write(svg)
print("wrote contrib-heatmap.svg", len(svg), "bytes")
