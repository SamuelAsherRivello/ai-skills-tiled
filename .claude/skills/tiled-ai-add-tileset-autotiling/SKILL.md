---
name: tiled-ai-add-tileset-autotiling
description: Add and verify Wang autotiling metadata on one existing Tiled tileset through the live Tiled AI MCP. Use after art has already been converted into an external tileset.
---

# Tiled AI Add Tileset Autotiling

Turn one existing external tileset into a **verified** Wang-autotiling
tileset. This skill authors metadata; `/tiled-ai-add-tileset` is responsible
for turning a source image into the external TSX first.

## Triage a collection before choosing an asset

A collection page that calls its entries "Wang" or "Blob" is an index, not a
shared source profile. Inspect and prove each child asset independently. In
particular, distinguish these three cases before authoring anything:

- **Configured source TSX:** open the supplier's exact TSX and inspect every
  returned Wang set. Legacy TSX files can contain both `<terraintypes>` and
  `<wangsets>`; Tiled 1.12.2 can expose the former as a generated `Terrains`
  corner set alongside the named Wang set, with identical assignments. Do not
  treat the duplicate as a second art family or save a rewritten TSX just to
  remove it. Choose the explicitly named supplier set for a proof and report
  the duplicate import result.
- **Labelled template plus artwork:** a diagnostic panel is not tileset art.
  Crop or otherwise isolate the artwork panel into a reviewed, disposable
  source image before creating the TSX. A grid across labels and art creates
  the wrong local IDs, even when its dimensions happen to divide cleanly.
- **Artwork with no metadata:** follow **Create a missing role key**. The
  image establishes the candidate roles only after the written table and a
  rendered fixture prove them.

Before a large fixture, run a small exterior-boundary probe through
`paint_terrain`. A valid source may still be unusable through this MCP's
single-colour paint operation: a two-colour legacy set can reject a paint on
an empty layer with `MISSING_WANG_PATTERN`, then reject the same paint over an
unchanged opposite-colour base with `BOUNDARY_CONFLICT`. Preserve the source
and its diagnostics; do not manufacture an all-zero tile or manually replace
boundary art. Report it as **Not Wang-ready through the current MCP** for that
requested footprint. This is a tool/fixture limitation, not evidence that the
supplier's TSX is corrupt or unusable in Tiled's UI.

## Inspect and classify

- Run `/tiled-ai-setup`, identify the exact open TSX with
  `get_editor_state`, then inspect it with `get_map_info`, `list_wang_sets`,
  and all pages of `get_tileset_images`. Never copy tile IDs from another
  tileset, even when both use the same image layout.
- When a supplied PNG has a title band, transparent spacing, or irregularly
  sized art, `inspect_tileset_image` may correctly report an unknown grid.
  Search the artwork directory and its project for a companion external TSX
  before treating the image as unusable. Open that exact TSX and inspect it:
  a collection-of-images TSX can establish the local IDs and source regions,
  but **does not** establish Wang roles merely by doing so. When no source key
  exists, create the missing, reviewed local-role table and a disposable proof
  fixture as described in **Create a missing role key**; do not stop solely
  because the supplier omitted metadata.
- Do not start Wang authoring from a TSX whose grid was guessed from a packed
  atlas. First prove that the exact TSX has meaningful local IDs for the
  intended terrain family. Props, trees, character sprites, and decorative
  overlays are not Wang candidates merely because they share an image file
  with terrain. Report **Not Wang-ready** with the source-layout evidence when
  the grid/collection definition is not established; do not create metadata
  just to make the terrain panel appear populated.
- Use an explicit reference block in the art, a companion key, an existing
  correct map, or a documented source profile to establish *every* Wang ID.
  Do not infer a profile from image dimensions, a filename, a familiar visual
  style, or the apparent colour of pixels. This prohibits borrowing a named
  profile without evidence; it does not override the required missing-key
  authoring workflow below. A rendered test, not the preview, establishes
  fitness.
- Classify the **matching topology**, not the subject matter of the artwork:
  - An **edge** set has values only at indices `0, 2, 4, 6`; it suits paths,
    fences, rails, and other side-connected features. Two edge colours require
    all 16 combinations for unrestricted painting.
  - A **corner** set has values only at `1, 3, 5, 7`; it suits patches and
    terrain transitions. Two corner colours require all 16 combinations;
    three corner colours require 81 for unrestricted painting.
  - A **mixed** set has both kinds of values. A two-colour mixed set is 256
    masks when complete. Reduced mixed sets are valid only for the explicitly
    identified family of masks they contain.
- For each candidate tile, record the eight samples in Tiled's clockwise order
  `N, NE, E, SE, S, SW, W, NW`. Keep the mapping as a table of **local tile
  ID -> eight values**. There is no safe visual shortcut for a facing, a
  concavity, or an asymmetric decorative tile.
