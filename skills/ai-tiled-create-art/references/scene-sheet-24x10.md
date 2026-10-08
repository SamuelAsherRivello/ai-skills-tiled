# Scene Sheet 24x10 v1

**Format ID:** `scene-sheet-24x10-v1`

This is a composed environment sheet with a repeatable cell grid, not a claim
that every cell is an independently useful Tiled tile. The source example was
384x160 pixels and suggests a 24-column by 10-row layout at 16x16 pixels.
Support another square or rectangular cell size by multiplying the same 24x10
cell layout. Render style is supplied by the user's brief; the format does not
require retro pixel art. The output has no spacing or margin outside the
canvas. Every material must remain legible at the requested native cell size.

## Layout contract

Preserve the source's visual ordering and approximate footprints:

| Region | Approximate cells | Purpose |
| --- | --- | --- |
| Left composition | columns 1-10, rows 0-8 | Bounded room or ground area with an inner repeating floor |
| Upper right composition | columns 12-23, rows 0-6 | Exterior walls, openings, corners, and variants |
| Lower middle | columns 12-13, rows 6-9 | Stairs or a theme-equivalent transition |
| Lower right | columns 14-22, rows 7-9 | Water, sewer, or other liquid terrain |

Leave the negative space between sections transparent unless the theme
explicitly replaces it with repeatable ground. Keep region boundaries on the
cell grid where the artwork is intended to be tileable. A reference image can
contain decorative overhangs; preserve their appearance without assuming they
are valid standalone cells.

## Theme briefs

- **Retro Dungeon:** Gray-blue stone walls and floor, small moss accents, dark
  openings, gray stairs, and blue water with readable repeating ripples. Keep
  the source palette family outside the water.
- **Retro Forest:** Picket-fence walls. Use one seamless 1x1-cell grass floor
  tile for the inner floor and for areas that were black openings; repeat the
  same tile without visible seams. Keep the transition and liquid regions in
  their established positions unless the user asks to replace them.
- **Retro Street:** Brick walls, a city-street ground tile repeating in the
  same places as the forest grass, and dark dirty-blue sewer water. Keep the
  same region order and cell grid.

These briefs are starting points, not a closed theme list. Use the user's
style, world, and size words as the primary creative direction.

## Verification

For a cell size of 16x16, the final PNG must be exactly 384x160 pixels. Run:

`python <skill-folder>/scripts/validate_scene_sheet.py <image.png> --tile 16x16`

The validator checks the PNG header, color mode, and dimensions. It cannot
prove visual tile alignment or seamless repetition; inspect those separately.
When identical cells are required, pass their clear coordinates with
`--repeat-cells '3,3;4,3;3,4'`; the validator then compares decoded pixels.
Only select cells without wall, fence, or other overlays.
If the user asks for a Tiled tileset, the existing import skill must still
assess whether the art is actually grid-importable.

The Retro Dungeon example therefore has a separate 16x16 Wang companion.
Its mixed set is verified only for the recorded Figure 8 footprint; do not
copy its local IDs to another generated theme.
