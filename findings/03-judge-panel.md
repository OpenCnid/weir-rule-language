# Judge Panel — "harper is useful to Trellis, and here is the shape"

**Run:** 2026-07-24 · **Skill:** `judge-composition` · **Driving question:** *does the record support
promoting these claims from belief to fact, and at what strength?*

> **The headline is that the panel broke the claim it was convened to test.** The central inference —
> that harper has solved an authoring-surface problem *"Trellis has not yet reached"* — was
> contradicted by Trellis's own source tree. Details in §3. The surviving finding is narrower, and
> better.

---

## 0. Who the claimant is

The user asked a **question**. A question is not a claim, so there was no user claim to file. The
candidate was authored **by me**, in this session, at `findings/01-spark-steering.md` §6.

So the filer and the claimant are the same process: the self-invested-claimant case at its hardest,
with no second party anywhere in the loop. Authorship was masked from every judge. It did not save me
— see §2.

---

## 2. The panel found three defects in my filing before it found anything about harper

**Charged against the filer, not the claims.** All three from the grounding seat, unprompted:

1. **I broke my own locators.** Step 0 filed every span with an address
   (`findings/01-spark-steering.md` + section). Building the authorship-masked evidence bundle, I
   stripped the addresses *along with* the authorship signal, leaving a "reading access" list whose
   first entry was `DENSITY-CHAIN.md` — a file that contains none of the spans. The seat checked the
   locator it was offered, found nothing, and charged `locator_unresolvable` on P1, P5, P6. Its
   reasoning: *"the seat checks the locator that was offered, not the one that would have worked."*
   It then located the real addresses anyway (`01-spark-steering.md:76-78`, `:150-153`, `:155-159`,
   `:37-38`), which is how I know the spans themselves were faithful.

2. **I dropped a hedge — while writing the hazards section.** The source reads *"the pillar harper
   would **supposedly** supply."* My P2 decomposition dropped "supposedly." That is **filing
   inflation**, the failure the skill names as the single most damaging one, committed by me inside
   the very section disclosing filing hazards.

3. **My hazard disclosure was itself wrong.** I said Span A's cut omitted a following paragraph
   beginning "Deferred to the user gate…". The seat checked: the next paragraph is "Not licensed by
   this diagnosis" (line 155); "Deferred to the user gate" is at line 161.

**Disposition: P1, P5, P6 grounding verdicts are REMANDED, not failed.** Per Step 7, misquote-family
grounding drawbacks indict the filing. I am explicitly not interpreting around them — a remand
interpreted-around is a paraphrased verdict. Re-judging needs a corrected bundle and a fresh spawn,
which this session did not run.

---

## 3. The verdicts

| # | claim | mode | J1 grounding | J2 coherence | J3 corroboration | disposition |
|---|---|---|---|---|---|---|
| **P1** | harper is structurally a composable expert system over English prose | `fact` | *remanded* | clean, full | clean, **bounded** | **promote-weakened** |
| **P2** | Trellis already holds the span/addressing capability | `fact` | clean, **bounded** | clean, **bounded** | clean, **bounded** | **promote-weakened** |
| **P3** | Weir shows a rule + its own tests can be one artifact | `fact` | clean, **full** | clean, **full** | clean, **full** | **promote** |
| **P4** | 64 of 351 Weir rules ship zero assertions; the test still passes | `fact` | clean, reading-strength | clean, reading-strength | clean, **full** | **promote-refined** |
| **P5** | the authoring-surface problem is one Trellis "has not yet reached" | `inference` | *remanded* | **drawback**<br>`scope_creep_past_declared_bound` | **drawback**<br>`independent_channel_contradicts` | **REFUSED** |
| **P6** | adopting harper-core would be a wrong-axis move | `inference` | *remanded* | clean, bounded | **abstain: evidence** | **no-global-section** |
| **P7** | the Weir lesson "is portable to Python" | `prediction` | abstain: evidence | clean, reading-strength | clean, **bounded** | **promote-weakened** |
| **P8** | Trellis *should* copy the co-location and add a floor | `value` | abstain: jurisdiction | abstain: jurisdiction | abstain: jurisdiction | **user-gated** |

---

## 4. P5 is refused, and the refusal is the most useful result in the run

Two differently-blind seats independently rejected it.

**Coherence** charged `scope_creep_past_declared_bound`: my own §4 self-check stated the bound
precisely — Trellis has a registration surface *"but no single-artifact authoring unit… and no
packaging/distribution unit"* — and Span C then restated it with every qualifier dropped as *"the
authoring-surface problem Trellis has not yet reached."* Its verdict: *"Two named absences plus three
partial presences do not entail an unreached problem, and the drop is what makes the claim
uncheckable."*

**Corroboration** went further and read the receiving tree directly — a base fully disjoint from my
citation chain — and **found the thing I said was absent, built and shipped**:

