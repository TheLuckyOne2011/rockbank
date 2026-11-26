"""Parametric concept questions: Bowen's series, phase diagrams, facies, grain size, compositions, dating."""
import itertools, math
from common import RNG, add, mcq, tf, short

# ---------------------------------------------------------------- Bowen's reaction series
BOWEN = [("olivine", 1), ("pyroxene", 2), ("amphibole", 3), ("biotite", 4), ("potassium feldspar", 5), ("muscovite", 6), ("quartz", 7)]
PLAG = [("calcium-rich plagioclase", 1.5), ("sodium-rich plagioclase", 4)]
ALLB = BOWEN + PLAG
RANK = dict(ALLB)


def bowen():
    for (a, ra), (b, rb) in itertools.combinations(ALLB, 2):
        if abs(ra - rb) < 1.5:
            continue
        first, last = (a, b) if ra < rb else (b, a)
        mcq("3h.xi", f"According to Bowen's reaction series, which crystallizes at a higher temperature: {a} or {b}?", first, [last], n=1,
            tags=["Bowen"], diff=1, explanation=f"{first.capitalize()} forms earlier (hotter) than {last}.")
        mcq("3h.xi", f"Which of these minerals is more resistant to chemical weathering at Earth's surface: {a} or {b}?", last, [first], n=1,
            tags=["Bowen", "weathering", "Goldich"], diff=2,
            explanation="Goldich dissolution series: minerals that crystallize last (closest to surface conditions) weather most slowly.")
    for combo in itertools.combinations(BOWEN, 4):
        names = [c[0] for c in combo]
        add("order", "3h.xi", f"Order these minerals from first to last to crystallize from a cooling magma: {', '.join(sorted(names))}.",
            names, tags=["Bowen", "ranking"], diff=2, explanation="Olivine -> pyroxene -> amphibole -> biotite -> K-feldspar -> muscovite -> quartz.")
    disc = ["olivine", "pyroxene", "amphibole", "biotite"]
    for m in disc:
        mcq("3h.xi", f"On which branch of Bowen's reaction series is {m} found?", "discontinuous branch",
            ["continuous branch", "neither - it forms after both branches merge"], n=2, tags=["Bowen"], diff=1,
            explanation="The discontinuous branch is the ferromagnesian series olivine -> pyroxene -> amphibole -> biotite.")
    mcq("3h.xi", "On which branch of Bowen's reaction series is plagioclase feldspar found?", "continuous branch",
        ["discontinuous branch", "neither - it forms after both branches merge"], n=2, tags=["Bowen"], diff=1,
        explanation="Plagioclase changes composition continuously from Ca-rich to Na-rich without changing structure.")
    for m in ["potassium feldspar", "muscovite", "quartz"]:
        mcq("3h.xi", f"Where does {m} appear in Bowen's reaction series?", "after the two branches merge, at the lowest temperatures",
            ["at the top of the discontinuous branch", "at the top of the continuous branch", "between olivine and pyroxene"], tags=["Bowen"],
            diff=1, explanation="K-feldspar, muscovite and quartz crystallize last.")
    structs = [("olivine", "isolated tetrahedra (nesosilicate)"), ("pyroxene", "single chains"), ("amphibole", "double chains"),
               ("biotite", "sheets"), ("quartz", "framework")]
    for m, s in structs:
        mcq("3h.xi", f"Down the discontinuous series, silicate structures become more polymerized. What structure does {m} have?", s,
            [x[1] for x in structs if x[0] != m], tags=["Bowen", "silicate structure"], diff=2,
            explanation="Olivine (isolated) -> pyroxene (single chain) -> amphibole (double chain) -> biotite (sheet) -> quartz (framework).")
    rocks = [("peridotite", "olivine and pyroxene"), ("gabbro/basalt", "Ca-rich plagioclase, pyroxene and olivine"),
             ("diorite/andesite", "intermediate plagioclase and amphibole"), ("granite/rhyolite", "K-feldspar, Na-plagioclase, quartz and micas")]
    for r, ms in rocks:
        mcq("3h.xi", f"Which Bowen's-series minerals dominate {r}?", ms, [x[1] for x in rocks if x[0] != r], tags=["Bowen"], diff=1)
    for m in ("olivine", "calcium-rich plagioclase", "pyroxene"):
        tf("3h.xi", f"{m.capitalize()} is commonly found together with quartz in granite.", False, tags=["Bowen"], diff=2,
           explanation=f"{m.capitalize()} crystallizes at high temperature from mafic magma; quartz crystallizes last from felsic magma.")
    # fractional crystallization reasoning
    add("frq", "3i.iv.6", "If olivine forms first as any magma cools, why is olivine rarely found in granite?",
        "Olivine crystallizes early and is removed (by settling) or reacts with the melt to form pyroxene; the remaining melt becomes "
        "silica-rich, and by the time granite crystallizes there is excess silica, so quartz forms instead of olivine.",
        keypoints=["early crystals removed or react with melt", "melt becomes silica-rich", "excess silica gives quartz not olivine"],
        tags=["Bowen", "fractional crystallization"], diff=3)


