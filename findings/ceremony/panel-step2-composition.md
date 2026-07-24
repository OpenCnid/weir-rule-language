# Step 2 — Panel composition (candidate-blind)

Composed for the pool characterized in `step1-characterization.md`. The candidate set was withheld by
design and no attempt was made to infer it; every seat below is composed for the pool's claim kinds,
its credibility standard, and its authority order.

**Driving question the panel serves:** *does the record support promoting these claims from belief to
fact, and at what strength?*

**Registry policy for this panel.** `Emotional` and `Sensorial`/`Ethical` are not admitted by default.
The question is epistemic — locator resolution, entailment, independence — so no seat draws on
`Emotional`, and no seat draws on `Ethical`. `Sensorial` *is* admitted, twice, and the reason is stated
in each seat's orientation: reading whether a locator resolves and where a quoted span was cut is an
act of textual perception, not of inference, and giving it a `Logical` parameter would let a seat
reason its way to a fidelity verdict it should have had to *look* at.

**Strength.** No schema field carries strength, so each seat's `orientation` fixes a three-step
strength vocabulary — `full | bounded | reading-strength` — and requires the verdict clause to name
one. `reading-strength` is the ceiling for anything the pool declares unexecuted.

---

## Seat 1 — Grounding

```yaml
judge: Locator_Fidelity_Grounding
purpose: >
  Decide whether the bytes a claim cites, read at the stated pin, contain what the claim says they
  contain — and whether the span was cut at a boundary that reports them fairly. Fidelity only.
  Whether the claim is TRUE is never this seat's business: a claim may be faithfully cited and wrong,
  and this seat returns clean on it. A claim may also be true and mis-cited, and this seat returns a
  drawback on it. The seat's product is a distance measurement between a sentence and an openable
  locator, plus a strength ceiling implied by what the cited bytes can bear.
claim_modes: [fact, inference, prediction, belief, experience]
select:
  - Sensorial.Legibility/locator_resolution
  - Sensorial.Granularity/span_boundary_fairness
  - Logical.Correspondence/quoted_referent_match
orientation:
  - >
    Identical procedure across every admitted claim mode. A prediction's citation is checked exactly
    as a code fact's is: does the cited span say the thing attributed to it. The seat does not
    discount a citation because the sentence it supports is a forecast — that discount belongs to
    other seats.
  - >
    Read the locator first, the claim second. If the order inverts, the seat is reconstructing a
    reading rather than checking one.
  - >
    Boundary fairness is in remit and is a first-class drawback, not a footnote. A span cut to end
    immediately before an adjacent qualifier — a condition, an exception, a flag guard, a "when"
    clause — tilts by omission and is a drawback even when every quoted byte is verbatim correct.
    Ask of every span: does the sentence immediately outside each edge change what the span means.
  - >
    The pin is part of the locator. A path-and-line with no pin addresses a moving target; the seat
    reports it as a fidelity defect, not as an absent citation.
  - >
    Sensorial parameters are used here, and only here, because locator resolution and span-edge
    reading are perceptual acts. Recording them as `Logical` would license the seat to infer that a
    span probably says the right thing.
  - >
    Compound claims are decomposed before ruling. A recommendation packages a code fact, an
    inferential step, and a normative judgment; this seat rules on the code-fact component and routes
    the normative component to abstention rather than dragging it into a fidelity verdict.
  - >
    Verdict clause must name a strength: `full` when the cited span alone carries the whole sentence;
    `bounded` when it carries a narrower sentence than the one written; `reading-strength` when the
    span supports the claim only under the pool's declared non-execution boundary.
  - >
    Abstention is typed and is not a soft fail. `jurisdiction` when what remains after decomposition
    is normative or value-mode; `evidence` when no locator was offered at all, or the cited artifact
    is outside the settling authority the pool names.
taxonomy:
  - locator_unresolvable
  - span_truncates_qualifier
  - referent_mismatch
  - overstated_beyond_cited_bytes
  - pin_absent_or_drifted
  - faithful
  - abstain_jurisdiction
  - abstain_evidence
blind_to:
  - whether the claim is true, correct, or good for Trellis
  - the claim's own stated rationale for why the citation supports it
  - who authored the claim, what standing tier it sits at, and whether it has been proposed before
  - other seats' verdicts, and any prior panel record on the same claim
  - the rendered view of any source whose markdown is declared ground truth over it
```

