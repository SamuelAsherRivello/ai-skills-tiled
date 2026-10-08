"""One-time repackaging of the PR gallery from existing local source art."""

from __future__ import annotations

import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt


SOURCE = Path(__file__).resolve().parents[1]
TARGET = Path(sys.argv[1]).resolve()
EXAMPLES = TARGET / "documentation/examples"
REFERENCE = SOURCE / "skills/tiled-ai-create-tileset-png/references/scene-sheet-layout-reference.png"
SCENES = SOURCE / "documentation/art-formats/scene-sheet-24x10"

ITEMS = [
    ("01-mossy-retro-dungeon", "Mossy Retro Dungeon", 16, "mossy blue-gray retro dungeon", SCENES / "retro-dungeon.png", "Existing Retro Dungeon scene sheet and live-checked Figure 8 Wang companion. The reference layout came from user-supplied art; original creator and license were not provided."),
    ("02-fenced-forest-clearing", "Fenced Forest Clearing", 16, "picket fenced forest clearing", SCENES / "retro-forest.png", "Existing Retro Forest scene sheet and live-checked Figure 8 Wang companion. The layout derives from user-supplied art; original creator and license were not provided."),
    ("03-rainwashed-brick-street", "Rainwashed Brick Street", 16, "rainwashed retro brick street", SCENES / "retro-street.png", "Existing Retro Street scene sheet and corrected live-checked Figure 8 Wang companion. See the source notes under documentation/art-formats/scene-sheet-24x10/retro-street."),
    ("04-painted-moss-river", "Painted Moss River", 64, "painted moss river clearings", SOURCE / "output/painted-moss-river-blue-grey-scene-64x64.png", "Existing painted moss river scene and Wang companion from the open dungeon chat. Its original 50×50 Figure 8 was painted and checked through Tiled; see the source verification.md."),
    ("05-robotic-coolant-facility", "Robotic Coolant Facility", 64, "robotic steel coolant facility", SCENES / "space-tech-robot.png", "Existing Space Tech Robot scene and Wang companion from the open robot chat. A user-supplied robot screenshot inspired its palette; original creator and license were not provided."),
    ("06-sunlit-desert-oasis", "Sunlit Desert Oasis", 32, "sunlit sandstone desert oasis", None, "Original generated material swatches were composed into the reference layout for this gallery. The companion covers the 21 Figure 8 masks; the packaged map was opened in Tiled, but was not terrain-painted live."),
    ("07-snowbound-pine-village", "Snowbound Pine Village", 32, "snowbound timber pine village", None, "Original generated material swatches were composed into the reference layout for this gallery. The companion covers the 21 Figure 8 masks; the packaged map was opened in Tiled, but was not terrain-painted live."),
    ("08-volcanic-basalt-keep", "Volcanic Basalt Keep", 32, "volcanic basalt lava keep", None, "Original generated material swatches were composed into the reference layout for this gallery. The companion covers the 21 Figure 8 masks; the packaged map was opened in Tiled, but was not terrain-painted live."),
    ("09-coral-sunken-temple", "Coral Sunken Temple", 32, "coral sunken sea temple", None, "Original generated material swatches were composed into the reference layout for this gallery. The companion covers the 21 Figure 8 masks; the packaged map was opened in Tiled, but was not terrain-painted live."),
    ("10-indigo-crystal-dungeon", "Indigo Crystal Dungeon", 64, "indigo crystal dungeon", SOURCE / "output/indigo-dungeon-scene-64x64.png", "Existing Indigo Dungeon scene and Wang companion from the open dungeon chat. Its original 50×50 Figure 8 was painted and checked through Tiled."),
]


def exact_alpha(tile: int) -> np.ndarray:
    with Image.open(REFERENCE) as source:
        image = source.convert("RGBA").resize((24 * tile, 10 * tile), Image.Resampling.NEAREST)
    return np.asarray(image)[:, :, 3]


