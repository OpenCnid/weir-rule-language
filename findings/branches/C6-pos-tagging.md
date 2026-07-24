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
