# Retro Street source and composition

The [384×160 Scene Sheet](../retro-street.png) was generated for
`scene-sheet-24x10-v1` with 16×16 cells. The original
[source concept](source-concept.png) was made with the built-in image
generation tool, then [composed](compose_scene_sheet.py) into the original
format's upper-left room, upper-right exterior wallset, lower-middle stairs,
and lower-right water footprints. The composition script requires Pillow. It
takes brick, cobblestone, stair, and sewer pixels from that generated concept
and repeats one identical cobblestone tile in clear ground cells.

The image generation prompt was:

> Use case: stylized-concept. Asset type: original pixel-art environment tileset concept for a Tiled 2D game. Primary request: Retro Street theme for a fixed 24-column by 10-row scene sheet at 16x16 pixels per cell (384x160 final target). Keep the composition of a classic dungeon sheet: a large bounded room in the upper left, a separate exterior wall group in the upper right, narrow transition steps near the lower middle, and liquid terrain in the lower right. Replace walls with reddish brown urban brick masonry; replace every black/open space and the bounded room's floor with the SAME small repeatable one-cell cobblestone city-street ground tile. Lower-right water is dark dirty blue sewer water. Crisp orthographic top-down 1990s game pixel art, hard pixel edges, no antialiasing, no modern lighting, no text, no characters, no objects, no border or framing. Materials should read clearly at 16x16. Align every edge to an invisible square grid, leave no gutters between tiles. Ensure the cobblestone ground repeat is consistent across interior and exterior spaces. Give distinct brick wall caps, corners, side runs, and an urban transition stair/curb. The image should be a sheet, not an isometric scene.

The Scene Sheet validator confirmed a 384×160 RGBA image and exact equality
for clear cobblestone cells `(3,3)`, `(4,3)`, `(3,4)`, and `(0,1)`.
The source concept and resulting artwork were generated and composed by Codex
from the user's requested format and theme. The original dungeon layout
reference supplied by the user had no known creator or license information.
