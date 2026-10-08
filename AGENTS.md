# Repository instructions

## Source and packages

Author skills in `skills/`. Keep each skill independently installable, including required references and helper scripts. Run `python scripts/sync-client-skills.py` after source changes and `python scripts/sync-client-skills.py --check` before committing. The Codex and Claude Code package directories are generated outputs. The Claude Code setup adapter is `scripts/adapters/claude-tiled-ai-setup.md`.

## Tiled work

Use the live `rpgjs/tiled-ai` MCP bridge for skills requiring an editor connection. Inspect the active document and revision before editing; verify the result through the editor and save only when requested. Keep external TSX files and referenced images together when sharing examples. Do not claim live editor verification from file existence alone.

## Documentation and examples

Keep README counts, links, install commands, examples, and marketing images accurate. Preserve source attribution. A Tiled example must open with referenced assets present. Do not copy Blender-specific examples or 3D export rules into this repository.

## Process execution

On Windows, create no auxiliary command windows, including transient flashes. Prefer an existing MCP connection. Before launching a helper, establish no-console creation for the outer launcher and every descendant. If a required boundary is unknown or unsupported, report the operation blocked and continue independent safe work. Preserve diagnostics, bounded execution, and cleanup of owned processes.
