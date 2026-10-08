"""Build a 16px Retro Dungeon Wang companion for the Figure 8 proof footprint.

The output is a new, grid-safe PNG and a local-ID role key. The scene sheet is
left untouched. This builder intentionally supports the Dungeon theme only;
other themes need their own reviewed materials before using these masks.
"""

import argparse
import json
from pathlib import Path
import struct
import zlib


TILE = 16
COLUMNS = 6
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
VOID_ID = 21
WATER_ID = 22
STAIRS_ID = 23
NEIGHBORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def chunk(kind: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def png_bytes(width: int, height: int, pixel) -> bytes:
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            rows.extend(pixel(x, y))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
            + chunk(b"IEND", b""))


def floor_at(mask: int, x: int, y: int) -> bool:
    samples = (
        (bool(mask & 128), bool(mask & 1), bool(mask & 2)),
        (bool(mask & 64), True, bool(mask & 4)),
        (bool(mask & 32), bool(mask & 16), bool(mask & 8)),
    )
    fx = (x + 0.5) / TILE * 2
    fy = (y + 0.5) / TILE * 2
    sx, tx = (0, fx) if fx < 1 else (1, fx - 1)
    sy, ty = (0, fy) if fy < 1 else (1, fy - 1)
    value = (samples[sy][sx] * (1 - tx) * (1 - ty)
             + samples[sy][sx + 1] * tx * (1 - ty)
             + samples[sy + 1][sx] * (1 - tx) * ty
             + samples[sy + 1][sx + 1] * tx * ty)
    return value >= 0.5


def stone_pixel(mask: int, x: int, y: int) -> tuple[int, int, int, int]:
    grain = ((x * 13 + y * 7 + x * y * 3 + mask) % 9) - 4
    if floor_at(mask, x, y):
        # The floor tile has a periodic slab seam and sparse moss flecks.
        if x in (0, 15) or y in (0, 15):
            return 59 + grain, 67 + grain, 80 + grain, 255
        if (x * 7 + y * 11 + mask) % 101 == 0:
            return 47, 102, 54, 255
        return 91 + grain, 100 + grain, 115 + grain, 255
    near_floor = any(
        0 <= x + dx < TILE and 0 <= y + dy < TILE
        and floor_at(mask, x + dx, y + dy)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0),
                       (0, -2), (2, 0), (0, 2), (-2, 0))
    )
    if near_floor:
        return 121 + grain, 132 + grain, 148 + grain, 255
    mortar = y in (0, 8) or x == (0 if y < 8 else 8)
    if mortar:
        return 30 + grain, 37 + grain, 49 + grain, 255
    highlight = y in (1, 9)
    return (69 + grain + (12 if highlight else 0),
            79 + grain + (12 if highlight else 0),
            94 + grain + (12 if highlight else 0), 255)


def tile_pixel(tile_id: int, x: int, y: int) -> tuple[int, int, int, int]:
    if tile_id < len(MASKS):
        return stone_pixel(MASKS[tile_id], x, y)
    if tile_id == VOID_ID:
        grain = ((x * 5 + y * 11) % 7) - 3
        return 14 + grain, 16 + grain, 23 + grain, 255
    if tile_id == WATER_ID:
        wave = ((x + y * 2) % 16 in (0, 1)) or ((x - y * 2) % 16 in (0, 1))
        if wave:
            return 40, 177, 229, 255
        grain = ((x * 3 + y * 7) % 11) - 5
        return 9, 83 + grain, 165 + grain, 255
    step = y // 4
    if y % 4 == 0:
        return 132, 144, 160, 255
    grain = ((x * 5 + y * 3) % 7) - 3
    shade = 80 - step * 5 + grain
    return shade, shade + 10, shade + 22, 255


def figure8_footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def tiled_mask(x: int, y: int) -> int:
    """Tiled corners are filled only when both touching sides also continue."""
    north, east, south, west = (
        figure8_footprint(x + dx, y + dy) for dx, dy in NEIGHBORS
    )
    return (north * 1
            + (north and east and figure8_footprint(x + 1, y - 1)) * 2
            + east * 4
            + (east and south and figure8_footprint(x + 1, y + 1)) * 8
            + south * 16
            + (south and west and figure8_footprint(x - 1, y + 1)) * 32
            + west * 64
            + (west and north and figure8_footprint(x - 1, y - 1)) * 128)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    required_masks = sorted({tiled_mask(x, y)
                             for y in range(14) for x in range(28)
                             if figure8_footprint(x, y)})
    missing = set(required_masks) - set(MASKS)
    if missing:
        raise ValueError(f"Figure 8 needs missing masks: {sorted(missing)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sheet = png_bytes(COLUMNS * TILE, 4 * TILE,
                      lambda x, y: tile_pixel((y // TILE) * COLUMNS + x // TILE,
                                              x % TILE, y % TILE))
    (args.output_dir / "tiles.png").write_bytes(sheet)
    mapping = {
        "theme": "Retro Dungeon",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 4,
        "wang_set": "Walkable rooms",
        "wang_color": "Walkable floor",
        "wang_type": "mixed",
        "painted_direction": "floor footprint over dark stone",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "figure8_required_masks": required_masks,
        "tiles": [
            {"local_id": i, "mask": mask,
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "void_tile_id": VOID_ID,
        "water_tile_id": WATER_ID,
        "stairs_tile_id": STAIRS_ID,
    }
    (args.output_dir / "mapping.json").write_text(
        json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(f"Built {args.output_dir / 'tiles.png'} and mapping.json")


if __name__ == "__main__":
    main()
