# Seat 2 — Coherence (The Load-Bearing Layer): reasoning

Method: for each unit I asked whether every layer carries load no other layer already carries, and
whether the layers agree. Per `uncertainty_posture`, before calling any redundancy I required myself
to write the sentence naming a construction the two layers treat differently; where I could write it,
the unit is clean. I read structure only; I ran nothing.

---

## The match-contract ladder (U1, U2, U3)

The four coexisting layers are not four peers. Two blanket impls make them a strict ladder:

- `expr/step.rs:12-19` — `impl<P> Step for P where P: Pattern`, body
  `self.matches(&tokens[cursor..], source).map(|i| i as isize)`
- `expr/mod.rs:72-85` — `impl<S> Expr for S where S: Step + ?Sized`

Because both are blanket, no type can implement two rungs. `Expr` is the sole consumption interface:
`ExprLinter::expr(&self) -> &dyn Expr`, `SequenceExpr { exprs: Vec<Box<dyn Expr>> }`,
`AstExprNode::to_expr(..) -> Box<dyn Expr>`, `Filter { steps: Vec<Box<dyn Expr>> }`. Both
`SequenceExpr::then` (`sequence_expr.rs:169`) and `::with` (`:90`) are keyed on `impl Expr`, not on
`Step`.

### U1 — `Pattern` — DRAWBACK, `tier_duplication`

`Pattern::matches` is strictly narrower than `Step::step`: it is handed `&tokens[cursor..]`, so it
cannot see left context, and it returns `Option<usize>`, so it cannot move backward. A narrower
contract expresses less, never more. The lift in U2 is information-free — one `map`, no added term.

I searched for the distinguishing construction and could not write it:

- Six direct `impl Pattern` types (`DerivedFrom`, `Invert`, `ModalVerb`, `NominalPhrase`, `UPOSSet`,
  `WhitespacePattern`). Each is a verbatim `impl Step` with the slice inlined.
- Eleven `impl SingleTokenPattern` types reach `Expr` only via
  `patterns/mod.rs:116` (`impl<S: SingleTokenPattern> Pattern for S`). That blanket retargets onto
  `Step` with no coherence conflict — nothing else blanket-impls `Step` for a single-token shape.
- The one API consuming `Pattern` as a distinct type is `Invert { inner: Box<dyn Pattern> }`
  (`patterns/invert.rs:7`), used once (`then_than.rs:39`). `Box<dyn Step>` serves identically. And
  `Invert`'s body — `if inner.matches(..).is_some() { None } else { Some(1) }` — is the same job as
  `UnlessStep::new(e, |_,_| true)`, the idiom `OwnedExprExt::but_not` (`expr/mod.rs:190`) and
  `AstExprNode::Not` (`weir/ast.rs:117`) both use.
- `PatternExt` / `DocPattern` / `find_all_matches` / `find_all_matches_in_doc` have **zero**
  non-test consumers repo-wide (hits only in `patterns/{word,word_set,nominal_phrase,
  implies_quantity}.rs` `#[cfg(test)]` blocks). All production match iteration goes through
  `ExprExt::iter_matches_in_doc` (`document.rs:550`) and `ExprExt::iter_matches`
  (`expr_linter.rs:141`).

The nearest thing to a load is that `PatternExt::iter_matches` may advance by `len.max(1)`, sound
only because a Pattern match cannot extend backward, whereas `ExprExt::iter_matches` needs the
`span.start >= last_end` filter. That narrower-contract benefit is consumed only by tests. The
module's own doc calls `Pattern` "a simplified abstraction over [`Expr`]" — an ergonomic restatement,
which my `evidence_standard` excludes ("not merely how it reads").

Chronology corroborates: `Pattern` 2024-09-01; `Expr` renamed *from* `Pattern` 2025-06-13
(`a8fb0c6d`, 103 files) — the rename left the old rung standing beside its successor.

### U2 — `Step` — CLEAN

`Step` is also expressively subsumed by `Expr`. But the distinguishing construction exists and is
hard: `sequence_expr.rs:684-693`, `impl<S> From<S> for SequenceExpr where S: Step + 'static`.
Keyed on `Expr` this cannot be written — `SequenceExpr: Expr`, so it would collide with the standard
library's reflexive `impl<T> From<T> for T`. `Step` is the marker separating leaf steps from
composite expressions, and that is what makes the conversion expressible. It is consumed:
`confident.rs:16` (`SequenceExpr::from(|tok, _| ..)`) and `repeating.rs:66,77`. `Step` also carries
the signed-offset and cursor-plus-full-stream reach that `Pattern` cannot express — `AnchorStart`
(`step(.., cursor, ..) -> Some(0)` gated on `iter_word_like_indices().next() == Some(cursor)`) is
inexpressible as a `Pattern`. Removal changes what the structure can express. Clean.

### U3 — `Expr` — CLEAN

