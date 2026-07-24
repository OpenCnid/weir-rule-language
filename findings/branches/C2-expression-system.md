## C2 — The Expression System: Composable Matchers Over the Token Stream

*Charter: the combinator layer (`harper-core/src/expr/`) and its `Pattern` ancestor (`harper-core/src/patterns/`) that let a rule declare a token shape instead of hand-rolling a scanner — not the individual rules built on it, and not the Weir language that compiles down to it.*

- **T1 — essence.** A checker that flags phrases needs a way for a rule to say "tokens shaped like this" without every rule hand-rolling a scanner. The invariant is a closed algebra: primitives that match one token, a literal, or a boundary; combinators that sequence, alternate, repeat, optionalise, negate, and narrow; and the guarantee that any composite is itself usable as a primitive. Each carries one operation — given a cursor into a token stream, return the matched window or nothing. The sweep that finds matches lives outside, so rules stay declarative and readable.

- **T2 — current machinery.** Two layered traits in `harper-core`. `patterns::Pattern` matches from a slice's start and returns a length; `SingleTokenPattern` narrows that to one token, and bare closures implement it. `expr::Step` returns a signed cursor delta; `expr::Expr` returns a `Span<Token>`. Blanket impls lift Pattern into Step into Expr, one way only. `SequenceExpr` is the fluent builder nearly every rule uses; around it sit `All`, `FirstMatchOf`, `LongestMatchOf`, `Optional`, `Repeating`, `Filter`, `UnlessStep`, `ExprMap`, `WordExprGroup`, and the zero-width anchors `AnchorStart`/`AnchorEnd`. `ExprExt::iter_matches` sweeps non-overlapping matches; `ExprLinter` drives it.

