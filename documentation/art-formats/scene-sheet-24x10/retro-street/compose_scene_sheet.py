"""Fit the generated Street concept to the exact Scene Sheet 24x10 grid.

Requires Pillow. The concept supplies every material; this script aligns the
composition and repeats one sampled cobblestone cell exactly in clear areas.
"""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-concept.png"
OUTPUT = ROOT.parent / "retro-street.png"
TILE = 16


def cell(image, x, y):
    return image.crop((x * TILE, y * TILE, (x + 1) * TILE, (y + 1) * TILE))


def main():
    concept = Image.open(SOURCE).convert("RGBA")
    draft = concept.resize((384, 160), Image.Resampling.NEAREST)
    ground = cell(draft, 2, 3)
    water = cell(draft, 16, 8)
    sheet = Image.new("RGBA", (384, 160))

    def place(tile, x, y):
        sheet.paste(tile, (x * TILE, y * TILE))

    for y in range(10):
        for x in range(24):
            place(ground, x, y)

    # A brick room retains the source wall materials and leaves identical
    # cobblestone cells across both its interior and the exterior ground.
    top = cell(draft, 4, 0)
    bottom = cell(draft, 4, 5)
    face = cell(draft, 15, 1)
    left = cell(draft, 0, 3)
    right = cell(draft, 11, 3)
    for x in range(1, 11):
        place(top, x, 0)
        place(bottom, x, 8)
    for x in range(2, 10):
        place(face, x, 1)
    for y in range(1, 8):
        place(left, 1, y)
        place(right, 10, y)
    for x, y, sx, sy in ((1, 0, 0, 0), (10, 0, 11, 0),
                         (1, 8, 0, 5), (10, 8, 11, 5)):
        place(cell(draft, sx, sy), x, y)

    # Match the original external wallset footprint: a room with a thick
    # lower wall band, followed by narrow vertical wall and street channels.
    for x in range(12, 20):
        place(top, x, 0)
    for y in range(1, 4):
        place(left, 12, y)
        place(right, 18, y)
        place(face, 19, y)
    for x in range(12, 20):
        place(bottom, x, 4)
        place(face, x, 5)
        place(face, x, 6)
    for y in range(0, 6):
        place(right, 20, y)
        place(left, 22, y)
    for y in (0, 1, 4, 5):
        place(face, 23, y)

    # Move the generated staircase into the established lower-middle slot.
    stair = draft.crop((8 * TILE, 7 * TILE, 10 * TILE, 10 * TILE))
    stair = stair.resize((2 * TILE, 4 * TILE), Image.Resampling.NEAREST)
    sheet.paste(stair, (12 * TILE, 6 * TILE))

    # Sewer water uses one dark blue source cell, with brick banks from the
    # generated concept. This remains separate from the repeatable street.
    for y in range(7, 10):
        for x in range(14, 22):
            place(water, x, y)
    bank = cell(draft, 15, 7)
    for x in range(14, 23):
        place(bank, x, 6)
    side = cell(draft, 23, 8)
    for y in range(7, 10):
        place(side, 22, y)

    sheet.save(OUTPUT)
    print(f"Wrote {OUTPUT} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
