"""Mineral questions generated from kb/minerals.py."""
import itertools
from common import (MINERALS, RNG, add, mcq, tf, short, pick, mineral_accept, fmt_range, overlap,
                    wt_pct, ELEMENT_NAMES, NAME_TO_SYMBOL, parse_formula, article)

MS = list(MINERALS.values())
SYSTEMS = ["cubic", "tetragonal", "orthorhombic", "monoclinic", "triclinic", "trigonal", "hexagonal"]
CLASSES = ["native element", "sulfide", "oxide", "halide", "carbonate", "sulfate", "phosphate", "borate", "silicate"]
SIL = {"nesosilicate (isolated tetrahedra)": "nesosilicate", "sorosilicate (paired tetrahedra)": "sorosilicate",
       "cyclosilicate (ring)": "cyclosilicate", "inosilicate (single chain)": "inosilicate (single chain)",
       "inosilicate (double chain)": "inosilicate (double chain)", "phyllosilicate (sheet)": "phyllosilicate",
       "tectosilicate (framework)": "tectosilicate"}
SIL_ALL = ["nesosilicate", "sorosilicate", "cyclosilicate", "inosilicate (single chain)", "inosilicate (double chain)",
           "phyllosilicate", "tectosilicate"]


def sil_of(m):
    s = m["sil"]
    if not s:
        return None
    if s.startswith("inosilicate (single chain"):
        return "inosilicate (single chain)"
    if s.startswith("tectosilicate"):
        return "tectosilicate"
    return SIL.get(s)


def is_quartz_family(m):
    return m.get("variety_of") == "quartz" or m["slug"] == "opal"


def same_species(a, b):
    """Varieties of one species (quartz varieties, gypsum varieties) share most properties."""
    if a["slug"] == b["slug"]:
        return True
    if a.get("variety_of") and a.get("variety_of") == b.get("variety_of"):
        return True
    if a["formula"] == b["formula"] and a["cls"] == b["cls"] and a["system"] == b["system"]:
        return True
    return False


def streak_cat(s):
    s = s.lower()
    for k, cat in [("none", "none"), ("copper", "copper red"), ("golden", "yellow"), ("silver", "silver"),
                   ("orange", "orange"), ("reddish", "red-brown"), ("yellowish brown", "yellow-brown"),
                   ("blue", "blue"), ("green-blue", "blue"), ("light green", "green"), ("greenish black", "black"),
                   ("black", "black"), ("lead gray", "gray"), ("gray-green", "gray"), ("pale brown", "brown"),
                   ("light brown", "brown"), ("pale yellow", "yellow"), ("yellow", "yellow"), ("white", "white")]:
        if k in s:
            return cat
    return s


def hstr(m):
    return fmt_range(*m["H"])


def sg_mid(m):
    return round(sum(m["SG"]) / 2, 1)


# ---------------------------------------------------------------- formulas & chemistry
def formulas():
    seen_formula = {}
    for m in MS:
        seen_formula.setdefault(m["formula"], []).append(m)
    for m in MS:
        others = [o["formula"] for o in MS if o["formula"] != m["formula"]]
        same_cls = [o["formula"] for o in MS if o["formula"] != m["formula"] and o["cls"] == m["cls"]]
        pool = same_cls if len(same_cls) >= 3 else others
        mcq("3h.vi", f"What is the chemical formula of {m['name']}?", m["formula"], pool, specimens=[m["slug"]],
            tags=["formula"], diff=2, explanation=f"{m['name']} is {m['formula']} ({m['cls']}).")
        if len(same_cls) >= 3 and len(others) >= 3:
            mcq("3h.vi", f"Which formula belongs to {m['name']}?", m["formula"],
                [o for o in others if o not in same_cls], specimens=[m["slug"]], tags=["formula"], diff=1,
                explanation=f"{m['name']} is {m['formula']}.")
    for f, group in seen_formula.items():
        names = [g["name"] for g in group]
        acc = set().union(*[mineral_accept(g) for g in group])
        m = group[0]
        expl = f"{f} is the formula of {', '.join(names)}."
        if len(group) == 1:
            dpool = [o["name"] for o in MS if o["formula"] != f and o["cls"] == m["cls"]] or [o["name"] for o in MS if o["formula"] != f]
            mcq("3h.vi", f"Which mineral has the formula {f}?", m["name"], dpool, specimens=[m["slug"]], tags=["formula"],
                explanation=expl)
        if m["slug"] in ("calcite", "aragonite"):
            continue  # polymorph prompt handled separately
        short("3h.vi", f"Name a mineral on the official list with the formula {f}.", names[0], acc,
              specimens=[g["slug"] for g in group], tags=["formula"], diff=2, explanation=expl)


def elements_and_ores():
    for m in MS:
        if m["ore"]:
            ores = m["ore"]
            in_formula = {ELEMENT_NAMES.get(e) for e in parse_formula(m.get("calc") or m["formula"])}
            pool = [e for e in ["iron", "copper", "lead", "zinc", "aluminum", "titanium", "manganese", "lithium", "beryllium",
                                "barium", "strontium", "antimony", "vanadium", "zirconium", "silver", "gold", "magnesium", "boron"]
                    if e not in ores and e not in in_formula]
            mcq("3h.xii.1", f"{m['name']} is mined as an ore of which element?", ores[0], pool, specimens=[m["slug"]],
                tags=["ore"], diff=1, explanation=f"{m['name']} ({m['formula']}) is an ore of {', '.join(ores)}.")
            short("3h.xii.1", f"{m['name']} is an important ore of what element?", ores[0],
                  ores + [NAME_TO_SYMBOL.get(o, o) for o in ores] + (["aluminium"] if "aluminum" in ores else []),
                  specimens=[m["slug"]], tags=["ore"], diff=1, explanation=f"Ore of {', '.join(ores)}.")
    # reverse: element -> which mineral is an ore of it
    by_el = {}
    for m in MS:
        for e in m["ore"]:
            by_el.setdefault(e, []).append(m)
    for e, ms in by_el.items():
        nots = [o["name"] for o in MS if e not in o["ore"] and NAME_TO_SYMBOL.get(e, "?") not in parse_formula(o.get("calc") or o["formula"])]
        for m in ms:
            mcq("3h.xii.1", f"Which of these minerals is an ore of {e}?", m["name"], nots, specimens=[m["slug"]],
                tags=["ore"], diff=1, explanation=f"{m['name']} ({m['formula']}) is an ore of {e}.")
    # weight-percent calculations
    targets = {"Cu": ["chalcopyrite", "bornite", "azurite", "malachite"],
               "Fe": ["hematite", "magnetite", "goethite-limonite", "siderite", "pyrite", "chalcopyrite"],
               "Pb": ["galena", "pyromorphite", "vanadinite"], "Zn": ["zincite", "willemite", "sphalerite"],
               "Al": ["corundum", "kyanite", "kaolinite"], "Ba": ["barite"], "Sr": ["celestite"], "Sb": ["stibnite"],
               "Ti": ["rutile"], "Mn": ["pyrolusite", "rhodochrosite"], "Mg": ["magnesite"], "Ca": ["calcite", "fluorite"],
               "Zr": ["zircon"], "Li": ["spodumene"], "Be": ["beryl"], "Na": ["halite"], "S": ["pyrite"]}
    for el, slugs in targets.items():
        for s in slugs:
            m = MINERALS[s]
            calc = m["calc"]
            pct = wt_pct(calc, el)
            name = ELEMENT_NAMES[el]
            note = " (use the ideal end-member ZnS)" if s == "sphalerite" else ""
            add("numeric", "3h.vi", f"Using the ideal formula {calc}{note}, what percent of {m['name']}'s mass is {name}? "
                "Give your answer to one decimal place.", round(pct, 1), tolerance=0.6, unit="%",
                specimens=[s], tags=["calculation", "weight percent"], diff=3,
                explanation=f"Mass of {name} / formula mass = {pct:.1f}%.")
            # mass of metal recoverable from a sample
            mass = RNG.choice([50, 100, 250, 500, 1000, 2000])
            add("numeric", "3h.xii.1", f"A miner extracts {mass} kg of pure {m['name']} ({calc}). Assuming 100% recovery, "
                f"how many kilograms of {name} could be produced? (nearest whole kg)", round(mass * pct / 100),
                tolerance=max(1, round(mass * 0.01)), unit="kg", specimens=[s], tags=["calculation", "ore grade"], diff=3,
                explanation=f"{name.capitalize()} is {pct:.1f}% of {calc} by mass, so {mass} x {pct/100:.3f} = {mass*pct/100:.0f} kg.")
        if len(slugs) >= 3:
            ranked = sorted(slugs, key=lambda s: -wt_pct(MINERALS[s]["calc"], el))
            for combo in itertools.combinations(ranked, 3):
                vals = [wt_pct(MINERALS[s]["calc"], el) for s in combo]
                if min(abs(a - b) for a, b in itertools.combinations(vals, 2)) < 2:
                    continue
                names = [MINERALS[s]["name"] for s in combo]
                best = names[0]
                listing = ", ".join(MINERALS[s]["name"] + " " + MINERALS[s]["calc"] for s in sorted(combo))
                mcq("3h.xii.1", f"By mass, which of these minerals contains the highest percentage of {ELEMENT_NAMES[el]}? "
                    f"({listing})", best,
                    names[1:], n=2, specimens=list(combo), tags=["calculation", "ore grade"], diff=3,
                    explanation="; ".join(f"{n}: {v:.1f}%" for n, v in zip(names, vals)))


