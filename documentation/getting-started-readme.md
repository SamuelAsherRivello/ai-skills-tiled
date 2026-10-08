# Getting Started

## Prerequisites

1. Install [Tiled](https://www.mapeditor.org/) and open the map or tileset you want to edit.
2. Set up the independent [rpgjs/tiled-ai](https://github.com/rpgjs/tiled-ai) bridge, its Tiled extension, and its MCP registration for your AI client. Follow that project's current installation instructions.
3. Install selected skills from this repository. These skills do not install Tiled or the bridge automatically.

## Install Skills

The shared sources are in [skills/](../skills/). The client packages give explicit installation paths:

- [Codex instructions](../.codex/INSTALL.md)
- [Claude Code instructions](../.claude/INSTALL.md)

From a project directory, `npx skills@latest add SamuelAsherRivello/ai-skills-tiled --copy` can install selected shared skills. Install only one copy of a given skill name for one client.

## Verify the Connection

Invoke `$tiled-ai-setup` in Codex or `/tiled-ai-setup` in Claude Code. The setup report checks the editor, bridge, extension, MCP registration, and live document session separately. A running bridge process alone does not prove Tiled is connected.

After setup passes, try a focused skill such as `tiled-ai-create-tileset-tsx` or `tiled-ai-create-sample-map-tmx`. The skills explain when changes stay in the editor and when a save is needed.

## Updating

Pull this repository and reinstall the selected package. The Windows installers support `-DryRun` and preserve an existing installation with a backup when `-Replace` is supplied.
