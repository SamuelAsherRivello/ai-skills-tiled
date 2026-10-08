# Figure 8 Autotiling

![Figure 8 room sample with a bridge and an unwalkable core](output/preview.png)

This portable 28 × 14 Tiled sample shows a Wang-tiled Figure 8 room footprint: two 10 × 10 lobes joined by a four-tile-tall bridge, with a 4 × 4 unwalkable core in the right lobe. The map has a repeated `Floor` layer, a `Walls` layer using the mixed `Walkable rooms` Wang set, and an empty `Objects` layer.

- [Open the TMX map](output/figure-8.tmx) in Tiled. Keep its [external TSX](output/tiles.tsx) and [tile image](output/tiles.png) together in the same directory.
- [Prompt](input/prompt.txt) describes the requested shape. The [builder](../../../scripts/build_figure8_example.py) creates the tile art, Wang assignments, map, and preview using Python's standard library.
- The TSX assigns one `Walkable floor` color to the 21 mixed Wang masks needed by this exact footprint. The `Walls` layer uses those assignments. Its dark 4 × 4 core is deliberately filled with a separate void tile after the Wang footprint is calculated.

The artwork is original to this example. The builder selected each map tile from its neighboring footprint cells and rendered the preview without an editor session. This demonstrates a portable Wang-configured fixture; it does not claim that the Tiled AI bridge painted or visually verified this file. The 21-mask set is scoped to this Figure 8 layout and is not a complete mixed Wang set for arbitrary shapes.
