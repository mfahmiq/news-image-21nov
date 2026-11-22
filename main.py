"""One image summing up the world news of Saturday 21 November 2026.

A 1024x1024 PNG: navy header naming the date, then a 2-by-3 grid of
story panels. Every panel carries a tag, a headline, a short factual
summary and a small illustration drawn from PIL shapes (no photos, no
network). The six stories are the day's verified reporting; nothing is
invented. The program is deterministic: same bytes on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   -> out/entry.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (250, 249, 246)
NAVY = (15, 42, 74)
GOLD = (198, 162, 60)
INK = (24, 24, 24)
SOFT = (90, 96, 104)
EDGE = (214, 210, 203)
WHITE = (255, 255, 255)
PALE = (205, 216, 230)

DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    out, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def burst(draw, cx, cy, r, colour):
    """A starburst: filled circle plus eight spikes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    for k in range(8):
        ang = k * math.pi / 4
        x1 = cx + int(r * 0.9 * math.cos(ang))
        y1 = cy + int(r * 0.9 * math.sin(ang))
        x2 = cx + int(r * 1.7 * math.cos(ang))
        y2 = cy + int(r * 1.7 * math.sin(ang))
        draw.line([x1, y1, x2, y2], fill=colour, width=5)


def draw_missile(draw, bx, by, s):
    """Story 1: a missile streaking toward a burst."""
    draw.line([bx + 8, by + s - 14, bx + s - 30, by + 26],
              fill=(120, 124, 130), width=10)
    draw.polygon([(bx + s - 34, by + 16), (bx + s - 8, by + 30),
                  (bx + s - 30, by + 44)], fill=(90, 94, 100))
    burst(draw, bx + s - 22, by + 22, 12, (232, 126, 32))
    burst(draw, bx + s - 22, by + 22, 6, (245, 196, 66))


def draw_cuffs(draw, bx, by, s):
    """Story 2: handcuffs, two linked rings."""
    steel = (70, 110, 150)
    draw.ellipse([bx + 6, by + 34, bx + 46, by + 74],
                 outline=steel, width=8)
    draw.ellipse([bx + 54, by + 34, bx + 94, by + 74],
                 outline=steel, width=8)
    draw.line([bx + 44, by + 54, bx + 56, by + 54], fill=steel, width=8)
    draw.ellipse([bx + 44, by + 12, bx + 56, by + 24], fill=steel)
    draw.ellipse([bx + 18, by + 48, bx + 34, by + 64],
                 outline=(255, 255, 255), width=3)


def draw_attack(draw, bx, by, s):
    """Story 3: a drone above a blast."""
    draw.line([bx + 50, by + 12, bx + 50, by + 30], fill=(60, 60, 60),
              width=4)
    draw.ellipse([bx + 34, by + 26, bx + 66, by + 42], fill=(60, 60, 60))
    draw.line([bx + 22, by + 30, bx + 78, by + 30], fill=(60, 60, 60),
              width=4)
    burst(draw, bx + 50, by + 72, 16, (200, 60, 32))
    burst(draw, bx + 50, by + 72, 8, (245, 180, 60))
    draw.line([bx + 14, by + 88, bx + 86, by + 88], fill=(120, 124, 130),
              width=4)


def draw_chart(draw, bx, by, s):
    """Story 4: a market line falling, with a red down arrow."""
    draw.line([bx + 10, by + 16, bx + 10, by + 84], fill=(140, 144, 150),
              width=4)
    draw.line([bx + 10, by + 84, bx + 90, by + 84], fill=(140, 144, 150),
              width=4)
    pts = [(bx + 14, by + 26), (bx + 30, by + 32), (bx + 46, by + 30),
           (bx + 62, by + 52), (bx + 78, by + 70)]
    draw.line(pts, fill=(200, 40, 40), width=5, joint="curve")
    draw.polygon([(bx + 78, by + 62), (bx + 90, by + 78),
                  (bx + 66, by + 80)], fill=(200, 40, 40))
    draw.line([bx + 74, by + 20, bx + 74, by + 44], fill=(200, 40, 40),
              width=5)
    draw.polygon([(bx + 68, by + 44), (bx + 80, by + 44),
                  (bx + 74, by + 54)], fill=(200, 40, 40))


