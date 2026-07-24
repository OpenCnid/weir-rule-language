# Step 1 — Pool characterization (candidate-blind)

> **Retype disclosure for the audit:** re-emitted by the orchestrator from the characterizer's return
> (the harness writes zero-length transcripts in this session). No content added, removed, reordered,
> or reworded. Treat as orchestrator-touched.

### Pool

Claims in this pool assert that an external, third-party engine — one OpenCnid neither built nor governs — is or is not useful to Trellis, and in what specific shape. They are produced by a reverse-engineering read of `Automattic/harper` pinned at `efa59c33`, and they are candidates for promotion **from** an unratified orientation artifact (`weir-rule-language/docs/density-chain/DENSITY-CHAIN.md`, self-labeled PROPOSED, "subordinate to everything it summarizes") **to** something Trellis would act on: a design record, an adoption-bounds entry, or a build. The pool therefore straddles two authority regimes. On the source side, authority is absolute and one-directional (`harper source → this map → any downstream decision`); on the receiving side, Trellis's own standing ladder governs (`ratified → adopted → design → orientation → skill/memory`). Nothing in this pool has entered that ladder. Every claim here is at most orientation-tier, and the map says so about itself.

### Claim kinds native to this pool

- **Code fact** — a structural or quantitative statement about harper's source: a type at a `path:line`, a count of files or assertions, a lowering relation between two constructs. Settled by re-reading the pinned tree at the cited locator. Falsifiable cheaply and unilaterally.
- **History fact** — a birth commit, PR number, date, or adoption rate derived from the commit and PR record. Settled by `git`/`gh` against the same pin; distinct from code fact because the record can be sampled unevenly and the map discloses that it was.
- **Reachability claim** — "nothing outside the test suite calls this." Settled by callgraph reading, and *scoped*: the map defines it as workspace-internal only, so it is a bounded claim, not a claim about the world.
- **Status assignment** — placement of an entity into the closed label set `shipped | shipped-but-unreachable | shipped-but-unenforced | proposed | retired`. Settled by whether the evidence for the label's defining predicate was actually gathered, not by whether the entity works.
- **Derived defect** — a claimed bug or contradiction inferred from reading (an unset flag, a colliding key, a doc/flag mismatch). Settled in principle by an executed counterexample; the map states none was run.
- **Portability forecast** — a claim that a structure would or would not carry into Trellis's substrate. Not settled by harper's source at all; settled, if ever, by a Trellis-side design record or drill.
- **Recommendation** — "copy this," "avoid that," aggregated from per-branch `Trellis-relevant observation` slots. Compound: it packages a code fact, an inference, and a normative judgment about Trellis's own goals into one sentence.

### What credibility looks like here

A claim earns belief in proportion to how short the distance is between it and a locator someone else can open. The local standard is layered: a claim carrying a `path:line`, SHA, or PR number against the stated pin is checkable by a second reader without trusting the first; a claim whose warrant is an inference from those locators is credible only if the inferential step is stated separately from the fact it rests on; and a claim about what Trellis should do is credible only when it names which of its components are harper facts and which are judgments about Trellis's target function, since the latter cannot be settled by the source at all. Two structural discounts apply to everything: nothing was executed, so every defect and test count is a reading, and every status label is a claim about evidence gathered rather than behavior observed. A credible claim in this pool also survives its own scope — reachability is workspace-scoped, `T5` records requests and not commitments, and a claim that quietly widens past those declared bounds has lost the thing that made it checkable. Silence is not credit: each branch is required to carry an `## Uncovered` list, so an unmentioned gap is a defect in the map rather than evidence of coverage.

### Evidence channels

- The pinned harper tree at `efa59c33` — the only settling authority for code, history, and reachability claims.
- The map's per-branch entity ledgers and status ledgers, which carry locators per claim rather than per section.
- The map's `Provenance & method` and `Honest gaps` sections, which disclose sampling skew, the non-execution boundary, and one retype step.
- Each branch's `## Uncovered` list — the declared negative space.
- On the Trellis side: `docs/GLOSSARY.md`, `docs/ORIENTATION.md` D4 (Record standing), and the adoption bounds register at `docs/product/epistemic-support/RESEARCH_MAP.md` §9, which governs what may be built on which evidence class (notably AB-6 on licensing, AB-10 on provenance standing for un-promoted sources).
- `docs/benchmarks/` — where a dated report is what separates a Trellis claim from a hypothesis.

### Authority structure

Disputes settle in this order. (1) **harper's source at the pin** wins over any sentence in the map, without appeal — the map's own contract says so. (2) **The map's markdown** wins over its HTML render. (3) **A Trellis ratified or adopted record** wins over anything the map proposes for Trellis, including the adoption bounds register, which fixes evidence classes before any build. (4) **A design record** leads implementation but does not outrank the ratified record it sits under. (5) **The map, as an orientation artifact**, sits below all of those and above nothing except skills and memory. (6) **A collaborator's live instruction** outranks the committed record on the session contract only, leaving the AST-immutability, zero-paid, and attribution invariants untouched. Standing across any of these boundaries moves by a user gate, not by a reader's confidence.

### Vocabulary

| Term | What it denotes here |
|---|---|
| Locator | A `path:line`, commit SHA, or PR number attached to a claim; the unit that makes it independently checkable |
| Pin | The fixed commit (`efa59c33`) all source claims are relative to; a claim without it addresses a moving target |
| `shipped-but-unreachable` | Code exists and may be correct, but has no non-test caller in-workspace — reachability reported as a claim separate from correctness |
| `shipped-but-unenforced` | A stated policy nothing mechanically checks |
| Tier T1–T5 | Fixed-length density rungs: essence / current machinery / receipts / frontier / proposed; deeper tiers add entities, never correct shallower ones |
| Uncovered | The mandatory per-branch declaration of what was not reached, so a gap cannot pass as absence of one |
| Trellis-relevant observation | The per-branch slot where a source reading is turned into a portability or recommendation claim |
| Standing | Trellis's label for what a record *is* (RATIFIED / ADOPTED / DESIGN / PROPOSED / IMPLEMENTED / DERIVED / DEPRECATED); the header decides, the index orients |
| Adoption bound | A dated entry in the AB register fixing what may be built on which evidence class; amended by dated entry, never silent edit |
| Derived-source substitution | Acting on a compression of a governing record instead of the record, on a load-bearing act — the failure mode a map like this structurally invites |

## Uncovered

- Which specific set of claims is under examination was withheld by design; no claim was singled out, and no attempt was made to infer the set.
- The nine branches were sampled, not read end to end — C3 in full, others by their contract, ledger, and takeaway sections. Claim kinds are characterized from that sample plus the map's own declared frame.
- harper's source was never opened. Whether the map's locators resolve is exactly the check this pool's credibility standard names, and performing it was out of scope here.
- `DENSITY-CHAIN.html` and `render.py` were not read; the markdown is declared ground truth over both.
- No Trellis record was checked for an existing entry absorbing anything from this map, so whether any claim here has already moved on the standing ladder is unknown.
