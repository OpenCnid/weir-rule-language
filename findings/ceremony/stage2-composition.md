# Stage 2 — Composed cover (candidate-blind)

Composed from `stage1-characterization.md` alone. The unit under examination is unknown to me and I
made no attempt to infer it; every anchor below is improvised from the domain's vocabulary and names
no file in the subject repository.

Driving question, fixed: **is this complexity warranted, and if not, what specifically should change?**

Registry access: the question is epistemic, so the **Emotional** and **Ethical** planes stay closed.
The domain's talk of "interrupting a writer mid-thought" and "training them to distrust the checker"
is a live temptation toward `Emotional.trust`, but in this domain that construct is *already
instrumented* — false-positive labels, per-lint-ID tallies, challenge lint IDs — so it enters
Corroboration as an external evidence channel under `Logical.causal_reasoning`, not as an affective
parameter a judge weighs by taste. Selections draw from **Logical** and **Sensorial** only.

**Disjointness.** Pairwise disjoint at the *parameter* level, not merely the aspect level, so no
gluing rule is required:

| seat | Logical parameters | Sensorial parameters |
|---|---|---|
| grounding | `falsification` | `observation_quality`, `signal_fidelity` |
| coherence | `consistency`, `deduction`, `counterfactuals`, `abduction` | — |
| corroboration | `induction`, `causal_reasoning` | `usability`, `spatial_and_temporal_coherence` |

No parameter appears in two seats. Cross-seat disagreement is therefore data, and both verdicts stand.

---

## Seat 1 — Grounding

```yaml
judge: The Rescued Sentence
  purpose: >
    For each layer of the unit, does the artifact itself contain a text — wherever it sits — whose
    committed behavior differs depending on whether that layer exists?
  claim_modes: [fact, inference]
  select:
    - Logical.falsification/absence-discriminating-text     # would deleting this layer change a committed byte
    - Sensorial.observation_quality/negative-surface-reach   # do the silence obligations actually exercise the guard
    - Sensorial.signal_fidelity/trace-lands-on-live-bytes    # the cited text still reaches the structure it justifies
  orientation:
    evidence_standard: >
      A committed text in the artifact — a test input, an `allows` line, a whole-document snapshot, a
      dialect-pinned fixture, an issue-or-PR-numbered regression file, a registration entry — that a
      reader can point to and say: without this layer, this byte reads differently. Distance is
      irrelevant; a justification in another file, another crate, or the snapshot tree is still the
      unit's, and I go find it before I call anything untraced. Prose that explains the layer is not
      evidence of a need; it is a claim about one.
    uncertainty_posture: >
      Doubt never rounds up to warrant. If I can construct no committed input that discriminates
      presence from absence, that is `undistinguished_structure`, not a clean pending discovery.
      Symmetrically, doubt never rounds down: if I have not searched the snapshot tree, the Weir
      corpus, and the regression corpus, I have not searched.
    temporal_horizon: >
      The artifact as committed now. A layer justified by a text that once existed and no longer does
      is untraced today, however sound its history — history is Coherence's seat, not mine.
    stakeholder_scope: >
      The artifact's own bytes. Not users, not maintainers' intentions, not the wider ecosystem.
    reversibility: >
      A drawback is reopened by exhibiting the discriminating text I missed — one address is enough,
      and I am expected to be wrong that way. A clean is reopened by showing the text I trusted does
      not in fact reach the layer.
    contradiction_sensitivity: >
      If two committed texts require opposite behavior of the same layer, I report the fidelity fact
      and do not adjudicate which is right; that is Coherence's business.
    abstention_boundary: >
      `jurisdiction` — whenever the question turns on whether a lighter mechanism, a different
      expression, or no rule at all would have served; on elegance, cost, or taste; or on a claim in
      `value`, `belief`, or `experience` mode. `evidence` — whenever the artifact's justifying
      channel for this unit is unreadable to me (a trained model file, a generated snapshot I cannot
      regenerate, a byte outside my allowlist).
  taxonomy:
    undistinguished_structure -> Logical.falsification/absence-discriminating-text
    orphaned_guard            -> Sensorial.observation_quality/negative-surface-reach
    phantom_variant_arm       -> Sensorial.observation_quality/negative-surface-reach
    stale_trace               -> Sensorial.signal_fidelity/trace-lands-on-live-bytes
    unregistered_surface      -> Sensorial.signal_fidelity/trace-lands-on-live-bytes
  blind_to: >
    Every alternative design, including simpler ones — I am forbidden to ask whether a declarative
    tier, a shorter expression, or a different combinator could have done this; whether the rule
    should exist at all; runtime cost, latency, and footprint; the external issue record, user
    reports, production tallies, and peer projects; the opinions of other seats; authorship of any
    kind; and stylistic quality of code or messages. I also do not judge redundancy against sibling
    units — a layer traced twice is still traced.
```

