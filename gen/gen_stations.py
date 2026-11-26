"""Station-style chains: a specimen image, then follow-ups that refer to 'this specimen' without naming it.

Every part carries  station = {"id": "<slug>-<n>", "part": k}  so the game can present them in order;
part 1 is always the identification.
"""
from common import MINERALS, ROCKS, RNG, add, mineral_accept, rock_accept, article, fmt_range
from gen_minerals import CLASSES, SYSTEMS, SIL_ALL, sil_of, streak_cat, same_species, sg_mid

MS = list(MINERALS.values())
RS = list(ROCKS.values())


def opts(correct, pool, n=3):
    pool = [p for p in dict.fromkeys(pool) if p != correct]
    if len(pool) < n:
        return None
    return [correct] + RNG.sample(pool, n)


def chain(slug, kind, parts, variant):
    sid = f"{slug}-{variant}"
    k = 0
    for fmt, topic, prompt, answer, extra in parts:
        if fmt == "mcq" and not extra.get("options"):
            continue
        k += 1
        kw = dict(extra)
        tags = kw.pop("tags", [])
        q = add(fmt, topic, f"[Specimen {variant}] {prompt}", answer, specimens=[slug], image={"specimen": slug}, tags=["station"] + tags, **kw)
        if q:
            q["station"] = {"id": sid, "part": k}


def mineral_chains():
    for m in MS:
        GEN = ("gem", "ornamental", "collector", "jewelry", "lapidary", "carving", "decorative", "indicator", "beads")
        use = next((u for u in m["uses"] if not any(g in u for g in GEN)), m["uses"][0])
        use_pool = [u for o in MS if not same_species(o, m) and not set(o["ore"]) & set(m["ore"]) for u in o["uses"]
                    if not any(g in u for g in GEN)]
        env_pool = [o["env"][0] for o in MS if o["cls"] != m["cls"] and not same_species(o, m)]
        streak_pool = list({streak_cat(o["streak"]): o["streak"] for o in MS if streak_cat(o["streak"]) != streak_cat(m["streak"])}.values())
        hard_pool = [fmt_range(*o["H"]) for o in MS if o["H"][1] - o["H"][0] <= 1.5 and (o["H"][0] > m["H"][1] + 0.5 or o["H"][1] < m["H"][0] - 0.5)]
        ident = ("short", "3h.ii", "Identify this specimen.", m["name"], {"accept": mineral_accept(m), "diff": 2})
        base = [
            ("mcq", "3h.vi", "What is the chemical formula of this specimen?", m["formula"],
             {"options": opts(m["formula"], [o["formula"] for o in MS if o["formula"] != m["formula"]]), "diff": 2}),
            ("mcq", "3h.viii.1", "To which chemical class does this specimen belong?", m["cls"],
             {"options": opts(m["cls"], CLASSES), "diff": 1}),
            ("mcq", "3h.iii", "What color streak would this specimen leave?", m["streak"], {"options": opts(m["streak"], streak_pool), "diff": 2}),
            ("mcq", "3h.ix", "In what environment does this specimen typically form?", m["env"][0],
             {"options": opts(m["env"][0], env_pool), "diff": 2, "accept": m["env"]}),
            ("mcq", "3h.xii.1", "What is an important use of this specimen?", use, {"options": opts(use, use_pool), "diff": 2, "accept": m["uses"]}),
        ]
        if m["H"][1] - m["H"][0] <= 1.5:
            base.append(("mcq", "3h.iii", "What is this specimen's Mohs hardness?", fmt_range(*m["H"]),
                         {"options": opts(fmt_range(*m["H"]), hard_pool), "diff": 2}))
        if m["system"] in SYSTEMS:
            bad = {"trigonal": "hexagonal", "hexagonal": "trigonal"}.get(m["system"])
            base.append(("mcq", "3h.viii.3", "What is this specimen's crystal system?", m["system"],
                         {"options": opts(m["system"], [s for s in SYSTEMS if s != bad]), "diff": 2}))
        if sil_of(m):
            base.append(("mcq", "3h.viii.2", "What type of silicate is this specimen?", sil_of(m), {"options": opts(sil_of(m), SIL_ALL), "diff": 2}))
        if m["ore"]:
            base.append(("short", "3h.xii.1", "This specimen is an ore of which element?", m["ore"][0], {"accept": m["ore"], "diff": 1}))
        if m["special"].get("acid"):
            base.append(("short", "3h.iv", "How does this specimen react with dilute HCl?", m["special"]["acid"],
                         {"accept": [m["special"]["acid"], "fizzes", "effervesces"], "diff": 2}))
        if m["cleave"][1] not in ("poor", "fair"):
            n = m["cleave"][0]
            base.append(("mcq", "3h.iii", "How many directions of cleavage does this specimen have?", "none" if n == 0 else str(n),
                         {"options": opts("none" if n == 0 else str(n), ["none", "1", "2", "3", "4", "6"]), "diff": 2}))
        if m.get("etym"):
            base.append(("mcq", "3h.ii", "Where does this specimen's name come from?", m["etym"],
                         {"options": opts(m["etym"], [o["etym"] for o in MS if o.get("etym") and o["slug"] != m["slug"]]), "diff": 3}))
        if m["series"]:
            nm, ends, note = m["series"]
            base.append(("frq", "3h.vi.1", "This specimen belongs to a solid solution series. Name the series and the substitution involved.",
                         f"{nm} series: {note}", {"keypoints": [nm, note], "diff": 3}))
        for v in (1, 2):
            RNG.shuffle(base)
            chain(m["slug"], "mineral", [ident] + base[:6], v)


