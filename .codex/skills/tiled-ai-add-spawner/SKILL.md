---
name: tiled-ai-add-spawner
description: Add or revise Tiled-authored actor spawners as reusable editor palette items whose saved type and position drive runtime spawning. Use for player, NPC, enemy, or character spawner placement and migration; do not use for direct one-off actor placement without population behavior.
---

# Tiled AI Add Spawner

## Tiled AI MCP requirement

Run `$tiled-ai-setup` first. Use the live `tiled-ai` MCP to inspect the active
map and its object layers, then create or update the spawner object and its
properties through the MCP. Verify the result and explicitly save the map;
follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

Build one coherent path from a placeable Tiled spawner item to validated runtime
configuration and visible spawned actors. Keep level layout in the map and keep
behavior defaults wherever the user and repository say they belong.

## Establish the Existing Contract

Before editing, inspect repository instructions, the active map and project,
external tilesets or object templates, object layers, origin marker, coordinate
conversion, spawner catalog/controller, actor factories, diagnostic markers,
tests, and planning artifacts. Inspect the working tree again before editing
shared TMJ, TSJ, parser, catalog, or composition files; preserve concurrent and
unrelated authored content.

Determine these material choices from the request and current code:

- which reusable palette items the editor needs;
- whether an item identifies a population role, a concrete character, or both;
- which data Tiled owns versus which defaults runtime code derives;
- required versus optional spawner types and allowed multiplicity;
- the exact validation behavior for missing, duplicate, or unsupported types;
- whether positions are cell-aligned or arbitrary pixels and which anchor is
  authoritative.

Do not expose settings in Tiled merely because the runtime has them. If the user
wants a minimal discriminator such as one `type` property, author only that
property and map it to role, character, counts, timing, initial population, and
other defaults in the runtime catalog. Conversely, preserve an established
multi-property contract unless the user asks to simplify it.

Keep role and character identity distinguishable in runtime data when multiple
characters share a population role. A compact authored type may still map, for
example, two concrete enemy characters to the same `enemy` role.

## Work Test-First

Add the smallest focused tests before production changes and run them to prove
they fail for the missing behavior. Cover the parts that apply:

- exact palette item names, count, images, class, and authored properties;
- tile-definition defaults and per-instance overrides;
- tile-object anchor and Tiled-to-game coordinate conversion;
- supported type values and source-rich validation errors;
- required spawner count, optional omissions, and allowed duplicates;
- runtime mapping from authored data to complete spawner configurations;
- independence of repeated non-player spawners;
- migration of the real map without implicit hardcoded duplicates.

When a real map references several external tilesets, load every referenced
tileset in integration fixtures. Do not weaken production validation to make an
incomplete test fixture pass.

## Author the Tiled Palette and Placements

Prefer the repository's established representation. For a visual drag-and-drop
palette, an external collection-of-images TSJ with tile objects is usually a
good fit. Use named items and editor-only previews that are recognizable on the
map. Text or simple temporary icons are acceptable when the user allows them;
matching runtime diagnostic marker art is polish, not an implicit requirement.

Keep editor icon files separate from runtime actor textures unless reuse is
intentional. Ensure spawner tile objects are excluded from ordinary terrain or
prop rendering.

Place objects only on the designated spawner object layer. Preserve stable
object IDs when converting an existing placement where practical. Calculate
TMJ coordinates from the map's actual tile size, origin, Y direction, and tile
object alignment; do not guess from screen pixels. Record chosen cells in tests
when the user delegates location choice.

For a type-selecting palette item, put the common value on the tileset item and
use an instance property only for a genuine override. Do not serialize inherited
or runtime-derived properties redundantly onto every placed object.

## Normalize, Validate, and Compose

Resolve the placed object's tileset definition by GID, merge only the supported
instance overrides, and emit the smallest normalized record the runtime needs.
Retain source object ID/name for actionable errors when useful, but do not leak
editor-only icon data into gameplay composition.

Validate the complete authored spawner list before creating actors, renderer
layers, timers, or input owners. Preserve exact user-requested error wording.
Never silently add hardcoded placements when the map is declared authoritative.
If one player/input owner is required, reject both zero and multiple player
spawners before gameplay setup.

Map normalized values through a centralized runtime catalog. The generic
spawner controller should continue receiving full validated configuration and
should not learn Tiled file details. When several spawners share a runtime role,
aggregate them rather than storing them in a single-value map that drops all but
the last.

## Migrate and Verify the Real Level

Update the requested map with explicit placements for every required actor.
Preserve unrelated layers, decorations, collision metadata, tilesets, and
concurrent character additions. Update level-authoring documentation with the
exact project, map, palette, layer, property, supported-value, required-count,
and error contracts.

Verify in increasing scope:

1. focused palette, loader, validation, and catalog tests;
2. related integration tests, the full suite, and production build;
3. Tiled's own loader or rasterizer, plus visual inspection of editor icons and
   saved placements;
4. a real browser or actual runtime showing the intended actors at authored
   positions and no duplicate hardcoded spawners;
5. diagnostic markers when available, confirming one marker per authored
   spawner and correct character-specific marker selection.

Report known platform warnings separately from errors. Do not mark an optional
stretch goal complete unless it was actually implemented, and do not claim the
editor workflow is verified solely because JSON parses outside Tiled.

Finish by giving the exact Tiled project and map paths to reopen, the authored
type-to-runtime mapping, chosen locations, validation rules, tests/build/runtime
results, and any optional polish that remains.

## Result Links

Give the exact Tiled project and map as clickable Markdown links, followed by
links to every changed runtime source file and external tileset. Link only
verified existing files; do not present a planned path as a completed result.
