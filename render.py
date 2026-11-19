#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news infographic (1024x1024 PNG).

Original artwork drawn programmatically with Pillow: masthead with the
date, one hero story (GTA VI launch) and four more verified stories from
Thursday 19 November 2026. No photographs, no copied art, no network.
Deterministic: same input always produces the same bytes.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

NAVY = (15, 30, 51)
NAVY_LIGHT = (24, 46, 76)
CREAM = (247, 243, 232)
CARD = (255, 255, 255)
INK = (18, 28, 43)
MUTED = (84, 96, 112)
GOLD = (201, 162, 39)
LIGHT = (159, 179, 200)

MAGENTA = (214, 51, 108)
RED = (176, 42, 48)
SAFFRON = (214, 110, 22)
TEAL = (14, 124, 123)
BRONZE = (168, 124, 18)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_controller(d, cx, cy, s, body, detail):
    """Hand-drawn game controller, centred at (cx, cy), scale s."""
    body_w, body_h = int(150 * s), int(92 * s)
    x0, y0 = cx - body_w // 2, cy - body_h // 2
    d.rounded_rectangle([x0, y0, x0 + body_w, y0 + body_h],
                        radius=int(30 * s), fill=body)
    # grips
    d.ellipse([x0 - 6, y0 + body_h - 34 * s, x0 + 34 * s, y0 + body_h + 10 * s],
              fill=body)
    d.ellipse([x0 + body_w - 34 * s, y0 + body_h - 34 * s,
               x0 + body_w + 6, y0 + body_h + 10 * s], fill=body)
    # d-pad (left)
    px, py = x0 + int(34 * s), y0 + int(38 * s)
    d.rectangle([px - 5, py - 16 * s, px + 5, py + 16 * s], fill=detail)
    d.rectangle([px - 16 * s, py - 5, px + 16 * s, py + 5], fill=detail)
    # buttons (right)
    bx, by = x0 + body_w - int(36 * s), y0 + int(38 * s)
    for dx, dy in ((-14, 0), (14, 0), (0, -14), (0, 14)):
        d.ellipse([bx + dx * s - 6, by + dy * s - 6,
                   bx + dx * s + 6, by + dy * s + 6],
                  fill=detail, outline=body, width=2)
    # sticks
    for sx in (x0 + int(58 * s), x0 + body_w - int(62 * s)):
        d.ellipse([sx - 10, y0 + body_h - 34 * s, sx + 10, y0 + body_h - 14 * s],
                  fill=detail, outline=body, width=2)


