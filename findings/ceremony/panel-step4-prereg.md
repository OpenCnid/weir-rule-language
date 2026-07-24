# Step 4 — Pre-registration (judge panel, candidate P1–P8)

**Written:** 2026-07-24, before the Stage-1 characterizer returned and before any judge was composed
or spawned. **Never reaches a judge prompt** (rule 11). A forecast filed after the run does not count
(rule 20).

---

## Forecast

| Sub-claim | Mode | J1 grounding | J2 coherence | J3 corroboration | Confidence |
|---|---|---|---|---|---|
| **P1** harper is structurally a composable expert system over English prose | `fact` | clean | clean | clean | high |
| **P2** Trellis already holds the span/addressing capability | `fact` | clean | clean | **drawback** | medium |
| **P3** Weir demonstrates rule + tests as one artifact | `fact` | clean | clean | clean | high |
| **P4** 64 of 351 Weir rules ship zero assertions; generated test still passes | `fact` | clean | clean | **abstain: evidence** | medium |
| **P5** the authoring-surface problem is one Trellis "has not yet reached" | `inference` | **drawback** | **drawback** | abstain: evidence | high |
| **P6** adopting harper-core would be a wrong-axis move | `inference` | clean | **drawback** | abstain: jurisdiction | medium |
| **P7** the Weir lesson "is portable to Python" | `prediction` | abstain: evidence | clean | abstain: evidence | high |
| **P8** Trellis *should* copy the co-location and add a registration floor | `value` | abstain: jurisdiction | abstain: jurisdiction | abstain: jurisdiction | high |

## Reasoning, recorded so it can be scored

- **P5 is the weakest link and I expect the panel to say so.** "Has not yet reached" is a claim about
  Trellis's *absence* of something, and absence is the hardest thing to ground. I filed it; I expect
  it to come back a drawback on both grounding and coherence, and I will treat that as the panel
  working rather than as the panel erring.
- **P2's corroboration drawback is my most specific prediction.** Grounding will find the docstring
  says what I said it says. Corroboration, which is blind to the artifact's own rationale comments,
  has to look at *call sites* — and a docstring describing a capability is not evidence the capability
  is exercised. If corroboration returns `clean` on P2 without checking callers, that is a
  `convention_blind` finding for the audit, not a vindication for me.
- **P7 is a prediction with nothing built.** Two evidence-abstains is the honest outcome. If any seat
  returns `clean` on P7, it has treated a forecast as a fact, and I want that named.
- **P8 is a value claim.** Under the standing model it is **user-gated, never panel-ratified.** All
  three abstaining on `jurisdiction` is the *designed* outcome, so per rule 12 it must be disclosed as
  **untestable as composed** and never presented as neutral silence. **This row is struck from any
  calibration tally as tautological** (rule 11) — I authored the gate that guarantees it.
- **P4 is the cheapest claim to refute and should be attacked first.** A recount either confirms 64/351
  or it does not.

## What would falsify my read of this panel

If P5 comes back `clean` on all three seats, the composition failed to discriminate on exactly the
sub-claim I flagged in the filing as my weakest — and I commit to reporting that as a **panel
failure**, not as my claim being stronger than I thought.

If every seat returns `clean` on every non-value row, the panel did not discriminate at all, and the
Step-3 validity gate passed on paper while failing in practice.

## Struck from calibration in advance

- **P8, all three seats.** Consequence of a gate I authored.
- **P7's abstentions**, if they come back `evidence` — I filed P7 knowing nothing is built, so an
  evidence-abstain is near-tautological. Counted only if a seat abstains for a *different* stated
  reason than the one I anticipated.
