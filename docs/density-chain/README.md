# The harper density-trellis

Two files, one artifact:

| File | Role |
|---|---|
| [`DENSITY-CHAIN.md`](DENSITY-CHAIN.md) | **Ground truth.** The map itself, in markdown, with every claim carrying a locator. |
| [`DENSITY-CHAIN.html`](DENSITY-CHAIN.html) | **The map.** A self-contained, theme-aware render of the same content. Follows the markdown; never leads it. |

**The markdown wins.** If the two disagree, the HTML has a defect. If the markdown and the harper
source disagree, the *markdown* has a defect. Authority runs one direction only:

```
harper source  →  DENSITY-CHAIN.md  →  DENSITY-CHAIN.html
```

## What a density-trellis is

[Chain of density](https://arxiv.org/abs/2309.04269) (Adams et al. 2023) rewrites one summary five
times **at a fixed length**, fusing in new entities each pass by compressing what is already there.
Fixed length is the engine — without it, "add detail" produces a longer summary, never a denser one.

A *trellis* is the second tier of that format: one shared **trunk** (the whole system at three
densities) plus one **branch per subsystem class**, each branch its own fixed-length five-tier chain,
plus a lattice of cross-links so the branches interlock instead of standing in parallel columns.

Because salience runs from the invariant to the specific, each branch's tiers traverse time:

| Tier | What it carries |
|---|---|
| **T1 — essence** | the invariant idea, true of any system solving this problem |
| **T2 — current machinery** | what is actually built, named by file and type |
| **T3 — with receipts** | the same story with exact numbers, SHAs, PR numbers, dates |
| **T4 — the frontier** | what is unfinished, unreachable, or known-broken *right now* |
| **T5 — future plans** | what is proposed but not built — open PRs and issues only |

Each branch is conceptually complete at every tier. T2–T5 **add** entities; they never **correct** a
shallower tier. Stop at the first tier that answers your question.

## Status labels are load-bearing

The branches use a closed label set, and blurring it is the failure this format exists to prevent:

- **`shipped`** — committed code, reachable from a non-test caller.
- **`shipped-but-unreachable`** — the code exists and may be correct, but nothing outside the test
  suite calls it. *Correct is not the same claim as reachable.*
- **`shipped-but-unenforced`** — a stated policy that nothing mechanically checks.
- **`proposed`** — an open PR or issue only. Nobody has committed to it.
- **`retired`** — was shipped, has been removed. Recorded because the removal is the finding.

## How it was made

Nine read-only sub-agent cartographers, one per class, each holding a byte-identical ground block and
a rigid return frame, none permitted to read another's output. Cross-class judgment — the trunk, the
cross-link lattice — belongs to the orchestrator, because a sibling speculating about a class it
cannot see produces exactly the unreconcilable claim the fan-out discipline is designed to prevent.

Full method, sampling disclosures, and honest gaps live in the map's own *Provenance & method*
section. Every branch also carries an `## Uncovered` list, so silence about a gap cannot be mistaken
for absence of one.
