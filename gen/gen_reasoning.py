"""Reasoning generators: questions answerable from principles rather than memorized facts.

Every question here is tagged with a reasoning tag (see game/lib/kind.js), and its answer follows
from a rule stated in the explanation.
"""
import itertools, math
from common import RNG, add, mcq, tf, short, MINERALS, wt_pct, ELEMENT_NAMES

TAG = "scenario"


# ---------------------------------------------------------------- igneous naming from texture + chemistry
COMP = [("ultramafic", 38, 44), ("mafic", 46, 51), ("intermediate", 54, 62), ("felsic", 66, 76)]
NAMES = {("phaneritic", "felsic"): "granite", ("aphanitic", "felsic"): "rhyolite", ("phaneritic", "intermediate"): "diorite",
         ("aphanitic", "intermediate"): "andesite", ("phaneritic", "mafic"): "gabbro", ("aphanitic", "mafic"): "basalt",
         ("phaneritic", "ultramafic"): "peridotite"}
COLOR = {"felsic": (5, 15), "intermediate": (25, 40), "mafic": (45, 65), "ultramafic": (90, 98)}
WHERE = {"phaneritic": ["a batholith exposed in a mountain range", "the core of an eroded pluton", "a quarry cut deep into a stock"],
         "aphanitic": ["a lava flow on a volcano's flank", "a thin dike", "the chilled top of a flow"]}


def igneous_naming():
    for (tex, comp), name in NAMES.items():
        c = next(x for x in COMP if x[0] == comp)
        for _ in range(9):
            si = RNG.randint(c[1], c[2])
            where = RNG.choice(WHERE[tex])
            grain = "coarse, visible crystals" if tex == "phaneritic" else "crystals too small to see without a lens"
            short("3i.iv.2", f"A rock from {where} has {grain} and contains {si}% SiO2. Name the rock.", name.capitalize(), [name],
                  specimens=[name], tags=[TAG, "classification"], diff=2,
                  explanation=f"{si}% SiO2 is {comp}; {tex} texture -> {name}.")
        lo, hi = COLOR[comp]
        for _ in range(5):
            ci = RNG.randint(lo, hi)
            short("3i.iv.2", f"An igneous rock is {'coarse-grained' if tex == 'phaneritic' else 'fine-grained'} with a color index of {ci} "
                  "(percent dark minerals). Name the most likely rock.", name.capitalize(), [name], specimens=[name],
                  tags=[TAG, "classification"], diff=2, explanation=f"Color index {ci} suggests {comp}; {tex} -> {name}.")
    # the glassy/vesicular family
    for desc, ans in [("frothy, pale, glassy and floats on water", "pumice"), ("dark red-black, full of holes, and sinks in water", "scoria"),
                      ("black, glassy, and breaks with razor-sharp conchoidal edges", "obsidian"),
                      ("made of compacted volcanic ash fragments", "tuff")]:
        for setting in ["after an explosive eruption", "near a volcano", "in a volcanic field"]:
            short("3i.iv.1", f"You find a rock {setting} that is {desc}. Name it.", ans.capitalize(), [ans], specimens=[ans],
                  tags=[TAG, "cooling"], diff=1)
    # silica vs viscosity vs eruption style
    for comp, visc, style in [("felsic", "high", "explosive"), ("mafic", "low", "effusive (gentle lava flows)")]:
        tf("3i.iv.3", f"A {comp} magma would be expected to have {visc} viscosity and a {style.split(' ')[0]} eruption style.", True,
           tags=[TAG, "magma"], diff=1)
    tf("3i.iv.3", "A magma with 48% SiO2 would usually erupt more explosively than one with 72% SiO2.", False, tags=[TAG, "magma"], diff=2,
       explanation="Higher silica = more viscous = traps gas = more explosive.")