### Grounding anchors — five drawbacks

**G-D1 · `locator_unresolvable`.** A claim names a type and gives a path-and-line inside the pinned
tree. The path resolves; the line holds an unrelated declaration, and the named type is nowhere in
the file. *Calibrates:* resolution failure is a drawback even when the type plainly exists elsewhere
in the tree — the seat checks the locator that was offered, not the one that would have worked.

**G-D2 · `span_truncates_qualifier`.** A claim reports that a policy is stated in the source and
quotes a span that ends one sentence before the adjacent clause conditioning the policy on a flag
that is off by default. Every quoted byte is verbatim. *Calibrates:* the boundary, not the bytes, is
the defect; a fair edge would have included the condition or the claim would have named it.

**G-D3 · `referent_mismatch`.** A claim asserts one construct lowers into another. The cited span
shows both names listed side by side in a closed label set, with no lowering relation expressed
anywhere in the span. *Calibrates:* co-location is not relation; the seat rules on what the bytes
assert, not on what an informed reader would guess they imply.

**G-D4 · `overstated_beyond_cited_bytes`.** A claim states a suite-wide count of assertions. The
cited locator is a single file's header comment declaring an *intended* count for that file.
*Calibrates:* the span supports a narrower sentence than the one written; a quantitative claim
inherits the scope of its locator, and widening it is a fidelity defect, not an inference defect.

**G-D5 · `pin_absent_or_drifted`.** A claim carries a path-and-line but no pin, and the cited line
differs between the pin the pool declares and the moving branch tip. *Calibrates:* the seat reports
this at the same weight as a wrong line — an unpinned locator was never independently checkable, which
is the exact property the pool's credibility standard is built on.

### Grounding anchors — five cleans

**G-C1 · `faithful`, strength `full`.** A claim states a type's name and its defining fields; the
cited span at the pin contains that declaration and those fields, and nothing adjacent to either edge
qualifies it. *Calibrates:* the ordinary clean — locator resolves, referent matches, boundary fair.

**G-C2 · `faithful`, strength `full`.** A claim reports a policy *and* the condition gating it; the
quoted span extends through the gating clause. *Calibrates:* the mirror of G-D2 — an included
qualifier is what a fair boundary looks like, and the seat must be able to recognize it as clean
rather than treating any qualifier's presence as suspicious.

**G-C3 · `faithful`, strength `full`.** A claim assigns an entity the unreachable-in-workspace label
and cites a ledger row; the row carries the locator and states that a callgraph read was the evidence.
*Calibrates:* the seat confirms the row says what the claim says it says, and stops. Whether the
entity really has no caller is another seat's question entirely.

**G-C4 · `faithful`, strength `bounded`.** A recommendation sentence is decomposed; its code-fact
component's locator resolves and the span carries it, while the normative component is routed to
`abstain_jurisdiction`. The seat returns clean on the component in remit. *Calibrates:* partial
jurisdiction produces a bounded clean plus a typed abstention, never a blanket drawback.

**G-C5 · `faithful`, strength `full`.** A claim declares that a named area was not reached and cites
the branch's declared negative-space list; the list contains that area in those terms. *Calibrates:*
a citation to an artifact's own declaration of its gaps is a normal, checkable locator — the seat
does not discount self-disclosure.

### Grounding abstention calibration

- `abstain_jurisdiction` — the sentence remaining after decomposition asserts what Trellis *should*
  do, or is otherwise `value`-mode. No fidelity question survives; the seat does not rule.
- `abstain_evidence` — no locator was offered, or the only locator points outside the settling
  authority the pool names for that claim kind (e.g. a portability forecast citing source bytes,
  which the pool says cannot settle it).

---

## Seat 2 — Coherence

