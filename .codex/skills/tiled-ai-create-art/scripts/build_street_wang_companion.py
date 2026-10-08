"""Build original 16px Retro Street tiles for the verified Figure 8 footprint.

The Street Scene Sheet supplies cobblestone, sewer, and full-width brick wall
art from its upper-left room. Directional roles use that room's wall cells.
This is not a complete 256-mask mixed set.
"""

import argparse
import json
from pathlib import Path

from build_forest_wang_companion import (COLUMNS, MASKS, TILE, png_bytes,
                                         pixels_for_cell, tiled_mask,
                                         figure8_footprint)
from validate_scene_sheet import read_png


VOID_ID = 21
SEWER_ID = 22
PLAIN_BRICK_ID = 23


def wall_pixel(mask: int, x: int, y: int,
               street: tuple[tuple[int, ...], ...],
               walls: dict[str, tuple[tuple[int, ...], ...]]) -> tuple[int, ...]:
    index = y * TILE + x
    north, east, south, west = (not mask & bit for bit in (1, 4, 16, 64))
    # A diagonal hole needs a full corner, facing the same way as the room's
    # outer corner. The missing diagonal is opposite that visible corner.
    if not (north or east or south or west):
        for bit, role in ((8, "NW"), (32, "NE"),
                          (2, "SW"), (128, "SE")):
            if not mask & bit:
                return walls[role][index]
    for side_a, side_b, role in (
        (north, west, "NW"), (north, east, "NE"),
        (south, west, "SW"), (south, east, "SE"),
    ):
        if side_a and side_b:
            return walls[role][index]
    for absent, role in ((north, "N"), (east, "E"),
                         (south, "S"), (west, "W")):
        if absent:
            return walls[role][index]
    return street[index]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene_sheet", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    _, rows, channels = read_png(args.scene_sheet, TILE, TILE, True)
    if channels != 4:
        raise ValueError("Street Scene Sheet must be RGBA")
    street = pixels_for_cell(rows, channels, 3, 3)
    sewer = pixels_for_cell(rows, channels, 16, 8)
    walls = {
        role: pixels_for_cell(rows, channels, x, y)
        for role, (x, y) in {
            "N": (4, 0), "E": (10, 3), "S": (4, 8), "W": (1, 3),
            "NW": (1, 0), "NE": (10, 0), "SW": (1, 8), "SE": (10, 8),
        }.items()
    }
    plain_brick = walls["N"]
    if street == sewer or street == plain_brick:
        raise ValueError("Street, sewer, and wall cells must differ")
    required = sorted({tiled_mask(x, y) for y in range(14) for x in range(28)
                       if figure8_footprint(x, y)})
    missing = set(required) - set(MASKS)
    if missing:
        raise ValueError(f"Figure 8 needs missing masks: {sorted(missing)}")

    def pixel(sheet_x: int, sheet_y: int) -> tuple[int, ...]:
        tile_id = sheet_y // TILE * COLUMNS + sheet_x // TILE
        x, y = sheet_x % TILE, sheet_y % TILE
        if tile_id < len(MASKS):
            return wall_pixel(MASKS[tile_id], x, y, street, walls)
        if tile_id == VOID_ID:
            return 0, 0, 0, 255
        if tile_id == SEWER_ID:
            return sewer[y * TILE + x]
        return plain_brick[y * TILE + x]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "tiles.png").write_bytes(png_bytes(96, 64, pixel))
    key = {
        "theme": "Retro Street",
        "source_scene_sheet": str(args.scene_sheet),
        "authored_by": "Codex",
        "authored_date": "2026-10-08",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 4,
        "wang_set": "Walled streets",
        "wang_color": "Walkable street",
        "wang_type": "mixed",
        "painted_direction": "walkable cobblestone footprint enclosed by brick walls",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "figure8_required_masks": required,
        "tiles": [
            {"local_id": i, "mask": mask,
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "excluded_tiles": {
            "21": "solid black void",
            "22": "dark dirty blue sewer",
            "23": "uniform brick top wall for the basic sample",
        },
        "street_source_cell": [3, 3],
        "sewer_source_cell": [16, 8],
        "plain_brick_source_cell": [4, 0],
        "room_wall_source_cells": {
            "N": [4, 0], "E": [10, 3], "S": [4, 8], "W": [1, 3],
            "NW": [1, 0], "NE": [10, 0], "SW": [1, 8], "SE": [10, 8],
        },
        "corner_equivalences": {
            "inner_NW": "outer_NW", "inner_NE": "outer_NE",
            "inner_SW": "outer_SW", "inner_SE": "outer_SE",
        },
        "bridge_join_overlays": [
            {"cell": [11, 5], "corner": "SW", "local_id": 0},
            {"cell": [16, 5], "corner": "SE", "local_id": 9},
            {"cell": [11, 8], "corner": "NW", "local_id": 1},
            {"cell": [16, 8], "corner": "NE", "local_id": 4},
        ],
    }
    (args.output_dir / "mapping.json").write_text(
        json.dumps(key, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {args.output_dir / 'tiles.png'} and mapping.json")


if __name__ == "__main__":
    main()
