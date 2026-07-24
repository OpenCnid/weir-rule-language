# Shared ground — harper density-trellis cartography

You are one of nine sibling cartographers. You cannot see the others and they cannot see you.
Cross-cutting judgment belongs to the orchestrator, not to you. Report only your own class.

## The subject

A local clone of the `Automattic/harper` repository sits at:

```
C:/Users/Darian/AppData/Local/Temp/claude/D--trellis-engine--claude-worktrees-exciting-gould-08c722/a81c86a8-d2bb-4451-821a-64d1b5de32f2/scratchpad/harper
```

Harper is an offline, privacy-first English grammar checker written in Rust. It is Apache-2.0,
12,312 stars, 457 forks, homepage writewithharper.com. The GitHub repo is `Automattic/harper` and
`gh` is authenticated, so `gh api` and `gh pr` work against it for PR and issue archaeology.

## Repository-level facts already verified — do not re-derive these

- 4,460 commits, first `57b90e33` (2023-10-19, "Some stuff??"), most recent at clone time
  `efa59c33` (2026-07-24). 226 release tags, latest `v2.6.0`.
- 135 distinct authors. Top: Elijah Potter 2,409 commits, Andrew Dunbar 740, hippietrail 444,
  dependabot 334, Grant Lemons 267, Matthew Espino 118.
- 2,266 pull requests: 1,924 merged, 220 closed-unmerged, 122 open. 561 open issues, 940 closed.
- Commits per quarter: 2023-Q4 8 · 2024-Q1 182 · 2024-Q2 38 · 2024-Q3 163 · 2024-Q4 421 ·
  2025-Q1 1,636 · 2025-Q2 631 · 2025-Q3 339 · 2025-Q4 282 · 2026-Q1 388 · 2026-Q2 317 · 2026-Q3 55.
- Conventional-commit type distribution: feat 1,252 · fix 890 · build 384 · chore 262 · docs 160 ·
  refactor 139 · test 61 · hotfix 22 · style 14 · perf 11.
- Exactly two `!` breaking-change commits in the whole history, both 2026-03-30:
  `90bc5436 refactor!: take argument by value instead of mut ref (#3051)` and
  `2b5c8cd3 refactor(core)!: Lrc<[char]> instead of Lrc<Vec<char>> (#3060)`.
- Cargo workspace members: harper-cli, harper-core, harper-ls, harper-comments, harper-wasm,
  harper-tree-sitter, harper-html, harper-literate-haskell, harper-typst, harper-stats,
  harper-pos-utils, harper-brill, harper-ink, harper-python, harper-jjdescription,
  harper-thesaurus, harper-asciidoc, fuzz, harper-tex, harper-desktop/src-tauri, harper-git-commit.
- pnpm packages: chrome-plugin, components, harper-editor, harper.js, lint-framework,
  obsidian-plugin, vscode-plugin, web, wordpress-plugin.
- Subsystem birth commits (first commit touching the path):
  `harper-core/src/linting` and `spell` 2024-01-15 `309d840e`; `harper-ls` 2024-01-17 `dd0e4de2`;
  `mask` 2024-07-14 `676527ea`; `patterns` 2024-09-01 `6107594e`; `harper.js` 2024-12-15 `47ba722c`;
  `harper-stats` 2025-01-23 `1f113f46`; `chrome-plugin` 2025-05-02 `a2e0da7a` (#1072);
  `expr` 2025-06-13 `a8fb0c6d` (#1393, "Pattern -> Expr"); `harper-brill` + `harper-pos-utils`
  2025-06-16 `db89187c` (#1344); `harper-ink` 2025-09-26 `690100cf` (#1894);
  `harper-thesaurus` 2026-01-13 `50490b8c` (#2085); `weir` 2026-01-12 `46f4547f` (#2357);
  `weirpack` 2026-02-03 `3a5cd68b` (#2491); `harper-desktop` 2026-05-12 `f96274e2` (#3324).
- harper-core is ~105,805 lines of Rust. `harper-core/src/linting/` holds 300 `.rs` files.
  351 `.weir` files exist in the tree. The Weir implementation is 2,491 LOC across
  `weir/{ast.rs 212, error.rs 27, mod.rs 699, optimize.rs 61, parsing/expr.rs 505,
  parsing/mod.rs 498}` and `weirpack/{error.rs 25, manifest.rs 82, mod.rs 244}`.
- The repo ships `AGENTS.md` (265 lines) and `AGENT_POLICY.md` (35 lines, a verbatim copy of the
  maintainer's blog post setting policy on LLM-authored PRs). `ARCHITECTURE.md` and
  `CONTRIBUTING.md` are 3-line redirects to writewithharper.com.

## Method — chain of density, system mode

Chain of density (Adams et al. 2023, arXiv:2309.04269) rewrites one summary five times **at a fixed
length**, fusing new entities each pass by compressing what is already there. Fixed length is the
engine: without it, "add detail" produces a longer summary, never a denser one.

You are writing **one branch** of a density-trellis: a five-tier chain covering exactly one subsystem
class. The tiers traverse time:

- **T1 — essence.** The invariant idea, as it would be true of any system solving this problem.
  No proper nouns from this repo unless the name *is* the idea.
- **T2 — current machinery.** What is actually built and shipped, named concretely: files, types,
  functions, entry points.
- **T3 — with receipts.** The same story again with exact numbers, commit SHAs, PR numbers, dates,
  LOC counts, test counts. This is the tier where every claim carries an address.
- **T4 — the frontier.** What is unfinished, inconsistent, unreachable, or known-broken *right now*.
  Open issues, TODOs, code with no non-test caller, documented review findings, known false-positive
  classes. Findings, not accusations.
- **T5 — future plans.** What is proposed but not built: open PRs, roadmap issues, maintainer
  statements of direction. Label clearly as proposed.

**Hold ~90 words per tier.** Every tier is conceptually complete on its own terms; T2–T5 *add*
entities, they never *correct* a shallower tier.

## Binding constraints

1. **The repository is the source that wins.** Reverse-engineer from `git log`, the code, and the
   PR record. Never from memory or from what a grammar checker "usually" does. If you cannot locate
   a capability, do not write it.
2. **Exact numbers with locators, or nothing.** Every quantitative claim carries a `path:line`, a
   commit SHA, or a PR number. Never round, never estimate, never fill a number in from memory.
3. **Status labels are load-bearing.** Distinguish `shipped` (committed code, reachable, tested) from
   `shipped-but-unreachable` (no non-test caller) from `proposed` (open PR or issue only) from
   `retired`. Blurring them is the failure this format exists to prevent.
4. **Own words.** At most one short attributed quote (under 15 words, in quotation marks) in your
   whole branch. Never paste a function body, table, or passage as your prose.
5. **Reachability is reported separately from correctness.** Correct is not the same claim as
   reachable. If a type or function has no non-test caller, that belongs in T4.
6. **Read-only on the harper clone.** Do not modify, build, format, or run any harper code. `git log`,
   `git show`, `gh api`, `grep`, and file reads only. Never run `cargo`, `pnpm`, `just`, or `npm`.
