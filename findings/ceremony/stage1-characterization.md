# Stage 1 — Domain characterization (candidate-blind)

> **Retype disclosure, for the Stage-5 audit.** The characterizer's transcript file was written
> zero-length by the harness, so these bytes were re-emitted by the orchestrator from the return it
> received, rather than copied mechanically. That is a retype step, and per `JUDGE_INTAKE_DESIGN.md`
> §1.2 a retype step reintroduces the filer's-pen risk the substrate normally removes. No content was
> added, removed, reordered, or reworded — but the auditor should treat this file as
> orchestrator-touched and weigh it accordingly.

### Domain

This is a rule-engine neighborhood for natural-language linting: a Rust workspace whose engine crate turns plain prose into a token stream, tags it, and runs a large population of independent detectors over it, each emitting a span, a message, a taxonomy label, and zero or more machine-applicable edits. Unlike the code-linter systems it structurally resembles (ESLint, Clippy), the input grammar is not formally specified and the "correct" parse is not recoverable, so every detector operates on a lossy, probabilistic substrate — a Brill tagger and chunker with trained model files, an FST-backed dictionary with per-word metadata, and a set of expression combinators standing in for a real parser. Unlike its nearest domain peers (LanguageTool, hunspell, Vale), this one is shipped as an offline, in-process library targeted at millisecond latency and WebAssembly-scale footprint, which makes cost a first-class design constraint rather than an afterthought. The rule population here is roughly 354 Rust modules under `harper-core/src/linting/` plus 351 `.weir` DSL files, surfacing as 820 individually user-toggleable rules across 15 thematic groups, 811 of them on by default. It is a domain where the artifact under construction is less a program than a curated, adversarially-maintained corpus of linguistic judgments, each of which a real user can see, disagree with, and switch off.

### Native complexity forms

- **Ambiguity guarding** — because English admits no ground-truth parse, a detector's match condition is rarely the hard part, and most accumulated structure is exclusion logic: context lookarounds (`match_to_lint_with_context` receives the token slices before and after the match), POS-set constraints, edit-distance bounds, and `Filter`/`UnlessStep` combinators whose only job is to suppress a construction the naive pattern would have caught.
- **A graduated authoring ladder** — the same conceptual rule can legitimately live at five different levels of mechanism (a tuple in the phrase-corrections table, an entry in the phrase-set many-to-many table, a JSON proper-noun entry, a `.weir` file, or a hand-written `ExprLinter`/`Linter` impl), so apparent structural variety across rules is often a deliberate cost-tier choice rather than inconsistency.
- **A statistical substrate under symbolic rules** — POS tags and chunk boundaries arrive from trained models (`harper-brill/trained_tagger_model.json`, `trained_chunker_model.json`), so rules inherit upstream tagger error and often carry structure that exists solely to be robust to a mistagged token.
- **Dialect and register variance** — correctness is parameterized by a `Dialect` bitflag (American, Canadian, Australian, British, Indian) plus per-word dictionary metadata, so a single "rule" frequently fans out into dialect-conditional branches and dialect-pinned snapshot fixtures.
- **Host-format multiplexing** — the prose being checked is usually embedded in something else (Markdown, Org, HTML, TeX, Typst, AsciiDoc, source-code comments, commit messages), and the `parsers/` and `mask/` layers plus a dozen sibling crates exist to isolate English from its carrier without shifting the character offsets rules depend on.
- **Suggestion mechanics as a separate problem from detection** — finding an error and producing a safe, non-destructive edit are distinct burdens; `Suggestion::replace_with_match_case` and the casing/span machinery mean a correct detector can still owe substantial code to emit an edit that preserves the author's capitalization and surrounding text.
- **Cross-rule arbitration** — rules are independent by construction but overlap in practice, so `Lint` carries a `priority: u8` (lower is more important) and a `spanless_hash`, and the documented CLI behavior of showing only the first of two overlapping lints is a known consequence contributors are told to design around.
- **Performance as a functional requirement** — the project states outright that long lint times are treated as bugs, which legitimizes structure that exists only for cost: the `insert_expr_rule` vs `insert_struct_rule` split exists so expression-based rules can share the framework's caching.
- **An obligatory negative surface** — every rule owes not just examples it must catch but a body of text on which it must stay silent, and that obligation is itself carried in the artifact (924 `assert_no_lints` call sites, 450 `allows` lines in the Weir corpus).

