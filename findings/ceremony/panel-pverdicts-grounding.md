# Seat 1 — Locator_Fidelity_Grounding — verdicts on P1–P8

Anchors worked first (G-D1…G-D5, G-C1…G-C5, both abstention types). Results not reported per
instruction.

---

## The bundle-level locator finding (decides P1, P5, P6, P7; noted on P2)

The evidence bundle's reading-access item 3 asserts one provenance locator covering all five spans:

> **The orientation artifact these spans were cut from**:
> `…/scratchpad/weir-rule-language/docs/density-chain/DENSITY-CHAIN.md`

Read the locator first, the claim second. That file is 1042 lines. Searched for the distinctive
strings of each span:

```
grep -c "S axis|roster|target function|Licensed"  DENSITY-CHAIN.md  ->  0
grep -n  "trellis_textedit"                        DENSITY-CHAIN.md  ->  (no hits)
```

**Span E resolves there.** DENSITY-CHAIN.md:411 carries it verbatim:

> *Trellis-relevant observation:* Weir is the cleanest available demonstration that a rule can be
> *data plus its own acceptance tests in one artifact* — `test` and `allows` live beside `expr main`,
> and a generated harness runs every shipped rule's assertions without anyone maintaining a test
> file. Trellis should copy that co-location and also copy the honesty check it makes possible: 64 of
> 351 rules ship zero assertions and the generated test still passes, so a self-testing artifact
> needs a *floor* enforced at registration, not merely a runner. What to avoid is the asymmetric API:
> the Rust pack writer is dead code while the real authoring path lives in TypeScript with its own
> re-implemented validation, so the same invariant is stated twice and can drift.

**Spans A, B, C, D do not resolve there.** They live in an artifact the bundle never names:
`…/scratchpad/harper-analysis/findings/01-spark-steering.md` — Span D at lines 37–38, Span C at
lines 76–78, Span A at lines 150–153, Span B at lines 155–159 (with a byte-identical duplicate at
`…/scratchpad/weir-rule-language/findings/01-spark-steering.md`).

Per G-D1 the seat checks the locator that was offered, not the one that would have worked. The
spans plainly exist elsewhere in reach; that is exactly the case G-D1 calibrates as still a
drawback. The class is `locator_unresolvable`.

Where a claim carries its own independently resolvable locator (P2 does; P3 and P4 resolve through
Span E), the claim-level fidelity check proceeds on that locator and this finding is recorded as
context rather than as the ruling.

## Span E's boundary — checked, fair

Span E was cut at both edges. Leading: `*Trellis-relevant observation:*` was dropped — a framing
label, not a condition. Trailing: the "What to avoid is the asymmetric API…" sentence was dropped.
Ask the boundary question of that edge: does it change what the span means? It concerns the
weirpack *writer* API (Rust dead code vs the TypeScript authoring path) — a different feature from
rule/test co-location. It neither conditions nor exempts the co-location lesson or the 64/351
count. Boundary fair; no `span_truncates_qualifier`.

## Span A's boundary — the disclosed hazard is itself misfiled

The bundle discloses that Span A's cut ends at "portable to Python" and that the paragraph following
it in the source is "Deferred to the user gate…". Read at the source: the paragraph immediately
following Span A (01-spark-steering.md:150–153) is **"Not licensed by this diagnosis:"** at line
155. "Deferred to the user gate" is at line 161, two paragraphs later. The disclosure names the
wrong neighbour. The real adjacent paragraph *is* the conditioning one — and it is filed in the
bundle as Span B, so the bundle as a whole preserves the qualifier even though the disclosure
mis-describes it. Recorded; it does not add a separate drawback.

---

## P1 — `fact`, Span C

Claim: Harper is structurally a composable expert system whose expertise is English prose.

Locator offered: Span C, at DENSITY-CHAIN.md. Does not resolve there (see above). No in-tree
locator is offered for the structural characterization either — no byte in the pinned harper tree at
`efa59c33` calls harper a "composable expert system"; the vocabulary is imported from Trellis's own
target function, which Span C states one clause earlier. There is in-tree material an informed
reader would reach for (`LintGroup`, `harper-core/src/linting/`), but per G-D3 the seat rules on
bytes offered, not on what a reader would assemble.

**drawback · locator_unresolvable**

## P2 — `fact`, Span D

Claim: Trellis already holds the span/addressing capability harper would supply, in
`trellis_textedit.py`.

This claim carries its own locator and it resolves. At
`D:/trellis-engine/.claude/worktrees/exciting-gould-08c722/src/rlm/trellis_textedit.py`:

- `wc -l` = **1183** — the stated "1,183 LOC" is exact.
- Module docstring lines 5–9 carry, byte-for-byte, the text Span D block-quotes: "the model never
  counts, and the model never copies. Locations are engine-computed and returned by query
  (`locate`); existing bytes are moved by code at computed addresses (`splice` over a held
  list-of-lines frame); writes are hash-guarded (`write_back` re-hashes the disk bytes against the
  load-time digest and REFUSES a stale write)."
- Docstring lines 40–41 add "Addresses are 0-based, half-open [start, end) — Python slice semantics,
  computed by `locate`, never estimated by the model." The span/addressing capability is carried.

Two narrowings, which set the ceiling rather than defeat the claim:

1. The cited bytes say nothing about harper. "the capability harper would supply" is a comparative
   attachment no byte in `trellis_textedit.py` can settle; the docstring settles only Trellis's
   possession.
2. The source span hedges — "states the pillar harper would **supposedly** supply". The
   decomposition dropped "supposedly", against the bundle's own rule that decomposition is "cuts and
   tags… never a rewrite". The dropped hedge bears on the harper half, not on Trellis's possession,
   so it narrows rather than breaks.