# ---------------------------------------------------------------- metamorphic naming from protolith + conditions
COND = {
    "low": [("about 300 °C at 10 km depth", "greenschist"), ("about 350 °C and 0.3 GPa", "greenschist")],
    "medium": [("about 550 °C at 20 km depth", "amphibolite"), ("about 600 °C and 0.6 GPa", "amphibolite")],
    "high": [("about 750 °C at 30 km depth", "upper amphibolite to granulite"), ("about 800 °C and 0.9 GPa", "granulite")],
}
PRODUCT = {
    ("shale", "low"): (["Slate", "Phyllite"], "slate"), ("shale", "medium"): (["Mica Schist", "Garnet Schist", "Schist"], "mica-schist"),
    ("shale", "high"): (["Gneiss"], "gneiss"), ("basalt", "medium"): (["Amphibolite"], "amphibolite"),
    ("basalt", "high"): (["Amphibolite", "Granulite"], "amphibolite"),
    ("limestone", "low"): (["Marble"], "marble"), ("limestone", "medium"): (["Marble"], "marble"), ("limestone", "high"): (["Marble"], "marble"),
    ("quartz sandstone", "low"): (["Quartzite"], "quartzite"), ("quartz sandstone", "medium"): (["Quartzite"], "quartzite"),
    ("quartz sandstone", "high"): (["Quartzite"], "quartzite"), ("granite", "high"): (["Gneiss"], "gneiss"),
}


def metamorphic_naming():
    for (proto, grade), (answers, slug) in PRODUCT.items():
        for desc, facies in COND[grade]:
            for setting in ["during a continental collision", "deep in a mountain belt"]:
                short("3i.vi.4", f"{proto.capitalize()} is metamorphosed {setting} at {desc}. What rock most likely forms?", answers[0],
                      [a.lower() for a in answers], specimens=[slug], tags=[TAG, "protolith", "grade"], diff=2,
                      explanation=f"{proto.capitalize()} at {grade} grade ({facies} facies) becomes {' or '.join(answers).lower()}.")
    for proto, ans, slug in [("peridotite", "serpentinite", "serpentinite"), ("dunite", "serpentinite", "serpentinite")]:
        short("3i.vi.4", f"Seawater circulates through hot {proto} beneath a mid-ocean ridge, hydrating its olivine. What rock forms?", ans.capitalize(),
              [ans, "serpentine"], specimens=[slug], tags=[TAG, "protolith"], diff=2)
    for proto, ans in [("shale", "hornfels"), ("mudstone", "hornfels")]:
        short("3i.vi.5", f"A thin layer of {proto} is baked at 650 °C and very low pressure next to a granite intrusion. What rock forms?", ans.capitalize(),
              [ans], tags=[TAG, "metamorphism type"], diff=2, explanation="High T, low P contact metamorphism of fine sediment -> hornfels.")
    # foliated or not, reasoned from composition + stress
    for proto, fol, why in [("shale", "foliated", "platy clay and mica minerals align under directed pressure"),
                            ("pure limestone", "non-foliated", "calcite grains are equant, so they recrystallize without aligning"),
                            ("quartz sandstone", "non-foliated", "quartz grains are equant and recrystallize without aligning"),
                            ("granite", "foliated (banded)", "micas and hornblende align and segregate into bands at high grade")]:
        mcq("3i.vi.1", f"If {proto} undergoes regional metamorphism, will the resulting rock be foliated or non-foliated?", fol,
            ["foliated", "non-foliated", "foliated (banded)"] if fol != "foliated" else ["foliated", "non-foliated"], n=1 if fol == "foliated" else 2,
            tags=[TAG, "protolith"], diff=2, explanation=why)


# ---------------------------------------------------------------- index-mineral maps
ZONES = ["chlorite", "biotite", "garnet", "staurolite", "kyanite", "sillimanite"]
DIRS = ["north", "south", "east", "west"]
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def index_maps():
    for _ in range(45):
        k = RNG.randint(3, 5)
        start = RNG.randint(0, len(ZONES) - k)
        seq = ZONES[start:start + k]
        d = RNG.choice(DIRS)
        rev = RNG.random() < 0.5
        listed = seq[::-1] if rev else seq
        toward = OPP[d] if rev else d
        mcq("3i.vi.6", f"Walking {d} across a metamorphic terrane, a geologist passes through these zones in order: {', '.join(listed)}. "
            "In which direction does metamorphic grade increase?", toward, [x for x in DIRS if x != toward], tags=[TAG, "index minerals"], diff=2,
            explanation=f"{seq[0]} -> {seq[-1]} is increasing grade.")
        hottest = listed[0] if rev else listed[-1]
        mcq("3i.vi.6", f"Zones mapped in order: {', '.join(listed)}. Which zone experienced the highest temperature?", hottest,
            [z for z in listed if z != hottest], tags=[TAG, "index minerals"], diff=1)
    for _ in range(15):
        z = RNG.sample(ZONES, 2)
        a, b = sorted(z, key=ZONES.index)
        add("frq", "3i.vi.6", f"Schist A contains {a} as its highest-grade index mineral and schist B contains {b}. Which reached higher "
            "temperature, and why?", f"Schist B, because {b} forms at a higher metamorphic grade (temperature) than {a}.",
            keypoints=[f"schist B", f"{b} higher grade"], tags=[TAG, "index minerals"], diff=2, source="generated")