def classes():
    for m in MS:
        mcq("3h.viii.1", f"To which chemical class does {m['name']} belong?", m["cls"], CLASSES, specimens=[m["slug"]],
            tags=["class"], diff=1, explanation=f"{m['name']} ({m['formula']}) is {article(m['cls'])} {m['cls']}.")
        s = sil_of(m)
        if s:
            mcq("3h.viii.2", f"Which silicate structure does {m['name']} have?", s, SIL_ALL, specimens=[m["slug"]],
                tags=["silicate structure"], diff=2, explanation=f"{m['name']} is {article(s)} {m['sil']}.")
    # reverse: given class, which mineral
    for cls in CLASSES:
        ins = [m for m in MS if m["cls"] == cls]
        outs = [m["name"] for m in MS if m["cls"] != cls]
        for m in ins:
            mcq("3h.viii.1", f"Which of the following minerals is {article(cls)} {cls}?", m["name"], outs,
                specimens=[m["slug"]], tags=["class"], diff=1, explanation=f"{m['name']} is {article(cls)} {cls}.")
        if len(ins) >= 3:
            for m in RNG.sample(outs, min(6, len(outs))):
                mm = next(x for x in MS if x["name"] == m)
                three = RNG.sample([x["name"] for x in ins], 3)
                mcq("3h.viii.1", f"Which of these minerals is NOT {article(cls)} {cls}?", m, three, specimens=[mm["slug"]],
                    tags=["class", "odd one out"], diff=2, explanation=f"{m} is {article(mm['cls'])} {mm['cls']}; the others are {cls}s.")
    for s in SIL_ALL:
        ins = [m for m in MS if sil_of(m) == s]
        outs = [m["name"] for m in MS if sil_of(m) and sil_of(m) != s]
        for m in ins:
            mcq("3h.viii.2", f"Which of these silicates is {article(s)} {s}?", m["name"], outs, specimens=[m["slug"]],
                tags=["silicate structure"], diff=2, explanation=f"{m['name']}: {m['sil']}.")


def groups():
    grp = {"Garnet Group": "garnet", "Mica Group": "mica", "Amphibole Group": "amphibole", "Pyroxene Group": "pyroxene",
           "Feldspar Group - Plagioclase": "feldspar", "Feldspar Group - Potassium": "feldspar", "Apatite Group": "apatite",
           "Quartz varieties": "quartz (silica) varieties", "Gypsum varieties": "gypsum varieties"}
    names = sorted(set(grp.values()))
    for m in MS:
        g = grp.get(m["group"])
        if not g:
            continue
        mcq("3h.viii.1", f"{m['name']} belongs to which mineral group?", g, names, specimens=[m["slug"]], tags=["group"],
            diff=1, explanation=f"{m['name']} is in the {g} group.")
    fs = [m for m in MS if m["group"] and m["group"].startswith("Feldspar")]
    for m in fs:
        kind = "plagioclase" if "Plagioclase" in m["group"] else "potassium (alkali) feldspar"
        mcq("3h.viii.1", f"Is {m['name']} a plagioclase feldspar or a potassium feldspar?", kind,
            ["plagioclase", "potassium (alkali) feldspar", "feldspathoid"], n=2, specimens=[m["slug"]], tags=["feldspar"],
            diff=2, explanation=f"{m['name']}: {m['group'].split(' - ')[1].lower()} feldspar.")


def crystal_systems():
    for m in MS:
        sysm = m["system"]
        if sysm not in SYSTEMS:
            continue
        bad = {"trigonal": ["hexagonal"], "hexagonal": ["trigonal"]}.get(sysm, [])
        mcq("3h.viii.3", f"In which crystal system does {m['name']} crystallize?", sysm,
            [s for s in SYSTEMS if s not in bad], specimens=[m["slug"]], tags=["crystal system"], diff=2,
            explanation=f"{m['name']} is {sysm}." + (" (Trigonal minerals are sometimes grouped in the hexagonal family.)" if sysm == "trigonal" else ""))
    for sysm in SYSTEMS:
        ins = [m for m in MS if m["system"] == sysm and not is_quartz_family(m)]
        outs = [m["name"] for m in MS if m["system"] in SYSTEMS and m["system"] != sysm and
                not (sysm in ("trigonal", "hexagonal") and m["system"] in ("trigonal", "hexagonal"))]
        for m in ins:
            mcq("3h.viii.3", f"Which of these minerals belongs to the {sysm} crystal system?", m["name"], outs,
                specimens=[m["slug"]], tags=["crystal system"], diff=2, explanation=f"{m['name']} is {sysm}.")
    tf("3h.viii.3", "Opal has no crystal system because it is amorphous.", True, specimens=["opal"],
       tags=["crystal system", "mineraloid"], explanation="Opal lacks long-range atomic order, so it is a mineraloid.")


