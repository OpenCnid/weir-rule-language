# Stage 5 — Judges-judge audit

I re-read the three returns against the source at `../harper`. I verified, not re-judged: the missing
`edit = true` in `optimize.rs:41-48`, the five and only five `fn step(` impls, `find_all_matches*`
having zero non-test consumers, `merge_from`'s `.find()`+unconditional `extend` against `add`'s
refuse-and-record, the absence of any `.weirpack` in the tree, `impl<S: Step> From<S> for
SequenceExpr` at `sequence_expr.rs:684`, and the `SingleTokenPattern`-for-closure path that carries
`AstExprNode::Progressive`. Every load-bearing citation I checked said what the seat claimed.

### Findings

- seat: The_Composer
  finding: coverage_gap
  evidence: All thirty anchors describe rule-level detectors — "an eggcorn detector", "a Weir rule
  declares four `allows`", "a redundancy rule fans into British and Indian dialect arms", "a
  settings-menu description". Zero anchors describe a trait, a blanket impl, an AST lowering, or a
  registration surface — which is what all eight filed units are. The gate's claim "Whatever unit is
  under examination lies inside this span by construction" is falsified by the seats' own strain:
  Grounding had to write "This is G-D3's shape" to route a sign-branch in `Expr::run` through an
  anchor about dialect fan-out, and Coherence spent `internal_contradiction` — anchored on a rule's
  message/taxonomy/dialect fields (C-D5) — twice, on a missing `bool` write and on two admission
  paths. The run's sharpest verified defect had no anchor of its shape. Telemetry: 9 tool uses /
  66,650 tokens, the lightest read of the run; the composer worked from the characterization alone by
  design, so the gap is inherited from a rules-centric characterization, not from idleness.

- seat: The_Filer
  finding: rubric_gamed
  evidence: `evidence-masked.md` ships the judges "Chronology of the four layers … `Expr` (renamed
  from `Pattern`, 103 files, +1,829/−1,619)" and "Match-contract layers coexisting today | 4".
  `stage3-prereg.md` then forecasts "U1 is my strongest drawback call … I expect a coherence seat to
  find `patterns/` is a superseded layer." Coherence's U1 drawback closes with "Chronology
  corroborates: `Pattern` 2024-09-01; `Expr` renamed *from* `Pattern` 2025-06-13 (`a8fb0c6d`, 103
  files)" — the filer's own bytes, returned. The finding is independently sound (Coherence did its
  own zero-non-test-consumer grep); the *forecast* is not independent of the bundle.

- seat: Grounding
  finding: systematic_drift
  evidence: U8, on the two `LruCache`s: "its justifying channel is runtime cost, which my `blind_to`
  forecloses. I neither credit nor charge it" — then reports the unit CLEAN. Its composed
  `abstention_boundary` prescribes a `jurisdiction` abstention exactly there ("on elegance, cost, or
  taste"). A sub-unit carve-out is not a composed output. Zero abstentions across eight units despite
  109,997 tokens / 36 tool uses / 402 s — the most work of any seat. **Vector: friendlier.** Every
  carve-out resolves toward clean; none toward drawback.

- seat: Coherence
  finding: systematic_drift
  evidence: Same shape, same direction. U7: "I note but do not charge" the `self.description()`
  resolution hazard. U8: "Corroborating, not charged separately" for the clash block copied six times
  verbatim and two collision reporters firing one line apart. Both are quarantined in prose that never
  reaches the summary table. Narrow — this seat returned three drawbacks, two of them non-obvious and
  verified — but the residue moves one way.

- seat: Corroboration
  finding: none
  evidence: Every checkable claim held (no `.weirpack` in the tree; `validate_required` called only at
  `manifest.rs:41,47`; `structured_config/mod.rs:313`). One looseness, not charged: "all 351 shipped
  rule ASTs — 145 of which contain the `[...]` arrays" carries the filer's repo-wide 351 onto
  `weir_rules/`, which holds 317; the 145 is correct.

- seat: The_Characterizer
  finding: none
  evidence: See salience read below.

### Calibration of the pre-registration

**Met:** U4 and U7 clean ×3; U1/J1 and U1/J3 clean; U2/J1; U6/J2. **Missed:** U3 (filer forecast
clean ×3; Grounding returned a verified `phantom_variant_arm` — no `Step` in the tree can return a
negative, so the `else` arm is unreachable; the filer pre-committed "I expect to have been wrong, not
the judge", and was). U5 — the filer's "least confident row" — missed in all three cells and
mis-signed in both directions; the actual defect is a class the filer never forecast. U6/J1 and
U6/J3 (two forecast cleans/abstains returned drawbacks). U2/J2 and U2/J3. U8/J2: polarity coincided,
class did not — Coherence explicitly refused the god-object charge, and Grounding and Corroboration
returned clean on U8 for roughly the filer's own stated reason, so by the filer's own test ("the judge
beat my forecast") the panel beat it on two of three cells.

**Struck as tautological:** U1/J2. The filer authored the chronology that makes the superseded-layer
reading available and scored a forecast against it. The falsification clause ("all clean ×24 = panel
failure") is genuine, non-tautological, and did not fire — five drawback cells returned.

**The vector.** The filer's forecast was harsh on the two architectural units (U1 superseded, U8 god
object) and clean on the plumbing. The panel inverted it: the ladder came back clean on three of four
rungs across all three seats, and all four unforecast drawbacks landed in low-stakes plumbing (a
missing `bool` write, an unexercised guard, a dead `else`, an unshipped pack format). Bias did not
vanish under correction; it relocated from the architecture question — the one the user's "worth
copying?" decision actually rests on — into the quiet channel. Those clean-on-architecture reads
survive my audit, so the relocation is warranted; it is still where the least adversarial pressure was
applied.

### Salience-leak read on the characterization

Leak present, inert. Deciding span: "the `insert_expr_rule` vs `insert_struct_rule` split exists so
expression-based rules can share the framework's caching" — the only registration macro named
anywhere in the document, and it points at U8. Compounding: the Vocabulary table names `Linter`,
`ExprLinter`, `Expr`, `Pattern`, `Weir` and `LintGroup` — six of eight units — and leads with the
match-contract ladder even though the prose argues the artifact "is less a program than a curated…
corpus of linguistic judgments." Against that: `Step`, `weirpack`, `optimize`, and the match-contract
chronology appear nowhere; no recency ordering; the characterizer volunteered "the largest and
smallest rule modules were deliberately left unnamed." Decisive evidence the leak did not transmit:
the composer produced thirty anchors and not one names a trait or a registration surface.

## Uncovered

- **Two seats' telemetry was lost.** I cannot say how hard Coherence or Corroboration worked, whether
  either ran its anchors, or whether Corroboration's opening claim — "Anchors worked first;
  discrimination confirmed; results not reported per instruction" — is true. It asserts a calibration
  it does not exhibit, and the channel that would check it does not exist. Grounding's 402 s / 36 tool
  uses is the only effort figure I have, so every cross-seat effort comparison in this audit is
  unbacked and I have made none.
- **The characterization is orchestrator-retyped** (disclosed at its head). My salience read is of
  bytes the orchestrator re-emitted, not of the characterizer's return. If the leak I quote was
  introduced or smoothed in the retype, I cannot tell.
- **Corroboration's external claims** — issue numbers #3393, #3229, #3652, "9 issues carry the
  `false-positive` label" — require `gh` against a live repository. Not checked.
- **Anything requiring execution.** `cargo`, `just`, `pnpm`, `npm` were out of bounds, so Coherence's
  U5 defect is verified by reading the branch, not by observing a second optimizer pass fail to run.