- **T3 — with receipts.** `patterns/` was born 2024-09-01 `6107594e`; `a8fb0c6d` (#1393, 2025-06-13) moved it under `expr/`, touching 103 files, +1,829/−1,619, deleting twelve pattern files including `sequence_pattern.rs` and `pattern_map.rs`. Today `expr/` is 23 files / 2,718 lines, `patterns/` 16 files / 930. `sequence_expr.rs` is 792 lines: 64 hand-written `pub fn` plus 66 `gen_then_from_is!` expansions emitting four methods each. 279 files implement `ExprLinter`; `lint_group/mod.rs` holds 224 `insert_expr_rule!` calls. Tests: 59 in `expr/`, 14 in `patterns/`.

- **T4 — the frontier.** `IntoBoxedExpr` (expr/mod.rs:202) has zero callers repo-wide, a duplicate of `AsBoxedExpr` born in the same commit `854a7626` (#3670). `PronounBe` ships fifteen tests and no non-test caller since #2944. `DocPattern` and `PatternExt::find_all_matches` (patterns/mod.rs:49–140) are reached only from `#[cfg(test)]`. The negative branch of `Expr::run` (expr/mod.rs:81) is unreachable — no in-tree `Step` returns negative. Zero-width negation is missing: `Invert` takes `Box<dyn Pattern>` and consumes a token, so `Invert::new(AnchorStart)` will not compile (#3848).

- **T5 — future plans.** All open and unmerged. #2934 (hippietrail, 2026-03-15, +228/−37) adds `run_rev`/`step_rev` across all 23 `expr/` files so rules can walk backwards through preceding context. #3850 (2026-07-18, agent-authored) adds `expr::Not`, a zero-width assertion accepting any `Expr`, closing #3848. #2994 proposes a capture range for `SequenceExpr`; #3107 adds `patterns/dictionary_token.rs`; #3263 a `Word` constructor for standard case combinations; #3032 a `CharSlice` with `==`; #3266 direct `Token` equality helpers; #3748 an adverbial-particle builder method; #3717 probability-aware `UPOSSet`.

*Status ledger:* `Expr` trait + blanket lifts (`Pattern`→`Step`→`Expr`) — **shipped** · `SequenceExpr` fluent builder — **shipped** · combinators `All`/`FirstMatchOf`/`LongestMatchOf`/`Optional`/`Repeating`/`Filter`/`UnlessStep` — **shipped** · dispatch accelerators `ExprMap`/`WordExprGroup` — **shipped** · zero-width anchors `AnchorStart`/`AnchorEnd` — **shipped** · domain exprs `DurationExpr`/`TimeUnitExpr`/`SpelledNumberExpr`/`ReflexivePronoun`/`MergeableWords`/`SimilarToPhrase`/`SpaceOrHyphen`/`FixedPhrase` — **shipped** · `ExprExt::iter_matches` traversal — **shipped** · `PronounBe` — **shipped-but-unreachable** · `IntoBoxedExpr` — **shipped-but-unreachable** · `DocPattern` / `PatternExt::find_all_matches` / `MatchIter` — **shipped-but-unreachable** (test-only) · negative-delta branch of `Expr::run` — **shipped-but-unreachable** · `Pattern::matches -> Option<NonZeroUsize>` — **retired** (#1124 in, #1153 out five days later, to permit zero-width matches) · `SequencePattern` / `ExactPhrase` / `pattern_map.rs` / `PatternLinter` / `any_capitalization.rs` — **retired** · `expr::Not` zero-width negation — **proposed** (#3850) · reverse matching `run_rev`/`step_rev` — **proposed** (#2934) · `SequenceExpr` capture range — **proposed** (#2994) · non-greedy `Repeating` — **not built** (limitation documented in-tree)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Pattern` trait (`matches` → `Option<usize>`) | T2 | harper-core/src/patterns/mod.rs:42 |
| `SingleTokenPattern` (+ blanket impl for closures) | T2 | harper-core/src/patterns/mod.rs:112, :126 |
| `Step` trait (signed cursor delta) | T2 | harper-core/src/expr/step.rs:8 |
| `impl Step for P: Pattern` (the one-way lift) | T2 | harper-core/src/expr/step.rs:12 |
| `Expr` trait (`run` → `Option<Span<Token>>`) | T2 | harper-core/src/expr/mod.rs:68 |
| `impl Expr for S: Step` | T2 | harper-core/src/expr/mod.rs:72 |
| `ExprExt::iter_matches` (live traversal) | T2 | harper-core/src/expr/mod.rs:139 |
| `OwnedExprExt` (`or`, `and`, `but_not`, `or_longest`) | T2 | harper-core/src/expr/mod.rs:165 |
| `SequenceExpr` | T2 | harper-core/src/expr/sequence_expr.rs:12 |
| `gen_then_from_is!` macro (4 methods per POS quality) | T2 | harper-core/src/expr/sequence_expr.rs:17 |
| `All` / `FirstMatchOf` / `LongestMatchOf` | T2 | harper-core/src/expr/{all,first_match_of,longest_match_of}.rs |
| `Optional` / `Repeating` / `Filter` / `UnlessStep` | T2 | harper-core/src/expr/{optional,repeating,filter,unless_step}.rs |
| `ExprMap<T>` (expr→payload lookup) | T2 | harper-core/src/expr/expr_map.rs:19 |
| `WordExprGroup<E>` (first-word hash dispatch) | T2 | harper-core/src/expr/word_expr_group.rs:13 |
| `AnchorStart` / `AnchorEnd` (zero-width) | T2 | harper-core/src/expr/anchor_start.rs:9, anchor_end.rs:11 |
| `Word` / `WordSet` / `UPOSSet` / `AnyPattern` | T2 | harper-core/src/patterns/{word,word_set,upos_set,any_pattern}.rs |
| `ExprLinter` (the consumer trait) | T2 | harper-core/src/linting/expr_linter.rs:40 |
| Rename `Pattern` → `Expr` | T3 | `a8fb0c6d`, PR #1393, 2025-06-13 |
| Birth of `patterns/` + `PatternLinter` | T3 | `6107594e`, 2024-09-01 |
| First adopters (`MultipleSequentialPronouns`, `RepeatedWords`) | T3 | `9f180f6c`, `e3bf6bea`, 2024-09-02 |
| `NonZeroUsize` return type, added then reverted | T3 | `8b2135b0` (#1124) → `bbb980da` (#1153), 2025-04-24 → 2025-04-29 |
| Removal of unused patterns | T3 | `087e99f2`, PR #1141, 2025-04-26 |
| `ACO` → `Word` rename | T3 | `f37fcd2c`, PR #1149, 2025-04-29 |
| `ExactPhrase` retired | T3 | `2c3f0c65`, PR #1361, 2025-06-04 |
| Authorship shift (expr/: Dunbar 57 of 81; patterns/: Potter 80 of 133) | T3 | `git log --format=%an -- harper-core/src/{expr,patterns}/` |
| `IntoBoxedExpr` (dead duplicate) | T4 | harper-core/src/expr/mod.rs:202 |
| `AsBoxedExpr` (the live one) | T4 | harper-core/src/expr/mod.rs:218 |
| Both born in one commit | T4 | `854a7626`, PR #3670, 2026-06-24 |
| `PronounBe` (tests only) | T4 | harper-core/src/expr/pronoun_be.rs:5; PR #2944 merged 2026-03-25 |
| `DocPattern` / `MatchIter` (test-only reach) | T4 | harper-core/src/patterns/mod.rs:132, :67 |
| Unreachable negative-delta branch | T4 | harper-core/src/expr/mod.rs:81 |
| `Invert` (Pattern-only, consumes one token) | T4 | harper-core/src/patterns/invert.rs:18 |
| "no way to match when not at the start" | T4 | issue #3848, 2026-07-18 |
| Weir's `Not` lowered to token-consuming `UnlessStep` | T4 | harper-core/src/weir/ast.rs:117 |
| No non-greedy `Repeating` (documented in-tree) | T4 | harper-core/src/linting/best_of_all_time.rs:27 |
| `SpaceOrHyphen` reallocates two boxes per cursor | T4 | harper-core/src/expr/space_or_hyphen.rs:12 |
| `PrepositionalPrecederPattern` reached only via free fn | T4 | harper-core/src/patterns/prepositional_preceder.rs:57 |
| `expr::Not` (zero-width negation) | T5 | PR #3850, opened 2026-07-18 |
| `run_rev` / `step_rev` reverse matching | T5 | PR #2934, opened 2026-03-15 |
| `SequenceExpr` capture range | T5 | PR #2994 |
| `patterns/dictionary_token.rs` | T5 | PR #3107 |

*Trellis-relevant observation:* The lift is one-way — every `Pattern` becomes an `Expr`, never the reverse — and after the 2025-06 rename the two traits still coexist, so a user hits a compile error the moment they try to combine a leaf-level negator with a zero-width anchor (#3848); a composable expert system should pick one match contract and express the "simplified" tier as constructors over it, not as a second trait. Conversely, the `Expr`-returns-a-span contract is worth copying: because a match is a `Span` rather than a boolean, the sweep (`iter_matches`) is written once and every rule inherits non-overlapping traversal, caching, and context slicing for free. The frozen leaves are the tell for how much survives: `patterns/` has taken three commits since 2026-03-26 while `expr/` kept moving, so the layer that ossifies is the one whose contract could not grow.

## Uncovered
- The Weir language and `weirpack` (explicitly out of charter) — touched only where `weir/ast.rs:117` proves how `Not` is lowered onto `UnlessStep`.
- The 300 individual rules in `harper-core/src/linting/` — sampled only for caller counts and for two in-tree limitation comments; their correctness and false-positive classes belong to another class.
- Runtime/allocation cost of `SequenceExpr` composition is reported structurally (boxed `dyn Expr` per step, per-run allocation in `SpaceOrHyphen`), never measured: the read-only constraint bars running `cargo bench`.
- `harper-wasm` / `harper.js` surface any `Expr` reaches was not traced; no `expr::` symbol appeared in the pnpm packages during the grep sweep of Rust sources, but the JS side was not read.
- PR #2934's claim that the negative-delta branch never fires was corroborated structurally (every in-tree `Step` impl returns `0` or a cast `usize`) but not by executing the asserts.
