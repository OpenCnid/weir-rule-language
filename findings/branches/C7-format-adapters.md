## C7 — Format Adapters and the Masking Layer

*Charter: every mechanism that decides which bytes of a structured file are natural-language prose worth checking — the `Parser` trait, the `Masker`/`Mask` abstraction, the per-format crates, and language detection — but not the lint rules that later run on the prose those mechanisms extract.*

- **T1 — essence.** Any checker of natural language embedded in a structured file must first decide, byte by byte, which spans are prose and which are syntax. Two strategies exist: subtract, by running a format-aware recognizer and keeping only the spans it labels prose; or translate, by walking the document's own syntax tree and emitting prose tokens directly. Subtraction composes, because a span selector is a pure function from text to sorted, non-overlapping allowed regions — selectors stack, wrap, and filter one another. Every extracted span must keep its offset into the original file, or no correction can be applied.

- **T2 — current machinery.** `Parser` (`harper-core/src/parsers/mod.rs:24`) is one method: `parse(&self, &[char]) -> Vec<Token>`. `Masker` (`mask/mod.rs:15`) returns a `Mask` — sorted, non-overlapping allowed `Span<char>`s. `parsers::Mask<M, P>` (`parsers/mask.rs:6`) welds any masker to any parser, shifting token spans back and inserting `ParagraphBreak` across gaps. `TreeSitterMasker` selects grammar nodes by predicate; `CommentMasker` wraps it to drop ignore-directive blocks. Format crates supply only a predicate and an inner parser: html, asciidoc, ink, python use `PlainEnglish`; jjdescription, git-commit use `Markdown`. `TeX` and literate-Haskell hand-roll maskers; `Typst` translates its AST instead.

