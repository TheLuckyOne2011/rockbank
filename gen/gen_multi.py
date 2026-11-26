"""Select-all-that-apply questions and pairwise comparisons, built from verified properties."""
import itertools
from common import MINERALS, ROCKS, RNG, add, mcq, fmt_range, overlap
from gen_minerals import sil_of, SYSTEMS, same_species, sg_mid

MS = list(MINERALS.values())
RS = list(ROCKS.values())

# (topic, prompt, predicate, "unsure" predicate excluded from options, explanation-fn)
MIN_PROPS = [
    ("3h.iv", "Select ALL minerals that effervesce readily in cold, dilute HCl.",
     lambda m: "cold" in m["special"].get("acid", "") and "powder" not in m["special"].get("acid", ""),
     lambda m: bool(m["special"].get("acid")) and "cold" not in m["special"].get("acid", "")),
    ("3h.iii", "Select ALL minerals hard enough to scratch glass (hardness above ~5.5).", lambda m: m["H"][0] >= 6.5,
     lambda m: m["H"][1] >= 5.5 and m["H"][0] < 6.5),
    ("3h.iii", "Select ALL minerals that a fingernail (~2.5) can scratch.", lambda m: m["H"][1] <= 2,
     lambda m: m["H"][0] <= 3 and m["H"][1] > 2),
    ("3h.iii", "Select ALL minerals with a metallic luster.", lambda m: m["luster"][0] in ("metallic",),
     lambda m: "metallic" in m["luster"] or "submetallic" in m["luster"]),
    ("3h.iii", "Select ALL minerals whose streak is NOT white or colorless.",
     lambda m: not any(w in m["streak"] for w in ("white", "none", "colorless")),
     lambda m: "to white" in m["streak"] or "white (" in m["streak"]),
    ("3h.iii", "Select ALL minerals with a specific gravity above 4.5.", lambda m: m["SG"][0] > 4.6, lambda m: m["SG"][1] > 4.3 and m["SG"][0] <= 4.6),
    ("3h.iii", "Select ALL minerals with no cleavage.", lambda m: m["cleave"][0] == 0 and m["cleave"][1] == "none",
     lambda m: m["cleave"][1] in ("poor", "fair")),
    ("3h.iii", "Select ALL minerals with perfect cleavage in exactly one direction.",
     lambda m: m["cleave"][0] == 1 and m["cleave"][1] == "perfect", lambda m: m["cleave"][1] in ("poor", "fair", "good")),
    ("3h.iii", "Select ALL minerals with three cleavage directions.", lambda m: m["cleave"][0] == 3, lambda m: m["cleave"][1] in ("poor", "fair")),
    ("3h.iii", "Select ALL minerals that are malleable.", lambda m: "malleable" in m["tenacity"], lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are carbonates.", lambda m: m["cls"] == "carbonate", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are sulfides.", lambda m: m["cls"] == "sulfide", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are oxides or hydroxides.", lambda m: m["cls"] == "oxide", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are sulfates.", lambda m: m["cls"] == "sulfate", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are native elements.", lambda m: m["cls"] == "native element", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are phosphates (or apatite-group vanadates).", lambda m: m["cls"] == "phosphate", lambda m: False),
    ("3h.viii.1", "Select ALL minerals that are NOT silicates.", lambda m: m["cls"] != "silicate", lambda m: False),
    ("3h.viii.2", "Select ALL minerals that are nesosilicates (isolated tetrahedra).", lambda m: sil_of(m) == "nesosilicate", lambda m: False),
    ("3h.viii.2", "Select ALL minerals that are phyllosilicates (sheet silicates).", lambda m: sil_of(m) == "phyllosilicate", lambda m: False),
    ("3h.viii.2", "Select ALL minerals that are tectosilicates (framework silicates).", lambda m: sil_of(m) == "tectosilicate", lambda m: False),
    ("3h.viii.2", "Select ALL minerals that are inosilicates (chain silicates).", lambda m: (sil_of(m) or "").startswith("inosilicate"), lambda m: False),
    ("3h.viii.2", "Select ALL minerals that are cyclosilicates (ring silicates).", lambda m: sil_of(m) == "cyclosilicate", lambda m: False),
    ("3h.viii.3", "Select ALL minerals that crystallize in the cubic system.", lambda m: m["system"] == "cubic", lambda m: m["system"] not in SYSTEMS),
    ("3h.viii.3", "Select ALL minerals that crystallize in the monoclinic system.", lambda m: m["system"] == "monoclinic", lambda m: m["system"] not in SYSTEMS),
    ("3h.viii.3", "Select ALL minerals that crystallize in the orthorhombic system.", lambda m: m["system"] == "orthorhombic", lambda m: m["system"] not in SYSTEMS),
    ("3h.viii.3", "Select ALL minerals that crystallize in the triclinic system.", lambda m: m["system"] == "triclinic", lambda m: m["system"] not in SYSTEMS),
    ("3h.viii.3", "Select ALL minerals that crystallize in the tetragonal system.", lambda m: m["system"] == "tetragonal", lambda m: m["system"] not in SYSTEMS),
    ("3h.viii.3", "Select ALL minerals that crystallize in the trigonal system.", lambda m: m["system"] == "trigonal",
     lambda m: m["system"] not in SYSTEMS or m["system"] == "hexagonal"),
    ("3h.xii.1", "Select ALL minerals that are ores of copper.", lambda m: "copper" in m["ore"], lambda m: "Cu" in m["formula"]),
    ("3h.xii.1", "Select ALL minerals that are ores of iron.", lambda m: "iron" in m["ore"], lambda m: "Fe" in m["formula"]),
    ("3h.xii.1", "Select ALL minerals that are ores of lead or zinc.", lambda m: bool({"lead", "zinc"} & set(m["ore"])),
     lambda m: "Pb" in m["formula"] or "Zn" in m["formula"]),
    ("3h.vi", "Select ALL minerals that contain iron as an essential element in their formula.",
     lambda m: "Fe" in m["formula"] and "(Mg,Fe)" not in m["formula"] and "(Al,Fe)" not in m["formula"] and "(Zn,Fe)" not in m["formula"]
     and "(Fe,Mg" not in m["formula"] and "Fe,Al" not in m["formula"],
     lambda m: "Fe" in m["formula"] or m["slug"] in ("tourmaline", "staurolite")),
    ("3h.vi", "Select ALL minerals that contain water or hydroxyl (OH) in their formula.", lambda m: "H" in m["formula"].replace("Hg", ""), lambda m: False),
    ("3h.vi", "Select ALL minerals that contain calcium as an essential element.", lambda m: "Ca" in m["formula"] and m["formula"] != "(Ca,Na)(Al,Si)4O8",
     lambda m: "(Ca,Na)" in m["formula"] or "Ca" in m["formula"]),
    ("3h.xii.2", "Select ALL minerals that have gem varieties named on the official rules (emerald, aquamarine, morganite, kunzite, hiddenite, peridot, ruby, sapphire).",
     lambda m: m["slug"] in ("beryl", "spodumene", "olivine", "corundum"), lambda m: bool(m["varieties"])),
]

