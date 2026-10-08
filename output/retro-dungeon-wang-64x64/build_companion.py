"""Build the 64px Wang companion from the generated dungeon scene sheet."""

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "retro-dungeon-scene-sheet-64x64.png"
DEST = Path(__file__).resolve().parent
SIZE = 64
MASKS = (7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
         207, 223, 231, 241, 243, 247, 249, 252, 253, 255)


def wall_at(mask, x, y):
    north, northeast, east, southeast, south, southwest, west, northwest = (
        bool(mask & (1 << bit)) for bit in range(8))
    if not north and y < 48 or not east and x >= 16:
        return True
    if not south and y >= 16 or not west and x < 48:
        return True
    if north and east and not northeast and x >= 40 and y < 24:
        return True
    if east and south and not southeast and x >= 40 and y >= 40:
        return True
    if south and west and not southwest and x < 24 and y >= 40:
        return True
    if west and north and not northwest and x < 24 and y < 24:
        return True
    return False


def cap_at(mask, x, y):
    return ((not mask & 1 and y < 22) or
            (not mask & 4 and x >= 42) or
            (not mask & 16 and y >= 42) or
            (not mask & 64 and x < 22))


def main():
    scene = Image.open(SOURCE).convert("RGBA")
    floor = scene.crop((200, 190, 264, 254)).convert("RGB")
    wall = scene.crop((330, 60, 394, 124)).convert("RGB")
    cap = scene.crop((390, 0, 454, 64)).convert("RGB")
    water = scene.crop((1040, 460, 1104, 524)).convert("RGB")
    stairs = scene.crop((765, 405, 829, 469)).convert("RGB")
    sheet = Image.new("RGBA", (6 * SIZE, 4 * SIZE), (0, 0, 0, 0))
    for tile_id, mask in enumerate(MASKS):
        tile = Image.new("RGBA", (SIZE, SIZE))
        pixels = tile.load()
        for y in range(SIZE):
            for x in range(SIZE):
                material = ((cap if cap_at(mask, x, y) else wall)
                            if wall_at(mask, x, y) else floor)
                rgb = material.getpixel((x, y))
                pixels[x, y] = (*rgb, 255)
        sheet.paste(tile, ((tile_id % 6) * SIZE, (tile_id // 6) * SIZE))
    for tile_id, tile in ((21, Image.new("RGB", (SIZE, SIZE), (40, 44, 46))),
                          (22, water), (23, stairs)):
        sheet.paste(tile, ((tile_id % 6) * SIZE, (tile_id // 6) * SIZE))
    sheet.save(DEST / "tiles.png", optimize=True)
    mapping = {
        "source_scene_sheet": str(SOURCE),
        "art_source_attribution": "Style reference supplied by the user; original creator and license were not provided.",
        "author_date": "2026-10-08",
        "theme": "Retro Dungeon based on user-supplied reference",
        "tile_width": SIZE,
        "tile_height": SIZE,
        "columns": 6,
        "rows": 4,
        "wang_set": "Walkable rooms",
        "wang_color": "Walkable floor",
        "wang_type": "mixed",
        "painted_direction": "floor footprint over dark stone",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "figure8_required_masks": [7, 28, 31, 112, 124, 127, 193,
                                   199, 223, 241, 247, 253, 255],
        "known_missing_masks": [mask for mask in range(256) if mask not in MASKS],
        "verified_fixture": "../tiled-ai-sample-level/retro-dungeon-64-figure-8-wang.tmx",
        "verified_wang_cells": 200,
        "erase_repaint_probe": {"x": 11, "y": 20, "tile_id": 1},
        "tiles": [{"local_id": i, "mask": mask,
                   "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
                  for i, mask in enumerate(MASKS)],
        "void_tile_id": 21,
        "water_tile_id": 22,
        "stairs_tile_id": 23,
    }
    (DEST / "mapping.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