# ---------------------------------------------------------------- physical properties
def hardness():
    usable = [m for m in MS if m["H"][1] - m["H"][0] <= 1.5]
    for m in usable:
        dist = [hstr(o) for o in usable if not overlap(o["H"], m["H"], 0.5)]
        mcq("3h.iii", f"What is the Mohs hardness of {m['name']}?", hstr(m), dist, specimens=[m["slug"]],
            tags=["hardness"], diff=2, explanation=f"{m['name']} has a hardness of {hstr(m)}.")
    tests = [("a fingernail", 2.5), ("a copper coin", 3.5), ("a steel knife or glass plate", 5.5)]
    for m in MS:
        lo, hi = m["H"]
        for obj, h in tests:
            if hi <= h - 0.5:
                tf("3h.iii", f"{m['name']} can be scratched by {obj} (hardness ~{h}).", True, specimens=[m["slug"]],
                   tags=["hardness", "scratch test"], diff=1, explanation=f"{m['name']} is {hstr(m)}, softer than {h}.")
            elif lo >= h + 0.5:
                tf("3h.iii", f"{m['name']} can be scratched by {obj} (hardness ~{h}).", False, specimens=[m["slug"]],
                   tags=["hardness", "scratch test"], diff=1, explanation=f"{m['name']} is {hstr(m)}, harder than {h}.")
        if lo >= 7:
            tf("3h.iii", f"{m['name']} is hard enough to scratch glass.", True, specimens=[m["slug"]], tags=["hardness"],
               explanation=f"{m['name']} ({hstr(m)}) is harder than glass (~5.5).")
        elif hi <= 5:
            tf("3h.iii", f"{m['name']} is hard enough to scratch glass.", False, specimens=[m["slug"]], tags=["hardness"],
               explanation=f"{m['name']} ({hstr(m)}) is softer than glass (~5.5).")
    # which mineral would scratch X
    for a in usable:
        harder = [b["name"] for b in usable if b["H"][0] >= a["H"][1] + 1 and not same_species(a, b)]
        softer = [b["name"] for b in usable if b["H"][1] <= a["H"][0] - 0.5 and not same_species(a, b)]
        if harder and len(softer) >= 3:
            c = RNG.choice(harder)
            cm = next(x for x in MS if x["name"] == c)
            mcq("3h.iii", f"Which of these minerals could scratch {a['name']}?", c, softer, specimens=[a["slug"], cm["slug"]],
                tags=["hardness", "scratch test"], diff=2, explanation=f"{c} ({hstr(cm)}) is harder than {a['name']} ({hstr(a)}).")
    # ranking
    for _ in range(220):
        four = RNG.sample(usable, 4)
        four.sort(key=lambda m: m["H"][0])
        if any(overlap(x["H"], y["H"], 0.4) for x, y in itertools.combinations(four, 2)):
            continue
        order = ", ".join(m["name"] for m in four)
        names = sorted(m["name"] for m in four)
        add("order", "3h.iii", f"Rank these minerals from softest to hardest: {', '.join(names)}.", [m["name"] for m in four],
            specimens=[m["slug"] for m in four], tags=["hardness", "ranking"], diff=2,
            explanation="; ".join(f"{m['name']} {hstr(m)}" for m in four))
    # mohs scale index minerals
    mohs = {1: "talc", 2: "gypsum", 3: "calcite", 4: "fluorite", 5: "apatite", 6: "orthoclase", 7: "quartz", 8: "topaz",
            9: "corundum", 10: "diamond"}
    for h, n in mohs.items():
        mcq("3h.iii", f"Which mineral defines hardness {h} on the Mohs scale?", n, [v for k, v in mohs.items() if k != h],
            tags=["hardness", "Mohs scale"], diff=1, explanation=f"Mohs {h} = {n}.")
        short("3h.iii", f"What is the Mohs hardness of {n}, a reference mineral on the Mohs scale?", str(h), [str(h)],
              tags=["hardness", "Mohs scale"], diff=1, explanation=f"{n.capitalize()} = {h}.")


def streak_luster():
    for m in MS:
        cat = streak_cat(m["streak"])
        dist = list({streak_cat(o["streak"]): o["streak"] for o in MS if streak_cat(o["streak"]) != cat}.values())
        mcq("3h.iii", f"What color is the streak of {m['name']}?", m["streak"], dist, specimens=[m["slug"]], tags=["streak"],
            diff=2 if cat != "white" else 1, explanation=f"{m['name']} leaves a {m['streak']} streak.")
        if cat not in ("white", "none"):
            others = [o for o in MS if streak_cat(o["streak"]) == "white" and not same_species(o, m)]
            mcq("3h.iii", f"Which of these minerals has a {m['streak']} streak?", m["name"],
                [o["name"] for o in others], specimens=[m["slug"]], tags=["streak"], diff=2,
                explanation=f"{m['name']}: {m['streak']} streak; the others streak white.")
        lus = m["luster"][0]
        dl = ["metallic", "adamantine", "vitreous", "resinous", "pearly", "silky", "greasy", "waxy", "dull", "earthy", "submetallic"]
        excl = set(m["luster"]) | ({"submetallic", "adamantine"} if "metallic" in m["luster"] else set()) | (
            {"earthy"} if "dull" in m["luster"] else {"dull"} if "earthy" in m["luster"] else set()) | (
            {"greasy", "waxy", "resinous"} if set(m["luster"]) & {"greasy", "waxy", "resinous"} else set())
        mcq("3h.iii", f"Which luster best describes {m['name']}?", lus, [d for d in dl if d not in excl],
            specimens=[m["slug"]], tags=["luster"], diff=2, accept=m["luster"], explanation=f"{m['name']}: {', '.join(m['luster'])} luster.")
        metal = "metallic" in m["luster"] and "dull" not in m["luster"]
        tf("3h.iii", f"{m['name']} has a metallic luster.", metal or "metallic" in m["luster"], specimens=[m["slug"]],
           tags=["luster"], diff=1, explanation=f"{m['name']}: {', '.join(m['luster'])}.")


def cleavage():
    words = {0: "no cleavage", 1: "1 direction", 2: "2 directions", 3: "3 directions", 4: "4 directions", 6: "6 directions"}
    for m in MS:
        n, q, d = m["cleave"]
        if q in ("poor", "fair") or (n == 0 and q != "none"):
            continue
        mcq("3h.iii", f"How many directions of cleavage does {m['name']} have?", words[n], list(words.values()),
            specimens=[m["slug"]], tags=["cleavage"], diff=2, explanation=f"{m['name']}: {d}.")
    special = {"halite": "cubic (3 directions at 90°)", "galena": "cubic (3 directions at 90°)",
               "calcite": "rhombohedral (3 directions not at 90°)", "dolomite": "rhombohedral (3 directions not at 90°)",
               "rhodochrosite": "rhombohedral (3 directions not at 90°)", "fluorite": "octahedral (4 directions)",
               "diamond": "octahedral (4 directions)", "sphalerite": "dodecahedral (6 directions)",
               "muscovite": "basal (1 direction)", "biotite": "basal (1 direction)", "talc": "basal (1 direction)",
               "graphite": "basal (1 direction)", "topaz": "basal (1 direction)", "lepidolite": "basal (1 direction)",
               "hornblende": "prismatic, 2 directions at about 56° and 124°", "actinolite": "prismatic, 2 directions at about 56° and 124°",
               "augite": "prismatic, 2 directions at about 87° and 93°", "orthoclase-microcline": "2 directions at 90°"}
    kinds = sorted(set(special.values()))
    for s, k in special.items():
        m = MINERALS[s]
        mcq("3h.iii", f"Which best describes the cleavage of {m['name']}?", k, kinds, specimens=[s], tags=["cleavage"], diff=2,
            explanation=f"{m['name']}: {m['cleave'][2]}.")
    for a, b in [("hornblende", "augite"), ("actinolite", "augite"), ("hornblende", "spodumene")]:
        A, B = MINERALS[a], MINERALS[b]
        add("frq", "3h.iii", f"{A['name']} and {B['name']} can look alike in hand sample. How can cleavage angles tell them apart?",
            f"{A['name']} (an amphibole) has two cleavages at about 56° and 124°; {B['name']} (a pyroxene) has two cleavages at nearly 90° (87°/93°).",
            keypoints=["amphibole 56/124 degrees", "pyroxene ~90 degrees"], specimens=[a, b], tags=["cleavage", "distinguish"], diff=2)
    for m in MS:
        if m["cleave"][0] == 0 and m["cleave"][1] == "none" and "conchoidal" in m["fracture"]:
            tf("3h.iii", f"{m['name']} breaks with a conchoidal fracture rather than along cleavage planes.", True,
               specimens=[m["slug"]], tags=["fracture"], diff=1, explanation=f"{m['name']}: no cleavage; {m['fracture']} fracture.")
    for m in MS:
        if m["fracture"] == "hackly":
            tf("3h.iii", f"{m['name']} shows a hackly (jagged) fracture.", True, specimens=[m["slug"]], tags=["fracture"],
               explanation="Native metals break with hackly fracture.")


