# Seat 3 — Chain_Disjoint_Corroboration — verdicts P1–P8

## Base construction

The claim's citation chain is the orientation artifact
`scratchpad/weir-rule-language/docs/density-chain/DENSITY-CHAIN.md` (reading access item 3), from
which all five spans were cut. It and everything warranted only by it are **out of base**. I did not
open it, and I did not read the spans' stated rationales — only their assertions.

The base is therefore two channels:

- **C1 — the pinned source**, `harper` @ `efa59c33b2915108f52c385ce1e3311a3cfa1439` (settling
  authority for source claims).
- **C2 — the receiving engine tree**, `D:/trellis-engine/.claude/worktrees/exciting-gould-08c722`
  (settling authority for what Trellis holds).
- **C3 — a history/execution channel**: `git log` on C1 and the GitHub check-run record for the
  pinned commit.

**Chain-leakage check on C2.** A repo-wide case-insensitive search of the Trellis tree for `harper`
returns only substring hits on the word *sharper* (`SELF_DESCRIBING_SURFACES.md:308`,
`TEST_TIME_TRAINING.md:16`, `COLLABORATOR_BRIEFING.md:446`, `orchestrator_prompt.ts:45`). **Zero**
genuine references. C2 is fully chain-disjoint: nothing in the receiving tree was written in
response to this reading, so its agreement is not relocation.

---

## P1 — Harper is structurally a composable expert system whose expertise is English prose. `fact`

**Channel:** C1, direct read, rationale not in view.

Composability is present at the settling authority and is not a summary sentence about itself:
`harper-core/src/linting/lint_group/mod.rs:376` `pub fn add(&mut self, name: impl AsRef<str>,
linter: impl Linter + 'static) -> bool` inserts a **named** linter into a keyed map and refuses
duplicate keys; `:488` `pub fn set_all_rules_to(&mut self, enabled: Option<bool>)` is per-rule
configuration; `:1048` `impl Linter for LintGroup` makes a group itself a linter, and
`harper-core/src/linting/weir_rules/mod.rs` exercises exactly that recursion — a directory under
`weir_rules` builds an inner `LintGroup` (`let mut grouped_rule = LintGroup::default();`) which is
then `group.add($group_name, grouped_rule)`. Nested, named, individually-toggleable rules is the
structural sentence the claim asserts.

The knowledge base is English prose: 300 `.rs` rule files in `harper-core/src/linting/`, 351
`.weir` rule files, a curated FST dictionary (`FstDictionary::curated()`, used at
`harper-core/src/weir/mod.rs:245`), plus `harper-brill` (POS) and `harper-thesaurus`.

**Bound.** The phrase "expert system" occurs **0 times** anywhere in the pinned tree
(`grep -rniI "expert system"` over `*.rs`, `*.md`, `*.ts`). The independent channel corroborates the
*structure* the claim describes, not the *label*; the label is the claimant's frame, imported.

**Falsification shape:** had the claim been false, `LintGroup` would have been a monolithic `lint()`
with no per-rule key, no `set_all_rules_to`, and no `impl Linter for LintGroup` to nest with.

**Verdict:** clean · `independently_corroborated` · `bounded`.

---

## P2 — Trellis already holds the span/addressing capability harper would supply, in `trellis_textedit.py`. `fact`

**Channel:** C2, direct read.

`wc -l src/rlm/trellis_textedit.py` → **1183**. The filed figure "1,183 LOC" is exact.

The module docstring does state a pillar, verbatim: *"The pillar in one line: the model never counts,
and the model never copies. Locations are engine-computed and returned by query (`locate`); existing
bytes are moved by code at computed addresses (`splice` over a held list-of-lines frame); writes are
hash-guarded"*, and *"Addresses are 0-based, half-open [start, end) — Python slice semantics,
computed by `locate`, never estimated by the model."* The methods exist: `locate` (:372), `splice`
(:406), `replace_lines` (:524), `insert_lines` (:590), `delete_lines` (:656), `write_back` (:737).

