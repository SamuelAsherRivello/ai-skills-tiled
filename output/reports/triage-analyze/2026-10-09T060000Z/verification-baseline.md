[Overview](overview.md) · [Standardization analysis](standardization-analysis.md) · [Architecture analysis](architecture-analysis.md) · Verification baseline · [Back](overview.md)

# Verification baseline

## Discovered checks

| # | Check or scenario | Source and scope | State | Result or limitation |
| --- | --- | --- | --- | --- |
| VERI01 | `python scripts/sync-client-skills.py --check` | [`AGENTS.md`](../../../../AGENTS.md), helper guide; compares canonical `skills/` with generated Codex/Claude packages. | run | Passed: `Codex and Claude skill packages are synchronized.` |
| VERI02 | `python scripts/validate-skills.py skills --expected-count 12 --require-openai-metadata` | Helper guide; source skill frontmatter, local links, and OpenAI metadata. | run | Passed: `Validated 12 skills.` |
| VERI03 | `python scripts/validate-skills.py .agents/skills --expected-count 12 --require-openai-metadata` | Helper guide; generated Codex package metadata and links. | run | Passed: `Validated 12 skills.` |
| VERI04 | `python scripts/validate-skills.py .claude/skills --client claude --expected-count 12` | Helper guide; generated Claude package metadata and links. | run | Passed: `Validated 12 skills.` |
| VERI05 | `python scripts/validate_repository.py` | Helper guide and script; repository Markdown links plus starter/Figure 8 TMX, TSX, and PNG structural checks. | run | Passed: `Repository links and Tiled examples are valid.` |
| VERI06 | `python scripts/build_starter_example.py` | Helper guide and starter example README; regenerates checked-in map/preview. | discovered, not run | Not run because it is a write-generating command and this analysis is read-only; no claim about regeneration determinism beyond the validator result. |
| VERI07 | `python scripts/build_figure8_example.py` | Figure 8 example README; generates portable art, Wang assignments, map, and preview. | discovered, not run | Not run because it writes generated example outputs. Existing output is covered structurally by `validate_repository.py`. |
| VERI08 | `python scripts/build_wang_gallery.py` | Tracked repository script; no durable helper-guide or README command reference found. | discovered, not run | Scope and ownership are unclear; do not treat absence of a run as failure. |
| VERI09 | `scripts/validate_scene_sheet.py` | `tiled-ai-create-tileset-png` skill and Scene Sheet reference; validates generated sheet dimensions/layout. | discovered, not run | No single repository-wide fixture/command is documented for all themes; run on a named final PNG when changing that skill. |
| VERI10 | Live Tiled/MCP inspection and visual verification | [`documentation/references/tiled-ai-mcp.md`](../../../../documentation/references/tiled-ai-mcp.md) and MCP-backed skills; checks active document, revision, mutations, and visual result. | not run | No live editor/MCP session was used in this read-only repository triage. File existence cannot establish editor verification. |
| VERI11 | Downstream runtime tests for character/object/pickup/spawner skills | Individual skill contracts require consuming-game tests/build/runtime inspection. No runtime project or test suite exists in this checkout. | not available | Must be supplied by the consuming project; repository-local validation cannot prove runtime behavior. |

## Recommended verification sequence for approved changes

1. Run the focused skill/package validator and any named helper script.
2. Run all three package validations, `sync-client-skills.py --check`, and `validate_repository.py`.
3. For changed examples or assets, open the packaged Tiled files with referenced images present and perform the documented editor/visual checks; record the editor and bridge revisions.
4. For runtime-integrating skills, run the consuming project's focused tests, broader tests/build, and runtime/browser scenario.
5. Recheck documentation counts, links, attribution, and generated-package synchronization before release.

## Coverage interpretation

The passing checks provide good evidence for metadata, local Markdown links, source/package parity, and selected portable TMX/TSX/PNG invariants. They are static or fixture-level checks, not behavioral coverage. No unit, integration, end-to-end, lint, type-check, or CI command was discovered for this repository itself. That is an evidence boundary, not automatically a defect, because the repository publishes workflows and examples rather than a game runtime.

