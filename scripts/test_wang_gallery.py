"""Focused offline gallery regressions; no editor or production assets are changed."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from PIL import Image

import build_wang_gallery as gallery
from render_tiled_bundle import render_bundle


class GalleryPackagingTests(unittest.TestCase):
    def setUp(self):
        fixture_parent = Path(__file__).resolve().parents[1] / "tmp"
        fixture_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="tiled-gallery-test-", dir=fixture_parent)
        self.root = Path(self.temporary.name)
        if not self.root.resolve().is_relative_to(fixture_parent.resolve()):
            raise ValueError("Temporary fixture escaped the repository tmp directory")
        self.addCleanup(self.temporary.cleanup)
        self.source = self.root / "source"
        self.source.mkdir()
        self.colours = ((200, 10, 20, 255), (30, 200, 40, 255), (50, 60, 200, 255))
        atlas = Image.new("RGBA", (7, 7))
        for tile_id, colour in enumerate(self.colours):
            left, top = 1 + (tile_id % 2) * 3, 1 + (tile_id // 2) * 3
            atlas.paste(colour, (left, top, left + 2, top + 2))
        atlas.save(self.source / "atlas.png")
        tsx = ET.Element("tileset", tilewidth="2", tileheight="2", tilecount="3",
                         columns="2", margin="1", spacing="1")
        ET.SubElement(tsx, "image", source="atlas.png", width="7", height="7")
        ET.ElementTree(tsx).write(self.source / "atlas.tsx")
        self.map = ET.Element("map", orientation="orthogonal", width="2", height="2",
                              tilewidth="2", tileheight="2", infinite="0")
        ET.SubElement(self.map, "tileset", firstgid="7", source="atlas.tsx")
        for layer_id, name, gids in ((1, "Floor", "7,7,7,7"),
                                     (2, "Walls", "8,0,0,0"),
                                     (3, "Wall Joints", "0,9,0,0"),
                                     (4, "Wall Details", "0,0,8,0")):
            layer = ET.SubElement(self.map, "layer", id=str(layer_id), name=name,
                                  width="2", height="2")
            ET.SubElement(layer, "data", encoding="csv").text = gids
        ET.SubElement(self.map, "objectgroup", id="5", name="Objects")
        self.save_map()

    def save_map(self):
        ET.ElementTree(self.map).write(self.source / "source.tmx")

    def test_missing_preview_preserves_canonical_layers(self):
        with patch.object(gallery, "EXAMPLES", self.root / "examples"):
            gallery.package_existing("fixture", self.source / "atlas.png",
                                     self.source / "atlas.tsx", self.source / "source.tmx", None)
        target = self.root / "examples/fixture/output"
        packaged = ET.parse(target / "level.tmx").getroot()
        source_layers = [ET.tostring(n) for n in self.map if n.tag in ("layer", "objectgroup")]
        packaged_layers = [ET.tostring(n) for n in packaged if n.tag in ("layer", "objectgroup")]
        # XML indentation may differ; preserve attributes, data and ordering.
        self.assertEqual(len(source_layers), len(packaged_layers))
        for original, copied in zip(list(self.map)[1:], list(packaged)[1:]):
            self.assertEqual(original.tag, copied.tag)
            self.assertEqual(original.attrib, copied.attrib)
            self.assertEqual(original.findtext("data", "").strip(), copied.findtext("data", "").strip())
        self.assertEqual(packaged.find("tileset").get("source"), "tiles.tsx")
        self.assertEqual(packaged.find("tileset").get("firstgid"), "7")
        with Image.open(target / "preview.png") as preview:
            self.assertEqual(preview.tobytes(), render_bundle(self.source / "source.tmx").tobytes())
        self.assertTrue((target / "preview-native.png").is_file())

    def test_atlas_columns_margin_spacing_and_firstgid(self):
        rendered = render_bundle(self.source / "source.tmx")
        self.assertEqual(rendered.getpixel((0, 0)), self.colours[1])
        self.assertEqual(rendered.getpixel((2, 0)), self.colours[2])
        self.assertEqual(rendered.getpixel((0, 2)), self.colours[1])
        self.assertEqual(rendered.getpixel((2, 2)), self.colours[0])

    def test_visible_unsupported_features_are_not_silently_omitted(self):
        ET.SubElement(self.map, "imagelayer", name="Unsupported")
        self.save_map()
        with self.assertRaisesRegex(ValueError, "Unsupported visible map feature: imagelayer"):
            render_bundle(self.source / "source.tmx")

    def test_hidden_unsupported_layer_is_not_visible(self):
        ET.SubElement(self.map, "imagelayer", name="Hidden", visible="0")
        self.save_map()
        self.assertEqual(render_bundle(self.source / "source.tmx").size, (4, 4))

    def test_transformed_gid_is_rejected(self):
        self.map.find("layer/data").text = "2147483655,7,7,7"
        self.save_map()
        with self.assertRaisesRegex(ValueError, "transformed"):
            render_bundle(self.source / "source.tmx")

    def test_out_of_range_gid_is_rejected(self):
        self.map.find("layer/data").text = "10,7,7,7"
        self.save_map()
        with self.assertRaisesRegex(ValueError, "outside"):
            render_bundle(self.source / "source.tmx")

    def test_partial_opacity_is_composited(self):
        self.map.findall("layer")[1].set("opacity", "0.5")
        self.save_map()
        pixel = render_bundle(self.source / "source.tmx").getpixel((0, 0))
        self.assertEqual(pixel[3], 255)
        self.assertNotEqual(pixel, self.colours[0])
        self.assertNotEqual(pixel, self.colours[1])


if __name__ == "__main__":
    unittest.main()