def density():
    for m in MS:
        d = sg_mid(m)
        dist = ["%.1f" % sg_mid(o) for o in MS if abs(sg_mid(o) - d) >= (0.6 if d < 4 else 1.2)]
        mcq("3h.iii", f"What is the approximate specific gravity of {m['name']}?", "%.1f" % d, dist, specimens=[m["slug"]],
            tags=["specific gravity"], diff=3 if d < 5 else 2, explanation=f"{m['name']}: SG {fmt_range(*m['SG'])}.")
    for _ in range(200):
        four = RNG.sample(MS, 4)
        four.sort(key=sg_mid)
        if any(abs(sg_mid(x) - sg_mid(y)) < 0.5 for x, y in itertools.combinations(four, 2)):
            continue
        add("order", "3h.iii", f"Rank these minerals from lowest to highest specific gravity: {', '.join(sorted(m['name'] for m in four))}.",
            [m["name"] for m in four], specimens=[m["slug"] for m in four], tags=["specific gravity", "ranking"], diff=3,
            explanation="; ".join(f"{m['name']} {sg_mid(m)}" for m in four))
    # heft: which feels heaviest
    for _ in range(140):
        three = RNG.sample(MS, 3)
        three.sort(key=lambda m: -sg_mid(m))
        if sg_mid(three[0]) - sg_mid(three[1]) < 1.0:
            continue
        mcq("3h.iii", f"Three same-sized specimens of {', '.join(sorted(m['name'] for m in three))} are picked up. "
            "Which one has the greatest heft?", three[0]["name"], [m["name"] for m in three[1:]], n=2,
            specimens=[m["slug"] for m in three], tags=["specific gravity", "heft"], diff=2,
            explanation=f"Highest SG: {three[0]['name']} ({sg_mid(three[0])}).")
    # density calculations: mass + water displacement -> identify
    cands = [m for m in MS if m["SG"][1] - m["SG"][0] <= 0.3]
    for m in cands:
        for _ in range(2):
            vol = RNG.choice([4, 5, 8, 10, 12, 15, 20, 25])
            sg = round(RNG.uniform(*m["SG"]), 2)
            mass = round(sg * vol, 1)
            others = [o for o in cands if abs(sg_mid(o) - sg) > 0.45 and not same_species(o, m)]
            if len(others) < 3:
                continue
            opts = RNG.sample(others, 3)
            q = mcq("3h.iii", f"A specimen has a mass of {mass} g and displaces {vol} mL of water. Based on its specific gravity, "
                    f"which mineral is it most likely to be?", m["name"], [o["name"] for o in opts],
                    specimens=[m["slug"]], tags=["specific gravity", "calculation"], diff=3,
                    explanation=f"SG = {mass}/{vol} = {mass/vol:.2f}, matching {m['name']} ({fmt_range(*m['SG'])}).")
        L, W, H = RNG.choice([2, 3, 4]), RNG.choice([2, 3, 5]), RNG.choice([1, 2, 3])
        sgm = sg_mid(m)
        add("numeric", "3h.iii", f"A rectangular cleavage block of {m['name']} (SG ≈ {sgm}) measures {L} cm x {W} cm x {H} cm. "
            "What is its mass in grams? (nearest gram)", round(L * W * H * sgm), tolerance=max(1, round(L * W * H * sgm * 0.02)),
            unit="g", specimens=[m["slug"]], tags=["specific gravity", "calculation"], diff=2,
            explanation=f"V = {L*W*H} cm³; mass = V x SG = {L*W*H*sgm:.0f} g.")
    for _ in range(60):
        dry = RNG.choice([20.0, 30.0, 45.0, 60.0, 80.0, 120.0])
        m = RNG.choice(cands)
        sg = sg_mid(m)
        wet = round(dry - dry / sg, 1)
        add("numeric", "3h.iii", f"A mineral weighs {dry} g in air and {wet} g when suspended in water. What is its specific gravity? "
            "(two decimals)", round(dry / (dry - wet), 2), tolerance=0.05, tags=["specific gravity", "calculation"], diff=3,
            explanation=f"SG = weight in air / (weight in air - weight in water) = {dry}/{dry - wet:.1f} = {dry/(dry-wet):.2f}.")


def other_properties():
    cold = [m for m in MS if "cold" in m["special"].get("acid", "") and "powder" not in m["special"].get("acid", "")]
    warm_or_powder = [m for m in MS if m["special"].get("acid") and m not in cold]
    no_acid = [m for m in MS if not m["special"].get("acid") and m["cls"] not in ("carbonate",)]
    for m in cold:
        mcq("3h.iv", "Which of these minerals effervesces readily in cold, dilute hydrochloric acid?", m["name"],
            [o["name"] for o in no_acid + warm_or_powder], specimens=[m["slug"]], tags=["acid test"], diff=1,
            explanation=f"{m['name']} {m['special']['acid']}.")
        tf("3h.iv", f"{m['name']} fizzes in cold, dilute HCl.", True, specimens=[m["slug"]], tags=["acid test"], diff=1,
           explanation=m["special"]["acid"])
    for m in warm_or_powder:
        add("short", "3h.iv", f"How does {m['name']} react to dilute HCl?", m["special"]["acid"],
            accept=[m["special"]["acid"], "powder" if "powder" in m["special"]["acid"] else "warm"], specimens=[m["slug"]],
            tags=["acid test"], diff=2, explanation=m["special"]["acid"])
        tf("3h.iv", f"{m['name']} fizzes vigorously in cold, dilute HCl as a whole specimen.", False, specimens=[m["slug"]],
           tags=["acid test"], diff=2, explanation=f"{m['name']} {m['special']['acid']}.")
    for m in no_acid[::2]:
        tf("3h.iv", f"{m['name']} effervesces in dilute HCl.", False, specimens=[m["slug"]], tags=["acid test"], diff=1,
           explanation=f"{m['name']} is not a carbonate and does not fizz.")
    signature = {
        "magnetite": "strong magnetism", "halite": "salty taste", "calcite": "double refraction", "ulexite": "fiber-optic 'TV' effect",
        "kyanite": "hardness that differs with direction", "willemite": "bright green fluorescence under short-wave UV",
        "tourmaline": "pyroelectricity (attracts dust when heated)", "rock-crystal": "piezoelectricity",
        "labradorite": "labradorescence (iridescent flash)", "graphite": "greasy feel and marks paper", "talc": "soapy feel",
        "sulfur": "smell of sulfur", "stibnite": "melts in a match flame", "kaolinite": "clay smell when breathed on",
        "zircon": "slight radioactivity", "tigers-eye": "chatoyancy", "opal": "play-of-color", "fluorite": "the namesake of fluorescence",
        "bornite": "iridescent purple-blue tarnish", "copper": "malleability and a hackly fracture", "barite": "high SG for a light-colored mineral",
        "aventurine": "aventurescence (glittering inclusions)", "pyrite": "sparks when struck with steel", "diamond": "very high dispersion ('fire')",
        "sodalite": "orange fluorescence and tenebrescence (hackmanite)", "dolomite": "fizzes only when powdered",
    }
    keys = list(signature)
    for s, p in signature.items():
        m = MINERALS[s]
        mcq("3h.iv", f"{m['name']} is best known for which property?", p, [signature[k] for k in keys if k != s],
            specimens=[s], tags=["special property"], diff=1, explanation=f"{m['name']}: {p}.")
        mcq("3h.iv", f"Which mineral is known for {p}?", m["name"], [MINERALS[k]["name"] for k in keys if k != s],
            specimens=[s], tags=["special property"], diff=1, explanation=f"{p.capitalize()}: {m['name']}.")
    for m in MS:
        mag = m["slug"] == "magnetite"
        if mag or m["slug"] not in ("hematite", "siderite", "pyrolusite", "goethite-limonite"):
            if mag or RNG.random() < 0.3:
                tf("3h.iv", f"A hand magnet is strongly attracted to {m['name']}.", mag, specimens=[m["slug"]], tags=["magnetism"],
                   explanation="Of the listed minerals only magnetite is strongly magnetic.")
    for m in MS:
        if "fluor" in m["special"]:
            short("3h.iv", f"Describe the fluorescence of {m['name']}.", m["special"]["fluor"], [m["special"]["fluor"], "fluoresces", "yes"],
                  specimens=[m["slug"]], tags=["fluorescence"], diff=2, explanation=m["special"]["fluor"])
        if "piezo" in m["special"]:
            tf("3h.iv", f"{m['name']} is piezoelectric (produces a voltage when squeezed).", True, specimens=[m["slug"]],
               tags=["piezoelectricity"], explanation=m["special"]["piezo"])
    for m in MS:
        ten = m["tenacity"]
        dist = ["brittle", "malleable and ductile", "flexible and elastic", "flexible but inelastic", "sectile"]
        key = ("malleable and ductile" if "malleable" in ten else "flexible and elastic" if "elastic" in ten and "inelastic" not in ten
               else "flexible but inelastic" if "inelastic" in ten else "brittle" if ten == "brittle" else None)
        if key:
            mcq("3h.iii", f"Which term best describes the tenacity of {m['name']}?", key, [d for d in dist if d != key and not (key.startswith('flexible but') and d == 'sectile')],
                specimens=[m["slug"]], tags=["tenacity"], diff=2 if key != "brittle" else 1, explanation=f"{m['name']}: {ten}.")
        dia = m["dia"]
        if dia in ("opaque", "transparent"):
            tf("3h.iii", f"{m['name']} is typically {dia}.", True, specimens=[m["slug"]], tags=["diaphaneity"], diff=1,
               explanation=f"{m['name']}: {dia}.")