def draw_globe(d, cx, cy, r, color):
    """Hand-drawn globe: circle, meridians and parallels."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - int(r * 0.62), cx + r, cy + int(r * 0.62)],
          0, 360, fill=color, width=3)
    d.arc([cx - r, cy + int(r * 0.35), cx + r, cy + int(r * 1.05)],
          180, 360, fill=color, width=3)


def draw_shield(d, cx, cy, s, color):
    """Hand-drawn shield with a check mark."""
    pts = [(cx - 52 * s, cy - 46 * s), (cx + 52 * s, cy - 46 * s),
           (cx + 52 * s, cy + 6 * s), (cx, cy + 62 * s),
           (cx - 52 * s, cy + 6 * s)]
    d.polygon(pts, outline=color, width=5)
    d.line([(cx - 26 * s, cy + 2 * s), (cx - 6 * s, cy + 22 * s),
            (cx + 30 * s, cy - 24 * s)], fill=color, width=7, joint="curve")


def draw_cyclone(d, cx, cy, color):
    """Hand-drawn cyclone spiral (Archimedean), plus rain drops."""
    pts = []
    for t in range(0, 1080, 6):
        ang = math.radians(t)
        rad = 4 + t * 0.055
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.line(pts, fill=color, width=5, joint="curve")
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)
    for dx in (-46, 0, 46):
        d.line([(cx + dx, cy + 52), (cx + dx - 6, cy + 68)],
               fill=color, width=4)


def draw_satellite(d, cx, cy, color):
    """Hand-drawn satellite: body, solar panels, dish, stars."""
    d.rectangle([cx - 16, cy - 14, cx + 16, cy + 14], fill=color)
    d.rectangle([cx - 62, cy - 8, cx - 20, cy + 8], outline=color, width=4)
    d.rectangle([cx + 20, cy - 8, cx + 62, cy + 8], outline=color, width=4)
    d.line([cx - 62, cy, cx - 20, cy], fill=color, width=2)
    d.line([cx + 20, cy, cx + 62, cy], fill=color, width=2)
    d.line([cx, cy - 14, cx + 22, cy - 38], fill=color, width=4)
    d.arc([cx + 12, cy - 52, cx + 38, cy - 26], 300, 60, fill=color, width=4)
    for sx, sy in ((-40, -30), (30, -38), (38, 32), (-30, 38)):
        d.ellipse([cx + sx - 3, cy + sy - 3, cx + sx + 3, cy + sy + 3],
                  fill=color)


def card(draw, x, y, w, h, accent, kicker, headline, sub, icon_fn):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD)
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    icon_cx, icon_cy = x + 62, y + 78
    draw.ellipse([icon_cx - 52, icon_cy - 52, icon_cx + 52, icon_cy + 52],
                 outline=accent, width=3)
    icon_fn(draw, icon_cx, icon_cy, accent)
    tx = x + 132
    draw.text((tx, y + 22), kicker, font=font(SANS_BOLD, 19), fill=accent)
    f_head = font(SANS_BOLD, 29)
    lines = wrap(draw, headline, f_head, w - 152)
    hy = y + 52
    for ln in lines[:2]:
        draw.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 36
    f_sub = font(SANS, 19)
    for ln in wrap(draw, sub, f_sub, w - 152)[:3]:
        draw.text((tx, hy + 6), ln, font=f_sub, fill=MUTED)
        hy += 25


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.text((MARGIN, 26), "THE WORLD TODAY  ·  ONE IMAGE, ONE DAY",
           font=font(SANS_BOLD, 23), fill=GOLD)
    d.text((MARGIN, 58), "19 NOVEMBER 2026",
           font=font(SERIF_BOLD, 66), fill=(250, 247, 238))
    d.text((MARGIN, 136), "Thursday  ·  Five stories that defined the day",
           font=font(SANS, 22), fill=LIGHT)
    d.line([MARGIN, 168, W - MARGIN, 168], fill=GOLD, width=3)

    # --- hero card: GTA VI ---------------------------------------------
    hx, hy, hw, hh = MARGIN, 184, W - 2 * MARGIN, 224
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=16, fill=CREAM)
    d.rounded_rectangle([hx, hy, hx + 236, hy + hh], radius=16, fill=MAGENTA)
    d.rectangle([hx + 180, hy, hx + 236, hy + hh], fill=MAGENTA)
    draw_controller(d, hx + 118, hy + 112, 1.0, (255, 255, 255), MAGENTA)
    d.text((hx + 262, hy + 22), "ENTERTAINMENT  ·  GAMING",
           font=font(SANS_BOLD, 21), fill=MAGENTA)
    d.text((hx + 262, hy + 52), "GTA VI IS HERE",
           font=font(SANS_BOLD, 52), fill=INK)
    f_hero = font(SANS, 23)
    hero_sub = ("After 13 years, Rockstar's blockbuster rolls out worldwide "
                "— Metacritic 99, more than $1.5B already pre-sold.")
    hyy = hy + 122
    for ln in wrap(d, hero_sub, f_hero, hw - 292):
        d.text((hx + 262, hyy), ln, font=f_hero, fill=MUTED)
        hyy += 31

    # --- 2x2 grid of stories -------------------------------------------
    cw, ch, gap = 472, 232, 24
    gx, gy = MARGIN, 432
    stories = [
        (RED, "DIPLOMACY  ·  SHENZHEN", "TRUMP, XI & PUTIN MEET",
         "First-ever three-way summit in Shenzhen — nuclear arms and the "
         "Iran war on the table.",
         lambda dr, x, y, c: draw_globe(dr, x, y, 34, c)),
        (SAFFRON, "ASIA  ·  DEFENCE", "INDIA–JAPAN 2+2 IN TOKYO",
         "Singh and Jaishankar meet Koizumi and Motegi on defence, tech "
         "and a free Indo-Pacific.",
         lambda dr, x, y, c: draw_shield(dr, x, y, 0.72, c)),
        (TEAL, "WEATHER  ·  INDIA", "AKVAN TURNS VERY SEVERE",
         "Cyclone bears down on India's east coast; 200,000 people to be "
         "evacuated, landfall due Friday.",
         lambda dr, x, y, c: draw_cyclone(dr, x, y, c)),
        (BRONZE, "SPACE  ·  SCIENCE", "VOYAGER 1, ONE LIGHT-DAY AWAY",
         "NASA confirms the probe's signal now takes a full day to reach "
         "Earth — launched in 1977.",
         lambda dr, x, y, c: draw_satellite(dr, x, y, c)),
    ]
    for i, (accent, kicker, headline, sub, icon_fn) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        card(d, x, y, cw, ch, accent, kicker, headline, sub, icon_fn)

    # --- footer ----------------------------------------------------------
    d.line([MARGIN, 936, W - MARGIN, 936], fill=(52, 74, 102), width=2)
    d.text((MARGIN, 950),
           "Sources: Reuters · White House · Press Information Bureau of India · "
           "India Meteorological Department · NASA",
           font=font(SANS, 17), fill=LIGHT)
    d.text((MARGIN, 976),
           "Drawn programmatically — no photographs. make.fun news-image-20261119",
           font=font(SANS, 17), fill=LIGHT)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
