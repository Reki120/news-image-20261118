#!/usr/bin/env python3
"""Generate the 18 November 2026 world-news summary image (1024x1024 PNG).

One clear composition: a masthead with the date, one large Gulf scene for
the main story (US-Iran exchanges over Bahrain), three secondary cards
(Quad in Manila, NVIDIA's record quarter, Kerch bridge hit again), and a
source footer. Everything is drawn with PIL primitives; no network, no
timestamps and no randomness, so two runs write identical bytes.

Stories (all verified 18 Nov 2026 against Reuters / AP / Al Jazeera / CNN):
- MAIN: Iran's drones intercepted over Bahrain (third attack in five
  days); US jets hit an IRGC missile site on Qeshm Island; Bahrain
  all-clear after an overnight alert; Kuwait's air defences also
  countered drones.
- Quad leaders meet in Manila (US, Japan, Australia, India) for the
  first time in two years, ahead of APEC in Shenzhen.
- NVIDIA posts a record $115.8bn quarter, up 103%; board rules out
  Jensen Huang's return as CEO; Colette Kress is interim CEO.
- Ukraine strikes the Kerch bridge for a second day as Russia pounds
  Kyiv crossings.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                   "entry.png")

NAVY = (10, 26, 46)
PANEL = (16, 38, 62)
PANEL_LINE = (42, 74, 104)
GOLD = (232, 184, 75)
WHITE = (245, 247, 250)
MUTED = (196, 210, 224)
SKY_TOP = (24, 42, 71)
SKY_BOT = (198, 90, 46)
SEA = (12, 36, 54)
WAVE = (46, 90, 122)
LAND = (18, 24, 34)
DOME = (205, 212, 218)
RED = (220, 60, 45)
ORANGE = (255, 154, 31)
FLAME = (255, 122, 26)


def load_font(name, size):
    """DejaVu from the repo's fonts/ dir, else the system copy."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(here, "fonts", name),
                 "/usr/share/fonts/truetype/dejavu/" + name):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


