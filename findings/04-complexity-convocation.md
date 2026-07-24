# Complexity Convocation — harper's four-rung abstraction ladder

**Run:** 2026-07-23/24 · **Skill:** `complexity-convocation` · **Driving question:** *is this complexity
warranted, and if not, what specifically should change?*

Six sub-agents: one candidate-blind characterizer, one candidate-blind composer, three judges in
isolated clean contexts, one judges-judge over real run telemetry. **No judge was reused from any
prior ceremony**; every name, selection, taxonomy, and anchor below was composed for this artifact and
is dead now (rule 4 — there is no default cast).

---

## Scope, stated before the verdicts

Two facts change what a disposition can mean here, both filed at Stage 0 rather than discovered later:

1. **The artifact is not the user's.** Nobody in this house authored harper, so the
   self-invested-claimant case does not obtain. Authorship was still masked downstream — for the
   opposite reason: to stop a 12,312-star reputation from doing the judging.
2. **No cut is executable.** We cannot simplify someone else's repository. So **`cut` reads as "do not
   copy this rung"** and **`keep` reads as "this earned its place; the shape is worth copying."**

---

## Verdict per unit

| unit | J1 grounding<br>*The Rescued Sentence* | J2 coherence<br>*The Load-Bearing Layer* | J3 corroboration<br>*The Unauthored Witness* | disposition |
|---|---|---|---|---|
| **U1** `Pattern` — `patterns/mod.rs:42` | clean | **drawback**<br>`tier_duplication` | clean | **simplify** |
| **U2** `Step` — `expr/step.rs:3` | clean | clean | clean | **keep** |
| **U3** `Expr` — `expr/mod.rs:68` | **drawback**<br>`phantom_variant_arm` | clean | clean | **keep, typed fork** |
| **U4** Weir AST — `weir/ast.rs:84` | clean | clean | clean | **keep** |
| **U5** `optimize` — `weir/optimize.rs:3` | clean | **drawback**<br>`internal_contradiction` | clean | **simplify** |
| **U6** manifest guard — `weirpack/manifest.rs:75` | **drawback**<br>`orphaned_guard` | clean | **drawback**<br>`unexercised_in_the_wild` | **simplify — strongest signal** |
| **U7** `Linter` — `linting/mod.rs:346` | clean | clean | clean | **keep** |
| **U8** `LintGroup` — `lint_group/mod.rs` | clean | **drawback**<br>`internal_contradiction` | clean | **simplify** |

Composed **by the gates, never by majority**. Cross-role disagreement is a typed record: a drawback
feeds the cut case, a clean feeds the keep case, and both stand.

---

## Recommendations — every one is yours to gate

- **U6 → simplify. The strongest result in the run.** Two seats that cannot see each other, blind in
  *different* directions, independently found the same thing. Grounding: the guard's only observable
  effect is an error that nothing committed makes fire — *"passes identically with `validate_required`
  deleted"*, because the one test sets all four fields. Corroboration: no `.weirpack` artifact exists
  anywhere in the tree; every real consumer reads rules and dictionary and never touches
  author/version/description/license; the desktop pack list is hardcoded mock data (`settings-data.ts:299`,
  ids `pack-001`…); and the only external signal is open issue #3652 — *"Is there any registry of weir
  packs I could find?"* — meaning **the distribution channel this metadata exists to feed does not
  exist yet.** Coherence dissented and its dissent is recorded, not averaged away: the guard is
  well-formed and load-bearing *if* a manifest can be built incomplete, which `set_field` allows.
  **The fix is one fixture, not a deletion:** ship a `.weirpack` that makes the guard fire.

- **U1 → simplify.** Coherence went looking for the construction that separates `Pattern` from `Step`
  and reported it could not write one: all six implementors are verbatim `Step`s with the slice
  inlined, and the sole distinct-type consumer `Invert` works identically over `Box<dyn Step>` while
  duplicating an idiom `but_not` and Weir's `Not` already use. `PatternExt`/`DocPattern` have zero
  non-test consumers. **This is the rung that did not earn its continued existence** — note that the
  other two seats cleared it, because it *is* grounded and it *is* exercised. It is redundant, not
  broken.

- **U5 → simplify, with a reachable counterexample.** The doc says *"Returns whether an edit was
  made,"* but the `Arr` UPOS-collapse branch (`optimize.rs:41-48`) mutates the AST without setting
  `edit`, while its sibling arm four lines above does. Since the value drives two fixed-point loops,
  `false` terminates optimization early. Coherence supplied the separating input: `[[NOUN, VERB], [ADJ,
  ADV]]` collapses both inner arrays in pass 1, returns `false`, and exits — leaving work undone that a
  second pass would finish. The existing test covers only the flat case.

