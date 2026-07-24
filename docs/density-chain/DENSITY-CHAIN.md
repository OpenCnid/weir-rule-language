# The Harper Density-Trellis — a branching chain-of-density map of an engine we did not build

**Status: orientation artifact, reverse-engineered 2026-07-23/24 from a clone at `efa59c33`.**
PROPOSED / unratified. Subordinate to everything it summarizes. This map studies
[`Automattic/harper`](https://github.com/Automattic/harper) — a project OpenCnid has no authority
over — so the authority order is absolute and one-directional:

```
harper source  →  this map  →  any downstream decision
```

If a sentence here disagrees with harper's code, **harper wins and this file has a defect.**

> **Rendered companion.** An interactive, theme-aware HTML render lives beside this file at
> [`DENSITY-CHAIN.html`](DENSITY-CHAIN.html). The two are kept in sync; **this markdown is the ground
> truth, the HTML is the map.**

---

## Why we mapped someone else's engine

The question that opened this run was whether harper is useful to [Trellis](https://github.com/OpenCnid),
OpenCnid's Recursive Language Model runtime — *"in any shape or form."* Answering it honestly required
knowing what harper actually is, and the fastest wrong answer would have been to read its README and
guess. So we reverse-engineered it from the record instead: **4,460 commits, 2,266 pull requests, 226
releases, 135 authors, October 2023 through July 2026.**

The finding that named this repository is **Weir**: a declarative rule language, created 2026-01-12,
in which a grammar rule and its own acceptance tests are *one artifact*. Within six months of its
birth, 42.6% of all rule-adding commits chose it over hand-written Rust. That is the transferable
idea, and it is why this repo is called `weir-rule-language` rather than anything with "harper" in it.

## What harper is, in numbers we verified

| Fact | Value |
|---|---|
| What it does | Offline, privacy-first English grammar and style checker |
| Language / license | Rust / Apache-2.0 |
| Reach | 12,312 stars, 457 forks, 226 releases (latest `v2.6.0`) |
| History | `57b90e33` (2023-10-19, *"Some stuff??"*) → `efa59c33` (2026-07-24) |
| Scale | 21 Rust crates, 9 pnpm packages, ~105,805 lines in `harper-core` alone |
| Rules | 300 Rust linter files + 351 `.weir` declarative rules |
| Tests | 6,090 `#[test]` functions, plus 1,838 assertions living inside `.weir` rule files |
| Contribution | 1,924 merged PRs, 220 closed-unmerged, 122 open; 561 open issues |
| Concentration | Elijah Potter 2,409 commits of 4,460 — 54% |
| Claimed latency | 10 ms, against LanguageTool 650 ms and Grammarly 4,000 ms (`COMPARISON.md`) |

---

## How to read this file (the contract)

1. **The trunk is the whole system, three times.** T0–T2 below is under 500 words and orients everything else.
2. **Each branch is conceptually complete at every tier.** T2–T5 *add* entities; they never *correct* a shallower tier. Stop at the first tier that answers your question.
3. **Status labels are load-bearing.** `shipped` ≠ `shipped-but-unreachable` ≠ `shipped-but-unenforced` ≠ `proposed` ≠ `retired`. Blurring them is the failure this format exists to prevent.
4. **Reachability is reported separately from correctness.** *Correct is not the same claim as reachable.* Each branch names code with no non-test caller. Those are findings, not accusations.
5. **Nothing here was executed.** The cartographers were forbidden to run `cargo`, `pnpm`, `just`, or `npm`. Every test count is a **source count, not a green run**. Every defect is derived from reading, never from an executed counterexample.
6. **T4 is a dated observation against a moving target.** harper merges roughly 60 PRs a month. Some frontier findings will be stale within weeks. That is expected.

---

## The trunk — the whole system at three densities

### Trunk-T0 (what harper is, in one sentence)

Harper is an **offline grammar checker built as a rule engine over an addressable token stream** —
text becomes a flat sequence of typed, character-indexed spans; several hundred small independent
experts each report findings as spans with suggested replacements; a configurable group composes them
into one pass; and the whole thing runs locally in about ten milliseconds so that no user's prose ever
leaves their machine.

### Trunk-T1 (one paragraph)

A parser or masker decides which bytes of a structured file are prose ([C7](#c7)), a total lexer turns
those bytes into typed tokens carrying half-open `Span<char>` addresses ([C1](#c1)), a dictionary
answers whether each word exists and what is known about it ([C5](#c5)), and a trained Brill tagger
overwrites each token's part-of-speech from context ([C6](#c6)). Over that stream, rules match. Rules
are written three ways that all lower onto one contract: hand-rolled Rust, composable `Expr`
combinators ([C2](#c2)), or the declarative Weir language ([C3](#c3)). A `LintGroup` composes them,
configured per user, and suppression is per-lint rather than per-rule ([C4](#c4)). The result — a
`Lint` carrying a span, a message, and ranked suggestions — reaches users through a language server, a
WebAssembly build, a CLI, a desktop overlay, and browser and editor extensions ([C8](#c8)). Around all
of it sits an unusually deliberate contribution machine that publishes its rules for humans and models
alike ([C9](#c9)).

### Trunk-T2 (the class map — the nine branches)

| Class | Charter, in one line | Where it lives |
|---|---|---|
| **[C1](#c1)** Document model | text → typed, addressable token stream | `harper-core/src/{document,token,span,lexing}` |
| **[C2](#c2)** Expression system | composable matchers over that stream | `harper-core/src/{expr,patterns}` |
| **[C3](#c3)** Weir | rules as data, with their tests, packaged | `harper-core/src/{weir,weirpack}` |
| **[C4](#c4)** Linter corpus | many small experts, one configured group | `harper-core/src/linting` |
| **[C5](#c5)** Spelling & dictionaries | does this word exist, and what else is known | `harper-core/src/spell`, `harper-dictionary-wordlist` |
| **[C6](#c6)** POS tagging | the one learned model in a rule engine | `harper-brill`, `harper-pos-utils` |
| **[C7](#c7)** Format adapters | finding the prose inside a structured file | `harper-core/src/{parsers,mask}`, 10 format crates |
| **[C8](#c8)** Delivery surfaces | one engine, many places a user meets it | `harper-ls`, `harper-wasm`, `packages/*`, `harper-desktop` |
| **[C9](#c9)** Contribution machine | how a 135-author project absorbs work, including a model's | `AGENTS.md`, `AGENT_POLICY.md`, `justfile`, `.github/` |

---

## The spine of the whole story: a four-rung abstraction ladder

The single most legible arc in 4,460 commits is harper's repeated shortening of the distance between
*"I know this grammar rule"* and *"the engine knows it."* Four rungs, each verified to a birth commit:

| Rung | Born | What changed |
|---|---|---|
| **Hand-rolled Rust** | `309d840e`, 2024-01-15 | Every rule is a bespoke scanner. Adding one means writing Rust. |
| **`Pattern`** | `6107594e`, 2024-09-01 | A closed algebra of matchers. Rules declare a token shape instead of scanning. |
| **`Expr`** | `a8fb0c6d` (#1393), 2025-06-13 | The rename that was a redesign: a match returns a **`Span`**, not a length — so one traversal (`iter_matches`) is written once and 279 rule files inherit it. |
| **Weir** | `46f4547f` (#2357), 2026-01-12 | The rule becomes **data**: a `.weir` file with `expr main`, its metadata, and **its own tests**. |
| **Weirpack** | `3a5cd68b` (#2491), 2026-02-03 | The rule *set* becomes a **distributable unit**: a zip with a validated manifest and an optional bundled dictionary. |

Two years of work whose consistent direction is *make the expert cheaper to author and easier to
verify, without giving up determinism*. Every rung still lowers onto the one below it — Weir compiles
to `Expr`, `Expr` lifts from `Step`, `Step` lifts from `Pattern` — so nothing was replaced, and that
non-replacement is itself a finding ([C2](#c2) T4).

## The temporal cross-section — general → current → future, all nine at once

Read across instead of down: this is every class at the same tier, so the *shape* of the system's
maturity is visible in one pass.

- **T1, the invariants.** Every class's essence is a claim about *addressability*: prose must be found
  (C7), tokenized to stable addresses (C1), matched by shape (C2/C3), judged by composable experts
  (C4), informed by lexicon (C5) and context (C6), and delivered without losing the offset (C8) — under
  a process that scales past its maintainers (C9).
- **T2–T3, what is actually built.** Overwhelmingly complete. The engine ships, in production, to
  hundreds of thousands of users, with 6,090 tests and a snapshot corpus.
- **T4, the frontier.** The pattern that repeats across all nine classes is **duplicated knowledge**:
  two TLD tables (C1), a dead duplicate trait (C2), a manifest validated in both Rust and TypeScript
  (C3), lint colours in three files (C8), a CI gate documented nine months after retirement (C9). Also
  repeated: **reach lagging capability** — 50 parsers via LSP but 3 via WebAssembly (C7/C8).
- **T5, what is proposed.** Concentrated in two places: more formats (C7) and more surfaces (C8), plus
  one genuinely architectural open PR — #3717, replacing the Brill tagger and chunker with a joint
  neural model (C6).

---

## The branches

Each branch is a self-contained five-tier chain of density at a held **~90 words per tier**, returned
by an independent cartographer that could not see any sibling's work.


<a id="c1"></a>

## C1 — The Document Model: Characters, Spans, and the Typed Token Stream
*Charter: the path from a raw string to an addressable, typed token sequence — the document type, token kinds, spans, the lexer, and the character-level primitives beneath — deliberately excluding the rules that consume the stream and the markup parsers that feed it.*

- **T1 — essence.** Any checker over prose must first fix an addressing scheme, because every downstream claim is a claim about a location. Characters, not bytes, are the stable unit: byte offsets shift with encoding, character indices do not. Raw text becomes a flat sequence of typed, half-open, non-overlapping intervals, each carrying a kind rich enough that rules never re-read the string. The scanner must be greedy and priority-ordered, with a total fallback so no input is unrepresentable; a post-lex fusion pass then re-joins the multi-character idioms a character-local scanner necessarily splits.

- **T2 — current machinery.** `Document` (`document.rs:18`) pairs an `Lrc<[char]>` source with `Vec<Token>`; `Token` (`token.rs:7`) is a `Span<char>` plus `TokenKind`. `Span<T>` (`span.rs:19`) is a phantom-typed half-open range. `lex_with` drives `lex_english_token` (`lexing/mod.rs:26,65`), thirteen lexers in priority order ending at `lex_catch` → `Unlintable`. `apply_fixups` (`document.rs:156`) then runs thirteen fusion passes — spaces, newlines, dotted initialisms, ellipsis, TLDs, filename extensions, `tl;dr`, ampersand and slash pairs — before `match_quotes` pairs quotation marks. `TokenStringExt` (`token_string_ext.rs:49`) macro-generates the query surface.

- **T3 — with receipts.** Nineteen files, 5,798 lines, 186 `#[test]`s. `document.rs` (1,372 lines, 45 tests) dates to `309d840e` 2024-01-15; `token.rs` to `61dcf22b` 2024-01-25; `token_kind.rs` split out in `28448ad0` 2025-01-03. `TokenKind` has 13 variants and 67 macro-delegated metadata predicates; `Punctuation` 40 variants over 41 `from_char` arms; `Currency` 11 (`d39380f6`, 2025-01-14). `CharString` inlines 16 chars (`char_string.rs:8`, `6e7cbe18` 2024-03-25). `offsets.rs` (36 lines) arrived with `2076d2e9` (#2684, 2026-02-11). `2b5c8cd3` (#3060, 2026-03-30) made `source` an `Lrc<[char]>`.

- **T4 — the frontier.** Open issue #3863 (2026-07-22, `bug`/`harper-core`): `lex_spaces` (`lexing/mod.rs:307`) matches only U+0020, so a non-breaking space becomes `Unlintable` and every multi-token lint silently stops. `ffc9cbd7` (#1199, 2025-05-01) un-commented two signed-number tests without restoring `#[test]`, leaving dead functions at `lexing/mod.rs:405,417`. Two divergent TLD tables: 15 (`hostname.rs:61`) versus 106 (`document.rs:717`). `Regexish` is lexed but read by no non-test code. `Span::set_len` (`span.rs:122`) has one caller, `with_len`. `document.rs:32` calls its own intersection scan "Desperately needs optimization."

- **T5 — future plans.** Proposed only. #3032 (hippietrail, 2026-03-26, +248/−142 across 43 files) introduces a `CharSlice` newtype so `&[char]` gets `==`, superseding #2956 and retiring the `eq_*_ignore_ascii_case` family; #3266 (2026-04-29, +77/−109) adds equality conveniences directly on `Token`. #3739 (2026-06-29) fixes `lex_hostport` dropping host and path when a URL carries an explicit port. #3748 adds an adverbial-particle POS to `TokenKind`; #3717 rewires `Document::parse` for a probability-aware joint tagger; #2630 is flagged `feat(core)!` for dictionary case-sensitivity.

*Status ledger:* char-indexed `Span<T>` addressing — **shipped** · `Lrc<[char]>` shared source — **shipped** (breaking, #3060) · 13-lexer priority chain with total `lex_catch` fallback — **shipped** · 13-pass `apply_fixups` fusion — **shipped** · quote twin-matching — **shipped** · `TokenKind::Regexish` — **shipped-but-unreachable** (no non-test consumer) · `Span::set_len` — **shipped-but-unreachable** (only `with_len`) · signed-number lexing — **proposed** (no lexer, no registered test) · `CharSlice` `==` — **proposed** (#3032) · `Token` equality conveniences — **proposed** (#3266) · commented-out test blocks in `lexing/` — **retired** (#1199)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Document` | T2 | `harper-core/src/document.rs:18` |
| `Token` | T2 | `harper-core/src/token.rs:7` |
| `TokenKind` (13 variants) | T2 | `harper-core/src/token_kind.rs:36` |
| `Span<T>` (half-open, phantom-typed) | T2 | `harper-core/src/span.rs:19` |
| `FoundToken` / `lex_with` | T2 | `harper-core/src/lexing/mod.rs:15,26` |
| `lex_english_token` (13 lexers) | T2 | `harper-core/src/lexing/mod.rs:65` |
| `lex_weir_token` (12 lexers) | T2 | `harper-core/src/lexing/mod.rs:45` |
| `Document::apply_fixups` (13 passes) | T2 | `harper-core/src/document.rs:156` |
| `Document::match_quotes` / `Quote::twin_loc` | T2 | `document.rs:394`, `punctuation.rs:146` |
| `TokenStringExt` (24 `create_fns_for!`) | T2 | `harper-core/src/token_string_ext.rs:49` |
| `CharStringExt` / `CharString` (inline 16) | T2 | `harper-core/src/char_string.rs:8,21` |
| `CharExt::is_english_lingual` | T2 | `harper-core/src/char_ext.rs:26` |
| `FatToken` / `FatStringToken` | T2 | `harper-core/src/fat_token.rs:8,24` |
| `Punctuation` (40 variants) | T2 | `harper-core/src/punctuation.rs:10` |
| `Number` / `OrdinalSuffix` | T2 | `harper-core/src/number.rs:10,42` |
| `Currency` (11 variants) | T2 | `harper-core/src/currency.rs:8` |
| `Case` / `copy_casing` | T2 | `harper-core/src/case.rs:14,38` |
| `try_make_title_case` | T2 | `harper-core/src/title_case.rs:71` |
| `VecExt::remove_indices` | T2 | `harper-core/src/vec_ext.rs:13` |
| `Lrc` (Rc / Arc behind `concurrent`) | T2 | `harper-core/src/sync.rs:2` |
| document.rs birth | T3 | `309d840e` (2024-01-15) |
| token.rs birth | T3 | `61dcf22b` (2024-01-25) |
| token_kind.rs / fat_token.rs extraction | T3 | `28448ad0` (2025-01-03) |
| `CharString` introduction | T3 | `6e7cbe18` (2024-03-25) |
| `title_case.rs` first draft | T3 | `e50ffba0` (2024-12-27) |
| `Currency` expansion | T3 | `d39380f6` (2025-01-14) |
| `Number` dedicated type | T3 | `70c333d4` (2025-02-05) |
| `TokenKind::Regexish` | T3 | `f277857b` (2025-02-13) |
| `TokenKind::Decade` / `lex_long_decade` | T3 | `507fb2c7` (2025-02-14) |
| `TokenKind::HeadingStart` | T3 | `bfaa324c` (#2297, 2025-12-05) |
| `build_byte_to_char_map` | T3 | `2076d2e9` (#2684, 2026-02-11) |
| `Lrc<[char]>` breaking change | T3 | `2b5c8cd3` (#3060, 2026-03-30) |
| `TokenStringExt` refactor (−235/+124) | T3 | `436d61d5` (#2888, 2026-04-13) |
| `SinglePrime` / `DoublePrime` | T3 | `b6b12ea7` (#3275, 2026-06-16) |
| NBSP tokenizer defect | T4 | issue #3863 (2026-07-22) |
| Unregistered `#[ignore]` tests | T4 | `lexing/mod.rs:405,417`; `ffc9cbd7` (#1199) |
| Divergent TLD tables (15 vs 106) | T4 | `hostname.rs:61`, `document.rs:717` |
| Unoptimized intersection scans | T4 | `document.rs:32,42` |
| Ordinal-suffix spacing TODO | T4 | `document.rs:470` |
| `is_case_separator` TODO | T4 | `token_kind.rs:363` |
| Tab-as-two-columns approximation | T4 | `lexing/mod.rs:293` |
| `CharSlice` newtype | T5 | PR #3032 |
| `Token` equality conveniences | T5 | PR #3266 |
| `lex_hostport` port fix | T5 | PR #3739 |
| Adverbial-particle POS | T5 | PR #3748 |
| Probability-aware joint tagger | T5 | PR #3717 |
| Dictionary case-sensitivity (breaking) | T5 | PR #2630 |

*Trellis-relevant observation:* This class is a working instance of code-mediated text: the model of the document never holds strings, only engine-computed `Span<char>` addresses into one shared `Lrc<[char]>`, so every rule states its finding as an interval rather than a copied excerpt — exactly the discipline a composable expert system over user data needs to keep splices verifiable. The two-stage shape is the reusable part: a cheap total lexer that can never fail, followed by a separately-owned fusion pass that fixes up idioms, so new domain idioms are added without touching the scanner. The cautionary half is that the same knowledge got encoded twice in incompatible shapes — two TLD tables, one 15 entries and one 106 — because the fusion pass and the lexer each grew their own copy; a registry, not a literal, is the fix.

## Uncovered
- The markup parsers (`harper-core/src/parsers/`), masking (`mask/`), and the `expr`/`patterns` matcher: named by the charter as out of scope, and they belong to sibling classes.
- `lexing/url.rs` (256 lines) and `lexing/email_address.rs` (207 lines) were read only at the signature level; their RFC-shaped predicate chains were not audited line by line, so I make no correctness claim about them beyond open PR #3739.
- `DictWordMetadata` internals behind the 67 delegated `TokenKind` predicates: reachable from this class but owned by the dictionary/spell subsystem.
- Span translation across the WASM and `harper.js` boundary (char ↔ UTF-16) was not traced; only the in-core `build_byte_to_char_map` was.
- Of 122 open PRs, only those whose changed-file lists touch a C1 path were opened; PR bodies for the remainder were not read.

<a id="c2"></a>

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

<a id="c3"></a>

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

<a id="c4"></a>

## C4 — The Linter Corpus and Its Composition
*Charter: the `Linter` contract, the several hundred concrete rules implementing it, the group that runs them as one pass, the per-user configuration and default curation, and the user-suppression channel — excluding the Weir rule language itself and the expression combinators beneath `ExprLinter`.*

- **T1 — essence.** A text checker is a large population of narrow, independent, fallible detectors. The hard problem is not detection but governance of the population: one uniform interface so any detector plugs in; a stable identifier per detector so a user's on/off choice survives upgrades; a composer that runs only the enabled subset and merges their findings; a curated default deciding what fires unasked; and a suppression channel letting a user overrule one specific finding without silencing its whole rule. The identifier namespace, not the algorithm, is the real API.

- **T2 — current machinery.** `Linter` (`linting/mod.rs:346`) is two methods: `lint(&mut self, &Document) -> Vec<Lint>` and `description() -> &str`. A `Lint` (`lint.rs:11`) carries span, `LintKind`, suggestions, message, priority. `LintGroup` (`lint_group/mod.rs:329`) keys three `BTreeMap`s by name — plain linters, chunk `ExprLinter`s, sentence `ExprLinter`s — plus two LRU caches and a `FlatConfig`. It implements `Linter`, so groups nest. `new_curated(dictionary, dialect)` registers everything; `merge_from` folds sub-groups and user Weirpacks in. `IgnoredLints` stores context hashes.

- **T3 — with receipts.** `default_config.json` lists 820 rule names in 15 UI groups: 328 Weir-backed (317 standalone `.weir` + 11 directory-groups, born `df18ff1c` #3494 2026-05-26) and 492 Rust; 811 enabled, 9 off. `7fb35c0d` (2025-02-18) swapped the `create_lint_group_config!` macro's per-rule struct for `HashMap<String,bool>` plus a public `add`, so any crate registers rules at runtime. `b76e8dd39` (#3123, 2026-04-08, +7,225 lines/28 files) moved the default bit from Rust into JSON — 709 rules then. 5,295 `#[test]`; 1,838 `.weir` tests.

- **T4 — the frontier.** `Lint::spanless_hash` (`lint.rs:35`) has zero callers, orphaned when `b7d62678` (2025-01-30) replaced kind-only hashing with `LintContext`; `FlatConfig::set_rule_enabled_if_unset` (`flat_config.rs:70`) is uncalled. `clashing_linter_names` (`lint_group/mod.rs:348`) is read only at line 1241 under `#[cfg(test)]`, so #2374 shipped a CI test, not a warning — and it cannot see `merge_linters!` children (#3241, #3134). `merge_from` overwrites on clash. `LintKind::WordOrder` is missing from `from_string_key` (`lint_kind.rs:62`). `Setting::OneOfMany` has zero instances.

- **T5 — future plans.** 75 of 122 open PRs touch linting. #3244 (2026-04-25) walks merged linters for clashes and states its CI is expected to fail on a real `TooTo` collision; #3237 would run sub-linter tests from the CLI; #3134 asks to make them addressable at all. #3445 proposes `LintKind::Preposition`, #2431 moves `LintKind` colours into core, #3330 would let one rule emit several spans, #3422 proposes a regex-flavoured `RigLinter`. #3267 adds Singaporean and Malaysian dialects; #3402 and #2150 propose non-English. #3143 and #3592 want source-comment suppression; #1455 wants ignore files relocated.

*Status ledger:* `Linter`/`Lint`/`LintKind` contract — **shipped** · `LintGroup` three-map composition with LRU chunk/sentence caches — **shipped** · runtime `add`/`add_chunk_expr_linter`/`add_sentence_expr_linter` — **shipped** · Weirpack merge at runtime (harper-cli, harper-wasm) — **shipped** · `FlatConfig` string-keyed on/off — **shipped** · `StructuredConfig` + `default_config.json` curation — **shipped** · `Setting::OneOfMany` (code + two UIs, zero config instances) — **shipped-but-unexercised** · clash detection as runtime signal — **shipped-but-unreachable** (test-only reader) · clash detection through `merge_linters!` — **proposed** (#3244) · `Lint::spanless_hash` — **shipped-but-unreachable** · `FlatConfig::set_rule_enabled_if_unset` — **shipped-but-unreachable** · `LintKind::WordOrder` string parse — **shipped-but-unreachable** · macro-generated `LintGroupConfig` struct — **retired** (`7fb35c0d`) · per-registration `bool` default in Rust — **retired** (#3123) · sub-linter addressing in config — **proposed** (#3134) · source-comment suppression — **proposed** (#3143, #3592) · dialects beyond the five — **proposed** (#3267)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Linter` trait (`lint` + `description`) | T2 | `harper-core/src/linting/mod.rs:346` |
| `HtmlDescriptionLinter` blanket trait | T2 | `harper-core/src/linting/mod.rs:356` |
| `Lint` (span, kind, suggestions, message, priority) | T2 | `harper-core/src/linting/lint.rs:11` |
| `LintKind` (21 variants) | T2 | `harper-core/src/linting/lint_kind.rs:10` |
| `ExprLinter` with `Unit = Chunk \| Sentence` | T2 | `harper-core/src/linting/expr_linter.rs:40` |
| `LintGroup` (3 BTreeMaps + 2 LRU caches) | T2 | `harper-core/src/linting/lint_group/mod.rs:329` |
| `LintGroup::new_curated(dictionary, dialect)` | T2 | `harper-core/src/linting/lint_group/mod.rs:541` |
| `LintGroup::merge_from` | T2 | `harper-core/src/linting/lint_group/mod.rs:437` |
| `LintGroup::organized_lints` (name → lints) | T2 | `harper-core/src/linting/lint_group/mod.rs:935` |
| `impl Linter for LintGroup` (groups nest) | T2 | `harper-core/src/linting/lint_group/mod.rs:1048` |
| `FlatConfig` (`HashMap<String, Option<bool>>`) | T2 | `harper-core/src/linting/lint_group/flat_config.rs:35` |
| `StructuredConfig` / `Setting::{Bool,OneOfMany,Group}` | T2 | `harper-core/src/linting/lint_group/structured_config/mod.rs:15,80` |
| `HumanReadableStructuredConfig` (JSON mirror) | T2 | `.../structured_config/human_readable_structured_config.rs:7` |
| `IgnoredLints` (`HashSet<u64>` of context hashes) | T2 | `harper-core/src/ignored_lints/mod.rs:14` |
| `LintContext` (kind+suggestions+message+priority+FatTokens) | T2 | `harper-core/src/ignored_lints/lint_context.rs:13` |
| `Dialect` (American, Canadian, Australian, British, Indian) | T2 | `harper-core/src/dict_word_metadata.rs:1048` |
| `merge_linters!` macro (sub-linters, no LintGroup) | T2 | `harper-core/src/linting/merge_linters.rs:1` |
| `weir_rules::lint_group()` build-time registration | T2 | `harper-core/src/linting/weir_rules/mod.rs:9` |
| Weirpack `to_lint_group()` → runtime merge | T2 | `harper-core/src/weirpack/mod.rs:70`; `harper-wasm/src/lib.rs:563`; `harper-cli/src/lint.rs:455` |
| `refactor(core): make LintGroup runtime-extensible` | T3 | `7fb35c0d` (2025-02-18) |
| `feat: render configuration structurally` (#3123) | T3 | `b76e8dd39` (2026-04-08) |
| `feat(core): get more context in IgnoredLints` | T3 | `b7d62678` (2025-01-30) |
| `fix: warn about clashing linter names` (#2374) | T3 | `5e2afcda` (2026-03-13) |
| chunk/sentence `ExprLinter` split (#2165) | T3 | `256cf921` (2025-11-28) |
| Weir rule directory-groups (#3494) | T3 | `df18ff1c` (2026-05-26) |
| `LintKind::WordOrder` added (#3611) | T3 | `bed2d57a` (2026-06-25) |
| `curated_default_config_lists_every_registered_rule` | T3 | `.../structured_config/mod.rs:313` |
| `run_tests_for_weir_rules` (1,838 tests, one `#[test]`) | T3 | `harper-core/src/linting/weir_rules/mod.rs:64` |
| `no_linter_names_clash` (test-only clash reader) | T4 | `harper-core/src/linting/lint_group/mod.rs:1237` |
| `Lint::spanless_hash` (no callers) | T4 | `harper-core/src/linting/lint.rs:35` |
| `FlatConfig::set_rule_enabled_if_unset` (no callers) | T4 | `harper-core/src/linting/lint_group/flat_config.rs:70` |
| `LintKind::from_string_key` missing `WordOrder` | T4 | `harper-core/src/linting/lint_kind.rs:62` |
| `lint_kind_color` unreachable `WordOrder` arm | T4 | `harper-desktop/src-tauri/src/lint_kind_color.rs:56,61` |
| Issue: `TooTo` clash invisible to the test | T4 | #3241 (open, 2026-04-25) |
| Issue: sub-linters of merged linters unaddressable | T4 | #3134 (open, 2026-04-08) |
| Issue: ignored-lint files pollute the project dir | T4 | #1455 (open, 2025-06-25) |
| PR: clash detection through merged linters | T5 | #3244 (open) |
| PR: `LintKind::Preposition` | T5 | #3445 (open) |
| PR: one linter, multiple spans | T5 | #3330 (open) |
| PR: `RigLinter` | T5 | #3422 (open) |
| PR: Singaporean and Malaysian English | T5 | #3267 (open) |
| Issues: source-comment ignore directives | T5 | #3143, #3592 (open) |

*Trellis-relevant observation:* Harper's durable asset is a flat string namespace of 820 rule names that config, UI, telemetry, and user rule-packs all key on — the code behind a name is swappable (492 Rust, 328 Weir) precisely because the name is not. The lesson to avoid is that harper made the namespace flat but composition nested: `merge_linters!` children and merged Weirpack rules exist without being addressable, so clashes silently overwrite and #3134/#3241 sat open for months. A composable expert system should make the registry the enforced source of truth — one registration path, one uniqueness check at runtime, not a test.

## Uncovered
- Whether the LRU cache key is sound: `FlatConfig`'s `Hash` impl (`flat_config.rs:113`) iterates a `hashbrown::HashMap`, whose order is unspecified, so two equal configs may hash differently. Proving whether this degrades to cache misses only, or can collide two different configs onto one key, needs a runtime experiment — barred by the read-only, no-`cargo` constraint.
- False-positive rate and rule quality: 84.6% of `.weir` files (297/351) carry fewer than the 15 tests `AGENTS.md:225` requires, but I could not distinguish rules predating the standard from rules that violate it without per-file commit archaeology across 351 files.
- The exact split of the 492 Rust names among the five non-Weir merged sub-groups: 295 are registered directly in `new_curated`; the residual 197 come from `phrase_set_corrections`, `proper_noun_capitalization_linters`, `closed_compounds`, `initialisms`, and `be_adjective_confusions`, whose per-module counts are macro-generated and were not enumerated.
- Whether any of the 9 default-disabled rules (`NoOxfordComma`, `SpelledNumbers`, `PossessiveNoun`, `AvoidContractions`, `BoringWords`, `AnalogAcousticBike`, `AnotherThinkComing`, `ViciousCircleOrCycle`, `ViciousCycle`) were disabled for false positives versus opinionated style; the commits that flipped them were not traced.

<a id="c5"></a>

## C5 — The Lexicon: Word Existence, Word Knowledge, and Correction Ranking
*Charter: how a word is declared to exist, what the engine records about it, how a misspelling becomes a ranked correction list, and how user vocabulary composes with the curated core — excluding the grammar rules that consume word metadata and the part-of-speech tagger that writes into it.*

- **T1 — essence.** A speller answers three questions: does this token exist, what else is known about it, and if it does not exist what was meant. Existence is membership in a finite lexicon that must ship offline yet answer per token. Knowledge is a record attached to each entry — inflection, register, region, letter-case shape — because downstream rules need more than a yes. Correction is nearest-neighbour search under an edit metric, then re-ranked by priors the metric cannot see. And the lexicon is never one list: a curated core must compose with what the writer adds.

- **T2 — current machinery.** A `Dictionary` trait (`spell/dictionary.rs`) with four implementors. `MutableDictionary` stores a `WordMap` — `HashMap<WordId, WordMapEntry>` keyed by a case-folded hash. Curated data is `dictionary.dict` plus `annotations.json`, parsed by the `rune` module and affix-expanded by `AttributeList::expand_annotated_word`. `FstDictionary` wraps that with an `fst::Map` searched by a Levenshtein automaton; `MutableDictionary` falls back to Wagner-Fischer in `edit_distance.rs`. `score_suggestion` re-ranks. `DictWordMetadata` carries part-of-speech, `DialectFlags`, `OrthFlags`. `MergedDictionary` layers curated under user dictionaries. `harper-thesaurus` supplies synonyms.

- **T3 — with receipts.** `spell/` is 3,096 LOC across 15 files, 75 `#[test]`; `dict_word_metadata.rs` is 2,056 LOC with 156. `dictionary.dict` is 786,704 bytes and 54,669 entries (49,577 at `9291165c` 2024-01-20); `annotations.json` is 17,315 bytes, 25 affix flags, 54 properties. FST landed `d9a159d8` 2024-10-06 (PR #258); hash lookup `e48fb630` 2025-03-13, `hunspell`→`rune` `4829e0b7`, dialects `2e4445fc` — all PR #925. Scoring: `99e77c4f` 2025-03-07 (PR #844). Five dialects; Indian `f45addc4f` 2025-12-31 (#2397).

- **T4 — the frontier.** `MergedDictionary`'s doc says first-inserted wins (`merged_dictionary.rs:14`), but `get_word_metadata` has merged every child since `0d4feee7` (PR #1922, 2025-09-15). `WordId` stores only a 64-bit hash (`word_id.rs:14`); `WordMap::insert` overwrites by id, so canonical spelling is last-write-wins — the mechanism behind issue #2411. `FstDictionary` materializes the wordlist three ways (`fst_dictionary.rs:18-25`, issue #3725). `edit_distance()`, `get_word_from_id`, `find_words_with_prefix`, `WordMap::contains_str`/`with_capacity` have no non-test caller. `rune/mod.rs:114` lost its `#[test]`.

- **T5 — future plans.** Proposed, not built: PR #3351 (2026-05-11) adds Metaphone phonetic matching to suggestions, +359/−4 over 5 files. Issue #3347 proposes replacing the additive score with multiplicative weights, calling the present scheme a code smell. PR #2630 (2026-01-30) is a breaking rework of dictionary case-sensitivity, +1,262/−1,074 over 49 files. PR #2879 would spell-check compounds whose parts are absent; PR #3194 relaxes apostrophe matching; draft PR #2133 adds `harper-cli dictionary-normalize`. Issues #115 and #3092 request multi-word and hyphenated user entries.

*Status ledger:* FST curated lookup + Levenshtein-automaton fuzzy match — **shipped** · hash-keyed `WordMap` — **shipped** · Rune affix expansion (25 flags, 54 properties) — **shipped** · additive `score_suggestion` re-ranking — **shipped** · five-dialect `DialectFlags` + document dialect guessing — **shipped** · nine-flag `OrthFlags` — **shipped** · `MergedDictionary` four-layer composition (curated/user/workspace/file) — **shipped** · `TrieDictionary` prefix search — **shipped** (one consumer, `SplitWords`) · thesaurus synonyms — **shipped** (one consumer, `BoringWords`, five trigger words) · Wagner-Fischer `edit_distance_min_alloc` — **shipped** (user dictionaries only; curated path uses the DFA) · `Dictionary::get_word_from_id` — **shipped-but-unreachable** · `Dictionary::find_words_with_prefix` — **shipped-but-unreachable** · `edit_distance::edit_distance` wrapper — **shipped-but-unreachable** (module is private, so not public API either) · `WordMap::contains_str`, `WordMap::with_capacity` — **shipped-but-unreachable** · full-line-comment expansion test — **shipped-but-unreachable** (missing `#[test]`) · `harper-cli audit-dictionary` — **shipped** (gated in `justfile:437`) · Metaphone phonetic suggestions — **proposed** (PR #3351) · weight-based suggestion ranking — **proposed** (issue #3347) · explicit dictionary case-sensitivity — **proposed** (PR #2630) · compound spell-check — **proposed** (PR #2879) · `harper-dictionary-parsing` crate — **retired** (`1cd50d60` 2024-10-30, undone by `a7ffd4fb` 2024-11-14) · `FullDictionary` — **retired** (renamed `b84d105c`, PR #658) · `hunspell` module name — **retired** (`4829e0b7`) · `affixes.json` — **retired** (`92b964d0`, PR #1504) · `WordMetadata` — **retired** (renamed `88dbd058`, PR #1572)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Dictionary` trait (15 methods) | T2 | `harper-core/src/spell/dictionary.rs:12-57` |
| `MutableDictionary` | T2 | `harper-core/src/spell/mutable_dictionary.rs:25` |
| `FstDictionary` | T2 | `harper-core/src/spell/fst_dictionary.rs:18-25` |
| `MergedDictionary` | T2 | `harper-core/src/spell/merged_dictionary.rs:17` |
| `TrieDictionary` | T2 | `harper-core/src/spell/trie_dictionary.rs:13` |
| `WordMap` / `WordMapEntry` | T2 | `harper-core/src/spell/word_map.rs:9,14` |
| `WordId` (64-bit case-folded hash) | T2 | `harper-core/src/spell/word_id.rs:14-26` |
| `rune` module (Rune word-list format) | T2 | `harper-core/src/spell/rune/mod.rs` |
| `parse_word_list` (count header, `#` comments, `/` flags) | T2 | `harper-core/src/spell/rune/word_list.rs:13-54` |
| `AttributeList::expand_annotated_word` | T2 | `harper-core/src/spell/rune/attribute_list.rs:56-204` |
| `Matcher` (simplified regex for affix conditions) | T2 | `harper-core/src/spell/rune/matcher.rs:9-70` |
| `DictWordMetadata` | T2 | `harper-core/src/dict_word_metadata.rs:20-56` |
| `score_suggestion` / `order_suggestions` | T2 | `harper-core/src/spell/mod.rs:295-390` |
| `suggest_correct_spelling` | T2 | `harper-core/src/spell/mod.rs:394-406` |
| `edit_distance_min_alloc` (two-row Wagner-Fischer) | T2 | `harper-core/src/edit_distance.rs:6-39` |
| `SpellCheck` linter (LRU 10,000; `MAX_SUGGESTIONS = 3`) | T2 | `harper-core/src/linting/spell_check.rs:13-67` |
| `IrregularNouns` / `IrregularVerbs` | T2 | `harper-core/src/irregular_nouns.rs:8`, `irregular_verbs.rs` |
| `get_plurals` / `get_singulars` (dictionary-validated) | T2 | `harper-core/src/regular_nouns.rs:5-27` |
| `starts_with_vowel` / `InitialSound` | T2 | `harper-core/src/indefinite_article.rs:10-21` |
| `harper_thesaurus::Thesaurus` | T2 | `harper-thesaurus/src/thesaurus.rs:31-96` |
| `thesaurus_helper::get_synonym_replacement_suggestions` | T2 | `harper-core/src/thesaurus_helper.rs:57-64` |
| `harper-dictionary-wordlist` (`load_dict` / `save_dict`) | T2 | `harper-dictionary-wordlist/src/lib.rs:13-73` |
| Four-layer merge order: curated → user → workspace → file | T2 | `harper-ls/src/backend.rs:203-225` |
| `dictionary.dict`: 786,704 B, 54,669 entries, header `54800` | T3 | `harper-core/dictionary.dict:1` |
| `annotations.json`: 17,315 B, 25 affixes, 54 properties | T3 | `harper-core/annotations.json` |
| `EXPECTED_DISTANCE = 3`, `TRANSPOSITION_COST_ONE = true` | T3 | `harper-core/src/spell/fst_dictionary.rs:27-28` |
| Damerau transposition cost lowered to one | T3 | `d56bd72b` 2025-09-11 (PR #1899) |
| Back-off search: distances 2,3,4; `result_limit` 200 | T3 | `harper-core/src/linting/spell_check.rs:44-46` |
| `Dialect` enum (5 variants) + `try_from_bcp47` | T3 | `harper-core/src/dict_word_metadata.rs:1048-1094` |
| `DialectFlags` (u8 bitflags) + document dialect guessing | T3 | `harper-core/src/dict_word_metadata.rs:1128-1215` |
| Dialect-tagged base entries: US 151, GB 1,219, CA 504, AU 1,233, IN 1,225 | T3 | `harper-core/dictionary.dict` × `annotations.json` properties `<`, `!`, `@`, `_`, `₹` |
| `OrthFlags` (9 flags, u16 backing) | T3 | `harper-core/src/dict_word_metadata_orthography.rs:6-49` |
| Roman-numeral orthography flag | T3 | `fbab9880` 2025-09-09 (PR #1851) |
| Letter-case flags added to word metadata | T3 | `569d6162` 2025-07-24 (PR #1578) |
| `VerbFormFlags` (6 forms) | T3 | `harper-core/src/dict_word_metadata.rs:827-841` |
| `irregular_nouns.json` 163 pairs; `irregular_verbs.json` 135 | T3 | `harper-core/irregular_nouns.json`, `irregular_verbs.json` |
| `thesaurus.txt` 30,259 entries / 24,822,771 B; `word-freq.txt` 22,297 lines | T3 | `harper-thesaurus/thesaurus.txt`, `word-freq.txt` |
| zstd build-time thesaurus compression | T3 | `harper-thesaurus/build.rs:20-27` |
| `harper-thesaurus` birth | T3 | `50490b8c` 2026-01-13 (PR #2085) |
| FST-based curated spellchecking | T3 | `d9a159d8` 2024-10-06, PR #258 merged 2024-11-23 |
| `MutableDictionary` word-hash lookup | T3 | `e48fb630` 2025-03-13 (PR #925) |
| Scoring replaced shuffling for suggestions | T3 | `99e77c4f` 2025-03-07 (PR #844) |
| Blank lines and `#` comments allowed in `dictionary.dict` | T3 | `0c9b2204` 2025-03-13 (PR #756) |
| Suggestion-score tuning passes | T3 | `e4955aeb` 2025-11-13 (#2189); `150656ee` 2025-12-02 (#2288); `2cdaf158` 2026-03-17 (#2927) |
| Lowercase-DFA skip + `spellcheck` bench | T3 | `0fe03c35` 2026-03-30 (PR #3025), `harper-core/benches/spellcheck.rs` |
| `harper-cli audit-dictionary` (duplicate/unknown/unused flags) | T3 | `harper-cli/src/main.rs:730-848`; `justfile:437,866` |
| `MergedDictionary` doc/behavior divergence | T4 | `merged_dictionary.rs:14` vs `:96-118`; changed by `0d4feee7` (PR #1922) |
| Case-fold collision / last-write-wins canonical spelling | T4 | `word_id.rs:20-26`, `word_map.rs:67-71`; issue #2411 |
| Wordlist materialized 2–3× in `FstDictionary` | T4 | `fst_dictionary.rs:18-25`; issue #3725 |
| `Dictionary::get_word_from_id` — no caller | T4 | `spell/dictionary.rs:50` |
| `Dictionary::find_words_with_prefix` — no non-test caller | T4 | `spell/dictionary.rs:53` |
| `edit_distance()` wrapper — no non-test caller, private module | T4 | `edit_distance.rs:41`; `harper-core/src/lib.rs:11` |
| `WordMap::contains_str`, `WordMap::with_capacity` — no caller | T4 | `word_map.rs:28,89` |
| Dormant test (missing `#[test]`) | T4 | `harper-core/src/spell/rune/mod.rs:114` |
| Stale `u8` comment over a `u16` type | T4 | `dict_word_metadata_orthography.rs:27-30` |
| Open metadata TODOs (abstract nouns, non-personal pronouns, positive degree) | T4 | `dict_word_metadata.rs:872,905,1918` |
| All-caps suggestions degraded | T4 | issue #1419 (2025-06-20) |
| User-added word not recognized with `'s` | T4 | issue #3875 (2026-07-23) |
| Dictionary-member words still flagged | T4 | issues #2585, #3043, #2725 |
| `im` → `I'm` missing from suggestions | T4 | issue #3184 (2026-04-16) |
| Metaphone phonetic suggestion matching | T5 | PR #3351 (2026-05-11, +359/−4, 5 files) |
| Weight-based rather than additive suggestion ranking | T5 | issue #3347 (2026-05-11) |
| Explicit dictionary case-sensitivity (breaking) | T5 | PR #2630 (2026-01-30, +1,262/−1,074, 49 files) |
| Compound spell-check with unknown parts | T5 | PR #2879 (2026-03-06) |
| Case-insensitive apostrophe diff for contractions | T5 | PR #3194 (2026-04-16) |
| `harper-cli dictionary-normalize` (draft) | T5 | PR #2133 (2025-11-04) |
| Multi-word and hyphenated user-dictionary entries | T5 | issues #115 (2024-08-22), #3092 (2026-04-02) |
| Per-programming-language dictionaries | T5 | issue #2451 (2026-01-09) |
| Broader synonym suggestions | T5 | issue #2035 (2025-09-30) |
| Transitivity and abstract-noun marking in the dictionary | T5 | issues #2773, #2772 (2026-02-22) |

*Trellis-relevant observation:* The reusable shape is the two-stage retrieve-then-rerank split — a cheap automaton finds every candidate within an edit budget, and a separate, readable scoring function encodes the priors (first letter rarely mistyped, dialect variants, apostrophe forms) that the metric cannot express; the priors are editable without touching the index. The reusable failure is `WordId`: keying a store by a lossy 64-bit case-folded hash makes two entries silently one, and the surviving canonical form depends on insertion order — a real defect (issue #2411) that a personalized system merging user vocabulary into a curated core would inherit exactly. Worth copying too: user layers add existence but carry no metadata, so composition is a union in which the curated layer wins every scalar field — precedence that is explicit in code rather than implied.

## Uncovered
- The expanded (post-affix) word count of the shipped dictionary. Only the 54,669 base entries in `dictionary.dict` are countable statically; the runtime `word_count()` is the size of the expanded `WordMap`, and deriving it requires running `harper-cli words`, which the read-only boundary forbids.
- The compressed size of the embedded thesaurus. `build.rs:23-24` annotates 3.84 MiB at max level and 7.02 MiB at level 4, but those are comments in the source, not verified artifact sizes, and the artifact is only produced by a build.
- Whether the flagged unreachable items (`get_word_from_id`, `find_words_with_prefix`, `WordMap::contains_str`) are consumed by any downstream crate outside this repository. They sit on public types, so reachability was assessed within the workspace only.
- The `packages/` TypeScript surface for user dictionaries (browser extension, Obsidian, VS Code). Several open issues (#2749, #3662, #2624) concern where those store words; the Rust-side merge was traced, the JS-side storage was not.

<a id="c6"></a>

## C6 — Part-of-Speech Tagging: The Statistical Grammar Layer Inside a Rule Engine

*Charter: the learned tagger that assigns a syntactic role to each token, its shipped artifact, its training pipeline, and the contract rules read it through — excluding the noun-phrase chunker except where the same crates or the same boundary make it load-bearing.*

- **T1 — essence.** A word's part of speech is a property of its position, not of its spelling: one string is a noun here and a verb there. Any solver needs four things — a fixed tag inventory, a cheap baseline guess such as a lexicon's most-frequent tag per word, an ordered list of context-conditioned rewrite rules learned from hand-annotated text, and a contract letting downstream consumers read the result. Learning by transformation keeps the artifact auditable: each correction is a readable "retag A as B when the neighbourhood looks like this," not a weight.

- **T2 — current machinery.** `BrillTagger<FreqDict>` in `harper-pos-utils/src/tagger/brill_tagger/mod.rs` wraps a lowercased word-to-tag `FreqDict` baseline, then replays an ordered `Vec<Patch>`; each `Patch` carries from-tag, to-tag, and a `PatchCriteria` tree over neighbouring tags and literal words. `harper-brill/src/lib.rs` `include_str!`s the trained JSON and serves one process-wide `Arc` from `brill_tagger()`. `Document::parse` in `harper-core/src/document.rs` tags each sentence and writes the result into `DictWordMetadata::pos_tag`. Rules read it via `UPOSSet`, `TokenKind::is_upos`, and bare tag names inside `.weir` files.

- **T3 — with receipts.** Born 2025-06-16, `db89187c3` (#1344, +51,863/−16,125). `harper-brill/trained_tagger_model.json` is 659,686 bytes, 30,468 lines: 26,900 `FreqDict` entries plus 201 patches, 158 of which carry a `WordIs` test over 22 distinct words. `UPOS` (`harper-pos-utils/src/upos.rs:25`) has 16 variants, defaults to `NOUN`, and drops CoNLL-U `X` (`upos.rs:80`). Training is `harper-cli` `TrainBrillTagger` (`harper-cli/src/main.rs:150`, `:573`), gated behind feature `training`. `document.rs:208` makes the tagger win; `infer_pos_tag` is the fallback only when the tagger returns `None`.

- **T4 — the frontier.** `PatchCriteria::WordIs` zips characters without a length check (`harper-pos-utils/src/patch_criteria.rs:99`), so it is a case-insensitive *prefix* match: the shipped `"us"` patch also fires on "used," and 158 of 201 patches route through this predicate. `enforce_pos_exclusivity` (`harper-core/src/dict_word_metadata.rs:200`) has no caller. `test_pos_tagger` never prints `pos_tag` — its only tagger-sensitive column is `np_member` (`harper-core/tests/pos_tags.rs:231`) — and it fails on big-endian hosts (issue #1823, open since 2025-08-28). No `#[test]` exists in either crate; no `.conllu` corpus ships.

- **T5 — future plans.** PR #3717 (2026-06-25, open, not draft) proposes replacing both the Brill tagger and the Burn chunker with one char-CNN plus BiLSTM joint model in `harper-pos-utils::joint`, claiming UPOS accuracy 0.9463 and NP-chunk F1 0.8872, embedded footprint falling from roughly 2.05 MiB to 787 KiB, and seeded end-to-end retraining in about fourteen minutes. It adds runtime-only `pos_tag_topk`, `UPOSSet::new_loose`, and a per-token `~TAG` operator in Weir. It is stacked on PR #3694 (2026-06-21, open), which unifies CoNLL-U extraction and fixes a multiword-token span shift.

*Status ledger:* Brill transformation tagger (`BrillTagger<FreqDict>`) — **shipped** · trained tagger artifact `trained_tagger_model.json` — **shipped** · `UPOS` 16-tag inventory — **shipped** · tag consumption via `UPOSSet` / `is_upos` / Weir bare tag names — **shipped** · `harper-cli TrainBrillTagger` — **shipped** (feature-gated `training`; no corpus in repo, so not reproducible from the clone alone) · `FreqDictBuilder` — **shipped** (training-only; no caller outside `BrillTagger::train`) · `enforce_pos_exclusivity` — **shipped-but-unreachable** · `brill_chunker()` + `trained_chunker_model.json` — **shipped-but-unreachable** (no non-crate caller since #1579 swapped `Document::parse` to `burn_chunker()`; 52,717 bytes still `include_str!`d) · `UPOSIter` re-export — **shipped-but-unreachable** (named only at `harper-pos-utils/src/lib.rs:14`) · `harper-brill` `[build-dependencies] serde_json` — **retired in effect** (no `build.rs` in the crate) · joint neural tagger + probability-aware matching — **proposed** (PR #3717) · unified CoNLL-U extraction — **proposed** (PR #3694)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Tagger` trait | T2 | `harper-pos-utils/src/tagger/mod.rs:15` |
| `BrillTagger<B>` | T2 | `harper-pos-utils/src/tagger/brill_tagger/mod.rs:23` |
| `apply_patches` (ordered replay) | T2 | `harper-pos-utils/src/tagger/brill_tagger/mod.rs:42` |
| `FreqDict` baseline tagger | T2 | `harper-pos-utils/src/tagger/freq_dict.rs:10` |
| `Patch` (from/to/criteria) | T2 | `harper-pos-utils/src/tagger/brill_tagger/patch.rs:9` |
| `PatchCriteria` (6 variants) | T2 | `harper-pos-utils/src/patch_criteria.rs:6` |
| `brill_tagger()` process-wide `Arc` | T2 | `harper-brill/src/lib.rs:20` |
| `include_str!` of the trained model | T2 | `harper-brill/src/lib.rs:9` |
| `Document::parse` tagging loop | T2 | `harper-core/src/document.rs:181` |
| `DictWordMetadata::pos_tag` | T2 | `harper-core/src/dict_word_metadata.rs:55` |
| `UPOSSet` pattern | T2 | `harper-core/src/patterns/upos_set.rs:10` |
| `TokenKind::is_upos` | T2 | `harper-core/src/token_kind.rs:375` |
| Weir bare-tag parse site | T2 | `harper-core/src/weir/parsing/expr.rs:69` |
| Birth commit / PR | T3 | `db89187c3`, 2025-06-16, PR #1344 |
| `trained_tagger_model.json` (659,686 B, 30,468 lines, 26,900 dict entries, 201 patches) | T3 | `harper-brill/trained_tagger_model.json` |
| `UPOS` enum, 16 variants, default `NOUN` | T3 | `harper-pos-utils/src/upos.rs:25`, `:41` |
| CoNLL-U `X` dropped on import | T3 | `harper-pos-utils/src/upos.rs:80` |
| `UPOS::from_conllu` | T3 | `harper-pos-utils/src/upos.rs:62` |
| `BrillTagger::train` (epochs, candidate_selection_chance) | T3 | `harper-pos-utils/src/tagger/brill_tagger/mod.rs:262` |
| `epoch` candidate scoring + contraction merge list | T3 | `harper-pos-utils/src/tagger/brill_tagger/mod.rs:133`, `:157` |
| `Patch::generate_candidate_patches` | T3 | `harper-pos-utils/src/tagger/brill_tagger/patch.rs:19` |
| `ErrorCounter` / `ErrorKind` | T3 | `harper-pos-utils/src/tagger/error_counter.rs:6` |
| `FreqDictBuilder::inc_from_conllu_file` | T3 | `harper-pos-utils/src/tagger/freq_dict_builder.rs:62` |
| `iter_sentences_in_conllu` | T3 | `harper-pos-utils/src/conllu_utils.rs:7` |
| `TrainBrillTagger` CLI subcommand | T3 | `harper-cli/src/main.rs:150`, `:573` |
| `training` feature gate | T3 | `harper-pos-utils/Cargo.toml:25`, `harper-cli/Cargo.toml` `[features]` |
| Tagger-wins precedence over dictionary | T3 | `harper-core/src/document.rs:208` |
| `infer_pos_tag` (dictionary fallback, `exactly_one`) | T3 | `harper-core/src/dict_word_metadata.rs:132`, `:183` |
| 95% accuracy claim, UD_English_GUM | T3 | PR #1344 body, merged 2025-06-16T21:33:49Z |
| Sole post-birth model edit (one hand-written patch) | T3 | `7c338eb6f`, 2025-07-04, PR #1486 |
| Docs page (8 lines, never revised) | T3 | `packages/web/src/routes/docs/contributors/brill/+page.md` |
| `WordIs` prefix-match defect | T4 | `harper-pos-utils/src/patch_criteria.rs:99` |
| `enforce_pos_exclusivity` with no caller | T4 | `harper-core/src/dict_word_metadata.rs:200` |
| `test_pos_tagger` snapshot harness | T4 | `harper-core/tests/pos_tags.rs:366`, `:231` |
| Big-endian snapshot failure | T4 | issue #1823, opened 2025-08-28, open |
| Orphaned `brill_chunker()` | T4 | `harper-brill/src/lib.rs:35`; orphaned by `7f10ac605`, 2025-07-31, PR #1579 |
| Vestigial `[build-dependencies]`, no `build.rs` | T4 | `harper-brill/Cargo.toml:13` |
| Divergent blog-post URLs (hyphen vs underscore) | T4 | `harper-pos-utils/src/tagger/brill_tagger/mod.rs:21` vs docs `+page.md:8` |
| Asymmetric candidate window `-3..3` vs `-4..=4` | T4 | `harper-pos-utils/src/tagger/brill_tagger/patch.rs:32` vs `:57` |
| Joint tagger proposal | T5 | PR #3717, opened 2026-06-25 |
| CoNLL-U extraction unification / span-shift fix | T5 | PR #3694, opened 2026-06-21 |

*Trellis-relevant observation:* The learned artifact is a plain-text ordered rule list, so a maintainer could hand-append a single patch as a normal code review (`7c338eb6f`) — learning and authoring share one representation, which is exactly the property a composable expert system wants when user data must be promotable into engine behaviour. The precedence rule is worth copying and worth watching: `document.rs:208` lets the statistical layer overwrite curated per-word metadata unconditionally, with the curated inference reduced to a null-fallback, and nothing narrows the remaining metadata afterwards because the narrowing function is unreachable. The cautionary half is verification: a 659 KB learned artifact ships with zero unit tests in its own crates and a regression harness named for it that never prints the value it produces.

## Uncovered
- No CoNLL-U corpus is present in the clone and `justfile`/`.gitignore` name none, so the exact treebank revision behind the shipped 201 patches and 26,900 dictionary entries cannot be recovered from the repository; only PR #1344's prose names `UD_English_GUM`.
- The shipped model's own accuracy is unstated anywhere in-tree. PR #1344's 95% figure is explicitly a mid-review measurement followed by an intent to train further, so it does not necessarily describe the committed artifact.
- Read-only constraint: I did not build, run, or train anything, so the `WordIs` prefix-match finding is derived from source, not from an executed counterexample.
- Elijah Potter's linked blog post on transformation-based learning was not fetched; only the two divergent in-repo URLs were compared.

<a id="c7"></a>

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

<a id="c8"></a>

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

<a id="c9"></a>

## C9 — The Contribution Machine: Policy, Task Runner, CI, and the Review Gate

*Charter: the social and mechanical apparatus that converts an outside patch — including one written by a model — into a merged commit; the code being contributed is out of scope.*

- **T1 — essence.** A project taking patches from strangers must convert unverified intent into trusted commits at a cost that does not grow with contributor count. Three levers carry it: publish the rules where humans and machines both read them; make every gate runnable by the contributor before submission, so reviewers spend attention on judgment rather than mechanics; and vest merge authority in a named person who can be held responsible. Machine-written patches add a fourth — provenance disclosure — because reviewers must allocate scrutiny by how a patch was produced, not only by what it changes.

- **T2 — current machinery.** Two root files carry policy: `AGENT_POLICY.md`, a verbatim maintainer blog post, and `AGENTS.md`, a route map plus rule-authoring instructions. One `justfile` is the whole tooling surface; `.github/workflows/just_checks.yml` fans its task names across a CI matrix, and `merge_group` triggers route merges through a queue. `.github/pull_request_template.md` adds an AI Disclosure checkbox block and a test-provenance block. `harper-core/tests/snapshot.rs` diffs generated output against committed `.snap.yml` baselines; `fuzz/` holds `cargo-fuzz` targets; `contributors/committer` vests merge authority; `stale.yml` closes inactivity.

- **T3 — with receipts.** The `justfile` (973 lines) defines 63 recipes and 30 aliases; CI runs nine (`just_checks.yml:19-30`). 6,090 `#[test]` functions exist, 5,976 in harper-core, plus 1,838 inline tests across 351 `.weir` files, 34 macro-built corpus tests (`run_tests.rs`), 64 Playwright tests across 23 specs, and 20 snapshot baselines over 10 corpus documents. `AGENTS.md` was born 2026-02-18 (`463533a6c`, #2751) at 143 lines, now 265. `AGENT_POLICY.md` landed 2026-06-30 (`8d48e6b8f`, #3738); AI-disclosure checkboxes 2026-05-15 (`591c524ee`, #3375).

- **T4 — the frontier.** Disclosure is unenforced — no workflow reads the checkbox. Of 227 merges after the template landed, 50 dropped the section and 6 left it blank; enforcement is manual and rare, four closures citing the policy (#3196, #3425, #3431, #3610), Elijah Potter writing "I am closing this PR for violating the agent policy." `committing/+page.md:10` still claims CI runs `just precommit`, retired 2025-10-01 (`bb2af3ca1`, #2037). `cargo-fuzz` appears in no workflow or recipe. `snapshot.rs:67` rewrites its baseline before failing. Median `.weir` file: 2 tests.

- **T5 — future plans.** Proposed, not built. Issue #3473 (2026-05-22, labels `ci`, `harper-cli`) asks for a published GitHub Action wrapping `harper-cli`, turning the project's own checker into other repositories' CI. Issues #3242 and #3337 (both labelled `justfile`, `good first issue`) propose `ls-linters` and a wrong-preposition tool as new recipes, continuing the pattern of growing the runner surface rather than adding loose scripts. PR #2241 (open since 2025-11-25, +428/-0) proposes a consistency check over the linter registry. `AGENTS.md:15` asks humans to migrate agent guidance into the website; unstarted.

*Status ledger:* `AGENT_POLICY.md` in-repo — **shipped** · AI Disclosure checkbox — **shipped-but-unenforced** · manual agent-policy closure — **shipped** · `justfile` as sole tooling surface — **shipped** · `just_checks.yml` 9-task matrix — **shipped** · merge queue (`merge_group`) — **shipped** · `just precommit` as the CI gate — **retired** (2025-10-01, `bb2af3ca1`) · snapshot baselines — **shipped** · `just fuzz` (quickcheck loop) — **shipped** · `cargo-fuzz` targets — **shipped-but-unenforced** (no CI or recipe caller) · 15-test floor for Weir rules — **shipped-but-unenforced** · committer review gate — **shipped** (social only; no CODEOWNERS) · stale bot 60/14 days — **shipped** · dependabot weekly with 7-day cooldown — **shipped** · `harper-cli` GitHub Action — **proposed** (#3473) · linter-registry consistency check — **proposed** (#2241)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `AGENT_POLICY.md` (35 lines, three rules: brief, grounded, honest) | T2 | `AGENT_POLICY.md:19,25,29` |
| `AGENTS.md` (265 lines) | T2 | `AGENTS.md`; born `463533a6c` / PR #2751 |
| `justfile` — 63 recipes, 30 aliases, 973 lines | T2 | `justfile`; born `66da0b27b` 2024-07-07 |
| `just_checks.yml` 9-task matrix | T2 | `.github/workflows/just_checks.yml:19-30` |
| Merge queue (`merge_group` trigger) | T2 | `.github/workflows/just_checks.yml:8` |
| AI Disclosure checkbox block (4 options) | T2 | `.github/pull_request_template.md`; `591c524ee` / PR #3375 |
| Test-provenance checkbox block | T2 | `.github/pull_request_template.md` ("If Your PR Implements or Enhances a Linter") |
| `snapshot_all_text_files` harness | T2 | `harper-core/tests/snapshot.rs:76` |
| `test_most_lints` / `test_pos_tagger` | T3 | `harper-core/tests/linters.rs:192`, `tests/pos_tags.rs:366` |
| 20 snapshot baselines over 10 corpus docs | T3 | `harper-core/tests/text/linters/`, `tests/text/tagged/` |
| 5 `cargo-fuzz` targets | T2 | `fuzz/Cargo.toml`; added `ad429ad0d` / PR #1949, 2025-11-19 |
| `just fuzz` = `QUICKCHECK_TESTS=100000 cargo test` loop | T3 | `justfile:644-653` |
| `register-linter` codegen recipe (sed-injects into `mod.rs`/`lint_group.rs`) | T3 | `justfile:655-664` |
| Committer role and 15-merged-PR heuristic | T2 | `packages/web/src/routes/docs/contributors/committer/+page.md:9,20` |
| Testing-strategy doc (risk-driven, "check" vs "testing") | T2 | `.../contributors/testing-strategy/+page.md`; `dd2f10fad` / PR #3845 |
| Reviewer playbook (Actions artifacts, `cargo install --git`, Docker) | T2 | `.../contributors/review/+page.md` |
| Production feedback loop → "challenge" lint IDs | T2 | `.../contributors/testing-strategy/+page.md:125` |
| Stale bot: 60 days stale, 14 to close | T2 | `.github/workflows/stale.yml:18-19` |
| Dependabot: cargo/npm/actions weekly, 7-day cooldown | T3 | `.github/dependabot.yml` |
| Toolchain pins: `stable` + wasm32 target; Node `lts/*`; biome 2.3.3 | T2 | `rust-toolchain.toml`, `.node-version`, `biome.json:2` |
| Nix devShell | T2 | `flake.nix` |
| Docker path used for review (web + demo) | T2 | `Dockerfile`; `.../contributors/review/+page.md:43-49` |
| Stale claim: "we run `just precommit` through GitHub Actions" | T4 | `.../contributors/committing/+page.md:10` (written `4901fc38d` 2025-01-16) |
| CI's precommit→matrix migration | T4 | `bb2af3ca1` 2025-10-01, PR #2037; workflow renamed `precommit.yml`→`just-checks.yml`→`just_checks.yml` |
| Self-overwriting snapshot baseline | T4 | `harper-core/tests/snapshot.rs:62-71` |
| Agent-only 15-test floor (absent from human `author-a-rule`) | T4 | `AGENTS.md:226,248` vs `.../contributors/author-a-rule/+page.md` (301 lines, no floor) |
| Policy-violation closures | T4 | PRs #3196, #3425, #3431, #3610 (+ #3434 closed for non-response) |
| Review doc cites "PR #445" but links `/pull/455` | T4 | `.../contributors/review/+page.md:30` |
| Absent: CODEOWNERS, labeler, disclosure-checking workflow | T4 | `.github/` (7 workflows, none of these) |
| `harper-cli` as a published GitHub Action | T5 | issue #3473 |
| `ls-linters` recipe; wrong-preposition recipe | T5 | issues #3242, #3337 |
| Linter-registry consistency test | T5 | PR #2241 |
| Migrate `AGENTS.md` guidance into the website | T5 | `AGENTS.md:15-16` |

*Sampling disclosure:* Four complete censuses, not random samples. (1) All 227 PRs merged 2026-05-18→2026-07-23 — every merge after the AI-disclosure template landed 2026-05-15 — fetched with full bodies and parsed for checkbox state. (2) All 220 closed-unmerged PRs (2024-03-04→2026-07-17) with full comment threads. (3) All 122 open PRs. (4) All 561 open issues. Repo totals at query time: 1,931 merged / 220 closed / 122 open. This census supports claims about disclosure behavior *in the post-template window only*; it cannot speak to the 1,704 merges before the template existed. It is also author-skewed: hippietrail authored 130 of 227 (57%), so the aggregate 85% non-bot section-retention rate (76% excluding him) reflects a small active core, not 135 authors. Enforcement counts derive from string-matching comment bodies for "agent polic", so silently-enforced cases are invisible; four is a floor, not a total.

*Trellis-relevant observation:* The reusable move is that harper turned a prose policy into a checkbox the contributor must physically edit — the disclosure rate is high (85% retention, 68/171 admitting AI involvement, 7 fully autonomous PRs merged) precisely because the template makes silence visible rather than default. The cautionary half is that no workflow reads that checkbox, so the whole apparatus rests on one maintainer noticing; four closures in 220 is enforcement by attention, which does not scale, and the same gap explains why an agent-only "at least 15 tests" instruction is met by 20% of post-instruction Weir rules. For a house prompt: an instruction with no reader is a wish, and the drift found here (`committing/+page.md` advertising a CI gate retired nine months earlier) argues for generating contributor docs from the workflow files rather than restating them.

## Uncovered
- Branch-protection settings and required-check configuration — readable only with repo admin scope; the merge gate described in `committer/+page.md` could not be verified against GitHub's actual enforcement.
- Review *latency* (time-to-first-review, merge lead time) was not computed; the closed-PR fetch captured lifetime but the merged-PR fetch did not carry `createdAt`.
- Whether the 122 open PRs include stalled agent-authored work was not characterized beyond title matching; PR bodies were not fetched for the open set.
- Discord, where `contributors/introduction/+page.md` routes questions, is off-record and outside the repository.
- Per-rule (as opposed to per-file) Weir test counts: 11 grouped directories under `weir_rules/` collapse several `.weir` files into one public rule, so the median-2-tests figure is per file and may understate per-rule coverage.

---

## The cross-link lattice

The branches were written in isolation, so every link below was drawn afterwards by the orchestrator
from the branches' own entity ledgers. Each edge names the shared artifact, not a shared theme.

| From → To | The artifact they share |
|---|---|
| C7 → C1 | `Mask` yields sorted `Span<char>`s that become the lexer's input window; both classes independently name offset preservation as the load-bearing invariant. |
| C1 → C2 | `Expr::run` returns `Span<Token>` — C1's addressing type is C2's return type. The 2025-06 `Pattern`→`Expr` rename is what made this true. |
| C2 → C3 | `AstExprNode::to_expr` (`weir/ast.rs:104`) lowers every Weir node onto C2's combinators. Weir has **no second matcher** — which is why C2's `Not` gap (#3848) is also Weir's: `!x` compiles to a token-consuming `UnlessStep`. |
| C3 → C4 | `WeirLinter` implements C4's `ExprLinter`, so 328 of the 820 registered rule names are Weir-backed and indistinguishable to config. |
| C5 → C1 | `DictWordMetadata` is written into token metadata during `Document::parse`; C1's 67 delegated `TokenKind` predicates read C5's record. |
| C6 → C5 | `document.rs:208` lets the Brill tagger **overwrite** the dictionary's part-of-speech unconditionally; C5's curated metadata is the loser in that precedence, and C6 flags the narrowing function that would repair it as unreachable. |
| C6 → C3 | Weir's 16 bare UPOS keywords are C6's tag inventory. A tagger error is therefore a Weir rule misfire, with no channel between them. |
| C4 → C8 | The 820-name flat namespace *is* the config API every surface in C8 keys on — LSP settings, `harper.js`, the desktop settings UI. |
| C3 → C8 | Weirpacks reach users through exactly one entry point, `harper-wasm/src/lib.rs:531`; the Rust writer half is dead code (C3 T4). |
| C9 → C3 | `AGENTS.md:226` sets a 15-test floor for new rules; C3 measures 89 of 351 rules meeting it and C4 measures 297 of 351 below it. C9's finding — *an instruction with no reader is a wish* — is the mechanism. |
| C9 → C4 | The clash-detection test (`#2374`) is C4's namespace guard; C9's CI census explains why a test rather than a runtime warning was enough to close the issue. |

### The two findings every branch reached independently

Nine cartographers, no contact, two convergent results:

1. **Duplicated knowledge is harper's dominant defect class.** Two TLD tables (C1), a dead duplicate
   trait born in the same commit as its live twin (C2), a manifest validated in both Rust and
   TypeScript (C3), a flat namespace whose composition is nested (C4), a lossy hash key merging two
   dictionary entries into one (C5), two divergent blog URLs (C6), a language list that is 50 long in
   one surface and 3 in another (C7/C8), lint colours in three files (C8), and a contributor doc
   advertising a CI gate retired nine months earlier (C9).
2. **Reach lags capability everywhere.** Every class ships more than its surfaces expose. This is why
   the map reports reachability as a claim separate from correctness — nine independent branches found
   the same asymmetry without being told to look for it.

---

## What a builder of a composable expert system should take

Aggregated from the nine `Trellis-relevant observation` slots. **These are the cartographers' words
compressed, not new claims**; each traces to a branch above.

**Copy:**

- **A rule and its acceptance tests as one artifact** (C3). `test` and `allows` sit beside `expr main`;
  a generated harness runs them with no test file to maintain.
- **A match that returns an address, not a boolean** (C2). Because `Expr` returns a `Span`, the
  traversal is written once and 279 rule files inherit non-overlapping iteration for free.
- **A flat, stable name as the real API** (C4). 820 names; the code behind each is swappable precisely
  because the name is not.
- **Two composable interfaces for format support** (C7): a pure `text → sorted allowed spans` selector
  and a pure `chars → tokens` parser. Twenty-plus formats at ~40 lines each.
- **Retrieve-then-rerank, with editable priors** (C5). A cheap automaton finds candidates; a separate
  readable scorer holds the priors the metric cannot express.
- **A learned artifact in the same representation as an authored one** (C6). The tagger's model is an
  ordered, readable rule list — a maintainer hand-appended one patch as an ordinary review.
- **Make silence visible** (C9). A disclosure checkbox the contributor must physically edit produced
  85% retention and 68 admissions of AI involvement.
- **Local-only telemetry** (C8). Records stay on disk and reach a summary view only if the user
  uploads their own file.

**Avoid:**

- **A self-testing artifact with no floor at registration** (C3). 64 of 351 Weir rules ship zero
  assertions and the generated test still passes vacuously. The runner is not the guard; registration is.
- **A lossy key over user-merged data** (C5). `WordId`'s 64-bit case-folded hash silently merges two
  entries and canonical spelling becomes insertion-order dependent (issue #2411) — a defect a
  personalized system merging user vocabulary into a curated core would inherit exactly.
- **A flat namespace over nested composition** (C4). Sub-linters and merged pack rules exist without
  being addressable, so clashes overwrite silently.
- **Two match contracts that never converge** (C2). `Pattern` and `Expr` still coexist; the user meets
  it as a compile error when combining a leaf negator with a zero-width anchor.
- **Restating engine-owned facts per surface** (C8). Lint colours in three hand-maintained copies.
- **An instruction with no reader** (C9). The 15-test floor is met by roughly one rule in five.

---

## Provenance & method

**Subject.** `Automattic/harper`, cloned 2026-07-23 with `--filter=blob:none`. Most recent commit at
clone time `efa59c33` (2026-07-24). Repo metadata read via `gh api` the same day.

**Method.** Nine read-only sub-agent cartographers, one per class, spawned in parallel from a single
byte-identical ground block (`GROUND.md`) and a rigid five-tier return frame. Composition discipline
followed the house `subagent-composition` skill; the prompt bytes were authored under
`prompt-engineering` and `hypershot-protocol` first, per house rule 16. Each cartographer:

- held a disjoint read charter and a disjoint write scope (one branch file);
- could not see, and was forbidden to read, any sibling's output;
- was required to carry a `path:line`, commit SHA, or PR number on every quantitative claim;
- was required to fill an `## Uncovered` slot, so a gap could not hide as silence;
- was forbidden to run `cargo`, `pnpm`, `just`, or `npm`.

The trunk, the temporal cross-section, the cross-link lattice, and the aggregation above were composed
by the orchestrator **after** all nine returned, because a sibling speculating about a class it cannot
see produces exactly the unreconcilable claim the fan-out discipline exists to prevent.

**Telemetry of the run**, as reported by the harness:

| Class | Tokens | Tool uses |
|---|---|---|
| C1 document model | 144,634 | 38 |
| C2 expression system | 113,508 | 49 |
| C3 Weir | 159,861 | 65 |
| C4 linter corpus | 167,251 | 70 |
| C5 spelling & dictionaries | 183,002 | 84 |
| C6 POS tagging | 114,271 | 64 |
| C7 format adapters | 124,806 | 61 |
| C8 delivery surfaces | 156,354 | 78 |
| C9 contribution machine | 120,134 | 49 |
| **Total** | **1,283,821** | **558** |

### Honest gaps — what this map cannot support

1. **Nothing was executed.** Every test count is a count of `#[test]` attributes or `test` lines in
   source, **never a green run**. Every defect — the NBSP tokenizer stop (C1), the `WordIs` prefix
   match (C6), the `WordId` collision (C5) — is derived from reading. None was confirmed by an
   executed counterexample.
2. **Reachability is workspace-scoped.** "No non-test caller" means no caller *inside this workspace*.
   Several flagged items sit on public types and may be consumed by downstream crates.
3. **The PR record was sampled unevenly.** Only C9 ran a complete census (all 227 post-template merges,
   all 220 closed-unmerged, all 122 open, all 561 open issues) and disclosed its author skew —
   hippietrail authored 130 of 227, so aggregate rates describe a small active core, not 135 authors.
   Other classes opened only the PRs touching their own paths.
4. **T5 records requests, not commitments.** An open PR or issue means someone asked. No maintainer
   endorsement should be read into any T5 entry.
5. **One retype step occurred.** The Stage-1 characterization used by the parallel complexity
   convocation was re-emitted by the orchestrator because the harness wrote a zero-length transcript.
   Disclosed in that file's header.
6. **The map is a snapshot of a fast-moving project.** harper merged roughly 60 PRs per month across
   the mapped period. T4 and T5 decay fastest; T1 and T2 should hold.

**Verification date:** 2026-07-24. **Pinned to:** `efa59c33`.

If you re-verify and something has moved, the source wins and this file has a defect. Fix the file.