BOLD = lambda s: load_font("DejaVuSans-Bold.ttf", s)      # noqa: E731
REG = lambda s: load_font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(y1 - y0, 1)
    for i in range(n):
        t = i / max(n - 1, 1)
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def star(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def drone(draw, x, y, s):
    draw.polygon([(x, y - s), (x + s, y + s * 0.7),
                  (x, y + s * 0.35), (x - s, y + s * 0.7)], fill=(22, 22, 30))


def bezier(p0, p1, p2, steps):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def build():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)

    # ---- masthead ---------------------------------------------------
    d.text((36, 24), "18 NOVEMBER 2026", font=BOLD(44), fill=GOLD)
    tag = "THE WORLD IN ONE IMAGE"
    d.text((988 - d.textlength(tag, font=BOLD(20)), 42), tag,
           font=BOLD(20), fill=MUTED)
    d.rectangle([0, 100, 1024, 104], fill=GOLD)

    # ---- headline band ----------------------------------------------
    d.text((36, 116), "GULF ON EDGE", font=BOLD(60), fill=WHITE)
    d.text((36, 186), "Iran's drones intercepted over Bahrain",
           font=BOLD(23), fill=MUTED)
    d.text((36, 216), "US jets hit missile site on Qeshm Island",
           font=BOLD(23), fill=MUTED)

    # ---- main scene: the Gulf at dusk, y 240-660 --------------------
    vgrad(d, (0, 240, 1024, 520), SKY_TOP, SKY_BOT)
    # low sun with glow
    for r, a in ((70, 22), (50, 40), (36, 70)):
        od.ellipse([770 - r, 470 - r, 770 + r, 470 + r],
                   fill=(242, 206, 154, a))
    d.ellipse([770 - 30, 470 - 30, 770 + 30, 470 + 30], fill=(245, 217, 168))
    # sea
    d.rectangle([0, 520, 1024, 660], fill=SEA)
    for row, y in enumerate((542, 568, 596, 624, 646)):
        for k in range(5):
            x = 40 + ((k * 197 + row * 61) % 900)
            d.line([(x, y), (x + 44 + row * 3, y)], fill=WAVE, width=2)
    # Bahrain headland + radar dome, left
    d.polygon([(0, 660), (0, 602), (60, 576), (140, 560), (230, 566),
               (300, 600), (320, 660)], fill=LAND)
    d.rectangle([95, 545, 205, 578], fill=(38, 48, 60))
    d.pieslice([102, 497, 198, 593], start=180, end=360, fill=DOME)
    d.arc([102, 497, 198, 593], start=200, end=340, fill=(150, 158, 166),
          width=2)
    d.line([(205, 545), (205, 505)], fill=(150, 158, 166), width=3)
    d.ellipse([201, 499, 209, 507], fill=RED)
    d.text((102, 614), "BAHRAIN", font=BOLD(15), fill=WHITE)
    # drone trails arcing in from the upper right
    for p0, p1, p2 in (((880, 272), (600, 330), (232, 500)),
                       ((830, 302), (580, 382), (262, 512))):
        for (x, y) in bezier(p0, p1, p2, 16):
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED)
    drone(d, 640, 322, 12)
    drone(d, 480, 382, 11)
    # interceptor burst
    od.ellipse([560 - 30, 300 - 30, 560 + 30, 300 + 30],
               fill=(255, 154, 31, 60))
    star(d, 560, 300, 26, 10, 8, ORANGE)
    star(d, 560, 300, 13, 5, 8, (255, 214, 90))
    # Qeshm Island + strike plume, right
    d.polygon([(700, 660), (720, 590), (790, 560), (880, 545), (960, 560),
               (1024, 590), (1024, 660)], fill=LAND)
    for (x, y, r) in ((872, 452, 22), (906, 432, 28), (934, 462, 20)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(105, 105, 110))
    d.polygon([(850, 520), (866, 446), (884, 520)], fill=FLAME)
    d.polygon([(866, 520), (884, 440), (902, 520)], fill=(255, 176, 66))
    d.polygon([(876, 520), (888, 470), (900, 520)], fill=(255, 222, 120))
    d.text((798, 622), "QESHM ISLAND", font=BOLD(15), fill=WHITE)
    # US Navy ship in the gulf
    d.polygon([(420, 588), (520, 588), (505, 602), (435, 602)],
              fill=(120, 130, 140))
    d.rectangle([460, 574, 490, 588], fill=(140, 150, 160))
    d.line([(475, 574), (475, 558)], fill=(150, 158, 166), width=2)
    d.line([(400, 606), (430, 606)], fill=(200, 210, 220), width=2)
    d.line([(520, 606), (556, 606)], fill=(200, 210, 220), width=2)
    # fact pill over the sky
    pill = "THIRD ATTACK IN A WEEK"
    d.rounded_rectangle([36, 256, 36 + 216, 284], radius=14,
                        fill=(10, 26, 46))
    d.text((48, 261), pill, font=BOLD(14), fill=GOLD)

    # ---- secondary cards, y 676-924 ---------------------------------
    cards = [
        ("QUAD MEETS AGAIN",
         "Trump in Manila with Japan, Australia, India \u2014 first summit in two years",
         "quad"),
        ("NVIDIA'S $115.8BN QUARTER",
         "Record sales, up 103% \u2014 board rules out Huang's return",
         "chip"),
        ("KERCH BRIDGE HIT AGAIN",
         "Ukraine hits the Kerch bridge again as Russia pounds Kyiv crossings",
         "bridge"),
    ]
    for i, (title, body, kind) in enumerate(cards):
        x = 36 + i * 324
        d.rounded_rectangle([x, 676, x + 304, 924], radius=10,
                            outline=PANEL_LINE, width=2, fill=PANEL)
        ix, iy = x + 24, 700
        if kind == "quad":
            for j, c in enumerate(((58, 89, 152), (200, 60, 50),
                                   (240, 180, 60), (40, 140, 90))):
                d.ellipse([ix + j * 34, iy, ix + j * 34 + 28, iy + 28],
                          fill=c)
        elif kind == "chip":
            d.rounded_rectangle([ix, iy, ix + 64, iy + 56], radius=6,
                                fill=(22, 120, 70))
            for px in (ix - 8, ix + 64):
                for py in (iy + 10, iy + 28, iy + 46):
                    d.rectangle([px, py, px + 8, py + 4], fill=(140, 150, 160))
            d.text((ix + 8, iy + 15), "NVDA", font=BOLD(16), fill=WHITE)
        else:
            d.line([(ix, iy + 44), (ix + 110, iy + 44)], fill=(170, 180, 190),
                   width=4)
            for tx in (ix + 18, ix + 78):
                d.line([(tx, iy + 44), (tx, iy + 4)], fill=(170, 180, 190),
                       width=4)
            d.line([(ix, iy + 44), (ix + 18, iy + 4)], fill=(120, 130, 140),
                   width=2)
            d.line([(ix + 110, iy + 44), (ix + 78, iy + 4)],
                   fill=(120, 130, 140), width=2)
            star(d, ix + 96, iy + 18, 12, 5, 8, ORANGE)
        for j, line in enumerate(wrap(d, title, BOLD(23), 256)):
            d.text((x + 24, 772 + j * 28), line, font=BOLD(23), fill=WHITE)
        by = 772 + 28 * max(len(wrap(d, title, BOLD(23), 256)), 1) + 10
        for j, line in enumerate(wrap(d, body, REG(16), 256)):
            d.text((x + 24, by + j * 21), line, font=REG(16), fill=MUTED)

    # ---- footer -------------------------------------------------------
    d.rectangle([0, 940, 1024, 942], fill=GOLD)
    d.text((36, 962), "Wednesday 18 November 2026", font=BOLD(16),
           fill=WHITE)
    src = "Sources: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 CNN"
    d.text((988 - d.textlength(src, font=REG(14)), 965), src,
           font=REG(14), fill=MUTED)

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    print(build())
