---
name: tiled-ai-update-tileset-colliders-tsj
description: Inspect and quantize only the existing collider shapes in a user-named external Tiled JSON tileset, preserving collider-free tiles and stopping for ambiguous geometry or artwork conflicts.
---

# Tiled AI Update Tileset Colliders TSJ

## Tiled AI MCP requirement

Run `/tiled-ai-setup` first. Open and inspect the target external tileset
through the live `tiled-ai` MCP. Apply approved collider geometry with
`set_tile_collisions`, verify the changed tiles, and save the external tileset
explicitly. Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

Normalize collider geometry in one user-named `.tsj` file. Do not add colliders to tiles that currently have none, and do not propagate edits to sibling tilesets unless the user explicitly requests that broader scope.

## Inspect Before Editing

1. Parse the TSJ and resolve its referenced tilesheet image relative to the TSJ.
2. Record the tile dimensions and every tile ID whose `objectgroup.objects` contains collider objects.
3. Classify all existing nonzero collider objects from their current geometry. Crop or otherwise inspect the corresponding tilesheet cells to confirm the visible artwork supports that interpretation.
4. If any shape or orientation remains uncertain, or the artwork conflicts with the geometry, report the affected tile IDs and ask the user before changing the file. Make no edits until all tiles are classified.

Zero-width or zero-height rectangle objects with no polygon are artifacts, not meaningful colliders. Record them for removal; they do not by themselves make a tile ambiguous. Do not remove a polygon merely because Tiled stores zero in its rectangle `width` and `height` fields; determine polygon area from its vertices.

## Canonical Shapes

Quantize dimensions relative to the TSJ grid. For a 64 by 64 grid, use these exact shapes:

- Full square: rectangle at `x: 0`, `y: 0`, `width: 64`, `height: 64`.
- Half-tile triangle: polygon using exactly three tile corners, covering half the tile. Preserve the evident orientation; only the four corner-based orientations are valid.
- Left edge: rectangle at `x: 0`, `y: 0`, `width: 4`, `height: 64`.
- Right edge: rectangle at `x: 60`, `y: 0`, `width: 4`, `height: 64`.
- Top edge: rectangle at `x: 0`, `y: 0`, `width: 64`, `height: 4`.
- Bottom edge: rectangle at `x: 0`, `y: 60`, `width: 64`, `height: 4`.

For another grid size, do not invent an edge thickness. Ask the user unless they already supplied one.

A tile may have one, two, three, or four edge rectangles. Retain one full-length rectangle for every detected side. Corner overlaps are intentional. Four edge rectangles remain four border colliders; do not reinterpret them as a full-square collider.

## Edit Conservatively

After the read-only visual classification is confirmed, `scripts/quantize_tsj_colliders.mjs <path>` can report the deterministic geometry transformation. Add `--write` only after reviewing that report. The helper refuses shapes outside the supported categories; it does not replace the artwork check or authorize guessing.

- Quantize existing objects in place rather than rebuilding the object group or combining shapes.
- Preserve object IDs, names, types/classes, properties, visibility, and other non-geometry metadata.
- Remove confirmed zero-area rectangle objects, never valid polygon objects whose rectangle width and height fields are zero.
- Keep rectangles as rectangles and triangles as polygons.
- Preserve tile entries, object-group metadata, unrelated tileset data, and JSON semantics.

For a Tiled polygon, choose a valid canonical `x`, `y`, and relative `polygon` point representation whose absolute vertices are exactly the intended three tile corners. Do not retain fractional or out-of-bounds coordinates.

## Verify and Report

After editing:

1. Parse the TSJ again as strict JSON.
2. Verify that tiles without colliders before the edit still have none.
3. Verify every remaining collider is exactly one allowed square, triangle, or edge shape and lies within the tile bounds.
4. Verify no zero-area rectangle objects remain and every polygon has three distinct vertices with nonzero area.
5. Inspect the diff to ensure only the named TSJ and intended collider geometry changed.

Report tile IDs grouped as changed, zero-area objects removed, already canonical, and unresolved. State the exact grid size and edge thickness used.

## Result Links

Finish with a clickable Markdown link to the verified changed external tileset.
Link only the existing named `.tsj` file; do not present a planned path as a
completed result.