# ---------------------------------------------------------------- metamorphic grade & facies
INDEX = ["chlorite", "muscovite", "biotite", "garnet", "staurolite", "kyanite", "sillimanite"]
FACIES = {
    "zeolite": ((150, 220), (0.1, 0.3), "burial metamorphism of volcanic sediments (very low grade)"),
    "greenschist": ((350, 450), (0.3, 0.6), "low-grade regional metamorphism; seafloor alteration of basalt (chlorite, epidote, actinolite)"),
    "amphibolite": ((550, 650), (0.5, 0.9), "medium- to high-grade regional metamorphism (hornblende + plagioclase)"),
    "granulite": ((800, 900), (0.6, 1.0), "very high-temperature metamorphism of the deep continental crust (pyroxene, no hydrous minerals)"),
    "blueschist": ((250, 350), (0.8, 1.1), "high pressure, low temperature in subduction zones (glaucophane)"),
    "eclogite": ((600, 800), (1.6, 2.2), "very high pressure at depth in subduction zones (garnet + omphacite)"),
    "hornfels": ((550, 750), (0.02, 0.15), "contact metamorphism next to intrusions (high T, low P)"),
}


def metamorphism():
    for a, b in itertools.combinations(range(len(INDEX)), 2):
        mcq("3i.vi.6", f"Which index mineral indicates a higher metamorphic grade: {INDEX[a]} or {INDEX[b]}?", INDEX[b], [INDEX[a]], n=1,
            tags=["index minerals"], diff=1, explanation=" -> ".join(INDEX))
    for combo in itertools.combinations(INDEX, 4):
        add("order", "3i.vi.6", f"Order these index minerals from lowest to highest metamorphic grade: {', '.join(sorted(combo))}.",
            list(combo), tags=["index minerals", "ranking"], diff=2, explanation=" -> ".join(INDEX))
    zones = {"chlorite": "low", "muscovite": "low", "biotite": "low to medium", "garnet": "medium", "staurolite": "medium",
             "kyanite": "medium to high", "sillimanite": "high"}
    for mn, g in zones.items():
        short("3i.vi.6", f"A pelitic schist contains {mn} as its highest-grade index mineral. What metamorphic grade does this indicate?", g,
              [g] + g.split(" to "), tags=["index minerals"], diff=1, explanation=f"{mn.capitalize()} zone: {g} grade.")
    for f, ((t1, t2), (p1, p2), d) in FACIES.items():
        mcq("3i.vi.7", f"Which metamorphic facies matches: {d.split(' (')[0]}?", f, [x for x in FACIES if x != f], tags=["facies"],
            diff=2, explanation=f"{f.capitalize()}: {d}.")
        for _ in range(8):
            T = RNG.randint(t1 // 10, t2 // 10) * 10
            P = round(RNG.uniform(p1, p2), 2)
            depth = round(P * 33)
            mcq("3i.vi.7", f"A rock equilibrated at about {T} °C and {P} GPa (roughly {depth} km depth). Which metamorphic facies is this?",
                f, [x for x in FACIES if x != f], tags=["facies", "P-T"], diff=3,
                explanation=f"{f.capitalize()} facies: about {t1}-{t2} °C, {p1}-{p2} GPa ({d}).")
    settings = {"blueschist": "subduction zone (cold, sinking oceanic crust)", "eclogite": "deep subduction zone",
                "hornfels": "contact aureole around a magma intrusion", "greenschist": "mid-ocean ridge seafloor or shallow mountain belts",
                "granulite": "base of thickened continental crust in collision zones", "amphibolite": "middle crust of continental collision zones"}
    for f, s in settings.items():
        mcq("3i.vi.8", f"In what plate-tectonic setting does {f}-facies metamorphism typically occur?", s,
            [v for k, v in settings.items() if k != f], tags=["facies", "plate tectonics"], diff=2, explanation=f"{f.capitalize()}: {s}.")
    # pressure / depth calculations
    for _ in range(40):
        depth = RNG.choice(range(5, 61, 5))
        add("numeric", "3i.vi.7", f"Assuming pressure in the crust rises by about 1 GPa per 33 km, what is the pressure at {depth} km depth? (GPa, two decimals)",
            round(depth / 33, 2), tolerance=0.03, unit="GPa", tags=["P-T", "calculation"], diff=2,
            explanation=f"{depth}/33 = {depth/33:.2f} GPa.")
        grad = RNG.choice([15, 20, 25, 30, 35])
        add("numeric", "3i.vi.7", f"With a surface temperature of 15 °C and a geothermal gradient of {grad} °C/km, what is the temperature at {depth} km? (°C)",
            15 + grad * depth, tolerance=2, unit="°C", tags=["P-T", "geothermal gradient", "calculation"], diff=2,
            explanation=f"15 + {grad} x {depth} = {15 + grad*depth} °C.")
    # Al2SiO5 phase diagram
    regions = {"kyanite": ((400, 650), (0.8, 1.1)), "andalusite": ((400, 600), (0.05, 0.2)), "sillimanite": ((750, 900), (0.4, 0.7))}
    for poly, ((t1, t2), (p1, p2)) in regions.items():
        for _ in range(12):
            T = RNG.randint(t1 // 10, t2 // 10) * 10
            P = round(RNG.uniform(p1, p2), 2)
            mcq("3h.vi.2", f"On the Al2SiO5 phase diagram (triple point near 500 °C and 0.4 GPa), which polymorph is stable at {T} °C and {P} GPa?",
                poly, [x for x in regions if x != poly], n=2, specimens=["kyanite"], tags=["phase diagram", "Al2SiO5", "polymorph"], diff=3,
                explanation="Kyanite = high pressure; andalusite = low pressure, moderate temperature; sillimanite = high temperature.")
    for poly, d in [("kyanite", "high pressure (and low to moderate temperature)"), ("andalusite", "low pressure"),
                    ("sillimanite", "high temperature")]:
        mcq("3h.vi.2", f"Which Al2SiO5 polymorph is stable at {d}?", poly, [x for x in regions if x != poly], n=2, specimens=["kyanite"],
            tags=["phase diagram", "Al2SiO5"], diff=2)
    add("frq", "3h.vi.2", "What does it mean if kyanite, andalusite and sillimanite are all found in equilibrium in the same rock?",
        "The rock formed at the triple point of the Al2SiO5 phase diagram (about 500 °C and 0.4 GPa), where all three polymorphs are stable together.",
        keypoints=["triple point", "~500 °C, ~0.4 GPa"], specimens=["kyanite"], tags=["phase diagram", "Al2SiO5"], diff=3)
    # contact aureole zoning
    add("order", "3i.vi.5", "Moving AWAY from a granite intrusion through its contact aureole, order the zones encountered: "
        "hornfels, slightly altered shale, spotted slate.", ["hornfels", "spotted slate", "slightly altered shale"],
        tags=["contact metamorphism", "ranking"], diff=2, explanation="Temperature (and grade) decrease with distance from the intrusion.")


# ---------------------------------------------------------------- phase diagrams (binary)
def phase_diagrams():
    # eutectic: diopside (Di) - anorthite (An)
    for _ in range(60):
        E = RNG.choice([35, 40, 42, 45])
        TE = RNG.choice([1270, 1274, 1280])
        X = RNG.choice([x for x in range(10, 91, 5) if abs(x - E) >= 10])
        if X < E:
            L = RNG.choice([x for x in range(X + 5, E + 1)])
            frac = (L - X) / L
            first = "diopside"
            ex = f"Lever rule: solid is pure Di (0% An), liquid {L}% An. Fraction solid = ({L} - {X})/({L} - 0) = {frac:.2f}."
        else:
            L = RNG.choice([x for x in range(E, X - 4)])
            frac = (X - L) / (100 - L)
            first = "anorthite"
            ex = f"Lever rule: solid is pure An (100%), liquid {L}% An. Fraction solid = ({X} - {L})/(100 - {L}) = {frac:.2f}."
        stem = (f"In a simple binary eutectic diagram for diopside (Di) and anorthite (An), the eutectic is at {E}% An and {TE} °C. "
                f"A melt of {X}% An cools until the remaining liquid is {L}% An.")
        add("numeric", "3h.vi.2", stem + " What fraction of the system is crystalline? (two decimals)", round(frac, 2), tolerance=0.02,
            tags=["phase diagram", "lever rule", "eutectic"], diff=3, explanation=ex)
        mcq("3h.vi.2", f"In a Di-An eutectic system (eutectic {E}% An, {TE} °C), which mineral crystallizes first from a melt of {X}% An?",
            first, ["diopside", "anorthite", "both at once", "neither until the eutectic"], tags=["phase diagram", "eutectic"], diff=2,
            explanation=f"The bulk composition lies on the {first} side of the eutectic.")
        mcq("3h.vi.2", f"A {X}% An melt in a Di-An eutectic system (eutectic {E}% An, {TE} °C) cools until fully solid. What is the composition "
            "of the last drop of liquid?", f"{E}% An (the eutectic)", [f"{X}% An", "0% An", "100% An", f"{(X + E)//2}% An"],
            tags=["phase diagram", "eutectic"], diff=2, explanation="The liquid always evolves to the eutectic before the last of it freezes.")
    # solid solution loop (plagioclase, olivine)
    for series, lo, hi, unit in [("plagioclase (albite-anorthite)", "albite", "anorthite", "An"), ("olivine (fayalite-forsterite)", "fayalite", "forsterite", "Fo")]:
        for _ in range(45):
            L = RNG.randint(10, 55)
            S = RNG.randint(L + 15, min(L + 45, 95))
            X = RNG.randint(L + 3, S - 3)
            frac = (X - L) / (S - L)
            add("numeric", "3h.vi.2", f"In the {series} solid-solution system, a bulk composition of {unit}{X} is partly crystallized. At this "
                f"temperature the liquid is {unit}{L} and the crystals are {unit}{S}. What fraction of the system is solid? (two decimals)",
                round(frac, 2), tolerance=0.02, tags=["phase diagram", "lever rule", "solid solution"], diff=3,
                explanation=f"Fraction solid = ({X} - {L})/({S} - {L}) = {frac:.2f}.")
        mcq("3h.vi.2", f"In the {series} system, the first crystals to form from a melt are richer in which end-member than the melt?", hi,
            [lo, "neither - they match the melt"], n=2, tags=["phase diagram", "solid solution"], diff=2,
            explanation=f"The high-melting end-member ({hi}) is concentrated in early crystals.")
    for q, a, d in [
        ("On a phase diagram, what is the line above which a system is entirely liquid?", "liquidus", ["solidus", "solvus", "eutectic line"]),
        ("On a phase diagram, what is the line below which a system is entirely solid?", "solidus", ["liquidus", "solvus", "isograd"]),
        ("What is the lowest temperature at which a mixture of two minerals can be partly molten, where both crystallize together?",
         "eutectic point", ["peritectic point", "triple point", "critical point"]),
        ("A point where three phases (e.g., three polymorphs) coexist at one P and T is called the:", "triple point",
         ["eutectic point", "solvus", "liquidus"]),
        ("Which rule uses the distances on a tie line to find the proportions of two coexisting phases?", "lever rule",
         ["Bowen's rule", "Goldschmidt's rule", "Steno's law"]),
        ("Exsolution in alkali feldspar (forming perthite) happens when a cooling crystal crosses which curve?", "solvus",
         ["liquidus", "solidus", "geotherm"]),
        ("Why does pure forsterite melt at a higher temperature (~1890 °C) than pure fayalite (~1205 °C)?",
         "Mg-O bonds are stronger than Fe-O bonds", ["fayalite has a different crystal system", "forsterite contains water",
                                                     "fayalite is a framework silicate"]),
    ]:
        mcq("3h.vi.2", q, a, d, tags=["phase diagram"], diff=2)


# ---------------------------------------------------------------- compositions
PLAG_NAMES = [(0, 10, "albite"), (10, 30, "oligoclase"), (30, 50, "andesine"), (50, 70, "labradorite"), (70, 90, "bytownite"), (90, 100, "anorthite")]


def compositions():
    for _ in range(90):
        an = RNG.randint(1, 99)
        if any(abs(an - b) <= 2 for b in (10, 30, 50, 70, 90)):
            continue
        name = next(n for lo, hi, n in PLAG_NAMES if lo <= an < hi)
        mcq("3h.vi.1", f"A plagioclase feldspar is An{an} ({an}% anorthite, {100 - an}% albite). What is its name?", name,
            [n for *_, n in PLAG_NAMES], tags=["plagioclase", "solid solution"], diff=2,
            explanation=f"An{an} falls in the {name} range.")
    for lo, hi, n in PLAG_NAMES:
        mcq("3h.vi.1", f"What range of anorthite content defines {n}?", f"An{lo}-An{hi}", [f"An{a}-An{b}" for a, b, m in PLAG_NAMES if m != n],
            tags=["plagioclase"], diff=3)
    tf("3h.vi.1", "In plagioclase, Na+ + Si4+ are replaced by Ca2+ + Al3+ (a coupled substitution) going from albite to anorthite.", True,
       specimens=["albite", "labradorite"], tags=["solid solution"], diff=2)
    for _ in range(70):
        fo = RNG.randint(5, 95)
        mg = round(2 * fo / 100, 2)
        fe = round(2 - mg, 2)
        add("numeric", "3h.vi.1", f"An olivine has the formula (Mg{mg}Fe{fe})SiO4. What is its forsterite content (Fo number, %)?",
            round(100 * mg / (mg + fe)), tolerance=1, unit="%", specimens=["olivine"], tags=["olivine", "solid solution", "calculation"],
            diff=2, explanation=f"Fo = Mg/(Mg+Fe) x 100 = {mg}/2 x 100 = {100*mg/2:.0f}.")
    for _ in range(25):
        fo = RNG.choice([10, 20, 30, 40, 60, 70, 80, 90])
        sg = 3.22 + (4.39 - 3.22) * (100 - fo) / 100
        add("numeric", "3h.vi.1", f"Forsterite (Fo100) has SG 3.22 and fayalite (Fo0) has SG 4.39. Assuming SG changes linearly, estimate the SG of Fo{fo}. (two decimals)",
            round(sg, 2), tolerance=0.03, specimens=["olivine"], tags=["olivine", "solid solution", "calculation"], diff=3,
            explanation=f"3.22 + 1.17 x {(100 - fo)/100:.2f} = {sg:.2f}.")
    for fo, side in [(90, "forsterite"), (15, "fayalite"), (80, "forsterite"), (25, "fayalite")]:
        mcq("3h.vi.1", f"Olivine of composition Fo{fo} is closer to which end-member?", side, ["forsterite", "fayalite"], n=1,
            specimens=["olivine"], tags=["olivine"], diff=1)
    for el, end, oth in [("magnesium", "forsterite (Mg2SiO4)", "fayalite (Fe2SiO4)"), ("iron", "fayalite (Fe2SiO4)", "forsterite (Mg2SiO4)")]:
        mcq("3h.vi.1", f"Which olivine end-member is the {el}-rich one?", end, [oth, "tephroite (Mn2SiO4)", "monticellite (CaMgSiO4)"],
            specimens=["olivine"], tags=["olivine"], diff=1)
    # carbonate & sulfate series
    for (a, b, what) in [("calcite", "rhodochrosite", "Ca and Mn"), ("siderite", "rhodochrosite", "Fe and Mn"), ("magnesite", "siderite", "Mg and Fe"),
                         ("barite", "celestite", "Ba and Sr"), ("tremolite", "actinolite", "Mg and Fe")]:
        short("3h.vi.1", f"Which two cations substitute for each other in the {a}-{b} solid solution?", what, [what, what.replace(" and ", ", ")],
              specimens=[a, b], tags=["solid solution"], diff=2)
    # Silicate ratios
    sil = [("nesosilicate", "SiO4", "1:4", 0, "olivine, garnet, zircon, topaz, kyanite"),
           ("sorosilicate", "Si2O7", "2:7", 1, "epidote"),
           ("cyclosilicate", "Si6O18", "1:3", 2, "beryl, tourmaline, dioptase"),
           ("inosilicate (single chain)", "SiO3", "1:3", 2, "pyroxenes: augite, spodumene"),
           ("inosilicate (double chain)", "Si4O11", "4:11", "2 and 3 (alternating)", "amphiboles: hornblende, tremolite, actinolite"),
           ("phyllosilicate", "Si2O5", "2:5", 3, "micas, talc, kaolinite"),
           ("tectosilicate", "SiO2", "1:2", 4, "quartz, feldspars, sodalite, zeolites")]
    for n, unit, ratio, shared, ex in sil:
        mcq("3h.viii.2", f"Which silicate structure has a basic structural unit of {unit} (Si:O = {ratio})?", n, [s[0] for s in sil if s[0] != n and s[2] != ratio],
            tags=["silicate structure"], diff=2, explanation=f"{n}: {unit}; examples {ex}.")
        mcq("3h.viii.2", f"How many oxygens does each tetrahedron share with neighboring tetrahedra in {n}s?", str(shared),
            [str(s[3]) for s in sil if str(s[3]) != str(shared)], tags=["silicate structure"], diff=2, explanation=f"{n}: shares {shared}.")
        mcq("3h.viii.2", f"Which minerals are examples of {n}s?", ex, [s[4] for s in sil if s[0] != n], tags=["silicate structure"], diff=1)
    add("order", "3h.viii.2", "Order these silicate structures from least to most polymerized (fewest to most shared oxygens): "
        "framework, isolated tetrahedra, sheet, single chain.", ["isolated tetrahedra", "single chain", "sheet", "framework"],
        tags=["silicate structure", "ranking"], diff=2)
    # crystal systems
    axes = {"cubic": "three equal axes, all at 90°", "tetragonal": "two equal axes and one of different length, all at 90°",
            "orthorhombic": "three unequal axes, all at 90°", "monoclinic": "three unequal axes, one angle not 90°",
            "triclinic": "three unequal axes, no angles at 90°", "hexagonal": "three equal horizontal axes at 120° plus a perpendicular vertical axis with six-fold symmetry",
            "trigonal": "like hexagonal axes but with three-fold symmetry about the vertical axis"}
    for s, d in axes.items():
        mcq("3h.viii.3", f"Which crystal system has {d}?", s, [x for x in axes if x != s], tags=["crystal system"], diff=2)
        mcq("3h.viii.3", f"Which describes the axes of the {s} system?", d, [v for k, v in axes.items() if k != s], tags=["crystal system"], diff=2)
    for s, ex in [("cubic", "halite, galena, pyrite, fluorite, garnet"), ("hexagonal", "beryl, apatite"), ("trigonal", "quartz, calcite, corundum, tourmaline"),
                  ("tetragonal", "zircon, rutile, chalcopyrite"), ("orthorhombic", "olivine, topaz, barite, sulfur"),
                  ("monoclinic", "gypsum, micas, hornblende, augite, orthoclase"), ("triclinic", "plagioclase, microcline, kyanite, rhodonite")]:
        mcq("3h.viii.3", f"Which group of minerals all crystallize in the {s} system?", ex,
            ["halite, galena, pyrite, fluorite, garnet", "beryl, apatite", "quartz, calcite, corundum, tourmaline", "zircon, rutile, chalcopyrite",
             "olivine, topaz, barite, sulfur", "gypsum, micas, hornblende, augite, orthoclase", "plagioclase, microcline, kyanite, rhodonite"],
            tags=["crystal system"], diff=2)
    tf("3h.viii.3", "Isotropic (cubic) minerals such as halite and garnet do not show double refraction.", True, tags=["crystal system", "optics"], diff=2)
    tf("3h.viii.3", "Cleavage planes form where atomic bonds within the crystal structure are weakest.", True, tags=["cleavage", "structure"], diff=1)


# ---------------------------------------------------------------- sediments
WENT = [(0, 1 / 256, "clay"), (1 / 256, 1 / 16, "silt"), (1 / 16, 2, "sand"), (2, 4, "granule"), (4, 64, "pebble"),
        (64, 256, "cobble"), (256, 10 ** 6, "boulder")]
ROCK_FOR = {"clay": "shale", "silt": "siltstone", "sand": "sandstone", "granule": "conglomerate or breccia", "pebble": "conglomerate or breccia",
            "cobble": "conglomerate or breccia", "boulder": "conglomerate or breccia"}


def sediments():
    vals = [0.001, 0.002, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 3, 6, 10, 20, 40, 100, 150, 200, 300, 500, 1000]
    for v in vals:
        cls = next(n for lo, hi, n in WENT if lo <= v < hi)
        if any(abs(v - b) / b < 0.15 for b in (1 / 256, 1 / 16, 2, 4, 64, 256)):
            continue
        mcq("3i.v.3", f"On the Wentworth scale, what is a sediment grain {v} mm across?", cls, [w[2] for w in WENT], tags=["grain size"], diff=2,
            explanation="Clay <1/256 mm; silt 1/256-1/16; sand 1/16-2; granule 2-4; pebble 4-64; cobble 64-256; boulder >256 mm.")
        mcq("3i.v.3", f"A clastic rock is made mostly of {v} mm grains. Which rock type is it?", ROCK_FOR[cls],
            sorted(set(ROCK_FOR.values())), tags=["grain size"], diff=2)
    add("order", "3i.v.3", "Order these grain sizes from smallest to largest: boulder, clay, cobble, pebble, sand, silt.",
        ["clay", "silt", "sand", "pebble", "cobble", "boulder"], tags=["grain size", "ranking"], diff=1)
    for size, energy in [("boulders and cobbles", "very high energy (fast floods, steep streams)"), ("pebbles and sand", "moderate to high energy (rivers, beaches)"),
                         ("silt and clay", "very low energy (lakes, deep ocean, floodplains)")]:
        mcq("3i.v.4", f"Deposits dominated by {size} indicate what kind of depositional energy?", energy,
            ["very high energy (fast floods, steep streams)", "moderate to high energy (rivers, beaches)", "very low energy (lakes, deep ocean, floodplains)"],
            n=2, tags=["energy", "grain size"], diff=1)
    hj = [("Which grain size is eroded at the LOWEST stream velocity on the Hjulström curve?", "fine to medium sand (about 0.1-0.5 mm)",
           ["clay", "pebbles", "boulders"]),
          ("Why does clay require a higher velocity to erode than sand on the Hjulström curve?", "clay particles are cohesive (stick together) and form a smooth bed",
           ["clay is denser than sand", "clay grains are larger", "clay is magnetic"]),
          ("As a river slows down, which sediment is deposited first?", "the largest, heaviest grains (gravel)",
           ["clay", "silt", "dissolved ions"]),
          ("Once eroded, why can clay stay in suspension even at very low velocities?", "its tiny grains settle extremely slowly",
           ["it is less dense than water", "it is cohesive", "it dissolves"]),
          ("What happens to the maximum grain size a stream can carry when its velocity increases?", "it increases",
           ["it decreases", "it stays the same", "only clay can be carried"])]
    for q, a, d in hj:
        mcq("3i.v.3", q, a, d, tags=["Hjulström", "stream velocity"], diff=2)
    for sorting, mean in [("well sorted", "long transport or constant energy (beach, dunes) separated grains by size"),
                          ("poorly sorted", "rapid deposition with little transport (glacial till, alluvial fan, debris flow)")]:
        mcq("3i.v.3", f"What does a {sorting} sediment indicate?", mean, ["long transport or constant energy (beach, dunes) separated grains by size",
            "rapid deposition with little transport (glacial till, alluvial fan, debris flow)", "chemical precipitation from seawater"],
            n=2, tags=["sorting"], diff=1)


# ---------------------------------------------------------------- naming igneous rocks from modes
MODES = {
    ("phaneritic", "granite"): {"quartz": (20, 40), "potassium feldspar": (30, 45), "sodium plagioclase": (15, 30), "biotite": (3, 10)},
    ("aphanitic", "rhyolite"): {"quartz": (20, 40), "potassium feldspar": (30, 45), "sodium plagioclase": (15, 30), "biotite": (3, 10)},
    ("phaneritic", "diorite"): {"intermediate plagioclase": (50, 65), "hornblende": (25, 40), "biotite": (2, 10), "quartz": (0, 4)},
    ("aphanitic", "andesite"): {"intermediate plagioclase": (50, 65), "hornblende": (25, 40), "biotite": (2, 10), "quartz": (0, 4)},
    ("phaneritic", "gabbro"): {"calcium plagioclase": (45, 60), "pyroxene": (30, 45), "olivine": (3, 15)},
    ("aphanitic", "basalt"): {"calcium plagioclase": (45, 60), "pyroxene": (30, 45), "olivine": (3, 15)},
    ("phaneritic", "peridotite"): {"olivine": (60, 90), "pyroxene": (10, 35)},
    ("phaneritic", "syenite"): {"potassium feldspar": (60, 80), "sodium plagioclase": (5, 15), "hornblende": (8, 20), "quartz": (0, 4)},
}


def modes():
    names = sorted({k[1] for k in MODES})
    for (tex, rock), comp in MODES.items():
        for _ in range(14):
            v = {m: RNG.randint(*r) for m, r in comp.items()}
            tot = sum(v.values())
            v = {m: round(100 * x / tot) for m, x in v.items()}
            v[max(v, key=v.get)] += 100 - sum(v.values())
            desc = ", ".join(f"{p}% {m}" for m, p in sorted(v.items(), key=lambda x: -x[1]) if p > 0)
            g = "coarse-grained (phaneritic)" if tex == "phaneritic" else "fine-grained (aphanitic); mineral proportions determined in thin section"
            mcq("3i.iv.2", f"An igneous rock is {g} and contains {desc}. Name the rock.", rock.capitalize(), [n.capitalize() for n in names],
                specimens=[rock], tags=["classification", "modes"], diff=3,
                explanation=f"{tex.capitalize()} + this mineralogy = {rock}.")


# ---------------------------------------------------------------- dating (geochronology use of minerals)
SYSTEMS = [("U-238 -> Pb-206", 4.47e9, "zircon"), ("U-235 -> Pb-207", 7.04e8, "zircon"), ("K-40 -> Ar-40", 1.25e9, "biotite or muscovite"),
           ("Rb-87 -> Sr-87", 4.9e10, "micas and K-feldspar"), ("C-14 -> N-14", 5730, "organic material (not minerals)")]


def dating():
    for sysn, hl, mineral in SYSTEMS:
        for n in (1, 2, 3, 4):
            frac = 0.5 ** n
            age = hl * n
            fmt = (f"{age/1e9:g} billion" if age >= 1e9 else f"{age/1e6:g} million" if age >= 1e6 else f"{age:,.0f}")
            add("numeric", "3h.xii.1", f"The half-life of {sysn} is {hl:,.0f} years. A sample retains {frac*100:g}% of its original parent isotope. "
                "How many half-lives have passed?", n, tolerance=0, tags=["radiometric dating", "calculation"], diff=2,
                explanation=f"{frac*100:g}% = (1/2)^{n}; age = {n} x {hl:,.0f} = {fmt} years.")
        for dp in (1, 3, 7, 15):
            n = math.log2(1 + dp)
            add("numeric", "3h.xii.1", f"A mineral has a daughter-to-parent ratio of {dp}:1 for {sysn} (half-life {hl:,.0f} years). "
                "Assuming no initial daughter, how many half-lives old is it?", round(n), tolerance=0, tags=["radiometric dating", "calculation"],
                diff=3, explanation=f"D/P = 2^n - 1 -> n = log2(1 + {dp}) = {n:g}.")
    tf("3h.xii.1", "Zircon is ideal for U-Pb dating because uranium substitutes for zirconium in its structure while lead is excluded when it forms.",
       True, specimens=["zircon"], tags=["radiometric dating"], diff=2)
    tf("3h.xii.1", "Carbon-14 is used to date billion-year-old igneous rocks.", False, tags=["radiometric dating"], diff=1,
       explanation="C-14's 5,730-year half-life limits it to organic material younger than ~50,000 years.")


def run():
    bowen(); metamorphism(); phase_diagrams(); compositions(); sediments(); modes(); dating()