### Anchors — Grounding (5 drawback, 5 clean)

**G-D1 — `undistinguished_structure`.** An eggcorn detector carries a three-token lookbehind that
excludes a preceding modal verb. Its own test block holds six positive catch cases and one negative;
none of the seven places a modal anywhere near the match window, and no snapshot, Weir `allows` line,
or numbered regression fixture in the artifact contains one either. Deleting the lookbehind changes
no committed byte. *Expected: drawback.*

**G-D2 — `orphaned_guard`.** A Weir rule declares four `allows` sentences. In all four the target
phrase is absent entirely, so even the naive pattern would stay silent on them. The negative surface
is present in form and reaches nothing: the exclusion steps it nominally protects are unexercised.
*Expected: drawback.*

**G-D3 — `phantom_variant_arm`.** A redundancy rule fans into British and Indian dialect arms with
distinct messages. Every fixture that reaches the rule is pinned American, and no dialect-pinned
document in the artifact exercises either arm. The fan-out's need is asserted, never exhibited.
*Expected: drawback.*

**G-D4 — `stale_trace`.** A capitalization rule keeps a case-matching path for all-caps input. The
numbered regression fixture that motivated it was rewritten to lowercase prose during an unrelated
snapshot regeneration; the fixture is still committed, still passes, and no longer enters the
all-caps path. The trace exists but no longer lands on the layer. *Expected: drawback.*

**G-D5 — `unregistered_surface`.** A hand-written linter builds conditional messages and a
priority-carrying lint, presupposing a switchable, user-visible rule — but the artifact carries no
short stable name for it, no settings-menu description, and no entry in the curated default
configuration. The user-facing unit its structure is built around has no bytes. *Expected: drawback.*

**G-C1 — clean, distant justification.** A malapropism detector bounds edit distance at 1. The two
sentences that make the bound load-bearing sit nowhere near the rule — they are lines inside a
committed whole-document literary snapshot whose diff flips if the bound widens. A justification a
scroll (or a directory) away is still the unit's, and I found it. *Expected: clean.*

**G-C2 — clean, exercised exclusion.** An expression carries a negative step suppressing the match
when the preceding token is a proper noun. Three committed negative assertions place exactly that
proper noun in exactly that position, one of them lifted from an issue-numbered regression file.
Remove the step and three committed silences become lints. *Expected: clean.*

**G-C3 — clean, pinned variants.** A boundary-error rule fans into Canadian and American arms and
ships two dialect-pinned fixture documents, each committing full output under its own dialect flag.
Each arm has a text that fails without it. *Expected: clean.*

**G-C4 — clean, arbitration traced.** A rule sets its priority below the default. A committed
whole-document snapshot contains a sentence where two overlapping lints collide and the intended one
survives — the ordering the field buys is visible as bytes, not asserted in prose. *Expected: clean.*

**G-C5 — clean, iteration-unit traced.** A rule declares sentence iteration rather than chunk. A
committed test input places a comma between the trigger token and the context token the expression
requires; narrowed to chunk, the rule goes silent on that committed input. *Expected: clean.*

---

## Seat 2 — Coherence

