# How agents consume and maintain this repo

This repo is a **study of someone else's system**. That single fact governs everything below.

## What this repo is

A system-mode chain-of-density map of [`Automattic/harper`](https://github.com/Automattic/harper),
reverse-engineered from its commit and PR record, plus the OpenCnid skill outputs that produced and
adjudicated it. The name points at **Weir**, harper's declarative rule language, because that is the
transferable finding — not because this repo is about grammar checking.

## The one-way rule, in its system-mode form

The paper-repo rule is *when a note and its paper disagree, the paper wins.* Here:

> **When this map and the harper source disagree, the harper source wins and the map gets fixed.**

Authority runs `harper source → this map → any downstream Trellis decision`, one direction only.
A capability you cannot locate at a `path:line`, a commit SHA, or a PR number does not go in.

## Do not do these things

- **Do not update the map from memory.** Re-clone or re-fetch harper and verify. Every number in
  `docs/density-chain/DENSITY-CHAIN.md` carries a locator precisely so it can be re-checked.
- **Do not open issues or pull requests on `Automattic/harper` from this repo's findings** without the
  owner saying so explicitly. The T4 sections name real defects in a real project; routing them
  upstream is a courtesy that belongs to a human, and harper's own `AGENT_POLICY.md` asks for a
  disclaimer and a grounded human need on any agent-authored PR.
- **Do not treat the T4 "frontier" sections as a grievance list.** They are dated observations against
  a moving target. Several will be stale within weeks; that is expected and is what the verification
  date is for.
- **Do not reuse the judge panels.** The convocation and judge-composition outputs in `findings/`
  record judges that were composed for one ceremony and are dead after it. Reusing them rebuilds the
  standing roster the house rolled back.

## Maintenance

The map is pinned to a clone state. To re-verify:

```bash
git clone --filter=blob:none https://github.com/Automattic/harper.git
```

Then walk `docs/density-chain/DENSITY-CHAIN.md` branch by branch. Each branch's status ledger uses a
closed label set — `shipped`, `shipped-but-unreachable`, `shipped-but-unenforced`, `proposed`,
`retired` — and those labels are load-bearing. A capability that moved from `proposed` to `shipped`
is a real change to record; a capability whose label you cannot re-derive is a defect in the map.

Update the frontmatter's verification date whenever you re-check, and say what moved.

## Structure

```
docs/density-chain/DENSITY-CHAIN.md    the map — ground truth
docs/density-chain/DENSITY-CHAIN.html  the interactive render — follows the markdown, never leads it
findings/                              the five skill outputs, in run order
findings/branches/                     the nine per-class cartographer returns, unedited
```

The HTML is generated from the markdown's content. **The markdown wins.** If you change one, change
both, and change the markdown first.