ROCK_PROPS = [
    ("3i.iii", "Select ALL igneous rocks.", lambda r: r["type"] == "igneous", lambda r: False),
    ("3i.iii", "Select ALL sedimentary rocks.", lambda r: r["type"] == "sedimentary" and r["slug"] != "anthracite", lambda r: r["slug"] == "anthracite"),
    ("3i.iii", "Select ALL metamorphic rocks.", lambda r: r["type"] == "metamorphic", lambda r: r["slug"] == "anthracite"),
    ("3i.iv.3", "Select ALL intrusive (plutonic) igneous rocks.", lambda r: r["sub"] == "intrusive", lambda r: False),
    ("3i.iv.3", "Select ALL extrusive or pyroclastic igneous rocks.", lambda r: r["type"] == "igneous" and r["sub"] != "intrusive", lambda r: False),
    ("3i.iv.2", "Select ALL felsic igneous rocks.", lambda r: r["comp"] == "felsic", lambda r: r["comp"] not in (None, "felsic", "intermediate", "mafic", "ultramafic")),
    ("3i.iv.2", "Select ALL mafic or ultramafic igneous rocks.", lambda r: r["comp"] in ("mafic", "ultramafic"),
     lambda r: r["comp"] not in (None, "felsic", "intermediate", "mafic", "ultramafic")),
    ("3i.iv.1", "Select ALL rocks with a vesicular texture.", lambda r: "vesicular" in r["texture"], lambda r: False),
    ("3i.v.1", "Select ALL clastic sedimentary rocks.", lambda r: r["sub"] == "clastic", lambda r: r["slug"] == "chert-flint"),
    ("3i.v.1", "Select ALL chemical sedimentary rocks.", lambda r: r["sub"] == "chemical" and r["slug"] not in ("chert-flint", "oolitic-limestone"), lambda r: r["slug"] in ("chert-flint", "oolitic-limestone")),
    ("3i.v.1", "Select ALL biochemical (organic) sedimentary rocks.", lambda r: r["sub"] == "biochemical", lambda r: r["slug"] in ("chert-flint", "oolitic-limestone")),
    ("3i.v.2", "Select ALL rocks that fizz vigorously in cold, dilute HCl.", lambda r: (r.get("acid") or "").startswith("fizzes vigorously"),
     lambda r: "fizz" in (r.get("acid") or "") and not (r.get("acid") or "").startswith("fizzes vigorously")),
    ("3i.v.2", "Select ALL rocks composed mainly of silica (SiO2).", lambda r: r["slug"] in ("chert-flint", "diatomite", "quartz-sandstone", "quartzite", "obsidian"),
     lambda r: r["slug"] in ("rhyolite", "pumice", "granite", "pegmatite", "arkose", "banded-iron-formation")),
    ("3i.vi.1", "Select ALL foliated metamorphic rocks.", lambda r: r["type"] == "metamorphic" and r["sub"] == "foliated" and r["slug"] not in ("amphibolite", "talc-schist"),
     lambda r: r["slug"] in ("amphibolite", "talc-schist")),
    ("3i.vi.4", "Select ALL rocks whose protolith is shale.", lambda r: (r.get("protolith") or "").startswith("shale"), lambda r: r["slug"] == "gneiss"),
    ("3i.v.2", "Select ALL limestones (rocks made mainly of calcite).", lambda r: r["group"] == "Limestone varieties", lambda r: r["slug"] in ("marble", "dolostone")),
]


