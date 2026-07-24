## C3 — Weir, the Rule Language, and Weirpacks, its Distribution Unit

*Charter: the declarative language in which a grammar rule is written as data — grammar, lexer, parser, AST, lowering, optimizer, parse cache, error surface, in-rule tests, and the `.weirpack` archive that makes a rule set distributable; the `expr` combinators Weir lowers onto and the hand-written Rust linters it competes with are out of scope.*

- **T1 — essence.** A checker whose rules are compiled code can only be extended by rebuilding it. Making a rule *data* — a small declarative language over a token stream — separates the people who write rules from the people who maintain the engine. The minimum surface is a match expression, replacement metadata, and assertions carried inside the same artifact, so a rule validates itself. Distribution needs one thing more: an archive binding a rule set to a manifest, so third parties ship rules without touching the engine. Rules must lower onto the engine's existing matching primitives, never a second matcher.

- **T2 — current machinery.** Weir is line-oriented: five statement forms (`#`, `let`, `expr`, `test`, `allows`) in `weir/parsing/stmt.rs`, twelve expression forms in `parsing/expr.rs`, lexed by `lex_weir_token`. `weir/ast.rs` holds `Ast`, `AstStmtNode`, `AstExprNode`, `AstVariable`; `AstExprNode::to_expr` lowers each node onto existing combinators — `SequenceExpr`, `LongestMatchOf`, `Filter`, `UnlessStep`, `UPOSSet`, `DerivedFrom`. `WeirLinter` reads reserved `let` names and implements `ExprLinter` at chunk or sentence scope. `harper-core/build.rs` scans the rule directory and generates the registry macro. `weirpack/` zips rules, `manifest.json`, and an optional dictionary.