**Where the independent channel stops.** `locate` iterates `enumerate(frame["lines"])` and returns
`{"line": i, "preview": ...}` — the address space is **whole lines**. Harper's is not:
`harper-core/src/span.rs:19` `pub struct Span<T> { pub start: usize, pub end: usize, ... }` indexes
into a `Vec<char>` / token stream, and lints are placed by `suggestion.apply(lint.span, &mut
text_chars)`. Both are half-open index pairs, but they are not the same granularity, and nothing in
C2 supplies tokenization or character-offset spans.

The narrower sentence C2 does establish: *Trellis holds a line-granular, engine-computed,
hash-guarded addressing surface at exactly 1,183 LOC whose docstring states the code-mediated-text
pillar.* The wider sentence — that this is the capability harper would supply — is not established;
character-level span placement over a tokenized document is absent from the base.

**Verdict:** clean · `bounded_corroboration` · `bounded`.

---

## P3 — Weir demonstrates that a rule plus its own acceptance tests can be one artifact. `fact`

**Channel:** C1, two warrant-disjoint reads.

*Read 1 — the artifacts themselves.* `harper-core/src/linting/weir_rules/AfterAll.weir` is, in
full, `expr main (afterall)`, four `let` statements, and `test "I hope it will pop up afterall but
that remains to be seen." "I hope it will pop up after all but that remains to be seen."`.
`BadRap.weir` likewise carries `expr main [(bed rap), (bad rep)]` and a `test` line. Rule and
assertion are one file.

*Read 2 — the harness that consumes them, a different warrant.*
`harper-core/src/linting/weir_rules/mod.rs` declares `macro_rules! generate_boilerplate!`, which
emits both `lint_group()` (production registration via
`include_str!(concat!(env!("WEIR_RULE_DIR"), "/", $path))`) **and** `#[cfg(test)] mod tests { #[test]
fn run_tests_for_weir_rules() { ... assert_passes_all(&mut linter); } }` over the *same* path list,
for standalone rules and grouped children alike. There is no per-rule test file to maintain: the
same manifest entry serves shipping and testing.

`assert_passes_all` is `harper-core/src/weir/mod.rs:415`; `WeirLinter::run_tests` (:214) reads
`self.ast.iter_tests()`, and `ast.rs:61-67` shows that iterator yields both `AstStmtNode::Test {
expect, to_be }` and `AstStmtNode::Allows { value }` — so `test` and `allows` are the two assertion
forms, exactly as the artifacts co-locate them.

**Falsification shape:** had the claim been false, the assertions would live in a hand-maintained
`.rs` test module keyed to rule names, and `generate_boilerplate!` would have had no `#[cfg(test)]`
arm over the shipped path list.

The pinned source settles source claims outright. **Verdict:** clean · `independently_corroborated`
· `full`.

---

## P4 — 64 of 351 Weir rules ship zero assertions and the generated test still passes. `fact`

This is the disclosed load-bearing number. Both halves were checked on independent channels.

**The count — C1, direct enumeration.**
`find harper-core -name "*.weir" | wc -l` → **351** (317 at `weir_rules/` top level plus 34 across
11 grouped subdirectories: CapitalizeOn 8, EnvironmentVariable 4, Hazzle 4, MayOfPronoun 3,
NotLongAfter 3, ClicheAccent/ExpandConfiguration/ExpandPreference/IncidentReport/LinkedList/
NeitherHereNorThere 2 each). Repo-wide the figure is also 351 — no `.weir` file lives outside
`harper-core`.

Files matching neither `^\s*test\b` nor `^\s*allows\b` → **64**. Cross-check: files with no `test`
statement → 64; the two sets coincide, so no rule is assertion-bearing by `allows` alone. Both
filed numbers reproduce exactly. Sample of the 64: `AlzheimersDisease.weir`, `AvoidAndAlso.weir`,
`BanTogether.weir`, `BareInMind.weir`, `BeckAndCall.weir`, `CapitalizeOn/Ise3PersSing.weir`,
`CaseSensitive.weir`.

