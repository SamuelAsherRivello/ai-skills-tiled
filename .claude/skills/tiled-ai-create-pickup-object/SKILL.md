---
name: tiled-ai-create-pickup-object
description: Create a Tiled-authored pickup object type and integrate its reusable runtime creation path without adding a spawner.
---

# Tiled AI Create Pickup Object

## Tiled AI MCP requirement

Run `/tiled-ai-setup` first. Use the live `tiled-ai` MCP for any pickup tileset
and optional map object data: inspect the target, create or attach the palette,
create/update the pickup object when it is placeable, verify it, and explicitly
save every changed map and external tileset. Follow the shared
[MCP editing contract](references/tiled-ai-mcp.md).

Use this skill when adding a new pickup that resembles an existing pickup.

- Define sprite, size, collider, and lifecycle using existing object/pickup conventions.
- Keep pickup creation independent from Tiled spawners. Create pickups on demand through the shared pickup system, which accepts a pickup definition and arbitrary world start/destination positions.
- Preserve origin-relative level coordinates and bottom-centered Tiled object placement.
- If placeable in Tiled, add tileset/object metadata and loader validation, but do not add it to the spawner catalog.
- Verify spawning, collection, disposal, renderer attachment, and focused tests/build behavior.

## Result Links

Finish with clickable Markdown links to every created or changed pickup asset,
runtime source file, map, and external tileset. Link only verified existing
files; do not present a planned path as a completed result.
