"""Build a self-contained Figure 8 Wang autotiling example without Tiled."""

from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib


ROOT = Path(__file__).resolve().parents[1] / "documentation/examples/figure-8-autotiling"
OUTPUT = ROOT / "output"
TILE = 32
WIDTH, HEIGHT = 28, 14
MASKS = (
    7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
    207, 223, 231, 241, 243, 247, 249, 252, 253, 255,
)
VOID_ID = len(MASKS)
MASK_TO_ID = {mask: index for index, mask in enumerate(MASKS)}
NEIGHBORS = ((0, -1), (1, -1), (1, 0), (1, 1),
             (0, 1), (-1, 1), (-1, 0), (-1, -1))


def chunk(kind, payload):
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def png_bytes(width, height, pixel):
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            rows.extend(pixel(x, y))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
            + chunk(b"IEND", b""))


def floor_at(mask, x, y):
    """Interpolate the eight Wang samples and a filled tile center."""
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


def tile_pixel(tile_id, x, y):
    grain = ((x * 17 + y * 31 + x * y * 3) % 13) - 6
    if tile_id >= VOID_ID:
        shade = 31 + grain // 2 + (4 if (x // 8 + y // 8) % 2 else 0)
        return shade, shade + 7, shade + 13, 255
    mask = MASKS[tile_id]
    if floor_at(mask, x, y):
        # Small, deterministic stone flecks make the full-floor tile readable.
        fleck = 10 if (x * 11 + y * 7 + mask) % 43 == 0 else 0
        return 183 + grain + fleck, 151 + grain + fleck, 105 + grain // 2 + fleck, 255
    near_floor = any(
        0 <= x + dx < TILE and 0 <= y + dy < TILE
        and floor_at(mask, x + dx, y + dy)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0),
                       (0, -2), (2, 0), (0, 2), (-2, 0))
    )
    if near_floor:
        return 122 + grain, 119 + grain, 108 + grain, 255
    return 65 + grain, 72 + grain, 77 + grain, 255


def footprint(x, y):
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def mask_at(x, y):
    return sum(1 << bit for bit, (dx, dy) in enumerate(NEIGHBORS)
               if footprint(x + dx, y + dy))


def csv_layer(rows):
    return "\n".join(",".join(str(value) for value in row)
                     + ("," if i < len(rows) - 1 else "")
                     for i, row in enumerate(rows))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    unsupported = {mask_at(x, y) for y in range(HEIGHT) for x in range(WIDTH)
                   if footprint(x, y)} - MASK_TO_ID.keys()
    if unsupported:
        raise ValueError(f"Figure 8 requires unsupported Wang masks: {sorted(unsupported)}")

    image = png_bytes(6 * TILE, 4 * TILE,
                      lambda x, y: tile_pixel((y // TILE) * 6 + x // TILE,
                                              x % TILE, y % TILE))
    (OUTPUT / "tiles.png").write_bytes(image)

    floor = [[VOID_ID + 1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    walls = [[(MASK_TO_ID[mask_at(x, y)] + 1) if footprint(x, y)
              else (VOID_ID + 1 if 19 <= x < 23 and 5 <= y < 9 else 0)
              for x in range(WIDTH)] for y in range(HEIGHT)]
    preview = png_bytes(WIDTH * TILE, HEIGHT * TILE,
                        lambda x, y: tile_pixel((walls[y // TILE][x // TILE] or
                                                  floor[y // TILE][x // TILE]) - 1,
                                                 x % TILE, y % TILE))
    (OUTPUT / "preview.png").write_bytes(preview)

    tileset = ET.Element("tileset", version="1.10", tiledversion="1.12.2",
                         name="figure-8-stone", tilewidth=str(TILE),
                         tileheight=str(TILE), tilecount="24", columns="6")
    ET.SubElement(tileset, "image", source="tiles.png", width=str(6 * TILE),
                  height=str(4 * TILE))
    sets = ET.SubElement(tileset, "wangsets")
    wang = ET.SubElement(sets, "wangset", name="Walkable rooms", type="mixed",
                         tile=str(MASK_TO_ID[255]))
    ET.SubElement(wang, "wangcolor", name="Walkable floor", color="#b79769",
                  tile=str(MASK_TO_ID[255]), probability="1")
    for tile_id, mask in enumerate(MASKS):
        ET.SubElement(wang, "wangtile", tileid=str(tile_id),
                      wangid=",".join(str((mask >> bit) & 1) for bit in range(8)))
    ET.indent(tileset, space=" ")
    ET.ElementTree(tileset).write(OUTPUT / "tiles.tsx", encoding="utf-8",
                                   xml_declaration=True)

    map_root = ET.Element("map", version="1.10", tiledversion="1.12.2",
                          orientation="orthogonal", renderorder="right-down",
                          width=str(WIDTH), height=str(HEIGHT),
                          tilewidth=str(TILE), tileheight=str(TILE),
                          infinite="0", nextlayerid="4", nextobjectid="1")
    ET.SubElement(map_root, "tileset", firstgid="1", source="tiles.tsx")
    for layer_id, name, rows in ((1, "Floor", floor), (2, "Walls", walls)):
        layer = ET.SubElement(map_root, "layer", id=str(layer_id), name=name,
                              width=str(WIDTH), height=str(HEIGHT))
        ET.SubElement(layer, "data", encoding="csv").text = "\n" + csv_layer(rows) + "\n"
    ET.SubElement(map_root, "objectgroup", id="3", name="Objects")
    ET.indent(map_root, space=" ")
    ET.ElementTree(map_root).write(OUTPUT / "figure-8.tmx", encoding="utf-8",
                                   xml_declaration=True)
    print("Built Figure 8 TMX, Wang TSX, tile art, and preview.")


if __name__ == "__main__":
    main()