```yaml
judge: Bounded_Entailment_Coherence
purpose: >
  Decide whether the claim holds together — internally, and against the live record it must sit
  beside. Entailment only. The seat asks whether the claim's conclusion follows from its stated
  premises and its declared scope, whether its parts contradict each other, and whether its label
  assignments meet their own defining predicates. It never asks whether the world agrees.
claim_modes: [fact, inference, prediction, belief, experience]
select:
  - Logical.Entailment/scope_conservation
  - Logical.Consistency/non_contradiction
  - Logical.Classification/label_predicate_fit
orientation:
  - >
    No empirical weighing. The seat may not go and look at whether a thing is so; it takes cited
    content as quoted (Grounding owns that) and independent evidence as out of reach (Corroboration
    owns that). Its only instruments are the claim's own premises, its declared scope, the closed
    label sets it uses, and the standing records already live.
  - >
    Scope conservation is the seat's sharpest test in this pool, because the pool's bounded claims
    are bounded by declaration rather than by grammar. A claim defined as workspace-internal that is
    later restated without the qualifier has failed entailment: the wider sentence is not entailed by
    the narrower one, and the drop is invisible unless someone tracks it across restatements.
  - >
    Label predicate fit: a status label from a closed set is an assertion that the label's defining
    predicate was established. The seat checks the claim's own reasoning against that predicate. A
    label asserting that nothing enforces a policy is unmet if the reasoning establishes only that the
    policy exists.
  - >
    Density-tier discipline: deeper rungs add entities and never correct shallower ones. A claim that
    depends on a deeper rung contradicting a shallower one is internally incoherent regardless of
    which rung is right.
  - >
    Structural discounts are entailment facts here, not evidence facts. If the pool declares nothing
    was executed, then a defect claim stated at execution strength does not follow from its own
    premises. Cap it at `reading-strength` or record the overreach.
  - >
    Compound recommendations must state the normative premise separately. If the normative conclusion
    is made to follow from the source fact alone, the claim has a missing premise and fails
    entailment — this is a drawback the seat *can* return, distinct from abstaining on the normative
    content itself.
  - >
    Against the live record: where a ratified or adopted record already fixes an evidence class or a
    standing rule, a claim that presupposes otherwise is incoherent against the record even if
    nothing empirical is weighed. Authority order is read, never re-litigated.
  - >
    Abstention is typed. `jurisdiction` for `value`-mode claims and for the isolated normative
    residue of a decomposed recommendation — user-gated, never panel-ratified. `evidence` when the
    live record needed to test entailment is not available to the seat.
taxonomy:
  - internal_contradiction
  - scope_creep_past_declared_bound
  - label_predicate_unmet
  - tier_inversion
  - fact_judgment_conflation
  - entails_cleanly
  - abstain_jurisdiction
  - abstain_evidence
blind_to:
  - whether independent evidence supports or contradicts the claim
  - byte-level verification of any citation; cited spans are taken as quoted
  - the author, the claim's popularity, and any downstream plan that depends on it
  - other seats' verdicts
  - rendered views where markdown is declared ground truth
```

### Coherence anchors — five drawbacks

**C-D1 · `internal_contradiction`.** A claim labels an entity as having no caller outside the test
suite, while the same claim's stated reasoning cites a non-test call site as the evidence for the
entity's shape. *Calibrates:* the seat needs no external check to fail this — the premises collide
inside the sentence.

**C-D2 · `scope_creep_past_declared_bound`.** Reachability is defined workspace-internal. The claim
restates it as an unqualified assertion that nothing anywhere calls the entity, and the downstream
recommendation depends on the unqualified form. *Calibrates:* the bounded premise does not entail the
unbounded conclusion; a claim that quietly widens has lost the property that made it checkable.

**C-D3 · `label_predicate_unmet`.** An entity receives the label meaning *a stated policy nothing
mechanically checks*, but the claim's reasoning establishes only that the policy is stated, never
that no mechanism checks it. *Calibrates:* the seat tests the label against its own defining
predicate, not against plausibility.

**C-D4 · `tier_inversion`.** A claim leans on a deeper-rung entity that *corrects* a shallower rung's
statement, and simultaneously leans on that shallower statement. *Calibrates:* the density
contract's add-never-correct rule makes this incoherent independent of which rung is factually right.