```yaml
judge: The Load-Bearing Layer
  purpose: >
    Taking the unit's internals and their accretion history as given, does every layer carry load
    that no other layer already carries, and do the layers agree with each other?
  claim_modes: [fact, inference]
  select:
    - Logical.consistency/no-two-layers-one-job      # duplication within and across mechanism tiers
    - Logical.deduction/every-declaration-consumed   # each intermediate feeds something downstream
    - Logical.counterfactuals/tier-collapse          # behavior already entailed by a lighter tier present here
    - Logical.abduction/accretion-subsumption        # a later guard whose condition swallows an earlier one
  orientation:
    evidence_standard: >
      Entailment between parts of the unit and the artifact's own live record — the mechanism tiers
      available (a phrase-corrections tuple, a many-to-many phrase set, a proper-noun entry, a Weir
      file, a hand-written impl), the declarations the unit makes, the fields it sets, the guards it
      accumulated. A layer is load-bearing when its removal changes what the rest of the structure
      can express, not merely how it reads. I reason about the structure; I do not run it.
    uncertainty_posture: >
      A layer whose load I cannot locate is a finding, but only after I have looked for the case that
      distinguishes it — the domain's exclusion logic is routinely subtle, and "I did not see the
      difference" is not "there is none." Where the distinguishing case is *constructible in English*,
      I owe myself the sentence before I call redundancy.
    temporal_horizon: >
      The unit as it stands, read against how it got here. Accretion is legitimate; accretion whose
      earlier terms a later term has swallowed is not.
    stakeholder_scope: >
      The unit and its siblings inside the artifact's structure. No users, no downstream consumers.
    reversibility: >
      A redundancy finding is reopened by one construction the two layers treat differently. A clean
      is reopened by showing the divergence I relied on is unreachable — that no admissible token
      sequence separates the layers.
    contradiction_sensitivity: >
      High and terminal. A unit whose message, taxonomy assignment, and variant conditions disagree
      about the same construction is a drawback regardless of how well any single field is grounded.
    abstention_boundary: >
      `jurisdiction` — whenever the question requires evidence outside the structure: real usage,
      reports, measured cost, peer practice, or whether a committed text exists that justifies a
      layer at all (Grounding's seat). Also on `value`, `belief`, `experience`, and `prediction`
      modes. `evidence` — whenever the unit's history or a tier it duplicates is not legible to me,
      or the deciding structure lives in a trained model whose contents I cannot read.
  taxonomy:
    tier_duplication      -> Logical.consistency/no-two-layers-one-job
    subsumed_alternative  -> Logical.consistency/no-two-layers-one-job
    dead_layer            -> Logical.deduction/every-declaration-consumed
    tier_overshoot        -> Logical.counterfactuals/tier-collapse
    accretion_subsumption -> Logical.abduction/accretion-subsumption
    internal_contradiction -> Logical.consistency/no-two-layers-one-job
  blind_to: >
    All evidence external to the artifact's structure: the issue record, false-positive and
    false-negative reports, production tallies, challenge lint IDs, dogfood output, benchmarks,
    fuzzing, peer projects, and any measured behavior. Also blind to whether any layer is *justified*
    by a committed text — a perfectly coherent structure may be entirely untraced, and saying so is
    not my seat. Blind to authorship, to other seats' verdicts, and to prose quality of messages
    except where a message contradicts another field.
```

### Anchors — Coherence (5 drawback, 5 clean)

**C-D1 — `tier_duplication`.** A single phrase substitution is encoded twice: once as a tuple in the
phrase-corrections table and once as a hand-written impl with the same replacement and a message
differing only in punctuation. Both register under distinct short names, so one construction yields
two lints and a user must switch off two rules to silence one opinion. *Expected: drawback.*

**C-D2 — `dead_layer`.** A Weir file declares three `let` bindings. Two are stepped into the rule's
expression; the third is referenced nowhere in the file and nothing downstream consumes it.
*Expected: drawback.*

**C-D3 — `subsumed_alternative`.** An expression's alternatives list holds a general nominal-phrase
step and, separately, a step matching one specific noun that the nominal-phrase step already admits
at the same position. No admissible token sequence makes the specific arm the deciding match.
*Expected: drawback.*

**C-D4 — `accretion_subsumption`.** The unit accumulated an early POS-set constraint and, later, a
context lookaround. The lookaround's condition entails the constraint's on every token the rule can
reach, so the earlier guard now excludes nothing the later one does not. Two layers, one exclusion.
*Expected: drawback.*

**C-D5 — `internal_contradiction`.** A rule's message tells the writer the construction is
nonstandard; its taxonomy assignment is `Regionalism`; and its variant condition enables it only
under the dialect where the construction is standard. The three fields cannot all describe the same
phenomenon. *Expected: drawback.*

**C-C1 — clean, heavier tier earns its tier.** A hand-written impl sits beside declarative table
entries for related phrases, but its message varies with the matched determiner and its edit
case-matches the author's capitalization. Neither is expressible in the tuple table or the phrase-set
table — the overshoot is only apparent. *Expected: clean.*

**C-C2 — clean, shared layer consumed everywhere.** A pattern is defined once and stepped into four
expressions across a thematic group; each consumer opens a different match window around it, so the
shared declaration carries load at every site and inlining it would multiply the definition.
*Expected: clean.*

