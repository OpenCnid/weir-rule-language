## C8 — Delivery Surfaces: The Adapters That Carry One Engine To Many Hosts

*Charter: every binding, protocol adapter, and application through which a user reaches the checking engine — language server, WebAssembly build and its JS wrapper, CLI, desktop app, browser/editor/CMS extensions, shared browser lint framework, and the telemetry crate; the engine's own linting, parsing, and dictionary logic is out of scope.*

- **T1 — essence.** One engine, many meeting places. Surfaces differ in only three ways: how text arrives (a buffer, a DOM node, a screen rectangle), how corrections travel back, and what the host permits — a thread, a sandbox, an accessibility API, a byte budget. A delivery surface is therefore an adapter plus a policy: it translates positions between the engine's coordinates and the host's, persists what the engine refuses to remember, and negotiates the host's ceiling on size, memory, and permission. Everything beyond that is duplication, and duplication is where surfaces silently drift apart.

- **T2 — current machinery.** `harper-ls`'s `Backend` (backend.rs) speaks LSP: full-sync diagnostics, quick-fix code actions, six `executeCommand` verbs, three dictionary scopes, an ignored-lint store, and `Config::from_lsp_config`. `harper-wasm` exports a `#[wasm_bindgen] Linter`; `harper.js` wraps it as `LocalLinter` (same thread) and `WorkerLinter` (inline worker, `Serializer` RPC), both fed by a `BinaryModule` in full or slim glue. `lint-framework`'s `LintFramework` paints DOM highlights for Chrome, web, and `harper-editor`. `harper-desktop` pairs a Tauri shell with an egui overlay child process. `harper-cli` and `harper-stats` complete the set.

- **T3 — with receipts.** `harper-ls`: 1,737 lines over eight files (backend.rs 868), born 2024-01-17 `dd0e4de2`, 522 commits, tests only in pos_conv.rs (11). `harper-wasm`: 844 lines, 226 commits. `harper.js`: 2,261 lines, born 2024-12-15 `47ba722c`; `WorkerLinter` `7bdcaf7bf`; slim/full split `6c700f3c7`, 2026-03-30, #3050, after an Obsidian OOM. `lint-framework` extracted 2025-09-10 `353b8cd5b` (#1893), 3,320 lines. `harper-desktop`: `f96274e2`, 2026-05-12, #3324, 43 commits, 9,216 lines. `binaries.yml` ships seven targets each for harper-ls and harper-cli.

- **T4 — the frontier.** config.rs:148-154 assigns `statsPath` to `base.file_dict_path` — the stats location has never been settable, since `b5639947e`, surviving #1669; the error still says "fileDict". backend.rs:546 advertises save support with no `did_save`. `harper-desktop/.github/workflows/build_artifacts.yml` sits below the repo root, so Actions never reads it, and it invokes nonexistent recipes `build-linux`/`build-macos`. The overlay is macOS-only (`NoopBroker`, os_broker.rs:80-96; issue #3554). `strip = true` has been commented out since `91d915c5c` (2025-05-15, #1278) for a wasm-opt bug. Lint colours exist in triplicate.

- **T5 — future plans.** Proposed only. Open PRs: #3282 adds a configurable diagnostic delay to harper-ls; #3136 adds `--format github` for CI annotations (issue #3128); draft #2431 moves `LintKind` colours into core so CLI and harper.js fetch rather than restate them; #3514 adds Overleaf support and #3853 site-support feedback to the extension; #3866 documents JetBrains via LSP4IJ; #3858 adds report graphs to the web. Open issues propose Xcode (#2499), Eclipse (#2497), OnlyOffice (#2775), non-Apple desktop (#3554), a harper-cli GitHub Action (#3473), and a `harper-cli lint` REPL (#2628).

