"""Build a tiny portable Tiled example using only Python's standard library."""
from pathlib import Path
import struct
import zlib


ROOT = Path(__file__).resolve().parents[1] / "documentation/examples/starter-map"
OUTPUT = ROOT / "output"
GRID = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 3, 3, 1, 1, 1, 2],
    [2, 1, 1, 1, 3, 3, 1, 1, 1, 2],
    [2, 1, 1, 1, 3, 3, 1, 4, 1, 2],
    [2, 1, 1, 1, 3, 3, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


def tile(gid, x, y):
    if gid == 1:  # grass
        return (62, 154, 77, 255) if (x * 7 + y * 11) % 19 else (113, 186, 78, 255)
    if gid == 2:  # water
        return (39, 113, 183, 255) if (x + y * 3) % 9 else (94, 181, 219, 255)
    if gid == 3:  # path
        return (195, 151, 89, 255) if (x * 3 + y * 5) % 11 else (160, 117, 70, 255)
    # stone
    return (115, 123, 132, 255) if (y % 8 == 0 or x % 8 == 0) else (157, 165, 169, 255)


def chunk(kind, payload):
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(
        ">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def write_png(path, width, height, pixel):
    scanlines = bytearray()
    for y in range(height):
        scanlines.append(0)
        for x in range(width):
            scanlines.extend(pixel(x, y))
    header = b"\x89PNG\r\n\x1a\n"
    image = chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0))
    image += chunk(b"IDAT", zlib.compress(bytes(scanlines), 9))
    image += chunk(b"IEND", b"")
    path.write_bytes(header + image)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_png(OUTPUT / "tiles.png", 64, 16,
              lambda x, y: tile(x // 16 + 1, x % 16, y))
    write_png(OUTPUT / "preview.png", 160, 128,
              lambda x, y: tile(GRID[y // 16][x // 16], x % 16, y % 16))
    (OUTPUT / "tiles.tsx").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<tileset version="1.10" tiledversion="1.12.2" name="starter-tiles" '
        'tilewidth="16" tileheight="16" tilecount="4" columns="4">\n'
        ' <image source="tiles.png" width="64" height="16"/>\n'
        '</tileset>\n', encoding="utf-8")
    csv = "\n".join(",".join(map(str, row)) + ("," if i < len(GRID) - 1 else "")
                    for i, row in enumerate(GRID))
    (OUTPUT / "starter-map.tmx").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<map version="1.10" tiledversion="1.12.2" orientation="orthogonal" '
        'renderorder="right-down" width="10" height="8" tilewidth="16" '
        'tileheight="16" infinite="0" nextlayerid="3" nextobjectid="2">\n'
        ' <tileset firstgid="1" source="tiles.tsx"/>\n'
        ' <layer id="1" name="Ground" width="10" height="8">\n'
        '  <data encoding="csv">\n' + csv + '\n  </data>\n'
        ' </layer>\n'
        ' <objectgroup id="2" name="Markers">\n'
        '  <object id="1" name="Player Spawn" type="spawn" x="80" y="64">\n'
        '   <point/>\n'
        '  </object>\n'
        ' </objectgroup>\n'
        '</map>\n', encoding="utf-8")
    print("Built starter-map TMX, TSX, tiles PNG, and preview PNG.")


if __name__ == "__main__":
    main()
