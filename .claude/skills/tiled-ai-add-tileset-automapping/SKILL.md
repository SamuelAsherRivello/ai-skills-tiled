---
name: tiled-ai-add-tileset-automapping
description: Create and verify Tiled Automapping rule assets for an existing tileset. Use for input/output rule maps, rules.txt registration, and generated secondary map layers; not for Wang terrain metadata.
---

# Tiled AI Add Tileset Automapping

Create a tested Automapping **rule bundle for** an existing external tileset.
Automapping is not stored in a TSX: its outputs are a rule map (TMX or TMJ),
a `rules.txt` manifest or an explicitly approved project setting, and a saved
proof map. Use `/tiled-ai-add-tileset-autotiling` instead when the task is
to select connected edge/corner terrain art from Wang metadata.

## Preconditions and scope

- Require an existing external TSX plus a source reference that identifies the
  exact local tile IDs and the intended input-to-output behaviour. Inspect the
  exact source image and tileset; do not infer that a visually similar tile is
  a cliff side, reset tile, or replacement.
- A user-approved demonstration contract may provide that reference when the
  art has no inherent semantic pairing. Record it literally, for example
  “marker tile 0 on `Markers` emits decoration tile 2 one cell east on
  `Decorations`”; do not relabel it as an inferred cliff or terrain rule.
- Treat the rule bundle as map/project scoped. A TSX does not “have
  automapping” on its own. Ask for the target layer names and output location
  only when a safe convention is not already supplied.
- Use the live `tiled-ai` MCP for open documents. Never modify an open map or
  tileset behind Tiled's back. Tiled's command-line map reads are detached and
  cannot execute Automapping, so an editor-attached AutoMap operation is the
  only automated proof path.
- Do not alter the TSX unless the caller separately requests a tileset change.
  Do not overwrite an existing rule map, manifest, project, or fixture.

## Author rule assets

1. Create a normal rule map with one or more tile layers named
   `input[not][index]_TargetLayer` and `output[index]_TargetLayer`. A
   contiguous input/output region is one rule; leave space between distinct
   rules. Keep target layer names explicit rather than relying on display
   order.
2. Add only the tiles supported by the supplied mapping. The normal
   Automapping Rules Tileset may supply `Empty`, `Ignore`, `NonEmpty`,
   `Other`, and `Negate` when a precise rule needs them. Do not use legacy
   `regions` layers in new rules.
3. Register rule maps in a new, scoped `rules.txt`. Preserve declaration
   order: reset/cleanup passes come before generation passes. Prefer a
   colocated manifest or a filename filter to changing a project-wide
   Automapping Rules File; change the project only with explicit approval.
4. For rules intended for AutoMap While Drawing, include the cleanup path for
   prior output and set an evidence-backed `AutomappingRadius`. The RPG-cliff
   pattern normally needs a radius of at least `1` because editing the top
   affects tiles below it.

## Execute a proof, not only a structural check

Use a new, saved fixture map with a minimal input pattern. It must use the
same external TSX and target layer names as the rule map.

- Before promising an execution proof, check whether the available bridge can
  invoke AutoMap on an editor-attached map. The present bridge does not expose
  that operation; author and structurally verify the rule bundle, then report
  the execution gate rather than attempting a detached command-line fallback.
- Apply the manifest through Tiled's native Automapping engine on an
  editor-attached fixture, using **Map > AutoMap** or a bridge operation that
  invokes it. Do not treat `tiled --evaluate` as an execution fallback:
  command-line map reads are detached, and Tiled rejects `TileMap.autoMap` on
  detached maps. A command-line probe may document that capability gap, but it
  cannot prove a rule passed.
- Assert the expected output-layer name, exact coordinates, local tile IDs,
  and no unexpected cells. Render the bounded fixture to inspect direction,
  joins, offsets, and transparency.
- Change or erase an input tile and run the same proof again. Verify that the
  cleanup pass removes or normalizes obsolete output. Run unchanged input a
  third time and require the second and third outputs to be identical.
- If native AutoMap execution is unavailable, save only the rule bundle and
  report **authored but execution-unverified**. Do not call it working merely
  because the rule map parses or layer names look correct.

## Integration with sample-level generation

`/tiled-ai-add-sample-level` consumes an existing, verified rule bundle; it
does not create rules from arbitrary tileset art. It may still create a
Wang-only sample when no compatible bundle exists. If its live-editor bridge
cannot execute Automapping safely, it must preserve that fallback and report
the companion rule bundle instead of editing an open map through another
process.

## Result links

Return clickable links to the saved rule map, `rules.txt`, proof input, proof
output, and an unchanged TSX when useful. State the source mapping, targeted
layers, registration scope, cleanup strategy, exact assertions, and whether
execution passed or remains unverified.
