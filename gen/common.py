"""Shared helpers for question generation."""
import random, re, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kb.minerals import MINERALS  # noqa: E402
from kb.rocks import ROCKS  # noqa: E402

RNG = random.Random(2027)

# Rulebook section codes -> names (2027 Rocks and Minerals C, section 3)
TOPICS = {
    "3h.i": "Mineral definition",
    "3h.ii": "Mineral identification",
    "3h.iii": "Physical properties",
    "3h.iv": "Other properties (acid, fluorescence, magnetism, etc.)",
    "3h.v": "Mineral habit",
    "3h.vi": "Chemical composition",
    "3h.vi.1": "Solid solution series",
    "3h.vi.2": "Phase diagrams",
    "3h.vii": "Polymorphs",
    "3h.viii.1": "Mineral groups",
    "3h.viii.2": "Silicate structures",
    "3h.viii.3": "Crystal systems",
    "3h.ix": "Mineral formation environments",
    "3h.x": "Minerals of rock-forming environments",
    "3h.xi": "Bowen's reaction series",
    "3h.xii.1": "Uses of minerals and ores",
    "3h.xii.2": "Gemstones and varieties",
    "3i.i": "Rock definition",
    "3i.ii": "Rock identification",
    "3i.iii": "Rock classification",
    "3i.iv.1": "Igneous textures",
    "3i.iv.2": "Igneous composition",
    "3i.iv.3": "Intrusive/extrusive environments",
    "3i.iv.4": "Igneous texture vs. environment",
    "3i.iv.5": "Igneous rocks and plate boundaries",
    "3i.iv.6": "Evolution of igneous melts",
    "3i.iv.6b": "Incompatible elements and pegmatites (State/Nationals)",
    "3i.v.1": "Sedimentary textures",
    "3i.v.2": "Sedimentary composition",
    "3i.v.3": "Grain size, sorting and rounding",
    "3i.v.4": "Sedimentary texture vs. environment",
    "3i.v.5": "Depositional environments",
    "3i.v.6": "Sedimentary structures",
    "3i.vi.1": "Metamorphic textures",
    "3i.vi.2": "Metamorphic composition",
    "3i.vi.3": "Metamorphic minerals",
    "3i.vi.4": "Protoliths",
    "3i.vi.5": "Regional and contact metamorphism",
    "3i.vi.6": "Metamorphic grade and index minerals",
    "3i.vi.7": "Metamorphic facies",
    "3i.vi.8": "Metamorphism and plate tectonics",
    "3i.vii": "Rock cycle",
    "3i.viii": "Economic uses of rocks",
    "3i.ix": "Thin sections (State/Nationals)",
}
STATE_ONLY_TOPICS = {"3i.iv.6b", "3i.ix"}

_seen = set()
QUESTIONS = []


def norm(s):
    return re.sub(r"\W+", " ", str(s).lower()).strip()


def add(fmt, topic, prompt, answer, *, options=None, accept=None, explanation="", diff=2,
        specimens=(), tags=(), level=None, tolerance=None, unit=None, keypoints=None, image=None, source="generated"):
    """Register a question. Returns it, or None if it duplicates an existing prompt+answer.
    Image questions are keyed by their specimen too, since the prompt hides the specimen's name."""
    assert topic in TOPICS, topic
    key = (norm(prompt), norm(answer if not isinstance(answer, list) else "|".join(map(str, answer))),
           tuple(specimens) if image else ())
    if key in _seen:
        return None
    _seen.add(key)
    if options is not None:
        opts = list(dict.fromkeys(options))
        assert len(opts) == len(options), ("duplicate options", prompt, options)
        if fmt == "mcq":
            assert answer in opts, (prompt, answer, opts)
        RNG.shuffle(opts)
        options = opts
    lvl = level
    if lvl is None:
        lvl = "state" if topic in STATE_ONLY_TOPICS or any(
            (MINERALS.get(s) or ROCKS.get(s) or {}).get("level") == "state" for s in specimens) else "regional"
    q = {"format": fmt, "topic": topic, "topicName": TOPICS[topic], "prompt": prompt, "answer": answer,
         "difficulty": diff, "level": lvl, "specimens": list(specimens), "tags": list(tags), "source": source}
    if options is not None:
        q["options"] = options
    if accept:
        q["accept"] = sorted(set(a.lower() for a in accept))
    if tolerance is not None:
        q["tolerance"] = tolerance
    if unit:
        q["unit"] = unit
    if keypoints:
        q["keypoints"] = keypoints
    if image:
        q["image"] = image
    if explanation:
        q["explanation"] = explanation
    QUESTIONS.append(q)
    return q


