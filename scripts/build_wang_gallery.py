"""Package ten portable Figure 8 Wang examples for the documentation gallery.

Existing verified examples are copied without changing their source projects.
Five new 32px companions sample original generated material sheets in each
example's input directory. This script writes portable TMX/TSX files and PNG
previews; editor verification is a separate step.
"""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "documentation/examples"
SCENES = ROOT / "documentation/art-formats/scene-sheet-24x10"
MASKS = (7, 28, 31, 63, 112, 124, 126, 127, 159, 193, 199,
         207, 223, 231, 241, 243, 247, 249, 252, 253, 255)
MASK_TO_ID = {mask: tile_id for tile_id, mask in enumerate(MASKS)}
NEIGHBORS = ((0, -1), (1, -1), (1, 0), (1, 1),
             (0, 1), (-1, 1), (-1, 0), (-1, -1))
SIZE = (28, 14)


def footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def wang_mask(x: int, y: int) -> int:
    return sum(1 << bit for bit, (dx, dy) in enumerate(NEIGHBORS)
               if footprint(x + dx, y + dy))


def csv_layer(rows: list[list[int]]) -> str:
    return "\n" + ",\n".join(",".join(map(str, row)) for row in rows) + "\n"


def write_map(path: Path, tile: int) -> None:
    width, height = SIZE
    root = ET.Element("map", version="1.10", tiledversion="1.12.2",
                      orientation="orthogonal", renderorder="right-down",
                      width=str(width), height=str(height), tilewidth=str(tile),
                      tileheight=str(tile), infinite="0", nextlayerid="4",
                      nextobjectid="1")
    ET.SubElement(root, "tileset", firstgid="1", source="tiles.tsx")
    floor = [[22 for _ in range(width)] for _ in range(height)]
    walls = [[MASK_TO_ID[wang_mask(x, y)] + 1 if footprint(x, y) else 0
              for x in range(width)] for y in range(height)]
    for layer_id, name, rows in ((1, "Floor", floor), (2, "Walls", walls)):
        layer = ET.SubElement(root, "layer", id=str(layer_id), name=name,
                              width=str(width), height=str(height))
        ET.SubElement(layer, "data", encoding="csv").text = csv_layer(rows)
    ET.SubElement(root, "objectgroup", id="3", name="Objects")
    ET.indent(root, space=" ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def rewrite_portable_xml(source: Path, destination: Path, kind: str) -> None:
    tree = ET.parse(source)
    root = tree.getroot()
    if kind == "tsx":
        image = root.find("image")
        assert image is not None
        image.set("source", "tiles.png")
    else:
        tilesets = root.findall("tileset")
        assert len(tilesets) == 1
        tilesets[0].set("source", "tiles.tsx")
    ET.indent(root, space=" ")
    tree.write(destination, encoding="utf-8", xml_declaration=True)


def package_existing(name: str, image: Path, tsx: Path, tmx: Path,
                     preview: Path | None) -> None:
    target = EXAMPLES / name / "output"
    target.mkdir(parents=True, exist_ok=True)
    # The gallery outputs remain self-contained on clones that do not include
    # an older local source project used while the gallery was assembled.
    image = image if image.exists() else target / "tiles.png"
    tsx = tsx if tsx.exists() else target / "tiles.tsx"
    tmx = tmx if tmx.exists() else target / "level.tmx"
    if image.resolve() != (target / "tiles.png").resolve():
        shutil.copyfile(image, target / "tiles.png")
    rewrite_portable_xml(tsx, target / "tiles.tsx", "tsx")
    if preview is None:
        write_map(target / "level.tmx", 64)
        render_preview(target)
    else:
        rewrite_portable_xml(tmx, target / "level.tmx", "tmx")
        preview = preview if preview.exists() else target / "preview.png"
        if preview.resolve() != (target / "preview.png").resolve():
            shutil.copyfile(preview, target / "preview.png")


def material_patch(source: Image.Image, quadrant_x: int,
                   quadrant_y: int, tile: int) -> Image.Image:
    width, height = source.size
    half_x, half_y = width // 2, height // 2
    center_x = quadrant_x * half_x + half_x // 2
    center_y = quadrant_y * half_y + half_y // 2
    radius = min(96, half_x // 3, half_y // 3)
    patch = source.crop((center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius))
    patch = patch.resize((tile, tile), Image.Resampling.NEAREST).convert("RGBA")
    pixels = patch.load()
    # The outer two pixel columns and rows agree, so the repeated base tile
    # has no hard color discontinuity at its own boundary.
    for y in range(tile):
        average = tuple((pixels[0, y][c] + pixels[tile - 1, y][c]) // 2
                        for c in range(4))
        pixels[0, y] = pixels[tile - 1, y] = average
    for x in range(tile):
        average = tuple((pixels[x, 0][c] + pixels[x, tile - 1][c]) // 2
                        for c in range(4))
        pixels[x, 0] = pixels[x, tile - 1] = average
    return patch


def floor_at(mask: int, x: int, y: int, tile: int) -> bool:
    samples = ((bool(mask & 128), bool(mask & 1), bool(mask & 2)),
               (bool(mask & 64), True, bool(mask & 4)),
               (bool(mask & 32), bool(mask & 16), bool(mask & 8)))
    fx = (x + 0.5) * 2 / tile
    fy = (y + 0.5) * 2 / tile
    sx, tx = (0, fx) if fx < 1 else (1, fx - 1)
    sy, ty = (0, fy) if fy < 1 else (1, fy - 1)
    value = (samples[sy][sx] * (1 - tx) * (1 - ty)
             + samples[sy][sx + 1] * tx * (1 - ty)
             + samples[sy + 1][sx] * (1 - tx) * ty
             + samples[sy + 1][sx + 1] * tx * ty)
    return value >= 0.5


def write_tileset(path: Path, tile: int, name: str) -> None:
    root = ET.Element("tileset", version="1.10", tiledversion="1.12.2",
                      name=name, tilewidth=str(tile), tileheight=str(tile),
                      tilecount="24", columns="6")
    ET.SubElement(root, "image", source="tiles.png", width=str(tile * 6),
                  height=str(tile * 4))
    sets = ET.SubElement(root, "wangsets")
    wang = ET.SubElement(sets, "wangset", name="Walkable rooms", type="mixed",
                         tile="20")
    ET.SubElement(wang, "wangcolor", name="Walkable floor", color="#f5d7a0",
                  tile="20", probability="1")
    for tile_id, mask in enumerate(MASKS):
        ET.SubElement(wang, "wangtile", tileid=str(tile_id),
                      wangid=",".join(str((mask >> bit) & 1)
                                      for bit in range(8)))
    ET.indent(root, space=" ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def build_generated(name: str) -> None:
    example = EXAMPLES / name
    target = example / "output"
    target.mkdir(parents=True, exist_ok=True)
    source = Image.open(example / "input/source.png").convert("RGBA")
    tile = 32
    floor = material_patch(source, 0, 0, tile)
    wall = material_patch(source, 1, 0, tile)
    water = material_patch(source, 0, 1, tile)
    void = material_patch(source, 1, 1, tile)
    atlas = Image.new("RGBA", (tile * 6, tile * 4))
    for tile_id, mask in enumerate(MASKS):
        cell = Image.new("RGBA", (tile, tile))
        for y in range(tile):
            for x in range(tile):
                cell.putpixel((x, y), (floor if floor_at(mask, x, y, tile)
                                       else wall).getpixel((x, y)))
        atlas.paste(cell, ((tile_id % 6) * tile, (tile_id // 6) * tile))
    atlas.paste(void, (tile * 3, tile * 3))
    atlas.paste(water, (tile * 4, tile * 3))
    atlas.paste(wall, (tile * 5, tile * 3))
    atlas.save(target / "tiles.png")
    write_tileset(target / "tiles.tsx", tile, name.removeprefix(name[:3]))
    write_map(target / "level.tmx", tile)
    render_preview(target)


def render_preview(target: Path) -> None:
    image = Image.open(target / "tiles.png").convert("RGBA")
    map_root = ET.parse(target / "level.tmx").getroot()
    tile = int(map_root.get("tilewidth"))
    width, height = int(map_root.get("width")), int(map_root.get("height"))
    canvas = Image.new("RGBA", (width * tile, height * tile))
    for layer in map_root.findall("layer"):
        data = layer.find("data")
        assert data is not None and data.get("encoding") == "csv"
        ids = [int(value) for value in (data.text or "").replace("\n", "").split(",")
               if value.strip()]
        assert len(ids) == width * height
        for index, gid in enumerate(ids):
            if gid == 0:
                continue
            local_id = gid - 1
            cell = image.crop(((local_id % 6) * tile, (local_id // 6) * tile,
                               (local_id % 6 + 1) * tile,
                               (local_id // 6 + 1) * tile))
            canvas.alpha_composite(cell, ((index % width) * tile,
                                          (index // width) * tile))
    if tile == 64:
        canvas = canvas.resize((width * 32, height * 32), Image.Resampling.NEAREST)
    canvas.save(target / "preview.png")


GALLERY = (
    ("01-mossy-retro-dungeon", "Mossy Retro Dungeon", 16,
     "retro pixel art, mossy blue-gray dungeon walls and stone floor",
     "Adapted from the existing [Retro Dungeon Wang companion](../../art-formats/scene-sheet-24x10/retro-dungeon-wang/README.md). The underlying visual reference was user supplied; its original creator and license were not provided. The source Figure 8 was previously painted and checked in Tiled."),
    ("02-fenced-forest-clearing", "Fenced Forest Clearing", 16,
     "retro pixel art, grass clearing, picket fence, forest pond",
     "Adapted from the existing [Retro Forest Wang companion](../../art-formats/scene-sheet-24x10/retro-forest-wang/README.md). Its layout derives from user-supplied art whose original creator and license were not provided. The source Figure 8 was previously painted and checked in Tiled."),
    ("03-rainwashed-brick-street", "Rainwashed Brick Street", 16,
     "retro pixel art, red brick walls, cobblestone street, blue sewer",
     "Adapted from the existing [Retro Street Wang companion](../../art-formats/scene-sheet-24x10/retro-street-wang/README.md). The source notes explain its generated concept and composition; the corrected source Figure 8 was previously painted and checked in Tiled."),
    ("04-stone-courtyard-ruins", "Stone Courtyard Ruins", 32,
     "warm stone courtyard tiles, dark ruined boundary, restrained pixel art",
     "Adapted from a local Figure 8 Autotiling fixture built by a repository script. That source was a portable fixture, not a live terrain-painting result."),
    ("05-robotic-coolant-facility", "Robotic Coolant Facility", 64,
     "robotic steel facility, blue coolant, dark panel walls",
     "Uses an existing Space Tech Robot scene sheet and its Wang companion. A user-supplied robot screenshot inspired its palette; its original creator and license were not provided. The compact map and preview were assembled by this gallery builder."),
    ("06-sunlit-desert-oasis", "Sunlit Desert Oasis", 32,
     "sunlit sandstone oasis, carved walls, teal water, pixel art",
     "Original material swatches were generated for this gallery with the built-in image tool. The gallery builder sampled them into a 21-mask Wang companion."),
    ("07-snowbound-pine-village", "Snowbound Pine Village", 32,
     "snowy pine village, timber walls, frozen pond, pixel art",
     "Original material swatches were generated for this gallery with the built-in image tool. The gallery builder sampled them into a 21-mask Wang companion."),
    ("08-volcanic-basalt-keep", "Volcanic Basalt Keep", 32,
     "volcanic basalt keep, ember cracks, lava, pixel art",
     "Original material swatches were generated for this gallery with the built-in image tool. The gallery builder sampled them into a 21-mask Wang companion."),
    ("09-coral-sunken-temple", "Coral Sunken Temple", 32,
     "sunken coral temple, sea-green mosaic, seawater, pixel art",
     "Original material swatches were generated for this gallery with the built-in image tool. The gallery builder sampled them into a 21-mask Wang companion."),
    ("10-glowing-mushroom-grove", "Glowing Mushroom Grove", 32,
     "glowing mushroom grove, violet moss, roots, luminous pool",
     "Original material swatches were generated for this gallery with the built-in image tool. The gallery builder sampled them into a 21-mask Wang companion."),
)


def write_example_docs() -> None:
    for slug, title, tile, theme, provenance in GALLERY:
        example = EXAMPLES / slug
        prompt = (f"$tiled-ai-create-tileset-png Create a grid-safe mixed Wang tileset at "
                  f"{tile}x{tile} with the theme {theme}; then add the tileset "
                  "and Wang terrain in Tiled and make a 28x14 Figure 8 sample "
                  "level with a 4x4 unwalkable core.")
        input_dir = example / "input"
        input_dir.mkdir(parents=True, exist_ok=True)
        (input_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
        source_line = ("\n[Original material swatches](input/source.png) are included.\n"
                       if (input_dir / "source.png").exists() else "")
        content = (f"# {title}\n\n"
                   f"Grid: **{tile}x{tile}**. Wang type: **mixed**. "
                   "Sample: **28x14 Figure 8**.\n\n"
                   "## Try this prompt\n\n"
                   f"```text\n{prompt}\n```\n\n"
                   "## Wang results\n\n"
                   "| Tileset PNG | Sample level PNG |\n"
                   "|---|---|\n"
                   f"| ![{title} Wang tileset](output/tiles.png) "
                   f"| ![{title} Wang sample level](output/preview.png) |\n\n"
                   "[Open the Tiled map](output/level.tmx) with its "
                   "[external tileset](output/tiles.tsx) and "
                   "[local tile image](output/tiles.png). Keep all three "
                   "output files together.\n\n"
                   f"{provenance}{source_line}\n"
                   "The mixed Wang assignments cover the 21 masks used by "
                   "this Figure 8 footprint. The packaged map was opened "
                   "in Tiled and its tileset and assignments were inspected. "
                   "Other terrain shapes have not been paint-tested here.\n")
        (example / "README.md").write_text(content, encoding="utf-8")


def main() -> None:
    package_existing(
        "01-mossy-retro-dungeon",
        SCENES / "retro-dungeon-wang/tiles.png",
        SCENES / "retro-dungeon-wang/output/retro-dungeon-wang.tsx",
        SCENES / "retro-dungeon-wang/output/retro-dungeon-figure-8-wang.tmx",
        SCENES / "retro-dungeon-wang/output/preview.png")
    package_existing(
        "02-fenced-forest-clearing",
        SCENES / "retro-forest-wang/tiles.png",
        SCENES / "retro-forest-wang/output/retro-forest-wang.tsx",
        SCENES / "retro-forest-wang/output/retro-forest-figure-8-wang.tmx",
        SCENES / "retro-forest-wang/output/preview.png")
    package_existing(
        "03-rainwashed-brick-street",
        SCENES / "retro-street-wang/tiles.png",
        SCENES / "retro-street-wang/output/retro-street-wang-corners.tsx",
        SCENES / "retro-street-wang/output/retro-street-figure-8-wang-corners.tmx",
        SCENES / "retro-street-wang/output/preview-corners.png")
    package_existing(
        "04-stone-courtyard-ruins",
        EXAMPLES / "figure-8-autotiling/output/tiles.png",
        EXAMPLES / "figure-8-autotiling/output/tiles.tsx",
        EXAMPLES / "figure-8-autotiling/output/figure-8.tmx",
        EXAMPLES / "figure-8-autotiling/output/preview.png")
    package_existing(
        "05-robotic-coolant-facility",
        SCENES / "space-tech-robot/tiles.png",
        SCENES / "space-tech-robot/wang/output/space-tech-robot-wang.tsx",
        ROOT / "output/tiled-ai-sample-level/space-tech-robot-figure-8-wang.tmx",
        None)
    for name in ("06-sunlit-desert-oasis", "07-snowbound-pine-village",
                 "08-volcanic-basalt-keep", "09-coral-sunken-temple",
                 "10-glowing-mushroom-grove"):
        build_generated(name)
    write_example_docs()
    print("Packaged 10 Wang examples")


if __name__ == "__main__":
    main()
