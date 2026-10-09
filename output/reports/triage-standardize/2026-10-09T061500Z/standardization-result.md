Standardization result · Back

# Standardization result

## Scope and baseline

Whole repository at the current working tree. The shipped [`standards-document.md`](C:/Users/srive/.agents/skills/triage-standardize/references/standards-document.md) remains `Shipped default`; repository [`AGENTS.md`](../../../AGENTS.md) remains the project-specific precedence source. No `.aiignore` or `.triageignore` was created or changed.

## Applied changes

| # | Change | Before | After | Verification |
| --- | --- | --- | --- | --- |
| CHANGE01 | Release command discovery | Validation commands were split between helper documentation and contributor guidance. | Added [`documentation/maintenance-readme.md`](../../../documentation/maintenance-readme.md) with the complete repository check sequence and generated-output ownership. | All listed commands run successfully. |
| CHANGE02 | Live integration boundary | MCP/editor verification was described in skills but not in one repository-level release guide. | Added a focused smoke scenario requiring setup, revision inspection, minimal mutation, editor verification, and explicit save authorization. | Documentation review; no live Tiled/MCP session available in this run. |
| CHANGE03 | Gallery builder ownership | `scripts/build_wang_gallery.py` was tracked without a durable supported-use reference. | Documented it as maintained repository tooling with bounded output and verification expectations. | Repository link validation passed. |
| CHANGE04 | Temporary artifact classification | Tracked `tmp/` files had no maintained-surface explanation. | Added [`tmp/README.md`](../../../tmp/README.md) and root README structure guidance; classified the files as historical authoring material, without deletion or movement. | Documentation review; no artifact deletion performed. |

## Deferred

- No `.aiignore` was added because no concrete protected path beyond existing repository instructions and `.gitignore` was identified.
- No module, dependency, ownership, or runtime architecture was changed; those remain potential `$triage-rearchitect` work only if a concrete integration problem appears.
- No live editor/MCP or downstream game-runtime test was run; those require external environments.

## Verification evidence

- `python scripts/sync-client-skills.py --check` — passed.
- `python scripts/validate-skills.py skills --expected-count 12 --require-openai-metadata` — passed.
- `python scripts/validate-skills.py .agents/skills --expected-count 12 --require-openai-metadata` — passed.
- `python scripts/validate-skills.py .claude/skills --client claude --expected-count 12` — passed.
- `python scripts/validate_repository.py` — passed.
- `git diff --check` — passed.

