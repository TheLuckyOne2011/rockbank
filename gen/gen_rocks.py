"""Rock questions generated from kb/rocks.py."""
import itertools
from common import ROCKS, MINERALS, RNG, add, mcq, tf, short, rock_accept, article

RS = list(ROCKS.values())
IGN = [r for r in RS if r["type"] == "igneous"]
SED = [r for r in RS if r["type"] == "sedimentary"]
MET = [r for r in RS if r["type"] == "metamorphic"]


def same_family(a, b):
    return a["slug"] == b["slug"] or (a["group"] and a["group"] == b["group"])


def classification():
    for r in RS:
        mcq("3i.iii", f"Is {r['name']} igneous, sedimentary or metamorphic?", r["type"], ["igneous", "sedimentary", "metamorphic"],
            n=2, specimens=[r["slug"]], tags=["rock type"], diff=1,
            explanation=f"{r['name']} is {article(r['type'])} {r['type']} rock ({r['sub']}).")
        wrong = RNG.choice([t for t in ("igneous", "sedimentary", "metamorphic") if t != r["type"]])
        tf("3i.iii", f"{r['name']} is {article(wrong)} {wrong} rock.", False, specimens=[r["slug"]], tags=["rock type"], diff=1,
           explanation=f"It is {r['type']}.")
        tf("3i.iii", f"{r['name']} is {article(r['type'])} {r['type']} rock.", True, specimens=[r["slug"]], tags=["rock type"], diff=1)
    for t in ("igneous", "sedimentary", "metamorphic"):
        ins = [r for r in RS if r["type"] == t]
        outs = [r["name"] for r in RS if r["type"] != t]
        for r in ins:
            mcq("3i.iii", f"Which of these rocks is {t}?", r["name"], outs, specimens=[r["slug"]], tags=["rock type"], diff=1,
                explanation=f"{r['name']} is {t}.")
            three = RNG.sample(outs, 3)
            odd_others = [x for x in RS if x["name"] in three]
            if len({x["type"] for x in odd_others}) == 1:
                ot = odd_others[0]["type"]
                mcq("3i.iii", f"Which rock does NOT belong: three are {ot} and one is not.", r["name"], three,
                    specimens=[r["slug"]] + [x["slug"] for x in odd_others], tags=["rock type", "odd one out"], diff=2,
                    explanation=f"{r['name']} is {t}; the others are {ot}.")
    # sedimentary subclass
    for r in SED:
        sub = r["sub"]
        mcq("3i.v.1", f"Is {r['name']} a clastic, chemical or biochemical sedimentary rock?", sub,
            ["clastic", "chemical", "biochemical"], n=2, specimens=[r["slug"]], tags=["sedimentary texture"],
            diff=2, explanation=f"{r['name']}: {sub}.")
    for sub in ("clastic", "chemical", "biochemical"):
        ins = [r for r in SED if r["sub"] == sub]
        outs = [r["name"] for r in SED if r["sub"] != sub and r["slug"] not in ("chert-flint", "oolitic-limestone")]
        for r in ins:
            mcq("3i.v.1", f"Which of these sedimentary rocks is {sub}?", r["name"], outs, specimens=[r["slug"]],
                tags=["sedimentary texture"], diff=2, explanation=f"{r['name']} is {sub}.")
    # metamorphic foliation
    for r in MET:
        fol = r["sub"] == "foliated"
        tf("3i.vi.1", f"{r['name']} is a foliated metamorphic rock.", fol, specimens=[r["slug"]], tags=["foliation"], diff=1,
           explanation=f"{r['name']} is {r['sub']} ({', '.join(r['texture'])}).")
    for r in [x for x in MET if x["sub"] == "non-foliated"]:
        mcq("3i.vi.1", "Which of these metamorphic rocks is non-foliated?", r["name"],
            [x["name"] for x in MET if x["sub"] == "foliated" and x["slug"] != "amphibolite"], specimens=[r["slug"]],
            tags=["foliation"], diff=1, explanation=f"{r['name']} is non-foliated.")
    for r in [x for x in MET if x["sub"] == "foliated" and x["slug"] not in ("amphibolite", "talc-schist")]:
        mcq("3i.vi.1", "Which of these metamorphic rocks is foliated?", r["name"],
            [x["name"] for x in MET if x["sub"] == "non-foliated"], specimens=[r["slug"]], tags=["foliation"], diff=1,
            explanation=f"{r['name']}: {', '.join(r['texture'])}.")
    textures = {"slate": "slaty cleavage", "phyllite": "phyllitic (silky sheen)", "mica-schist": "schistosity",
                "garnet-schist": "schistosity", "gneiss": "gneissic banding"}
    for s, t in textures.items():
        mcq("3i.vi.1", f"What type of foliation does {ROCKS[s]['name']} display?", t, sorted(set(textures.values())),
            specimens=[s], tags=["foliation"], diff=2, explanation=f"{ROCKS[s]['name']}: {t}.")


