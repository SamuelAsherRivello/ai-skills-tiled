# Tiled AI Skills

Art generation plus MCP-backed workflows for editing an open
[Tiled](https://www.mapeditor.org/) project. Run setup before any skill that
edits the live editor; it verifies the `rpgjs/tiled-ai` bridge and connection.

## Setup

| Skill | What it does |
|---|---|
| [Tiled AI Setup](../skills/tiled-ai-setup/SKILL.md) | Set up and verify the Tiled AI bridge before map edits. |

## Map

| Skill | What it does |
|---|---|
| [Tiled AI Create Sample Map TMX](../skills/tiled-ai-create-sample-map-tmx/SKILL.md) | Create a layered floor, walls, and objects sample map from one tileset. |
| [Tiled AI Create Tileset Automapping TSX](../skills/tiled-ai-create-tileset-automapping-tsx/SKILL.md) | Author and verify map-scoped Automapping rules for an existing tileset. |

## Tileset

| Skill | What it does |
|---|---|
| [Tiled AI Copy Tileset Colliders TSJ](../skills/tiled-ai-copy-tileset-colliders-tsj/SKILL.md) | Copy verified collider geometry with the live editor. |
| [Tiled AI Create Tileset Autotiling TSX](../skills/tiled-ai-create-tileset-autotiling-tsx/SKILL.md) | Add and visually verify Wang terrain metadata on an existing tileset. |
| [Tiled AI Create Tileset PNG](../skills/tiled-ai-create-tileset-png/SKILL.md) | Generate an original Scene Sheet PNG from a style, world, and tile-size brief. |
| [Tiled AI Create Tileset TSX](../skills/tiled-ai-create-tileset-tsx/SKILL.md) | Convert tile-sheet art into an inspected external tileset. |
| [Tiled AI Update Tileset Colliders TSJ](../skills/tiled-ai-update-tileset-colliders-tsj/SKILL.md) | Inspect and update existing collider shapes through Tiled AI. |

## Object

| Skill | What it does |
|---|---|
| [Tiled AI Create Character](../skills/tiled-ai-create-character/SKILL.md) | Create an animated character with Tiled AI placement data and runtime integration. |
| [Tiled AI Create Object](../skills/tiled-ai-create-object/SKILL.md) | Create a tested, independently placeable object through Tiled AI. |
| [Tiled AI Create Pickup Object](../skills/tiled-ai-create-pickup-object/SKILL.md) | Create a pickup object and its reusable runtime path. |
| [Tiled AI Create Spawner Object](../skills/tiled-ai-create-spawner-object/SKILL.md) | Create map-authored actor spawners through the live editor. |
