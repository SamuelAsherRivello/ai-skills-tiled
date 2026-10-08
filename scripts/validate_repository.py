"""Check repository links and portable Tiled examples."""
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def local_target(doc, target):
    if target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return
    path = target.split("#", 1)[0]
    if not path:
        return
    resolved = (doc.parent / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.exists():
        ERRORS.append(f"{doc.relative_to(ROOT)}: missing or nonportable {target}")


for doc in [ROOT / "README.md", ROOT / "CONTRIBUTING.md", *ROOT.glob("documentation/**/*.md"),
            *ROOT.glob(".codex/*.md"), *ROOT.glob(".claude/*.md")]:
    text = doc.read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+)\)", text):
        local_target(doc, link)
    for src in re.findall(r"<img[^>]+src=[\"']([^\"']+)", text):
        local_target(doc, src)

output = ROOT / "documentation/examples/starter-map/output"
tmx = ET.parse(output / "starter-map.tmx").getroot()
tsx_path = output / tmx.find("tileset").attrib["source"]
if not tsx_path.is_file():
    ERRORS.append("starter map external tileset is missing")
else:
    tsx = ET.parse(tsx_path).getroot()
    image_path = tsx_path.parent / tsx.find("image").attrib["source"]
    if not image_path.is_file():
        ERRORS.append("starter tileset image is missing")
    gids = [int(value) for value in re.findall(r"\d+", tmx.find("layer/data").text or "")]
    size = int(tmx.attrib["width"]) * int(tmx.attrib["height"])
    if len(gids) != size or max(gids, default=0) > int(tsx.attrib["tilecount"]):
        ERRORS.append("starter map tile layer has an invalid cell count or tile ID")
    for path, expected in [(image_path, (64, 16)), (output / "preview.png", (160, 128))]:
        data = path.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", data[16:24]) != expected:
            ERRORS.append(f"invalid PNG dimensions: {path.name}")

figure_output = ROOT / "documentation/examples/figure-8-autotiling/output"
figure_map = ET.parse(figure_output / "figure-8.tmx").getroot()
figure_tsx_path = figure_output / figure_map.find("tileset").attrib["source"]
figure_tsx = ET.parse(figure_tsx_path).getroot()
figure_image = figure_tsx_path.parent / figure_tsx.find("image").attrib["source"]
for path, expected in [(figure_image, (192, 128)),
                       (figure_output / "preview.png", (896, 448))]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", data[16:24]) != expected:
        ERRORS.append(f"invalid Figure 8 PNG dimensions: {path.name}")

layers = list(figure_map)
layers = [node for node in layers if node.tag in ("layer", "objectgroup")]
if [(node.tag, node.attrib["name"]) for node in layers] != [
    ("layer", "Floor"), ("layer", "Walls"), ("objectgroup", "Objects")
]:
    ERRORS.append("Figure 8 layers are not Floor, Walls, Objects")
else:
    width, height = int(figure_map.attrib["width"]), int(figure_map.attrib["height"])
    cells = []
    for layer in layers[:2]:
        values = [int(value) for value in re.findall(r"\d+", layer.find("data").text or "")]
        if len(values) != width * height or max(values, default=0) > int(figure_tsx.attrib["tilecount"]):
            ERRORS.append(f"invalid Figure 8 {layer.attrib['name']} cells")
        cells.append(values)
    floor, walls = cells
    void_gid = 22
    if any(gid != void_gid for gid in floor):
        ERRORS.append("Figure 8 Floor is not a repeated void tile")
    wang = figure_tsx.find("wangsets/wangset")
    if wang is None or wang.attrib.get("type") != "mixed":
        ERRORS.append("Figure 8 mixed Wang set is missing")
    else:
        assignments = {
            int(node.attrib["tileid"]): tuple(int(value) for value in node.attrib["wangid"].split(","))
            for node in wang.findall("wangtile")
        }
        if len(assignments) != 21 or len(wang.findall("wangcolor")) != 1:
            ERRORS.append("Figure 8 Wang assignments or color are incomplete")
        offsets = ((0, -1), (1, -1), (1, 0), (1, 1),
                   (0, 1), (-1, 1), (-1, 0), (-1, -1))
        painted = {(x, y) for y in range(height) for x in range(width)
                   if walls[y * width + x] not in (0, void_gid)}
        if len(painted) != 200 or len([gid for gid in walls if gid == void_gid]) != 16:
            ERRORS.append("Figure 8 footprint or core has the wrong size")
        used_ids = set()
        for x, y in painted:
            tile_id = walls[y * width + x] - 1
            expected = tuple(int((x + dx, y + dy) in painted) for dx, dy in offsets)
            if assignments.get(tile_id) != expected:
                ERRORS.append(f"Figure 8 Wang mismatch at ({x}, {y})")
            used_ids.add(tile_id)
        if used_ids != assignments.keys():
            ERRORS.append("Figure 8 has unused or missing Wang masks")
    if list(layers[2]):
        ERRORS.append("Figure 8 Objects layer is not empty")

print("\n".join(ERRORS) if ERRORS else "Repository links and Tiled examples are valid.")
sys.exit(bool(ERRORS))
