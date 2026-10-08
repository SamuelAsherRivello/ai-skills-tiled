# Scene Sheet 24x10 v1

![Retro Dungeon sheet](retro-dungeon.png)

`scene-sheet-24x10-v1` is a composed 24-column by 10-row environment sheet.
At 16x16 pixels per cell, the PNG is 384x160 pixels. It places an interior
room on the left, exterior wall variants at the upper right, a transition or
stairs at the lower middle, and liquid terrain at the lower right.

The first theme, **Retro Dungeon**, keeps gray-blue stone, small green moss
details, dark openings, and stairs, with blue water. The visual reference was
the user-supplied `Tileset_Dungeon.png`; its original creator and license were
not provided. This derived sheet is an art-format example, not a verified
Tiled TSX or a claim that every cell tiles seamlessly.

Planned themes using this layout:

1. **Retro Forest:** picket-fence walls; a single repeating 16x16 grass tile
   for the interior and former black areas.
2. **Retro Street:** brick walls; repeating city-street ground in those same
   areas; dark dirty-blue sewer water.

The format contract and validator ship with
[`ai-tiled-create-art`](../../../skills/ai-tiled-create-art/SKILL.md).

The [basic Figure 8 sample](retro-dungeon-basic/README.md) demonstrates the
three-tile layout before autotiling. The
[Retro Dungeon Wang companion](retro-dungeon-wang/README.md) provides the
more complex, live-Tiled-verified sample after autotiling. The composed
384x160 Scene Sheet itself has no Wang metadata.