# ---------------------------------------------------------------- Bowen's series: what forms next
DISC = ["olivine", "pyroxene", "amphibole", "biotite"]


def bowen_next():
    for i in range(len(DISC) - 1):
        done = DISC[:i + 1]
        mcq("3h.xi", f"A cooling magma has so far crystallized {', '.join(done)}. On the discontinuous branch, which mineral forms next?",
            DISC[i + 1], [m for m in DISC + ["quartz", "muscovite"] if m not in done and m != DISC[i + 1]], tags=[TAG, "Bowen"], diff=2)
    for rock, have, absent in [("a granite", "quartz and K-feldspar", "olivine"), ("a basalt", "olivine and Ca-plagioclase", "quartz"),
                               ("a gabbro", "pyroxene and Ca-plagioclase", "muscovite"), ("a rhyolite", "quartz and sanidine", "olivine")]:
        tf("3h.xi", f"Bowen's series predicts that {rock} containing {have} would also commonly contain {absent}.", False, tags=[TAG, "Bowen"], diff=2,
           explanation=f"{absent.capitalize()} crystallizes at a very different temperature/composition from {have}.")
    for t, m in [(1200, "olivine and Ca-rich plagioclase"), (1000, "pyroxene and Ca-Na plagioclase"), (850, "amphibole and intermediate plagioclase"),
                 (700, "biotite, Na-rich plagioclase, K-feldspar and quartz")]:
        mcq("3h.xi", f"Roughly which minerals would be crystallizing from a typical magma at about {t} °C?", m,
            ["olivine and Ca-rich plagioclase", "pyroxene and Ca-Na plagioclase", "amphibole and intermediate plagioclase",
             "biotite, Na-rich plagioclase, K-feldspar and quartz"], tags=[TAG, "Bowen"], diff=3)
    for a, b in itertools.combinations(["olivine", "pyroxene", "amphibole", "biotite", "K-feldspar", "muscovite", "quartz"], 2):
        mcq("3h.xi", f"A granite and a basalt weather side by side in a humid climate. Which of their minerals - {a} or {b} - will break down first?",
            a, [b], n=1, tags=[TAG, "Goldich", "weathering"], diff=2, explanation="Minerals that crystallize at higher temperature weather faster (Goldich).")


# ---------------------------------------------------------------- evaporite stages
def evaporites():
    stages = [((40, 55), "calcite (carbonates)"), ((15, 25), "gypsum"), ((5, 10), "halite"), ((1, 3), "potassium and magnesium salts")]
    for (lo, hi), m in stages:
        for v in range(lo, hi + 1, 2 if hi - lo > 4 else 1):
            mcq("3h.ix", f"A restricted lagoon of seawater has evaporated to about {v}% of its original volume. Which mineral is most likely "
                "precipitating now?", m, [s[1] for s in stages if s[1] != m], tags=[TAG, "mineral formation"], diff=3,
                explanation="Seawater evaporites: carbonates (~50%), gypsum (~20%), halite (~10%), K-Mg salts (<5% remaining).")
    for first, second in [("gypsum", "halite"), ("calcite", "gypsum"), ("calcite", "halite")]:
        mcq("3h.ix", f"In an evaporite sequence, which normally lies lower (precipitated first): {first} or {second}?", first, [second], n=1,
            tags=[TAG, "mineral formation"], diff=2, explanation="Less soluble minerals precipitate first and lie lower.")


