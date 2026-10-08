# Installing Tiled Skills for Codex

## Prerequisites

Install [Tiled](https://www.mapeditor.org/) and configure the independent [rpgjs/tiled-ai](https://github.com/rpgjs/tiled-ai) bridge and extension.

## Installation

From this repository in PowerShell, preview then install a project-local package:

```powershell
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

Use `-Scope User` for all projects. Select names with `-Skills`. Existing destinations require `-Replace` and receive recoverable backups. The generated package is in `.codex/skills/`; the installer copies it to the client's `.agents/skills/` discovery directory.

## Verify

Restart Codex if needed, then invoke `$tiled-ai-setup`. For updates, pull the repo and rerun the installer with `-Replace`. Author changes in `skills/` and regenerate packages with `python scripts/sync-client-skills.py`.
