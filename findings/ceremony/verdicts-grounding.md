# Seat 1 — Grounding (The Rescued Sentence) — verdicts

One question per unit: does the artifact contain a committed text — anywhere, any distance — whose
bytes read differently if this layer were absent? Prose about a layer is a claim, not evidence.

Search surfaces actually opened: `harper-core/src/{patterns,expr,weir,weirpack,linting}`, the 351-file
`.weir` corpus at `harper-core/src/linting/weir_rules/`, `harper-core/tests/` (snapshot harness
`snapshot.rs`, whole-document corpus `tests/text/`, issue-numbered regression corpus
`tests/test_sources/issue_*.md`), `packages/harper.js/src/*.test.ts`, `harper-cli`, `harper-wasm`.

---

## U1 — `harper-core/src/patterns/mod.rs:42` — `trait Pattern` — CLEAN

Discriminating texts, near and far:

- Near: `patterns/word.rs:80` `Word::new("banana").find_all_matches_in_doc(&doc)` and
  `patterns/nominal_phrase.rs:63`, `patterns/word_set.rs:86`, `patterns/implies_quantity.rs:54` —
  every one of these dispatches through `Pattern::matches` into `PatternExt`/`MatchIter`
  (`patterns/mod.rs:57-105`), whose advance rule `self.index += len.max(1)` is the Pattern layer's
  own, not `ExprExt::iter_matches`'s `last_end` rule.
- Distant (the G-C1 shape): `patterns/mod.rs:117` `impl<F: Fn(&Token,&[char])->bool>
  SingleTokenPattern for F` is the only reason `weir/ast.rs:110` can return a bare closure
  (`AstExprNode::Progressive => Ok(Box::new(|tok, _| tok.kind.is_verb_progressive_form()))`) as a
  `Box<dyn Expr>`. That closure is reached by `weir_rules/RallyToReally.weir`, whose 12 `test` and
  7 `allows` lines are executed by `weir_rules/mod.rs:64 run_tests_for_weir_rules`. Delete the
  Pattern layer and those committed sentences change what they assert.

Multi-token return length is also load-bearing and exercised: `NominalPhrase` returns spans wider
than one token in `nominal_phrase.rs:63-102`.

## U2 — `harper-core/src/expr/step.rs:3` — `trait Step` + blanket `impl<P: Pattern>` — CLEAN

The layer's distinctive content versus `Pattern` is the *absolute cursor* argument: `Pattern::matches`
receives `&tokens[cursor..]` and cannot know where it sits, while `Step::step` receives both `tokens`
and `cursor`. `expr/anchor_start.rs:11` uses exactly that
(`tokens.iter_word_like_indices().next() == Some(cursor)`), and `anchor_start.rs` test
`matches_first_word` commits `assert_eq!(matches, vec![Span::new(0, 0)])` — one match, not one per
position. `anchor_end.rs` commits six more, including `test_word_not_at_end_of_doc` asserting
`matches.len() == 0`. Without the Step layer those bytes cannot be written. Traced.

The signed half of `Option<isize>` is untraced, but the dead bytes sit in U3, and I file a finding
where its bytes are; I do not double-file the same fact across sibling units.

## U3 — `harper-core/src/expr/mod.rs:68` — `trait Expr` + blanket impl — DRAWBACK: `phantom_variant_arm`

The trait itself is traced past any doubt (every `ExprLinter`, every `.weir` rule, `Filter`'s doctest
at `expr/filter.rs:15-28`). The fan-out inside the filed span is not.

`Expr::run` fans on the sign of the step:

```rust
if s >= 0 { Span::new_with_len(cursor, s as usize) }
else      { Span::new(add(cursor, s).unwrap(), cursor) }
```

