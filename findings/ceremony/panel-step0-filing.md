# Step 0 — Filing the promotion candidate

**Filed:** 2026-07-24 · **Ceremony:** judge-composition · **Canonical law:** `JUDGE_COMPOSITION_GAME.md` §6

---

## Who the claimant is — stated first, because it changes the safeguards

The user asked a **question**: *"We want to find out if it'll be useful to use in any shape or form."*
A question is not a claim, so there is no user claim to file. The candidate under test was **authored
by me** in this session, at `findings/01-spark-steering.md` §6.

I am therefore the **self-invested claimant** — the exact case this ceremony exists to harden against,
with the aggravating factor that the filer and the claimant are the same process. Two consequences,
both binding:

1. **Authorship is masked downstream.** No judge learns who wrote the candidate or that it was written
   in this session. Not because authorship is shameful, but because "the orchestrator's own
   conclusion" is a salience signal that would tilt every seat.
2. **The filing-inflation failure mode is live at maximum.** Rule: file **verbatim byte spans with
   addresses**; decomposition is mode-tagged annotation *over* spans, never prose rewrite. I have a
   standing incentive to file my own conclusion in its strongest form. The spans below are copied
   exactly, including the hedges, and the cuts include the adjacent qualifiers.

---

## The filed candidate — verbatim spans

### Span A — the licensing claim
`findings/01-spark-steering.md:§6`

> **Licensed:** treating harper as a **reference design on the S axis** — a worked, load-bearing,
> production example of the authoring surface Trellis's target function implies. Reading Weir's
> grammar, its optimizer, its pack manifest, and its migration arc is cheap and the lesson is portable
> to Python.

### Span B — the refusal claim
`findings/01-spark-steering.md:§6`

> **Not licensed by this diagnosis:** taking `harper-core` as a Trellis dependency. That is an R-axis
> move against a ruled-out R-axis gap. If it is taken anyway it must be justified on a *different*
> symptom than the one diagnosed here — and the honest one would be narrow: "Trellis wants offline
> English grammar linting of user prose as a product feature," which is a real want but is not the
> capability gap this run located.

### Span C — the axis diagnosis the above rests on
`findings/01-spark-steering.md:§3`

> Trellis's ratified target function is *a personalized composable expert system whose expertise is the
> user's data.* Harper is, structurally, **a composable expert system whose expertise is English
> prose** — and it has already solved the authoring-surface problem Trellis has not yet reached

### Span D — the roster-check that ruled out R
`findings/01-spark-steering.md:§1`

> **It is already in the roster.** Trellis has `src/rlm/trellis_textedit.py`, 1,183 LOC, and its module
> docstring states the pillar harper would supposedly supply

### Span E — the transferable lesson, as the cartographer stated it (not mine)
`findings/branches/C3-weir-language.md`, *Trellis-relevant observation*

> Weir is the cleanest available demonstration that a rule can be *data plus its own acceptance tests
> in one artifact* — `test` and `allows` live beside `expr main`, and a generated harness runs every
> shipped rule's assertions without anyone maintaining a test file. Trellis should copy that
> co-location and also copy the honesty check it makes possible: 64 of 351 rules ship zero assertions
> and the generated test still passes, so a self-testing artifact needs a *floor* enforced at
> registration, not merely a runner.

---

## Step 1 — What promotion would assert, decomposed by claim mode

Compound candidates must decompose — applicability gates cannot run on a conjunction. The
decomposition below is **cuts and tags over the spans above**, not a rewrite.

| # | Sub-claim (tagged span) | Mode | Notes |
|---|---|---|---|
| **P1** | Harper is structurally a composable expert system whose expertise is English prose. (Span C) | `fact` | Checkable against harper's bytes. |
| **P2** | Trellis already holds the span/addressing capability harper would supply, in `trellis_textedit.py`. (Span D) | `fact` | Checkable against Trellis's bytes. |
| **P3** | Weir demonstrates that a rule plus its own acceptance tests can be one artifact. (Span E, first clause) | `fact` | Checkable against `.weir` files. |
| **P4** | 64 of 351 Weir rules ship zero assertions and the generated test still passes. (Span E, second clause) | `fact` | A specific count; falsifiable by recount. |
| **P5** | The authoring-surface problem is one "Trellis has not yet reached." (Span C, final clause) | `inference` | Depends on reading Trellis's current state as lacking it. |
| **P6** | Adopting harper-core as a dependency would be a wrong-axis move. (Span B) | `inference` | Rests on P2 plus the SPARK axis model. |
| **P7** | The Weir lesson "is portable to Python." (Span A, final clause) | `prediction` | Nothing has been built; this forecasts feasibility. |
| **P8** | Trellis *should* copy the co-location, and should add a registration-time floor. (Span E, final clause) | `value` | A recommendation. Per the standing model, user-gated — the panel records it, never ratifies it. |

**Driving question:** *Does the record support promoting P1–P8 from belief to fact, and at what strength?*

**Registry access this opens:** the question is **epistemic** — it asks what the record supports, not
what is beautiful or who is harmed. The Emotional and Ethical planes stay **out** for P1–P7. P8 is
`value`-mode and, under the standing model, is routed to the user gate rather than adjudicated;
it is filed so the panel can flag it if it is load-bearing for the others' coherence.

---

## Known filing hazards, disclosed

- **Span A cut.** I cut Span A at "portable to Python" rather than continuing into §6's third
  paragraph ("Deferred to the user gate"). That omission would *weaken* the candidate if included, so
  the cut tilts **toward** the claimant. Disclosed here; J1's remit includes judging the cut.
- **Span E is not mine.** It is a sub-agent's return, which per `subagent-composition` failure mode 9
  is **data, not testimony from an authority**. It is filed as bytes to be checked, not as support.
- **P4 is the load-bearing falsifiable number.** If it is wrong, Span E's second clause collapses and
  P8's "floor" recommendation loses its motive. It is the cheapest thing in this filing to refute and
  should be attacked first.