- **U8 → simplify.** Not the three maps — those are justified, since `Chunk` and `Sentence` are
  distinct iteration units. The finding is **two admission paths that disagree about the same
  collision**: `add`/`add_*_expr_linter` record a clash and refuse to insert (incumbent wins), while
  `merge_from` records at most the first clashing key and then `extend`s unconditionally (incomer
  wins). `new_curated` calls `merge_from` six times before ~600 `insert_*` calls, so a name shared by
  two sub-groups is silently overwritten where the identical name via macro would be refused. This is
  the same defect harper tracks as #3241 and #3134, reached independently.

- **U3 → keep, and record the fork.** Grounding charged `phantom_variant_arm`: the negative-step
  branch is reachable from no committed byte — every `fn step` in the tree returns a non-negative.
  Coherence cleared it: that branch is *the sole realization of `Step`'s backward reach, duplicated
  nowhere.* **Both are right, and they are not in the same jurisdiction** — one asks *is it exercised*,
  the other *is it redundant*. Composed, it is **capability-in-waiting**: dead today, non-redundant by
  design, and harper's own open PR #2934 (`run_rev`/`step_rev`) would light it up. Grounding named its
  own reopener: *"One committed `Step` returning a negative reopens this."*

- **U2, U4, U7 → keep, unanimous.** These are the shapes worth copying. `Expr`-returns-a-`Span` is what
  lets one traversal serve 279 rule files. The Weir AST is *"a lowering, not a rung"* — coherence
  explicitly tested and rejected the "fourth match-contract layer" charge. `Linter`'s two-method
  surface closes the loop from rule to user: `description()` reaches the public docs page and
  `organized_lints` reaches the LSP diagnostic `code`, so a writer who receives a lint can find the
  switch that turns it off.

---

## What the corroboration seat found that no other channel could

Its whole point is anti-circularity — it is blind to the artifact's own rationale comments. It went
and found **evidence nobody wrote as evidence**:

- Whole-document snapshots over *Alice's Adventures in Wonderland* (3,709 snapshot lines), *The Great
  Gatsby* (8,069), and *The Constitution of the United States* (1,873). Nobody wrote those as tests
  for any unit here.
- 20 `issue_NNNN.md` + 2 `pr_NNN.md` regression fixtures, joining a fixture back to the report that
  motivated it.
- `lint_descriptions_are_clean` lints all 820 rule descriptions with the full curated group — prose
  written as documentation, dogfooded as input.
- `just dogfood` runs the checker over the repository's own source comments.
- **9 issues carry the `false-positive` label across the entire repository history, against 811
  default-enabled rules.** In a domain whose own local currency is the false positive, that is the
  strongest single warrant in the run.

---

## Disclosed abstentions and designed silences

- **No seat abstained on any unit.** All 24 cells returned a substantive verdict. That is unusual and
  is itself worth flagging: it means no unit fell into a composed blind spot, so no
  `warrant-distributed` disposition was needed.
- **Cost was judged structurally, never measured.** The composer disclosed this at composition time:
  the characterization contains no runtime numbers, so corroboration's `unmeasured_standing_cost`
  class had to be judged from structural position rather than from a benchmark. Where it cleared cost
  (U5, U8) it cited the `PARSE_CACHE` and the committed benches — position, not measurement.
- **Nothing was executed.** Every finding here is derived from reading. The U5 counterexample
  `[[NOUN, VERB], [ADJ, ADV]]` is a *constructed* input, never run.

---

## Calibration against the pre-registration

Filed at `2026-07-24T01:26:41Z`, before composition, never shown to any judge.

| Unit | I forecast | Panel returned | |
|---|---|---|---|
| U1 | coherence drawback | **coherence drawback** | ✅ hit |
| U3 | clean ×3, *high confidence* | grounding **drawback** | ❌ **missed** |
| U5 | grounding + corroboration drawbacks | **coherence** drawback; other two clean | ❌ missed — right unit, wrong seats |
| U6 | clean / clean / abstain | **two drawbacks** | ❌ missed |
| U8 | coherence drawback (`god-object`) | coherence drawback (`internal_contradiction`) | ⚠️ right seat, **wrong reason** |
| U2, U4, U7 | clean | clean | ✅ hit |

**I was wrong more often than right, and wrong in the direction that matters.** My U8 forecast said I
expected a god-object finding *"on size alone (1,251 lines)"* and expected it to be **wrong** on
inspection. The panel did not take the bait: it explicitly cleared the three-map structure and found a
subtler, real defect instead. My U3 "high confidence" clean was the largest miss.

My stated falsifier — *"if all three seats return `clean` on all eight units, report a panel
failure"* — did not trigger. Five drawbacks across three seats and six units.

---

## Standing

Every **simplify** above is a `−1` doubt, and by the corrosion bound each cites **facts in harper's
own bytes only** — never another critique, never this house's preferences. None of it moves any
standing. The panel reports; **the user gates**, in both directions. This skill deleted and rewrote
nothing.
