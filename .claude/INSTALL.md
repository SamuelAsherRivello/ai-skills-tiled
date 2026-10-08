# Installing Tiled Skills for Claude Code

## Prerequisites

Install [Tiled](https://www.mapeditor.org/) and configure the independent [rpgjs/tiled-ai](https://github.com/rpgjs/tiled-ai) bridge and extension for Claude Code.

## Installation

From this repository in PowerShell, preview then install a project-local package:

```powershell
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

Use `-Scope User` for all projects. Select names with `-Skills`. Existing destinations require `-Replace` and receive recoverable backups. The generated package is in `.claude/skills/`. The Claude Code setup skill checks `claude mcp get tiled-ai` and uses `/skill-name` references.

## Verify

Restart Claude Code if needed, then invoke `/tiled-ai-setup`. Author changes in `skills/`, adapt the Claude setup source in `scripts/adapters/`, and regenerate packages with `python scripts/sync-client-skills.py`.