def habits():
    HAB = ["acicular", "bladed", "botryoidal", "cubic", "dendritic", "dodecahedral", "doubly terminated", "druzy", "geodic",
           "hexagonal", "hopper", "massive", "micaceous", "octahedral", "pisolitic", "prismatic", "radiating", "rosette",
           "stalactitic", "twinning", "tabular"]
    defs = {"acicular": "needle-like", "bladed": "flattened like a knife blade", "botryoidal": "rounded, grape-like masses",
            "cubic": "cube-shaped", "dendritic": "branching, tree- or fern-like", "dodecahedral": "twelve-sided (rhombic faces)",
            "doubly terminated": "pointed at both ends", "druzy": "a coating of many tiny crystals on a surface",
            "geodic": "crystals lining a hollow cavity", "hexagonal": "six-sided prisms", "hopper": "skeletal crystals with stepped, hollow faces",
            "massive": "no visible crystal form", "micaceous": "thin, flaky sheets", "octahedral": "eight-sided (two pyramids base-to-base)",
            "pisolitic": "pea-sized rounded grains", "prismatic": "elongated crystals with parallel faces", "radiating": "crystals spreading from a central point",
            "rosette": "flower-like arrangement of platy crystals", "stalactitic": "icicle-like forms", "twinning": "two or more crystals intergrown symmetrically",
            "tabular": "flat, tablet-shaped"}
    for h, d in defs.items():
        mcq("3h.v", f"Which habit term describes crystals that are {d}?", h, list(defs), tags=["habit"], diff=1,
            explanation=f"{h.capitalize()}: {d}.")
    famous = {"malachite": "botryoidal", "copper": "dendritic", "pyrolusite": "dendritic", "halite": "hopper", "galena": "cubic",
              "magnetite": "octahedral", "almandine": "dodecahedral", "muscovite": "micaceous", "kyanite": "bladed",
              "stibnite": "radiating", "barite": "rosette", "rhodochrosite": "stalactitic", "staurolite": "twinning",
              "beryl": "hexagonal", "amethyst": "geodic", "celestite": "geodic", "rutile": "acicular", "hematite": "botryoidal",
              "rock-crystal": "doubly terminated", "apophyllite": "prismatic", "biotite": "micaceous", "fluorite": "cubic",
              "pyrite": "cubic", "goethite-limonite": "botryoidal", "selenite": "tabular", "satin-spar": "acicular"}
    for s, h in famous.items():
        m = MINERALS[s]
        mcq("3h.v", f"Which habit is {m['name']} especially well known for?", h, [x for x in HAB if x not in m["habits"]],
            specimens=[s], tags=["habit"], diff=2, accept=m["habits"] + [h], explanation=f"{m['name']} is classically {h} ({defs[h]}).")
    for m in MS:
        tw = m.get("twinning")
        if tw:
            short("3h.v", f"Describe the twinning typical of {m['name']}.", tw, [tw], specimens=[m["slug"]], tags=["twinning"],
                  diff=3, explanation=tw)


def color_and_cause():
    for m in MS:
        cc = m.get("color_cause")
        if not cc:
            continue
        dist = [o["color_cause"] for o in MS if o.get("color_cause") and o["slug"] != m["slug"] and
                o.get("variety_of") != m.get("variety_of") and o["color_cause"] != cc]
        mcq("3h.vi", f"What causes the color of {m['name']}?", cc, dist, specimens=[m["slug"]], tags=["color", "trace elements"],
            diff=3, explanation=f"{m['name']}: {cc}.")
    idio = ["azurite", "malachite", "rhodochrosite", "dioptase", "chrysocolla", "olivine"]
    allo = ["corundum", "beryl", "amethyst", "smoky-quartz", "citrine", "rose-quartz", "fluorite"]
    for s in idio:
        tf("3h.vi", f"The color of {MINERALS[s]['name']} comes from an essential element in its formula (idiochromatic).", True,
           specimens=[s], tags=["color"], diff=3, explanation=MINERALS[s].get("color_cause") or "")
    for s in allo:
        tf("3h.vi", f"The color of {MINERALS[s]['name']} comes from an essential element in its formula (idiochromatic).", False,
           specimens=[s], tags=["color"], diff=3, explanation=f"Allochromatic: {MINERALS[s].get('color_cause') or 'trace impurities'}.")