- Treat duplicate art as a variant only when it has the exact same eight-value
  signature. It can make selection non-deterministic; it does not fill a
  missing mask. A rotated-looking tile is still a different local tile and
  needs its own explicit assignment. Do not rely on an editor transform to
  invent it.
- Report one of these outcomes:
  - **Wang-ready**: the requested fixture paints and renders with no missing,
    blank, wrong-facing, or broken cells.
  - **Limited Wang-ready**: a named footprint family works, but a required
    mask is absent. State the missing Wang IDs and reject wider requests.
  - **Not Wang-ready**: the authored role table cannot be made internally
    consistent, lacks a mask needed by the requested fixture, or fails visual
    proof. Preserve the evidence; do not save failed metadata.

### Create a missing role key

When a supplied tileset has no tile-ID-to-Wang reference, author one instead
of treating the omission as a terminal condition. This is a reviewed design
step, not an unchecked pixel inference:

1. Preserve the supplier's art and source TSX. Work in a separately named
   disposable TSX/map pair whenever the editor can create one; otherwise make
   the Wang change in Tiled's Undo history and save only after proof succeeds.
2. Inspect every local tile image at full size. For each tile, explicitly
   record the material's continuations on the four cardinal boundaries and
   any required diagonal ownership. Classify it as an edge, corner, or mixed
   candidate, then write a local **tile ID -> eight Wang values** table in a
   mapping note beside the fixture. The note must identify the source image,
   exact TSX, local IDs, author/date, intended painted colour, and any
   deliberately excluded decorative or bridge tiles.
3. For a path/fence/rail candidate, begin with one painted edge colour and
   set all diagonal indices to `0`; assign only the observed cardinal
   continuations. For terrain-transition art, use a mixed table only where
   both cardinal and diagonal ownership are explicitly recorded. Never fill
   unobserved masks with a visually similar tile.
4. Create the Wang set from that complete reviewed table, build the smallest
   coverage-first fixture for its declared footprint, and render it. A clean
   render plus `read_region` verification promotes the table from
   **provisional** to **verified for that footprint**. A missing-pattern
   error, wrong-facing join, gap, or overlap is a failed hypothesis: undo the
   Wang mutation, revise the written table, and retry with a new request ID.
5. Save the TSX and fixture only after a successful proof. Retain a limited
   mapping note with unsupported masks and its rendered evidence; do not
   advertise unrestricted painting merely because the first fixture passed.

The supplied image itself is sufficient authority to construct this
provisional table. Do not ask the caller for a pre-existing Wang key merely
because one was omitted: inspect, author, test, revise, and document the
actual limit. Ask only when the source cannot be read or the required visual
role is genuinely absent and new art would be needed.

## Reference profile: canonical 47-tile Blob

The public Stagecast Blob sheets are a reliable *reference profile*, not a
generic rule for every 7x7 image. They demonstrate a reduced two-edge /
two-corner mixed set with 47 masks rather than the 256 masks of a complete
two-colour mixed set. The linked Stagecast `wangbl.png` and its Dungeon,
Trench, Islands, Commune, and Bridge sheets use the same role layout with
different artwork; the separately described OpenGameArt template is labelled.

The OpenGameArt **Wang 'Blob' Tileset** download is a different, useful
reference artifact: it is a CC0 542x240 composite with a labelled panel and
an 8-columns-by-7-rows, 32px artwork panel. Its description says "7x8"; use
the explicit matrix orientation, not that ambiguous prose, when deriving
local IDs. The artwork panel has 56 physical cells: all 47 Blob masks plus
nine duplicates. For that exact file only, the row-major printed-mask table
is:

```text
16  20  32 112 | 28 124 116  64
29 125 119 193 | 23 223 245  80
31 247 193   0 | 21  71 213  81
31 241   4  84 | 85  68  93 113
23 221 124 113 | 17  28 127 241
 5  95 255 253 |117  87 215 209
 0   7 199 199 |197  69  65   1
```

Each displayed number is its Wang mask, not its local ID: after isolating the
art panel, local ID is its zero-based row-major position and each bit maps in
the normal `N, NE, E, SE, S, SW, W, NW` order. The duplicate masks are
`193`, `31`, `23`, `124`, `113`, `28`, `241`, `0`, and `199`. The two compact
Stagecast packings below are separate sheets; never reuse this 8x7 local-ID
table for the 7x7 or 6x8 layout.

- The profile paints one region colour. The contrasting background is **unset
  (`0`)**, not a second Wang colour. Do not create two colours just because the
  artwork visibly contains two materials.
- For a labelled canonical sheet, let `m` be its printed decimal mask. Bit
  weights are exactly `N=1, NE=2, E=4, SE=8, S=16, SW=32, W=64, NW=128`, so
  map it mechanically with `wangid[i] = 1 if (m & (1 << i)) else 0`. Use the
  actual colour ID returned by Tiled in place of `1` when authoring.
