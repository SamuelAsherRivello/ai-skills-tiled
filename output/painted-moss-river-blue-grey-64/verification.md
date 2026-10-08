# Slate-walled clearings: Wang verification

- Author and date: Codex, 2026-10-08
- Source scene: `../painted-moss-river-blue-grey-scene-64x64.png`
- Imported source image: `image-a344f4a3976e4296d61b633b1401b9acfc65c9089fea053b441559f2edc245a3.png`
- Exact tileset: `slate-clearings.tsx` (25 cells, 5 columns by 5 rows, 64x64 pixels)
- Local tile ID to eight-value Wang ID: `mapping.json`, in Tiled's N, NE, E, SE, S, SW, W, NW order
- Wang set: `Slate-walled clearings`, mixed; painted color: `Walkable grass`
- Excluded IDs: 21 dark void, 22 water, 23 basic wall, 24 stairs

The set contains 21 authored masks. The verified 50x50 Figure 8 at
`../tiled-ai-sample-level/slate-clearings-figure-8-wang.tmx` uses 13 of them:
`7, 28, 31, 112, 124, 127, 193, 199, 223, 241, 247, 253, 255`.
Tiled 1.12.2 painted all 200 expected footprint cells with the matching local
IDs; no footprint cell was blank, wrong-facing, or outside the painted shape.
All 2500 Floor cells use ID 20. The 4x4 dark core uses ID 21 and was placed
after Wang painting. The Objects layer is empty. The two room renders and
bridge render showed continuous slate borders and correct corners.

Erasing and repainting the upper-left exterior corner restored local ID 1.
An isolated one-cell paint at (1,1) was rejected with `MISSING_WANG_PATTERN`
for Wang ID `[0,0,0,0,0,0,0,0]` and changed no cells. This is **Limited
Wang-ready** for the tested Figure 8 footprint, not arbitrary painting.
All mixed masks outside the 21 IDs in `mapping.json` are unsupported; the
eight authored masks not exercised by this fixture are not separately proven.
