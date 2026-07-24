## C5 — The Lexicon: Word Existence, Word Knowledge, and Correction Ranking
*Charter: how a word is declared to exist, what the engine records about it, how a misspelling becomes a ranked correction list, and how user vocabulary composes with the curated core — excluding the grammar rules that consume word metadata and the part-of-speech tagger that writes into it.*

- **T1 — essence.** A speller answers three questions: does this token exist, what else is known about it, and if it does not exist what was meant. Existence is membership in a finite lexicon that must ship offline yet answer per token. Knowledge is a record attached to each entry — inflection, register, region, letter-case shape — because downstream rules need more than a yes. Correction is nearest-neighbour search under an edit metric, then re-ranked by priors the metric cannot see. And the lexicon is never one list: a curated core must compose with what the writer adds.

- **T2 — current machinery.** A `Dictionary` trait (`spell/dictionary.rs`) with four implementors. `MutableDictionary` stores a `WordMap` — `HashMap<WordId, WordMapEntry>` keyed by a case-folded hash. Curated data is `dictionary.dict` plus `annotations.json`, parsed by the `rune` module and affix-expanded by `AttributeList::expand_annotated_word`. `FstDictionary` wraps that with an `fst::Map` searched by a Levenshtein automaton; `MutableDictionary` falls back to Wagner-Fischer in `edit_distance.rs`. `score_suggestion` re-ranks. `DictWordMetadata` carries part-of-speech, `DialectFlags`, `OrthFlags`. `MergedDictionary` layers curated under user dictionaries. `harper-thesaurus` supplies synonyms.

