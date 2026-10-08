"""Build a 64 px Wang companion for the generated indigo dungeon scene.

The geometry and mask list are adapted from the repository's Dungeon Figure 8
companion builder. Colours and materials follow indigo-dungeon-scene-64x64.png.
This supports the recorded Figure 8 footprint, not arbitrary terrain painting.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


TILE = 64
COLUMNS = 6
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
VOID_ID, WATER_ID, STAIRS_ID = 21, 22, 23
NEIGHBORS = ((0, -1), (1, 0), (0, 1), (-1, 0))
DEST = Path(__file__).resolve().parent


def floor_at(mask: int, x: int, y: int) -> bool:
    samples = (
        (bool(mask & 128), bool(mask & 1), bool(mask & 2)),
        (bool(mask & 64), True, bool(mask & 4)),
        (bool(mask & 32), bool(mask & 16), bool(mask & 8)),
    )
    fx, fy = (x + 0.5) / TILE * 2, (y + 0.5) / TILE * 2
    sx, tx = (0, fx) if fx < 1 else (1, fx - 1)
    sy, ty = (0, fy) if fy < 1 else (1, fy - 1)
    value = (
        samples[sy][sx] * (1 - tx) * (1 - ty)
        + samples[sy][sx + 1] * tx * (1 - ty)
        + samples[sy + 1][sx] * (1 - tx) * ty
        + samples[sy + 1][sx + 1] * tx * ty
    )
    return value >= 0.5


def grain(x: int, y: int, salt: int = 0) -> int:
    return ((x * 17 + y * 31 + x * y * 3 + salt * 13) % 9) - 4


def pixel(tile_id: int, x: int, y: int) -> tuple[int, int, int, int]:
    n = grain(x, y, tile_id)
    if tile_id == VOID_ID:
        return (20 + n, 19 + n, 40 + n, 255)
    if tile_id == WATER_ID:
        wave = (x + y * 2) % 31 < 3 or (x - y * 2) % 37 < 2
        return ((91, 115, 174, 255) if wave else (43 + n, 76 + n, 138 + n, 255))
    if tile_id == STAIRS_ID:
        step = y // 12
        if y % 12 < 3:
            return (147 + n, 143 + n, 167 + n, 255)
        return (88 - step * 3 + n, 91 - step * 3 + n, 122 - step * 3 + n, 255)

    mask = MASKS[tile_id]
    if floor_at(mask, x, y):
        shadow = any(
            0 <= x + dx < TILE and 0 <= y + dy < TILE
            and not floor_at(mask, x + dx, y + dy)
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))
        )
        if shadow or x < 3 or y < 3:
            return (78 + n, 93 + n, 111 + n, 255)
        return (139 + n, 153 + n, 170 + n, 255)

    near_floor = any(
        0 <= x + dx < TILE and 0 <= y + dy < TILE
        and floor_at(mask, x + dx, y + dy)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0),
                       (0, -2), (2, 0), (0, 2), (-2, 0),
                       (0, -3), (3, 0), (0, 3), (-3, 0))
    )
    if near_floor:
        return (149 + n, 143 + n, 171 + n, 255)
    course = y // 16
    mortar = y % 16 < 3 or (x + (32 if course % 2 else 0)) % 32 < 3
    if mortar:
        return (38 + n, 39 + n, 68 + n, 255)
    return (68 + n, 65 + n, 103 + n, 255)


def footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def required_mask(x: int, y: int) -> int:
    north, east, south, west = (
        footprint(x + dx, y + dy) for dx, dy in NEIGHBORS
    )
    return (
        north * 1
        + (north and east and footprint(x + 1, y - 1)) * 2
        + east * 4
        + (east and south and footprint(x + 1, y + 1)) * 8
        + south * 16
        + (south and west and footprint(x - 1, y + 1)) * 32
        + west * 64
        + (west and north and footprint(x - 1, y - 1)) * 128
    )


def main() -> None:
    needed = sorted({required_mask(x, y) for y in range(14) for x in range(28)
                     if footprint(x, y)})
    missing = sorted(set(needed) - set(MASKS))
    if missing:
        raise ValueError(f"Missing Figure 8 Wang masks: {missing}")
    image = Image.new("RGBA", (COLUMNS * TILE, 4 * TILE))
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            tile_id = (y // TILE) * COLUMNS + x // TILE
            pixels[x, y] = pixel(tile_id, x % TILE, y % TILE)
    image.save(DEST / "tiles.png")
    mapping = {
        "theme": "Indigo dungeon",
        "source_image": "../indigo-dungeon-scene-64x64.png",
        "source_builder": "skills/tiled-ai-create-tileset-png/scripts/build_dungeon_wang_companion.py",
        "exact_tsx": "output/indigo-dungeon-wang/output/indigo-dungeon-wang.tsx",
        "author": "Codex",
        "date": "2026-10-08",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 4,
        "wang_set": "Walkable rooms",
        "wang_color": "Walkable floor",
        "wang_type": "mixed",
        "painted_direction": "walkable floor footprint over indigo brick",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a four-tile bridge and a 4x4 core",
        "figure8_required_masks": needed,
        "unsupported_masks": sorted(set(range(256)) - set(MASKS)),
        "verification": {
            "status": "limited Wang-ready",
            "live_tiled_version": "1.12.2",
            "painted_cells": 200,
            "rendered_sample": "output/tiled-ai-sample-level/indigo-dungeon-figure-8-wang.tmx",
            "observed_missing_mask": 0,
            "erase_repaint_repaired_outer_corner": True,
        },
        "tiles": [
            {"local_id": i, "mask": mask,
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "void_tile_id": VOID_ID,
        "water_tile_id": WATER_ID,
        "stairs_tile_id": STAIRS_ID,
        "excluded_from_wang": [VOID_ID, WATER_ID, STAIRS_ID],
    }
    (DEST / "mapping.json").write_text(
        json.dumps(mapping, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {DEST / 'tiles.png'} and mapping.json")


if __name__ == "__main__":
    main()