*Status ledger:* harper-ls diagnostics + code actions + six commands — **shipped** · harper-ls three-scope dictionaries and ignored-lint persistence — **shipped** · harper-ls `statsPath` config key — **shipped-but-unreachable** (parsed into the wrong field; never documented) · harper-ls `did_save` — **proposed by capability, absent in code** · `LocalLinter`/`WorkerLinter` split — **shipped** · slim WASM flavour — **shipped** · inlined dual-WASM bundling — **retired** (#3050) · release-profile `strip` — **retired** (`91d915c5c`) · `lint-framework` DOM highlighting — **shipped** (Chrome, web, harper-editor) · Obsidian CodeMirror highlighting — **shipped, reimplemented** · WordPress block highlighting — **shipped, reimplemented** · egui overlay highlighter — **shipped, macOS only** · desktop CI workflow — **shipped-but-unreachable** · `harper-stats` recording — **shipped** (harper-ls at shutdown; harper-wasm in memory) · stats visualisation — **shipped** (manual upload, `packages/web/src/routes/stats/+page.svelte`) · harper-cli `--format github` — **proposed** (#3136) · harper-ls diagnostic delay — **proposed** (#3282) · centralised lint colours — **proposed** (#2431)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Backend` (LSP server) | T2 | harper-ls/src/backend.rs:53 |
| Six `executeCommand` verbs | T2 | harper-ls/src/backend.rs:530-537 |
| `lint_to_code_actions` | T2 | harper-ls/src/diagnostics.rs:30 |
| `DocumentState` | T2 | harper-ls/src/document_state.rs:10 |
| `Config` (14 LSP keys) | T2 | harper-ls/src/config.rs:66 |
| `Linter` (wasm-bindgen) | T2 | harper-wasm/src/lib.rs:108 |
| `Linter` (TS interface, 33 methods) | T2 | packages/harper.js/src/Linter.ts:14 |
| `LocalLinter` | T2 | packages/harper.js/src/LocalLinter.ts:39 |
| `WorkerLinter` | T2 | packages/harper.js/src/WorkerLinter/index.ts:21 |
| `BinaryModule` / `SuperBinaryModule` | T2 | packages/harper.js/src/BinaryModule.ts:97,154 |
| `WasmGlueFlavor` ('full' \| 'slim') | T2 | packages/harper.js/src/BinaryModule.ts:11 |
| `Serializer` (worker RPC) | T2 | packages/harper.js/src/Serializer.ts:42 |
| `LintFramework` | T2 | packages/lint-framework/src/lint/LintFramework.ts:44 |
| `OutputFormat` (Default/Json/Compact) | T2 | harper-cli/src/lint.rs:77 |
| `Stats` / `Record` / `RecordKind` | T2 | harper-stats/src/lib.rs:16, record.rs:9,28 |
| `HighlighterService` | T2 | harper-desktop/src-tauri/src/highlighter_service/mod.rs:15 |
| `HighlighterProcess` (`current_exe highlighter`) | T2 | harper-desktop/src-tauri/src/highlighter_service/highlighter_process.rs:16 |
| `write_message` (newline-JSON framing) | T2 | harper-desktop/src-tauri/src/communication/framing.rs:6 |
| `Client` / `Server` protocol | T2 | harper-desktop/src-tauri/src/communication/mod.rs:10-13 |
| `OsBroker` trait | T2 | harper-desktop/src-tauri/src/os_broker.rs:21 |
| `Window` (transparent, click-through, always-on-top) | T2 | harper-desktop/src-tauri/src/highlighter/window.rs:20 |
| harper-ls birth | T3 | `dd0e4de2` (2024-01-17) |
| harper.js birth | T3 | `47ba722c` (2024-12-15) |
| `WorkerLinter` birth | T3 | `7bdcaf7bf` (2024-12-15) |
| slim/full WASM split | T3 | `6c700f3c7` (2026-03-30, #3050) |
| lint-framework extraction | T3 | `353b8cd5b` (2025-09-10, #1893) |
| chrome-plugin birth | T3 | `a2e0da7a` (2025-05-02, #1072) |
| vscode-plugin birth | T3 | `2dda7afaa` (2024-07-23) |
| obsidian-plugin birth | T3 | `3056b27cd` (2024-03-15) |
| harper-cli birth | T3 | `09a918065` (2024-05-15) |
| harper-desktop birth | T3 | `f96274e2` (2026-05-12, #3324) |
| `mac_broker` module | T3 | `0966f95bf` (2026-07-01, #3734) |
| `tray.rs` | T3 | `607d0f80a` (2026-07-20, #3779) |
| `just build-wasm` (two wasm-pack runs) | T3 | justfile:64-76 |
| `perl -pi -e 's/new URL(.*)/new URL()/'` dedup step | T3 | justfile:85-86 |
| binaries.yml (7 targets × 2 binaries) | T3 | .github/workflows/binaries.yml:18-113 |
| `statsPath` → `file_dict_path` misassignment | T4 | harper-ls/src/config.rs:148-154 |
| Save capability with no `did_save` | T4 | harper-ls/src/backend.rs:546 |
| Unreachable desktop workflow | T4 | harper-desktop/.github/workflows/build_artifacts.yml:1 |
| `NoopBroker` (non-macOS no-op) | T4 | harper-desktop/src-tauri/src/os_broker.rs:80-96 |
| Disabled `strip` | T4 | Cargo.toml:16-18; `91d915c5c` (2025-05-15, #1278) |
| Triplicated lint colours | T4 | harper-desktop/src-tauri/src/lint_kind_color.rs; packages/lint-framework/src/lint/lintKindColor.ts; packages/obsidian-plugin/src/lintKindColor.ts |
| Two engines inside one desktop app | T4 | harper-desktop/src/lib/EditorView.svelte:14-19 vs highlighter_process.rs:17 |
| `DISABLE_WASM_OPT=1` in the VS Code test path | T4 | justfile:335 |
| harper-ls diagnostic delay | T5 | PR #3282 |
| `--format github` | T5 | PR #3136 / issue #3128 |
| `LintKind` colours into core | T5 | PR #2431 (draft) |
| Overleaf support | T5 | PR #3514 |
| JetBrains via LSP4IJ | T5 | PR #3866 |
| Non-Apple desktop | T5 | issue #3554 |
| harper-cli GitHub Action | T5 | issue #3473 |
| harper-cli REPL mode | T5 | issue #2628 |

*Trellis-relevant observation:* The reusable pattern is the narrow `Linter` interface (packages/harper.js/src/Linter.ts) implemented twice — in-process and across a worker boundary — so a caller picks its isolation without changing a call site; the desktop repeats it at process scale, with the overlay child linting locally and asking the parent only for config and dictionary over newline-delimited JSON, which keeps user text on one side of the boundary. The pattern to avoid is per-surface restatement of engine-owned facts: lint colours now live in three hand-maintained copies and the desktop app ships two independent builds of the engine. Telemetry is the model to copy — records stay on disk locally and reach a summary view only by the user uploading their own file.

## Uncovered
- No byte size for either WASM artifact is recorded anywhere in the tree, and building is forbidden, so the concrete cost of the WASM boundary is stated only as build steps and the qualitative full/slim split, never as a number.
- `harper-python` is a tree-sitter parser for Python comments and docstrings consumed by `harper-ls` (backend.rs:399), not a Python binding; no Python-language delivery surface exists in this clone.
- The runtime behaviour of `LintFramework`, `Highlights`, and `RenderBox` was read but not exercised; DOM-coordinate correctness claims are outside what static reading can support.
- `packages/components` (1,356 lines) and `packages/harper-editor` (1,415 lines) were surveyed only at dependency level; their internal structure is unmapped.
- Which specific LSP clients actually invoke `HarperRecordLint` in practice is unverified — the command is attached to every suggestion code action, but client-side execution was not observed.
