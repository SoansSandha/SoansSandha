"""Shared palette + helpers. Amber-on-ink, like a departure board."""
from html import escape

INK = "#14161c"
EDGE = "#2a2e38"
PAPER = "#e6e2d6"
DIM = "#8b8f9a"
AMBER = "#f0b429"
AMBER_HI = "#ffd96b"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
RAMP = ["#1e2129", "#4a3a12", "#8a6a14", "#c9951a", "#f0b429"]  # level 0..4

def esc(s):
    return escape(str(s), quote=True)

def style_block(animated, extra=""):
    base = f"text{{font-family:{MONO};font-size:13px;fill:{PAPER}}}.dim{{fill:{DIM}}}.key{{fill:{AMBER};font-weight:600}}.hi{{fill:{AMBER_HI};font-weight:600}}.sm{{font-size:11px}}{extra}"
    if not animated:
        return base
    return base + "@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}}"
