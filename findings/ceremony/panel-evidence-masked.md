# Evidence bundle — filed claims P1–P8

Eight claims filed as verbatim spans from an unratified orientation artifact. **Authorship is
withheld**: do not infer, and do not weight, who wrote any span. Treat every span as an anonymous
assertion to be checked against the record.

---

## The spans, as filed

### Span A
> **Licensed:** treating harper as a **reference design on the S axis** — a worked, load-bearing,
> production example of the authoring surface Trellis's target function implies. Reading Weir's
> grammar, its optimizer, its pack manifest, and its migration arc is cheap and the lesson is portable
> to Python.

### Span B
> **Not licensed by this diagnosis:** taking `harper-core` as a Trellis dependency. That is an R-axis
> move against a ruled-out R-axis gap. If it is taken anyway it must be justified on a *different*
> symptom than the one diagnosed here — and the honest one would be narrow: "Trellis wants offline
> English grammar linting of user prose as a product feature," which is a real want but is not the
> capability gap this run located.

### Span C
> Trellis's ratified target function is *a personalized composable expert system whose expertise is the
> user's data.* Harper is, structurally, **a composable expert system whose expertise is English
> prose** — and it has already solved the authoring-surface problem Trellis has not yet reached

### Span D
> **It is already in the roster.** Trellis has `src/rlm/trellis_textedit.py`, 1,183 LOC, and its module
> docstring states the pillar harper would supposedly supply

### Span E
> Weir is the cleanest available demonstration that a rule can be *data plus its own acceptance tests
> in one artifact* — `test` and `allows` live beside `expr main`, and a generated harness runs every
> shipped rule's assertions without anyone maintaining a test file. Trellis should copy that
> co-location and also copy the honesty check it makes possible: 64 of 351 rules ship zero assertions
> and the generated test still passes, so a self-testing artifact needs a *floor* enforced at
> registration, not merely a runner.

---

## The claims, decomposed by mode

Decomposition is cuts and tags over the spans above, never a rewrite.

| # | Claim | Mode | Drawn from |
|---|---|---|---|
| **P1** | Harper is structurally a composable expert system whose expertise is English prose. | `fact` | Span C |
| **P2** | Trellis already holds the span/addressing capability harper would supply, in `trellis_textedit.py`. | `fact` | Span D |
| **P3** | Weir demonstrates that a rule plus its own acceptance tests can be one artifact. | `fact` | Span E, first clause |
| **P4** | 64 of 351 Weir rules ship zero assertions and the generated test still passes. | `fact` | Span E, second clause |
| **P5** | The authoring-surface problem is one "Trellis has not yet reached." | `inference` | Span C, final clause |
| **P6** | Adopting `harper-core` as a dependency would be a wrong-axis move. | `inference` | Span B |
| **P7** | The Weir lesson "is portable to Python." | `prediction` | Span A, final clause |
| **P8** | Trellis *should* copy the co-location, and should add a registration-time floor. | `value` | Span E, final clause |

---

## Disclosed filing hazards

Stated by the filer, and themselves a judged surface:

- **Span A's cut ends at "portable to Python."** The paragraph that follows it in the source artifact
  ("Deferred to the user gate…") was not included. That omission **weakens nothing and strengthens
  the claim**, so the cut tilts toward the claimant. The fairness of this boundary is in scope.
- **Span E was not written by the filer.** It is the return of an automated reader, filed as bytes to
  be checked, not as testimony from an authority.
- **P4 is the load-bearing falsifiable number.** If wrong, Span E's second clause collapses.

---

## Reading access — the record you may check against

1. **The pinned external source tree** (read-only), pinned at commit `efa59c33`:
   `C:/Users/Darian/AppData/Local/Temp/claude/D--trellis-engine--claude-worktrees-exciting-gould-08c722/a81c86a8-d2bb-4451-821a-64d1b5de32f2/scratchpad/harper`
   `git log` and `git show` are available on it.

2. **The receiving engine's own tree** (read-only):
   `D:/trellis-engine/.claude/worktrees/exciting-gould-08c722`

3. **The orientation artifact these spans were cut from**:
   `C:/Users/Darian/AppData/Local/Temp/claude/D--trellis-engine--claude-worktrees-exciting-gould-08c722/a81c86a8-d2bb-4451-821a-64d1b5de32f2/scratchpad/weir-rule-language/docs/density-chain/DENSITY-CHAIN.md`
   It self-labels PROPOSED and states that the source wins over it in every disagreement.

Never run `cargo`, `pnpm`, `just`, `npm`, or `pytest`. Reads only. Modify nothing.
