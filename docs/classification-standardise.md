# Standardise `Language.classification` from Glottolog

Proposal: set `classification` = the names of the language's Glottolog family-level
ancestors, joined with `", "` (the current format). Source: glottolog-cldf v5.4.

## Measured against current data (1081 languages)

| Outcome | n |
|---|---|
| Identical already | 538 |
| Would change | 472 |
| Glottolog gives no family (isolate) | 59 |
| No glottocode / code not in Glottolog | 11 / 1 |

Breakdown of the 472 changes:

- **Different root (228)**: mostly `Trans-New Guinea, …` → `Nuclear Trans New Guinea, …`.
- **Different branch (150)**: Glottolog has reshuffled or renamed subgroups, e.g. Siane
  `Trans-New Guinea, Kainantu-Goroka, Gorokan, Siane` → `Nuclear Trans New Guinea,
  Kainantu-Goroka, Goroka, Nuclear Goroka, Siane-Yagaria`.
- **TNG deeper (63)**: TNG has more structure than Glottolog, e.g. Sebe
  `Eastern Trans-Fly, Bine` → `Eastern Trans-Fly`. These may be deliberate
  expert edits, and overwriting would lose them.
- **Glottolog deeper (31)**: Glottolog adds levels.

The 59 isolates currently hold values like `Language isolate`, `Isolate`, `Central
Solomons`, or `Trans-New Guinea, Southeast Papuan, Goilalan, Fuyug`. Glottolog
would blank them.

## What it touches

`classification` is shown on language pages and in tables (`condense_classification`).
Clade filters use `classification__startswith` (`cognacy/views.py:124`,
`lexicon/.../write_table.py:66`), so filters and saved clade names keyed on
`Trans-New Guinea` stop matching. `Language` is reversion-registered, so a
`.save()` loop keeps history.

## Work

- Management command `sync_classification <cldf dir> [--apply]`: dry-run prints a
  diff, `--apply` saves within a revision. About 40 lines plus tests: **~2 hours**.
- Decisions, then reviewing the diff (yours): the 63 "TNG deeper" rows and the 59 isolates
  are where judgement is needed.

## Decisions needed

1. Should the 63 rows where TNG is more detailed be kept, overwritten, or skipped and listed?
	-> use the dry-run and --apply to check and review.
2. What should isolates get: blank, `Isolate`, or the language's own name?
	-> language name
3. Should this be a one-off or re-run on every Glottolog release? (A re-run overwrites hand edits each time.)
	-> every glottolog release.

## Languages skipped by the sync (no or bad glottocode)

| TNG slug | Proposed | Evidence | Confidence |
|---|---|---|---|
| magi-musak | `magi1243` Magi | Daniels 2016 Magɨ; Glottolog places it under Aisian (TNG's "Emuan") | high |
| kupera-pukwa | `kamo1255` Kamoro | Wollaston 1912; all 7 forms match Kamoro (otiri/utiri, aměta/amata, uweri/uwiri) | high |
| mohr | `morm1235` Mor (Mor Islands) | 4/5 numerals identical to TNG `mor-austronesian` | high |
| mowata | `sout2950` Southern Coast Kiwai | Mawata village; 27 forms identical to TNG `southern-kiwai` (sout2950) | high |
| proto-lower-sepik | `lowe1423` Lower Sepik | current `lowe1437` not in Glottolog | high |
| proto-north-adelbert | `nort3379` Northern Adelbert | name match | medium |
| proto-sub-rai | `raic1241` Rai Coast | TNG classification ends at Rai Coast; no "Sub-Rai" node | medium |
| proto-pihom | `nort3379`? | Z'graggen's Pihom ≈ Glottolog Northern Adelbert subgroups. That clashes with proto-north-adelbert | low |
| proto-isumrud | `croi1234` Croisilles? | no Isumrud node | low |
| proto-central-sogeram | `apal1258` Apalic or `sika1264` North Sogeram ("North Central Sogeram")? | needs checking against Daniels' Sogeram classification | low |
| proto-eleman-koriki | none | Glottolog has Eleman (`nucl1580`) and Purari (Koriki, `pura1257`) as separate top-level groups | none |

Note: for a family-level glottocode, the sync gives the node's ancestors but not
the node itself. For example, proto-north-adelbert would get `…, Croisilles, Greater Northern
Adelbert`, without "Northern Adelbert". The sync could include the node itself when it is a
family.

