# Space Tech Robot 64px tiles and Figure 8 samples

The approved [1536x640 Scene Sheet](../space-tech-robot.png) is a composed
`tileset-layout-wang-mixed` image with 64x64 cells. It is the visual source,
not an unrestricted Wang atlas. The separately composed [24-tile companion](tiles.png)
contains 21 directional Mixed Wang roles, an opaque dark void, electric-blue
coolant, and a plain wall tile. The [builder](build_wang_companion.py) samples
the approved sheet; [mapping.json](mapping.json) records every local tile ID,
source role, and eight-value Wang assignment.

## Tiled files

- [Basic external tileset](basic/output/space-tech-robot-basic.tsx) and
  [basic Figure 8 sample](../../../../output/tiled-ai-sample-level/space-tech-robot-figure-8-basic.tmx).
- [Mixed Wang external tileset](wang/output/space-tech-robot-wang.tsx),
  [8x8 room probe](wang/output/space-tech-robot-wang-probe.tmx), and
  [Wang Figure 8 sample](../../../../output/tiled-ai-sample-level/space-tech-robot-figure-8-wang.tmx).
- [Five further 64px scene-sheet variants](variants/README.md), named
  `future-1.png` through `future-5.png`. These are art variants and do not
  inherit this Wang metadata.

The two TSX files each have their MCP-imported image beside them. The basic
sample uses local tile `23` for all 88 boundary cells, tile `20` across all
2,500 Floor cells, and opaque void tile `21` in the right 4x4 core. Its Objects
layer is empty.

## Wang fitness

The `Robot rooms` Mixed Wang set paints one colour, `Walkable steel floor`,
over an otherwise unset background. Its 21 authored masks cover the tested
two-room Figure 8: two 10x10 rooms, a four-tile-tall bridge with a two-tile
walkable passage, and a 4x4 unpainted core in the right room. The Figure 8
requires masks `7, 28, 31, 112, 124, 127, 193, 199, 223, 241, 247, 253,
255`; all 200 painted cells were read back with the expected local tile IDs
and Wang signatures. The core was then filled with opaque void tile `21`.

Tiled 1.12.2 painted a separate 8x8 exterior-boundary probe with all four
corners, and its render showed continuous metal wall bands and floor. Erasing
and repainting the probe's northwest corner restored local tile `1` and the
correct rendered corner. An isolated one-cell paint returned
`MISSING_WANG_PATTERN` for mask `0` without changing a cell. This set is
**Limited Wang-ready** for the tested room/frame footprint; masks outside the
21 recorded roles are unsupported.

Four bridge joins in the Figure 8 use a separate `Wall Joints` overlay above
the Wang-painted `Walls` layer. Their map cells and local IDs are `(22,23)→0`,
`(27,23)→9`, `(22,26)→1`, and `(27,26)→4`. The underlying Walls cells retain
their correct Wang assignments. The floor uses one repeated 64x64 panel tile,
so its regular panel seams are intentional. Both samples use a 50x50-cell map
with 64x64 pixels per cell.

The approved robot sheet was inspired by a user-supplied screenshot; its
original creator and license were not provided. The companion only samples
that approved art and adds an opaque dark void for the core.