**C-C3 — clean, overlapping but separating arms.** Two alternatives of an expression agree on the
first token and diverge on the POS of the next. Each arm is the deciding match for a construction the
other cannot reach, and both constructions are ordinary English. *Expected: clean.*

**C-C4 — clean, one concern one layer.** A filter step exists solely to suppress matches inside
quoted spans. No other layer of the unit mentions quoting, no sibling tier handles it for this rule,
and removing it changes what the structure can express. *Expected: clean.*

**C-C5 — clean, ordered steps not redundant.** A cheap literal step precedes an expensive
POS-dependent tail. The cheap step is not subsumed by the tail: it anchors the left edge of the match
window, and without it the tail's window would begin at an indeterminate offset. *Expected: clean.*

---

## Seat 3 — Corroboration

```yaml
judge: The Unauthored Witness
  purpose: >
    Setting aside everything the artifact says about why this complexity is needed, do signals that
    were not produced as its justification show it earning its place?
  claim_modes: [fact, inference, prediction]
  select:
    - Logical.induction/behavior-on-unauthored-corpora     # documents nobody wrote to defend this unit
    - Logical.causal_reasoning/report-joins-back-to-layer  # external misfire reports that land on this structure
    - Sensorial.usability/switchable-identity-legibility   # the unit as a thing a real user can find and turn off
    - Sensorial.spatial_and_temporal_coherence/cost-borne-per-document
  orientation:
    evidence_standard: >
      Signals not authored to defend this unit: whole-document snapshots of literary and legal prose,
      the dogfood pass over source comments nobody wrote as a test, regression fixtures named for
      reports that predate the layer, the external issue record under its false-positive,
      false-negative, agreement, regionalism and dialect labels, published challenge lint IDs, the
      curated default surface as a user actually meets it, benchmark and fuzz channels, and the
      convention observed by offline checkers in the same domain. Volume is not corroboration:
      one unauthored document that exercises the layer outweighs twenty bespoke cases.
    uncertainty_posture: >
      Absence of an independent signal is a real finding here, because in this domain producing one
      is cheap — a rule that no unauthored corpus, no report, and no benchmark ever touches has not
      met the local bar. But absence of a *reachable* signal is an abstention, not a drawback: where
      the deciding record lives on a maintainer-side backend I cannot read, I say so and stop.
    temporal_horizon: >
      Present signals plus the forward cost the structure commits every user to. Prediction is in my
      modes only for the cost claim — how often this path runs and on whose documents — and I resolve
      it from measurement, never from plausibility.
    stakeholder_scope: >
      The writer being interrupted and the maintainer holding the misfire tally. In this domain a
      false positive costs more than a miss, so a structure that adds reach without adding precision
      is not neutral to me.
    reversibility: >
      Findings reopen on new external signal — a report closed, a fixture added from a real failure,
      a benchmark case, a dogfood hit. My verdicts are the most perishable of the three seats and I
      state them as of the record I read.
    contradiction_sensitivity: >
      Where an unauthored corpus and the external report record disagree about this unit, I report
      the split as the finding rather than averaging it.
    abstention_boundary: >
      `jurisdiction` — whenever the question is answerable only from the unit's own structure or its
      own justifying texts (the other two seats), or on `value`, `belief`, and `experience` modes.
      `evidence` — whenever the deciding independent channel is unreachable: production per-lint-ID
      tallies held off-repository, a current challenge list I cannot fetch, or a measurement that
      requires building and running what I may only read.
  taxonomy:
    unexercised_in_the_wild   -> Logical.induction/behavior-on-unauthored-corpora
    contradicted_by_reports   -> Logical.causal_reasoning/report-joins-back-to-layer
    convention_divergence     -> Logical.induction/behavior-on-unauthored-corpora
    illegible_switch_surface  -> Sensorial.usability/switchable-identity-legibility
    unmeasured_standing_cost  -> Sensorial.spatial_and_temporal_coherence/cost-borne-per-document
  blind_to: >
    The artifact's own self-justification, absolutely: doc comments and rationale prose attached to
    the unit, commit-message and pull-request argument for why the layer was added, contributor
    documentation asserting that this kind of structure is warranted, and any explanatory text
    committed alongside the code. Reading them would let the unit vouch for itself, which is the whole
    reason this seat exists. Also blind to internal redundancy and layer-load questions (Coherence's
    seat), to whether a justifying text exists in the artifact (Grounding's seat), to alternative
    designs I would prefer, and to authorship.
```

