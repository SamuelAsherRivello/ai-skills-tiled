"""Render the finite orthogonal atlas/tile-layer subset used by gallery bundles.

Reject unsupported visible features instead of silently producing a partial
preview. This is an offline packaging check, not live Tiled verification.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image


def reject_attributes(node: ET.Element, names: tuple[str, ...]) -> None:
    for name in names:
        value = node.get(name)
        allowed = (None, "1", "1.0") if name in ("parallaxx", "parallaxy") else (None, "0", "0.0")
        if value not in allowed:
            raise ValueError(f"Unsupported visible {node.tag} feature: {name}={value}")


def render_bundle(map_path: Path) -> Image.Image:
    """Return a native RGBA composite; paths, IDs and geometry come from XML."""
    map_path = Path(map_path)
    root = ET.parse(map_path).getroot()
    if root.tag != "map" or root.get("orientation") != "orthogonal" or root.get("infinite", "0") != "0":
        raise ValueError("Only finite orthogonal maps are supported")
    if root.get("renderorder", "right-down") != "right-down":
        raise ValueError("Unsupported map render order")
    width, height = int(root.get("width", "0")), int(root.get("height", "0"))
    tw, th = int(root.get("tilewidth", "0")), int(root.get("tileheight", "0"))
    if min(width, height, tw, th) <= 0:
        raise ValueError("Invalid map dimensions")
    refs = root.findall("tileset")
    if len(refs) != 1 or not refs[0].get("source"):
        raise ValueError("Expected exactly one external atlas TSX")
    firstgid = int(refs[0].get("firstgid", "0"))
    if firstgid <= 0:
        raise ValueError("Invalid firstgid")
    tsx_path = map_path.parent / refs[0].get("source")
    tsx = ET.parse(tsx_path).getroot()
    if (int(tsx.get("tilewidth", "0")), int(tsx.get("tileheight", "0"))) != (tw, th):
        raise ValueError("Unsupported tileset/map tile-size mismatch")
    if tsx.find("tileoffset") is not None:
        raise ValueError("Unsupported tileset tileoffset")
    for tile in tsx.findall("tile"):
        if tile.find("animation") is not None or tile.find("image") is not None:
            raise ValueError("Unsupported animated or collection tile")
    columns, count = int(tsx.get("columns", "0")), int(tsx.get("tilecount", "0"))
    margin, spacing = int(tsx.get("margin", "0")), int(tsx.get("spacing", "0"))
    if min(columns, count) <= 0 or min(margin, spacing) < 0:
        raise ValueError("Invalid atlas geometry")
    image_node = tsx.find("image")
    if image_node is None or not image_node.get("source") or image_node.get("trans"):
        raise ValueError("Expected an RGBA atlas without a colour-key transform")
    with Image.open(tsx_path.parent / image_node.get("source")) as source:
        atlas = source.convert("RGBA")
    if image_node.get("width") and int(image_node.get("width")) != atlas.width:
        raise ValueError("Atlas width metadata differs from image")
    if image_node.get("height") and int(image_node.get("height")) != atlas.height:
        raise ValueError("Atlas height metadata differs from image")
    rows = (count + columns - 1) // columns
    if (margin * 2 + columns * tw + (columns - 1) * spacing > atlas.width
            or margin * 2 + rows * th + (rows - 1) * spacing > atlas.height):
        raise ValueError("Atlas cells exceed image bounds")
    background = root.get("backgroundcolor")
    if background and (len(background) != 7 or not background.startswith("#")):
        raise ValueError("Unsupported map background colour")
    canvas = Image.new("RGBA", (width * tw, height * th), background or (0, 0, 0, 0))
    cells: dict[int, Image.Image] = {}
    for node in root:
        if node.tag in ("properties", "tileset", "editorsettings") or node.get("visible", "1") == "0":
            continue
        if node.tag == "objectgroup" and node.find("object") is None:
            continue
        if node.tag != "layer":
            raise ValueError(f"Unsupported visible map feature: {node.tag}")
        reject_attributes(node, ("offsetx", "offsety", "x", "y", "parallaxx", "parallaxy"))
        if node.get("tintcolor") or node.get("blendmode", "normal") != "normal":
            raise ValueError("Unsupported visible layer tint or blend mode")
        if (int(node.get("width", "0")), int(node.get("height", "0"))) != (width, height):
            raise ValueError("Unsupported layer dimensions")
        opacity = float(node.get("opacity", "1"))
        if not 0 <= opacity <= 1:
            raise ValueError("Invalid layer opacity")
        data = node.find("data")
        if data is None or data.get("encoding") != "csv" or data.get("compression") or list(data):
            raise ValueError("Only finite uncompressed CSV layers are supported")
        ids = [int(value.strip()) for value in (data.text or "").split(",") if value.strip()]
        if len(ids) != width * height:
            raise ValueError("Layer cell count differs from map dimensions")
        layer_image = Image.new("RGBA", canvas.size)
        for index, gid in enumerate(ids):
            if gid == 0:
                continue
            if gid < 0 or gid & 0xF0000000:
                raise ValueError("Unsupported transformed or invalid tile GID")
            local_id = gid - firstgid
            if not 0 <= local_id < count:
                raise ValueError(f"GID {gid} is outside the attached tileset")
            if local_id not in cells:
                left = margin + (local_id % columns) * (tw + spacing)
                top = margin + (local_id // columns) * (th + spacing)
                cells[local_id] = atlas.crop((left, top, left + tw, top + th))
            layer_image.alpha_composite(cells[local_id], ((index % width) * tw, (index // width) * th))
        if opacity != 1:
            layer_image.putalpha(layer_image.getchannel("A").point(lambda a: round(a * opacity)))
        canvas.alpha_composite(layer_image)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render_bundle(args.map).save(args.output)


if __name__ == "__main__":
    main()