def normalize_scene(path: Path, tile: int) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("RGBA")
    assert image.size == (24 * tile, 10 * tile), (path, image.size)
    pixels = np.asarray(image).copy()
    alpha = exact_alpha(tile)
    mask = alpha > 0
    opaque = pixels[:, :, 3] > 0
    if not opaque.all():
        nearest = distance_transform_edt(~opaque, return_distances=False, return_indices=True)
        missing = mask & ~opaque
        pixels[missing, :3] = pixels[nearest[0][missing], nearest[1][missing], :3]
    pixels[:, :, 3] = alpha
    return Image.fromarray(pixels, "RGBA")


def scene_from_swatches(path: Path, tile: int) -> Image.Image:
    with Image.open(path) as original:
        swatches = original.convert("RGBA")
    width, height = swatches.size
    patches = []
    for qx, qy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        cx = qx * width // 2 + width // 4
        cy = qy * height // 2 + height // 4
        radius = min(96, width // 6, height // 6)
        crop = swatches.crop((cx-radius, cy-radius, cx+radius, cy+radius))
        patches.append(np.asarray(crop.resize((tile, tile), Image.Resampling.NEAREST))[:, :, :3])
    with Image.open(REFERENCE) as original:
        template = np.asarray(original.convert("RGBA").resize((24*tile, 10*tile), Image.Resampling.NEAREST))
    yy, xx = np.indices((10*tile, 24*tile))
    cols, rows = xx // tile, yy // tile
    # Preserve the reference's region placement, stair bands, wall cap/face
    # shading, liquid footprint, and all detached supports.
    region = np.full((10*tile, 24*tile), 1, dtype=np.uint8)
    region[(cols >= 2) & (cols <= 9) & (rows >= 2) & (rows <= 7)] = 0
    region[(cols >= 14) & (cols <= 22) & (rows >= 7)] = 2
    stairs = (cols >= 12) & (cols <= 13) & (rows >= 6)
    region[stairs] = 1
    scene = np.zeros_like(template)
    for index, patch in enumerate(patches):
        selected = region == index
        scene[selected, :3] = patch[yy[selected] % tile, xx[selected] % tile]
    # Lightness from the reference gives steps and wall faces visible depth.
    luminance = template[:, :, :3].astype(np.float32).mean(axis=2)
    factor = np.clip(0.72 + luminance / 310, 0.68, 1.12)
    scene[:, :, :3] = np.clip(scene[:, :, :3].astype(np.float32) * factor[:, :, None], 0, 255).astype(np.uint8)
    stair_phase = (yy % tile) // max(1, tile // 4)
    stair_factor = np.where(stair_phase == 0, 0.88, np.where(stair_phase == 1, 0.54, 0.67))
    scene[stairs, :3] = np.clip(scene[stairs, :3].astype(np.float32) * stair_factor[stairs, None], 0, 255).astype(np.uint8)
    scene[:, :, 3] = template[:, :, 3]
    return Image.fromarray(scene, "RGBA")


def package_old_companion(slug: str, image: Path, tsx: Path) -> None:
    folder = EXAMPLES / slug / "output"
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image, folder / "tiles.png")
    tree = ET.parse(tsx)
    root = tree.getroot()
    root.find("image").set("source", "tiles.png")
    ET.indent(root, space=" ")
    tree.write(folder / "tiles.tsx", encoding="utf-8", xml_declaration=True)
    build_map_and_preview(folder)


NEIGHBORS = ((0, -1), (1, -1), (1, 0), (1, 1),
             (0, 1), (-1, 1), (-1, 0), (-1, -1))


def footprint(x: int, y: int) -> bool:
    left = 2 <= x < 12 and 2 <= y < 12
    right = 16 <= x < 26 and 2 <= y < 12
    bridge = 12 <= x < 16 and 5 <= y < 9
    core = 19 <= x < 23 and 5 <= y < 9
    return (left or right or bridge) and not core


