# Scripts and Validation

- `sync-client-skills.py` generates the Codex and Claude Code packages. `--check` reports drift without writing.
- `validate-skills.py` checks frontmatter, UI metadata, and local Markdown links using Python's standard library.
- `validate_repository.py` checks documentation links and the portable TMX/TSX/PNG example.
- `build_starter_example.py` regenerates the checked-in starter map and preview.
- `build_figure8_example.py` regenerates the portable Figure 8 map, Wang assignments, tile art, and preview.
- `build_wang_gallery.py` is the maintained gallery builder for selected generated art and Wang companion assets; see the [maintenance guide](../../documentation/maintenance-readme.md) for its ownership and verification boundary.
- `install-codex.ps1` and `install-claude.ps1` wrap `install-skills.ps1`; use `-DryRun` before installing.
- `scripts/adapters/claude-tiled-ai-setup.md` is the Claude Code setup variant.

From the repo root, validate all packages:

```sh
python scripts/sync-client-skills.py --check
python scripts/validate-skills.py skills --expected-count 12 --require-openai-metadata
python scripts/validate-skills.py .agents/skills --expected-count 12 --require-openai-metadata
python scripts/validate-skills.py .claude/skills --client claude --expected-count 12
python scripts/validate_repository.py
```

These are repository checks, not live editor or downstream runtime tests. For release changes, follow them with the focused Tiled/MCP smoke scenario documented in the [maintenance guide](../../documentation/maintenance-readme.md).

On Windows, follow [AGENTS.md](../../AGENTS.md) before launching a helper process.