def build(props, items, name_of, n_q=12):
    for topic, prompt, pred, unsure in props:
        yes = [x for x in items if pred(x)]  # unsure only keeps ambiguous items out of the wrong-answer pool
        no = [x for x in items if not pred(x) and not unsure(x)]
        if len(yes) < 2 or len(no) < 3:
            continue
        made = 0
        for _ in range(n_q * 4):
            k_yes = RNG.randint(1, min(3, len(yes)))
            k_no = RNG.randint(3, 5) if len(no) >= 5 else len(no)
            picks_yes = RNG.sample(yes, k_yes)
            picks_no = RNG.sample(no, k_no)
            opts = [name_of(x) for x in picks_yes + picks_no]
            if len(set(opts)) != len(opts):
                continue
            ans = sorted(name_of(x) for x in picks_yes)
            q = add("multi", topic, prompt, ans, options=opts, specimens=[x["slug"] for x in picks_yes + picks_no],
                    tags=["select all"], diff=2, explanation="Correct: " + ", ".join(ans) + ".")
            if q:
                made += 1
            if made >= n_q:
                break


def comparisons():
    ok = [m for m in MS if m["H"][1] - m["H"][0] <= 1.5]
    pairs = [(a, b) for a, b in itertools.combinations(ok, 2) if not overlap(a["H"], b["H"], 0.5) and not same_species(a, b)]
    for a, b in RNG.sample(pairs, min(320, len(pairs))):
        hard, soft = (a, b) if a["H"][0] > b["H"][1] else (b, a)
        mcq("3h.iii", f"Which is harder, {a['name']} or {b['name']}?", hard["name"], [soft["name"]], n=1, specimens=[a["slug"], b["slug"]],
            tags=["hardness", "comparison"], diff=1, explanation=f"{hard['name']} {fmt_range(*hard['H'])} vs {soft['name']} {fmt_range(*soft['H'])}.")
    pairs = [(a, b) for a, b in itertools.combinations(MS, 2) if abs(sg_mid(a) - sg_mid(b)) >= 0.8 and not same_species(a, b)]
    for a, b in RNG.sample(pairs, min(280, len(pairs))):
        hi, lo = (a, b) if sg_mid(a) > sg_mid(b) else (b, a)
        mcq("3h.iii", f"Which has the higher specific gravity, {a['name']} or {b['name']}?", hi["name"], [lo["name"]], n=1,
            specimens=[a["slug"], b["slug"]], tags=["specific gravity", "comparison"], diff=2,
            explanation=f"{hi['name']} ~{sg_mid(hi)} vs {lo['name']} ~{sg_mid(lo)}.")


def run():
    build(MIN_PROPS, MS, lambda m: m["name"], n_q=22)
    build(ROCK_PROPS, RS, lambda r: r["name"], n_q=22)
    comparisons()
