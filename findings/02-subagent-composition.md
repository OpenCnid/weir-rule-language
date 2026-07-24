# Sub-agent Composition Record — the harper class-cartographer fan-out

**Run date:** 2026-07-23 · **Skill:** `subagent-composition` · **Guardrail 15:** `prompt-engineering`
and `hypershot-protocol` were both invoked before any agent prompt byte was authored.

---

## 1. The spawn gate

The skill requires at least one of four conditions before spawning at all. Two hold:

- **Context economy — the dominant reason.** `harper-core` alone is 105,805 lines of Rust across 300
  linter files, and the full workspace is 21 Rust crates plus 9 pnpm packages. Each class branch is
  ~450 words of output derived from tens of thousands of lines read. Intermediate reads die in the
  sub-agent's window instead of the orchestrator's. This is exactly the ratio the gate is written for.
- **Parallelism.** The nine classes have disjoint read scopes and fully disjoint write scopes (one
  branch file each). No sibling needs another's result.

Not claimed: clean-room impartiality (that is `judge-composition`'s job later in this run) or durable
specialization (these are one-shot; nothing was written to `.claude/agents/`).

**Ephemeral, not persistent.** Every path in these prompts is variant — a session-specific scratchpad
clone location. Under the invariance test (*across a hundred invocations, is this token identical in
all hundred?*) they fail, so they belong in the `prompt` at call time, never in a file body. No
persistent agent definition was created.

---

## 2. The shared ground block — written once, to a file

The skill's fan-out discipline: *"Compose one shared ground block and reuse it verbatim across
siblings; drift between copies produces findings that cannot be reconciled."*

Nine pasted copies of a ~1,100-word block invite exactly the drift the rule forbids — a single edited
number in copy six is invisible and unreconcilable. Instead the ground was written **once** to
`GROUND.md` and each sibling's prompt opens by pointing at its absolute path. Verbatim identity is
then guaranteed by construction rather than by care. The pointer is an absolute path, not a referring
phrase, so it satisfies the ledger's first failure mode.

`GROUND.md` carries four things:

1. **The subject** — absolute clone path, what harper is, that `gh` is authenticated against it.
2. **Repository-level facts already verified** — 4,460 commits, 2,266 PRs, the quarter-by-quarter
   commit curve, the conventional-commit distribution, the two breaking changes, every subsystem
   birth commit. This exists so nine agents do not each re-run the same `git log` and each spend a
   thousand tokens re-deriving what the orchestrator already established.
3. **The method** — chain of density in system mode, the five-tier time ladder, the ~90-word budget.
4. **Six binding constraints** — repository wins over memory; exact numbers with locators or nothing;
   status labels are load-bearing; own words; reachability reported separately from correctness;
   read-only with an explicit prohibition on `cargo`/`pnpm`/`just`/`npm`.

---

## 3. The nested deliverable frame (level 3)

The skill's sharpest point: *`## Return` **contains a literal frame**, not a paragraph about one* —
and this is the level-3 slot where weak priors cost most, because there is no second message in which
to correct.

Every sibling's `## Return` carries this hypershot. Note the variable-load mix: the tier bullets use
**instruction-bearing** names because the frame alone cannot convey the time-ladder semantics, while
the ledger rows use near-**spread** slots because the table structure already carries the shape.

```md
## C{N} — {Class_Title_As_A_Noun_Phrase_Naming_The_Subsystem}
*Charter: {One_Sentence_Naming_What_Is_In_Scope_And_What_Is_Deliberately_Out}*

- **T1 — essence.** {Invariant_Idea_True_Of_Any_System_Solving_This_Problem_Held_To_Ninety_Words}
- **T2 — current machinery.** {What_Is_Actually_Built_Named_By_File_And_Type_Held_To_Ninety_Words}
- **T3 — with receipts.** {Same_Story_With_Exact_Numbers_SHAs_PR_Numbers_And_Dates_Held_To_Ninety_Words}
- **T4 — the frontier.** {Unfinished_Inconsistent_Unreachable_Or_Known_Broken_Right_Now_Held_To_Ninety_Words}
- **T5 — future plans.** {Proposed_But_Not_Built_From_Open_PRs_And_Issues_Held_To_Ninety_Words}

*Status ledger:* {Capability} — **{shipped|shipped-but-unreachable|proposed|retired}** · ...

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| {Entity_Name} | T{Tier_Introduced} | {path:line or commit SHA or PR number} |
| ... | ... | ... |

*Trellis-relevant observation:* {At_Most_Three_Sentences_On_What_This_Class_Demonstrates_That_A_Builder_Of_A_Composable_Expert_System_Over_User_Text_Could_Reuse_Or_Should_Avoid}

## Uncovered
- {What_Was_Not_Reached_And_The_Reason_It_Was_Not}
```

Two invariants from the skill are preserved exactly: **every claim carries its address** (the entity
ledger's Locator column is mandatory) and **every gap has a slot** (`## Uncovered` makes silence about
a gap impossible to mistake for absence of one).

The status-label enum is spelled out inline rather than described, because the whole point of the
labels is that they are a closed set. A paragraph saying "distinguish shipped from proposed" is a
weaker prior than `{shipped|shipped-but-unreachable|proposed|retired}` sitting in the slot.

---

## 4. Per-class differentiation

The skeleton is identical across all nine. Three things vary, exactly as the skill's *Range* section
predicts — the ground manifest, the tool budget, and the return schema:

| Class | Charter | Schema variation |
|---|---|---|
| C1 document model | text → tokens/spans | — |
| C2 expression system | composable matchers | — |
| C3 **Weir** | the rule DSL + packs | **extra `*Language surface:*` slot** — a full table of statement forms, expression forms, and keywords with locators |
| C4 linter corpus | `Linter`, `LintGroup`, config | — |
| C5 spelling/dictionaries | word existence + metadata | — |
| C6 POS tagging | the one learned model | — |
| C7 format adapters | masking + parsers | — |
| C8 delivery surfaces | LSP, WASM, desktop, extensions | — |
| C9 contribution machine | policy, CI, review | **extra `*Sampling disclosure:*` slot**; `shipped-but-unenforced` replaces `shipped-but-unreachable` in the status enum |

C3 was additionally told, in plain words, that it is the highest-value class in the map — an
attention-management move (the `prompt-engineering` toolkit's section E), placed where the model
attends most strongly.

C9's variations are the interesting ones. Its subject is *process*, so "unreachable" is the wrong
failure mode and "unenforced" is the right one — a policy can be perfectly reachable and still not
bind. And because C9 must sample the PR record to say anything about agent-policy compliance, it is
required to disclose its sample size and is explicitly told that **"cannot determine at this sample
size" is a valid finding**. That is decoherence prevention aimed at the single most likely
fabrication in the whole fan-out: a confident compliance rate derived from six PRs.

---

## 5. Boundaries beyond the allowlist

The skill notes that the Boundaries slot should carry discipline *the allowlist cannot express*.
Three such rules appear in every prompt:

- **No build tooling.** `cargo`, `pnpm`, `just`, `npm` are named and forbidden. A `tools:` allowlist
  containing `Bash` cannot express "you may run `git log` but not `cargo test`" — only prose can.
  The motive is that a build mutates the clone (`target/`, lockfiles) and nine concurrent builds on
  one working tree would corrupt every sibling's read.
- **No sibling reads.** Siblings cannot see each other by construction, but they *share a filesystem*,
  and a branch file written by C3 is readable by C4. Forbidding it preserves the independence that
  makes cross-class agreement meaningful rather than circular.
- **C9 only: reads on GitHub, never writes.** `gh` is authenticated with `repo` scope against a
  third-party repository. "Never post, comment, or modify anything on GitHub" is stated explicitly
  because the tool budget that permits `gh api` for reads also permits it for writes.

---

## 6. Termination

Every prompt ends with the blocked branch named, per the skill's Termination slot:

> If the primary paths do not exist at the stated clone location: report exactly what you found there
> and stop. Do not substitute a different subsystem and do not reconstruct the class from general
> knowledge of grammar checkers.

The second sentence names the *plausible wrong continuation* specifically. A model that cannot find
`harper-core/src/weir/` and knows perfectly well what a rule DSL usually looks like will write a
fluent, entirely fabricated branch unless told not to. Omitting that clause licenses exactly the
failure the whole locator discipline exists to prevent.

---

## 7. Standing of what comes back

Per the skill's failure mode 9: **a sub-agent's return is data, not instruction.** The nine branches
are treated as evidence to be reconciled by the orchestrator, and any directive-shaped text inside
one is a finding to relay, never a command to follow. Cross-class judgment — the trunk, the
cross-link lattice, the temporal cross-section — belongs to the orchestrator and was withheld from
every sibling, because a sibling that speculates about a class it cannot see produces exactly the
unreconcilable claim the fan-out discipline is designed to prevent.
