# Rockbank — Rocks & Minerals C question database (2027)

About 12,000 practice questions covering every part of section 3 of the 2027 Rocks and Minerals C rules,
built for a study game. Everything is generated from a hand-checked knowledge base, so a fix in
`kb/` flows through to every question that uses that fact.

```
python -I gen/build.py        # writes questions.json and prints counts
python -I tools/coverage.py . # writes COVERAGE.md
```

## Files

| Path | What it is |
|---|---|
| `questions.json` | The database: `{version, event, count, topics, questions[]}` |
| `COVERAGE.md` | Counts by rulebook section, format, level and specimen |
| `kb/minerals.py`, `kb/rocks.py` | Knowledge base for all 128 specimens on the official list (82 minerals, 46 rocks) |
| `gen/gen_minerals.py` | Property questions: formulas, classes, hardness, streak, luster, cleavage, SG, ores, uses, identification |
| `gen/gen_rocks.py` | Rock type, texture, composition, environment, protolith, grade, uses |
| `gen/gen_concepts.py` | Parameterized questions: Bowen's series, index minerals, facies from P-T, Al2SiO5 diagram, lever rule, plagioclase/olivine compositions, Wentworth sizes, rock names from mineral %, radiometric dating |
| `gen/gen_stations.py` | Station-style chains: a specimen photo, then follow-ups that refer to "this specimen" |
| `gen/gen_multi.py` | Select-all questions and pairwise hardness/SG comparisons |
| `gen/authored*.py`, `gen/concepts2.py`, `gen/concepts3.py` | Concept bank: ~680 hand-written questions plus hand-checked concept fact tables (glossary, environments, structures, intrusions, magma, plate settings, metamorphism, facies, weathering, thin-section optics, incompatible elements) that each yield several question types |
| `tools/harvest.py` | Downloads Division C R&M tests from scio.ly (online tests + Drive PDF archive) into `sources/` for reference |

## Question format

```json
{
  "id": "q00042", "format": "mcq", "topic": "3h.iii", "topicName": "Physical properties",
  "prompt": "What color is the streak of Hematite?", "options": ["…"], "answer": "reddish brown",
  "explanation": "…", "difficulty": 2, "level": "regional",
  "specimens": ["hematite"], "tags": ["streak"], "source": "generated"
}
```

- `format`: `mcq` (one answer), `multi` (select all: `answer` is a list), `tf`, `short` (grade against `accept`,
  lower-cased aliases), `numeric` (within `tolerance`, optional `unit`), `order` (`answer` is the correct order),
  `frq` (model `answer` plus `keypoints` for self-grading or LLM grading).
- `topic`: rulebook section code; `topics` at the top of the file maps codes to names.
- `level`: `state` if the question uses a starred (State/Nationals-only) specimen or a State/Nationals-only topic
  (thin sections, incompatible elements); otherwise `regional`.
- `image`: `{"specimen": "<slug>"}` means show a photo of that specimen. Slugs match the folders in
  `../rockid/images/<slug>/`, so any of the ~10k photos there can be used.
- `station`: `{"id": "<slug>-<n>", "part": k}` groups a specimen chain; part 1 is always "Identify this specimen."

## Notes

- Specimen list: taken from `rockid/data/specimens.json` (the official list with starred items). If the 2027 list
  adds or drops specimens, update `kb/` and rebuild.
- Style reference: 83 Division C online tests and the Division C R&M PDFs from the scio.ly archive
  (`sources/`, not redistributed), plus the practice tests in Downloads. The questions here are original;
  none are copied from those tests.
- Facts that vary between sources (hardness ranges, SG, coal carbon %, facies P-T boxes) use conservative
  textbook values, and distractors are only drawn from values that clearly differ.