**The vacuous pass — mechanism, C1.** `run_tests` (`weir/mod.rs:214`) builds
`let tests: Vec<(String,String)> = self.ast.iter_tests()...collect();` then pushes a `TestResult`
only inside `for (text, expected) in tests`. Zero statements → zero iterations → empty `results`.
`assert_passes_all` (:415) is `assert_eq!(Vec::<TestResult>::new(), linter.run_tests());` — empty vs
empty. A zero-assertion rule passes by construction, contributing no signal.

**The pass — C3, a real execution, warrant-disjoint from my code read.** `just test-rust` is
`cargo test -q` (`justfile:494-496`), and `.github/workflows/just_checks.yml` runs `test-rust` in
its matrix on `push` to `master` and on every `pull_request` to `master`. The check-run record for
the pinned commit `efa59c33b2915108f52c385ce1e3311a3cfa1439` returns `just test-rust :: completed ::
success`. The suite that contains `run_tests_for_weir_rules` **actually ran and actually passed**
with those 64 rules shipped.

This clears the structural discount: an execution exists in the base, so the behavioral half is not
capped at reading-strength.

**Falsification shape:** the count would have come back at some other pair, or `test-rust` would be
`failure` / the 64 rules would never have merged.

**Verdict:** clean · `independently_corroborated` · `full`.

---

## P5 — The authoring-surface problem is one "Trellis has not yet reached." `inference`

A negative claim about the receiving engine. Per the seat's negative-space parameter I went looking
in C2 rather than crediting the artifact's silence. C2 is chain-disjoint (zero genuine `harper`
references), so what it surfaces is not relocation.

**What the direct read surfaces — an implemented authoring surface, not an unreached one:**

- `docs/architecture/GROUNDED_AUTHORING.md`, header: *"Status: Phases 1–2 IMPLEMENTED (Session 19,
  July 9, 2026)"* and *"The mode (`trellis_agent.py --mode author`), pinned attribution, the fixed
  template, the deterministic anchor gate, and the operator driver (`npm run modules:author`)
  shipped in Session 19."*
- The code behind it: `src/core/authoring/` holds `assemble.ts`, `corpus.ts`, `seed.ts`,
  `template.ts`, `anchors.ts`, `estimate.ts`, each with a paired `.test.ts`.
  `src/rlm/trellis_agent.py:289` `def build_author_tools(workspace):`, invoked at `:361`.
- **The pack manifest already exists.** `modules/<name>/module.json` carries `name`, `version`,
  `purpose`, `research.sourceNodeIds`, `addendum`, `tools`, `bounds`, `acceptance`, `status`,
  `kernelCompat`, validated by a schema at `src/config/modules.ts:66`. Four modules are on disk
  (`estimation-discipline`, `reasoning-templates`, `spatial-flywheel`, `workspace-discipline`), and
  `GROUNDED_AUTHORING.md` records a completed paid authoring turn that produced one (PR #45,
  `modules/workspace-discipline/`).
- `docs/architecture/WORKSPACE_AND_MODULES.md` records the module system as *"§11 steps 1–5
  implemented (Sessions 14–17)"*, with the loader at `src/rlm/trellis_modules.py`.

The claim asserts an area Trellis has not reached; a direct read of the settling authority for
receiving-side facts surfaces that area built, tested, shipped, and exercised. Per the seat's
authority order this is a resolved contradiction, not a tie — the R-D3 shape.

**Honest bound on the finding, stated so it is not overread.** C2 does not hold a *rule DSL* with a
grammar and an optimizer, and its `acceptance` field is `.optional()` with no runner consuming it
(only `z.object({ zeroPaid: z.string().min(1) }).optional()` at `src/config/modules.ts:66`). A
sentence like "Trellis's authoring surface lacks Weir's grammar/optimizer layer and enforces no
assertion floor" would have survived this seat cleanly. The sentence actually filed — that the
problem is one Trellis *has not yet reached* — does not.

**Verdict:** drawback · `independent_channel_contradicts`.

---

## P6 — Adopting `harper-core` as a dependency would be a wrong-axis move. `inference`