# ---------------------------------------------------------------- climate & weathering
def weathering():
    cases = [("hot and humid (tropical rainforest)", "chemical"), ("cold with daily freeze-thaw cycles", "mechanical"),
             ("hot and dry with large day-night temperature swings", "mechanical"), ("warm and wet", "chemical"),
             ("polar and dry", "mechanical"), ("humid temperate forest", "chemical")]
    for cl, kind in cases:
        for rock in ["granite", "basalt", "sandstone"]:
            mcq("3i.vii", f"A {rock} outcrop sits in a {cl} climate. Which type of weathering dominates?", kind, ["chemical", "mechanical"], n=1,
                tags=[TAG, "weathering"], diff=1)
    for rock, climate, product in [("granite", "hot and humid", "clay (kaolinite) and loose quartz sand"),
                                   ("basalt", "hot and humid", "iron-rich, red laterite soil"),
                                   ("limestone", "wet", "dissolved calcium and bicarbonate (caves and sinkholes)"),
                                   ("feldspar-rich rock", "tropical", "bauxite after long, intense leaching")]:
        mcq("3i.vii", f"What product would you expect from intense chemical weathering of {rock} in a {climate} climate?", product,
            ["clay (kaolinite) and loose quartz sand", "iron-rich, red laterite soil", "dissolved calcium and bicarbonate (caves and sinkholes)",
             "bauxite after long, intense leaching", "fresh angular olivine sand"], tags=[TAG, "weathering"], diff=2)


# ---------------------------------------------------------------- Hjulström (clear-cut points only)
def hjulstrom():
    cases = [("0.5 mm sand", 100, "eroded"), ("0.5 mm sand", 1, "deposited"), ("50 mm pebbles", 20, "deposited"),
             ("50 mm pebbles", 400, "eroded"), ("0.001 mm clay already in suspension", 5, "transported (kept in suspension)"),
             ("2 mm granules", 2, "deposited"), ("0.2 mm sand", 150, "eroded"), ("100 mm cobbles", 30, "deposited")]
    for grain, v, fate in cases:
        mcq("3i.v.3", f"Using the Hjulström curve, what happens to {grain} in a stream flowing at about {v} cm/s?", fate,
            ["eroded", "deposited", "transported (kept in suspension)"], n=2, tags=[TAG, "Hjulström", "stream velocity"], diff=3)
    for before, after, outcome in [(200, 20, "gravel drops out first, then sand, while clay stays suspended"),
                                   (50, 0.5, "nearly all sand and silt settle out; only the finest clay stays suspended")]:
        mcq("3i.v.3", f"A flood slows from about {before} cm/s to {after} cm/s. What happens to its sediment load?", outcome,
            ["gravel drops out first, then sand, while clay stays suspended",
             "nearly all sand and silt settle out; only the finest clay stays suspended", "clay settles first, then gravel",
             "nothing settles until the water stops completely"], n=3, tags=[TAG, "Hjulström", "stream velocity"], diff=2)


# ---------------------------------------------------------------- tectonic setting from clues
CLUES = [
    ("pillow basalt, sheeted dikes and gabbro, with hydrothermally altered greenstone", "mid-ocean ridge"),
    ("a chain of andesite stratovolcanoes inland from a deep trench, with granite-diorite batholiths beneath", "ocean-continent subduction zone"),
    ("an arc of basaltic-andesite islands next to a trench, all on oceanic crust", "ocean-ocean subduction zone"),
    ("folded marble, schist and gneiss with granite intrusions, and marine fossils high on mountain peaks", "continent-continent collision"),
    ("blueschist and eclogite in a jumble of scraped-off deep-sea sediment", "subduction-zone accretionary wedge"),
    ("a long valley with normal faults, basalt and rhyolite flows, and arkose filling the basins", "continental rift"),
    ("a line of basalt shield volcanoes that get older away from one active volcano, in the middle of an ocean plate", "oceanic hotspot"),
    ("huge rhyolite calderas and thick welded tuffs in the middle of a continent, far from any plate boundary", "continental hotspot"),
    ("crushed fault breccia and mylonite with almost no volcanism, along a long strike-slip fault", "transform boundary"),
]


def settings():
    names = [c[1] for c in CLUES]
    for clue, ans in CLUES:
        for lead in ["A field team maps", "A region shows", "An ancient terrane preserves"]:
            mcq("3i.iv.5", f"{lead} {clue}. What plate-tectonic setting does this record?", ans, [n for n in names if n != ans],
                tags=[TAG, "plate setting"], diff=2)