def rock_chains():
    for r in RS:
        RGEN = ("decorative", "local", "crushed stone", "aggregate", "stone")
        ruse = next((u for u in r["uses"] if not any(g in u for g in RGEN)), r["uses"][0])
        ident = ("short", "3i.ii", "Identify this rock.", r["name"], {"accept": rock_accept(r), "diff": 2})
        base = [("mcq", "3i.iii", "Is this rock igneous, sedimentary, or metamorphic?", r["type"],
                 {"options": opts(r["type"], ["igneous", "sedimentary", "metamorphic"], 2), "diff": 1}),
                ("mcq", "3i.v.5" if r["type"] == "sedimentary" else "3i.iv.3" if r["type"] == "igneous" else "3i.vi.5",
                 "In what environment did this rock form?", r["env"][0],
                 {"options": opts(r["env"][0], [x["env"][0] for x in RS if x["type"] != r["type"]]), "diff": 2, "accept": r["env"]}),
                ("mcq", "3i.viii", "What is an economic use of this rock?", ruse,
                 {"options": opts(ruse, [u for x in RS if x["slug"] != r["slug"] and x["group"] != r["group"] for u in x["uses"]
                                         if u != ruse and not any(g in u for g in RGEN)]), "diff": 2, "accept": r["uses"]})]
        if r["type"] == "igneous":
            if r["comp"] in ("felsic", "intermediate", "mafic", "ultramafic"):
                base.append(("mcq", "3i.iv.2", "What is the composition of this rock?", r["comp"],
                             {"options": opts(r["comp"], ["felsic", "intermediate", "mafic", "ultramafic"]), "diff": 1}))
            base.append(("mcq", "3i.iv.1", "Which texture does this rock show?", r["texture"][0],
                         {"options": opts(r["texture"][0], [t for t in ["aphanitic", "phaneritic", "porphyritic", "vesicular", "glassy",
                                                                        "pyroclastic", "pegmatitic"] if t not in r["texture"]]), "diff": 1}))
            base.append(("mcq", "3i.iv.3", "Is this rock intrusive or extrusive?", "intrusive" if r["sub"] == "intrusive" else "extrusive",
                         {"options": ["intrusive", "extrusive"], "diff": 1}))
            if r["plate"]:
                base.append(("short", "3i.iv.5", "Name a plate-tectonic setting where this rock forms.", r["plate"], {"accept": [r["plate"]], "diff": 2}))
        if r["type"] == "sedimentary":
            base.append(("mcq", "3i.v.1", "Is this rock clastic, chemical, or biochemical?", r["sub"],
                         {"options": opts(r["sub"], ["clastic", "chemical", "biochemical"], 2), "diff": 2}))
            base.append(("short", "3i.v.2", "What is the main component of this rock?", r["minerals"][0], {"accept": [r["minerals"][0]], "diff": 2}))
        if r["type"] == "metamorphic":
            base.append(("mcq", "3i.vi.1", "Is this rock foliated or non-foliated?", r["sub"], {"options": ["foliated", "non-foliated"], "diff": 1}))
            base.append(("short", "3i.vi.4", "What is the protolith of this rock?", r["protolith"], {"accept": [r["protolith"]] + r["protolith"].replace(" or ", "/").replace(" (", "/").replace(")", "").split("/"), "diff": 2}))
            if r["grade"]:
                base.append(("short", "3i.vi.6", "What metamorphic grade does this rock represent?", r["grade"], {"accept": [r["grade"]], "diff": 2}))
        for v in (1, 2):
            RNG.shuffle(base)
            chain(r["slug"], "rock", [ident] + base[:5], v)


def run():
    mineral_chains(); rock_chains()
