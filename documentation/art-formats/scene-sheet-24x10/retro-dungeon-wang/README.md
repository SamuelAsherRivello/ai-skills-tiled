# Retro Dungeon Wang companion

![Retro Dungeon grid-safe Wang tiles](tiles.png)

![Live Tiled Figure 8 sample with uniform walkable floor](output/preview.png)

This 96x64 PNG contains 24 cells at 16x16 pixels: 21 authored mixed Wang
roles, one dark void, one blue-water tile, and one stair tile. It is a
companion to the [384x160 Scene Sheet](../README.md), not a replacement for
that composed image. The source style came from the user-supplied dungeon
reference; its original creator and license were not provided.

- [Open the freshly painted Wang Figure 8](output/retro-dungeon-figure-8-wang.tmx) with its
  [external tileset](output/retro-dungeon-wang.tsx) and the image beside it.
- The [earlier Wang sample](output/retro-dungeon-sample.tmx) remains available.
- [Role key](mapping.json) records every local tile ID and eight-value Wang
  assignment. The [builder](../../../../skills/tiled-ai-create-art/scripts/build_dungeon_wang_companion.py)
  creates the PNG and role key.

The `rpgjs/tiled-ai` live bridge imported the image into Tiled 1.12.2 and
authored the `Walkable rooms` mixed Wang set with one `Walkable floor` colour.
Mixed topology was chosen because the outer boundary and the right lobe's
inner void need both side and diagonal ownership. The set records 21 tile
masks; this Figure 8 requires 13 of them. A 4×4 boundary probe passed, and a
fresh 28×14 map was painted after the [user-picked basic sample](../retro-dungeon-basic/README.md).
Tiled populated all 200 requested Wang cells; `read_region` found no missing
or mismatched Wang IDs under Tiled's corner rules. The saved map has 392
repeated floor cells, 16 deliberate dark-core cells, and an empty Objects
layer. The same walkable floor tile fills the lower right. Its rendered room
joins were inspected before saving. The blue-water tile remains in the sheet
for maps that need it.
The preview above is the live Tiled region render, cropped to its map area.

This is **limited Wang-ready** for the tested Figure 8 room footprint.
The other assigned masks have not been proved for arbitrary corridor, island,
or erase-and-repaint shapes.

The basic Figure 8 uses tile 23 uniformly for walls, tile 20 for floor, and
tile 21 for its right-side void. This Wang version selects varied corners
from the 21 assigned masks and surrounds its interior core automatically.