# ---------------------------------------------------------------- silicate structure from Si:O
SIL = [("Mg2SiO4 (forsterite)", "SiO4", "nesosilicate"), ("ZrSiO4 (zircon)", "SiO4", "nesosilicate"),
       ("Fe3Al2(SiO4)3 (almandine)", "SiO4", "nesosilicate"), ("Al2SiO5 (kyanite)", "SiO4 + extra O", "nesosilicate"),
       ("Ca2(Al,Fe)3(SiO4)(Si2O7)O(OH) (epidote)", "Si2O7 pairs", "sorosilicate"),
       ("Be3Al2Si6O18 (beryl)", "Si6O18 rings", "cyclosilicate"), ("CuSiO3·H2O (dioptase)", "Si6O18 rings", "cyclosilicate"),
       ("LiAlSi2O6 (spodumene)", "Si2O6 = SiO3 chains", "inosilicate (single chain)"),
       ("MnSiO3 (rhodonite)", "SiO3 chains", "inosilicate (single chain)"),
       ("Ca2Mg5Si8O22(OH)2 (tremolite)", "Si8O22 = Si4O11 double chains", "inosilicate (double chain)"),
       ("Mg3Si4O10(OH)2 (talc)", "Si4O10 = Si2O5 sheets", "phyllosilicate"), ("Al2Si2O5(OH)4 (kaolinite)", "Si2O5 sheets", "phyllosilicate"),
       ("KAlSi3O8 (orthoclase)", "(AlSi3)O8 = TO2 framework", "tectosilicate"), ("SiO2 (quartz)", "SiO2 framework", "tectosilicate"),
       ("NaAlSi3O8 (albite)", "(AlSi3)O8 framework", "tectosilicate")]


def silicate_ratio():
    opts = ["nesosilicate", "sorosilicate", "cyclosilicate", "inosilicate (single chain)", "inosilicate (double chain)", "phyllosilicate", "tectosilicate"]
    for f, unit, s in SIL:
        mcq("3h.viii.2", f"The formula {f} contains the silicate unit {unit}. What silicate structure is it?", s,
            [o for o in opts if o != s], tags=[TAG, "classification"], diff=2,
            explanation="SiO4 isolated; Si2O7 pairs; Si6O18 rings / SiO3 single chains; Si4O11 double chains; Si2O5 sheets; SiO2 framework.")


# ---------------------------------------------------------------- ore grade and tonnage
def ore_grade():
    ores = [("chalcopyrite", "Cu"), ("galena", "Pb"), ("sphalerite", "Zn"), ("hematite", "Fe"), ("magnetite", "Fe"), ("bornite", "Cu"),
            ("stibnite", "Sb"), ("barite", "Ba")]
    for slug, el in ores:
        m = MINERALS[slug]
        pct = wt_pct(m["calc"], el)
        for grade in (1, 2, 5, 10, 20):
            kg = 1000 * grade / 100 * pct / 100
            add("numeric", "3h.xii.1", f"An ore body is {grade}% {m['name']} ({m['calc']}) by mass. How many kilograms of {ELEMENT_NAMES[el]} does one "
                "metric ton (1000 kg) of ore contain? (nearest 0.1 kg)", round(kg, 1), tolerance=max(0.1, round(kg * 0.03, 1)), unit="kg",
                specimens=[slug], tags=[TAG, "calculation"], diff=3,
                explanation=f"1000 x {grade/100} x {pct/100:.3f} = {kg:.1f} kg.")


# ---------------------------------------------------------------- dating word problems
def dating():
    for hl, iso, mineral in [(1.25, "K-40", "a biotite in a granite"), (4.47, "U-238", "a zircon"), (0.704, "U-235", "a zircon")]:
        for n in (1, 2, 3):
            age = round(hl * n, 3)
            add("numeric", "3h.xii.1", f"{mineral.capitalize()} has {100 / 2 ** n:g}% of its original {iso} left (half-life {hl} billion years). "
                "How old is it, in billions of years?", age, tolerance=round(hl * 0.05, 3), unit="billion years", tags=[TAG, "radiometric dating", "calculation"],
                diff=2, explanation=f"{n} half-lives x {hl} = {age} billion years.")
    tf("3h.xii.1", "If a zircon lost some lead during later metamorphism, its U-Pb age would come out too young.", True,
       tags=[TAG, "radiometric dating"], diff=3, explanation="Losing daughter lead lowers D/P, giving a younger apparent age.")
    tf("3h.xii.1", "A mineral that gains extra daughter isotope after forming will give an age that is too young.", False,
       tags=[TAG, "radiometric dating"], diff=3, explanation="Extra daughter raises D/P, making it look older.")


def run():
    igneous_naming(); metamorphic_naming(); index_maps(); bowen_next(); evaporites(); weathering(); hjulstrom(); settings()
    silicate_ratio(); ore_grade(); dating()