### What warrant looks like here

Structure earns its place in this domain when it can be traced to a specific text the engine would otherwise mishandle. The local currency is the false positive: a rule that fires on correct prose costs more than a rule that misses an error, because it interrupts a writer mid-thought and trains them to distrust or disable the checker — which is why the repository maintains distinct `false-positive` and `false-negative` issue labels, and why the production feedback loop routes user "this was wrong" reports back to a per-lint-ID tally so maintainers can publish "challenge" lint IDs for the worst offenders. Consequently a guard clause, an extra alternative in an expression, or a context lookaround is warranted by exhibiting the sentence it rescues, normally as a test case committed alongside it; conversely, structure that no test distinguishes from its absence has not met the local bar, however reasonable it reads. The second standard is placement on the authoring ladder: mechanism heavier than the linguistic phenomenon requires is disfavored, and the contributor documentation explicitly routes simple phrase substitutions away from Rust and into the declarative tables or Weir, so a hand-written trait impl is warranted by showing what the declarative tiers could not express — variable context, POS dependence, conditional messages, or casing-sensitive edits. Third, because rules are user-facing and individually switchable, each one owes a stable public identity: a registered name, a `description` written for a settings menu, a `LintKind` taxonomy assignment, and an entry in the curated default configuration. Structure that changes observable output must additionally reconcile with the committed snapshots, which is the domain's mechanism for making any behavioral drift visible rather than arguable. Finally, warrant is bounded by cost: this system's stated position against LanguageTool is latency and memory, so structure whose benefit is real but whose price is paid on every document by every user is held to a stricter standard than structure that only runs when a cheap pattern has already matched.

### Evidence channels

- `harper-core/src/linting/` — the per-rule modules, each conventionally carrying its own `#[cfg(test)] mod tests` block; 5,295 `#[test]` attributes across the directory, which is where a rule's claimed behavior is actually pinned.
- `harper-core/src/linting/weir_rules/*.weir` — declarative rules whose `test "input" "expected"` and `allows "..."` lines put the positive and negative surface in the same file as the rule; 1,838 `test` lines and 450 `allows` lines.
- `harper-core/src/linting/mod.rs` (the `pub mod tests` block, ~line 414 onward) — the shared assertion vocabulary (`assert_no_lints`, `assert_lint_count`, `assert_suggestion_result`, `assert_not_in_suggestion_result`, `assert_good_and_bad_suggestions`, `assert_lint_message`), which reveals what kinds of claims this domain considers checkable.
- `harper-core/tests/text/` with snapshots in `tests/text/linters/` and `tests/text/tagged/` — whole real documents (literary and legal prose, plus a dialect-pinned `Spell.US.md`) whose full lint and POS output is committed, so any behavioral change surfaces as a diff; regenerated via `just run-snapshots`.
- `harper-core/tests/test_sources/` — a regression corpus whose filenames are issue and PR numbers (`issue_2054.md`, `pr_504.md`), giving a direct join from a fixture back to the reported failure that motivated it.
- `harper-core/default_config.json` — the 15-group, 820-rule curated surface with each rule's default state, label, and group description; enumerable without building via `just ls-config verbose`.
- `gh api repos/Automattic/harper/issues` filtered on the `false-positive`, `false-negative`, `agreement`, `regionalism`, and `language-and-dialect` labels — the external record of which detectors misfired on real text.
- `just dogfood` — runs the built CLI over the repository's own Rust sources, exercising the comment-extraction path against text nobody wrote as a test.
- `harper-core/benches/` and `fuzz/` — the cost and robustness channels, relevant because latency is treated as correctness here.
- `packages/web/src/routes/docs/contributors/author-a-rule/+page.md` and `.../testing-strategy/+page.md` — the maintainers' own statement of the authoring ladder and of what quality means locally, including the production-feedback and challenge-lint-ID mechanism.