def igneous():
    for r in IGN:
        if r["comp"] in ("felsic", "intermediate", "mafic", "ultramafic"):
            mcq("3i.iv.2", f"What is the composition of {r['name']}?", r["comp"], ["felsic", "intermediate", "mafic", "ultramafic"],
                specimens=[r["slug"]], tags=["composition"], diff=1, explanation=f"{r['name']}: {r['comp']}; {r['silica']}.")
        sub = {"intrusive": "intrusive (plutonic)", "extrusive": "extrusive (volcanic)", "pyroclastic": "extrusive (volcanic)"}[r["sub"]]
        mcq("3i.iv.3", f"Is {r['name']} intrusive or extrusive?", sub, ["intrusive (plutonic)", "extrusive (volcanic)"], n=1,
            specimens=[r["slug"]], tags=["intrusive/extrusive"], diff=1, explanation=f"{r['name']}: {r['sub']}.")
        for t in r["texture"]:
            pool = ["aphanitic", "phaneritic", "porphyritic", "vesicular", "glassy", "pyroclastic", "pegmatitic"]
            mcq("3i.iv.1", f"Which texture is characteristic of {r['name']}?", t, [p for p in pool if p not in r["texture"]],
                specimens=[r["slug"]], tags=["texture"], diff=2, accept=r["texture"], explanation=f"{r['name']}: {', '.join(r['texture'])}.")
        if r["equiv"] and r["equiv"] in [x["name"].lower() for x in IGN]:
            eq = next(x for x in IGN if x["name"].lower() == r["equiv"])
            mcq("3i.iv.3", f"{r['name']} has the same composition as which {('extrusive' if r['sub'] == 'intrusive' else 'intrusive')} rock?",
                eq["name"], [x["name"] for x in IGN if x["slug"] not in (r["slug"], eq["slug"]) and x["sub"] == eq["sub"]],
                specimens=[r["slug"], eq["slug"]], tags=["equivalents"], diff=1,
                explanation=f"{r['name']} and {eq['name']} are both {r['comp']}.")
        if r["plate"]:
            pool = [x["plate"] for x in IGN if x["plate"] and x["comp"] != r["comp"] and x["slug"] != r["slug"]]
            mcq("3i.iv.5", f"In which tectonic setting does {r['name']} commonly form?", r["plate"], pool, specimens=[r["slug"]],
                tags=["plate tectonics"], diff=2, explanation=f"{r['name']}: {r['plate']}.")
        for mn in r["minerals"][:2]:
            if "glass" in mn or "fragment" in mn or "ash" in mn:
                continue
            pool = ["quartz", "potassium feldspar", "calcium-rich plagioclase", "olivine", "pyroxene (augite)", "hornblende", "muscovite", "calcite",
                    "halite", "garnet", "talc", "kyanite"]
            def present(p):
                return any(p.split()[0] in x for x in r["minerals"])
            mcq("3i.iv.2", f"Which mineral is an essential component of {r['name']}?", mn,
                [p for p in pool if not present(p) and p != mn and not (r["comp"] == "felsic" and p in ("sodium plagioclase",))],
                specimens=[r["slug"]], tags=["composition", "minerals"], diff=2, accept=r["minerals"],
                explanation=f"{r['name']}: " + ", ".join(r["minerals"]) + ".")
    # equivalents table
    pairs = [("granite", "rhyolite"), ("diorite", "andesite"), ("gabbro", "basalt")]
    for a, b in pairs:
        tf("3i.iv.3", f"{ROCKS[a]['name']} is the intrusive equivalent of {ROCKS[b]['name']}.", True, specimens=[a, b],
           tags=["equivalents"], diff=1)
    for (a, _), (_, b) in itertools.permutations(pairs, 2):
        tf("3i.iv.3", f"{ROCKS[a]['name']} is the intrusive equivalent of {ROCKS[b]['name']}.", False, specimens=[a, b],
           tags=["equivalents"], diff=1, explanation=f"{ROCKS[a]['name']} is {ROCKS[a]['comp']}; {ROCKS[b]['name']} is {ROCKS[b]['comp']}.")
    # silica ranking
    order = ["granite", "diorite", "gabbro", "peridotite"]
    ext = ["rhyolite", "andesite", "basalt"]
    for combo in itertools.combinations(order, 3):
        names = [ROCKS[c]["name"] for c in combo]
        add("order", "3i.iv.2", f"Rank from highest to lowest silica content: {', '.join(sorted(names))}.", names,
            specimens=list(combo), tags=["silica", "ranking"], diff=2, explanation="Felsic > intermediate > mafic > ultramafic.")
    for combo in itertools.permutations(ext + ["obsidian"], 2):
        pass
    add("order", "3i.iv.2", "Rank these volcanic rocks from highest to lowest silica content: Andesite, Basalt, Rhyolite.",
        ["Rhyolite", "Andesite", "Basalt"], specimens=ext, tags=["silica", "ranking"], diff=1)
    add("order", "3i.iv.2", "Rank these volcanic rocks from MOST to LEAST viscous lava: Andesite, Basalt, Rhyolite.",
        ["Rhyolite", "Andesite", "Basalt"], specimens=ext, tags=["viscosity", "ranking"], diff=2,
        explanation="Viscosity rises with silica content (more polymerized SiO4 tetrahedra).")
    add("order", "3i.iv.2", "Rank these volcanic rocks from HIGHEST to LOWEST eruption temperature: Andesite, Basalt, Rhyolite.",
        ["Basalt", "Andesite", "Rhyolite"], specimens=ext, tags=["temperature", "ranking"], diff=2,
        explanation="Mafic magmas erupt hottest (~1100-1200 °C); felsic coolest (~700-900 °C).")
    # texture -> cooling history
    tex = {"phaneritic": "slow cooling deep underground (intrusive)", "aphanitic": "fast cooling at or near the surface (extrusive)",
           "porphyritic": "two stages of cooling: slow (phenocrysts) then fast (groundmass)",
           "glassy": "extremely rapid cooling (quenching) with no time for crystals",
           "vesicular": "gas bubbles escaping as lava cooled at the surface",
           "pegmatitic": "crystallization from a water-rich residual melt that let crystals grow very large",
           "pyroclastic": "explosive fragmentation and deposition of volcanic debris"}
    for t, d in tex.items():
        mcq("3i.iv.4", f"What does a {t} texture indicate about an igneous rock's history?", d, list(tex.values()),
            tags=["texture", "cooling"], diff=1, explanation=f"{t.capitalize()}: {d}.")
        mcq("3i.iv.4", f"Which texture results from {d}?", t, list(tex), tags=["texture", "cooling"], diff=1)
    for r in IGN:
        for t in r["texture"][:1]:
            if t in tex:
                short("3i.iv.4", f"{r['name']} has a {t} texture. What does that tell you about how it formed?", tex[t], [tex[t]],
                      specimens=[r["slug"]], tags=["texture", "cooling"], diff=2, explanation=tex[t])


