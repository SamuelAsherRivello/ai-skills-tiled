# Tiled AI MCP editing contract

Use the `tiled-ai` MCP as the authority for live Tiled documents. Do not edit a
TMX, TSX, TMJ, or TSJ behind Tiled's back while its document is open.

1. Call `get_editor_state` and use its returned session and explicit document
   identifiers. If there is no connected editor session, stop and run
   `$tiled-ai-setup`.
2. Inspect the intended map or tileset before changing it: use `get_map_info`,
   `list_layers`, `list_tilesets`, `list_wang_sets`, `get_objects`, or
   `inspect_tileset_image` as appropriate.
3. Every mutation supplies the latest `expectedRevision` and a new
   `requestId`. Re-read the document after each mutation; do not reuse a stale
   revision.
4. Use the focused MCP operation: `create_tileset_from_image` and
   `attach_tileset` for palettes, `create_layer` and `set_tiles` for tile data,
   `create_objects` or `update_objects` for map objects,
   `set_tile_collisions` for collision shapes, and `create_wang_set` plus
   `paint_terrain` for autotiling.
5. Verify the result through the MCP before saving. Save maps with `save_map`
   and external tilesets separately with `save_tileset`; saving a map does not
   save an external tileset.
6. Treat `list_layers` root ordering as bottom-to-top. To obtain a visual stack
   of `Objects`, `Walls`, `Floor` from top to bottom, verify returned root
   order `Floor`, `Walls`, `Objects` after creating layers.
7. Paginate `read_region` at 256 cells. `get_region_image` is bounded to 1024
   pixels per dimension, so split larger visual checks into bounded regions.
8. Treat a Wang set as authored content, not a name-only prerequisite. Before
   `paint_terrain`, verify its tile assignments against the selected tileset
   and visually test the required combinations. Use
   `$tiled-ai-create-tileset-autotiling-tsx` when a compatible set is absent.
   When that tileset is attached to a map, re-read `list_wang_sets` from the
   map and use its returned Wang-set and color IDs: attachment can assign
   map-local IDs that differ from the source tileset document.
9. `paint_terrain` paints one declared terrain colour. For room-frame art,
   paint the complete walkable footprint—not a one-cell wall stroke—so its
   boundary cells receive directional wall art and its interior receives the
   floor tile. Keep the footprint within the masks the exact TSX proves.

Use normal repository edits only for runtime code, tests, and documentation.
When the MCP does not expose the required editor operation, stop and explain
the missing capability rather than silently editing an open Tiled data file.
