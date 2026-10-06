"""PNG assets GitHub won't take as SVG: avatar + repo social previews. Upload them by hand."""
import os
from PIL import Image, ImageDraw, ImageFont
from theme import INK, EDGE, PAPER, DIM, AMBER

FONT = "/System/Library/Fonts/Menlo.ttc"  # index 0 regular, 1 bold
TILE = "#1e2129"
os.makedirs("assets", exist_ok=True)

def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)

def flap(d, x, y, w, h, ch, size):
    d.rounded_rectangle((x, y, x + w, y + h), radius=max(6, w // 12), fill=TILE, outline=EDGE, width=2)
    d.text((x + w / 2, y + h / 2), ch, font=font(size, True), fill=AMBER, anchor="mm")
    mid = y + h // 2
    d.rectangle((x, mid - max(1, h // 80), x + w, mid + max(1, h // 80)), fill=INK)
    r = max(3, w // 30)
    for cx in (x + r * 2, x + w - r * 2):
        d.ellipse((cx - r, mid - r, cx + r, mid + r), fill=EDGE)

def avatar():
    im = Image.new("RGB", (500, 500), INK)
    flap(ImageDraw.Draw(im), 150, 110, 200, 280, "S", 210)  # fits inside the circular crop
    im.save("assets/avatar.png")

def preview(repo, desc):
    W, H = 1280, 640
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    gap = 8
    tw = min(110, (W - 120 - gap * (len(repo) - 1)) // len(repo))
    th = int(tw * 1.35)
    x0 = (W - (len(repo) * tw + (len(repo) - 1) * gap)) // 2
    y0 = 335 - (th + 85) // 2  # centre tiles + description between the rule and the url
    for i, ch in enumerate(repo.upper()):
        flap(d, x0 + i * (tw + gap), y0, tw, th, ch, int(tw * 0.8))
    d.text((W / 2, y0 + th + 70), desc, font=font(30), fill=PAPER, anchor="mm")
    d.text((W / 2, H - 70), f"github.com/SoansSandha/{repo}", font=font(24), fill=DIM, anchor="mm")
    d.line((60, 100, W - 60, 100), fill=EDGE, width=2)
    d.text((60, 60), "DEPARTURES", font=font(24, True), fill=AMBER, anchor="lm")
    im.save(f"assets/{repo}-preview.png")

avatar()
preview("running-order", "Sort a Spotify playlist without losing date-added.")
preview("placeless", "A Spyfall-style multiplayer game in the browser.")
print("wrote", sorted(os.listdir("assets")))
