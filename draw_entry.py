#!/usr/bin/env python3
"""Draw entry.png: one image summing up the world news of
Wednesday, 18 November 2026, from the full day's reporting.

Newspaper front-page layout, navy/gold palette:
  masthead with the date, one large Gulf scene for the main story,
  three secondary cards, and a source footer.
Deterministic: no network, no timestamps, no randomness. Pillow only.
Output: entry.png in the output directory ($MAKEFUN_OUTPUT_DIR, or the
directory holding this script when the variable is unset).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or HERE
OUT = os.path.join(OUT_DIR, "entry.png")

W, H = 1024, 1024

PAPER = (247, 243, 234)      # warm off-white newsprint
INK = (18, 24, 34)           # near-black text
NAVY = (14, 42, 71)          # masthead / sea
NAVY_DARK = (9, 30, 52)
NAVY_LIGHT = (24, 62, 99)
GOLD = (201, 168, 106)
GOLD_DARK = (176, 140, 78)
RED = (178, 44, 34)
ORANGE = (224, 122, 42)
SAND = (214, 190, 148)
CARD = (255, 255, 255)
MUTED = (92, 96, 104)

FONTS = os.path.join(HERE, "fonts")


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines of text; returns the y just below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def burst(draw, cx, cy, r, fill):
    """Eight-point explosion starburst centred on (cx, cy)."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8.0
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def arc_pts(p0, p1, lift, n=24):
    """Points along a quadratic bezier from p0 to p1, lifted upward."""
    import math
    mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0 - lift
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * mx + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * my + t ** 2 * p1[1]
        pts.append((x, y))
    return pts


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    d.text((24, 14), "THE WORLD IN ONE IMAGE",
           font=font(True, 46), fill=(255, 255, 255))
    d.text((24, 74), "Wednesday, 18 November 2026  ·  the full day's news",
           font=font(False, 24), fill=GOLD)
    d.text((700, 78), "make.fun bounty", font=font(False, 20), fill=(180, 190, 205))

    # ---- Main story ----------------------------------------------
    d.text((24, 138), "MAIN STORY  —  THE GULF",
           font=font(True, 20), fill=RED)
    d.text((24, 162), "GULF WAR WIDENS",
           font=font(True, 66), fill=INK)
    d.text((24, 238),
           "Iran strikes Kuwait and Bahrain as US jets hit Qeshm Island",
           font=font(False, 26), fill=(52, 58, 68))

    # Schematic Gulf scene panel.
    px0, py0, px1, py1 = 24, 278, 1000, 522
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    d.rectangle([px0, py0, px1, py1], outline=GOLD, width=3)
    # Land masses (stylised): Arabia lower-left, Iran upper-right.
    d.polygon([(px0 + 8, py1 - 8), (px0 + 8, py0 + 128),
               (px0 + 210, py0 + 96), (px0 + 330, py0 + 150),
               (px0 + 300, py1 - 8)], fill=SAND)
    d.polygon([(px0 + 560, py0 + 8), (px1 - 8, py0 + 8),
               (px1 - 8, py0 + 150), (px0 + 700, py0 + 118),
               (px0 + 560, py0 + 60)], fill=SAND)
    # Sea label (open water, upper left).
    d.text((px0 + 36, py0 + 22), "STRAIT OF HORMUZ",
           font=font(True, 17), fill=(150, 180, 210))

    # Missile arcs from Iran toward Kuwait / Bahrain.
    d.line(arc_pts((px0 + 800, py0 + 52), (px0 + 280, py0 + 72), 80),
           fill=ORANGE, width=3)
    d.line(arc_pts((px0 + 760, py0 + 62), (px0 + 450, py0 + 107), 50),
           fill=ORANGE, width=3)

    # Strikes: Qeshm Island, Kuwait, Bahrain, Riyadh pipeline.
    # (cx, cy, name, note, name_xy, note_xy)
    strikes = [
        (290, 350, "KUWAIT", "Ali Al Salem Air Base hit",
         (322, 328), (322, 351)),
        (470, 385, "BAHRAIN", "3rd attack in a week",
         (502, 363), (502, 386)),
        (760, 420, "QESHM ISLAND", "US jets strike IRGC missile site",
         (695, 452), (635, 475)),
        (340, 480, "RIYADH", "Houthi drones hit Saudi pipeline",
         (372, 458), (372, 481)),
    ]
    for cx, cy, name, note, nxy, txy in strikes:
        burst(d, cx, cy, 26, ORANGE)
        burst(d, cx, cy, 15, RED)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 120))
        d.text(nxy, name, font=font(True, 18), fill=(255, 255, 255))
        d.text(txy, note, font=font(False, 15), fill=(205, 215, 228))

    # Summary strip under the scene.
    summary = ("Overnight, Iran fired on US forces in Kuwait and Bahrain; "
               "Houthis hit two Saudi pipeline pumping stations; the Mossad "
               "chief lobbied Washington for new joint strikes; Qatar warned "
               "against escalation; Vance vowed no forever war; Trump said "
               "it would end fairly soon.")
    text_block(d, 24, 534, wrap(d, summary, font(False, 17), 976),
               font(False, 17), (52, 58, 68), leading=22)

    # ---- Secondary cards ------------------------------------------
    cards = [
        ("APEC · SHENZHEN", "Xi greets Trump on the tarmac",
         "Xi Jinping welcomed Trump in Shenzhen as APEC opened — a gesture "
         "he skipped in May. Xi met Putin on Wednesday; first-ever "
         "Trump–Xi–Putin talks are set for Thursday. The US–China tariff "
         "truce runs to 10 Jan 2027."),
        ("GAZA WARNING", "Board of Peace warns ceasefire may collapse",
         "Trump's Board of Peace report, seen by Reuters, accused Israel "
         "and Hamas of failing to meet commitments. Gaza's ceasefire faces "
         "imminent collapse as heavy rain floods displacement camps."),
        ("HORN OF AFRICA", "Ethiopia and Eritrea mass troops at border",
         "Both sides amassed forces along their shared border; ACLED "
         "reported artillery shelling and clashes near Badme, raising "
         "fears of outright war between the historic rivals."),
    ]
    card_w, gap, cy0, cy1 = 312, 20, 606, 884
    for i, (kicker, head, body) in enumerate(cards):
        x0 = 24 + i * (card_w + gap)
        x1 = x0 + card_w
        d.rectangle([x0, cy0, x1, cy1], fill=CARD, outline=GOLD, width=2)
        d.rectangle([x0, cy0, x1, cy0 + 6], fill=NAVY)
        y = cy0 + 18
        d.text((x0 + 14, y), kicker, font=font(True, 16), fill=RED)
        y += 30
        y = text_block(d, x0 + 14, y,
                       wrap(d, head, font(True, 23), card_w - 28),
                       font(True, 23), INK, leading=29)
        y += 8
        text_block(d, x0 + 14, y,
                   wrap(d, body, font(False, 16), card_w - 28),
                   font(False, 16), (52, 58, 68), leading=21)

    # ---- Footer ----------------------------------------------------
    d.rectangle([24, 908, 1000, 912], fill=GOLD)
    d.text((24, 926), "Sources: Reuters  ·  Associated Press  ·  Al Jazeera  ·  CNN",
           font=font(False, 19), fill=MUTED)
    foot2 = ("All events: Wednesday, 18 November 2026. Image drawn by an AI "
             "agent for the make.fun bounty “Sum up 18 November's world "
             "news in one image”.")
    text_block(d, 24, 956, wrap(d, foot2, font(False, 17), 976),
               font(False, 17), fill=MUTED, leading=21)
    d.text((24, 1000), "One image, the full day's news — no events from 19 November.",
           font=font(False, 15), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
