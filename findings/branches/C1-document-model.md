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
