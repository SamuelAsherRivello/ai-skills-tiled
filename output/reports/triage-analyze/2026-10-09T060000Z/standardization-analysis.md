[Overview](overview.md) · Standardization analysis · [Architecture analysis](architecture-analysis.md) · [Verification baseline](verification-baseline.md) · [Back](overview.md)

# Standardization analysis

## Active baseline

[`standards-document.md`](C:/Users/srive/.agents/skills/triage-standardize/references/standards-document.md) has not been customized by user. Using defaults. Repository instructions in [`AGENTS.md`](../../../../AGENTS.md) take precedence and establish `skills/` as the authoring source, `.agents/skills/` and `.claude/skills/` as generated outputs, and `scripts/sync-client-skills.py` as the synchronization boundary.

## Findings

| # | Area | Observed evidence | Desired standard / delta | Severity | Recommended owner |
| --- | --- | --- | --- | --- | --- |
| STND01 | Source and generated packages | 12 source skills, 12 Codex packages, and 12 Claude packages are present; `sync-client-skills.py --check` passes. | Preserve one-way source ownership and keep the check in release/PR verification. No current delta observed. | Informational | Standardize |
| STND02 | Documentation and counts | README advertises 12 skills; `documentation/skills-readme.md` has 12 skill rows; README's ten Wang examples align with the ten numbered examples, while `figure-8-autotiling` and `starter-map` are separate fixtures. | Keep count language scoped to the named collection. Current claims are consistent. | Informational | Standardize |
| STND03 | Maintained artifact surface | `tmp/gallery-contact.png`, `tmp/verify_wang_gallery.py`, and `tmp/wang_layout_redo.py` are tracked but have no references from maintained Markdown or scripts found in the scan. | Mark authoring artifacts as historical, move them behind a documented boundary, or document their supported use before more contributors rely on them. Static non-reference is not proof of dead code. | Medium | Standardize / user decision |
| STND04 | Gallery builder discoverability | `scripts/build_wang_gallery.py` is tracked and contains substantial generation logic, but the helper guide and README do not document it as a supported command. | Document its inputs/outputs and verification, or explicitly label it internal/historical. | Medium | Standardize |
| STND05 | AI readiness | `AGENTS.md`, README, CONTRIBUTING.md, `.gitignore`, helper documentation, and per-skill contracts are discoverable; `.aiignore` is absent. | Current safety guidance is useful. An optional `.aiignore` is only warranted if a concrete protected local path exists beyond `.gitignore` and AGENTS rules; absence alone is not a defect. | Low | Standardize / user decision |

## AI readiness

| # | Area | Status | Evidence | Practical improvement |
| --- | --- | --- | --- | --- |
| READY01 | Canonical agent instructions | nailed | [`AGENTS.md`](../../../../AGENTS.md) defines source ownership, generated outputs, Tiled/MCP boundaries, Windows process safety, and save behavior. | Keep it authoritative when adding new client packages. |
| READY02 | Command discovery | partial | [`scripts/script-documentation/helpers.md`](../../../../scripts/script-documentation/helpers.md) lists validation and sync commands; bridge build commands are described in the setup skill, not a repository runtime manifest. | Add a concise “release checks” section to the root docs if publishing cadence increases. |
| READY03 | Project orientation | nailed | README explains `skills/`, generated packages, scripts, documentation, examples, and bridge dependency. | Maintain links and counts when catalog size changes. |
| READY04 | Definition of done | partial | CONTRIBUTING asks contributors to run relevant checks and report limitations; AGENTS requires sync checking, but no CI workflow or single release checklist is present. | Make the existing helper command sequence the explicit contribution checklist. |
| READY05 | Maintenance relationships | nailed | AGENTS and CONTRIBUTING link source-to-generated synchronization; example READMEs link builders and packaged assets. | Document the gallery builder relationship or classify it as non-maintained. |
| READY06 | Safety boundaries | partial | `.gitignore` protects credentials/cache/editor state; AGENTS covers Tiled save behavior and no-console Windows execution; no `.aiignore` exists. | Add only repository-specific protected-path patterns if a concrete need is identified. |

## Repository integrity

| # | Candidate | Classification | Evidence and limits | Recommended owner |
| --- | --- | --- | --- | --- |
| INTG01 | `tmp/gallery-contact.png`, `tmp/verify_wang_gallery.py`, `tmp/wang_layout_redo.py` | orphan candidate | Tracked and unreferenced by the scanned Markdown/Python/PowerShell/YAML surface. They may be historical authoring inputs or manually invoked helpers; no deletion is justified from static non-reference. | Standardize / user decision |
| INTG02 | `scripts/build_wang_gallery.py` | orphan candidate | No durable documentation reference found, despite substantial generation code. Framework-free discovery is unlikely, but manual use or release history may explain it. | Standardize |
| INTG03 | `output/` generated art and Tiled artifacts | not assessed | Many files are referenced by example/documentation trees or may be authoring outputs; a complete semantic ownership audit would require understanding gallery history and external consumers. | User decision |
| INTG04 | Forward-looking `variants/future-*.png` assets | intentionally future-facing | The containing README labels these variants as future-oriented; absence from current examples is not stale documentation. | No action |
| INTG05 | README, example, and reference links | not stale | `validate_repository.py` reports all repository links and portable Tiled examples valid; this is link/fixture evidence, not proof of visual/editor behavior. | No action |

## Score rationale

Standardization is 84/100: strong source ownership, naming/metadata consistency, documentation orientation, and passing integrity validators; deductions are for undocumented tracked authoring artifacts and a partially distributed verification/release contract. No score reduction is made for the missing `.aiignore`.

