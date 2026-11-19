#!/usr/bin/env python3
"""Make the GTA 6 meme picture for the gta6-meme-x-01 bounty.

Original scene drawn in code with PIL: a Vice City sunset (gradient sky,
slatted synthwave sun, ocean, beach, neon skyline, palm trees) and the
official make.fun ghost (assets/mark-1024.png, from https://make.fun/press/)
waiting on the beach. No Rockstar logo or official GTA artwork is used.
Output: meme.png (1200x675).
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
HORIZON = 380
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

random.seed(6)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, width, y0, y1, top, bottom):
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(0, y), (width, y)], fill=lerp(top, bottom, t))


def bezier(p0, p1, p2, steps=24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def palm(draw, x, y, s, color):
    """Draw a palm tree silhouette rooted at (x, y), scale s."""
    # trunk: curved line leaning right
    pts = bezier((x, y), (x + 18 * s, y - 90 * s), (x + 42 * s, y - 165 * s))
    draw.line(pts, fill=color, width=int(13 * s), joint="curve")
    crown = (x + 42 * s, y - 165 * s)
    # fronds: drooping arcs from the crown
    for ang in (-165, -135, -105, -75, -45, -15):
        rad = math.radians(ang)
        tip = (crown[0] + math.cos(rad) * 95 * s,
               crown[1] + math.sin(rad) * 55 * s + 38 * s)
        mid = (crown[0] + math.cos(rad) * 55 * s,
               crown[1] + math.sin(rad) * 30 * s - 18 * s)
        draw.line(bezier(crown, mid, tip), fill=color,
                  width=int(8 * s), joint="curve")
    # coconuts
    for dx, dy in ((-8, 4), (8, 6), (0, 10)):
        draw.ellipse([crown[0] + dx * s - 6 * s, crown[1] + dy * s - 6 * s,
                      crown[0] + dx * s + 6 * s, crown[1] + dy * s + 6 * s],
                     fill=color)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # --- sky: deep purple -> magenta -> orange ---
    vgrad(draw, W, 0, HORIZON, (26, 11, 46), (255, 126, 61))
    # soft magenta band in the middle of the sky
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i, a in enumerate(range(60, 0, -6)):
        od.ellipse([600 - 200 + i * 4, 120 + i * 3,
                    600 + 200 - i * 4, 420 - i * 2],
                   fill=(255, 46, 136, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # --- synthwave sun with slats ---
    cx, cy, r = 600, 310, 105
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 209, 102))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 150, 80), width=3)
    for i, (y, h) in enumerate([(cy + 8, 6), (cy + 26, 8), (cy + 48, 11),
                                (cy + 72, 14)]):
        draw.rectangle([cx - r - 4, y, cx + r + 4, y + h],
                       fill=(255, 126, 61))

    # --- skyline silhouette with neon windows ---
    for bx in range(0, W, 46):
        bh = random.randint(28, 95)
        draw.rectangle([bx, HORIZON - bh, bx + 42, HORIZON],
                       fill=(22, 8, 38))
        for _ in range(random.randint(2, 6)):
            wx = bx + random.randint(5, 34)
            wy = HORIZON - bh + random.randint(6, bh - 12)
            wc = random.choice([(0, 255, 255), (255, 46, 136),
                                (255, 209, 102)])
            draw.rectangle([wx, wy, wx + 4, wy + 6], fill=wc)

    # --- ocean with sun reflection ---
    vgrad(draw, W, HORIZON, 500, (38, 16, 74), (16, 8, 40))
    refl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(refl)
    for i in range(16):
        w = 44 + i * 11
        y = HORIZON + 4 + i * 7
        rd.rectangle([cx - w // 2, y, cx + w // 2, y + 5],
                     fill=(255, 180, 90, 160 - i * 9))
    img.paste(Image.alpha_composite(img.convert("RGBA"), refl).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # --- beach ---
    vgrad(draw, W, 500, H, (232, 176, 106), (178, 124, 66))
    for _ in range(160):
        sx, sy = random.randint(0, W - 1), random.randint(505, H - 1)
        draw.ellipse([sx, sy, sx + 3, sy + 2], fill=(150, 100, 50))

    # --- beach umbrella (left, the waiting spot) ---
    ux, uy = 235, 545
    draw.line([(ux, uy), (ux, uy - 150)], fill=(120, 60, 30), width=7)
    for k, c in enumerate([(255, 46, 136), (255, 255, 255),
                           (0, 200, 200), (255, 255, 255)]):
        x0 = ux - 95 + k * 48
        draw.polygon([(ux, uy - 150), (x0, uy - 118), (x0 + 48, uy - 118)],
                     fill=c, outline=(90, 40, 20))

    # --- palm trees ---
    palm(draw, 130, 675, 1.45, (24, 10, 40))
    palm(draw, 1150, 665, 1.25, (24, 10, 40))

    # --- the make.fun ghost, waiting on the beach ---
    ghost = Image.open("assets/mark-1024.png").convert("RGBA")
    gs = 330
    ghost = ghost.resize((gs, gs), Image.LANCZOS)
    gx, gy = 800, 285
    # soft shadow under the ghost
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([gx + 30, gy + gs - 18, gx + gs - 30, gy + gs + 6],
               fill=(60, 25, 10, 110))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"))
    img.paste(ghost, (gx, gy), ghost)
    draw = ImageDraw.Draw(img)

    # --- meme text, bold white with black stroke ---
    def meme_text(text, size, y):
        font = ImageFont.truetype(FONT, size)
        draw.text((W / 2, y), text, font=font, fill="white",
                  anchor="ma", stroke_width=5, stroke_fill="black")

    meme_text("ME WAITING FOR GTA 6", 62, 26)
    meme_text("SINCE 2013", 78, 568)
    # brand label under the ghost, unmistakable at small size
    font_small = ImageFont.truetype(FONT, 34)
    draw.text((965, 632), "make.fun", font=font_small, fill="white",
              anchor="ma", stroke_width=4, stroke_fill="black")

    img.save("meme.png", "PNG")
    print("saved meme.png", img.size)


if __name__ == "__main__":
    main()
