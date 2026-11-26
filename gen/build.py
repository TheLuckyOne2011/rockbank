"""Build the question database: python -I gen/build.py  (run from the rockbank folder)."""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common  # noqa: E402
import gen_minerals  # noqa: E402

MODULES = [gen_minerals]
for name in ("gen_rocks", "gen_concepts", "gen_stations", "gen_multi", "authored2", "authored3", "authored", "concepts2", "concepts3", "gen_reasoning", "authored4"):
    try:
        MODULES.append(__import__(name))
    except ModuleNotFoundError as e:
        if e.name != name:
            raise

for mod in MODULES:
    before = len(common.QUESTIONS)
    mod.run()
    print(f"{mod.__name__:14s} {len(common.QUESTIONS) - before:6d}")

qs = common.QUESTIONS
for i, q in enumerate(qs, 1):
    q["id"] = f"q{i:05d}"
    q = {k: q[k] for k in ["id"] + [k for k in q if k != "id"]}

out = os.path.join(HERE, "..", "questions.json")
with open(out, "w", encoding="utf8") as f:
    json.dump({"version": 1, "event": "Rocks and Minerals C (2027)", "count": len(qs), "topics": common.TOPICS,
               "questions": qs}, f, ensure_ascii=False, indent=1)

print("TOTAL", len(qs))
print("formats", dict(collections.Counter(q["format"] for q in qs)))
print("levels", dict(collections.Counter(q["level"] for q in qs)))
print("difficulty", dict(sorted(collections.Counter(q["difficulty"] for q in qs).items())))
tc = collections.Counter(q["topic"] for q in qs)
for t in common.TOPICS:
    print(f"  {t:9s} {tc.get(t, 0):5d}  {common.TOPICS[t]}")
