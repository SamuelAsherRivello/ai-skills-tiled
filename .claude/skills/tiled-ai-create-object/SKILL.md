---
name: tiled-ai-create-object
description: Create one independently placeable Tiled tile object from supplied static or animated artwork, including editor preview bounds, class/properties, collider or sensor geometry, runtime integration, tests, and visual verification. Use for props, decorations, doors, triggers, interactables, and similar Tiled-authored objects; do not use for ordinary painted terrain tiles or character actor pipelines.
---

# Tiled AI Create Object

## Tiled AI MCP requirement

Run `/tiled-ai-setup` first. Use the live `tiled-ai` MCP to inspect the map,
create or attach the object tileset, create the placeable object, verify its
properties and bounds, and explicitly save the changed map and tileset. Follow
the shared [MCP editing contract](references/tiled-ai-mcp.md); keep the
runtime integration below for repository code only.

Create one coherent object-authoring path from source art to Tiled placement and
runtime behavior. Preserve the user's requested art size, placement semantics,
animation, interaction, and collision behavior.

## Ground the Change

Before editing, inspect the repository's instructions and established Tiled
contract: project/map/tileset files, tile size, object layers, project classes,
anchors, coordinate conversion, loader/normalizer, render ordering, collision
model, attribution, and tests. Prefer existing names and patterns.

Distinguish the object from painted terrain. A thing that must be selected,
moved, duplicated, configured, triggered, animated independently, or assigned a
class belongs as an object even when its artwork is tile-like.

Resolve only material ambiguity. In particular, determine whether collision is
blocking or a non-blocking sensor, what activates animation, whether playback
loops, how it resets or rearms, which entities can trigger it, and which object
layer owns it. When the user's behavior is already explicit, proceed without
asking them to restate it.

## Implement Test-First

Add or update the smallest automated contract test before production changes.
Run it and confirm it fails for the missing object behavior. Then implement the
smallest complete path and rerun the same test.

For concrete TSJ/TMJ structure and asset handling, read
[references/tiled-object-contract.md](references/tiled-object-contract.md).

The finished object should normally provide:

- one named item in Tiled's Tilesets panel;
- tile-object placement on the repository's designated object layer;
- independent object identity, placement, properties, and runtime state;
- an appropriate Tiled project class with reusable defaults and per-placement
  overrides;
- an explicit bottom-center or repository-established ground anchor;
- blocking collision or sensor geometry that matches the declared semantics;
- runtime normalization, validation, rendering, lifecycle, and interaction;
- source attribution when required by the repository or asset license.

## Keep Editor and Runtime Art Independent

Treat the Tiled preview as editor UI, not automatically as the runtime texture.
For animated or padded artwork, use a single preview image for the logical
object and keep the untouched runtime sheet plus true frame metadata separate.
Do not expose every animation frame as a separately placeable palette item.

Unless the user or repository specifies another footprint, make the Tiled
selection bounds exactly one map tile. Fit the visible art proportionally inside
that preview, center it, preserve nearest-neighbor sampling for pixel art, and
use a tile offset to retain the intended anchor. Never silently change in-game
scale just to improve editor selection bounds.

## Verify the Complete Path

Verify the focused test, related tests, full suite, and production build. Inspect
the saved Tiled JSON or open it in Tiled to confirm one palette item, the correct
object layer/class, selection dimensions, anchor, and collider. For runtime
behavior, use a real browser or the project's actual runtime and check size,
placement, collision passage/blocking, animation rules, independent instances,
render ordering, and disposal.

Tell the user which project and map to reopen. Tiled may cache tileset previews,
so close and reopen the map or tileset after preview changes.

Do not claim completion if editor structure, runtime behavior, or required
verification remains unfinished. Report unrelated pre-existing test failures
separately and do not repair them without scope.

## Result Links

Finish with clickable Markdown links to each created or changed object asset,
runtime source file, map, and external tileset. Link only verified existing
files; do not present a planned path as a completed result.
