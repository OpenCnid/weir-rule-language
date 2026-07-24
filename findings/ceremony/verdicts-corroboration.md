# Seat 3 — Corroboration (The Unauthored Witness) — verdicts

Anchors worked first; discrimination confirmed; results not reported per instruction.

## Independent channels located in this artifact

| Channel | Where | What it is |
|---|---|---|
| Whole-document snapshots | `harper-core/tests/text/` + `.../linters/*.snap.yml` | 10 documents incl. *Alice's Adventures in Wonderland* (3,709 snapshot lines), *The Great Gatsby* (8,069), *The Constitution of the United States* (1,873). `linters.rs` runs `LintGroup::new_curated` over each and diffs against a committed snapshot. Nobody wrote these documents as tests for any unit. |
| Report-named regression fixtures | `harper-core/tests/test_sources/` | 20 `issue_NNNN.md` + 2 `pr_NNN.md` fixtures; `run_tests.rs` lints each through `LintGroup::new_curated`. |
| Description dogfood | `lint_group/mod.rs:1200` `lint_descriptions_are_clean` | Lints all 820 rule descriptions — prose written as documentation — with the full curated group. |
| Source-comment dogfood | `justfile:477` `dogfood` | `harper-cli lint` over every `.rs` file in the repository. |
| Benchmark channel | `harper-core/benches/parse_essay.rs` | `lint_essay` (warm) and `lint_essay_uncached` (cold: rebuilds `new_curated` each iteration) over a real essay. |
| Fuzz channel | `fuzz/fuzz_targets/` | 5 targets, all on document parsers; none on `weir`, `weirpack`, or the lint group. |
| External record | `gh` on `Automattic/harper` | Labels incl. `false-positive`, `false-negative`, `agreement`, `language-and-dialect`, `weir`. |
| Curated switch surface | `harper-core/default_config.json` | 820 `Bool` switches (811 enabled), each labelled, under 15 named groups (Proper Nouns … Regionalisms and Dialect). Enforced complete by `structured_config/mod.rs:313`. |
| Rule identity at the writer | `harper-ls/src/diagnostics.rs:134` | `code: origin_tag` — the rule name from `organized_lints` reaches the editor diagnostic. |

## U1 — `Pattern` trait — **clean**

Six implementors (`patterns/{derived_from,invert,modal_verb,nominal_phrase,upos_set,whitespace_pattern}.rs`). Consumed by 111 files under `linting/`. Decisively, `AstExprNode::to_expr` boxes `UPOSSet`, `WhitespacePattern`, `DerivedFrom` (`weir/ast.rs:113-116`), so all 351 shipped `.weir` rules lower onto this trait. Those rules and those 111 Rust rules all sit in `new_curated`, which the snapshot harness runs over Alice, Gatsby and the Constitution. Unauthored corpora exercise it.

## U2 — `Step` trait + blanket `impl<P: Pattern>` — **clean**

Direct implementors: `AnchorStart`, `AnchorEnd`, `UnlessStep`. `AnchorStart` is used at `lib.rs:270` in `remove_lints_overlapping_expr`, on the path of every linted document. `SequenceExpr::then_unless` (`sequence_expr.rs:277`) constructs `UnlessStep`; `need_to_noun.rs` and `weir/ast.rs` import it. The blanket impl is what every `.t_aco("…")` token step in hundreds of rules travels through, and those rules fire in the committed whole-document snapshots.

## U3 — `Expr` trait + blanket `impl<S: Step>` — **clean**

279 files implement `ExprLinter`; 224 `insert_expr_rule!` calls place them in the curated group. Every lint in the three whole-document snapshots that is not spellcheck comes through this contract. `lint_essay` and `lint_essay_uncached` measure the composed cost on real prose.

## U4 — `AstExprNode` — **clean**

`lint_group/mod.rs:588` merges `weir_rules::lint_group()` into the curated group, so all 351 `.weir` rules parse to this enum and run over the unauthored corpora. The external record joins back and closes: #1965 (*Create DSL So Users Can Author Rules*, external, predates the layer) motivated it; #3393, filed by an outside contributor against `let becomes` alternatives, is CLOSED 2026-05-19 and fixed by `cd4547838` "fix(weir): test runner now tries all 'becomes' alternatives"; #3229 is an open false-positive against `DoToDueTo`, a `.weir` rule — reports land on this structure and are acted on. A dedicated `weir` issue label and a shipped Weir Studio surface (`packages/web/src/routes/weir/studio/`) exist.

