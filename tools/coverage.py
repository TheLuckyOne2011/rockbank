"""Write COVERAGE.md from questions.json: counts per rulebook section, format, level and specimen."""
import collections, json, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
d = json.load(open(os.path.join(ROOT, "questions.json"), encoding="utf8"))
qs, topics = d["questions"], d["topics"]
tc = collections.Counter(q["topic"] for q in qs)
fc = collections.Counter(q["format"] for q in qs)
spec = collections.Counter(s for q in qs for s in q["specimens"])
sys.path.insert(0, ROOT)
from kb.minerals import MINERALS  # noqa: E402
from kb.rocks import ROCKS  # noqa: E402

L = [f"# Coverage report\n\n{len(qs):,} questions. Rebuild with `python -I gen/build.py`, then `python -I tools/coverage.py`.\n",
     "## By rulebook section (2027 Rocks & Minerals C, section 3)\n", "| Section | Topic | Questions |", "|---|---|---:|"]
L += [f"| {t} | {n} | {tc.get(t, 0):,} |" for t, n in topics.items()]
L += ["\n## By format\n", "| Format | Questions |", "|---|---:|"] + [f"| {k} | {v:,} |" for k, v in fc.most_common()]
L += ["\n## By level\n", "| Level | Questions |", "|---|---:|"] + [f"| {k} | {v:,} |" for k, v in collections.Counter(q['level'] for q in qs).items()]
L += ["\n## Questions per specimen (official list)\n", "| Specimen | Kind | Level | Questions |", "|---|---|---|---:|"]
for s, x in list(MINERALS.items()) + list(ROCKS.items()):
    L.append(f"| {x['name']} | {'mineral' if s in MINERALS else 'rock'} | {x['level']} | {spec.get(s, 0)} |")
open(os.path.join(ROOT, "COVERAGE.md"), "w", encoding="utf8").write("\n".join(L) + "\n")
print("min per specimen:", min(spec.get(s, 0) for s in list(MINERALS) + list(ROCKS)))