The convergence point; every tier lowers here. Its two branches disagree about nothing: `s >= 0` →
`Span::new_with_len(cursor, s as usize)`, else `Span::new(add(cursor, s).unwrap(), cursor)`. The
negative branch is exactly what gives `Step` its backward reach and is not duplicated anywhere. The
`s == 0` case yields an empty span, which `SequenceExpr::run` reads as a zero-width assertion
(`let is_zero_width = out.end == out.start;`) — the layers agree. `impl Expr for Box<dyn Expr>`
(`:96`) is not reachable through the `Step` blanket (`Box<dyn Expr>` is not `Step`), so it is not a
duplicate. Clean.

---

## U4 — `AstExprNode` + `to_expr` — CLEAN

Twelve variants; I checked each is both produced and consumed. All twelve are produced by the parser
(`weir/parsing/expr.rs:49,54,61,64,71,76,77,93,100,115,125,128` plus the `Seq` root at `:17`), and
`to_expr` (`weir/ast.rs:108-158`) matches all twelve exhaustively with no catch-all. No two variants
lower onto the same mechanism: `Anything`→`AnyPattern`, `Progressive`→`is_verb_progressive_form`
closure, `UPOSSet`→`UPOSSet`, `Whitespace`→`WhitespacePattern`, `Word`→`Word`,
`DerivativeOf`→`DerivedFrom`, `Not`→`UnlessStep`, `Seq`→`SequenceExpr`, `Arr`→`LongestMatchOf`,
`Filter`→`Filter`, `Punctuation`→closure, `ExprRef`→context lookup.

The obvious redundancy charge — "a fourth match-contract layer" — does not survive. This is a
lowering, not a rung: it expresses a parsed, cached, user-authored, serializable rule source that no
Rust tier can express. This is the C-C1 shape: the apparent overshoot is only apparent.

## U5 — `optimize` — DRAWBACK, `internal_contradiction`

The declared contract is `/// Returns whether an edit was made.` (`optimize.rs:4`, repeated at
`:20`). The `Arr` UPOS-collapse branch (`:41-48`) violates it:

```rust
} else if !children.is_empty() && children.iter().all(|n| n.is_upos_set()) {
    *ast = AstExprNode::UPOSSet(
        children.iter_mut().flat_map(|n| n.as_upos_set().unwrap()).copied().collect(),
    )
}
```

It assigns `*ast` — an edit — and never sets `edit = true`. Its own sibling branch four lines up
(`children.len() == 1` → `*ast = children.pop().unwrap(); edit = true;`) does set it, so the two
arms of one `match` disagree about what counts as an edit.

The value is consumed by two fixed-point loops: `while optimize(&mut stmts) {}`
(`weir/parsing/stmt.rs:44`) and `while optimize_expr(&mut root) {}` (`weir/parsing/expr.rs:20`). A
`false` therefore terminates optimization.

Distinguishing construction (owed by my `uncertainty_posture`, and it exists): the `[` branch at
`parsing/expr.rs:105-115` calls `parse_collection(.., parse_single_expr)`, so brackets nest. Weir
source `[[NOUN, VERB], [ADJ, ADV]]` parses to `Arr([Arr([UPOSSet, UPOSSet]), Arr([UPOSSet,
UPOSSet])])`. Pass 1: the outer `Arr`'s children are not `is_upos_set`, so it recurses; each inner
`Arr` collapses to a `UPOSSet` and returns `false`; the outer `edit` stays `false`; the loop exits.
The tree is left as `Arr([UPOSSet([N,V]), UPOSSet([ADJ,ADV])])`, lowering to a `LongestMatchOf` over
two `UPOSSet`s, where a second pass would have produced the single `UPOSSet([N,V,ADJ,ADV])` the
test `optimizes_upos_set` (`parsing/expr.rs:451-457`) shows is intended for the flat case.

The existing test only covers the flat `[PROPN, NOUN, VERB]`, where nothing follows the collapse —
which is why the missing write is invisible. The contradiction is internal to the unit: doc-declared
contract versus branch. Per `contradiction_sensitivity`, high and terminal.

## U6 — `validate_required` — CLEAN