The span's stated provenance (DENSITY-CHAIN.md) is wrong — it is at 01-spark-steering.md:37–38 —
but the code fact stands on its own resolvable locator.

**clean · faithful · bounded**

## P3 — `fact`, Span E first clause

Claim: Weir demonstrates that a rule plus its own acceptance tests can be one artifact.

Span resolves at DENSITY-CHAIN.md:411. The two in-tree assertions it makes both check out at
`efa59c33`:

- `test` and `allows` beside `expr main`: `harper-core/src/linting/weir_rules/AllOfASudden.weir`
  opens `expr main [(all of the sudden), (all of sudden), (all the sudden)]` and carries eleven
  `test` lines and one `allows` line in the same file.
- "a generated harness runs every shipped rule's assertions without anyone maintaining a test file":
  `harper-core/build.rs` walks `src/linting/weir_rules`, emits `weir_rules_generated_list.rs`, and
  `weir_rules/mod.rs:57-78` expands it into `#[cfg(test)] mod tests { fn run_tests_for_weir_rules()
  }`, calling `assert_passes_all` once per standalone rule and once per grouped child. No
  hand-maintained test file exists for the rules.

Locator resolves, referent matches, boundary fair. The cited span alone carries the whole sentence.

**clean · faithful · full**

## P4 — `fact`, Span E second clause

Claim: 64 of 351 Weir rules ship zero assertions and the generated test still passes.

Counted at the pin over `harper-core/src/linting/weir_rules`, treating a `test` or `allows` line as
an assertion:

```
TOTAL=351  ZERO=64
```

Exact on both numbers. The denominator is the `.weir` file count (317 top-level plus 34 inside 11
group directories); `weir_rules/mod.rs` calls the grouped children "regular Weir rules inside an
inner LintGroup", so counting them as rules is faithful to the tree's own vocabulary. (The count of
*public Harper* rules is 328, a different quantity the claim does not assert.) The 64 include
`AlzheimersDisease.weir`, `FreeRein.weir`, `Towards.weir`, `CapitalizeOn/Ise3PersSing.weir`, etc.

Second conjunct — "the generated test still passes". `harper-core/src/weir/mod.rs:415-417`:

```rust
pub fn assert_passes_all(linter: &mut WeirLinter) {
    assert_eq!(Vec::<TestResult>::new(), linter.run_tests());
}
```

`run_tests` (mod.rs:214) iterates declared tests; a rule with none returns an empty vector, so the
assertion holds vacuously. DENSITY-CHAIN.md:309 states the same in terms: "the generated
`run_tests_for_weir_rules` passes vacuously on an empty rule." This is a source reading, not an
executed run — the pool forbids `cargo`. Under that declared non-execution boundary the span
supports the claim, which is precisely `reading-strength`.

**clean · faithful · reading-strength**

## P5 — `inference`, Span C final clause

Claim: the authoring-surface problem is one "Trellis has not yet reached."

Locator offered: Span C at DENSITY-CHAIN.md. Does not resolve there. Unlike G-C5 — where a claim of
non-reach cited the branch's own declared negative-space list and was clean — nothing here is cited
for the negative. (The source artifact does hold a "Trellis today" column at
01-spark-steering.md:80-86 with entries such as "Separate test files" and "No packaging unit", but
that table is not inside the filed span and is not what the bundle points at.)

**drawback · locator_unresolvable**

## P6 — `inference`, Span B

Claim: adopting `harper-core` as a dependency would be a wrong-axis move.

Locator offered: Span B at DENSITY-CHAIN.md. Does not resolve there; it is at
01-spark-steering.md:155-159. Decomposed, the residue after the checkable component ("harper-core
exists as a Rust crate that would become a dependency" — trivially resolvable at
`harper-core/Cargo.toml`) is a framework classification about Trellis's own diagnosis, which no
byte in any of the three trees settles; had the locator resolved, that residue would have routed to
abstention. The ruling is decided at the first check.

**drawback · locator_unresolvable**

## P7 — `prediction`, Span A final clause

Claim: the Weir lesson "is portable to Python."

Two independent reasons the seat cannot rule on fidelity here, and the second is decisive.

1. Locator: Span A does not resolve at DENSITY-CHAIN.md; it is at 01-spark-steering.md:150-153. The
   cut of the sentence itself is fair — "Reading Weir's grammar… is cheap and the lesson is portable
   to Python" — P7 extracts the second conjunct without distorting it.
2. Settling authority: this is a forecast about a lesson's transfer between languages. None of the
   three artifacts the pool names — a pinned Rust tree, the Trellis tree, a PROPOSED map — can
   contain bytes that settle it. This is the literal abstention calibration: a portability forecast
   whose only locator is source bytes that cannot settle it.

Abstention is typed and is not a soft fail; the locator defect is recorded above rather than
converted into a fidelity verdict on an unsettleable forecast.

**abstain · evidence**

## P8 — `value`, Span E final clause

Claim: Trellis *should* copy the co-location, and should add a registration-time floor.

Span E resolves at DENSITY-CHAIN.md:411 and the sentence is quoted faithfully ("Trellis should copy
that co-location… so a self-testing artifact needs a *floor* enforced at registration, not merely a
runner"). Decomposed, the code-fact components — co-location exists; the harness passes on
assertion-less rules — are already ruled at P3 and P4 respectively. What remains is a sentence
asserting what Trellis *should* do. No fidelity question survives decomposition; the seat does not
rule on it. Per G-C4 this is the partial-jurisdiction pattern: the components in remit returned
clean, and the normative residue is routed here.

**abstain · jurisdiction**