- Its allowed mask set is:

  ```text
  0, 1, 4, 5, 7, 16, 17, 20, 21, 23, 28, 29, 31,
  64, 65, 68, 69, 71, 80, 81, 84, 85, 87, 92, 93, 95,
  112, 113, 116, 117, 119, 124, 125, 127,
  193, 197, 199, 209, 213, 215, 221, 223,
  241, 245, 247, 253, 255
  ```

  The 7x7 packing has 49 cells because mask `0` appears three times; the 6x8
  packing has one duplicate `255`. Map every duplicate to its same mask; do
  not mistake the packing extras for new terrain roles.
- A quick corroboration (not a substitute for the labelled source) is the
  Blob invariant: for each side, a filled corner on either end requires the
  intervening edge to be filled. Equivalently, an unset edge must have both
  adjacent corners unset. This produces outer and inner corners while keeping
  a connected central fill. It is deliberately directional: the profile can
  draw the designated blob material over its background, but not the inverse.
- Use this profile only after confirming the exact source identity or a
  pixel-for-pixel/role-for-role companion reference. A merely similar 7x7
  sheet is **Not Wang-ready** until its own tile-to-mask key is supplied.

Sources for this profile: [Stagecast Blob reference](https://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob.html),
[labelled Blob variants](https://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob_g.html), and
[Tiled terrain-set documentation](https://doc.mapeditor.org/en/stable/manual/terrain/).

## Author the terrain set

1. Create or update one `edge`, `corner`, or `mixed` Wang set from the source
   art. Keep the eight-index order used by Tiled: top, top-right, right,
   bottom-right, bottom, bottom-left, left, top-left. A tile may have one
   assignment; variants may share an assignment. Use `mixed` whenever the
   requested topology needs both side and diagonal information, including an
   inner void whose diagonal corner cells are indistinguishable from ordinary
   floor in an edge-only set.
2. Name each colour for the **region that will be painted**. Do not label an
   edge set "wall" merely because its boundary tiles draw walls.
3. A common room-frame sheet uses a single `Walkable floor` edge colour. Its
   paint footprint includes the visual boundary cells; Tiled selects outer
   wall/corner art at that footprint's boundary and a repeated floor tile in
   its interior. For this pattern, a separate repeated `Floor` map layer may
   sit underneath the generated `Walls` renderer layer.
4. Derive all assignments from a complete source reference block. Use a
   mechanical profile mapping when the source provides one; otherwise build a
   reviewed local-ID table before editing. Do not assign a tile whose mask is
   ambiguous, and do not silently omit a mask the requested fixture needs.
   For the observed Dungeon Figure 8 **limited** profile, use one `Walkable
   floor` colour and these mixed-set assignments (the array is in Tiled's
   eight-index order):

   ```text
   0:  [0,0,1,1,1,0,0,0]  1:  [0,0,1,1,1,1,1,0]
   5:  [0,0,0,0,1,1,1,0] 12: [1,1,1,1,1,0,0,0]
   13: [1,1,1,1,1,1,1,1] 17: [1,0,0,0,1,1,1,1]
   48: [1,1,1,0,0,0,0,0] 49: [1,1,1,0,0,0,1,1]
   53: [1,0,0,0,0,0,1,1] 6:  [1,1,1,0,1,1,1,1]
   8:  [1,1,1,1,1,0,1,1] 30: [1,0,1,1,1,1,1,1]
   32: [1,1,1,1,1,1,1,0]
   ```

   Tile `31` is a decorative alternative to tile `1` in the reference art;
   give it tile `1`'s ID only when either visual variant is acceptable. A Wang
   set cannot deterministically select two different art tiles for the same
   neighbor mask. Do not invent missing masks for other sheets.
5. Save an external TSX only after a matching rendered fixture passes. For a
   limited set, save the precise allowed topology and the missing Wang IDs in
   the result; future maps must not expand its claim.

## Coverage-first proof fixtures

Build the smallest disposable fixture that reaches the masks the caller needs,
then verify both its data and rendered output. Do not treat a large attractive
map as evidence of coverage.

| Requested behaviour | Required fixture feature | What it catches |
| --- | --- | --- |
| Exterior boundary | Filled rectangle with all four turns | reversed or wrong-facing outer corners |
| Concavity / rooms | 2x2 or larger unpainted hole in a filled area | missing diagonal-aware inner corners |
| Corridors | horizontal and vertical runs, one-cell turns, a T and a plus | absent straights, caps, joins, or rotation errors |
| Sparse detail | one-cell island and one-cell notch, only when requested | unsupported isolated/concave masks |
| Blob profile | all four behaviours above, painted in the profile's declared direction | use of the non-invertible 47-mask set backwards |

- Before painting, make a required-mask inventory from the fixture's eight
  samples. For each cell, state its expected mask/signature and the local tile
  that must satisfy it. If an expected signature has no mapped tile, stop with
  **Limited Wang-ready** or **Not Wang-ready**; never let the Terrain Brush
  choose an unrelated fallback unnoticed.
- After `paint_terrain`, use `read_region` to assert that every expected cell
  is populated by a local tile with the recorded signature, and use
  `get_region_image` to check joins, orientation, transparent gaps, and visual
  inversions. Repeat the fixture after an erase/repaint near a boundary: the
  brush must also repair neighboring tiles correctly.
- A Blob set is Wang-ready only for the requested painted direction and
  tested footprint family. Do not claim it supports a reversed terrain, a
  second colour, or every arbitrary mixed mask merely because all 47 supplied
  tiles render cleanly.

### Observed collection compatibility

- **OGA Wang 'Blob' Tileset:** The exact 8x7 artwork panel and matrix above
  were imported as a disposable 32px TSX, given one mixed `Carpet` colour,
  and painted successfully in Tiled 1.12.2. A 14x10 painted rectangle with a
  2x2 unpainted core produced 136 populated cells, clean outer/inner joins,
  and a clean erase/repaint repair of an exterior corner. This is
  **Wang-ready** for the tested, one-direction Blob footprint family.
- **OGA Dirt Wang:** Its supplied legacy TSX opens with identical `Terrains`
  and `Dirt` corner sets plus a `Dirt Path` edge set. Do not recreate this
  metadata from the PNG. In Tiled 1.12.2, the named `Dirt` corner set rejected
  a colour-2 exterior on an empty map (`MISSING_WANG_PATTERN`); after a
  colour-1 base tile was placed it rejected the untouched boundary
  (`BOUNDARY_CONFLICT`). Its named `Dirt Path` edge set also rejected a
  six-cell colour-2 line over that base with `BOUNDARY_CONFLICT`. Both are
  therefore **Not Wang-ready through the current MCP** for these isolated
  fixtures. Retain the original TSX rather than recreating or weakening it.

## Figure 8 proof

For the default Figure 8, create a disposable map using the exact TSX:

- A repeated Floor layer, an empty Objects object layer, and a Walls tile
  layer in the visual order `Objects`, `Walls`, `Floor`.
- Use the same walkable tile throughout the Floor layer. Keep optional water,
  props, and other materials out of the default Wang proof so the rendered
  boundary and corner joins are easy to inspect; add them only when requested.
- Paint the **walkable footprint** on Walls, not a one-cell wall stroke: a
  10×10 left lobe, a 10×10 right lobe, and a four-tile-tall bridge between
  them. The bridge contains a two-tile-tall walkable passage, so its top and
  bottom rows become walls. Leave a 4×4 unpainted core inside the right lobe.
  This topology requires the four diagonal-aware inner-corner masks above.
- When the art has an opaque void tile, place it in the unpainted 4×4 core
  after the Wang operation so that core is visibly non-walkable. This is a
  deliberate fill, not a claimed Wang result.
- Verify the complete cell set with `read_region` and the rendered map with
  `get_region_image`. The test fails if any expected Wang cell is null,
  transparent, a wrong-facing edge, or a broken join.
- Keep positive and negative controls together. In Tiled 1.12.2, the exact
  Dungeon Figure 8 assignments above painted a clean 8x8 rectangle with local
  tile IDs `0, 1, 5, 12, 13, 17, 48, 49, 53` and a seamless rendered border.
  The same set rejected a one-cell paint with `MISSING_WANG_PATTERN` for
  `[0,0,0,0,0,0,0,0]`, changing no cells. This is evidence that it is
  **Limited Wang-ready** for room/frame footprints, not evidence of general
  mixed-terrain coverage. Never add an all-zero assignment just to silence
  that error; it must be visually identified as a legitimate source tile.

Do not widen corridors to one cell or create isolated floor cells unless the
tileset has been separately proven by the relevant coverage fixture. The Blob
profile is a candidate for these forms, not a waiver for visual verification.
`paint_terrain` works on one declared colour and cannot recover an
unrepresented pattern.

Follow the shared [MCP editing contract](references/tiled-ai-mcp.md).

## Result Links

Finish with clickable links to the saved TSX and fixture map. Name the Wang
set, colour, matching topology, source of the local-ID mapping, supported
footprint family, known missing masks, and fitness outcome.

For a preflight **Not Wang-ready** result, do not invent TSX or fixture links.
Identify the exact source image and/or TSX, its observed grid or collection
evidence, the intended art family, and the unmet prerequisite (for example,
no verified local-ID layout, no role table, or no supported MCP import path).
State that no Wang metadata was saved and name the smallest viable follow-up.