- **T3 — with receipts.** `spell/` is 3,096 LOC across 15 files, 75 `#[test]`; `dict_word_metadata.rs` is 2,056 LOC with 156. `dictionary.dict` is 786,704 bytes and 54,669 entries (49,577 at `9291165c` 2024-01-20); `annotations.json` is 17,315 bytes, 25 affix flags, 54 properties. FST landed `d9a159d8` 2024-10-06 (PR #258); hash lookup `e48fb630` 2025-03-13, `hunspell`→`rune` `4829e0b7`, dialects `2e4445fc` — all PR #925. Scoring: `99e77c4f` 2025-03-07 (PR #844). Five dialects; Indian `f45addc4f` 2025-12-31 (#2397).

- **T4 — the frontier.** `MergedDictionary`'s doc says first-inserted wins (`merged_dictionary.rs:14`), but `get_word_metadata` has merged every child since `0d4feee7` (PR #1922, 2025-09-15). `WordId` stores only a 64-bit hash (`word_id.rs:14`); `WordMap::insert` overwrites by id, so canonical spelling is last-write-wins — the mechanism behind issue #2411. `FstDictionary` materializes the wordlist three ways (`fst_dictionary.rs:18-25`, issue #3725). `edit_distance()`, `get_word_from_id`, `find_words_with_prefix`, `WordMap::contains_str`/`with_capacity` have no non-test caller. `rune/mod.rs:114` lost its `#[test]`.

- **T5 — future plans.** Proposed, not built: PR #3351 (2026-05-11) adds Metaphone phonetic matching to suggestions, +359/−4 over 5 files. Issue #3347 proposes replacing the additive score with multiplicative weights, calling the present scheme a code smell. PR #2630 (2026-01-30) is a breaking rework of dictionary case-sensitivity, +1,262/−1,074 over 49 files. PR #2879 would spell-check compounds whose parts are absent; PR #3194 relaxes apostrophe matching; draft PR #2133 adds `harper-cli dictionary-normalize`. Issues #115 and #3092 request multi-word and hyphenated user entries.

*Status ledger:* FST curated lookup + Levenshtein-automaton fuzzy match — **shipped** · hash-keyed `WordMap` — **shipped** · Rune affix expansion (25 flags, 54 properties) — **shipped** · additive `score_suggestion` re-ranking — **shipped** · five-dialect `DialectFlags` + document dialect guessing — **shipped** · nine-flag `OrthFlags` — **shipped** · `MergedDictionary` four-layer composition (curated/user/workspace/file) — **shipped** · `TrieDictionary` prefix search — **shipped** (one consumer, `SplitWords`) · thesaurus synonyms — **shipped** (one consumer, `BoringWords`, five trigger words) · Wagner-Fischer `edit_distance_min_alloc` — **shipped** (user dictionaries only; curated path uses the DFA) · `Dictionary::get_word_from_id` — **shipped-but-unreachable** · `Dictionary::find_words_with_prefix` — **shipped-but-unreachable** · `edit_distance::edit_distance` wrapper — **shipped-but-unreachable** (module is private, so not public API either) · `WordMap::contains_str`, `WordMap::with_capacity` — **shipped-but-unreachable** · full-line-comment expansion test — **shipped-but-unreachable** (missing `#[test]`) · `harper-cli audit-dictionary` — **shipped** (gated in `justfile:437`) · Metaphone phonetic suggestions — **proposed** (PR #3351) · weight-based suggestion ranking — **proposed** (issue #3347) · explicit dictionary case-sensitivity — **proposed** (PR #2630) · compound spell-check — **proposed** (PR #2879) · `harper-dictionary-parsing` crate — **retired** (`1cd50d60` 2024-10-30, undone by `a7ffd4fb` 2024-11-14) · `FullDictionary` — **retired** (renamed `b84d105c`, PR #658) · `hunspell` module name — **retired** (`4829e0b7`) · `affixes.json` — **retired** (`92b964d0`, PR #1504) · `WordMetadata` — **retired** (renamed `88dbd058`, PR #1572)

*Entity ledger:*

| Entity | Tier | Locator |
|---|---|---|
| `Dictionary` trait (15 methods) | T2 | `harper-core/src/spell/dictionary.rs:12-57` |
| `MutableDictionary` | T2 | `harper-core/src/spell/mutable_dictionary.rs:25` |
| `FstDictionary` | T2 | `harper-core/src/spell/fst_dictionary.rs:18-25` |
| `MergedDictionary` | T2 | `harper-core/src/spell/merged_dictionary.rs:17` |
| `TrieDictionary` | T2 | `harper-core/src/spell/trie_dictionary.rs:13` |
| `WordMap` / `WordMapEntry` | T2 | `harper-core/src/spell/word_map.rs:9,14` |
| `WordId` (64-bit case-folded hash) | T2 | `harper-core/src/spell/word_id.rs:14-26` |
| `rune` module (Rune word-list format) | T2 | `harper-core/src/spell/rune/mod.rs` |
| `parse_word_list` (count header, `#` comments, `/` flags) | T2 | `harper-core/src/spell/rune/word_list.rs:13-54` |
| `AttributeList::expand_annotated_word` | T2 | `harper-core/src/spell/rune/attribute_list.rs:56-204` |
| `Matcher` (simplified regex for affix conditions) | T2 | `harper-core/src/spell/rune/matcher.rs:9-70` |
| `DictWordMetadata` | T2 | `harper-core/src/dict_word_metadata.rs:20-56` |
| `score_suggestion` / `order_suggestions` | T2 | `harper-core/src/spell/mod.rs:295-390` |
| `suggest_correct_spelling` | T2 | `harper-core/src/spell/mod.rs:394-406` |
| `edit_distance_min_alloc` (two-row Wagner-Fischer) | T2 | `harper-core/src/edit_distance.rs:6-39` |
| `SpellCheck` linter (LRU 10,000; `MAX_SUGGESTIONS = 3`) | T2 | `harper-core/src/linting/spell_check.rs:13-67` |
| `IrregularNouns` / `IrregularVerbs` | T2 | `harper-core/src/irregular_nouns.rs:8`, `irregular_verbs.rs` |
| `get_plurals` / `get_singulars` (dictionary-validated) | T2 | `harper-core/src/regular_nouns.rs:5-27` |
| `starts_with_vowel` / `InitialSound` | T2 | `harper-core/src/indefinite_article.rs:10-21` |
| `harper_thesaurus::Thesaurus` | T2 | `harper-thesaurus/src/thesaurus.rs:31-96` |
| `thesaurus_helper::get_synonym_replacement_suggestions` | T2 | `harper-core/src/thesaurus_helper.rs:57-64` |
| `harper-dictionary-wordlist` (`load_dict` / `save_dict`) | T2 | `harper-dictionary-wordlist/src/lib.rs:13-73` |
| Four-layer merge order: curated → user → workspace → file | T2 | `harper-ls/src/backend.rs:203-225` |
| `dictionary.dict`: 786,704 B, 54,669 entries, header `54800` | T3 | `harper-core/dictionary.dict:1` |
| `annotations.json`: 17,315 B, 25 affixes, 54 properties | T3 | `harper-core/annotations.json` |
| `EXPECTED_DISTANCE = 3`, `TRANSPOSITION_COST_ONE = true` | T3 | `harper-core/src/spell/fst_dictionary.rs:27-28` |
| Damerau transposition cost lowered to one | T3 | `d56bd72b` 2025-09-11 (PR #1899) |
| Back-off search: distances 2,3,4; `result_limit` 200 | T3 | `harper-core/src/linting/spell_check.rs:44-46` |
| `Dialect` enum (5 variants) + `try_from_bcp47` | T3 | `harper-core/src/dict_word_metadata.rs:1048-1094` |
| `DialectFlags` (u8 bitflags) + document dialect guessing | T3 | `harper-core/src/dict_word_metadata.rs:1128-1215` |
| Dialect-tagged base entries: US 151, GB 1,219, CA 504, AU 1,233, IN 1,225 | T3 | `harper-core/dictionary.dict` × `annotations.json` properties `<`, `!`, `@`, `_`, `₹` |
| `OrthFlags` (9 flags, u16 backing) | T3 | `harper-core/src/dict_word_metadata_orthography.rs:6-49` |
| Roman-numeral orthography flag | T3 | `fbab9880` 2025-09-09 (PR #1851) |
| Letter-case flags added to word metadata | T3 | `569d6162` 2025-07-24 (PR #1578) |
| `VerbFormFlags` (6 forms) | T3 | `harper-core/src/dict_word_metadata.rs:827-841` |
| `irregular_nouns.json` 163 pairs; `irregular_verbs.json` 135 | T3 | `harper-core/irregular_nouns.json`, `irregular_verbs.json` |
| `thesaurus.txt` 30,259 entries / 24,822,771 B; `word-freq.txt` 22,297 lines | T3 | `harper-thesaurus/thesaurus.txt`, `word-freq.txt` |
| zstd build-time thesaurus compression | T3 | `harper-thesaurus/build.rs:20-27` |
| `harper-thesaurus` birth | T3 | `50490b8c` 2026-01-13 (PR #2085) |
| FST-based curated spellchecking | T3 | `d9a159d8` 2024-10-06, PR #258 merged 2024-11-23 |
| `MutableDictionary` word-hash lookup | T3 | `e48fb630` 2025-03-13 (PR #925) |
| Scoring replaced shuffling for suggestions | T3 | `99e77c4f` 2025-03-07 (PR #844) |
| Blank lines and `#` comments allowed in `dictionary.dict` | T3 | `0c9b2204` 2025-03-13 (PR #756) |
| Suggestion-score tuning passes | T3 | `e4955aeb` 2025-11-13 (#2189); `150656ee` 2025-12-02 (#2288); `2cdaf158` 2026-03-17 (#2927) |
| Lowercase-DFA skip + `spellcheck` bench | T3 | `0fe03c35` 2026-03-30 (PR #3025), `harper-core/benches/spellcheck.rs` |
| `harper-cli audit-dictionary` (duplicate/unknown/unused flags) | T3 | `harper-cli/src/main.rs:730-848`; `justfile:437,866` |
| `MergedDictionary` doc/behavior divergence | T4 | `merged_dictionary.rs:14` vs `:96-118`; changed by `0d4feee7` (PR #1922) |
| Case-fold collision / last-write-wins canonical spelling | T4 | `word_id.rs:20-26`, `word_map.rs:67-71`; issue #2411 |
| Wordlist materialized 2–3× in `FstDictionary` | T4 | `fst_dictionary.rs:18-25`; issue #3725 |
| `Dictionary::get_word_from_id` — no caller | T4 | `spell/dictionary.rs:50` |
| `Dictionary::find_words_with_prefix` — no non-test caller | T4 | `spell/dictionary.rs:53` |
| `edit_distance()` wrapper — no non-test caller, private module | T4 | `edit_distance.rs:41`; `harper-core/src/lib.rs:11` |
| `WordMap::contains_str`, `WordMap::with_capacity` — no caller | T4 | `word_map.rs:28,89` |
| Dormant test (missing `#[test]`) | T4 | `harper-core/src/spell/rune/mod.rs:114` |
| Stale `u8` comment over a `u16` type | T4 | `dict_word_metadata_orthography.rs:27-30` |
| Open metadata TODOs (abstract nouns, non-personal pronouns, positive degree) | T4 | `dict_word_metadata.rs:872,905,1918` |
| All-caps suggestions degraded | T4 | issue #1419 (2025-06-20) |
| User-added word not recognized with `'s` | T4 | issue #3875 (2026-07-23) |
| Dictionary-member words still flagged | T4 | issues #2585, #3043, #2725 |
| `im` → `I'm` missing from suggestions | T4 | issue #3184 (2026-04-16) |
| Metaphone phonetic suggestion matching | T5 | PR #3351 (2026-05-11, +359/−4, 5 files) |
| Weight-based rather than additive suggestion ranking | T5 | issue #3347 (2026-05-11) |
| Explicit dictionary case-sensitivity (breaking) | T5 | PR #2630 (2026-01-30, +1,262/−1,074, 49 files) |
| Compound spell-check with unknown parts | T5 | PR #2879 (2026-03-06) |
| Case-insensitive apostrophe diff for contractions | T5 | PR #3194 (2026-04-16) |
| `harper-cli dictionary-normalize` (draft) | T5 | PR #2133 (2025-11-04) |
| Multi-word and hyphenated user-dictionary entries | T5 | issues #115 (2024-08-22), #3092 (2026-04-02) |
| Per-programming-language dictionaries | T5 | issue #2451 (2026-01-09) |
| Broader synonym suggestions | T5 | issue #2035 (2025-09-30) |
| Transitivity and abstract-noun marking in the dictionary | T5 | issues #2773, #2772 (2026-02-22) |

*Trellis-relevant observation:* The reusable shape is the two-stage retrieve-then-rerank split — a cheap automaton finds every candidate within an edit budget, and a separate, readable scoring function encodes the priors (first letter rarely mistyped, dialect variants, apostrophe forms) that the metric cannot express; the priors are editable without touching the index. The reusable failure is `WordId`: keying a store by a lossy 64-bit case-folded hash makes two entries silently one, and the surviving canonical form depends on insertion order — a real defect (issue #2411) that a personalized system merging user vocabulary into a curated core would inherit exactly. Worth copying too: user layers add existence but carry no metadata, so composition is a union in which the curated layer wins every scalar field — precedence that is explicit in code rather than implied.

## Uncovered
- The expanded (post-affix) word count of the shipped dictionary. Only the 54,669 base entries in `dictionary.dict` are countable statically; the runtime `word_count()` is the size of the expanded `WordMap`, and deriving it requires running `harper-cli words`, which the read-only boundary forbids.
- The compressed size of the embedded thesaurus. `build.rs:23-24` annotates 3.84 MiB at max level and 7.02 MiB at level 4, but those are comments in the source, not verified artifact sizes, and the artifact is only produced by a build.
- Whether the flagged unreachable items (`get_word_from_id`, `find_words_with_prefix`, `WordMap::contains_str`) are consumed by any downstream crate outside this repository. They sit on public types, so reachability was assessed within the workspace only.
- The `packages/` TypeScript surface for user dictionaries (browser extension, Obsidian, VS Code). Several open issues (#2749, #3662, #2624) concern where those store words; the Rust-side merge was traced, the JS-side storage was not.