def sedimentary():
    for r in SED:
        mn = r["minerals"][0]
        pool = [x["minerals"][0] for x in SED if x["minerals"][0] != mn and not same_family(x, r)
                and not (r["group"] == "Coal varieties" and x["group"] == "Coal varieties")]
        mcq("3i.v.2", f"What is the main component of {r['name']}?", mn, pool, specimens=[r["slug"]], tags=["composition"], diff=2,
            explanation=f"{r['name']}: " + ", ".join(r["minerals"]) + ".")
        pool = [x["env"][0] for x in SED if x["sub"] != r["sub"] or abs(len(x["env"][0]) - len(r["env"][0])) > -1]
        pool = [p for p in pool if p not in r["env"] and not any(w in p for w in ("marine", "swamp")) or True]
        pool = [x["env"][0] for x in SED if not same_family(x, r) and not set(x["env"]) & set(r["env"]) and
                not (("marine" in x["env"][0]) and ("marine" in r["env"][0]))]
        mcq("3i.v.5", f"In what environment does {r['name']} typically form?", r["env"][0], pool, specimens=[r["slug"]],
            tags=["environment"], diff=2, accept=r["env"], explanation=f"{r['name']}: " + "; ".join(r["env"]) + ".")
        if r.get("acid"):
            fizz = "fizz" in r["acid"] and "only" not in r["acid"] and "not" not in r["acid"]
            tf("3i.v.2", f"{r['name']} fizzes vigorously in cold, dilute HCl.", fizz, specimens=[r["slug"]], tags=["acid test"], diff=1,
               explanation=f"{r['name']}: {r['acid']}.")
    lime = [r for r in SED if r["group"] == "Limestone varieties"]
    for r in lime:
        mcq("3i.v.2", "Which of these rocks would fizz vigorously in cold, dilute HCl?", r["name"],
            ["Quartz Sandstone", "Shale", "Chert / Flint", "Diatomite", "Rock Gypsum", "Bauxite", "Conglomerate"],
            specimens=[r["slug"]], tags=["acid test"], diff=1, explanation=f"{r['name']} is limestone (calcite).")
    # coal rank
    coals = ["lignite", "bituminous", "anthracite"]
    add("order", "3i.v.2", "Rank these coals from lowest to highest rank: Anthracite, Bituminous Coal, Lignite.",
        ["Lignite", "Bituminous Coal", "Anthracite"], specimens=coals, tags=["coal", "ranking"], diff=1,
        explanation="Peat -> lignite -> sub-bituminous -> bituminous -> anthracite.")
    for prop, order, expl in [("carbon content (lowest to highest)", ["Lignite", "Bituminous Coal", "Anthracite"], "Carbon rises with rank."),
                              ("moisture content (highest to lowest)", ["Lignite", "Bituminous Coal", "Anthracite"], "Moisture falls with rank."),
                              ("heat of burning per kilogram (lowest to highest)", ["Lignite", "Bituminous Coal", "Anthracite"],
                               "Heating value generally rises with rank."),
                              ("volatile content (highest to lowest)", ["Lignite", "Bituminous Coal", "Anthracite"],
                               "Volatiles are driven off with increasing rank.")]:
        add("order", "3i.v.2", f"Rank these coals by {prop}: Anthracite, Bituminous Coal, Lignite.", order, specimens=coals,
            tags=["coal", "ranking"], diff=2, explanation=expl)
    for c in coals:
        r = ROCKS[c]
        mcq("3i.v.2", f"Approximately how much fixed carbon does {r['name']} contain?", r["carbon"],
            [ROCKS[o]["carbon"] for o in coals if o != c] + ["over 99% fixed carbon"], specimens=[c], tags=["coal"], diff=3,
            explanation=f"{r['name']}: {r['carbon']} (USGS ranges).")
    mcq("3i.v.2", "Which organic material is the precursor of all coal?", "peat",
        ["kerogen from plankton", "amber", "graphite", "diatoms"], tags=["coal"], diff=1,
        explanation="Coal forms from peat - partly decayed plant matter accumulated in swamps.")
    # clast shape / energy
    trips = [("conglomerate", "rounded", "long transport by high-energy water"), ("breccia", "angular", "little transport; a nearby source")]
    for s, shape, mean in trips:
        mcq("3i.v.3", f"The gravel clasts in {ROCKS[s]['name']} are {shape}. What does that indicate?", mean,
            [t[2] for t in trips if t[0] != s] + ["deposition by evaporation", "deep, still water"], specimens=[s],
            tags=["rounding"], diff=1, explanation=f"{shape.capitalize()} clasts: {mean}.")
    mature = [("quartz-sandstone", "mature"), ("arkose", "immature"), ("greywacke", "immature")]
    for s, mat in mature:
        mcq("3i.v.3", f"Is {ROCKS[s]['name']} texturally and compositionally mature or immature?", mat, ["mature", "immature"], n=1,
            specimens=[s], tags=["maturity"], diff=2, explanation=ROCKS[s].get("other") or ROCKS[s]["grain"])
    add("order", "3i.v.3", "Rank these sandstones from least to most mature: Arkose, Greywacke, Quartz Sandstone.",
        ["Greywacke", "Arkose", "Quartz Sandstone"], specimens=["greywacke", "arkose", "quartz-sandstone"], tags=["maturity", "ranking"],
        diff=3, explanation="Greywacke (muddy matrix, rock fragments) < arkose (feldspar-rich) < quartz sandstone (>90% quartz, rounded).")


