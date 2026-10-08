---
name: tiled-ai-copy-tileset-colliders-tsj
description: Validate a one-to-one Tiled tileset mapping and copy collider object groups from one external JSON tileset to another using required from and to paths.
---

# Tiled AI Copy Tileset Colliders TSJ

## Tiled AI MCP requirement

Run `/tiled-ai-setup` first. Open and inspect the target external tileset
through the live `tiled-ai` MCP. Apply verified collider geometry with
`set_tile_collisions`, verify the changed tile data, and save the external
tileset explicitly. Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

Copy collider metadata between two corresponding external Tiled JSON tilesets. Require the user to identify both arguments:

- `from`: source `.tsj` whose collider object groups are authoritative.
- `to`: destination `.tsj` that will receive the collider object groups.

Never infer a missing argument and never reverse their direction silently.

## Validate One-to-One Mapping

Perform all validation before writing. Accept the pair only when:

- Both files parse as JSON tilesets.
- Their `tilewidth`, `tileheight`, `tilecount`, `columns`, `margin`, and `spacing` match exactly.
- Their declared image dimensions match and agree with the referenced image files.
- Each local tile ID therefore identifies the same cell coordinates in both sheets.
- The source and destination artwork are corresponding variants, confirmed by visual inspection or an exact per-tile occupied-pixel/transparency-mask comparison.
- Any animation frame mappings or tile transformations that affect local tile identity are compatible.

Reject the copy and report the mismatch when any required check fails. Similar filenames alone are not proof of a one-to-one mapping.

## Preview, Copy, and Save

Run `scripts/copy_tsj_colliders.mjs --from <source.tsj> --to <destination.tsj>` first. It performs a dry run and reports the planned source and destination collider tile IDs. Add `--write` only after the one-to-one artwork check is also confirmed.

The copy operation SHALL:

- Deep-copy each source tile's complete `objectgroup` to the same local tile ID in the destination.
- Remove a destination `objectgroup` when the corresponding source tile has none, so destination collision becomes an exact mirror of the source.
- Preserve all destination tileset identity, image, animation, properties, and other non-collider metadata.
- Create destination tile entries when needed and retain existing destination tile entries even when their collider is removed.
- Keep destination tile entries ordered by local tile ID.
- Never modify the source file.

## Verify

After writing:

1. Parse both TSJs again.
2. Compare every local tile ID and require deep equality between source and destination `objectgroup` values, including absence.
3. Confirm source bytes did not change and destination identity/image metadata remained unchanged.
4. Run relevant focused tests. Optionally smoke-test the destination in Tiled or the game when that adds useful confidence.
5. Inspect the diff and report the copied collider tile count and IDs, any destination colliders replaced or removed, and verification results.

## Result Links

Finish with clickable Markdown links to both the unchanged source tileset and
the verified changed destination tileset. Link only existing files.