- **T3 — with receipts.** `676527ea` (2024-07-14) created the Mask pattern; the same day `0f5c0f3d` split `TreeSitterMasker` into harper-tree-sitter. `17585f32` (2024-12-28, issue #230) changed `parse(&mut self)` to `&self` across 16 files, unblocking closures and shared ownership. `0bb4ead8` (#825, 2025-03-08) moved `spellchecker:ignore` filtering out of harper-tree-sitter into a wrapping `CommentMasker`, adding `impl FromIterator<Span> for Mask`. `CommentParser::new_from_language_id` covers 28 language IDs over 25 grammar crates; `filename_to_filetype` maps 41 extensions. 23 `Parser` impls, 5 `Masker` impls, 39 harper-comments tests, 5 fuzz targets, 440 commits.

- **T4 — the frontier.** harper-wasm's `Language` enum has three variants (`harper-wasm/src/lib.rs:55`), so harper.js, Obsidian and Chrome never reach the other twenty parsers; Typst panics if its cargo feature is off (`lib.rs:75`), and line 65 holds a TODO — Markdown options are unconfigurable there. harper-cli ignores its own `markdown_options` argument (`single_input.rs:136`) and routes no `.html`. `math_mode_at_cursor` (`harper-tex/src/masker.rs:74`) consumes to EOF on an unmatched `$` (#3791, #3613). `merge_whitespace_sep` fuses adjacent comments, so one ignore directive silences the block (#2436). Python docstrings get `PlainEnglish` (#2417).

- **T5 — future plans.** Proposed, not built: PR #3757 adds YAML, #3631 MDX, #3754 Gleam comments, #3782 Sublime's `git` language ID. Open TeX work: #3833 preserves inline-math boundaries, #3835 fixes the halt-after-`$`, #3836 a multi-line capitalization false positive, #3108 masks whitespace before `%`. Issues request ReStructuredText (#2703), djot (#2704), XML (#3837), Fountain screenplays (#3245), templ (#3722), R (#3447), Nim/Mojo/Jai (#2765/#2766/#2767), a `.weir` grammar (#2511), regex preprocessing (#3450), per-line ignore comments (#3143), Obsidian tag masking (#3871), Go doc-comment conventions (#2777). PR #3402 proposes non-English languages.

*Status ledger:* `Parser` trait, non-`mut`, blanket-derived over `Ref`/`Box`/`Arc`/`Rc` — **shipped** · `Masker`/`Mask`/`parsers::Mask` composition — **shipped** · `TreeSitterMasker` + `CommentMasker` (28 language IDs, 25 grammars) — **shipped** · six doc-comment dialects (`Go`, `JavaDoc`, `JsDoc`, `Lua`, `Solidity`, `Unit`) — **shipped** · `Markdown` + `MarkdownOptions` — **shipped** (options not plumbed into harper-wasm or harper-cli) · `OrgMode`, `PlainEnglish` — **shipped** · `HtmlParser`, `AsciidocParser`, `InkParser`, `PythonParser`, `JJDescriptionParser`, `GitCommitParser`, `LiterateHaskellParser`, `TeX`, `Typst` — **shipped**, reachable only from harper-ls and (partly) harper-cli, never from harper.js · `RegexMasker` + `OopsAllHeadings` — **shipped**, sole non-test callers are `harper-wasm/src/lib.rs:324` and `:333` · `IsolateEnglish` / `is_likely_english` — **shipped** · incremental tree-sitter reparse — **proposed** (TODO, `harper-tree-sitter/src/lib.rs:26`) · in-core `parsers/typst.rs` — **retired** (deleted `1672de3f`, 2025-01-04) · in-core `harper-ls/src/git_commit_parser.rs` — **retired** (replaced by harper-git-commit, `b67d32c4`, #3681, 2026-06-24) · YAML / MDX / Gleam / RST / djot / XML — **proposed**

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Parser` trait (`parse(&self, &[char]) -> Vec<Token>`) | T2 | `harper-core/src/parsers/mod.rs:24` |
| `StrParser` blanket impl | T2 | `harper-core/src/parsers/mod.rs:28` |
| `Masker` trait | T2 | `harper-core/src/mask/mod.rs:15` |
| `Mask` (sorted non-overlapping `Span<char>`) | T2 | `harper-core/src/mask/mod.rs:21` |
| `Mask::merge_whitespace_sep` (recursive fuse) | T2 | `harper-core/src/mask/mod.rs:77` |
| `parsers::Mask<M, P>` composer | T2 | `harper-core/src/parsers/mask.rs:6` |
| `TreeSitterMasker` | T2 | `harper-tree-sitter/src/lib.rs:9` |
| `byte_spans_to_char_spans` | T2 | `harper-tree-sitter/src/lib.rs:123` |
| `CommentMasker` (ignore-directive filter, shebang trim) | T2 | `harper-comments/src/masker.rs:5` |
| `CommentParser::new_from_language_id` (28 IDs) | T2 | `harper-comments/src/comment_parser.rs:21` |
| `CommentParser::filename_to_filetype` (41 extensions) | T2 | `harper-comments/src/comment_parser.rs:86` |
| `node_condition` = `kind().contains("comment")` | T2 | `harper-comments/src/comment_parser.rs:120` |
| Doc-comment dialects `Go`/`JavaDoc`/`JsDoc`/`Lua`/`Solidity`/`Unit` | T2 | `harper-comments/src/comment_parsers/mod.rs:1` |
| `without_initiators` / `is_comment_character` | T2 | `harper-comments/src/comment_parsers/mod.rs:18` |
| `Markdown` + `MarkdownOptions` (pulldown-cmark) | T2 | `harper-core/src/parsers/markdown.rs:13` |
| `OrgMode` | T2 | `harper-core/src/parsers/org_mode.rs:131` |
| `PlainEnglish` | T2 | `harper-core/src/parsers/plain_english.rs:10` |
| `HtmlParser` (node kind `"text"`) | T2 | `harper-html/src/lib.rs:6` |
| `AsciidocParser` (5 node kinds) | T2 | `harper-asciidoc/src/lib.rs:11` |
| `InkParser` (3 node kinds) | T2 | `harper-ink/src/lib.rs:11` |
| `PythonParser` (comments + docstrings) | T2 | `harper-python/src/lib.rs:12` |
| `JJDescriptionParser` | T2 | `harper-jjdescription/src/lib.rs:6` |
| `GitCommitParser` (subject/message_line/breaking_change) | T2 | `harper-git-commit/src/lib.rs:10` |
| `TeX` + hand-written `Masker` | T2 | `harper-tex/src/lib.rs:13`, `harper-tex/src/masker.rs:8` |
| `LiterateHaskellMasker` (`text_only` / `code_only`) | T2 | `harper-literate-haskell/src/masker.rs:27` |
| `Typst` + `TypstTranslator` (AST, no mask) | T2 | `harper-typst/src/lib.rs:16`, `typst_translator.rs` |
| `CollapseIdentifiers` (`snake_case`/`kebab-case`) | T2 | `harper-core/src/parsers/collapse_identifiers.rs:13` |
| `IsolateEnglish` wrapper | T2 | `harper-core/src/parsers/isolate_english.rs:7` |
| `is_likely_english` / `is_doc_likely_english` (4 thresholds) | T2 | `harper-core/src/language_detection.rs:8`, `:13` |
| `create_ident_dict` (identifiers become dictionary words) | T2 | `harper-tree-sitter/src/lib.rs:30` |
| harper-ls parser dispatch (22 IDs + CommentParser first) | T2 | `harper-ls/src/backend.rs:343` |
| harper-cli extension dispatch (22 arms + CommentParser) | T2 | `harper-cli/src/input/single_input.rs:136` |
| `render_markdown` (pulldown-cmark + ammonia, docs only) | T2 | `harper-core/src/render_markdown.rs:6` |
| Mask pattern birth | T3 | `676527ea` (2024-07-14) |
| tree-sitter Masker split into own crate | T3 | `0f5c0f3d` (2024-07-14) |
| `harper-tree-sitter` → `harper-comments` rename | T3 | `1c69cb02` (2024-06-29) |
| Parser trait made non-`mut` (16 files) | T3 | `17585f32` (2024-12-28, issue #230) |
| Wrapping masker + `FromIterator<Span> for Mask` | T3 | `0bb4ead8` (PR #825, 2025-03-08) |
| Typst moved out of harper-core | T3 | `1672de3f` (2025-01-04) |
| `CollapseIdentifiers` (born as `Cases`, renamed) | T3 | `6ff8037f` (2024-10-01), `3e322c99` (2024-10-04) |
| Language detection prototype | T3 | `078ac694` (2024-07-06) |
| `OrgMode` parser added | T3 | `55f5e8b6` (PR #1369, 2025-06-09) |
| `OopsAllHeadings` added | T3 | `bfaa324c` (PR #2297, 2025-12-05) |
| `RegexMasker` added | T3 | `2076d2e9` (PR #2684, 2026-02-11) |
| harper-ink crate | T3 | `690100cf` (PR #1894, 2025-09-26) |
| harper-python crate | T3 | `041d5a0b` (PR #2038, 2025-10-02) |
| harper-jjdescription crate | T3 | `506dae14` (PR #2082, 2025-10-22) |
| harper-asciidoc crate | T3 | `a0aab09d` (PR #2407, 2026-01-01) |
| harper-tex crate | T3 | `12292d50` (PR #2689, 2026-02-13) |
| harper-git-commit crate (tree-sitter) | T3 | `b67d32c4` (PR #3681, 2026-06-24) |
| harper-wasm `Language` enum (3 variants) | T4 | `harper-wasm/src/lib.rs:55` |
| `LintOptions.language` in harper.js (3 strings) | T4 | `packages/harper.js/src/main.ts:77` |
| Markdown-options TODO in wasm | T4 | `harper-wasm/src/lib.rs:65` |
| Unmatched-`$` runaway in TeX masker | T4 | `harper-tex/src/masker.rs:74` |
| Incremental-parsing TODO | T4 | `harper-tree-sitter/src/lib.rs:26` |
| YAML support | T5 | PR #3757 |
| MDX support | T5 | PR #3631, issue #2702 |
| Gleam comment support | T5 | PR #3754 |
| TeX inline-math repairs | T5 | PRs #3833, #3835, #3836, #3108; issues #3791, #3613, #3224 |
| ReStructuredText / djot / XML / Fountain / templ / R | T5 | issues #2703, #2704, #3837, #3245, #3722, #3447 |
| `.weir` tree-sitter grammar | T5 | issue #2511 |
| Regex preprocessing before parsing | T5 | issue #3450 |
| Per-line ignore comments | T5 | issue #3143 |

*Trellis-relevant observation:* The whole adapter layer reduces to two composable interfaces — a pure `text -> sorted allowed spans` selector and a pure `chars -> tokens` parser — so twenty-plus formats are each about forty lines, and cross-cutting behaviours (identifier collapsing, English isolation, regex masking, heading forcing) are wrappers that need no format's cooperation. That is exactly the shape a composable expert system over user text wants: the offset-preserving span is the load-bearing primitive, because it is what lets an engine compute addresses and splice corrections back without the model ever counting characters. The cautionary half is the surface split — the same core exposes fifty language IDs through the LSP and three through WebAssembly, so capability and reach must be tracked as separate claims.

## Uncovered
- I did not read `harper-core/src/parsers/markdown.rs` past line ~220, `org_mode.rs` past line 60, `typst_translator.rs`, `offset_cursor.rs`, `harper-tex/src/masker.rs` past line 90, `literate-haskell/src/masker.rs`, or the `jsdoc`/`lua`/`solidity`/`go`/`unit` dialect bodies in full; my claims about them are confined to their declared types, entry points, and the lines I quote.
- I did not verify that every one of the 39 harper-comments tests, 10 harper-tex tests, 20 harper-typst tests, or 5 fuzz targets passes — the ground rules bar running `cargo`, so all test counts are source counts, not green-run evidence.
- I did not audit the editor plugins (vscode, chrome, obsidian, wordpress) for their own language-ID mapping tables; the harper.js three-language limit is read from `packages/harper.js/src/main.ts:77` and `harper-wasm/src/lib.rs:55` only.
- Issue and PR titles are taken from `gh` listings at read time; I did not open each thread, so the T5 entries record what was requested, not maintainer commitment.
