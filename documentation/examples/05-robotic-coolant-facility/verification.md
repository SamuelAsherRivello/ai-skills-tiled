# Robot wall-quality verification

Status: **repair pending; current gallery art is not accepted under this contract**.
This note records the 2026-10-09 review, not a new live Wang verification.

## Source and annotated acceptance criteria

The preserved [original scene](input/scene-source.png) is 1536x640, with a
64x64 cell grid. The internal room occupies columns 1-10, rows 0-8
(zero-based); the approximate count in the feedback is not a 6x6 grid.
The [current derived scene](output/scene-sheet.png) and
[current map](output/level.tmx) remain available for comparison, not as
accepted repairs. Palette inspiration came from a user-supplied screenshot;
its original creator and license were not provided. No new license is implied.

| Annotation | Source or map region | Required relationship |
| --- | --- | --- |
| 1 | Internal-room northwest corner, source cell (1,0), including continuation below | Finish its exposed outline without clipping the cap, face, or shadow. Inspect the other three corners and all perimeter directions too. |
| 3 | Northwest corners of both Figure 8 lobes, map cells (2,2) and (16,2) | Use the corrected internal-room corner 1, with its complete native footprint. |
| 6 | Internal-room top run, source cap row 0 and machinery face row 1 | Preserve both rows as anchored native-size pieces, not a cap-only crop or a compressed single tile. |
| 4 | Top runs of both lobes | Retain treatment 6, including the face, while preserving the bridge's two clear passage rows. |
| 9 | Right-lobe core, map x=19..22, y=5..8 and its surrounding boundary | Keep the non-walkable core and route around it; select the reviewed void-facing/exterior family, not the room-facing family. |

## Current observations, not repair claims

- The companion builder takes only source cell (4,0) for its north wall;
  it omits the machinery face in row 1.
- The current role key declares every inner corner equivalent to an outer
  room corner without proving the separate void-facing context.
- Local tile 10, signature 199, occurs both at room-bottom cell (3,11)
  and core-top cell (20,4). Connectivity alone cannot choose their family.
- The current map's Floor uses GID 22, which is the companion's void tile,
  not its steel floor. It also lacks the source fixture's explicit joins.
- The scene normalizer's cross-theme alpha mask is not evidence of finished
  blue bevels, outlines, or correct native wall depth.

## Identity baseline

SHA-256 values below bind these observations to the existing files. They do
not confer readiness on a changed image or ID table.

| File | SHA-256 |
| --- | --- |
| input/scene-source.png | `fb4bdbf21447bce88ea7561f366df98a02eda0f60a48ef4dd246b8d8bd070870` |
| output/scene-sheet.png | `900c3e99afa281045b9ad9cbc5c49d1b9fc0af5eb9a6aad8dec600848a85e882` |
| output/tiles.png | `b1009cb1b24cef39e2f7a3f4489793a0830142f44ab3d396d74b0137a7a67aa7` |
| output/level.tmx | `d50f367e7c444776b151c8e1c323a150cdb02ef9d1949f2d7d61a9812b760242` |

## Pending evidence

Both constrained built-in image edits returned 1942x809 rather than 1536x640.
They were rejected and did not replace any repository art. Implementation is
paused pending a choice of deterministic grid alignment with native-cell
inspection, or an explicitly authorized alternative image workflow. Neither
candidate establishes exact cell alignment from dimensions alone. A native-grid source
repair, complete role/assembly key, current-asset live cell readback,
room/void erase-and-repaint proof, and matching packaged/Tiled renders are
still required. A connected editor or older fixture cannot replace those
checks. The open editor documents belong to other projects and were not edited.

The intended composite order is Objects, Wall Details, Wall Joints, Walls,
optional Void Fill, Floor (top to bottom), with exactly one attached TSX.
The raw Wang layer must remain separately inspectable. Explicit replacement
recipes must cover the displaced drawing completely and disclose their cells.

## Independent packaging regression proof

`python scripts/test_wang_gallery.py` passed seven disposable offline tests
on 2026-10-09. Packaging now retains canonical layer data/order even without
a supplied preview, then derives native and documentation images from the
packaged map. The tests exercise joints/details, firstgid 7, a two-column atlas
with margins/spacing, opacity, hidden layers, invalid IDs and unsupported
visible features. They prove the packaging boundary, not Robot artistic
acceptance or live Tiled agreement. The original Robot bundle remains unchanged.
