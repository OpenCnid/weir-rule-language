## C9 — The Contribution Machine: Policy, Task Runner, CI, and the Review Gate

*Charter: the social and mechanical apparatus that converts an outside patch — including one written by a model — into a merged commit; the code being contributed is out of scope.*

- **T1 — essence.** A project taking patches from strangers must convert unverified intent into trusted commits at a cost that does not grow with contributor count. Three levers carry it: publish the rules where humans and machines both read them; make every gate runnable by the contributor before submission, so reviewers spend attention on judgment rather than mechanics; and vest merge authority in a named person who can be held responsible. Machine-written patches add a fourth — provenance disclosure — because reviewers must allocate scrutiny by how a patch was produced, not only by what it changes.

- **T2 — current machinery.** Two root files carry policy: `AGENT_POLICY.md`, a verbatim maintainer blog post, and `AGENTS.md`, a route map plus rule-authoring instructions. One `justfile` is the whole tooling surface; `.github/workflows/just_checks.yml` fans its task names across a CI matrix, and `merge_group` triggers route merges through a queue. `.github/pull_request_template.md` adds an AI Disclosure checkbox block and a test-provenance block. `harper-core/tests/snapshot.rs` diffs generated output against committed `.snap.yml` baselines; `fuzz/` holds `cargo-fuzz` targets; `contributors/committer` vests merge authority; `stale.yml` closes inactivity.