# ---------------------------------------------------------------- varieties, polymorphs, series
def varieties():
    pairs = []
    for m in MS:
        for v, d in m["varieties"].items():
            pairs.append((v, m, d))
    species_name = lambda m: {"Orthoclase / Microcline": "orthoclase"}.get(m["name"], m["name"])
    for v, m, d in pairs:
        others = [species_name(o) for o in MS if o["slug"] != m["slug"] and not same_species(o, m)]
        mcq("3h.xii.2", f"{v.capitalize()} is a variety of which mineral?", m["name"], others, specimens=[m["slug"]],
            tags=["variety", "gem"], diff=1, explanation=f"{v.capitalize()}: {d}.")
    gemlist = [("emerald", "beryl", "green, colored by chromium or vanadium"), ("aquamarine", "beryl", "blue, colored by iron"),
               ("morganite", "beryl", "pink, colored by manganese"), ("kunzite", "spodumene", "pink to lilac, colored by manganese"),
               ("hiddenite", "spodumene", "green, colored by chromium"), ("peridot", "olivine", "yellow-green gem olivine"),
               ("ruby", "corundum", "red, colored by chromium"), ("sapphire", "corundum", "blue (iron + titanium) or any non-red color")]
    for g, s, d in gemlist:
        others = ["beryl", "spodumene", "olivine", "corundum", "topaz", "tourmaline", "quartz", "zircon"]
        mcq("3h.xii.2", f"The gem {g} is a variety of:", MINERALS[s]["name"].lower(), [o for o in others if o != s],
            specimens=[s], tags=["gem", "variety"], diff=1, explanation=f"{g.capitalize()} is {d} {s}.")
        short("3h.xii.2", f"What mineral species is {g} a variety of?", MINERALS[s]["name"], [s], specimens=[s], tags=["gem"],
              diff=1, explanation=f"{g.capitalize()}: {d}.")
        mcq("3h.xii.2", f"What gives {g} its characteristic color?", d.split(", ", 1)[-1] if ", " in d else d,
            [x[2].split(", ", 1)[-1] for x in gemlist if x[0] != g and x[2] != d and ", " in x[2]], specimens=[s],
            tags=["gem", "color"], diff=3, explanation=f"{g.capitalize()}: {d}.")
    pearl = ("Pearls are made mainly of which mineral, deposited by mollusks?", "aragonite", ["calcite", "dolomite", "opal", "barite"])
    mcq("3h.xii.2", pearl[0], pearl[1], pearl[2], specimens=["aragonite"], tags=["gem", "organic gem"], diff=2,
        explanation="Nacre is aragonite platelets bound by conchiolin protein.")
    tf("3h.i", "Amber is a mineral.", False, tags=["mineraloid", "gem"], diff=1,
       explanation="Amber is fossilized tree resin - organic and non-crystalline, so it is not a mineral.")
    tf("3h.i", "Pearl is a mineral.", False, tags=["mineraloid", "gem"], diff=2,
       explanation="Pearl is made biologically of aragonite plus organic conchiolin; it is an organic gem, not a mineral.")
    birth = {"January": "garnet", "February": "amethyst", "March": "aquamarine", "April": "diamond", "May": "emerald",
             "August": "peridot", "October": "opal or tourmaline", "November": "topaz or citrine", "December": "turquoise, zircon or tanzanite"}
    for mo, g in birth.items():
        mcq("3h.xii.2", f"Which gem is a traditional birthstone for {mo}?", g, [v for k, v in birth.items() if k != mo],
            tags=["gem", "birthstone"], diff=2, explanation=f"{mo}: {g}.")


def polymorphs_series():
    poly = [("calcite", "aragonite", "CaCO3", "Aragonite is the high-pressure form; calcite is stable at Earth's surface."),
            ("diamond", "graphite", "C", "Diamond forms at the high pressures of the mantle; graphite is stable at the surface."),
            ("kyanite", "andalusite / sillimanite", "Al2SiO5", "Kyanite = high pressure, andalusite = low pressure, sillimanite = high temperature."),
            ("orthoclase-microcline", "sanidine", "KAlSi3O8", "Sanidine (high-T), orthoclase (intermediate), microcline (low-T)."),
            ("rutile", "anatase / brookite", "TiO2", "All three are TiO2 polymorphs.")]
    for a, b, f, e in poly:
        A = MINERALS[a]
        short("3h.vii", f"Name a polymorph of {A['name']} ({f}).", b.split(" / ")[0], b.split(" / ") + ([A["name"]] if False else []),
              specimens=[a], tags=["polymorph"], diff=2, explanation=e)
        tf("3h.vii", f"{A['name']} and {b.split(' / ')[0]} are polymorphs: same composition ({f}), different crystal structures.", True,
           specimens=[a], tags=["polymorph"], diff=1, explanation=e)
    nonpoly = [("calcite", "dolomite"), ("pyrite", "chalcopyrite"), ("hematite", "magnetite"), ("muscovite", "biotite"),
               ("albite", "orthoclase-microcline"), ("barite", "celestite"), ("galena", "sphalerite")]
    for a, b in nonpoly:
        tf("3h.vii", f"{MINERALS[a]['name']} and {MINERALS[b]['name']} are polymorphs.", False, specimens=[a, b], tags=["polymorph"],
           diff=2, explanation=f"They have different compositions ({MINERALS[a]['formula']} vs {MINERALS[b]['formula']}).")
    mcq("3h.vii", "Which pair are polymorphs?", "diamond and graphite",
        ["calcite and dolomite", "pyrite and chalcopyrite", "galena and sphalerite", "hematite and magnetite", "barite and celestite"],
        tags=["polymorph"], diff=1, explanation="Both are pure carbon.")
    mcq("3h.vii", "Which pair are polymorphs?", "calcite and aragonite",
        ["calcite and dolomite", "hematite and magnetite", "muscovite and biotite", "albite and anorthite"], tags=["polymorph"],
        diff=1, explanation="Both are CaCO3.")
    mcq("3h.vii", "Which pair are polymorphs?", "kyanite and sillimanite",
        ["kyanite and staurolite", "albite and anorthite", "barite and celestite", "pyrite and chalcopyrite"], tags=["polymorph"],
        diff=2, explanation="Both are Al2SiO5.")
    series = [m for m in MS if m["series"]]
    for m in series:
        nm, ends, note = m["series"]
        if m["slug"] in [e for e in ends]:
            partner = [e for e in ends if e != m["slug"]]
            nm2 = ", ".join(partner)
            short("3h.vi.1", f"{m['name']} forms a solid solution series with which mineral(s)?", partner[0],
                  partner + [p.capitalize() for p in partner], specimens=[m["slug"]], tags=["solid solution"], diff=2,
                  explanation=note)
        add("frq", "3h.vi.1", f"Explain the substitution that makes {m['name']} part of the {nm} solid solution series.", note,
            keypoints=[note], specimens=[m["slug"]], tags=["solid solution"], diff=3)


def environments():
    CATS = {"hydrothermal": "hydrothermal", "evaporit": "evaporite", "pegmatite": "pegmatite", "oxidized": "oxidized zone",
            "metamorph": "metamorphic", "skarn": "metamorphic", "schist": "metamorphic", "basalt": "basalt cavities",
            "mantle": "mantle", "fumarole": "volcanic", "placer": "placer", "weathering": "weathering", "sediment": "sedimentary",
            "igneous": "igneous", "granite": "igneous", "gabbro": "igneous", "syenite": "igneous", "shell": "biological",
            "cave": "caves", "precipitation": "sedimentary", "banded iron": "sedimentary", "kimberlite": "mantle"}

    def cats(m):
        txt = " ".join(m["env"]).lower()
        return {c for k, c in CATS.items() if k in txt}
    for m in MS:
        mc = cats(m)
        pool = [o["env"][0] for o in MS if not (cats(o) & mc) and not same_species(o, m)]
        mcq("3h.ix", f"In which environment does {m['name']} typically form?", m["env"][0], pool, specimens=[m["slug"]],
            tags=["environment"], diff=2, accept=m["env"], explanation=f"{m['name']}: " + "; ".join(m["env"]) + ".")
    groupings = {
        "evaporite deposits": ["halite", "selenite", "alabaster", "satin-spar", "ulexite", "celestite"],
        "the oxidized (supergene) zone above copper deposits": ["azurite", "malachite", "chrysocolla", "dioptase", "turquoise"],
        "granite pegmatites": ["beryl", "lepidolite", "spodumene", "tourmaline", "topaz", "amazonite"],
        "gas cavities (vesicles) in basalt": ["apophyllite", "stilbite", "prehnite"],
        "medium- to high-grade metamorphism of shale": ["almandine", "kyanite", "staurolite"],
        "mafic and ultramafic igneous rocks": ["olivine", "augite", "labradorite"],
        "contact-metamorphosed (skarn) limestone": ["grossular", "wollastonite"],
        "the oxidized zone of lead deposits": ["pyromorphite", "vanadinite"],
        "metamorphosed zinc deposits at Franklin, New Jersey": ["willemite", "zincite"],
    }
    allg = [s for v in groupings.values() for s in v]
    for env, slugs in groupings.items():
        for s in slugs:
            outs = [MINERALS[o]["name"] for o in allg if o not in slugs]
            mcq("3h.x", f"Which mineral is characteristic of {env}?", MINERALS[s]["name"], outs, specimens=[s],
                tags=["environment"], diff=2, explanation=f"{MINERALS[s]['name']} forms in {env}.")
        if len(slugs) >= 3:
            three = RNG.sample(slugs, 3)
            odd = RNG.choice([o for o in allg if o not in slugs])
            mcq("3h.x", f"Three of these minerals are typical of {env}. Which one is NOT?", MINERALS[odd]["name"],
                [MINERALS[t]["name"] for t in three], specimens=three + [odd], tags=["environment", "odd one out"], diff=2,
                explanation=f"{MINERALS[odd]['name']}: {MINERALS[odd]['env'][0]}.")


