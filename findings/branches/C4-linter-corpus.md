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