## U5 — `optimize` — **clean**

`WeirLinter::new` calls `parse_str(weir_code, true)` unconditionally (`weir/mod.rs:70`; the expression form at `:31`). `use_optimizer: false` appears only inside the parsing module's own unit tests. So `while optimize(&mut stmts) {}` (`parsing/stmt.rs:44`) runs over all 351 shipped rule ASTs — 145 of which contain the `[...]` arrays its `Arr` branch collapses (`expr main [(all of the sudden), (all of sudden), (all the sudden)]`). That is exercise on a corpus nobody wrote to defend the optimizer, which outweighs its three bespoke unit tests. Cost is bounded: parse happens once per distinct rule source behind a 10,000-entry static `PARSE_CACHE` (`stmt.rs:25`), so it is not borne per document and `unmeasured_standing_cost` does not reach. Noted as perishable: no channel measures the optimizer's *benefit*; that is a benefit claim, outside my cost class.

## U6 — `validate_required` — **drawback: `unexercised_in_the_wild`**

- No `.weirpack` artifact exists anywhere in the tree.
- Across the entire workspace, the only reads of `author()`, `version()`, `description()`, `license()` are the four asserts in the authored `round_trip_weirpack_bytes` test (`weirpack/mod.rs:238-241`). Every real consumer reads rules and dictionary only and never touches these fields: `harper-cli` (`lint.rs:453` `pack.to_lint_group()`), `harper-wasm::import_weirpack` (`lib.rs:531-566`), and the Chrome background worker — whose `WeirpackMeta.version` (`background/index.ts:586`) comes from `chrome.storage.local`, not the manifest.
- The desktop pack list is hardcoded mock data: `settings-data.ts:299` with fabricated ids `pack-001`/`pack-002`/`pack-003`, sizes and dates.
- The only external item is #3652 (OPEN, external user): "Is there any registry of weir packs I could find?" — the distribution channel this metadata exists to feed does not exist.
- Counter-signal, named rather than averaged: the Weir Studio independently re-validates the same four fields (`weir/studio/+page.svelte:215`). That is a pre-flight mirror placed downstream of this check on the same project's own authoring surface, not an outside signal that the requirement earns its place.

Producing one fixture pack in this domain is cheap; none exists. Under my uncertainty posture that absence is a finding, not an abstention — the deciding in-repo reader count is fully reachable and #3652 is a reachable external proxy that answers negatively.

## U7 — `Linter` trait — **clean**

`description()` feeds `all_descriptions()` (`lint_group/mod.rs:500`), rendered on the public rules docs page (`packages/web/src/routes/docs/rules`). `lint_descriptions_are_clean` (`mod.rs:1200`) lints all 820 descriptions with the full curated group — prose written as documentation, not as fixtures, and a real dogfood hit surface. The switch path closes: `organized_lints` keys by rule name and `harper-ls` emits it as the LSP diagnostic `code` (`diagnostics.rs:134`), so a writer who receives a lint has the identity needed to find the labelled switch. Sampled descriptions are user-facing prose ("Looks and provides corrections for misspelled words.", "Guides this expression toward the standard `all of a sudden`."), not mechanism restatements — the `illegible_switch_surface` class does not fire.

## U8 — `lint_group/mod.rs` — **clean**

Standing cost is measured, not assumed: `lint_essay` and `lint_essay_uncached` (`benches/parse_essay.rs`) benchmark this exact composed surface on a real essay, warm and cold. Switch legibility is enforced mechanically: `curated_default_config_lists_every_registered_rule` (`structured_config/mod.rs:313-336`) fails if any registered rule lacks a `default_config.json` entry, and all 820 carry a human label under 15 named groups. The runtime-extensible `add` introduced by `7fb35c0d` is exercised by three independent consumer surfaces (`harper-cli --weirpack`, `harper-wasm::import_weirpack`, the Chrome background worker), not by tests alone. The external misfire record is thin against 811 default-enabled rules: 9 issues carry the `false-positive` label across the repository's whole history, several closed (#3861, #3851, #2682, #721) — `contradicted_by_reports` does not fire.

---

Verdicts are as of the record read 2026-07-23 and reopen on new external signal: a `.weirpack` fixture landing, a pack registry appearing, a benchmark case for the weir parse path, or accumulation of false-positive reports against the expression layers.