def uses():
    GENERIC = ("gem", "ornamental", "collector", "jewelry", "lapidary", "carving", "decorative", "indicator", "beads")
    for m in MS:
        u = next((x for x in m["uses"] if not any(g in x.lower() for g in GENERIC)), None)
        if not u:
            continue
        pool = [x for o in MS if not same_species(o, m) and not set(o["ore"]) & set(m["ore"])
                for x in o["uses"] if not any(g in x.lower() for g in GENERIC)]
        mcq("3h.xii.1", f"What is a major use of {m['name']}?", u, pool, specimens=[m["slug"]], tags=["uses"], diff=2, accept=m["uses"],
            explanation=f"{m['name']}: " + "; ".join(m["uses"]) + ".")
        mcq("3h.xii.1", f"Which mineral is used for: {u}?", m["name"],
            [o["name"] for o in MS if not same_species(o, m) and not set(o["ore"]) & set(m["ore"]) and
             not any(w in " ".join(o["uses"]).lower() for w in u.lower().split()[:2])],
            specimens=[m["slug"]], tags=["uses"], diff=2, explanation=f"{m['name']}: {u}.")


def etymology():
    ms = [m for m in MS if m["etym"]]
    for m in ms:
        mcq("3h.ii", f"The name '{m['name']}' comes from:", m["etym"], [o["etym"] for o in ms if o["slug"] != m["slug"]],
            specimens=[m["slug"]], tags=["etymology"], diff=3, explanation=m["etym"])
        mcq("3h.ii", f"Which mineral's name comes from: {m['etym']}?", m["name"], [o["name"] for o in ms if o["slug"] != m["slug"]],
            specimens=[m["slug"]], tags=["etymology"], diff=3, explanation=m["etym"])


# ---------------------------------------------------------------- identification
def identification():
    def clues(m):
        c = [("hardness", f"hardness {hstr(m)}"), ("streak", f"{m['streak']} streak"),
             ("luster", f"{' to '.join(m['luster'][:2])} luster"), ("color", f"color: {', '.join(m['colors'][:3])}"),
             ("cleave", m["cleave"][2] if m["cleave"][0] else f"no cleavage, {m['fracture']} fracture"),
             ("sg", f"specific gravity about {sg_mid(m)}")] + ([("system", f"{m['system']} crystal system")] if m["system"] in SYSTEMS else []) + [
             ("class", f"{article(m['cls'])} {m['cls']}")]
        if m["habits"]:
            c.append(("habit", f"often {m['habits'][0]}"))
        for k, v in m["special"].items():
            c.append(("special:" + k, v))
        return c

    def consistent(o, kind, m):
        if kind == "hardness":
            return overlap(o["H"], m["H"], 0.25)
        if kind == "streak":
            return streak_cat(o["streak"]) == streak_cat(m["streak"])
        if kind == "luster":
            return bool(set(o["luster"]) & set(m["luster"][:2]))
        if kind == "color":
            return any(any(w in oc for w in mc.split()) for oc in o["colors"] for mc in m["colors"][:3])
        if kind == "cleave":
            return o["cleave"][0] == m["cleave"][0]
        if kind == "sg":
            return abs(sg_mid(o) - sg_mid(m)) < 0.35
        if kind == "system":
            return o["system"] == m["system"]
        if kind == "class":
            return o["cls"] == m["cls"]
        if kind == "habit":
            return m["habits"][0] in o["habits"]
        if kind.startswith("special:"):
            return kind[8:] in o["special"]
        return True

    for m in MS:
        cl = clues(m)
        made = 0
        for attempt in range(200):
            k = RNG.choice([3, 4, 4, 5])
            chosen = RNG.sample(cl, min(k, len(cl)))
            matches = [o for o in MS if all(consistent(o, kind, m) for kind, _ in chosen)]
            if len(matches) != 1:
                continue
            text = "; ".join(v for _, v in chosen)
            prompt = f"Identify the mineral: {text}."
            similar = [o["name"] for o in MS if o["slug"] != m["slug"] and sum(consistent(o, kind, m) for kind, _ in chosen) >= len(chosen) - 1]
            if made % 2 == 0 and len(similar) >= 3:
                q = mcq("3h.ii", prompt, m["name"], similar, specimens=[m["slug"]], tags=["identification", "properties"], diff=2,
                        explanation=f"Only {m['name']} fits all of these.")
            else:
                q = short("3h.ii", prompt, m["name"], mineral_accept(m), specimens=[m["slug"]], tags=["identification", "properties"],
                          diff=3, explanation=f"Only {m['name']} fits all of these.")
            if q:
                made += 1
            if made >= 16:
                break
        # clue line
        short("3h.ii", f"Identify the mineral: {m['clue']}.", m["name"], mineral_accept(m), specimens=[m["slug"]],
              tags=["identification"], diff=1, explanation=m["clue"])
        lookalike = [o["name"] for o in MS if o["slug"] != m["slug"] and not same_species(o, m) and
                     (o["cls"] == m["cls"] or streak_cat(o["streak"]) == streak_cat(m["streak"]))]
        mcq("3h.ii", f"Which mineral matches this description: {m['clue']}?", m["name"], lookalike, specimens=[m["slug"]],
            tags=["identification"], diff=1, explanation=m["clue"])
        # image-based identification (photos from the rockid project)
        add("short", "3h.ii", "Identify the specimen shown.", m["name"], accept=mineral_accept(m), specimens=[m["slug"]],
            tags=["identification", "image"], image={"specimen": m["slug"]}, diff=2)
        sib = [o["name"] for o in MS if o["slug"] != m["slug"] and (o["cls"] == m["cls"] or o["group"] == m["group"])]
        mcq("3h.ii", "Identify the specimen shown.", m["name"], sib, specimens=[m["slug"]], tags=["identification", "image"],
            image={"specimen": m["slug"]}, diff=1)


