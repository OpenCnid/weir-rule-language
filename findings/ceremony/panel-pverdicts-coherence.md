# Seat 2 — Bounded_Entailment_Coherence — reasoning

Entailment only. No empirical weighing: cited content is taken as quoted, harper's and Trellis's
bytes are Grounding's and Corroboration's. Instruments used: each claim's own premises, its declared
scope, the closed label sets it invokes (the SPARK S-vs-R gate; the density chain's tier contract),
and the artifact family the spans sit in.

## Records opened

- `weir-rule-language/findings/01-spark-steering.md` — the actual source of Spans A–D (the evidence
  bundle names `docs/density-chain/DENSITY-CHAIN.md` as "the orientation artifact these spans were
  cut from"; Spans A–D are not in that file, they are in the diagnosis. Recorded, not charged: the
  filing's pointer is imprecise, but every span is verbatim somewhere in the family, and no verdict
  below turns on which file holds it).
- `DENSITY-CHAIN.md` §"Weir" T1–T5 + Uncovered (lines ~300–420), §"What a builder of a composable
  expert system should take" (945–981), §"Honest gaps" (1020–1040) — Span E is the C3 branch's
  `Trellis-relevant observation` slot, verbatim.
- Not opened, deliberately: `step0-filing.md` and `step4-prereg.md` (authorship is withheld and the
  prereg carries per-seat predictions — reading either would breach `blind_to`), and
  `DENSITY-CHAIN.html` (a rendered view where the markdown is ground truth).

## Standing discounts found in the record, which govern strength below

1. `DENSITY-CHAIN.md:1022` — "**Nothing was executed.** Every test count is a count of `#[test]`
   attributes or `test` lines in source, **never a green run**."
2. `DENSITY-CHAIN.md:414` (= `C3-weir-language.md:116`) — "the claim that they pass rests on the
   generated `run_tests_for_weir_rules` existing and on CI, **not on execution here**."
3. `01-spark-steering.md:20-23` — "there is **no live session symptom** here… it is labelled
   speculative where it is."

These are entailment facts for this seat, not evidence facts. Any conclusion written at execution
strength over them does not follow from its own premises, and is capped at `reading-strength`.

## Per claim

**P1 — clean, full.** Span C assigns a label and names its defining predicate in the same breath
("a composable expert system whose expertise is English prose"), and §3's table establishes exactly
that predicate and no more: authoring (`.weir`: `expr main`, `let message/description/kind/becomes`),
composition (`LintGroup`, runtime-extensible), distribution (Weirpacks with a required-validated
manifest), per-user configuration (`default_config.json` + `FlatConfig`). The claim deliberately
drops "personalized" and swaps the expertise domain from "the user's data" to "English prose"
overtly, as the contrast is the point — nothing is smuggled from the ratified target function.
C4's "flat namespace over nested composition" defect narrows how well harper composes; it does not
deny that it composes.

**P2 — clean, bounded.** The label is the S-vs-R gate's closed pair, and "It is already in the
roster" asserts the S limb: capable tool present, ceiling low. Span D as cut supports it only with
"its module docstring **states** the pillar" — a docstring stating a pillar establishes that the
module asserts it, not that it holds it, and on the span alone this is `label_predicate_unmet`. The
continuation two sentences later meets the predicate at reading strength by naming implementation
entities rather than prose: `AnchorMismatchError`, `StaleFileError`, `replace_lines`/`insert_lines`/
`delete_lines`, and 0-based half-open addressing computed by `locate` (`01-spark-steering.md:45-49`).
The under-inclusive cut disadvantages the claimant rather than the reverse, so I read the label
against the record and not against the cut. Bounded because §1 confines it to span mechanics
("Adopting harper-core **for span mechanics**") and P2 conserves that qualifier.

**P3 — clean, full.** The claim is modal and structural — a rule plus its acceptance tests *can* be
one artifact — and co-location in source establishes exactly that: five statement forms including
`test` and `allows` in `weir/parsing/stmt.rs`, `build.rs` scanning the rule directory and generating
the harness (T2). The decomposition leaves the behavioral half ("runs every shipped rule's
assertions") in P4, so nothing in P3 reaches past reading. Full strength survives discount 1 because
discount 1 bites on behavior, and P3 asserts shape.

**P4 — clean, reading-strength.** The count half (64 of 351 carry zero assertions) is a reading
count, stated identically at T4 and in the aggregation. The second half — "and the generated test
still passes" — is written flatly at execution strength, while the very branch it comes from records
in its own `Uncovered` slot that "the claim that they pass rests on the generated
`run_tests_for_weir_rules` existing and on CI, not on execution here," and T4 phrases it as "passes
**vacuously** on an empty rule." The hedge is present at T4 and in the aggregation and absent from
Span E, so the conclusion is not entailed at the strength it is written; per orientation I cap
rather than charge, because the discount is disclosed in the record the claim sits in, not concealed.
Noted and not charged: `DENSITY-CHAIN.md:926` has C3 at 89 of 351 meeting the 15-test floor and C4
at 297 of 351 below it (89 + 297 = 386 > 351) — a live inter-branch inconsistency on the same stated
denominator, but on a different predicate than P4's, so it does not touch this claim.

**P5 — drawback, `scope_creep_past_declared_bound`.** The artifact's own self-check declares the
bound precisely: Trellis "has a registration surface (PR #179 descriptors) **but no single-artifact
authoring unit** that carries a rule and its own tests together, and **no packaging/distribution
unit** for a set of them" (§4). §3's table concedes an answer in four of five rows for Trellis today
— "Rust/Python module per linter-equivalent", "Separate test files", "Composition exists; not
runtime-extensible from data", "Descriptor registration (PR #179)". Span C's restatement drops every
qualifier: "the authoring-surface problem Trellis has not yet reached." Two absences plus three
partial presences do not entail an unreached problem; the narrow premise does not entail the wide
conclusion, and the drop is exactly what makes it uncheckable. This is load-bearing downstream:
Span A's "reference design on the S axis" licence consumes the unqualified form.

**P6 — clean, bounded.** The inference is stated separately from the fact it rests on: the fact is
§1's roster finding, the inference is "that is an R-axis move against a ruled-out R-axis gap," and
deleting the inference leaves the roster fact standing. The span then names its own defeater rather
than suppressing it — "If it is taken anyway it must be justified on a *different* symptom… 'Trellis
wants offline English grammar linting of user prose as a product feature,' which is a real want but
is not the capability gap this run located." That "must" is methodological, conditional, and
separated, so no normative residue is fused into the fact. Bounded because the conclusion holds only
relative to the symptom diagnosed, and the span carries that qualifier through to its last clause.

**P7 — clean, reading-strength.** Span A conjoins two things — reading Weir is cheap, and "the lesson
is portable to Python" — so the forecast is a second conjunct, not a conclusion drawn from
cheapness; there is no missing-premise failure to charge. But it names no receiving-side design
record and no condition that would settle it, and §0 promised the diagnosis would be "labelled
speculative where it is" while this forecast carries no such label, over an artifact that declares
nothing was executed and nothing built. So it cannot stand at full or bounded strength; capped.
The disclosed Span A cut ("Deferred to the user gate…") withholds a paragraph about the adopt/decline
call, which bears on P8's gating rather than on portability, so it does not change this verdict.

**P8 — abstain, jurisdiction.** Mode is `value`: "Trellis *should* copy the co-location, and should
add a registration-time floor." Standing on such a claim moves by user gate; the panel does not
ratify it and this seat will not launder it into a coherence pass. Recorded for the record rather
than charged as `fact_judgment_conflation`: in Span E's source sentence the normative step is fused
— "Trellis should copy that co-location" is made to follow from the Weir reading with no separately
stated premise about Trellis's target function — and the separation exists only because the filing
cut it out and tagged it `value`. Since the filing did separate it, and deleting P8 leaves P3 and P4
standing as facts while deleting them collapses P8, what remains in front of me is a properly
isolated normative premise, which is jurisdiction, not drawback.

## Distribution check

7 clean (1 full-full, 2 bounded, 2 reading-strength capped, plus P1/P3 full), 1 drawback, 1 abstain.
The pool is largely coherent; its single entailment failure is P5, and the two caps at
`reading-strength` are the artifact's own disclosed discounts being honored rather than defects.
