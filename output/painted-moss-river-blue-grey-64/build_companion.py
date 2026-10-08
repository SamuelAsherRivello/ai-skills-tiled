"""Build a 64px Wang companion for the blue-grey painted scene sheet.

The supplied scene provides the grass and water textures. Slate borders are
newly authored for the 21 observed Figure 8 masks. This is deliberately a
limited Figure 8 set, not a complete mixed Wang set.
"""

from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "painted-moss-river-blue-grey-scene-64x64.png"
TILE = 64
COLUMNS = 5
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
VOID_ID, WATER_ID, BASIC_WALL_ID, STAIRS_ID = 21, 22, 23, 24


def seamless_sample(source: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    image = source.crop(box).convert("RGBA")
    px = image.load()
    for y in range(TILE):
        pair = tuple((px[0, y][k] + px[TILE - 1, y][k]) // 2 for k in range(3)) + (255,)
        px[0, y] = px[TILE - 1, y] = pair
    for x in range(TILE):
        pair = tuple((px[x, 0][k] + px[x, TILE - 1][k]) // 2 for k in range(3)) + (255,)
        px[x, 0] = px[x, TILE - 1] = pair
    return image


def stone(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], seed: int) -> None:
    variations = ((67, 82, 96), (77, 92, 106), (83, 99, 112), (71, 88, 102))
    fill = variations[seed % len(variations)]
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0 + 1, y0 + 2, x1, y1 + 2), radius=5,
                           fill=(19, 28, 37, 255))
    draw.rounded_rectangle(box, radius=5, fill=fill,
                           outline=(27, 38, 49, 255), width=2)
    draw.arc((x0 + 3, y0 + 2, x1 - 3, y1 - 2), 195, 325,
             fill=(113, 128, 139, 255), width=2)
    draw.line((x0 + 5, y0 + 4, x1 - 6, y0 + 4),
              fill=(105, 120, 131, 255), width=1)


def draw_border(image: Image.Image, side: str) -> None:
    draw = ImageDraw.Draw(image)
    if side == "N":
        draw.rectangle((0, 0, 63, 19), fill=(28, 39, 51, 255))
        draw.rectangle((0, 19, 63, 22), fill=(30, 41, 49, 220))
        for i, x in enumerate((0, 21, 42)):
            stone(draw, (x, 0, min(x + 21, 63), 18), i)
    elif side == "S":
        draw.rectangle((0, 44, 63, 63), fill=(28, 39, 51, 255))
        draw.rectangle((0, 41, 63, 44), fill=(30, 41, 49, 220))
        for i, x in enumerate((0, 21, 42)):
            stone(draw, (x, 45, min(x + 21, 63), 62), i + 1)
    elif side == "W":
        draw.rectangle((0, 0, 19, 63), fill=(28, 39, 51, 255))
        draw.rectangle((19, 0, 22, 63), fill=(30, 41, 49, 220))
        for i, y in enumerate((0, 21, 42)):
            stone(draw, (0, y, 18, min(y + 21, 63)), i + 2)
    else:
        draw.rectangle((44, 0, 63, 63), fill=(28, 39, 51, 255))
        draw.rectangle((41, 0, 44, 63), fill=(30, 41, 49, 220))
        for i, y in enumerate((0, 21, 42)):
            stone(draw, (45, y, 62, min(y + 21, 63)), i + 3)


def wang_tile(mask: int, grass: Image.Image) -> Image.Image:
    image = grass.copy()
    missing = {"N": not mask & 1, "E": not mask & 4,
               "S": not mask & 16, "W": not mask & 64}
    for side in "NSWE":
        if missing[side]:
            draw_border(image, side)
    draw = ImageDraw.Draw(image)
    # A missing diagonal with both adjacent sides present depicts a concavity.
    for bit, a, b, box, seed in (
        (128, "N", "W", (0, 0, 18, 18), 1),
        (2, "N", "E", (45, 0, 63, 18), 2),
        (8, "S", "E", (45, 45, 63, 63), 3),
        (32, "S", "W", (0, 45, 18, 63), 0),
    ):
        if (missing[a] and missing[b]) or (
            not mask & bit and not missing[a] and not missing[b]
        ):
            stone(draw, box, seed)
    return image


def basic_wall() -> Image.Image:
    image = Image.new("RGBA", (TILE, TILE), (24, 35, 47, 255))
    draw = ImageDraw.Draw(image)
    for row in range(3):
        for col in range(3):
            x, y = col * 21, row * 21
            stone(draw, (x, y, min(x + 20, 63), min(y + 20, 63)), row * 3 + col)
    return image


def main() -> None:
    with Image.open(SOURCE) as src:
        source = src.convert("RGBA")
    grass = seamless_sample(source, (224, 272, 288, 336))
    water = seamless_sample(source, (1120, 465, 1184, 529))
    stairs = source.crop((796, 440, 860, 504)).convert("RGBA")
    tiles = [wang_tile(mask, grass) for mask in MASKS]
    tiles += [Image.new("RGBA", (TILE, TILE), (10, 17, 25, 255)),
              water, basic_wall(), stairs]
    atlas = Image.new("RGBA", (COLUMNS * TILE, 5 * TILE), (0, 0, 0, 0))
    for tile_id, tile in enumerate(tiles):
        atlas.alpha_composite(tile, ((tile_id % COLUMNS) * TILE,
                                     (tile_id // COLUMNS) * TILE))
    atlas.save(HERE / "tiles.png", optimize=True)
    mapping = {
        "theme": "Painted moss river with blue-grey slate",
        "source_scene_sheet": str(SOURCE),
        "authored_by": "Codex",
        "authored_date": "2026-10-08",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 5,
        "wang_set": "Slate-walled clearings",
        "wang_color": "Walkable grass",
        "wang_type": "mixed",
        "painted_direction": "walkable grass footprint enclosed by slate walls",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "tiles": [
            {"local_id": i, "mask": mask,
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "excluded_tiles": {
            str(VOID_ID): "opaque dark void",
            str(WATER_ID): "turquoise water decoration",
            str(BASIC_WALL_ID): "uniform blue-grey wall for basic sample",
            str(STAIRS_ID): "wooden stair decoration",
        },
        "grass_source_box": [224, 272, 288, 336],
        "water_source_box": [1120, 465, 1184, 529],
    }
    (HERE / "mapping.json").write_text(json.dumps(mapping, indent=2) + "\n",
                                       encoding="utf-8")
    print(HERE / "tiles.png")


if __name__ == "__main__":
    main()
