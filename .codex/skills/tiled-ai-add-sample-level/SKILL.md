---
name: tiled-ai-add-sample-level
description: Create a Tiled AI Figure 8 sample from one tileset. Before autotiling use one wall, one walkable floor, and one empty-looking tile; with verified Wang metadata use a more complex layout.
---

# Tiled AI Add Sample Level

Create a new, saved sample map through the live `tiled-ai` MCP. Accept one
tileset plus optional tile-grid and world dimensions. Defaults are 32×32 pixel
tiles and a 50×50-cell world. Never overwrite an existing map or tileset.

## Validate the inputs

- Require one open or supplied tileset. Inspect it with `list_tilesets`,
  `open_tileset`, or `inspect_tileset_image` rather than guessing its ID. Use
  the active map's sole attached tileset without asking. Ask one focused
  tileset question only when no safe single choice exists.
- If the caller omits dimensions, use 32×32 pixels and 50×50 cells. If a
  supplied tileset's grid differs, keep its grid and report that override.
- Do not ask for an output path. Unless the caller supplies one, save below
  `<workspace>/output/tiled-ai-sample-level/` as
  `<tileset-slug>-figure-8-basic.tmx` without Wang metadata or
  `<tileset-slug>-figure-8-wang.tmx` with verified Wang metadata. If it exists,
  increment a suffix such as `-2` before `.tmx` until the path is unused.
  Resolve the resulting absolute path before `create_map`; never overwrite an
  existing map.
- Run `$tiled-ai-setup` first and call `get_editor_state`; stop if Tiled is not
  connected.
- Inspect the selected tileset's current revision and `list_wang_sets` before
  choosing a layout. An empty list means **basic mode**. A Wang set is ready
  for **Wang mode** only when its documented footprint has been verified in
  the live editor; metadata alone is not proof that the Figure 8 will render.
- When the caller marks or names the three basic-mode tiles, use those picks
  for the stated roles. For an annotated image, confirm its grid and convert
  each marked cell to the exact local tile ID before editing; do not replace
  a caller's pick with your own visual preference.

## Build the map

1. Use `create_map` with the chosen dimensions and an initial `Floor` tile
   layer. Attach the selected tileset with `attach_tileset`.
2. Create an empty `Objects` object layer and an empty `Walls` tile layer.
   Keep the order `Objects`, `Walls`, `Floor` from top to bottom. The current
   MCP returns root layers bottom-to-top, so create and verify the returned
   order `Floor`, `Walls`, `Objects`; use the live layer IDs rather than names
   alone.
3. Use exactly the selected tileset. Inspect its image and choose explicit
   local tile IDs that visually match their roles. Do not attach, mix, or infer
   a second tileset. Fill the whole map with the tile that looks most like a
   walkable floor. Prefer a seamless repeat, but do not require one. Do not
   choose an obvious decorative, collision, or terrain-edge tile as the base
   when a better floor tile exists. If the image lacks a suitable tile for a
   required role, report that limitation instead of inventing an ID.
4. Treat Automapping as a companion **rule bundle**, not a property of the
   TSX. When the caller supplies a compatible, execution-verified rule map and
   `rules.txt` that target this map's layers, preserve their target-layer
   contract and use the bundle after building its inputs. Otherwise continue
   with the applicable basic or Wang flow below; a tileset without rules
   remains fully supported. The current live `tiled-ai` MCP does not expose
   Map > AutoMap.
   Never invoke an external process against the new map while Tiled has it
   open. If the caller needs Automapping output now, save and return the input
   map plus the verified bundle with a clear execution handoff, rather than
   claiming the rule output was generated. Use
   `$tiled-ai-add-tileset-automapping` to author or independently verify a
   rule bundle on a disposable, unopened fixture.
5. Build the layout for the tileset's current state. Unless the caller gives a
   different layout, centre two 10×10 lobes and connect them with a
   four-tile-tall bridge. Keep the bridge's central two rows walkable.
   - **Basic mode, no Wang set:** do this **before** invoking
     `$tiled-ai-add-tileset-autotiling`. Choose exactly three distinct local
     tile IDs by visual inspection when the caller has not picked them:
     (1) the tile that looks most like a
     non-directional, non-walkable wall, or a top-wall tile if no such tile
     exists; (2) the tile that looks most like walkable floor; and (3) a tile
     that indicates nothing, preferably all black or transparent. Put the
     same first tile on *every* Figure 8 boundary cell, including both lobes
     and the bridge, using `set_tiles` or `fill_region` on `Walls`. Put the
     floor tile under the whole map. Put the empty-looking third tile in a
     bounded patch inside the right lobe, leaving a walkable route around it.
     Keep the left interior walkable.
     Do not call `paint_terrain` or imply that these uniform walls are
     autotiled. Save this basic sample so it can be compared with a later
     Wang version.
   - **Verified Wang mode:** make a more complex Figure 8 with varied wall
     corners and a 4×4 interior core in the right lobe. Inspect
     `list_wang_sets` against the map and its attached tileset ID. Use the
     map-local Wang-set and color IDs returned after attachment—they may
     differ from the source tileset document's IDs—then use `paint_terrain`
     on `Walls`. For a limited Wang-ready tileset, stay within its verified
     footprint family. When the exact tileset has a verified opaque void
     tile, fill the core on `Walls` after painting. Otherwise use a core only
     when the render proves the intended result. Keep the same walkable floor
     tile across every `Floor` cell, including the exterior and lower-right
     area. Add water or other display materials only when the caller asks;
     the default sample should show the Figure 8 wall topology clearly.
     Where a bridge corner has the same Wang mask as an ordinary floor or
     straight-wall cell, place its matching room-corner tile on a separate
     `Wall Joints` layer above `Walls`. Document those manual join cells and
     verify that the underlying `Walls` layer still matches every Wang mask.
   - If Wang metadata exists but this footprint is unverified, use
     `$tiled-ai-add-tileset-autotiling` to verify or repair it before Wang
     painting. If the footprint cannot be verified, report that result; do
     not label a manually assembled map as Wang-autotiled. If painting
     produces a blank, wrong-facing, or broken join, return to that skill.
6. When the source sheet distinguishes an upper-left internal room from an
   upper-right external wallset, compare the rendered left lobe with the
   source's internal wall art. A correct Wang ID table is insufficient if its
   rendered wall thickness, cap, or material does not match that art; revise
   the companion roles and repaint before delivering the sample. For walls
   that depict height inside one tile, check that the cap, face, and lower
   shadow stay aligned through straight runs, all four room corners, and
   bridge joins in the full map render.
7. Verify the floor, empty Objects layer, Walls result, and layer order with
   `read_region`, `list_layers`, and `get_region_image`. `read_region` pages
   at 256 cells, and images are bounded to 1024 pixels per dimension; paginate
   cell reads and split a 50×50, 32-pixel visual inspection into bounded views.
   In basic mode, verify that every boundary cell has the one wall tile, the
   left interior has the walkable tile, and the right patch has the
   empty-looking third tile.
8. Re-read revisions after every mutation. Save the map with `save_map` and
   save the external tileset separately with `save_tileset` only if it changed.

Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

## Result Links

Finish with a clickable Markdown link to the saved `.tmx` result and, when
created or changed, its external tileset. Link only the path returned by
`save_map` or `save_tileset`; never link a planned destination.