def draw_globe(draw, bx, by, s):
    """Story 5: a globe with a leaf."""
    draw.ellipse([bx + 12, by + 10, bx + 88, by + 86],
                 fill=(46, 134, 193), outline=(23, 80, 120), width=3)
    draw.ellipse([bx + 22, by + 22, bx + 48, by + 46], fill=(39, 174, 96))
    draw.ellipse([bx + 52, by + 48, bx + 78, by + 74], fill=(39, 174, 96))
    draw.arc([bx + 12, by + 10, bx + 88, by + 86], 200, 340,
             fill=(255, 255, 255), width=3)
    draw.polygon([(bx + 74, by + 4), (bx + 92, by + 18), (bx + 76, by + 30),
                  (bx + 66, by + 16)], fill=(34, 139, 34))


def draw_summit(draw, bx, by, s):
    """Story 6: three leaders seated around a table."""
    cols = [(178, 34, 34), (27, 77, 158), (146, 90, 16)]
    for k, c in enumerate(cols):
        cx = bx + 22 + k * 28
        draw.ellipse([cx - 11, by + 22, cx + 11, by + 44], fill=c)
        draw.polygon([(cx - 14, by + 52), (cx + 14, by + 52),
                      (cx + 8, by + 76), (cx - 8, by + 76)], fill=c)
    draw.line([bx + 8, by + 78, bx + 92, by + 78], fill=(90, 96, 104),
              width=5)


ILLUSTRATIONS = [draw_missile, draw_cuffs, draw_attack,
                 draw_chart, draw_globe, draw_summit]

STORIES = [
    ("MIDDLE EAST", (178, 34, 34), "Iran strikes Bahrain",
     "Guards claim two US positions hit; fire at a civilian site, no "
     "injuries. Iran says it downed a US drone."),
    ("MEXICO", (21, 94, 117), "'Chapo Isidro' captured",
     "FBI most-wanted Meza Flores seized in Sinaloa; clashes and "
     "roadblocks leave at least 11 dead."),
    ("UKRAINE", (146, 90, 16), "Russia's largest attack yet",
     "110 missiles and 400+ drones; Kryvyi Rih hit, 2 killed, dozens "
     "hurt; debris strays into Poland."),
    ("MARKETS", (27, 77, 158), "AI sell-off hits US stocks",
     "S&P falls 3.7% as AI and chip shares slide into correction."),
    ("CLIMATE", (22, 122, 74), "COP31 talks run past deadline",
     "Antalya summit deadlocked over fossil fuels, no deal yet."),
    ("DIPLOMACY", (120, 53, 153), "Trump defends Putin ties",
     "After the Xi trilateral in Shenzhen; Zelensky calls Putin "
     "a 'killer'."),
]


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    d = ImageDraw.Draw(img)

    # Header: navy band, date, gold rule.
    d.rectangle([0, 0, CANVAS, 168], fill=NAVY)
    d.rectangle([0, 168, CANVAS, 174], fill=GOLD)
    d.text((48, 26), "21 NOVEMBER 2026", font=load(DEJA_B, 72), fill=WHITE)
    d.text((48, 112), "The world in one day  \u00b7  Saturday",
           font=load(DEJA, 26), fill=PALE)

    # Panel grid: two columns, three rows.
    gx, gy = 32, 198
    gw, gh = 464, 236
    gapx, gapy = 32, 24
    f_tag = load(DEJA_B, 20)
    f_head = load(DEJA_B, 32)
    f_det = load(DEJA, 20)

    for i, (tag, accent, head, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (gw + gapx)
        y0 = gy + row * (gh + gapy)
        x1, y1 = x0 + gw, y0 + gh
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE,
                            outline=EDGE, width=2)
        d.rectangle([x0, y0 + 14, x0 + 8, y1 - 14], fill=accent)
        tx = x0 + 28
        d.text((tx, y0 + 20), tag, font=f_tag, fill=accent)
        # Illustration top-right, clear of the headline column.
        ILLUSTRATIONS[i](d, x1 - 118, y0 + 14, 100)
        lines = fit_lines(d, head, f_head, gw - 56 - 112)
        yy = y0 + 52
        for ln in lines[:2]:
            d.text((tx, yy), ln, font=f_head, fill=INK)
            yy += 40
        # Summary wrapped to the full inner width, up to three lines.
        dlines = fit_lines(d, summary, f_det, gw - 56)
        yy = y0 + 146
        for ln in dlines[:3]:
            d.text((tx, yy), ln, font=f_det, fill=SOFT)
            yy += 26

    # Footer.
    d.text((32, CANVAS - 34),
           "Sources: AP  \u00b7  AFP  \u00b7  Reuters  \u00b7  BBC  \u00b7  NYT",
           font=load(DEJA, 18), fill=SOFT)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"))
    print("saved", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
