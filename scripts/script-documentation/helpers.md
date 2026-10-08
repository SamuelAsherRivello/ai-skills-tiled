# Scripts and Validation

- `sync-client-skills.py` generates the Codex and Claude Code packages. `--check` reports drift without writing.
- `validate-skills.py` checks frontmatter, UI metadata, and local Markdown links using Python's standard library.
- `validate_repository.py` checks documentation links and the portable TMX/TSX/PNG example.
- `build_starter_example.py` regenerates the checked-in starter map and preview.
- `install-codex.ps1` and `install-claude.ps1` wrap `install-skills.ps1`; use `-DryRun` before installing.
- `scripts/adapters/claude-tiled-ai-setup.md` is the Claude Code setup variant.

From the repo root, validate all packages:

```sh
python scripts/sync-client-skills.py --check
python scripts/validate-skills.py skills --expected-count 11 --require-openai-metadata
python scripts/validate-skills.py .codex/skills --expected-count 11 --require-openai-metadata
python scripts/validate-skills.py .claude/skills --client claude --expected-count 11
python scripts/validate_repository.py
```

On Windows, follow [AGENTS.md](../../AGENTS.md) before launching a helper process.