def build_map_and_preview(folder: Path) -> None:
    tileset = ET.parse(folder / "tiles.tsx").getroot()
    tile = int(tileset.get("tilewidth"))
    columns = int(tileset.get("columns"))
    wangset = tileset.find("wangsets/wangset")
    assert wangset is not None and wangset.get("type") == "mixed"
    masks = {}
    for item in wangset.findall("wangtile"):
        mask = sum(int(bit) << i for i, bit in enumerate(item.get("wangid").split(",")))
        masks[mask] = int(item.get("tileid"))
    assert len(masks) >= 21
    required = {sum((1 << i) for i, (dx, dy) in enumerate(NEIGHBORS) if footprint(x+dx, y+dy))
                for y in range(14) for x in range(28) if footprint(x,y)}
    assert required <= masks.keys(), (folder, required - masks.keys())
    floor_id = 21 if int(tileset.get("tilecount")) == 25 else 22
    floor = [[floor_id for _ in range(28)] for _ in range(14)]
    walls = [[masks[sum((1 << i) for i, (dx,dy) in enumerate(NEIGHBORS)
                         if footprint(x+dx,y+dy))] + 1 if footprint(x,y) else 0
              for x in range(28)] for y in range(14)]
    root = ET.Element("map", version="1.10", tiledversion="1.12.2", orientation="orthogonal",
                      renderorder="right-down", width="28", height="14", tilewidth=str(tile),
                      tileheight=str(tile), infinite="0", nextlayerid="4", nextobjectid="1")
    ET.SubElement(root, "tileset", firstgid="1", source="tiles.tsx")
    for lid, name, rows in ((1,"Floor",floor),(2,"Walls",walls)):
        layer = ET.SubElement(root,"layer",id=str(lid),name=name,width="28",height="14")
        ET.SubElement(layer,"data",encoding="csv").text = "\n" + ",\n".join(",".join(map(str,row)) for row in rows) + "\n"
    ET.SubElement(root,"objectgroup",id="3",name="Objects")
    ET.indent(root,space=" ")
    ET.ElementTree(root).write(folder/"level.tmx",encoding="utf-8",xml_declaration=True)
    with Image.open(folder/"tiles.png") as original:
        atlas = original.convert("RGBA")
    canvas = Image.new("RGBA",(28*tile,14*tile))
    for rows in (floor,walls):
        for y,row in enumerate(rows):
            for x,gid in enumerate(row):
                if gid:
                    i=gid-1
                    cell=atlas.crop(((i%columns)*tile,(i//columns)*tile,((i%columns)+1)*tile,((i//columns)+1)*tile))
                    canvas.alpha_composite(cell,(x*tile,y*tile))
    canvas.resize((28*32,14*32),Image.Resampling.NEAREST).save(folder/"preview.png")


def write_docs() -> None:
    table = ["[Back to README.md](../README.md)", "", "# Tiled Wang Examples", "",
             "Ten examples using the `tileset-layout-wang-mixed` scene layout. Every tileset thumbnail is a 24×10 scene sheet; each example also includes a separate Mixed Wang companion, external TSX, and portable Figure 8 TMX map. The 24×10 scene sheet is composed artwork and has no Wang assignments itself. Open the map using the companion assets kept beside it.", "",
             "| Name | Grid | Layout | Tileset PNG | Sample level PNG |", "|---|---|---|---|---|"]
    for slug,title,tile,theme,source,provenance in ITEMS:
        folder=EXAMPLES/slug
        prompt=(f"$tiled-ai-create-art Create a {tile}x{tile} scene sheet in layout tileset-layout-wang-mixed "
                f"with the theme {theme}. Keep the exact 24x10 reference silhouette, interior room, exterior assembly, "
                "detached supports, stairs, liquid, and transparent gaps. Then make a separate Mixed Wang companion "
                "and a 28x14 Figure 8 sample level with a 4x4 unwalkable core.")
        (folder/"input").mkdir(parents=True,exist_ok=True)
        (folder/"input/prompt.txt").write_text(prompt+"\n",encoding="utf-8")
        source_line=("[Original scene source](input/scene-source.png) is included. " if source else
                     "[Original generated material swatches](input/source.png) are included. ")
        doc=(f"# {title}\n\nGrid: **{tile}×{tile}**. Layout: **`tileset-layout-wang-mixed`**. Wang type: **mixed**.\n\n"
             f"## Try this prompt\n\n```text\n{prompt}\n```\n\n"
             "## Wang results\n\n| 24×10 scene sheet PNG | Sample level PNG |\n|---|---|\n"
             f"| ![{title} scene sheet](output/scene-sheet.png) | ![{title} Wang sample level](output/preview.png) |\n\n"
             "The [Wang companion PNG](output/tiles.png), [external TSX](output/tiles.tsx), and [TMX map](output/level.tmx) stay together in `output/`. "
             "Open the TMX in Tiled with all three files present. The scene sheet follows the 24×10 composition; the companion contains the actual Wang assignments.\n\n"
             f"{source_line}{provenance}\n\n"
             "The Mixed Wang companion includes the masks required for this Figure 8. This example does not establish arbitrary shape support.\n")
        (folder/"README.md").write_text(doc,encoding="utf-8")
        row=(f"| [{title}](examples/{slug}/README.md) | {tile}×{tile} | `tileset-layout-wang-mixed` | "
             f"<a href=\"examples/{slug}/output/scene-sheet.png\"><img src=\"examples/{slug}/output/scene-sheet.png\" width=\"240\" alt=\"{title} 24 by 10 scene sheet\" /></a> | "
             f"<a href=\"examples/{slug}/output/preview.png\"><img src=\"examples/{slug}/output/preview.png\" width=\"160\" alt=\"{title} Wang sample level\" /></a> |")
        table.append(row)
    table += ["", "## Prompts", "", "Each example page contains its full prompt and source notes. The layout reference is included as [layout-reference.png](examples/layout-reference.png).", "", "## Verification scope", "", "The 16×16 Retro Dungeon, Forest, and Street Wang sources and the 64×64 Painted Moss River and Indigo Dungeon sources had live Figure 8 terrain checks in their original sessions. The 64×64 Robot Wang source had a live check in its original session. The 32×32 companion maps were assembled from generated swatches and inspected in Tiled; they were not live terrain-painted. Each packaged map was generated or copied with local TSX and PNG references. A scene sheet alone is not a Wang tileset.", ""]
    (TARGET/"documentation/examples-readme.md").write_text("\n".join(table),encoding="utf-8")


def main() -> None:
    assert (TARGET/".git").exists(), TARGET
    shutil.copy2(REFERENCE, EXAMPLES/"layout-reference.png")
    for slug,title,tile,theme,source,provenance in ITEMS:
        folder=EXAMPLES/slug
        (folder/"input").mkdir(parents=True,exist_ok=True)
        (folder/"output").mkdir(parents=True,exist_ok=True)
        if source:
            shutil.copy2(source,folder/"input/scene-source.png")
            scene=normalize_scene(source,tile)
        else:
            scene=scene_from_swatches(folder/"input/source.png",tile)
        scene.save(folder/"output/scene-sheet.png")
        assert np.array_equal(np.asarray(scene)[:,:,3],exact_alpha(tile))
    package_old_companion("04-painted-moss-river", SOURCE/"output/painted-moss-river-blue-grey-64/tiles.png",
                          SOURCE/"output/painted-moss-river-blue-grey-64/slate-clearings.tsx")
    package_old_companion("10-indigo-crystal-dungeon", SOURCE/"output/indigo-dungeon-wang/tiles.png",
                          SOURCE/"output/indigo-dungeon-wang/output/indigo-dungeon-wang.tsx")
    write_docs()
    print("Wrote ten exact-mask 24x10 scene sheets and Wang gallery docs")


if __name__ == "__main__":
    main()
