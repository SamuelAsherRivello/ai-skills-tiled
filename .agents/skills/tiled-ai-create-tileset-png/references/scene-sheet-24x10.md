# Scene Sheet 24x10 v1

**Format ID:** `scene-sheet-24x10-v1`

**Layout codename:** `tileset-layout-wang-mixed`

This is a composed environment sheet with a repeatable cell grid, not a claim
that every cell is an independently useful Tiled tile. The exact layout
template is [scene-sheet-layout-reference.png](scene-sheet-layout-reference.png),
a 384x160-pixel, 24-column by 10-row Retro Dungeon sheet at 16x16 pixels per
cell. Its placement and silhouette, including the small support pieces on the
far right, are the layout contract. The image derives from the user-supplied
`Tileset_Dungeon.png`; its original creator and license were not provided.
The codename describes the layout's intended Mixed Wang companion. The
composed image itself has no Wang assignments; make and verify a separate
companion before calling an output Wang-ready.
Support another square or rectangular cell size by multiplying the same 24x10
cell layout. Render style is supplied by the user's brief; the format does not
require retro pixel art. The output has no spacing or margin outside the
canvas. Every material must remain legible at the requested native cell size.

## Layout contract

Recreate the reference image's structural arrangement exactly when changing
theme or cell size. Scale its cell coordinates to the requested size; preserve
the silhouette, wall bands, openings, and transparent gaps. Do not treat the
four broad regions below as permission to redraw the layout. The same canvas
size and grid alone do not establish the same format:

| Region | Grid area | Required arrangement |
| --- | --- | --- |
| Upper-left interior | columns 1-10, rows 0-8 | One enclosed room. Keep its one-cell side and bottom perimeter walls, thicker top wall face, rectangular inner floor, and the exact outer footprint. |
| Upper-right exterior | columns 12-23, rows 0-6 | One main exterior wall assembly with a large rectangular void, a narrow vertical opening, wall cap and face below, plus the detached vertical, corner, and end support pieces on the right. Keep each piece in its reference position. |
| Lower-middle transition | columns 12-13, rows 6-9 | A two-cell-wide stair or theme-equivalent transition, directly below the exterior wall. |
| Lower-right liquid | columns 14-22, rows 7-9 | Liquid directly below the exterior wall ledge, bounded by the same right-hand support pieces. |

The original sheet has transparent negative space between the left room and
right assembly, inside the large exterior opening, and around the detached
right-hand pieces. Preserve those gaps unless the user explicitly requests a
different layout. Do not move a support piece into a gap or fill an opening
with theme decoration. Keep region boundaries on the cell grid where the
artwork is intended to be tileable. Decorative overhangs may cross cell
boundaries; preserve their appearance without assuming they are valid
standalone cells.

A wall may depict height inside a single grid cell. Preserve the relative
depth of its top cap, vertical face, and lower shadow when changing themes or
building directional tiles. Check these bands across neighboring cells and
around all four corners at native size and enlarged size. Wall height does
not change the 24×10 grid or the requested cell dimensions.

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

The Retro Dungeon, Retro Forest, and Retro Street examples each have a
separate 16x16 Wang companion and a three-tile basic sample. Their mixed sets
are verified only for the recorded Figure 8 footprint. Do not copy one
theme's local IDs to another generated theme.