**C-D5 · `fact_judgment_conflation`.** A recommendation reads as one sentence in which "Trellis
should adopt this shape" is presented as following from a structural reading of the source, with no
separately stated premise about Trellis's own target function. *Calibrates:* the missing normative
premise is an entailment gap the seat returns as a drawback — distinct from abstaining, which applies
only to a normative residue that *is* properly stated and separated.

### Coherence anchors — five cleans

**C-C1 · `entails_cleanly`, strength `reading-strength`.** A defect claim states explicitly that it
is inferred from reading with no counterexample executed, and its conclusion is written at that
strength throughout. *Calibrates:* honoring a declared structural discount is a clean, and the
resulting reduced strength is not a drawback.

**C-C2 · `entails_cleanly`, strength `bounded`.** A reachability claim carries its workspace
qualifier in the ledger row, in the takeaway, and in the recommendation that consumes it.
*Calibrates:* the mirror of C-D2 — scope survives restatement.

**C-C3 · `entails_cleanly`, strength `bounded`.** A portability forecast is stated as conditional on
a receiving-side design record, and nothing later in the claim treats the forecast as settled by the
source. *Calibrates:* a prediction that names what could settle it, and does not claim that thing has
happened, is coherent at bounded strength.

**C-C4 · `entails_cleanly`, strength `full`.** A status label is assigned, its defining predicate is
named in the same breath, and the evidence line establishes exactly that predicate — no more, no
less. *Calibrates:* the mirror of C-D3.

**C-C5 · `entails_cleanly`, strength `full`.** A claim states its inferential step separately from
the fact it rests on, such that deleting the inference leaves a standing fact and deleting the fact
collapses the inference. *Calibrates:* the pool's layered credibility standard made structural — the
seat rewards separation even when the inference is arguable, because arguable-and-separated is
coherent while fused-and-obvious is not.

### Coherence abstention calibration

- `abstain_jurisdiction` — the claim is `value`-mode, or what remains is a properly separated
  normative premise about what Trellis should want. Standing on such a claim moves by user gate; the
  panel does not ratify it, and does not launder it into a coherence pass.
- `abstain_evidence` — the live standing record the claim must cohere against is not in the seat's
  reach, so no entailment test can be run without empirical weighing the seat is barred from.

---

## Seat 3 — Corroboration

```yaml
judge: Chain_Disjoint_Corroboration
purpose: >
  Decide whether evidence INDEPENDENT of the claim's own citation chain supports it, and how far.
  The seat's base is the record minus that chain. Anti-circularity is the entire point of the seat:
  a claim that is only ever supported by restatements of itself, at any density, has zero
  corroboration no matter how many times it is restated.
claim_modes: [fact, inference, prediction, belief]
select:
  - Logical.Independence/chain_disjointness
  - Logical.Convergence/cross_channel_agreement
  - Sensorial.Coverage/negative_space_sampling
orientation:
  - >
    Construct the base first: take the record, remove the claim's citation chain and every artifact
    that derives its warrant from that chain, and rule only on what remains. If the base is empty,
    that is an evidence abstention — never a quiet pass.
  - >
    The seat does not read the claim's stated rationale. It reads the claim's assertion and then goes
    looking. Reading the rationale would import the chain the seat exists to exclude.
  - >
    Same-warrant relocation is not independence. Another section of the same artifact summarizing the
    same reading is the same chain at a different address; agreement between them is repetition.
  - >
    Two channels corroborate only when they could have disagreed. Name, for each supporting channel,
    what it would have looked like had the claim been false.
  - >
    Silence is not credit. Where an artifact is required to declare what it did not reach, an
    unmentioned area is a declared-or-undeclared gap, not evidence of coverage. The seat checks the
    negative-space declaration before treating absence as support — this is why a `Sensorial` coverage
    parameter sits here: it is a looking act over declared gaps, not an inference.
  - >
    Bounded corroboration is a real, common, clean outcome: the independent channel supports a
    narrower sentence than the one claimed. Return clean at `bounded` and name the narrower sentence,
    rather than failing the claim or passing the wide version.
  - >
    Structural discounts propagate. If nothing was executed anywhere in the base, then no channel in
    the base can lift a behavioral claim above `reading-strength`, however many channels agree.
  - >
    Authority order governs which channel wins when channels disagree: the pinned source settles
    source claims outright, and a ratified or adopted receiving-side record settles what may be built
    on which evidence class. A disagreement resolved by that order is a finding, not a tie.
  - >
    Abstention is typed. `jurisdiction` for `value`-mode claims — no amount of independent evidence
    can ratify what only a user gate can. `evidence` when the base is empty or reaches only the
    claim's own chain.
taxonomy:
  - circular_restatement
  - single_channel_dependency
  - independent_channel_contradicts
  - silence_taken_as_support
  - chain_leakage
  - independently_corroborated
  - bounded_corroboration
  - abstain_jurisdiction
  - abstain_evidence
blind_to:
  - the claim's own stated rationale, and every artifact whose warrant descends from it
  - the artifact's summary sentences about its own reliability, thoroughness, or method quality
  - who authored the claim and what tier it currently sits at
  - other seats' verdicts, including whether Grounding found the citation faithful
  - rendered views where markdown is declared ground truth
```

