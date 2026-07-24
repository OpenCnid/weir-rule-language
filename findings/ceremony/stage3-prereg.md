# Pre-registration — filer's expected verdicts

**Written:** 2026-07-24T01:26:41Z
**Written before:** the Stage-2 composer returned, and before any judge was spawned.
**Never reaches a judge prompt.** Per rule 11, a pre-registration whose bytes reach a prompt is a
work order, not a forecast. Per rule 20, a forecast filed after the run does not count.

---

## Forecast

| Unit | Expected J1 grounding | Expected J2 coherence | Expected J3 corroboration | Confidence |
|---|---|---|---|---|
| U1 `Pattern` | clean | **drawback: superseded-layer** | clean | medium |
| U2 `Step` + lift | clean | **drawback: redundant-indirection** | abstain: evidence | low |
| U3 `Expr` + lift | clean | clean | clean | high |
| U4 Weir AST → `Expr` | clean | clean | clean | high |
| U5 `optimize.rs` | **drawback: speculative-generality** | clean | **drawback: unwarranted-optimization** | low |
| U6 Weirpack manifest | clean | clean | abstain: evidence | medium |
| U7 `Linter` trait | clean | clean | clean | high |
| U8 `LintGroup` | clean | **drawback: god-object** | clean | medium |

## Reasoning, recorded so it can be scored against

- **U1 is my strongest drawback call.** Two match contracts coexist eleven months after the rename
  that was supposed to unify them. I expect a coherence seat to find `patterns/` is a superseded
  layer that never got removed.
- **U3 and U4 are my strongest clean calls.** The `Expr`-returns-a-`Span` contract buys one shared
  traversal for 279 rule files; the Weir lowering reuses it rather than duplicating it. If a judge
  calls either a drawback I expect to have been wrong, not the judge.
- **U5 is my least confident row.** 61 lines of AST optimizer on a corpus of 351 small rules could be
  either a real parse-time win or optimization without a measured motive. I genuinely do not know,
  and I expect at least one abstain here.
- **U8: I expect a god-object finding on size alone (1,251 lines)** and I expect it to be *wrong* on
  inspection, because 224 of those lines are macro invocations registering rules, which is a
  manifest, not logic. If a judge calls this clean with that reasoning, the judge beat my forecast.

## What would falsify my read of this ceremony

If all three seats return `clean` on all eight units, the composition failed the falsifiability gate
in practice even if it passed on paper — a panel that cannot find a drawback in a four-rung ladder
with a known-dead duplicate trait in it is not discriminating. I commit to reporting that outcome as
a **panel failure**, not as harper's vindication.
