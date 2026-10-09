# Maintenance and release checks

This repository publishes reusable skill instructions, generated client packages, portable Tiled examples, and selected generated art. The authoritative skill sources are in `skills/`; `.agents/skills/` and `.claude/skills/` are generated projections and must stay synchronized.

## Standard repository checks

Run these from the repository root after changing skills, documentation, scripts, or examples:

```sh
python scripts/sync-client-skills.py --check
python scripts/validate-skills.py skills --expected-count 12 --require-openai-metadata
python scripts/validate-skills.py .agents/skills --expected-count 12 --require-openai-metadata
python scripts/validate-skills.py .claude/skills --client claude --expected-count 12
python scripts/validate_repository.py
```

If a source skill changed, run `python scripts/sync-client-skills.py` before the checks so generated packages reflect the source. Generated example builders are write operations; run only the builder relevant to the changed example, then rerun the validators.

## Gallery builder ownership

[`scripts/build_wang_gallery.py`](../scripts/build_wang_gallery.py) is maintained repository tooling for selected gallery assets and Wang companion outputs. Its generated results live under `output/` and the theme-specific examples under `documentation/`. It is not a general-purpose Tiled runtime or complete Wang-set generator. Changes to it should preserve source attribution and should be checked with the repository validators plus inspection of the affected packaged assets.

## Live Tiled/MCP smoke boundary

For a skill that edits an open Tiled document:

1. Run `$tiled-ai-setup` and record the bridge/editor status and revisions.
2. Inspect the active document before mutation; confirm the target path and current revision.
3. Run the smallest focused skill workflow on a disposable or explicitly selected fixture.
4. Verify the saved data through the editor, including the relevant tileset/map/object properties and a visual region when applicable.
5. Save only when the task or test fixture authorizes it, then report the document, revision, mutation, and visual result.

This smoke scenario proves the bridge/editor boundary only. Skills that integrate with a consuming game still require that project's focused tests, build, and runtime/browser scenario.

## Historical authoring material

The tracked `tmp/` directory contains retained authoring inputs and one-off verification helpers from gallery work. It is intentionally not a supported release interface. Do not use those files as canonical instructions; promote a helper into `scripts/` only when it gains a stable purpose, documented inputs/outputs, and repeatable verification.