def metamorphic():
    proto = {r["slug"]: r["protolith"] for r in MET}
    plist = ["shale", "limestone", "quartz sandstone", "granite", "basalt or gabbro", "peridotite", "coal"]
    simple = {"slate": "shale", "phyllite": "shale", "mica-schist": "shale", "garnet-schist": "shale", "marble": "limestone",
              "quartzite": "quartz sandstone", "amphibolite": "basalt or gabbro", "serpentinite": "peridotite", "talc-schist": "peridotite"}
    for s, p in simple.items():
        r = ROCKS[s]
        mcq("3i.vi.4", f"What is the protolith (parent rock) of {r['name']}?", p, [x for x in plist if x != p and x != "granite"],
            specimens=[s], tags=["protolith"], diff=1, explanation=f"{r['name']} forms from {proto[s]}.")
        short("3i.vi.4", f"Name the protolith of {r['name']}.", p, [p] + p.replace(" or ", "/").split("/") +
              (["mudstone", "claystone"] if p == "shale" else ["dunite"] if p == "peridotite" else ["dolostone"] if p == "limestone" else
               ["sandstone"] if "sandstone" in p else []), specimens=[s], tags=["protolith"], diff=1, explanation=proto[s])
    rev = {"shale": ["slate", "phyllite", "mica-schist", "garnet-schist"], "limestone": ["marble"], "quartz sandstone": ["quartzite"],
           "basalt or gabbro": ["amphibolite"], "peridotite": ["serpentinite", "talc-schist"]}
    for p, outs in rev.items():
        others = [ROCKS[x]["name"] for k, v in rev.items() if k != p for x in v]
        for s in outs:
            mcq("3i.vi.4", f"Metamorphism of {p} can produce which rock?", ROCKS[s]["name"], others, specimens=[s], tags=["protolith"],
                diff=1, explanation=f"{p.capitalize()} -> {ROCKS[s]['name']}.")
    seq = ["Slate", "Phyllite", "Mica Schist", "Gneiss"]
    add("order", "3i.vi.6", "Shale is metamorphosed at increasing grade. Put these rocks in order from lowest to highest grade: "
        "Gneiss, Mica Schist, Phyllite, Slate.", seq, specimens=["slate", "phyllite", "mica-schist", "gneiss"], tags=["grade", "ranking"],
        diff=1, explanation="Slate -> phyllite -> schist -> gneiss (-> migmatite).")
    for a, b in itertools.combinations(range(4), 2):
        mcq("3i.vi.6", f"Which formed at a higher metamorphic grade: {seq[a]} or {seq[b]}?", seq[b], [seq[a]], n=1,
            tags=["grade"], diff=1, explanation=" -> ".join(seq))
    for r in MET:
        if r["grade"]:
            short("3i.vi.6", f"What grade of metamorphism does {r['name']} typically represent?", r["grade"], [r["grade"]] + r["grade"].split(" to "),
                  specimens=[r["slug"]], tags=["grade"], diff=2, explanation=f"{r['name']}: {r['grade']} grade.")
        if r["facies"] and r["facies"] != "any":
            short("3i.vi.7", f"Which metamorphic facies is {r['name']} typical of?", r["facies"], [r["facies"]] + r["facies"].replace(" to ", "/").replace(" (lower)", "").split("/"),
                  specimens=[r["slug"]], tags=["facies"], diff=2, explanation=f"{r['name']}: {r['facies']} facies.")
    for r in MET:
        mn = r["minerals"][0]
        pool = [x["minerals"][0] for x in MET if x["slug"] != r["slug"] and x["minerals"][0].split()[0] not in " ".join(r["minerals"])]
        mcq("3i.vi.2", f"Which mineral dominates {r['name']}?", mn, pool, specimens=[r["slug"]], tags=["composition"], diff=2,
            explanation=f"{r['name']}: " + ", ".join(r["minerals"]) + ".")