**What the base does corroborate — the presupposition only.** The R/S axis vocabulary is genuine
receiving-side vocabulary, not an artifact coinage: `docs/architecture/REASONING_TEMPLATES.md:425`
heads *"17.R. Full R-axis operation inventory (code review, master @ 51d9c7a4)"* and enumerates
graph read/write and retrieval families; `:417` names `trellis_workspace.add_note`, `set_plan`,
`segment` as *"the S-axis operations."* So the axes the claim reasons over exist independently of
the chain.

**What the base cannot reach — the claim's whole content.** P6 turns on a *ruled-out R-axis gap*.
The ruling-out is a finding of the diagnosis the spans were cut from; after removing that chain,
nothing in C1, C2, or C3 rules an R-axis gap in or out, and nothing classifies a grammar-linting
dependency onto an axis. The R-axis inventory at §17.R is graph/retrieval operations, on which
`harper-core` supplies nothing at all — which is enough to show the classification is not
independently derivable, but not enough to affirm or deny the claim.

A collateral fact worth recording without weighting it: `harper-python/Cargo.toml` is a Rust crate
that lints Python *source comments* via `tree-sitter-python`, not a Python binding to `harper-core`.
No Python API exists in C1. That bears on feasibility, not on axis.

The only support for the claim's content is the chain itself. Recorded explicitly so an empty base
does not read as a weak pass.

**Verdict:** abstain · `abstain_evidence`.

---

## P7 — The Weir lesson "is portable to Python." `prediction`

**Channel: C2, and it is a real one.** The lesson's first half — an artifact carrying its own
acceptance declaration beside its data — is *already realized* in a Python/TypeScript system in the
base, independently of this reading. Every `modules/<name>/module.json` carries
`"acceptance": { "zeroPaid": "npm run test:modules" }` beside `purpose`, `addendum`, and `bounds`,
schema-validated at `src/config/modules.ts:66`, with `test:modules` wired at `package.json:64`
(`tsx scripts/test_modules.ts`, which spawns `scripts/test_modules.py` across the real cross-language
delivery path). That is an existence proof, not a forecast.

**Where it stops.** Two gaps the base makes visible:

1. `acceptance` is `.optional()` and **nothing consumes it** — `grep acceptance` over
   `src/config/modules.ts` and `scripts/test_modules.ts` returns only the schema line. Trellis has
   co-location as *metadata*; Weir has it as *executed assertions*.
2. Weir's generated harness is Rust compile-time machinery: `macro_rules! generate_boilerplate!`
   expanding `include_str!(concat!(env!("WEIR_RULE_DIR"), "/", $path))` into a `#[cfg(test)]`
   module. Nothing in the base demonstrates that the *generated-harness* half reproduces in Python,
   where the equivalent would have to be runtime discovery rather than macro expansion.

The narrower sentence the independent channel supports: *the co-location of an artifact with its own
acceptance declaration is already expressed in Python/TS in the receiving tree; the generated
run-every-shipped-rule harness is not corroborated as portable anywhere in the base.* Returning
clean on that, with the ceiling named, rather than passing the wide version or failing the claim.

**Verdict:** clean · `bounded_corroboration` · `bounded`.

---

## P8 — Trellis *should* copy the co-location, and should add a registration-time floor. `value`

Mode `value`. No quantity of chain-disjoint evidence can promote what is user-gated by construction;
the seat records the type and declines. Noted without weighting, and offered only so the gate has
the fact in hand: the base does show that Trellis's `acceptance` field is `.optional()`
(`src/config/modules.ts:66`), so the described floor is genuinely absent — but "absent" is a fact
and "should" is a ratification, and only the second is what P8 asks for.

**Verdict:** abstain · `abstain_jurisdiction`.

---

## Filing-hazard note (in scope per the bundle)

Span A's cut ends at "portable to Python," omitting the "Deferred to the user gate…" paragraph. From
this seat that omission is immaterial: P7 was ruled on the independent channel's reach, and a
deferral sentence is neither corroboration nor contradiction. Span E's non-filer authorship is
likewise immaterial here — the seat is blind to authorship, and Span E's two load-bearing clauses
(P3, P4) both reproduced exactly on channels that could have disagreed.
