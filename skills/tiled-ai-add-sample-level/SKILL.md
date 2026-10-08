---
name: tiled-ai-add-sample-level
description: Create a small Tiled AI sample level from one tileset with empty Objects, Wang-autotiled Walls, and a repeated Floor. Use when a project needs a fresh playable map or an end-to-end terrain test.
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
  `<tileset-slug>-figure-8.tmx`. If it exists, increment a suffix such as
  `-2` before `.tmx` until the path is unused. Resolve the resulting absolute
  path before `create_map`; never overwrite an existing map.
- Run `$tiled-ai-setup` first and call `get_editor_state`; stop if Tiled is not
  connected.

## Build the map

1. Use `create_map` with the chosen dimensions and an initial `Floor` tile
   layer. Attach the selected tileset with `attach_tileset`.
2. Create an empty `Objects` object layer and an empty `Walls` tile layer.
   Keep the order `Objects`, `Walls`, `Floor` from top to bottom. The current
   MCP returns root layers bottom-to-top, so create and verify the returned
   order `Floor`, `Walls`, `Objects`; use the live layer IDs rather than names
   alone.
3. Use exactly the selected tileset for the entire first iteration: select one
   caller-supplied or clearly designated base/floor tile and fill all 50×50
   default cells with it using `fill_region` or `set_tiles`. Use the same
   tileset's Wang set for Walls. Do not attach, mix, or infer a second tileset.
   Do not choose a decorative, collision, or terrain-edge tile as the floor
   without confirmation.
4. Treat Automapping as a companion **rule bundle**, not a property of the
   TSX. When the caller supplies a compatible, execution-verified rule map and
   `rules.txt` that target this map's layers, preserve their target-layer
   contract and use the bundle after building its inputs. Otherwise continue
   with the Wang-only flow below; a tileset without rules remains fully
   supported. The current live `tiled-ai` MCP does not expose Map > AutoMap.
   Never invoke an external process against the new map while Tiled has it
   open. If the caller needs Automapping output now, save and return the input
   map plus the verified bundle with a clear execution handoff, rather than
   claiming the rule output was generated. Use
   `$tiled-ai-add-tileset-automapping` to author or independently verify a
   rule bundle on a disposable, unopened fixture.
5. Run `$tiled-ai-add-tileset-autotiling` when the selected tileset has not
   already been classified. A default **Figure 8** must use one of its
   verified outcomes; never produce a floor-only substitute:
   - For a **Wang-ready** tileset, inspect `list_wang_sets` against the map
     and its attached tileset ID. Use the map-local Wang-set and color IDs
     returned after attachment—they may differ from the source tileset
     document's IDs—then use `paint_terrain` on `Walls`.
   - For a **limited Wang-ready** tileset, use only its declared supported
     footprint family. Do not turn a missing mask into manual wall art.
   Unless the caller supplies a different layout:
   - Fill the entire map with the repeated Floor tile first; there is no
     exterior void in the default sample.
   - Paint the walkable footprint onto `Walls`: a centred 10×10 left lobe and
     a centred 10×10 right lobe joined by a four-tile-tall bridge. Its central
     two rows are the walkable passage; its top and bottom rows render as
     boundary walls. Leave a 4×4 unpainted core inside the right lobe. Use a
     mixed Wang set for this layout so the four concave inner corners are
     distinguished from ordinary floor. The Wang output draws its boundary
     wall art and uses its repeated floor tile inside the footprint.
   - When the exact tileset has a verified opaque void tile, fill the core on
     `Walls` after painting. Otherwise leave the core visibly distinct only
     when the rendered test proves the intended result.
   If Wang painting rejects the footprint or its rendered result has a blank,
   wrong-facing, or broken join, return to
   `$tiled-ai-add-tileset-autotiling`; do not fake the result by manually
   picking edge tiles.
6. Verify the floor, empty Objects layer, Walls result, and layer order with
   `read_region`, `list_layers`, and `get_region_image`. `read_region` pages
   at 256 cells, and images are bounded to 1024 pixels per dimension; paginate
   cell reads and split a 50×50, 32-pixel visual inspection into bounded views.
7. Re-read revisions after every mutation. Save the map with `save_map` and
   save the external tileset separately with `save_tileset` only if it changed.

Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

## Result Links

Finish with a clickable Markdown link to the saved `.tmx` result and, when
created or changed, its external tileset. Link only the path returned by
`save_map` or `save_tileset`; never link a planned destination.