### Corroboration anchors — five drawbacks

**R-D1 · `circular_restatement`.** The only support available for a claimed defect is the same
reading, restated at a deeper density rung with more words. Base minus chain is empty of anything
bearing on it. *Calibrates:* depth is not independence; the seat returns a drawback here rather than
an evidence abstention, because a chain that fills the space *pretending* to corroborate is worse
than no channel at all.

**R-D2 · `single_channel_dependency`.** An adoption-rate claim rests entirely on one sampling of the
history record, and that record is disclosed as unevenly sampled. No second channel exists that could
have disagreed. *Calibrates:* one channel plus a disclosed skew supports the claim only as far as the
skew allows, which is not as far as the claim reaches.

**R-D3 · `independent_channel_contradicts`.** An entity is claimed to have no non-test caller; a
direct read of the pinned tree, undertaken without the claim's rationale, surfaces a non-test call
site. *Calibrates:* the settling authority wins outright per the pool's authority order — this is a
resolved contradiction, not a tie to be split.

**R-D4 · `silence_taken_as_support`.** A claim treats the absence of any contrary entity in the
artifact as evidence in its favor, while the relevant branch's declared negative-space list states
that area was never reached. *Calibrates:* the seat must look at the declaration before crediting
absence; unlooked-at silence is the pool's named failure mode.

**R-D5 · `chain_leakage`.** The corroborating source offered is a different branch of the same
artifact summarizing the same reading of the same locator. Presented as a second channel; it is the
first channel relocated. *Calibrates:* independence is by warrant, not by address.

### Corroboration anchors — five cleans

**R-C1 · `independently_corroborated`, strength `full`.** The pinned source is opened directly,
without the claim's rationale in view, and the structural relation the claim asserts is present at the
settling authority. *Calibrates:* the strongest available clean in this pool — one channel, but the
channel that settles the question by declared authority.

**R-C2 · `bounded_corroboration`, strength `bounded`.** The independent channel establishes that a
construct exists and carries no exercising test, but not the wider defect the claim asserts. The seat
returns clean on the narrower sentence and names it. *Calibrates:* narrowing is a clean verdict with
a stated ceiling, not a soft fail.

**R-C3 · `independently_corroborated`, strength `full`.** Two channels that share no warrant — a
direct source read and a history-record read — agree on where a construct was introduced, and each
would have looked different had the claim been false. *Calibrates:* convergence with a stated
falsification shape is what real corroboration looks like.

**R-C4 · `independently_corroborated`, strength `bounded`.** The branch's declared negative-space
list is read and does not contain the area the claim covers, so the coverage the claim assumes is
declared coverage rather than unexamined silence. *Calibrates:* the mirror of R-D4 — checking the
declaration converts a non-fact into a bounded, usable one.

**R-C5 · `independently_corroborated`, strength `bounded`.** A receiving-side ratified or adopted
record independently fixes the evidence class the claim presupposes, corroborating the claim's
premise without any reference to the claim's own rationale. *Calibrates:* a governing record can
corroborate a presupposition even when it says nothing about the claim's content.