### Vocabulary

| Term | What it denotes in this domain |
|---|---|
| Lint | A single found error instance: a char `Span`, a `LintKind`, a user-facing `message`, a `priority`, and zero or more `Suggestion`s. |
| Linter | The general trait for anything that queries a `Document` and returns lints; the widest and least constrained way to write a rule. |
| `ExprLinter` | The narrower framework trait: supply an `Expr`, receive matched token slices, map them to a lint; gets a blanket `Linter` impl and framework caching. |
| Expr | A declarative combinator describing which window of tokens satisfies a criterion — sequences, alternatives, optionals, repetition, anchors, filters, negative steps. |
| Pattern | A reusable predicate over a single token or short span (POS-set membership, nominal phrase, modal verb, edit-distance proximity) used as a step inside an `Expr`. |
| Weir | The in-repo rule DSL: `expr`/`let`/`test`/`allows` files that compile to rules without Rust, intended to let organizations encode their own style guides. |
| `allows` | A Weir negative assertion — a sentence the rule must *not* fire on; the DSL-level counterpart to `assert_no_lints`. |
| Suggestion | A machine-applicable edit (`ReplaceWith`, `InsertAfter`, `Remove`), often case-matched to the original so the fix preserves the author's capitalization. |
| `LintKind` | The user-facing taxonomy assigned to each lint — including `Agreement`, `Capitalization`, `Eggcorn`, `Malapropism`, `Nonstandard`, `Redundancy`, `Regionalism`, `Typo`, `WordChoice`, `BoundaryError`. |
| Lint ID | The short stable rule name that ties a suggestion back to the code that produced it; the unit of user configuration and of production false-positive tallies. |
| `LintGroup` | The composed collection of all registered rules, constructed curated-and-dialect-aware, and the object integrations actually run. |
| Chunk / Sentence | The two document iteration units a rule may declare — a clause between commas, or a full sentence — determining how much context the expression can span. |
| Document | The parsed input: source chars plus a token stream carrying kind, POS metadata, and dictionary metadata. |
| Dialect | The English variety parameter (American, Canadian, Australian, British, Indian), held as bitflags and guessable from a document. |
| Mask / Parser | The layer that isolates prose from its carrier format (Markdown, Org, comments, markup) without disturbing the character offsets lints are reported in. |
| Curated | The maintainer-blessed default set — of dictionary, of rules, of enabled states — as distinct from a user's customized configuration. |
| Challenge lint ID | A rule publicly flagged as producing an outsized share of user-reported bad suggestions, offered as high-value contributor work. |
| Snapshot | Committed full output (lints or POS tags) for a whole document, whose diff is the domain's tripwire for unintended behavioral change. |
| Dogfood | Running the checker over this repository's own source comments as an unscripted test corpus. |

### Uncovered

- The runtime behavior of any rule: I read only, and `cargo`, `just`, `pnpm`, and `npm` were out of bounds, so every count here is static (file counts, `#[test]` attribute counts, config entries) and no claim rests on observed engine output.
- The production false-positive telemetry itself — the per-lint-ID tallies POSTed to `writewithharper.com` live on a maintainer-side backend, not in the repository, so I could characterize the loop's existence and purpose but not its contents or the current challenge list.
- The full 4,460-commit and 2,266-PR history: I sampled the issue record through label queries and the `issue_NNN.md` / `pr_NNN.md` fixture names rather than reading the history, since the task asked for the domain's shape rather than its chronology.
- The trained tagger and chunker model files were noted as a substrate but not inspected; their contents are numeric and would not have changed the characterization.
- Which unit is under examination remains unknown to me by design, and I did not attempt to narrow it — the largest and smallest rule modules were deliberately left unnamed.
