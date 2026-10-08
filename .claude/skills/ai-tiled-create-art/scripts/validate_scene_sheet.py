"""Check Scene Sheet 24x10 PNG geometry and optional exact cell repetition."""

import argparse
from pathlib import Path
import struct
import sys
import zlib


def read_png(path: Path, tile_width: int, tile_height: int, decode: bool):
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("file is not a PNG")
    if data[12:16] != b"IHDR" or struct.unpack(">I", data[8:12])[0] != 13:
        raise ValueError("PNG has no standard IHDR")
    expected_crc = struct.unpack(">I", data[29:33])[0]
    actual_crc = zlib.crc32(data[12:29]) & 0xFFFFFFFF
    if actual_crc != expected_crc:
        raise ValueError("PNG IHDR checksum failed")
    width, height, depth, color, compression, filter_method, interlace = struct.unpack(
        ">IIBBBBB", data[16:29]
    )
    if (width, height) != (24 * tile_width, 10 * tile_height):
        raise ValueError(
            f"got {width}x{height}; expected {24 * tile_width}x{10 * tile_height}"
        )
    if depth != 8 or color not in (2, 6):
        raise ValueError("expected 8-bit RGB or RGBA PNG")
    if compression or filter_method or interlace:
        raise ValueError("expected a non-interlaced standard PNG")
    mode = "RGBA" if color == 6 else "RGB"
    summary = (
        f"scene-sheet-24x10-v1: {width}x{height}, 24x10 cells at "
        f"{tile_width}x{tile_height}, {mode}"
    )
    if not decode:
        return summary, None, 4 if color == 6 else 3

    channels = 4 if color == 6 else 3
    stride = width * channels
    expected = height * (stride + 1)
    if expected > 128_000_000:
        raise ValueError("PNG is too large for repeat-cell validation")
    offset = 8
    idat = []
    found_end = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG chunk")
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        claimed_crc = struct.unpack(">I", data[offset + 8 + length:end])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != claimed_crc:
            raise ValueError(f"PNG {kind.decode('ascii', 'replace')} checksum failed")
        if kind == b"IDAT":
            idat.append(payload)
        if kind == b"IEND":
            found_end = True
            break
        offset = end
    if not idat or not found_end:
        raise ValueError("PNG image data is incomplete")
    decoder = zlib.decompressobj()
    raw = decoder.decompress(b"".join(idat), expected + 1)
    if len(raw) != expected or not decoder.eof:
        raise ValueError("PNG pixel data has the wrong length")

    rows = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        current = bytearray(raw[offset + 1:offset + stride + 1])
        offset += stride + 1
        if filter_type > 4:
            raise ValueError(f"unsupported PNG filter {filter_type}")
        for i in range(stride):
            left = current[i - channels] if i >= channels else 0
            above = previous[i]
            upper_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                p = left + above - upper_left
                distances = (abs(p - left), abs(p - above), abs(p - upper_left))
                predictor = (left, above, upper_left)[distances.index(min(distances))]
            else:
                predictor = 0
            current[i] = (current[i] + predictor) & 255
        rows.append(bytes(current))
        previous = current
    return summary, rows, channels


def parse_cells(value: str) -> list[tuple[int, int]]:
    cells = []
    for pair in value.split(";"):
        try:
            x, y = (int(n) for n in pair.split(","))
        except ValueError as exc:
            raise ValueError(f"invalid cell coordinate {pair!r}") from exc
        if not 0 <= x < 24 or not 0 <= y < 10:
            raise ValueError(f"cell coordinate outside 24x10 grid: {x},{y}")
        cells.append((x, y))
    if len(set(cells)) < 2:
        raise ValueError("repeat check needs at least two distinct cells")
    return cells


def cell_bytes(rows, x: int, y: int, tile_width: int, tile_height: int,
               channels: int) -> bytes:
    start = x * tile_width * channels
    stop = (x + 1) * tile_width * channels
    return b"".join(row[start:stop]
                    for row in rows[y * tile_height:(y + 1) * tile_height])


def validate(path: Path, tile_width: int, tile_height: int,
             repeat_cells: list[tuple[int, int]] | None = None) -> str:
    summary, rows, channels = read_png(path, tile_width, tile_height,
                                       bool(repeat_cells))
    if repeat_cells:
        x0, y0 = repeat_cells[0]
        expected = cell_bytes(rows, x0, y0, tile_width, tile_height, channels)
        for x, y in repeat_cells[1:]:
            actual = cell_bytes(rows, x, y, tile_width, tile_height, channels)
            if actual != expected:
                raise ValueError(f"cell {x},{y} differs from {x0},{y0}")
        summary += f"; {len(repeat_cells)} repeat cells match exactly"
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--tile", default="16x16", help="cell size, e.g. 16x16")
    parser.add_argument(
        "--repeat-cells",
        help="semicolon-separated clear cells that must match, e.g. '3,3;4,3;3,4'",
    )
    args = parser.parse_args()
    try:
        tile_width, tile_height = (int(n) for n in args.tile.lower().split("x"))
        if tile_width <= 0 or tile_height <= 0:
            raise ValueError("tile dimensions must be positive")
        cells = parse_cells(args.repeat_cells) if args.repeat_cells else None
        print(validate(args.image, tile_width, tile_height, cells))
    except (OSError, ValueError) as exc:
        print(f"invalid Scene Sheet: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