Consumed at both boundaries: `from_reader` validates after parse (`manifest.rs:41`), `write_to`
validates before serialize (`:47`). It is the only manifest validator in the crate — `weirpack/mod.rs`
adds none. It composes `required_str` (`:66-72`) through the four generated getters, using their
`Result` and discarding the `&str`; that `Result` is load-bearing because `new()`/`Default` and the
open `set_field` path can produce a manifest missing fields (`new()`'s own doc says so).

The tempting finding — `set_author(v)` duplicates `set_field("author", Value::String(v))` — fails my
test. The typed setter makes a class of key error unrepresentable; `set_field("Author", ..)` compiles
and yields a manifest `write_to` rejects with `MissingManifestField("author")`, while `set_author`
cannot. The typed layer changes what the structure can express, at the type level. The open map and
the four required fields are two concerns, not two layers on one concern. Clean.

## U7 — `Linter` — CLEAN

Both declarations are consumed. `lint` is consumed by `LintGroup::organized_lints` and by
`impl Linter for LintGroup` (`lint_group/mod.rs:1048`); `description` by
`LintGroup::all_descriptions` (`:494`) and by the blanket `HtmlDescriptionLinter`
(`linting/mod.rs:354-366`).

Two candidate findings, both of which I talked myself out of by construction:

1. `ExprLinter` re-declares `description` with a byte-identical doc comment
   (`expr_linter.rs:80-83`). This is not two layers on one job — `ExprLinter` cannot be a subtrait of
   `Linter`, because `Linter` is blanket-implemented *from* it (`expr_linter.rs:115-134`). The
   re-declaration is the only way to require the string. Removal changes what the structure can
   express.
2. The trait doc says "A __stateless__ rule" (`linting/mod.rs:341`) while `lint`'s doc says "We pass
   `self` mutably for caching purposes." I looked for the construction where the mutability carries
   semantic state and could not build it: the only `&mut` uses are `chunk_expr_cache` /
   `sentence_expr_cache` (memoization keyed on a content hash plus a config hash), which preserve
   observational statelessness. "I did not see the difference" would be a finding only if the
   difference were constructible; it is not.

I note but do not charge: `impl Linter for L`'s body is `fn description(&self) -> &str {
self.description() }` with both same-named trait methods in scope — a resolution hazard the author
evidently met, since `all_descriptions` disambiguates with `ExprLinter::description(value)`. That is
a question about what the code does when run, which my `evidence_standard` puts outside my reach.

## U8 — `lint_group/mod.rs` — DRAWBACK, `internal_contradiction`

The three `BTreeMap`s and two LRU caches are *not* the finding. `Box<dyn Linter>` would hold every
`ExprLinter` (the blanket impl guarantees it), so `linters` expressively subsumes both expr maps —
but the split is what lets `chunk_expr_cache` and `sentence_expr_cache` key per unit type and "only
rerun the expr linters when a chunk changes" (`:337-342`). `Chunk` and `Sentence` are distinct
`DocumentIterator` units, so one map cannot hold both without erasing `Unit`. Removal changes what
the structure can express. Load-bearing — the C-C2/C-C4 shape.

The finding is that the unit has two admission paths into one name-keyed namespace, and they
disagree about the same construction — a duplicate rule name:

- `add` / `add_chunk_expr_linter` / `add_sentence_expr_linter` (`:374`, `:392`, `:414`): documented
  as "returning whether the operation was successful. If it returns `false`, it is because a linter
  with that key already existed." On clash they record the name and **do not insert** — the
  incumbent wins.
- `merge_from` (`:434-475`): for each map it does
  `other.linters.iter().find(|(k, _)| self.contains_key(k))`, records at most that one key, then
  runs `self.linters.extend(other.linters)` **unconditionally** — the incomer wins, and every clash
  after the first is neither recorded nor refused.

Same collision, opposite override semantics, and a clash record that is incomplete by construction
(`.find()`, not `.filter()`). The disagreement is not merely stylistic: `merge_from` records the
clash at all, which shows the unit treats a collision as an error there too, and then extends anyway.

The construction is reachable, not hypothetical: `new_curated` (`:541`) calls `merge_from` six times
— `weir_rules`, `phrase_set_corrections`, `proper_noun_capitalization_linters`, `closed_compounds`,
`initialisms`, `be_adjective_confusions` — before roughly six hundred `insert_*` calls. A name
present in two of those six sub-groups is silently overwritten and reported once; the same name
arriving through `insert_expr_rule!` is refused and the incumbent kept. One namespace, two laws.

Corroborating, not charged separately: the clash-append block is copied six times verbatim (`:378`,
`:402`, `:423`, `:442`, `:455`, `:468`), and the two collision-reporting mechanisms fire on the
identical condition one line apart — the `bool` return (never bound by any in-repo caller; the
`insert_*` macros and `Weirpack::to_lint_group` at `weirpack/mod.rs:74-81` all discard it) and
`clashing_linter_names` (read at exactly one site, the `#[test] no_linter_names_clash` at `:1235`).
I stop short of calling that pair redundant: `add` is `pub` on a library crate and
`clashing_linter_names` has no accessor, so the two serve different audiences — the separating
sentence exists, and I owe it to myself to honor it.

---

## Abstentions considered and not taken

No unit required a `jurisdiction` abstention. I was not asked whether any layer is justified by a
committed text (Grounding's seat), and I formed no view on false-positive reports, rule counts as
evidence of bloat, benchmarks, or peer practice — all outside `select`. `blind_to` held: I did not
consult authorship, the issue record, or the reason for the examination, and I ignored the filer's
note about the "principle"/"principal" misspelling in U2, which is prose quality contradicting no
other field.