### Anchors — Corroboration (5 drawback, 5 clean)

**R-D1 — `unexercised_in_the_wild`.** A rule is registered but off in the curated default surface, is
reached by no group-construction path any integration runs, appears in no committed whole-document
output, and surfaces nothing in the dogfood pass over the project's own comments. No signal outside
its own bespoke cases shows the structure ever executing. *Expected: drawback.*

**R-D2 — `contradicted_by_reports`.** After the guard layer was added, the external issue record
accumulated repeated false-positive reports naming this unit's short ID, and it was subsequently
published as a challenge lint. The independent record says the added structure did not buy the
precision it was added for. *Expected: drawback.*

**R-D3 — `convention_divergence`.** The unit strips its carrier format inline instead of consuming
the shared masking layer every sibling integration uses, and consequently reports character offsets
on a basis no other consumer in the workspace observes. Every domain peer — and every sibling here —
separates prose isolation from detection. *Expected: drawback.*

**R-D4 — `illegible_switch_surface`.** The unit's settings-menu description is a restatement of its
internal mechanism ("applies the nominal-phrase pattern with a negative lookahead"), it sits in a
thematic group whose description names a different phenomenon, and it is on by default. A writer who
receives its lint and wants it gone has no path from the message to the switch. *Expected: drawback.*

**R-D5 — `unmeasured_standing_cost`.** The added layer runs unconditionally over every token of every
document rather than behind a cheap match that has already succeeded, and the benchmark channel
carries no case covering the path. Every user pays on every document, and nobody has measured the
price. *Expected: drawback.*

**R-C1 — clean, unauthored corpora agree.** The unit's short ID appears in the committed full output
of two whole documents — one literary, one legal — that nobody wrote as its tests, at the spans a
reader of that prose would expect, and nowhere else in those documents. *Expected: clean.*

**R-C2 — clean, reports join back and close.** The regression corpus carries two fixtures named for
distinct reported failures, both of which reach this unit's layer, and the corresponding entries in
the external record are closed with no reopening under the false-positive label. *Expected: clean.*

**R-C3 — clean, cost is conditional and measured.** The expensive POS-dependent path runs only after
a cheap literal pattern has matched, the unit is built on the framework trait that shares the
expression cache rather than the unconstrained one, and the benchmark channel carries a case that
walks the expensive path. *Expected: clean.*

**R-C4 — clean, convention corroborates.** The phenomenon is treated as dialect-parameterized rather
than pinned to one blessed variety — matching how the domain's offline peers handle regional
correctness, and matching every sibling rule in the same thematic group. The structure's shape is
what the domain independently converged on. *Expected: clean.*

**R-C5 — clean, unscripted text exercises it.** The dogfood pass over the project's own source
comments surfaces this unit's lints on prose written as documentation rather than as fixtures, and
the external record carries no false-positive report against its ID in the period since. *Expected:
clean.*

---

## Cover gate (self-check, zero-model)

- **Validity** — no seat's anchors are all-pass, all-fail, or all-abstain: each seat is 5 drawback /
  5 clean, and each seat's drawbacks distribute across at least three of its own taxonomy classes.
- **Coverage** — the three seats span the domain's declared warrant standards: traced-to-a-rescued-text
  (Grounding), placement-and-non-duplication on the authoring ladder (Coherence), and
  independent-signal-plus-cost (Corroboration). Whatever unit is under examination lies inside this
  span by construction.
- **Overlap** — pairwise disjoint at parameter level; no gluing rule needed.
- **Falsifiability** — every seat has a closed drawback taxonomy and both typed abstention paths
  (`jurisdiction` and `evidence`), each with a stated trigger.

## Disclosed designed silences

- All three seats jurisdiction-abstain on `value`, `belief`, and `experience` modes. A claim that a
  rule *should* exist, or that its opinion about English is the right one, is untestable as composed.
- Grounding is composed so it can never say "a simpler design would do" — if the answer the ceremony
  wants is a simplification proposal, it comes from Coherence's `tier_overshoot` /
  `tier_duplication` classes or Corroboration's cost class, never from Grounding.
- Corroboration will evidence-abstain on any question whose deciding record is the production
  per-lint-ID tally, which the characterization states lives off-repository.
