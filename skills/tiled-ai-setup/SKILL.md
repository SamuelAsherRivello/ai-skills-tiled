---
name: tiled-ai-setup
description: Set up, troubleshoot, and verify the Tiled AI MCP bridge with fresh evidence from Codex and an open Tiled editor. Use when the bridge, extension, Codex MCP entry, or live editor connection is missing or needs an end-to-end check.
---

# Tiled AI Setup

Audit and, when the user has requested it, repair the local `rpgjs/tiled-ai`
bridge. A setup passes only when every row in the report passes. Never report a
partial setup as ready.

Default to a read-only audit. Installing dependencies, rebuilding the bridge,
writing bridge configuration, installing the extension, registering an MCP, or
starting a bridge requires the user's requested scope. Do not close, focus, or
otherwise alter the user's Tiled editor. Do not edit a map to test connectivity.

## Fresh Sequential Check

Start each invocation with fresh evidence. Work through the checks below in
order. Display all twelve report rows even if an earlier prerequisite fails;
mark dependent checks **Blocked** rather than guessing. Preserve independent
passes. A healthy setup should not reinstall dependencies, replace an
extension, or overwrite a Codex registration just to obtain a newer result.

1. Locate the Tiled AI checkout, Node.js, and an installed Tiled editor. Check
   the Tiled process separately; an installed executable does not prove that
   the editor is running. Do not launch, close, focus, or alter the editor.
2. Inspect the bridge dependency state. In a requested repair, run `npm ci` in
   the checkout, then run `npm run build`.
3. Run `node dist/cli.mjs init` and `node dist/cli.mjs doctor`. Preserve useful
   diagnostics and stop the repair at a failed command.
4. Inspect the installed extension at Tiled's configured extensions directory.
   On Windows, the usual location is `%LOCALAPPDATA%\Tiled\extensions`.
   Compare the installed `tiled-ai.mjs` with the built extension when both
   exist. Install only when absent or when replacement has been authorized.
5. Inspect the named Codex MCP registration with `codex mcp get tiled-ai`.
   A valid registration runs `node <bridge checkout>/dist/cli.mjs serve` over
   stdio. Do not replace an existing registration, configuration, or extension
   without showing the conflict and obtaining authorization.
6. Start or reuse the shared bridge with `node dist/cli.mjs bridge-start`.
   Confirm the configured loopback endpoint is listening or the command gives
   an existing/started bridge result.
7. When Tiled is running, ask the user to open a map and choose
   **Map → Tiled AI: Connect**. This can be silent; they must verify it in
   **Map → Tiled AI: Status**.
8. Call `get_editor_state` through the `tiled-ai` MCP. It passes only when a
   current session ID and the map opened in Tiled are both returned. A session
   proves the extension is connected; an empty session list does not.

## Bounded Dependency Recovery

If `npm ci` fails with `EPERM`/`EBUSY` while replacing a native `sharp` file,
inspect the process owning the configured bridge port and Node command lines.
Only after verifying the exact command is
`<node> <bridge checkout>/dist/cli.mjs serve`, stop those verified Tiled AI
processes, then retry `npm ci` once. Do not kill unrelated Node, Tiled, or user
processes. If the retry fails, report the locked path and process evidence.

If the bridge is repaired after Codex already launched its stdio server, the
current MCP transport can remain closed. Preserve the successful local checks,
then direct the user to restart/reconnect Codex before retrying the live MCP
row. If Tiled was connected to the stopped bridge, direct the user to choose
**Map → Tiled AI: Connect** again; do not assume reconnection.

## Tiled-Side Troubleshooting

If the menu is missing, the extension is not loaded. Verify the extension
directory, restart Tiled only with the user's authorization, then inspect
Tiled's extension console. If Status is disconnected, re-run `doctor`, ensure
the bridge is running, and have the user connect again. A listening loopback
port does not prove that Tiled's extension is loaded or connected.

## Report

Use **title case** for steps and headings. Use **Pass**, **Fail**, and
**Blocked** for statuses. Print this table in the exact order below, replacing
the comments with fresh evidence from the current invocation.

| Step | Status | Comment |
|---|---|---|
| 1. Tiled AI Checkout Available | observed status | Checkout location and readable bridge source |
| 2. Node.js Available | observed status | Executable and version used for the bridge |
| 3. Tiled Installed | observed status | Current installed-editor evidence |
| 4. Tiled Running | observed status | Fresh Tiled process evidence; do not infer from installation |
| 5. Bridge Dependencies | observed status | `npm ci` result, or audit evidence and repair action |
| 6. Bridge Build | observed status | `npm run build` result |
| 7. Bridge Configuration | observed status | `init` and `doctor` result without secrets |
| 8. Tiled Extension Installed | observed status | Installed extension path and build-match evidence |
| 9. Codex MCP Configured | observed status | `tiled-ai` registration and command evidence |
| 10. Shared Bridge Running | observed status | Fresh `bridge-start` or configured-listener evidence |
| 11. MCP Handshake / Tools | observed status | Current `tiled-ai` tool availability or transport error |
| 12. Live Tiled Communication | observed status | Fresh `get_editor_state` session and open map evidence |

Display statuses as **✅ Pass**, **❌ Fail**, or **⛔ Blocked**. Every Fail
comment must state the smallest concrete repair and the table row where the
next run resumes. Every Blocked comment must name the missing evidence or user
action. Below the table, state **MCP Readiness** and **Editor Readiness**
separately. When all rows pass, identify the active Tiled document and suggest
`$tiled-ai-add-sample-level` as the next authoring test.

## Result Links

When an active map or tileset is available, include it as a clickable Markdown
link in the final report. Link only the connected document's actual existing
file path; setup itself does not create a result file.