def rock_ids_and_uses():
    for r in RS:
        short("3i.ii", f"Identify the rock: {r['clue']}.", r["name"], rock_accept(r), specimens=[r["slug"]], tags=["identification"],
              diff=1, explanation=r["clue"])
        sib = [x["name"] for x in RS if x["slug"] != r["slug"] and x["type"] == r["type"]]
        mcq("3i.ii", f"Which rock matches this description: {r['clue']}?", r["name"], sib, specimens=[r["slug"]],
            tags=["identification"], diff=1, explanation=r["clue"])
        add("short", "3i.ii", "Identify the rock specimen shown.", r["name"], accept=rock_accept(r), specimens=[r["slug"]],
            tags=["identification", "image"], image={"specimen": r["slug"]}, diff=2)
        mcq("3i.ii", "Identify the rock specimen shown.", r["name"], sib, specimens=[r["slug"]], tags=["identification", "image"],
            image={"specimen": r["slug"]}, diff=1)
        add("mcq", "3i.iii", "Is the rock specimen shown igneous, sedimentary, or metamorphic?", r["type"],
            options=["igneous", "sedimentary", "metamorphic"], specimens=[r["slug"]], tags=["rock type", "image"],
            image={"specimen": r["slug"]}, diff=1)
        # structured descriptions
        desc = [f"{r['type']}", f"{r['sub']}", r["grain"]]
        if r["comp"]:
            desc.insert(1, r["comp"])
        short("3i.ii", "Identify the rock: " + "; ".join(desc) + "; minerals: " + ", ".join(r["minerals"][:3]) + ".", r["name"],
              rock_accept(r), specimens=[r["slug"]], tags=["identification", "description"], diff=2)
        GENERIC = ("decorative", "local", "crushed stone", "aggregate")
        u = next((x for x in r["uses"] if not any(g in x for g in GENERIC)), None)
        if u:
            pool = [x for o in RS if o["slug"] != r["slug"] and not same_family(o, r) for x in o["uses"] if not any(g in x for g in GENERIC)
                    and not any(w in x for w in ("building", "dimension", "countertop", "stone"))]
            if any(w in u for w in ("building", "dimension", "countertop", "stone")):
                pool = [p for p in pool]
            mcq("3i.viii", f"What is an important economic use of {r['name']}?", u, pool, specimens=[r["slug"]], tags=["uses"], diff=2, accept=r["uses"],
                explanation=f"{r['name']}: " + "; ".join(r["uses"]) + ".")
        if r.get("etym"):
            short("3i.ii", f"Which rock on the list is named for: {r['etym'].split('named for ')[-1]}?", r["name"], rock_accept(r),
                  specimens=[r["slug"]], tags=["etymology"], diff=3, explanation=r["etym"])


def run():
    classification(); igneous(); sedimentary(); metamorphic(); rock_ids_and_uses()
