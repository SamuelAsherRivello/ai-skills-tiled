"""Compose a 64px robot-room Wang companion from the approved scene sheet.

This is a limited Mixed set for the documented Figure 8 footprint. Every
visible material is sampled from the approved robot art; the opaque void uses
its opening's dark background colour. The scene sheet is never modified.
"""

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "space-tech-robot.png"
TILE = 64
COLUMNS = 6
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
SOURCE_CELLS = {
    "floor": (3, 3),
    "coolant": (16, 8),
    "N": (4, 0), "E": (10, 3), "S": (4, 8), "W": (1, 3),
    "NW": (1, 0), "NE": (10, 0), "SW": (1, 8), "SE": (10, 8),
}
VOID = (3, 7, 15, 255)


def footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def mask_at(x: int, y: int) -> int:
    n, e, s, w = (footprint(x, y - 1), footprint(x + 1, y),
                  footprint(x, y + 1), footprint(x - 1, y))
    return (n + (n and e and footprint(x + 1, y - 1)) * 2
            + e * 4 + (e and s and footprint(x + 1, y + 1)) * 8
            + s * 16 + (s and w and footprint(x - 1, y + 1)) * 32
            + w * 64 + (w and n and footprint(x - 1, y - 1)) * 128)


def source_cell(image: Image.Image, col: int, row: int) -> Image.Image:
    bounds = (col * TILE, row * TILE, (col + 1) * TILE, (row + 1) * TILE)
    crop = image.crop(bounds)
    opaque = Image.new("RGBA", (TILE, TILE), VOID)
    opaque.alpha_composite(crop)
    return opaque


def role_for_mask(mask: int) -> str:
    n, e, s, w = (not mask & bit for bit in (1, 4, 16, 64))
    # An unpainted diagonal uses the complete matching outer corner art.
    if not (n or e or s or w):
        for bit, role in ((8, "NW"), (32, "NE"), (2, "SW"), (128, "SE")):
            if not mask & bit:
                return role
    for a, b, role in ((n, w, "NW"), (n, e, "NE"),
                       (s, w, "SW"), (s, e, "SE")):
        if a and b:
            return role
    for absent, role in ((n, "N"), (e, "E"), (s, "S"), (w, "W")):
        if absent:
            return role
    return "floor"


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != (1536, 640):
        raise ValueError(f"Expected the approved 1536x640 scene sheet: {source.size}")
    cells = {role: source_cell(source, *location)
             for role, location in SOURCE_CELLS.items()}
    if cells["floor"].tobytes() == cells["coolant"].tobytes():
        raise ValueError("The selected floor and coolant source cells are identical")

    required = sorted({mask_at(x, y) for y in range(14) for x in range(28)
                       if footprint(x, y)})
    missing = set(required) - set(MASKS)
    if missing:
        raise ValueError(f"Figure 8 needs unsupported masks: {sorted(missing)}")

    atlas = Image.new("RGBA", (COLUMNS * TILE, 4 * TILE), VOID)
    for tile_id, mask in enumerate(MASKS):
        atlas.paste(cells[role_for_mask(mask)],
                    ((tile_id % COLUMNS) * TILE, (tile_id // COLUMNS) * TILE))
    void = Image.new("RGBA", (TILE, TILE), VOID)
    atlas.paste(void, (3 * TILE, 3 * TILE))
    atlas.paste(cells["coolant"], (4 * TILE, 3 * TILE))
    atlas.paste(cells["N"], (5 * TILE, 3 * TILE))
    atlas_path = ROOT / "tiles.png"
    atlas.save(atlas_path)

    key = {
        "theme": "Space Tech Robot",
        "source_scene_sheet": str(SOURCE),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "authored_by": "Codex",
        "authored_date": "2026-10-08",
        "tile_width": TILE,
        "tile_height": TILE,
        "columns": COLUMNS,
        "rows": 4,
        "wang_set": "Robot rooms",
        "wang_color": "Walkable steel floor",
        "wang_type": "mixed",
        "painted_direction": "walkable steel room footprint enclosed by robot walls",
        "supported_footprint": "Figure 8 with two 10x10 rooms, a 4-tile bridge, and a 4x4 core",
        "figure8_required_masks": required,
        "tiles": [
            {"local_id": i, "mask": mask,
             "source_role": role_for_mask(mask),
             "wang_id": [(mask >> bit) & 1 for bit in range(8)]}
            for i, mask in enumerate(MASKS)
        ],
        "excluded_tiles": {
            "21": "opaque dark void for the right core",
            "22": "electric blue coolant",
            "23": "plain top wall for the basic sample",
        },
        "source_cells": {role: list(location)
                         for role, location in SOURCE_CELLS.items()},
        "corner_equivalences": {
            "inner_NW": "outer_NW", "inner_NE": "outer_NE",
            "inner_SW": "outer_SW", "inner_SE": "outer_SE",
        },
    }
    (ROOT / "mapping.json").write_text(json.dumps(key, indent=2) + "\n",
                                       encoding="utf-8")
    print(f"Built {atlas_path} with {len(MASKS)} Mixed Wang roles")


if __name__ == "__main__":
    main()