def distinguish_pairs():
    pairs = [
        ("pyrite", "chalcopyrite", "Pyrite is harder (6-6.5, scratches glass) and pale brass-yellow; chalcopyrite is softer (3.5-4, scratched by a knife), deeper yellow and often iridescent."),
        ("pyrite", "gold", "Gold is soft, malleable and very heavy (SG ~19) with a yellow streak; pyrite is hard, brittle and has a greenish-black streak."),
        ("chalcopyrite", "gold", "Gold has a yellow streak and is malleable; chalcopyrite has a greenish-black streak and is brittle."),
        ("hematite", "magnetite", "Hematite has a reddish-brown streak and is not (or only weakly) magnetic; magnetite has a black streak and is strongly magnetic."),
        ("calcite", "rock-crystal", "Calcite is hardness 3, has rhombohedral cleavage and fizzes in HCl; quartz is hardness 7 with conchoidal fracture and no fizz."),
        ("calcite", "dolomite", "Calcite fizzes strongly in cold dilute HCl; dolomite fizzes only when powdered."),
        ("halite", "calcite", "Halite tastes salty and has cubic cleavage (90°); calcite has rhombohedral cleavage and fizzes in acid."),
        ("halite", "fluorite", "Halite (H 2.5) has cubic cleavage and tastes salty; fluorite (H 4) has octahedral cleavage."),
        ("muscovite", "biotite", "Muscovite is colorless to silvery and potassium/aluminum-rich; biotite is black/brown because it contains iron and magnesium."),
        ("orthoclase-microcline", "albite", "Plagioclase (albite) shows fine parallel striations from polysynthetic twinning; K-feldspar does not and is often pink."),
        ("fluorapatite", "beryl", "Both form hexagonal prisms, but apatite is hardness 5 (scratched by a knife) while beryl is 7.5-8."),
        ("sodalite", "azurite", "Sodalite has a white streak and does not fizz; azurite has a light blue streak and fizzes in HCl."),
        ("turquoise", "chrysocolla", "Turquoise is harder (5-6); chrysocolla is softer (2-4) and lighter."),
        ("galena", "stibnite", "Galena forms cubes with cubic cleavage; stibnite forms long, striated, bladed prisms."),
        ("sphalerite", "galena", "Sphalerite has a pale yellow-brown streak and resinous luster; galena has a lead-gray streak and metallic luster."),
        ("barite", "calcite", "Barite is much denser (SG ~4.5 vs 2.7) and does not fizz in acid."),
        ("selenite", "muscovite", "Both split into sheets, but selenite (gypsum) sheets are inelastic and it can be scratched by a fingernail; mica sheets spring back."),
        ("talc", "kaolinite", "Talc feels soapy and is hardness 1; kaolinite is earthy and smells of clay when breathed on."),
        ("diamond", "rock-crystal", "Diamond is hardness 10 with adamantine luster and octahedral cleavage; quartz is 7, vitreous, with conchoidal fracture."),
        ("amethyst", "fluorite", "Purple fluorite is hardness 4 with octahedral cleavage; amethyst is 7 with no cleavage."),
        ("olivine", "epidote", "Olivine is olive green, granular, with no good cleavage, in mafic igneous rocks; epidote is pistachio green, striated, with one perfect cleavage, in metamorphic rocks."),
        ("almandine", "grossular", "Almandine is iron-aluminum garnet (deep red, schists); grossular is calcium-aluminum garnet (green/orange/yellow, skarns)."),
        ("rhodochrosite", "rhodonite", "Rhodochrosite is a carbonate (hardness 3.5-4, fizzes in warm HCl); rhodonite is a silicate (5.5-6.5) with black manganese-oxide veins."),
        ("azurite", "malachite", "Azurite is deep blue; malachite is green and banded. Both are copper carbonates that fizz."),
        ("hornblende", "augite", "Hornblende (amphibole) cleaves at 56°/124° and forms long six-sided prisms; augite (pyroxene) cleaves near 90° and forms stubby eight-sided prisms."),
        ("milky-quartz", "albite", "Milky quartz has no cleavage (conchoidal fracture); albite has two cleavages with striations."),
        ("graphite", "pyrolusite", "Both are black and soil fingers, but graphite is greasy and conducts electricity; pyrolusite is manganese oxide with a sooty feel and forms dendrites."),
        ("goethite-limonite", "hematite", "Goethite/limonite has a yellow-brown streak; hematite has a reddish-brown streak."),
    ]
    for a, b, how in pairs:
        A, B = MINERALS[a], MINERALS[b]
        add("frq", "3h.ii", f"How could you distinguish {A['name']} from {B['name']} in hand sample?", how, keypoints=[how],
            specimens=[a, b], tags=["identification", "distinguish"], diff=2)


def mineral_definition():
    items = [("ice", True, "Naturally occurring, inorganic, solid, definite composition (H2O) and crystalline."),
             ("liquid water", False, "Not a solid."), ("table salt made in a factory", False, "Not naturally occurring (synthetic)."),
             ("natural halite", True, "Meets all criteria."), ("obsidian", False, "Volcanic glass - no crystal structure."),
             ("opal", False, "Amorphous - a mineraloid."), ("coal", False, "Organic and of variable composition - a rock."),
             ("amber", False, "Organic resin."), ("pearl", False, "Formed by an organism; aragonite plus organic material."),
             ("granite", False, "A rock - a mixture of several minerals."), ("quartz", True, "Meets all criteria."),
             ("native gold", True, "A native element mineral."), ("synthetic diamond", False, "Not naturally occurring."),
             ("mercury (liquid native metal)", False, "Liquid at room temperature, so it is traditionally not a mineral."),
             ("calcite in a limestone", True, "Naturally occurring crystalline CaCO3.")]
    for thing, ok, why in items:
        tf("3h.i", f"Under the Science Olympiad definition, {thing} is a mineral.", ok, tags=["definition"], diff=1, explanation=why)
    crit = ["naturally occurring", "inorganic", "solid", "definite chemical composition", "crystalline structure"]
    for c in crit:
        mcq("3h.i", "Which of the following is part of the definition of a mineral?", c,
            ["made by living organisms", "can be a liquid", "must be metallic", "must contain silicon", "must be visible to the naked eye",
             "amorphous internal structure"], tags=["definition"], diff=1, explanation="Mineral: " + ", ".join(crit) + ".")


def true_false_mix():
    for m in MS:
        o = RNG.choice([x for x in MS if x["cls"] != m["cls"]])
        tf("3h.viii.1", f"{m['name']} is {article(o['cls'])} {o['cls']}.", False, specimens=[m["slug"]], tags=["class"],
           explanation=f"{m['name']} is {article(m['cls'])} {m['cls']}.")
        tf("3h.viii.1", f"{m['name']} is {article(m['cls'])} {m['cls']}.", True, specimens=[m["slug"]], tags=["class"],
           explanation=f"{m['name']}: {m['formula']}.")
        if m["system"] in SYSTEMS:
            wrong = RNG.choice([s for s in SYSTEMS if s != m["system"] and {s, m["system"]} != {"trigonal", "hexagonal"}])
            tf("3h.viii.3", f"{m['name']} crystallizes in the {wrong} system.", False, specimens=[m["slug"]], tags=["crystal system"],
               explanation=f"{m['name']} is {m['system']}.")
        cat = streak_cat(m["streak"])
        o = RNG.choice([x for x in MS if streak_cat(x["streak"]) != cat])
        tf("3h.iii", f"{m['name']} leaves a {o['streak']} streak.", False, specimens=[m["slug"]], tags=["streak"],
           explanation=f"Its streak is {m['streak']}.")
        tf("3h.iii", f"{m['name']} leaves a {m['streak']} streak.", True, specimens=[m["slug"]], tags=["streak"],
           explanation=f"Streak: {m['streak']}.")
        if m["H"][1] - m["H"][0] <= 1.5:
            o = RNG.choice([x for x in MS if not overlap(x["H"], m["H"], 1)])
            tf("3h.iii", f"{m['name']} has a Mohs hardness of about {hstr(o)}.", False, specimens=[m["slug"]], tags=["hardness"],
               explanation=f"{m['name']} is {hstr(m)}.")
        if m["ore"]:
            wrong = RNG.choice([e for e in ["iron", "copper", "lead", "zinc", "aluminum", "titanium", "lithium", "barium"] if e not in m["ore"]
                                and NAME_TO_SYMBOL[e] not in parse_formula(m.get("calc") or m["formula"])])
            tf("3h.xii.1", f"{m['name']} is an important ore of {wrong}.", False, specimens=[m["slug"]], tags=["ore"],
               explanation=f"{m['name']} is an ore of {', '.join(m['ore'])}.")


def run():
    formulas(); elements_and_ores(); classes(); groups(); crystal_systems(); hardness(); streak_luster(); cleavage()
    density(); other_properties(); habits(); color_and_cause(); varieties(); polymorphs_series(); environments(); uses()
    etymology(); identification(); distinguish_pairs(); mineral_definition(); true_false_mix()