- **T3 — with receipts.** The `justfile` (973 lines) defines 63 recipes and 30 aliases; CI runs nine (`just_checks.yml:19-30`). 6,090 `#[test]` functions exist, 5,976 in harper-core, plus 1,838 inline tests across 351 `.weir` files, 34 macro-built corpus tests (`run_tests.rs`), 64 Playwright tests across 23 specs, and 20 snapshot baselines over 10 corpus documents. `AGENTS.md` was born 2026-02-18 (`463533a6c`, #2751) at 143 lines, now 265. `AGENT_POLICY.md` landed 2026-06-30 (`8d48e6b8f`, #3738); AI-disclosure checkboxes 2026-05-15 (`591c524ee`, #3375).

- **T4 — the frontier.** Disclosure is unenforced — no workflow reads the checkbox. Of 227 merges after the template landed, 50 dropped the section and 6 left it blank; enforcement is manual and rare, four closures citing the policy (#3196, #3425, #3431, #3610), Elijah Potter writing "I am closing this PR for violating the agent policy." `committing/+page.md:10` still claims CI runs `just precommit`, retired 2025-10-01 (`bb2af3ca1`, #2037). `cargo-fuzz` appears in no workflow or recipe. `snapshot.rs:67` rewrites its baseline before failing. Median `.weir` file: 2 tests.

- **T5 — future plans.** Proposed, not built. Issue #3473 (2026-05-22, labels `ci`, `harper-cli`) asks for a published GitHub Action wrapping `harper-cli`, turning the project's own checker into other repositories' CI. Issues #3242 and #3337 (both labelled `justfile`, `good first issue`) propose `ls-linters` and a wrong-preposition tool as new recipes, continuing the pattern of growing the runner surface rather than adding loose scripts. PR #2241 (open since 2025-11-25, +428/-0) proposes a consistency check over the linter registry. `AGENTS.md:15` asks humans to migrate agent guidance into the website; unstarted.

*Status ledger:* `AGENT_POLICY.md` in-repo — **shipped** · AI Disclosure checkbox — **shipped-but-unenforced** · manual agent-policy closure — **shipped** · `justfile` as sole tooling surface — **shipped** · `just_checks.yml` 9-task matrix — **shipped** · merge queue (`merge_group`) — **shipped** · `just precommit` as the CI gate — **retired** (2025-10-01, `bb2af3ca1`) · snapshot baselines — **shipped** · `just fuzz` (quickcheck loop) — **shipped** · `cargo-fuzz` targets — **shipped-but-unenforced** (no CI or recipe caller) · 15-test floor for Weir rules — **shipped-but-unenforced** · committer review gate — **shipped** (social only; no CODEOWNERS) · stale bot 60/14 days — **shipped** · dependabot weekly with 7-day cooldown — **shipped** · `harper-cli` GitHub Action — **proposed** (#3473) · linter-registry consistency check — **proposed** (#2241)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `AGENT_POLICY.md` (35 lines, three rules: brief, grounded, honest) | T2 | `AGENT_POLICY.md:19,25,29` |
| `AGENTS.md` (265 lines) | T2 | `AGENTS.md`; born `463533a6c` / PR #2751 |
| `justfile` — 63 recipes, 30 aliases, 973 lines | T2 | `justfile`; born `66da0b27b` 2024-07-07 |
| `just_checks.yml` 9-task matrix | T2 | `.github/workflows/just_checks.yml:19-30` |
| Merge queue (`merge_group` trigger) | T2 | `.github/workflows/just_checks.yml:8` |
| AI Disclosure checkbox block (4 options) | T2 | `.github/pull_request_template.md`; `591c524ee` / PR #3375 |
| Test-provenance checkbox block | T2 | `.github/pull_request_template.md` ("If Your PR Implements or Enhances a Linter") |
| `snapshot_all_text_files` harness | T2 | `harper-core/tests/snapshot.rs:76` |
| `test_most_lints` / `test_pos_tagger` | T3 | `harper-core/tests/linters.rs:192`, `tests/pos_tags.rs:366` |
| 20 snapshot baselines over 10 corpus docs | T3 | `harper-core/tests/text/linters/`, `tests/text/tagged/` |
| 5 `cargo-fuzz` targets | T2 | `fuzz/Cargo.toml`; added `ad429ad0d` / PR #1949, 2025-11-19 |
| `just fuzz` = `QUICKCHECK_TESTS=100000 cargo test` loop | T3 | `justfile:644-653` |
| `register-linter` codegen recipe (sed-injects into `mod.rs`/`lint_group.rs`) | T3 | `justfile:655-664` |
| Committer role and 15-merged-PR heuristic | T2 | `packages/web/src/routes/docs/contributors/committer/+page.md:9,20` |
| Testing-strategy doc (risk-driven, "check" vs "testing") | T2 | `.../contributors/testing-strategy/+page.md`; `dd2f10fad` / PR #3845 |
| Reviewer playbook (Actions artifacts, `cargo install --git`, Docker) | T2 | `.../contributors/review/+page.md` |
| Production feedback loop → "challenge" lint IDs | T2 | `.../contributors/testing-strategy/+page.md:125` |
| Stale bot: 60 days stale, 14 to close | T2 | `.github/workflows/stale.yml:18-19` |
| Dependabot: cargo/npm/actions weekly, 7-day cooldown | T3 | `.github/dependabot.yml` |
| Toolchain pins: `stable` + wasm32 target; Node `lts/*`; biome 2.3.3 | T2 | `rust-toolchain.toml`, `.node-version`, `biome.json:2` |
| Nix devShell | T2 | `flake.nix` |
| Docker path used for review (web + demo) | T2 | `Dockerfile`; `.../contributors/review/+page.md:43-49` |
| Stale claim: "we run `just precommit` through GitHub Actions" | T4 | `.../contributors/committing/+page.md:10` (written `4901fc38d` 2025-01-16) |
| CI's precommit→matrix migration | T4 | `bb2af3ca1` 2025-10-01, PR #2037; workflow renamed `precommit.yml`→`just-checks.yml`→`just_checks.yml` |
| Self-overwriting snapshot baseline | T4 | `harper-core/tests/snapshot.rs:62-71` |
| Agent-only 15-test floor (absent from human `author-a-rule`) | T4 | `AGENTS.md:226,248` vs `.../contributors/author-a-rule/+page.md` (301 lines, no floor) |
| Policy-violation closures | T4 | PRs #3196, #3425, #3431, #3610 (+ #3434 closed for non-response) |
| Review doc cites "PR #445" but links `/pull/455` | T4 | `.../contributors/review/+page.md:30` |
| Absent: CODEOWNERS, labeler, disclosure-checking workflow | T4 | `.github/` (7 workflows, none of these) |
| `harper-cli` as a published GitHub Action | T5 | issue #3473 |
| `ls-linters` recipe; wrong-preposition recipe | T5 | issues #3242, #3337 |
| Linter-registry consistency test | T5 | PR #2241 |
| Migrate `AGENTS.md` guidance into the website | T5 | `AGENTS.md:15-16` |

*Sampling disclosure:* Four complete censuses, not random samples. (1) All 227 PRs merged 2026-05-18→2026-07-23 — every merge after the AI-disclosure template landed 2026-05-15 — fetched with full bodies and parsed for checkbox state. (2) All 220 closed-unmerged PRs (2024-03-04→2026-07-17) with full comment threads. (3) All 122 open PRs. (4) All 561 open issues. Repo totals at query time: 1,931 merged / 220 closed / 122 open. This census supports claims about disclosure behavior *in the post-template window only*; it cannot speak to the 1,704 merges before the template existed. It is also author-skewed: hippietrail authored 130 of 227 (57%), so the aggregate 85% non-bot section-retention rate (76% excluding him) reflects a small active core, not 135 authors. Enforcement counts derive from string-matching comment bodies for "agent polic", so silently-enforced cases are invisible; four is a floor, not a total.

*Trellis-relevant observation:* The reusable move is that harper turned a prose policy into a checkbox the contributor must physically edit — the disclosure rate is high (85% retention, 68/171 admitting AI involvement, 7 fully autonomous PRs merged) precisely because the template makes silence visible rather than default. The cautionary half is that no workflow reads that checkbox, so the whole apparatus rests on one maintainer noticing; four closures in 220 is enforcement by attention, which does not scale, and the same gap explains why an agent-only "at least 15 tests" instruction is met by 20% of post-instruction Weir rules. For a house prompt: an instruction with no reader is a wish, and the drift found here (`committing/+page.md` advertising a CI gate retired nine months earlier) argues for generating contributor docs from the workflow files rather than restating them.

## Uncovered
- Branch-protection settings and required-check configuration — readable only with repo admin scope; the merge gate described in `committer/+page.md` could not be verified against GitHub's actual enforcement.
- Review *latency* (time-to-first-review, merge lead time) was not computed; the closed-PR fetch captured lifetime but the merged-PR fetch did not carry `createdAt`.
- Whether the 122 open PRs include stalled agent-authored work was not characterized beyond title matching; PR bodies were not fetched for the open set.
- Discord, where `contributors/introduction/+page.md` routes questions, is off-record and outside the repository.
- Per-rule (as opposed to per-file) Weir test counts: 11 grouped directories under `weir_rules/` collapse several `.weir` files into one public rule, so the median-2-tests figure is per file and may understate per-rule coverage.