- `GROUNDED_AUTHORING.md` states *"Phases 1–2 IMPLEMENTED (Session 19)"*, with
  `trellis_agent.py --mode author`, a fixed template, a deterministic anchor gate, `npm run modules:author`.
- `src/core/authoring/` holds assemble / corpus / seed / template / anchors / estimate, **each with a
  paired test**.
- `modules/*/module.json` **is a pack manifest carrying `acceptance`**, schema-validated at
  `src/config/modules.ts:66`, with four modules on disk.

So Trellis already has both things I claimed it lacked: an authoring unit *and* a packaging unit with
acceptance criteria. **My inference was false, and it was false about my own project's code.**

### What survives, and it is sharper than what it replaces

Corroboration named the narrower claim that would have passed: *"Trellis lacks Weir's
grammar/optimizer layer and enforces no assertion floor."* And it supplied the decisive detail:

> `acceptance` is `.optional()` at `src/config/modules.ts:66`, and **no code consumes it**.

That is the same defect harper has — 64 of 351 rules assert nothing while the generated harness passes
— reached from the opposite direction, in Trellis's own tree. **The transferable finding is therefore
not "build an authoring surface." It is: make `acceptance` non-optional and consume it at
registration.** One schema change, in code that already exists.

This is the bounded-composed-accuracy discipline paying out: the overreaching claim died, and the
bounded one is actionable today.

---

## 5. The other dispositions

- **P3 → promote, full strength, unanimous.** Corroboration reached it through two warrant-disjoint
  reads: `AfterAll.weir` carries `expr main`, four `let`s and a `test` in one file; separately
  `generate_boilerplate!` emits both `lint_group()` and `#[cfg(test)] run_tests_for_weir_rules()` over
  the same `include_str!` list, so no per-rule test file is maintained.
- **P4 → promote-refined.** Corroboration independently reproduced **351** and **64** exactly, and
  added a channel the others could not: `just_checks.yml` runs `just test-rust` on every push, and the
  check-run record for `efa59c33` returns **success** — so the vacuous pass is confirmed *in CI*, not
  merely by reading. Refined because the phrase "still passes" was written flatly where the source
  branch hedged it.
- **P1, P2, P7 → promote-weakened.** All bounded. P1: `grep -rniI "expert system"` returns **0** across
  harper — the structure corroborates, the *label* is imported. P2: Trellis's `locate` is
  **line-granular** (`enumerate(frame["lines"])`) while harper's `Span` indexes a char/token stream —
  so "already holds the capability" holds for hash-guarded line addressing, not for equivalence to
  harper's character-level spans. That is a real narrowing of a claim I made in §1 of the SPARK run.
- **P6 → no-global-section.** Coherence cleared it; corroboration abstained on `evidence`, and said
  why with unusual care: the axes are genuine Trellis vocabulary (`REASONING_TEMPLATES.md:425`), but
  the *ruling-out* of an R-axis gap is a finding of the very diagnosis the spans were cut from — so
  after removing the citation chain, **nothing** settles it. Recorded *"explicitly so an empty base
  does not read as a weak pass."*
- **P8 → user-gated, disclosed as untestable as composed.** All three abstained on `jurisdiction` by
  design: `value` is absent from every seat's `claim_modes`. This is **not** neutral silence, and per
  rule 12 it is disclosed as designed. Corroboration added one fact for the gate's benefit only:
  `acceptance` is `.optional()`, so the floor is genuinely absent — *"but 'absent' is a fact and
  'should' is a ratification."*

---

## 6. Calibration

Filed before composition, never shown to a judge.

| Claim | I forecast | Returned | |
|---|---|---|---|
| P5 | drawback on grounding **and** coherence | coherence drawback + **corroboration drawback** | ✅ hit, and it was worse than I predicted |
| P2 | corroboration **drawback** | clean, bounded, with a real narrowing | ⚠️ partial |
| P4 | corroboration abstain | clean at **full** strength, via CI | ❌ missed — I underestimated the base |
| P7 | two evidence-abstains | one abstain, two clean-bounded | ❌ missed |
| P1, P3 | clean | clean | ✅ hit |
| P8 | triple jurisdiction-abstain | triple jurisdiction-abstain | **struck as tautological** — I authored the gate |

My falsifier — *"if P5 comes back clean on all three, report a panel failure"* — did not trigger. My
strongest self-criticism in the prereg was the one the panel confirmed and then exceeded.

---

## 7. Standing

The panel emits signed findings; **it never moves standing**. Every promotion verb above is a *user
act the engine records*, not a panel act. Nothing here has entered Trellis's standing ladder, and this
skill deleted and rewrote nothing.

**One item is routed to you specifically:** P8. It is the keystone value — P3 and P4 stand without it,
but it does not stand without them, and it is the only row that says what Trellis should *do*.
