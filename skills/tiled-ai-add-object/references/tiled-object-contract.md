# Tiled Object Contract

Use this reference after inspecting the target repository. Repository-native
conventions override the illustrative names below.

## Choose the Representation

Use a tile object when the artwork should appear in the Tilesets panel and be
placed visually. Use an ordinary rectangle, point, ellipse, polygon, or polyline
object when the shape is gameplay metadata without tile artwork. Use a painted
tile layer only for repeated grid-cell terrain whose placements do not need
independent identity or state.

## One Logical Palette Item

For static art, one image-collection tileset entry may reference the editor and
runtime image directly when their dimensions and padding are suitable.

For animated, oversized, or heavily padded art:

1. Preserve the original runtime sheet unchanged.
2. Determine each runtime frame size/count and the first frame's visible alpha
   bounds.
3. Generate one editor preview canvas using the map tile size by default.
4. Fit the visible art proportionally and center it; use nearest-neighbor
   scaling for pixel art.
5. Reference only that preview from the image-collection tile.
6. Store the runtime image, frame width/height/count, duration, idle frame, and
   playback properties separately on the tile.

Keep TSJ `tilewidth`, `tileheight`, tile `imagewidth`, tile `imageheight`, and
placed TMJ object `width`/`height` synchronized with the editor selection
footprint. Use TSJ `objectalignment` and `tileoffset` to preserve the intended
visual anchor without moving the authored runtime position.

## Class and Property Precedence

Define reusable fields in the Tiled project class, asset-specific values on the
tileset tile, and instance overrides on the placed map object. Normalize them in
that order:

```text
project class defaults --> tileset tile defaults --> placed object overrides
```

Tiled JSON versions may serialize an assigned class as `class` or legacy
`type`. Follow the repository's supported Tiled version and loader behavior;
avoid rewriting unrelated saved-map formatting.

## Placement and Coordinates

Place visual props on the established object layer, commonly a Y-sorted props
layer. A bottom-center anchor usually gives one stable ground-contact point for
authored position, sensor alignment, and render depth. Convert Tiled's top-left,
positive-Y-down pixel coordinates once at the normalization boundary into the
game's coordinate system.

Do not derive runtime position from transparent frame bounds. If a preview is
cropped or fitted, retain runtime frame dimensions and anchor metadata so editor
presentation cannot change game scale or collision.

## Collision Versus Sensors

Blocking geometry enters movement/navigation obstacle collections. Sensor
geometry detects overlaps but must stay out of movement and projectile obstacle
collections unless explicitly requested.

Attach reusable local geometry to the tileset tile when every instance shares
it. Normalize the shape relative to the runtime anchor and true runtime frame,
not a cropped editor preview. Preserve supported rectangle, circle/ellipse, and
polygon shapes according to the repository contract.

## Runtime State

Each placed object owns its state. For an enter-triggered one-shot decoration,
track current occupant identities, armed/disarmed state, playback, completion,
and disposal. Trigger only on outside-to-inside transitions, avoid playback
restart or implicit queueing, reset to the declared idle frame, and rearm only
under the requested exit rule.

Use stable entity IDs when multiple entities can overlap one sensor. Filter by
the declared supported entity types and living/active state.

## Verification Checklist

- Source and preview image dimensions and PNG transparency are correct.
- The tileset exposes exactly one logical placeable item.
- Preview and placed selection bounds match the requested footprint.
- Runtime frame size/count and in-game scale remain unchanged by preview work.
- Class, tile defaults, and instance overrides resolve independently.
- The object is on the correct layer with the correct anchor and authored
  position.
- Collider/sensor geometry aligns and has the correct blocking classification.
- Animation trigger, loop, reset, rearm, and multi-occupant behavior match the
  request.
- Instances do not share mutable state.
- Y ordering uses ground contact where required.
- Removal/disposal stops animation and releases renderer state.
- Focused tests, broader tests, build, Tiled inspection, and runtime inspection
  pass, or unrelated failures are reported precisely.
