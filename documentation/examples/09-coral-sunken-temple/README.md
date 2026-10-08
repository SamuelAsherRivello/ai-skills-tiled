# Coral Sunken Temple

Grid: **32×32**. Layout: **`tileset-layout-wang-mixed`**. Wang type: **mixed**.

## Try this prompt

```text
$tiled-ai-create-art Create a 32x32 scene sheet in layout tileset-layout-wang-mixed with the theme coral sunken sea temple. Keep the exact 24x10 reference silhouette, interior room, exterior assembly, detached supports, stairs, liquid, and transparent gaps. Then make a separate Mixed Wang companion and a 28x14 Figure 8 sample level with a 4x4 unwalkable core.
```

## Wang results

| 24×10 scene sheet PNG | Sample level PNG |
|---|---|
| ![Coral Sunken Temple scene sheet](output/scene-sheet.png) | ![Coral Sunken Temple Wang sample level](output/preview.png) |

The [Wang companion PNG](output/tiles.png), [external TSX](output/tiles.tsx), and [TMX map](output/level.tmx) stay together in `output/`. Open the TMX in Tiled with all three files present. The scene sheet follows the 24×10 composition; the companion contains the actual Wang assignments.

[Original generated material swatches](input/source.png) are included. Original generated material swatches were composed into the reference layout for this gallery. The companion covers the 21 Figure 8 masks; the packaged map was opened in Tiled, but was not terrain-painted live.

The Mixed Wang companion includes the masks required for this Figure 8. This example does not establish arbitrary shape support.
