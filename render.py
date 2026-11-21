#!/usr/bin/env python3
"""Render the invented passport spread for
the-passport-page-of-a-countr-2-20261121-0318.

Output: entry/entry.png — 1024x1024 PNG, an open passport spread for the
invented Republic of Veskara. Drawn procedurally with Pillow; no network,
no external assets. Run: python3 render.py
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry", "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
MONO = os.path.join(FD, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FD, "DejaVuSansMono-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def centered(draw, x, y, s, f, fill):
    draw.text((x - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


# ---------------------------------------------------------------- MRZ
def mrz_check(s):
    vals = {c: (int(c) if c.isdigit() else (ord(c) - 55 if c.isalpha() else 0))
            for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<"}
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<VESKOVAC<<ELENA<MARIS" + "<" * 21
    assert len(line1) == 44, len(line1)
    doc = "VK847291<"  # 9 chars, ICAO TD3 positions 1-9
    dob, sex, exp = "940314", "F", "330612"
    personal = "<" * 14
    core = (doc + mrz_check(doc) + "VES" + dob + mrz_check(dob) + sex + exp
            + mrz_check(exp) + personal + mrz_check(personal))
    line2 = core + mrz_check(core)
    assert len(line2) == 44, len(line2)
    return line1, line2


# ---------------------------------------------------------------- portrait
def draw_portrait(size=(150, 190)):
    w, h = size
    img = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(img)
    # muted studio backdrop, vertical gradient
    for y in range(h):
        t = y / h
        r = int(126 + (88 - 126) * t)
        g = int(138 + (100 - 138) * t)
        b = int(152 + (116 - 152) * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    # soft backdrop shadow ellipse behind head
    d.ellipse([18, 8, w - 18, 130], fill=(96, 110, 126))
    cx = w // 2
    # shoulders / jacket
    d.polygon([(18, h), (48, 138), (62, 128), (88, 128), (102, 138), (132, h)],
              fill=(38, 48, 66))
    # shirt collar
    d.polygon([(62, 128), (75, 148), (cx, 158), (88, 148)], fill=(238, 234, 224))
    d.polygon([(62, 128), (cx, 158), (75, 148)], fill=(226, 221, 210))
    d.polygon([(88, 128), (cx, 158), (75, 148)], fill=(214, 209, 198))
    # neck
    d.rectangle([cx - 11, 108, cx + 11, 134], fill=(198, 148, 112))
    d.rectangle([cx - 11, 108, cx + 11, 116], fill=(176, 128, 96))
    # face
    d.ellipse([cx - 30, 34, cx + 30, 108], fill=(217, 169, 134))
    # ears
    d.ellipse([cx - 34, 62, cx - 26, 82], fill=(217, 169, 134))
    d.ellipse([cx + 26, 62, cx + 34, 82], fill=(217, 169, 134))
    # hair: dark bob framing the face
    d.pieslice([cx - 36, 22, cx + 36, 96], 180, 360, fill=(58, 40, 30))
    d.ellipse([cx - 36, 22, cx + 36, 78], fill=(58, 40, 30))
    d.ellipse([cx - 30, 34, cx + 30, 108], fill=(217, 169, 134))  # face over hair
    d.pieslice([cx - 36, 22, cx + 36, 96], 180, 360, fill=(58, 40, 30))
    # hair sides falling to shoulders
    d.polygon([(cx - 36, 40), (cx - 30, 40), (cx - 32, 132), (cx - 42, 132)],
              fill=(58, 40, 30))
    d.polygon([(cx + 36, 40), (cx + 30, 40), (cx + 32, 132), (cx + 42, 132)],
              fill=(58, 40, 30))
    # brows
    d.line([(cx - 20, 66), (cx - 8, 64)], fill=(58, 40, 30), width=3)
    d.line([(cx + 8, 64), (cx + 20, 66)], fill=(58, 40, 30), width=3)
    # eyes
    for ex in (cx - 14, cx + 14):
        d.ellipse([ex - 5, 69, ex + 5, 75], fill=(255, 250, 244))
        d.ellipse([ex - 3, 69, ex + 3, 75], fill=(46, 34, 28))
    # nose
    d.line([(cx, 76), (cx - 2, 88), (cx + 2, 89)], fill=(186, 138, 104), width=2)
    # lips
    d.polygon([(cx - 8, 98), (cx + 8, 98), (cx, 103)], fill=(168, 96, 84))
    d.line([(cx - 8, 98), (cx + 8, 98)], fill=(140, 74, 64), width=1)
    # cheek shading
    d.ellipse([cx - 26, 84, cx - 14, 94], fill=(206, 150, 118))
    d.ellipse([cx + 14, 84, cx + 26, 94], fill=(206, 150, 118))
    # fine grain
    rnd = random.Random(7)
    px = img.load()
    for _ in range(2600):
        x, y = rnd.randrange(w), rnd.randrange(h)
        v = rnd.randint(-14, 14)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)),
                    max(0, min(255, b + v)))
    return img


# ---------------------------------------------------------------- stamps
def circular_stamp(diam, color, top, date, bottom, code=""):
    """A round border-control stamp on its own RGBA layer."""
    layer = Image.new("RGBA", (diam, diam), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = diam // 2
    r_out, r_in = c - 4, c - 16
    d.ellipse([c - r_out, c - r_out, c + r_out, c + r_out],
              outline=color + (255,), width=4)
    d.ellipse([c - r_in, c - r_in, c + r_in, c + r_in],
              outline=color + (255,), width=2)
    f_top = font(SANS_B, 12)
    f_date = font(SANS_B, 13)
    f_bot = font(SANS_B, 12)
    centered(d, c, c - r_in + 8, top, f_top, color + (255,))
    centered(d, c, c - 9, date, f_date, color + (255,))
    centered(d, c, c + r_in - 26, bottom, f_bot, color + (255,))
    if code:
        centered(d, c, c + 24, code, font(MONO, 11), color + (230,))
    return layer


def paste_rotated(base, layer, box, angle):
    rot = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(rot, box)


# ---------------------------------------------------------------- build
def main():
    W = H = 1024
    img = Image.new("RGB", (W, H), (34, 38, 45))
    d = ImageDraw.Draw(img, "RGBA")
    # desk vignette
    for i in range(120):
        a = 26 - i // 6
        d.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, max(a, 0)))
    rnd = random.Random(11)
    px = img.load()
    for _ in range(9000):
        x, y = rnd.randrange(W), rnd.randrange(H)
        v = rnd.randint(-8, 8)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)),
                    max(0, min(255, b + v)))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- spread geometry
    X0, X1, Y0, Y1 = 40, 984, 168, 856
    MID = (X0 + X1) // 2
    # page shadows
    d.rectangle([X0 + 4, Y0 + 8, X1 + 4, Y1 + 8], fill=(0, 0, 0, 160))
    # paper
    d.rectangle([X0, Y0, MID, Y1], fill=(244, 239, 228, 255))
    d.rectangle([MID, Y0, X1, Y1], fill=(246, 241, 230, 255))
    # gutter
    d.rectangle([MID - 2, Y0, MID + 2, Y1], fill=(120, 110, 92, 255))
    d.rectangle([MID - 10, Y0, MID - 2, Y1], fill=(0, 0, 0, 26))
    d.rectangle([MID + 2, Y0, MID + 10, Y1], fill=(0, 0, 0, 26))
    # paper edge lines
    d.rectangle([X0, Y0, X1, Y1], outline=(150, 138, 116, 255), width=2)
    d.line([MID, Y0, MID, Y1], fill=(150, 138, 116, 255), width=2)

    ink = (32, 38, 52, 255)
    faint = (90, 96, 110, 255)
    rule = (120, 110, 92, 255)

    # faint guilloche arcs on both pages
    for cx0 in (X0 + 60, MID + 60):
        for k in range(5):
            d.arc([cx0 - 90 - k * 14, Y0 + 330 - k * 14,
                   cx0 + 330 + k * 14, Y0 + 750 + k * 14],
                  200, 340, fill=(150, 158, 172, 26), width=1)

    # ================================================= LEFT PAGE: data page
    # coat of arms: shield with mountain + waves + star
    ex, ey = (X0 + MID) // 2, Y0 + 26
    d.polygon([(ex - 26, ey), (ex + 26, ey), (ex + 26, ey + 26),
               (ex, ey + 44), (ex - 26, ey + 26)], outline=(42, 58, 84, 255), width=3)
    d.polygon([(ex - 20, ey + 22), (ex - 8, ey + 6), (ex, ey + 16),
               (ex + 8, ey + 4), (ex + 20, ey + 22)], fill=(42, 58, 84, 255))
    d.line([(ex - 20, ey + 28), (ex - 10, ey + 24), (ex, ey + 28),
            (ex + 10, ey + 24), (ex + 20, ey + 28)], fill=(42, 58, 84, 255), width=2)
    d.line([(ex - 20, ey + 34), (ex - 10, ey + 30), (ex, ey + 34),
            (ex + 10, ey + 30), (ex + 20, ey + 34)], fill=(42, 58, 84, 255), width=2)
    centered(d, ex, ey + 52, "★", font(SANS_B, 13), (42, 58, 84, 255))

    ty = Y0 + 96
    centered(d, (X0 + MID) // 2, ty, "REPUBLIC OF VESKARA",
             font(SERIF_B, 24), ink)
    centered(d, (X0 + MID) // 2, ty + 30, "R E P U B L I K A   V E S K A R A",
             font(SANS, 11), faint)
    centered(d, (X0 + MID) // 2, ty + 50, "P A S S P O R T",
             font(SANS_B, 16), ink)
    d.line([X0 + 28, ty + 74, MID - 28, ty + 74], fill=rule, width=2)
    d.line([X0 + 28, ty + 78, MID - 28, ty + 78], fill=rule, width=1)

    # type / code / number row
    ry = ty + 92
    for lx, lab, val in ((X0 + 28, "TYPE", "P"),
                         (X0 + 130, "CODE", "VES"),
                         (X0 + 240, "PASSPORT No.", "VK 847 291")):
        d.text((lx, ry), lab, font=font(SANS, 10), fill=faint)
        d.text((lx, ry + 13), val, font=font(SANS_B, 15), fill=ink)

    # portrait
    photo = draw_portrait()
    px0, py0 = X0 + 28, ry + 44
    img.paste(photo, (px0, py0))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([px0, py0, px0 + 150, py0 + 190], outline=(90, 84, 70, 255), width=2)
    # official seal overlapping photo corner
    seal = Image.new("RGBA", (56, 56), (0, 0, 0, 0))
    ds = ImageDraw.Draw(seal)
    ds.ellipse([4, 4, 52, 52], outline=(146, 116, 52, 235), width=3)
    ds.ellipse([11, 11, 45, 45], outline=(146, 116, 52, 235), width=1)
    ds.text((28, 18), "★", font=font(SANS_B, 14), fill=(146, 116, 52, 235),
            anchor="mm")
    ds.text((28, 36), "VES", font=font(SANS_B, 9), fill=(146, 116, 52, 235),
            anchor="mm")
    img.paste(seal, (px0 + 92, py0 + 140), seal)
    d = ImageDraw.Draw(img, "RGBA")

    # data fields, right of portrait
    fx = X0 + 198
    f_lab, f_val = font(SANS, 10), font(SANS_B, 15)
    fields = [
        ("SURNAME", "KOVAC"),
        ("GIVEN NAMES", "ELENA MARIS"),
        ("NATIONALITY", "VESKARRAN"),
        ("DATE OF BIRTH", "14 MAR 1994"),
        ("PLACE OF BIRTH", "VELLORA, VESKARA"),
        ("SEX", "F"),
        ("OCCUPATION", "LIGHTHOUSE KEEPER"),
    ]
    fy = py0 - 4
    for lab, val in fields:
        d.text((fx, fy), lab, font=f_lab, fill=faint)
        d.text((fx, fy + 12), val, font=f_val, fill=ink)
        fy += 30
    # signature
    d.text((px0, py0 + 198), "Holder's signature",
           font=font(SANS_I, 10), fill=faint)
    d.text((px0, py0 + 212), "Elena M. Kovac",
           font=font(SERIF, 20), fill=(52, 52, 66, 255))
    d.line([px0, py0 + 236, px0 + 150, py0 + 236], fill=rule, width=1)

    # issue / expiry / authority
    iy = py0 + 252
    d.text((X0 + 28, iy), "DATE OF ISSUE", font=f_lab, fill=faint)
    d.text((X0 + 28, iy + 12), "12 JUN 2023", font=f_val, fill=ink)
    d.text((X0 + 190, iy), "DATE OF EXPIRY", font=f_lab, fill=faint)
    d.text((X0 + 190, iy + 12), "12 JUN 2033", font=f_val, fill=ink)
    d.text((X0 + 340, iy), "PLACE OF ISSUE", font=f_lab, fill=faint)
    d.text((X0 + 340, iy + 12), "VELLORA", font=f_val, fill=ink)
    d.text((X0 + 28, iy + 34), "AUTHORITY", font=f_lab, fill=faint)
    d.text((X0 + 28, iy + 46), "MINISTRY OF THE INTERIOR — VELLORA",
           font=font(SANS_B, 13), fill=ink)

    # MRZ
    m1, m2 = mrz_lines()
    my = Y1 - 62
    d.rectangle([X0 + 14, my - 8, MID - 14, my + 44], fill=(232, 227, 214, 255))
    d.text((X0 + 24, my), m1, font=font(MONO, 14), fill=ink)
    d.text((X0 + 24, my + 20), m2, font=font(MONO, 14), fill=ink)
    d.text((MID - 30, Y1 - 18), "2", font=font(SANS, 11), fill=faint)

    # ================================================= RIGHT PAGE: visas & stamps
    rx = (MID + X1) // 2
    centered(d, rx, Y0 + 26, "VISAS", font(SERIF_B, 22), ink)
    centered(d, rx, Y0 + 54, "V I S A S   ·   S T A M P S",
             font(SANS, 11), faint)
    d.line([MID + 28, Y0 + 78, X1 - 28, Y0 + 78], fill=rule, width=2)

    # --- Kalyndor visa (the telling detail)
    vx0, vy0, vx1, vy1 = MID + 36, Y0 + 92, X1 - 36, Y0 + 232
    visa = (38, 74, 130, 255)
    d.rectangle([vx0, vy0, vx1, vy1], outline=visa, width=3)
    d.rectangle([vx0 + 6, vy0 + 6, vx1 - 6, vy1 - 6], outline=visa, width=1)
    centered(d, rx, vy0 + 12, "KALYNDOR — VISA", font(SANS_B, 15), visa)
    centered(d, rx, vy0 + 34, "CLASS B · LIGHTHOUSE SERVICE",
             font(SANS_B, 13), visa)
    centered(d, rx, vy0 + 56, "Single entry · 30 days · Issued 28 JUN 2025",
             font(SANS, 12), visa)
    centered(d, rx, vy0 + 76, "Valid for Northern Reach ports only",
             font(SANS, 12), visa)
    centered(d, rx, vy0 + 96, "FEE 40 KR — PAID", font(SANS_B, 13), visa)
    # small PAID circle on the visa
    d.ellipse([vx1 - 70, vy1 - 50, vx1 - 22, vy1 - 2], outline=(150, 40, 40, 255),
              width=2)
    d.text((vx1 - 46, vy1 - 27), "PAID", font=font(SANS_B, 10),
           fill=(150, 40, 40, 255), anchor="mm")

    # --- stamps (all after issue 12 JUN 2023, in travel order)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    stamps = [
        # (cx, cy, diam, color, top, date, bottom, angle)
        (MID + 130, Y0 + 312, 118, (96, 44, 128), "DRAVNIA", "08 SEP 2024",
         "ARRIVAL", -8),
        (MID + 330, Y0 + 312, 118, (96, 44, 128), "DRAVNIA", "21 SEP 2024",
         "DEPARTURE", 7),
        (MID + 130, Y0 + 452, 118, (32, 110, 96), "OSTMERE", "03 MAR 2025",
         "ARRIVAL", 6),
        (MID + 330, Y0 + 452, 118, (32, 110, 96), "OSTMERE", "10 MAR 2025",
         "DEPARTURE", -6),
        (MID + 130, Y0 + 592, 118, (150, 52, 40), "KALYNDOR", "17 JUL 2025",
         "ARRIVAL", -7),
        (MID + 330, Y0 + 592, 118, (38, 74, 130), "VESKARA", "02 AUG 2025",
         "ENTRY", 8),
    ]
    for cx, cy, diam, color, top, date, bottom, ang in stamps:
        layer = circular_stamp(diam, color, top, date, bottom)
        paste_rotated(base, layer, (cx - diam // 2, cy - diam // 2), ang)
    img = Image.alpha_composite(img.convert("RGBA"), base).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # footer note
    centered(d, rx, Y1 - 34,
             "This passport remains the property of the Republic of Veskara.",
             font(SANS_I, 11), faint)
    d.text((X1 - 30, Y1 - 18), "3", font=font(SANS, 11), fill=faint)

    # faint diagonal watermark on right page
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dw = ImageDraw.Draw(wm)
    dw.text((MID + 230, Y0 + 420), "VESKARA", font=font(SERIF_B, 54),
            fill=(120, 128, 140, 18), anchor="mm")
    wm = wm.rotate(-24, center=(MID + 230, Y0 + 420), resample=Image.BICUBIC)
    img = Image.alpha_composite(img.convert("RGBA"), wm).convert("RGB")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
