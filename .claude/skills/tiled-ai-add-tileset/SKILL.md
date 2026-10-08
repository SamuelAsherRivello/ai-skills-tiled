---
name: tiled-ai-add-tileset
description: Convert supplied tile-sheet art into a saved external Tiled TSX through the live Tiled AI MCP. Use before adding autotiling, colliders, or map palette references.
---

# Tiled AI Add Tileset

Convert an image into one inspected, saved external `.tsx` tileset. This skill
does not infer autotiling, collision, map placement, or game-runtime behavior:
use the dedicated follow-up skill for each of those concerns.

## Convert the art

1. Run `/tiled-ai-setup`, then inspect the supplied image through
   `inspect_tileset_image`. Determine the intended tile width, height, margin,
   spacing, columns, rows, and transparency from the actual pixels. Image
   divisibility is only a candidate grid, not proof.
2. Apply a source-suitability gate before creating anything. A grid import is
   appropriate only when one regular cell size and origin describe the intended
   tiles. Large transparent gaps, sprites of materially different footprints,
   label bands, or several unrelated art families are evidence of a packed
   atlas, not a grid tileset. Do not select the largest divisible candidate and
   generate blank or unrelated tiles. Search for a companion TSX/TSJ or
   separated source images; if none exists and the MCP cannot create the
   required collection-of-images or crop source, report **Not grid-importable
   through the current MCP** and leave the source unchanged.
   Treat animation strips or frame banks as a separate concern: preserve their
   source order and do not represent frames as unrelated static terrain tiles.
   This skill does not author tile animation; report that follow-up explicitly
   unless the source TSX already establishes the animation sequence.
3. Create a collision-free external `.tsx` with
   `create_tileset_from_image`. Use a stable user-supplied or project-local
   destination, never overwrite an existing file, and preserve the generated
   relative image reference.
4. Inspect the open TSX using `get_map_info` and all required pages of
   `get_tileset_images`. Verify the grid, tile count, and imported image match
   the source before saving it with `save_tileset`.
5. Do not attach the result to a map, write colliders, or add Wang metadata in
   this workflow. Route follow-up requests explicitly:
   - `/tiled-ai-add-tileset-autotiling` for Wang terrain metadata and a
     Figure 8 fitness proof.
   - `/tiled-ai-copy-tileset-colliders` or
     `/tiled-ai-update-tileset-colliders` for collision geometry.

Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

## Result Links

Finish with clickable links to the saved TSX and its MCP-imported source image.
Report the verified grid and tile count. Do not claim that converted art is
autotile-ready until `/tiled-ai-add-tileset-autotiling` has passed.

If the source-suitability gate stops the workflow, do not fabricate result
links. Instead report the absolute source path, inspection hash and dimensions,
the observed layout classification, the rejected candidate grids, and the
smallest concrete next action (a companion TSX/TSJ, separated images, or an
MCP operation that supports collection/crop import). This outcome is a
successful preflight, not a partially created tileset.
