"""Build original 16px Retro Forest tiles for a verified Figure 8 footprint.

The approved Scene Sheet supplies grass and pond pixels. Fence graphics are
authored for this theme and its 21 observed mixed Wang masks. This does not
claim a complete 256-mask mixed set or arbitrary corridor support.
"""

import argparse
import json
from pathlib import Path
import struct
import zlib

from validate_scene_sheet import cell_bytes, read_png


TILE = 16
COLUMNS = 6
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
VOID_ID = 21
POND_ID = 22
PLAIN_FENCE_ID = 23
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


def pixels_for_cell(rows, columns: int, x: int, y: int) -> tuple[tuple[int, ...], ...]:
    raw = cell_bytes(rows, x, y, TILE, TILE, columns)
    return tuple(tuple(raw[i:i + columns]) for i in range(0, len(raw), columns))


def picket_band(along: int, depth: int) -> tuple[int, int, int, int] | None:
    """A pointed six-pixel fence band; `along` is periodic across tile seams."""
    stripe = along % 4
    if depth == 0:
        return (245, 208, 132, 255) if stripe == 1 else None
    if depth == 1:
        return (82, 53, 29, 255) if stripe in (0, 2) else (232, 180, 103, 255) if stripe == 1 else None
    if depth in (4, 5):
        return (84, 54, 29, 255) if depth == 5 else (150, 94, 44, 255)
    if depth == 6:
        return (55, 39, 25, 255) if stripe in (0, 2) else (118, 72, 36, 255) if stripe == 1 else None
    if stripe == 3:
        return None
    grain = ((along * 3 + depth * 5) % 5) - 2
    if stripe == 0:
        return 123 + grain, 77 + grain, 38 + grain, 255
    if stripe == 2:
        return 174 + grain, 115 + grain, 57 + grain, 255
    return 225 + grain, 171 + grain, 94 + grain, 255


def post_pixel(x: int, y: int) -> tuple[int, int, int, int]:
    if x in (0, 4) or y in (0, 4):
        return 54, 38, 25, 255
    if x == 1 or y == 1:
        return 239, 189, 105, 255
    return 155, 96, 48, 255


def fence_pixel(mask: int, x: int, y: int,
                grass: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    color = grass[y * TILE + x]
    north, east, south, west = (not mask & bit for bit in (1, 4, 16, 64))
    if north and y <= 6:
        color = picket_band(x, y) or color
    if south and y >= 9:
        color = picket_band(x, y - 9) or color
    if west and x <= 6:
        color = picket_band(y, x) or color
    if east and x >= 9:
        color = picket_band(y, x - 9) or color
    for side_a, side_b, corner_x, corner_y in (
        (north, west, 0, 0), (north, east, 11, 0),
        (south, west, 0, 11), (south, east, 11, 11),
    ):
        if side_a and side_b and corner_x <= x < corner_x + 5 and corner_y <= y < corner_y + 5:
            color = post_pixel(x - corner_x, y - corner_y)
    # A missing diagonal with both adjoining sides present is an inner turn.
    for corner_bit, side_a, side_b, corner_x, corner_y in (
        (2, north, east, 11, 0), (8, east, south, 11, 11),
        (32, south, west, 0, 11), (128, west, north, 0, 0),
    ):
        if not mask & corner_bit and not side_a and not side_b:
            if corner_x <= x < corner_x + 5 and corner_y <= y < corner_y + 5:
                color = post_pixel(x - corner_x, y - corner_y)
    return color


def plain_fence_pixel(x: int, y: int,
                      grass: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    color = grass[y * TILE + x]
    if y in (9, 10):
        return 99, 61, 31, 255
    stripe = x % 4
    if y == 2:
        return (247, 211, 136, 255) if stripe == 1 else color
    if 3 <= y <= 13 and stripe != 3:
        if stripe == 0:
            return 75, 49, 29, 255
        if stripe == 2:
            return 153, 92, 46, 255
        return 220, 164, 87, 255
    return color


def figure8_footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def tiled_mask(x: int, y: int) -> int:
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
    parser.add_argument("scene_sheet", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    _, rows, channels = read_png(args.scene_sheet, TILE, TILE, True)
    if channels != 4:
        raise ValueError("Forest Scene Sheet must be RGBA")
    grass = pixels_for_cell(rows, channels, 3, 5)
    pond = pixels_for_cell(rows, channels, 18, 8)
    if grass == pond:
        raise ValueError("grass and pond source cells must differ")
    required = sorted({tiled_mask(x, y) for y in range(14) for x in range(28)
                       if figure8_footprint(x, y)})
    missing = set(required) - set(MASKS)
    if missing:
        raise ValueError(f"Figure 8 needs missing masks: {sorted(missing)}")

    def pixel(sheet_x: int, sheet_y: int) -> tuple[int, ...]:
        tile_id = sheet_y // TILE * COLUMNS + sheet_x // TILE
        x, y = sheet_x % TILE, sheet_y % TILE
        if tile_id < len(MASKS):
            return fence_pixel(MASKS[tile_id], x, y, grass)
        if tile_id == VOID_ID:
            return 0, 0, 0, 255
        if tile_id == POND_ID:
            return pond[y * TILE + x]
        return plain_fence_pixel(x, y, grass)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "tiles.png").write_bytes(png_bytes(96, 64, pixel))
    key = {
        "theme": "Retro Forest",
        "source_scene_sheet": str(args.scene_sheet),
        "authored_by": "Codex",
        "authored_date": "2026-10-08",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 4,
        "wang_set": "Fenced clearings",
        "wang_color": "Walkable grass",
        "wang_type": "mixed",
        "painted_direction": "walkable grass footprint enclosed by picket fencing",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "figure8_required_masks": required,
        "tiles": [
            {"local_id": i, "mask": mask,
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "excluded_tiles": {
            "21": "solid black void",
            "22": "forest pond",
            "23": "uniform picket fence for the basic sample",
        },
        "grass_source_cell": [3, 5],
        "pond_source_cell": [18, 8],
    }
    (args.output_dir / "mapping.json").write_text(
        json.dumps(key, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {args.output_dir / 'tiles.png'} and mapping.json")


if __name__ == "__main__":
    main()