- **T3 — with receipts.** Born `46f4547f7` (2026-01-12, #2357) with 182 rules and 3,991 insertions. Implementation now 2,491 Rust lines across ten files (`weir/mod.rs` 699, `parsing/expr.rs` 505, `parsing/stmt.rs` 498, `ast.rs` 212, `weirpack/mod.rs` 244), plus `build.rs` 153. Corpus: 351 `.weir` files, 5,269 lines, 425 `expr` statements, 1,838 `test` and 450 `allows` assertions. `1d6374db` (#2584, 2026-01-26) wrapped `parse_str` in a 10,000-entry `LruCache` keyed on `(Arc<String>, use_optimizer)`, returning `Arc<Ast>`. Only 20 commits ever touched `weir/` or `weirpack/`.

- **T4 — the frontier.** 64 of 351 rules carry zero assertions; only 89 meet the 15-test floor `AGENTS.md:226` demands — and the generated `run_tests_for_weir_rules` passes vacuously on an empty rule. `LintKind::from_string_key` (`lint_kind.rs:62`) resolves 20 of 21 variants; `let kind "WordOrder"` cannot be written. `optimize_expr`'s UPOS-set fusion (`optimize.rs:41-48`) mutates the AST without setting `edit`, contradicting its own doc. `Weirpack::from_bytes` flattens nested paths (`mod.rs:151-158`), so same-stem rules silently collide. The Rust *writer* half — `to_bytes`, `add_rule`, `remove_rule`, `write_to`, `from_reader`, `WeirpackManifest::get_field` — has no non-test caller. Docs say `--weirpack`; the flag is `--weirpacks`.

- **T5 — future plans.** Proposed only. Issues #2510 and #2511 (both 2026-01-17, open) ask for TextMate and Tree-Sitter grammars for `.weir`, the latter noting a Tree-Sitter grammar would also let Harper lint Weir files themselves. #3652 (2026-06-13) asks whether any Weirpack registry exists; none does. #2708 (2026-02-12) requests a user-rules folder for the Obsidian plugin, a delivery path Weirpacks do not yet cover. The docs page states plainly that more test kinds are planned: "In the future, expect new types of tests to become available." No open PR touches `weir/` or `weirpack/`.

*Status ledger:* Weir language core (5 statement forms, 12 expression forms) — **shipped** · in-rule `test` assertions — **shipped** · `allows` negative assertions — **shipped** (#2602) · expression references `@name` — **shipped** (#2664) · `$word` derivation operator — **shipped, zero corpus uses** · `PROG` progressive matcher — **shipped** (2 uses) · AST optimizer — **shipped** · LRU parse cache — **shipped** (#2584) · `let scope "Sentence"` — **shipped** (#3382, 1 corpus use) · grouped rule directories — **shipped** (#3494) · Weirpack read path (`from_bytes`, `to_lint_group`, `run_tests`, `load_dictionary`) — **shipped** · Weirpack Rust write path (`to_bytes`, `add_rule`, `remove_rule`, `write_to`, `from_reader`) — **shipped-but-unreachable** · `WeirpackManifest::get_field` — **shipped-but-unreachable** · `Ast::iter_variable_values` — **shipped-but-unreachable** · `Ast::get_expr` — **shipped-but-unreachable** (tests only) · `WeirLinter::count_tests` — **shipped-but-unreachable** (tests only) · `let kind "WordOrder"` — **unreachable by construction** · `[a,b]` as first-match — **retired** (became longest-match, #3523) · `.weir` syntax highlighting grammars — **proposed** (#2510, #2511) · Weirpack registry — **proposed** (#3652) · user rules folder — **proposed** (#2708)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Ast` | T2 | `harper-core/src/weir/ast.rs:13` |
| `AstStmtNode` (5 variants) | T2 | `harper-core/src/weir/ast.rs:177` |
| `AstExprNode` (12 variants) | T2 | `harper-core/src/weir/ast.rs:84` |
| `AstVariable` (String \| Array) | T2 | `harper-core/src/weir/ast.rs:164` |
| `AstExprNode::to_expr` (lowering) | T2 | `harper-core/src/weir/ast.rs:104` |
| `WeirLinter` | T2 | `harper-core/src/weir/mod.rs:53` |
| `ChunkWeirLinter` / `SentenceWeirLinter` | T2 | `harper-core/src/weir/mod.rs:64,66` |
| `WeirScope` (Chunk \| Sentence) | T2 | `harper-core/src/weir/mod.rs:42` |
| `ReplacementStrategy` (MatchCase \| Exact) | T2 | `harper-core/src/weir/mod.rs:36` |
| `resolve_exprs` (declaration-order only) | T2 | `harper-core/src/weir/mod.rs:395` |
| `weir_expr_to_expr` (Weir inside Rust linters) | T2 | `harper-core/src/weir/mod.rs:30` |
| `lex_weir_token` | T2 | `harper-core/src/lexing/mod.rs:45` |
| `weir::Error` (11 variants) | T2 | `harper-core/src/weir/error.rs:4` |
| `Weirpack` | T2 | `harper-core/src/weirpack/mod.rs:23` |
| `WeirpackManifest` | T2 | `harper-core/src/weirpack/manifest.rs:10` |
| `weirpack::Error` (10 variants) | T2 | `harper-core/src/weirpack/error.rs:4` |
| `generate_boilerplate!` registry macro | T2 | `harper-core/src/linting/weir_rules/mod.rs:4` |
| build-time rule scanner | T2 | `harper-core/build.rs:72` |
| `harper-cli test <file>` | T2 | `harper-cli/src/main.rs:224,991` |
| `--weirpacks` lint flag | T2 | `harper-cli/src/main.rs:87`, `harper-cli/src/lint.rs:41` |
| `import_weirpack` (wasm) | T2 | `harper-wasm/src/lib.rs:531` |
| Birth of Weir | T3 | `46f4547f7` / PR #2357 / 2026-01-12 |
| `PARSE_CACHE` LruCache(10 000) | T3 | `harper-core/src/weir/parsing/stmt.rs:25`; `1d6374db` / #2584 |
| `allows` keyword | T3 | `f7ca97ea0` / #2602 / 2026-01-27 |
| Weirpack format introduced | T3 | `3a5cd68b1` / #2491 / 2026-02-03 |
| Expression references `@` | T3 | `94c12059e` / #2664 / 2026-02-05 |
| Dictionary inside a Weirpack | T3 | `0e49ee1d4` / #2922 / 2026-03-24 |
| `let scope` | T3 | `0f00de8f0` / #3382 / 2026-05-14 |
| All-`becomes` test runner | T3 | `cd4547838` / #3424 / 2026-05-19 |
| Grouped rule directories | T3 | `df18ff1cb` / #3494 / 2026-05-26 |
| `FirstMatchOf` → `LongestMatchOf` | T3 | `242ba270f` / #3523 / 2026-05-28 |
| `MAX_SUGGESTION_TRANSFORMATION_DEPTH = 100` | T3 | `harper-core/src/linting/mod.rs:339` |
| Hardcoded lint `priority: 31` | T4 | `harper-core/src/weir/mod.rs:204` |
| `WordOrder` gap in `from_string_key` | T4 | `harper-core/src/linting/lint_kind.rs:62-85` vs `:57` |
| Optimizer edit-flag omission | T4 | `harper-core/src/weir/optimize.rs:41-48` |
| Path-flattening rule-name collision | T4 | `harper-core/src/weirpack/mod.rs:151-158` |
| TS pack writer (`packWeirpackFiles`) | T4 | `packages/harper.js/src/weirpack.ts:14` |
| Duplicated four-field validation | T4 | `harper-core/src/weirpack/manifest.rs:75` vs `packages/web/src/routes/weir/studio/+page.svelte:214` |
| TextMate / Tree-Sitter `.weir` grammars | T5 | issues #2510, #2511 |
| Weirpack registry request | T5 | issue #3652 |
| User-rules folder request | T5 | issue #2708 |

*Language surface:*

**Statement forms** — dispatched by keyword in `parse_stmt`.

| Form | Meaning | Locator |
|---|---|---|
| `# text` | Comment; parsed into `AstStmtNode::Comment` and then consumed by nothing | `weir/parsing/stmt.rs:94` |
| `let NAME "value"` | Declare a string variable | `weir/parsing/stmt.rs:106` (string branch `:110`) |
| `let NAME ["a", "b"]` | Declare an array variable (only `becomes` reads arrays) | `weir/parsing/stmt.rs:132-160` |
| `expr NAME <expression>` | Bind a named expression; `main` is the rule's matcher | `weir/parsing/stmt.rs:163` |
| `allows "text"` | Assert the rule changes nothing; encoded as a `Test` with `expect == to_be` | `weir/parsing/stmt.rs:177`; `weir/ast.rs:64` |
| `test "input" "output"` | Assert `input` transforms to `output` | `weir/parsing/stmt.rs:190` |

**Reserved `let` names** — read by `WeirLinter::new`.

| Name | Required | Type | Locator |
|---|---|---|---|
| `main` (an `expr`, not a `let`) | yes | expression | `weir/mod.rs:72`, resolved `:82` |
| `description` | yes | string | `weir/mod.rs:73,86` |
| `message` | yes | string | `weir/mod.rs:74,93` |
| `becomes` | yes | string or array | `weir/mod.rs:76,100-118` |
| `kind` | no (default `Miscellaneous`) | one of 20 `LintKind` keys | `weir/mod.rs:75,132-140`; `linting/lint_kind.rs:62` |
| `strategy` | no (default `MatchCase`) | `MatchCase` \| `Exact` | `weir/mod.rs:77,120-130`; enum `:36` |
| `scope` | no (default `Chunk`) | `Chunk` \| `Sentence` | `weir/mod.rs:78,142-150`; enum `:42` |

**Expression forms** — dispatched by token kind in `parse_single_expr`.

| Syntax | Node | Lowers to | Locator |
|---|---|---|---|
| ` ` (space) | `Whitespace` | `WhitespacePattern` | `weir/parsing/expr.rs:49`; lowering `ast.rs:114` |
| `@name` | `ExprRef` | previously-bound `Lrc<Box<dyn Expr>>`; backward references only | `weir/parsing/expr.rs:51`; `ast.rs:154` |
| `$word` | `DerivativeOf` | `DerivedFrom` | `weir/parsing/expr.rs:57`; `ast.rs:116` |
| `*` | `Anything` | `AnyPattern` | `weir/parsing/expr.rs:63`; `ast.rs:109` |
| `NOUN`, `VERB`, … (16 UPOS tags) | `UPOSSet` | `UPOSSet` | `weir/parsing/expr.rs:69`; tags `harper-pos-utils/src/upos.rs:25-58` |
| `PROG` | `Progressive` | closure over `is_verb_progressive_form` | `weir/parsing/expr.rs:76`; `ast.rs:110` |
| bare word | `Word` | `Word::from_chars` | `weir/parsing/expr.rs:77`; `ast.rs:115` |
| `( a b )` | `Seq` | `SequenceExpr` | `weir/parsing/expr.rs:88`; `ast.rs:121` |
| `!x` | `Not` | `UnlessStep` (one token, unless `x`) | `weir/parsing/expr.rs:96`; `ast.rs:117` |
| `[a, b]` | `Arr` | `LongestMatchOf` (was `FirstMatchOf` before #3523) | `weir/parsing/expr.rs:105`; `ast.rs:130` |
| `<a, b>` | `Filter` | `Filter` | `weir/parsing/expr.rs:118`; `ast.rs:139` |
| any other punctuation | `Punctuation` | closure comparing `tok.kind.as_punctuation()` | `weir/parsing/expr.rs:128`; `ast.rs:147` |

**UPOS keywords** (16, all reserved as barewords): `ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB` — `harper-pos-utils/src/upos.rs:25-58`. A word matching one of these can never be matched as a literal word; `PROG` is a 17th reserved bareword.

**Weirpack manifest** — `manifest.json` at archive root. Required fields `author`, `version`, `description`, `license`, each of which must be a JSON string (`manifest.rs:62-65`, checked by `validate_required` `:75` on both read and write). Any additional field is preserved untouched via the `HashMap<String, Value>` backing store. Recognized archive members: `manifest.json`, `*.weir`, `dictionary.dict`, `annotations.json` (`weirpack/mod.rs:140-171`); everything else is silently ignored. A dictionary requires *both* Rune files or `load_dictionary` returns `None` (`mod.rs:110-121`), so a Weirpack is a rules-plus-vocabulary unit, not rules alone.

**Corpus census** (all from `harper-core/src/linting/weir_rules/`): 317 top-level `.weir` files plus 11 group directories holding 34 children = 351 rules, 328 public rule names. `expr` statements 425 (74 auxiliary beyond `main`). Expression-line feature use: `<` filter 89, `@` reference 42, `!` exception 11, `*` wildcard 4, `PROG` 2, `$` derivation **0**. `let strategy` appears 54× as `MatchCase`, 8× as `Exact`; `let scope` exactly once (`IncludingButNotLimitedToPunctuation.weir`); `let becomes [...]` array form 43×; 8 rules omit `let kind`. 16 of the 20 accepted kinds are used, led by `Usage` 80 and `Typo` 58.

**Adoption vs. Rust.** From `46f4547f7` (2026-01-12) to `HEAD`, 359 `.weir` files were added (351 survive) against 108 new `.rs` files at the top level of `harper-core/src/linting/`, 94 of whose basenames are still declared modules. Counting commits rather than files: 75 commits added at least one `.weir` rule, 102 added at least one top-level linting `.rs`, exactly 1 did both — a union of 176 rule-adding commits, of which **42.6% (75/176) chose Weir**. `AGENTS.md:232` leaves the choice open: authors are told to pick whichever of Rust or Weir fits the task.

*Trellis-relevant observation:* Weir is the cleanest available demonstration that a rule can be *data plus its own acceptance tests in one artifact* — `test` and `allows` live beside `expr main`, and a generated harness runs every shipped rule's assertions without anyone maintaining a test file. Trellis should copy that co-location and also copy the honesty check it makes possible: 64 of 351 rules ship zero assertions and the generated test still passes, so a self-testing artifact needs a *floor* enforced at registration, not merely a runner. What to avoid is the asymmetric API: the Rust pack writer is dead code while the real authoring path lives in TypeScript with its own re-implemented validation, so the same invariant is stated twice and can drift.

## Uncovered
- Whether every one of the 351 rules actually parses and passes at build time — verifying that requires `cargo test`, which the boundaries forbid; the claim that they pass rests on the generated `run_tests_for_weir_rules` existing and on CI, not on execution here.
- False-positive quality of the Weir corpus in practice. Issues like #3229 and #3679 point at behavior of specific rules, but assessing rule accuracy needs runs, not reads.
- The Weir Studio UI (`packages/web/src/routes/weir/studio/+page.svelte`, created with 442 insertions in `3a5cd68b1` / #2491) was read only far enough to establish where pack writing and manifest validation actually happen; its full behavior belongs to the web class.
- `harper.js`/plugin-level exposure of `import_weirpack` beyond the wasm entry point at `harper-wasm/src/lib.rs:531`.
