# SPARK-Steering Diagnosis — Automattic/harper as a candidate Trellis lever

**Run date:** 2026-07-23 · **Skill:** `spark-steering` (user-level) · **Subject:** whether harper fills a short axis for Trellis

---

## 0. A framing correction, stated before the diagnosis

The request that opened this run was *"find out if it'll be useful in any shape or form."* That is a
**fitness** question. The skill's first rule forbids scoring a move against fitness:

> Ask *which axis is short*. Do not ask *will this help finish the task* — the task's goal is not a
> SPARK coordinate, and scoring a move against it misfires identically every time.

So this diagnosis does not answer "is harper good." It answers: **is any Trellis axis short in a way
harper touches, and if so which one** — because the axis determines whether harper enters as a
dependency, as a reference design, or not at all. Those three outcomes have wildly different
recurring costs, and picking the wrong one installs permanent capability against a temporary want.

**Honest precondition:** there is **no live session symptom** here. Nothing in Trellis failed and
sent me looking. This is lever-shopping, which is exactly the condition under which the skill warns
that R becomes the reflexive guess. The diagnosis below is therefore run *against Trellis's committed
state*, not against an observed failure, and it is labelled speculative where it is.

---

## 1. Ruling out the reflexive axis (R) first

The skill weights explicitly against R — it holds 40.1% of mapped capability mass and is dominant in
233 of 373 primitives, "which makes it the cheapest and most reachable class of move — and therefore
the default guess even when the gap sits elsewhere."

"Vendor harper-core as a dependency" is the archetypal R-axis move. Test it against the **S vs R**
gate: *is the capable tool already in the roster and merely producing a weak result (S), or is it
genuinely absent (R)?*

**It is already in the roster.** Trellis has `src/rlm/trellis_textedit.py`, 1,183 LOC, and its module
docstring states the pillar harper would supposedly supply:

> the model never counts, and the model never copies. Locations are engine-computed and returned by
> query (`locate`); existing bytes are moved by code at computed addresses (`splice` over a held
> list-of-lines frame); writes are hash-guarded (`write_back` re-hashes the disk bytes against the
> load-time digest and REFUSES a stale write).

It carries `AnchorMismatchError`, `StaleFileError`, a guarded splice family (`replace_lines`,
`insert_lines`, `delete_lines`) that verifies the removal set byte-exactly before staging, and
0-based half-open addressing computed by `locate`. Harper's `Span` machinery is the same idea and
Trellis's is further along on the guard side — harper has no equivalent of the stale-write refusal
because harper does not own the write.

**Verdict on R: ruled out.** Adopting harper-core for span mechanics would install a 21-crate Rust
workspace and a WASM build step to duplicate a Python module that already exists and is already
hardened past it. That is the wrong-axis move the skill exists to prevent.

---

## 2. Ruling out the second-most tempting axis (K)

**R vs K** gate: *did a query return nothing because the resource is absent, or because the retrieval
was formulated badly?* Not applicable — nothing was queried and returned empty.

But K deserves a direct test on its own signature: *is Trellis re-deriving the same fact each time,
or guessing a convention instead of citing one?* Partially, yes — and this is where harper is real.
See §3. The reason K is **not** the primary diagnosis is that harper's contribution is not a *fact*
Trellis keeps re-deriving; it is a *demonstrated ceiling* on an authoring surface. Facts go in
memory. Ceilings are S.

---

## 3. The axis that is actually short: **S — Skills**

**Signature match:** "the obvious tool runs, returns a correct-shaped result, and nothing errored or
was denied — but the output is shallow... the ceiling on what this configuration can *do* is just
low."

Trellis's ratified target function is *a personalized composable expert system whose expertise is the
user's data.* Harper is, structurally, **a composable expert system whose expertise is English
prose** — and it has already solved the authoring-surface problem Trellis has not yet reached:

| Concern | Harper's answer (verified in-tree) | Trellis today |
|---|---|---|
| How is one expert authored? | A `.weir` file: `expr main`, `let message/description/kind/becomes` | Rust/Python module per linter-equivalent |
| Where do the tests live? | **In the same artifact** — `test "input" "output"` lines in the rule file | Separate test files |
| How do experts compose? | `LintGroup`, made runtime-extensible in `refactor(core): make LintGroup runtime-extensible` (2025-02-18) | Composition exists; not runtime-extensible from data |
| How are experts distributed? | **Weirpacks** — a manifest (`author`/`version`/`description`/`license`, all required-validated) plus rules plus optional bundled dictionaries (#2922) | No packaging unit |
| How is a group configured per user? | `default_config.json` + `FlatConfig`, curated defaults | Descriptor registration (PR #179) |

The measured shape: **2,491 LOC of DSL implementation** (`ast.rs` 212, `mod.rs` 699, `parsing/expr.rs`
505, `parsing/stmt.rs` 498, `optimize.rs` 61, plus weirpack 351) carrying **351 `.weir` rules**. The
DSL was created 2026-01-12 (#2357) and within six months had displaced hand-written Rust as the
default way to add a rule. That is the ceiling-raise, and it is the thing Trellis's authoring surface
has not yet demonstrated.

**Cheaper move considered and rejected:** raising a model tier or swapping a subagent persona — the
S-axis's four cheap levers — does not reach this. The gap is not that a model produced a weak
artifact; it is that no *artifact shape* exists for "one composable expert, with its own tests,
packageable." No model tier invents that. The skill's own note applies: this is the case where
"the four cheap levers above genuinely don't reach."

---

## 4. Self-check

```
Symptom: Trellis's ratified target function (composable expert system) has a
         registration surface (PR #179 descriptors) but no single-artifact
         authoring unit that carries a rule and its own tests together, and no
         packaging/distribution unit for a set of them.
Axis: S
Confusable ruled out: R — the S-vs-R gate says check the roster first.
         src/rlm/trellis_textedit.py is already in the roster, already does
         engine-computed addressing, and already exceeds harper on write
         guarding (hash-guarded write_back; harper has no write side). So this
         is a low ceiling on an existing capability, not a missing one.
Cheaper move considered: asking the user (the un-tool) — partially applies and
         IS being spent: the promote/adopt decision is user-gated below, not
         taken here. It does not suffice on its own because the question
         "what shape should an authoring unit take" is answered by evidence
         from a working system, not by a preference the user can simply state.
Lever: skill-creator / Skill_Definition_File — package the Weir-shaped lesson
         (rule + inline tests + manifest = one artifact) as durable procedural
         knowledge, NOT as a code dependency.
Spends: Context-Tax-Per-Turn (class 1) + Retrieval/Dispatch Dilution (class 2),
         paid every turn once installed.
Left unmoved: R. Tempting because harper-core is a real, fast, Apache-2.0,
         12.3k-star artifact sitting right there. Moving R would not fix this
         symptom because the symptom is about the shape of Trellis's own
         authoring artifact — importing harper gives Trellis English grammar
         checking, which is not Trellis's expertise domain and not its target
         function. The dependency would run, and the ceiling would stay where
         it is.
```

---

## 5. Saturation check

Two of the eight self-observable tells fired during this run, both mine and both minor:

- **Tell 2 (R oversubscribed):** `ToolSearch` was used to resolve task tools mid-run rather than
  batched at the start. One redundant round-trip. Not repeated.
- **Tell 6 (A oversubscribed):** no subagent was spawned for the reverse-engineering pass even though
  it was multi-step, because the direct `git log` / `Grep` route finished it — the correct call per
  the tell, recorded here as a *passed* check rather than a failure.

---

## 6. What this diagnosis licenses, and what it does not

**Licensed:** treating harper as a **reference design on the S axis** — a worked, load-bearing,
production example of the authoring surface Trellis's target function implies. Reading Weir's
grammar, its optimizer, its pack manifest, and its migration arc is cheap and the lesson is portable
to Python.

**Not licensed by this diagnosis:** taking `harper-core` as a Trellis dependency. That is an R-axis
move against a ruled-out R-axis gap. If it is taken anyway it must be justified on a *different*
symptom than the one diagnosed here — and the honest one would be narrow: "Trellis wants offline
English grammar linting of user prose as a product feature," which is a real want but is not the
capability gap this run located.

**Deferred to the user gate:** the adopt/decline call itself. Per house method the panel does not
move standing; §5 of the final report carries the recommendation, the owner ratifies.
