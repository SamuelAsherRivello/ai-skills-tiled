# Space Tech Robot: Future variants

Five additional `scene-sheet-24x10-v1` compositions at **64×64 pixels per
cell** (24 columns × 10 rows; **1536×640 RGBA**). They follow the
`tileset-layout-wang-mixed` arrangement: an enclosed room at upper left,
exterior walls and detached supports at upper right, a stair transition below,
and a coolant basin at lower right. Floors are viewed from above; selected
raised walls and stair pieces show vertical side faces.

| Sheet | Treatment |
| --- | --- |
| [future-1.png](future-1.png) | Dark slate armor, amber hazard stripes, cyan status lights. |
| [future-2.png](future-2.png) | Light ceramic and titanium panels, orange maintenance bands, blue vents. |
| [future-3.png](future-3.png) | Weathered gunmetal, copper framing, turquoise instrumentation. |
| [future-4.png](future-4.png) | Mid-grey titanium, bold orange chevrons, yellow indicators. |
| [future-5.png](future-5.png) | Sand-ceramic walls, charcoal floor, orange vents, amber coolant. |

The user-supplied grey/orange robot-map screenshot inspired the square panel
materials and safety accents. Its central explosion was deliberately excluded.
The original creator and license of that screenshot were not provided. The
separate user-supplied tan-square robot screenshot inspired `future-5.png`;
its original creator and license were likewise not provided. The
arrangement comes from the project's
[`scene-sheet-layout-reference.png`](../../../../../skills/tiled-ai-create-tileset-png/references/scene-sheet-layout-reference.png),
which derives from a separate user-supplied dungeon sheet whose original
creator and license were also not provided. The previously approved
[`space-tech-robot.png`](../../space-tech-robot.png) guided the geometry.

Each variant was generated separately with the built-in image tool, scaled to
the required canvas, visually inspected, and passed
`validate_scene_sheet.py --tile 64x64`. The small far-right supports in
`future-2.png` and `future-3.png` were completed using matching generated wall
art and the approved support footprint. The main silhouettes of `future-1.png`
through `future-3.png` were aligned to the approved room and exterior footprints.
These are composed scene sheets; the
validator establishes image format and dimensions, not independently seamless
tiles or Wang metadata. Generated panel seams can deviate by a few pixels from
the nominal cell grid.