### Corroboration abstention calibration

- `abstain_jurisdiction` — the claim is `value`-mode. Independent evidence cannot promote what is
  user-gated by construction; the seat records the type and declines.
- `abstain_evidence` — after removing the citation chain and everything warranted by it, the base
  contains nothing that bears on the claim. Recorded explicitly so an empty base never reads as a
  weak pass.

---

## Panel-level properties

### Disjointness

The three `select` sets are pairwise disjoint at the qualified-parameter level — no
`registry.parameter/aspect` string appears in two seats, and no *parameter* is shared even where a
registry is. `Sensorial` appears in Grounding (`Legibility`, `Granularity`) and Corroboration
(`Coverage`); `Logical` appears in all three (`Correspondence` / `Entailment`+`Consistency`+
`Classification` / `Independence`+`Convergence`). Registry reuse with disjoint parameters requires no
gluing rule; none is declared, and none is relied on.

### Every seat can fail, and can abstain

Each `taxonomy` carries at least four failing classes, at least one clean class, and both typed
abstention classes. No seat's clean class can be reached by default: Grounding requires a resolving
locator *and* a fair boundary, Coherence requires premises that carry the conclusion at the stated
strength, Corroboration requires a non-empty base disjoint from the chain. A seat that cannot fail was
not composed here.

### Anchor discrimination

| seat | clean anchors | drawback anchors | all-one-way? |
|---|---|---|---|
| Grounding | 5 (G-C1…G-C5) | 5 (G-D1…G-D5) | no |
| Coherence | 5 (C-C1…C-C5) | 5 (C-D1…C-D5) | no |
| Corroboration | 5 (R-C1…R-C5) | 5 (R-D1…R-D5) | no |

Anchors calibrate; none is a verdict on any claim in the pool, and none names a file, commit, PR
number, or count from any real repository. Six of the ten pairs per seat are deliberate mirrors (a
drawback and its clean twin) so the seat is calibrated on the *boundary* between them rather than on
two unrelated extremes. Abstention exemplars are given per seat outside the ten-item sets, so no seat
is anchored toward abstaining.

### Value-mode handling

`value` is absent from every seat's `claim_modes`, and each seat's orientation additionally requires
compound claims — recommendations, which package a code fact, an inferential step, and a normative
judgment — to be decomposed *before* ruling, so that the normative residue routes to
`abstain_jurisdiction` with its type recorded rather than being absorbed into a fact-shaped verdict.
Grounding abstains on the residue and may still return a bounded clean on the code-fact component;
Coherence abstains on the residue but *does* return `fact_judgment_conflation` when the normative
conclusion is made to follow from the source fact with no separately stated premise; Corroboration
abstains outright, since independent evidence cannot promote what only a user gate can ratify.

## Uncovered

- **No exemplar claim text.** The characterization gives claim *kinds* and a credibility standard but
  no specimen sentence, so the anchors are improvised from the pool's vocabulary rather than
  calibrated against any observed phrasing. Anchor sharpness would improve with three or four
  redacted specimens spanning the modes.
- **The strength vocabulary is panel-local.** The schema has no strength field, so `full | bounded |
  reading-strength` lives in `orientation` prose. If the receiving standing ladder has its own
  strength names, these will need translating at the gate.
- **Corroboration's base is asserted, not enumerated.** "The record minus the claim's chain" is
  well-defined only if the seat can see the record; the characterization names the evidence channels
  but not what a seat is actually granted access to at run time. An empty-base abstention may
  therefore report a tooling limit as an evidence limit.
- **No licensing or provenance seat.** The characterization names an adoption-bounds register with
  entries governing licensing and the standing of un-promoted sources. Those are plausibly `Ethical`
  questions about a third-party engine, and this panel deliberately does not take them: they are
  admissibility conditions on a build, decided at the user gate, not belief-to-fact promotions. If
  the gate expects the panel to have screened them, that expectation is unmet by design.
- **Cross-seat compounding is unspecified.** Three bounded cleans and one reading-strength ceiling do
  not obviously compose into a promotion strength. The aggregation rule belongs to the audit seat or
  the gate, and nothing here should be read as proposing one.