def pick(pool, n, exclude=()):
    pool = [p for p in dict.fromkeys(pool) if p not in exclude]
    if len(pool) < n:
        return None
    return RNG.sample(pool, n)


def mcq(topic, prompt, correct, distractors, n=3, **kw):
    d = pick(distractors, n, exclude=[correct])
    if not d:
        return None
    return add("mcq", topic, prompt, correct, options=[correct] + d, **kw)


def tf(topic, statement, truth, **kw):
    return add("tf", topic, statement, "True" if truth else "False", options=["True", "False"], **kw)


def short(topic, prompt, answer, accept=(), **kw):
    acc = set([answer] + list(accept))
    return add("short", topic, prompt, answer, accept=acc, **kw)


def article(word):
    return "an" if word[:1].lower() in "aeiou" else "a"


def mineral_accept(m):
    names = {m["name"], *m.get("aka", [])}
    for part in m["name"].split(" / "):
        names.add(part)
    if m.get("variety_of"):
        pass
    return names


def rock_accept(r):
    names = {r["name"], *r.get("aka", [])}
    for part in r["name"].replace("(", "/").replace(")", "").split("/"):
        names.add(part.strip())
    return names


def fmt_range(lo, hi):
    f = lambda x: ("%g" % x)
    return f(lo) if lo == hi else f"{f(lo)}–{f(hi)}"


def overlap(a, b, margin=0.0):
    return not (a[1] + margin < b[0] or b[1] + margin < a[0])


ATOMIC = {"H": 1.008, "Li": 6.94, "Be": 9.012, "B": 10.81, "C": 12.011, "O": 15.999, "F": 18.998, "Na": 22.990,
          "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098, "Ca": 40.078,
          "Ti": 47.867, "V": 50.942, "Mn": 54.938, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Sr": 87.62, "Zr": 91.224,
          "Ag": 107.868, "Sb": 121.760, "Ba": 137.327, "Au": 196.967, "Pb": 207.2}
ELEMENT_NAMES = {"H": "hydrogen", "Li": "lithium", "Be": "beryllium", "B": "boron", "C": "carbon", "O": "oxygen",
                 "F": "fluorine", "Na": "sodium", "Mg": "magnesium", "Al": "aluminum", "Si": "silicon", "P": "phosphorus",
                 "S": "sulfur", "Cl": "chlorine", "K": "potassium", "Ca": "calcium", "Ti": "titanium", "V": "vanadium",
                 "Mn": "manganese", "Fe": "iron", "Cu": "copper", "Zn": "zinc", "Sr": "strontium", "Zr": "zirconium",
                 "Ag": "silver", "Sb": "antimony", "Ba": "barium", "Au": "gold", "Pb": "lead", "Rb": "rubidium"}
NAME_TO_SYMBOL = {v: k for k, v in ELEMENT_NAMES.items()}


def parse_formula(f):
    out = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f):
        out[el] = out.get(el, 0) + (int(n) if n else 1)
    return out


def molar_mass(f):
    return sum(ATOMIC[e] * n for e, n in parse_formula(f).items())


def wt_pct(f, el):
    c = parse_formula(f)
    return 100 * ATOMIC[el] * c.get(el, 0) / molar_mass(f)