I enumerated every `fn step(` in the whole tree — five, all of them:
`expr/step.rs:9` (declaration), `expr/step.rs:16` (`.map(|i| i as isize)` over a `usize`, never
negative), `expr/anchor_start.rs:10` (`Some(0)`), `expr/anchor_end.rs:12` (`Some(0)`),
`expr/unless_step.rs:23` (delegates to an inner `Step`). No committed byte in the artifact —
no test, no doctest, no `.weir` rule, no snapshot, no issue-numbered fixture — can produce a
negative offset, because negatives are producible only from Rust `Step` impls and there are no
others. The `else` arm, and `add`'s twin `if i.is_negative()` branch at `expr/mod.rs:112-114`, are
arms whose need is asserted by their presence and exhibited by nothing. This is G-D3's shape
(a fan-out no committed input reaches), not G-D1's.

Reopened by one address: any committed `Step` returning a negative.

Not adjudicated here (outside my seat): whether backward matching *should* be supported, or whether
a narrower return type would be better — that is design, and I am blind to it.

## U4 — `harper-core/src/weir/ast.rs:84` — `enum AstExprNode` + `to_expr` — CLEAN

All twelve variants have committed text that discriminates them, and every `to_expr` arm is reached:

| Variant | Discriminating text |
|---|---|
| `Whitespace` | `weir/parsing/expr.rs:144` |
| `Progressive` | `expr.rs` `parses_prog`; `weir_rules/RallyToReally.weir`, `TheirToTheyre.weir` (run by `run_tests_for_weir_rules`) |
| `UPOSSet` | `expr.rs:440-458` incl. `optimizes_upos_set` |
| `Word` | `expr.rs:151` |
| `DerivativeOf` | `expr.rs:405,414-418`; `weir_rules/AsMuchAs.weir`, `TheDifferenceBetween.weir` |
| `Punctuation` | `expr.rs:336-360` (Period/Comma/Hyphen) |
| `Not` | `expr.rs:237`; 22 `.weir` rules use `!` |
| `Seq` | `expr.rs:159-249` |
| `Arr` | `expr.rs:264,290` |
| `Filter` | `expr.rs:369,381,393`; `weir_rules/DoToDueTo.weir` `<(...), (do to)>` with committed `test` lines; `expr/filter.rs` doctest |
| `ExprRef` | `expr.rs` `parses_expr_ref`; 27 `.weir` rules use `@` |
| `Anything` | `expr.rs:489,497-501`; `weir_rules/DoToDueTo.weir`, `ImitateFrom.weir`, `IncludingButNotLimitedToPunctuation.weir` |

## U5 — `harper-core/src/weir/optimize.rs:3` — `fn optimize(&mut Vec<AstStmtNode>)` — CLEAN

The statement-level entry point (distinct from `optimize_expr`) is discriminated by
`weir/parsing/stmt.rs:321-330`:

```rust
assert_eq!(
    parse_str("expr main word", true).unwrap().stmts,
    vec![AstStmtNode::create_set_expr("main", AstExprNode::Word(char_string!("word")))]
)
```

The `expr` statement branch at `stmt.rs:163-170` always wraps in `AstExprNode::Seq(parse_seq(...))`,
so the unoptimized parse of that input is `Seq([Word])`. The assertion reads `Word` only because
`stmt.rs:43-45` runs `while optimize(&mut stmts) {}`. Delete `optimize` and that committed byte
flips. `optimize_expr`'s own arms are separately pinned by `expr.rs:281-293` and
`expr.rs:452-458`.

## U6 — `harper-core/src/weirpack/manifest.rs:75` — `validate_required` — DRAWBACK: `orphaned_guard`

`validate_required` is a rejection surface: it is called on every load (`manifest.rs:41`, inside
`from_reader`) and every write (`manifest.rs:47`), and its only observable effect is returning
`Err(Error::MissingManifestField(key))` / `Err(Error::InvalidManifestFieldType(key))`
(`manifest.rs:70-71`). Nothing in the artifact ever makes it return `Err`:

- The one Rust test, `weirpack/mod.rs:225 round_trip_weirpack_bytes`, sets all four fields
  (`set_author`/`set_version`/`set_description`/`set_license`, lines 227-230) and asserts only the
  four getters. It passes identically with the guard deleted.
