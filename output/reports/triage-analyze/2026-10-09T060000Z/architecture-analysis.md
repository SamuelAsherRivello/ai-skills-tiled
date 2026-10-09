[Overview](overview.md) · [Standardization analysis](standardization-analysis.md) · Architecture analysis · [Verification baseline](verification-baseline.md) · [Back](overview.md)

# Architecture analysis

## Module map

```text
skills/                         authoritative, independently installable skill packages
  <skill>/SKILL.md              workflow contract and safety/verification instructions
  references/                    local contracts and MCP guidance
  scripts/                       skill-specific deterministic helpers
.agents/skills/                 generated Codex projection with UI metadata
.claude/skills/                 generated Claude projection plus setup adapter
scripts/                        repository-level sync, install, validation, and example builders
documentation/                  orientation, references, examples, art formats, and marketing
output/                         checked-in generated examples and authoring results
```

## Contracts, ownership, and direction

The primary contract is textual and procedural rather than an object-oriented runtime API. `skills/` owns the canonical behavior; client directories are projections; repository scripts validate or generate artifacts; documentation and examples demonstrate supported usage. This is a sensible dependency direction for an installable skill library.

Most MCP-backed skills explicitly require setup, current-document/revision inspection, verified mutation, and explicit save behavior. The shared [`tiled-ai-mcp.md`](../../../../documentation/references/tiled-ai-mcp.md) establishes revision and visual-verification expectations, while individual copies preserve independent installability. The architecture favors composition of narrow workflows—art generation, TSX conversion, autotiling/automapping, objects, spawners, and collider operations—over one monolithic skill.

## Pressure points and candidates

| # | Candidate | Evidence | Expected value | Risk | Non-goals | Urgency | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ARCH01 | Make the source-to-client projection a release contract | Three maintained representations exist per skill family and are currently synchronized by `sync-client-skills.py --check`; manual omission remains possible if contributors skip it. | Prevent client drift as the catalog grows. | Low; the current generator is already the boundary. | Do not redesign skill content or merge client formats. | Medium | Standardize |
| ARCH02 | Define the external MCP/editor verification seam | Most mutation skills depend on live `rpgjs/tiled-ai`; repository validators cover portable files but not editor state, revisions, visual results, or downstream runtime behavior. | Make release confidence and responsibility explicit at the repository boundary. | Medium; requires access to Tiled, the bridge, and compatible consuming projects. | Do not embed the bridge or claim repository-only tests can replace it. | Medium-high | Rearchitect if structural; otherwise Standardize |
| ARCH03 | Decide ownership of gallery and temporary authoring tools | `build_wang_gallery.py` and tracked `tmp/` helpers are not discoverable through durable docs, while generated gallery assets are checked in. | Reduce ambiguity about supported tooling and cleanup ownership. | Low-to-medium; historical assets may have external value. | Do not delete or move artifacts based only on non-reference. | Medium | Standardize |
| ARCH04 | Add consumer-facing contract fixtures only if needed | There is no runtime package, test suite, or downstream game in this repository; skills such as object/character/pickup/spawner workflows describe runtime integration but cannot test it here. | Improve confidence at the actual integration seam when a supported consumer exists. | High scope risk if the repository tries to become a game-runtime test harness. | Do not invent a runtime architecture inside this library. | Low until a consumer is selected | Rearchitect / user decision |

## Score rationale

Architecture is 72/100: boundaries and dependency direction are clear, skills are narrow, and external integration contracts are explicit. The deductions reflect projection duplication, ambiguous ownership of some checked-in authoring artifacts, and the unavoidable absence of local seams for live MCP/editor and downstream runtime behavior. A broad rearchitecture is not currently justified; the next structural decision should be driven by an actual release or consumer failure.

