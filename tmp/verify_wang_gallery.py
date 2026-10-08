from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

root = Path(sys.argv[1])
examples = root / "documentation/examples"
reference = np.asarray(Image.open(examples / "layout-reference.png").convert("RGBA"))
folders = sorted(p for p in examples.iterdir() if p.is_dir() and p.name[:2].isdigit())
assert len(folders) == 10, len(folders)
for folder in folders:
    output = folder / "output"
    tsx = ET.parse(output / "tiles.tsx").getroot()
    tile = int(tsx.get("tilewidth"))
    assert tile in (16, 32, 64)
    assert int(tsx.get("tileheight")) == tile
    assert tsx.find("image").get("source") == "tiles.png"
    assert (output / "tiles.png").exists()
    scene = np.asarray(Image.open(output / "scene-sheet.png").convert("RGBA"))
    expected = np.asarray(Image.fromarray(reference).resize((24*tile,10*tile), Image.Resampling.NEAREST))
    assert scene.shape == (10*tile,24*tile,4)
    assert np.array_equal(scene[:,:,3], expected[:,:,3]), folder
    assert tsx.find("wangsets/wangset").get("type") == "mixed"
    masks = {tuple(int(x) for x in item.get("wangid").split(",")) for item in tsx.findall("wangsets/wangset/wangtile")}
    assert len(masks) >= 21, folder
    maproot = ET.parse(output / "level.tmx").getroot()
    assert maproot.find("tileset").get("source") == "tiles.tsx"
    assert (int(maproot.get("width")),int(maproot.get("height"))) == (28,14)
    assert int(maproot.get("tilewidth")) == tile
    assert len(maproot.findall("layer")) >= 2
    for layer in maproot.findall("layer"):
        ids = [int(x) for x in layer.find("data").text.replace("\n", "").split(",") if x.strip()]
        assert len(ids) == 28*14
        assert all(0 <= gid <= int(tsx.get("tilecount")) for gid in ids)
    with Image.open(output / "preview.png") as preview:
        assert preview.width > 0 and preview.height > 0
    docs = (folder / "README.md").read_text(encoding="utf-8")
    assert "tileset-layout-wang-mixed" in docs
    assert "output/scene-sheet.png" in docs and "output/preview.png" in docs
    print(folder.name, f"{tile}x{tile}", len(masks), "Wang masks", "OK")
