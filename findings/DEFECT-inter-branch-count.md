# Defect found by the panel, in the published map

**Found by:** the judge panel's coherence seat, while ruling on P4. Not by me, and not by any
cartographer. Filed here so the correction is traceable to its finder.

## The inconsistency

Two branches state counts of the same population that cannot both be right:

| Branch | Claim |
|---|---|
| **C3** (Weir) | "only 89 meet the 15-test floor `AGENTS.md:226` demands" |
| **C4** (linter corpus) | "84.6% of `.weir` files (297/351) carry fewer than the 15 tests `AGENTS.md:225` requires" |

`89 + 297 = 386 > 351`. If 297 of 351 are *below* the floor, then 54 meet it — not 89.

## The reconciliation — recounted against the pinned tree, 2026-07-24

My first hypothesis was wrong. I assumed the split was **per-file vs per-rule-name** (C9 had
disclosed that 11 grouped directories collapse several files into one public rule). A recount shows
the denominator is not the variable at all — **the definition of "assertion" is**:

```
total .weir files ................................. 351
public rule names ................................. 328

counting `test` + `allows` together:
  meeting the 15-assertion floor .................. 89   (files)
  meeting the 15-assertion floor .................. 89   (rule names)
  below the floor ................................. 262  (files) / 239 (names)

counting `test` lines only:
  meeting the floor ............................... 54
  below the floor ................................. 297  (= C4's figure)

zero assertions of any kind ....................... 64   (files) / 62 (rule names)
total: 1,838 `test` lines + 450 `allows` lines
```

**Both branches were right about their own predicate and neither named it.** C3 counted `test` +
`allows` and got 89 meeting the floor. C4 counted `test` lines only and got 297 below it. The two
numbers describe different questions, and stating them without their definitions made them look like
a contradiction — which, as *written*, they were.

Note the denominator coincidence that hid the real cause: 89 files and 89 rule names both meet the
floor under `test`+`allows`, so the per-file/per-name distinction — the obvious suspect, and the one
C9 flagged — turns out to be irrelevant here.

## Standing of the surrounding claim

Note what this does **not** touch. The load-bearing number in the map's headline finding is
**"64 of 351 rules ship zero assertions"** — a different predicate (zero vs. fewer-than-fifteen) on a
stated denominator. The coherence seat said so explicitly when it declined to charge P4 for this:
*"a live inter-branch inconsistency, but on a different predicate than P4's."* The zero-assertion
finding stands; the floor-compliance figures do not.

## Action

1. Recount both figures against `efa59c33`, with the denominator named.
2. Correct C3 and C4 in `DENSITY-CHAIN.md`, and re-render the HTML.
3. Leave this file in the repo as the record of who caught it.

**This is the ceremony working as designed.** A panel composed blind to the candidate, judging a
claim cut from the map, found an error in the map that nine independent cartographers and the
orchestrator all missed.