- `MissingManifestField` and `InvalidManifestFieldType` appear at exactly two addresses each —
  `weirpack/error.rs:16,18` and `manifest.rs:70,71`. No committed text asserts either.
- There are no `.weirpack` files and no `manifest.json` fixtures anywhere in the tree.
- `packages/harper.js/src/weirpack.test.ts` does exercise two negative cases, but both are the
  *presence of the file* (`'Weirpack is missing manifest.json'`), a separate TypeScript
  implementation; its own manifest object carries all four fields. It never omits `author`,
  `version`, `description`, or `license`, and never supplies a non-string one.

The guard is present in form and reaches nothing — G-D2's shape. Reopened by exhibiting any
committed manifest, fixture, or test input missing or mistyping one of the four fields.

## U7 — `harper-core/src/linting/mod.rs:346` — `trait Linter` — CLEAN

- `description()` is exercised, not merely declared: `lint_group/mod.rs:1206 lint_descriptions_are_clean`
  pulls `all_descriptions()` across the whole curated group and runs the full curated `LintGroup`
  over each description string, panicking on any non-`Style` lint. Every registered rule's
  description text is therefore a committed byte whose fate depends on the method existing.
  `dont_flag_low_hanging_fruit_desc` (`lint_group/mod.rs:1185`) pins one such string verbatim.
  `can_get_all_descriptions_as_html` pins the `HtmlDescriptionLinter` blanket at
  `linting/mod.rs:365`.
- `&mut self` on `lint` is load-bearing: `lint_group/mod.rs:975` and `:1021` mutate `self` during a
  lint (`chunk_expr_cache.put`, `sentence_expr_cache.put`), which is impossible with `&self`.

## U8 — `harper-core/src/linting/lint_group/mod.rs` — CLEAN

Each named layer has text that fails without it:

- Name-keyed dispatch across the three `BTreeMap`s: `lint_group/mod.rs:1104 corrects_extention`
  asserts `organized.get("SpellCheck")` yields exactly one lint carrying
  `"Replace with: “extension”"` while `organized.get("SplitWords")` is empty — a result only a
  per-name organization can commit. `no_linter_names_clash` (`:1223`) pins the maps' key disjointness.
- The sentence-vs-chunk split: `weir_linter_uses_configured_sentence_scope` (`:1136`) registers via
  `add_sentence_expr_linter` and asserts `"one, two."` → `"three."`; the same input is silent under
  chunk scope (the trigger spans a comma).
- Flat string-keyed config: the same test's `group.config.set_rule_enabled("TestSentenceWeir", true)`,
  plus 820 registered names in the curated default config, each reached by
  `lint_descriptions_are_clean`.
- Runtime extensibility (`add`, post-`7fb35c0d`): `weir_rules/mod.rs:37 group.add($group_name,
  grouped_rule)` composes nested groups at runtime, and `weirpack/mod.rs:70-84 to_lint_group` builds
  a `LintGroup` from pack bytes — reached by `round_trip_weirpack_bytes` and by
  `harper-wasm/src/lib.rs:531 import_weirpack`.

Layer not adjudicated: the two `LruCache`s (`:344,346`), keyed `(char_hash, config_hash)`. A cache is
built to leave behavior identical and change only time, so "no committed byte discriminates it" is
not a grounding finding about it — its justifying channel is runtime cost, which my `blind_to`
forecloses. I neither credit nor charge it, and the unit's other layers are traced.

---

## Summary

| Unit | Verdict | Class |
|---|---|---|
| U1 `patterns/mod.rs:42` | clean | — |
| U2 `expr/step.rs:3` | clean | — |
| U3 `expr/mod.rs:68` | drawback | `phantom_variant_arm` |
| U4 `weir/ast.rs:84` | clean | — |
| U5 `weir/optimize.rs:3` | clean | — |
| U6 `weirpack/manifest.rs:75` | drawback | `orphaned_guard` |
| U7 `linting/mod.rs:346` | clean | — |
| U8 `linting/lint_group/mod.rs` | clean | — |
