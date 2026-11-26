"""Concept fact tables (part 2): metamorphism, facies, rock cycle, weathering, thin sections, differentiation, mineral-forming processes."""
from tables import emit

META_TYPES = [
    dict(name="regional metamorphism", cause="high pressure and temperature during mountain building", scale="thousands of square kilometers",
         fabric="strongly foliated rocks", rocks="slate, phyllite, schist and gneiss", setting="convergent plate boundaries", sp=["mica-schist", "gneiss", "slate"]),
    dict(name="contact metamorphism", cause="heat from an adjacent magma body", scale="a zone meters to a few kilometers wide around the intrusion",
         fabric="non-foliated, fine-grained rocks", rocks="hornfels, marble and quartzite (and skarn)", setting="around plutons, dikes and sills",
         sp=["marble", "quartzite"]),
    dict(name="burial metamorphism", cause="the heat and pressure of deep burial under sediment", scale="the base of thick sedimentary basins",
         fabric="weak or no foliation", rocks="zeolite-facies rocks", setting="deep sedimentary basins"),
    dict(name="hydrothermal metamorphism", cause="hot, chemically active water circulating through rock", scale="along fractures and the seafloor",
         fabric="altered, often veined rock", rocks="greenstone, serpentinite and altered basalt", setting="mid-ocean ridges and geothermal areas",
         sp=["serpentinite", "epidote"]),
    dict(name="dynamic metamorphism", cause="intense shearing and grinding along faults", scale="narrow fault zones",
         fabric="crushed or finely sheared rock", rocks="mylonite and fault breccia", setting="fault and shear zones"),
    dict(name="impact metamorphism", cause="the shock wave of a meteorite impact", scale="around impact craters",
         fabric="shocked, shattered or melted rock", rocks="impact breccia with shocked quartz, coesite and tektites", setting="impact craters such as Vredefort and Meteor Crater"),
    dict(name="subduction-zone metamorphism", cause="high pressure at relatively low temperature as cold slabs sink", scale="long belts along trenches",
         fabric="foliated high-pressure rocks", rocks="blueschist and eclogite", setting="subduction zones"),
]

FACIES_T = [
    dict(name="zeolite facies", pt="lowest temperature and pressure (about 150-250 °C)", minerals="zeolites such as laumontite",
         setting="burial of volcanic sediments"),
    dict(name="prehnite-pumpellyite facies", pt="very low grade, slightly above zeolite facies", minerals="prehnite and pumpellyite",
         setting="burial and low-grade alteration of basalt", sp=["prehnite"]),
    dict(name="greenschist facies", pt="low temperature (about 300-500 °C) and low to moderate pressure",
         minerals="chlorite, epidote, actinolite and albite", setting="low-grade regional metamorphism and seafloor alteration", sp=["epidote", "actinolite"]),
    dict(name="amphibolite facies", pt="medium to high temperature (about 500-700 °C) and moderate pressure", minerals="hornblende and plagioclase (plus garnet)",
         setting="mid-crustal regional metamorphism", sp=["amphibolite", "hornblende"]),
    dict(name="granulite facies", pt="very high temperature (over about 700 °C) at moderate to high pressure",
         minerals="pyroxenes and garnet with no hydrous minerals", setting="the deep crust of collision zones"),
    dict(name="blueschist facies", pt="high pressure and low temperature", minerals="glaucophane (blue amphibole) and lawsonite",
         setting="subduction zones"),
    dict(name="eclogite facies", pt="very high pressure at medium to high temperature", minerals="garnet and omphacite (green pyroxene)",
         setting="deep subduction zones and the mantle", sp=["almandine"]),
    dict(name="hornfels facies", pt="high temperature at low pressure", minerals="andalusite, cordierite and pyroxene in fine-grained rock",
         setting="contact aureoles"),
]

PROCESSES = [
    dict(name="weathering", frm="any rock exposed at the surface", to="sediment and dissolved ions", energy="external (sun-driven water and atmosphere)"),
    dict(name="erosion and transport", frm="weathered sediment", to="sediment moved by water, wind, ice or gravity", energy="external (gravity, water and wind)"),
    dict(name="deposition", frm="transported sediment", to="layers of sediment in basins", energy="external (loss of transport energy)"),
    dict(name="burial, compaction and cementation", frm="loose sediment", to="sedimentary rock", energy="external and internal (weight of overburden, groundwater)"),
    dict(name="metamorphism", frm="igneous, sedimentary or metamorphic rock", to="metamorphic rock", energy="internal (Earth's heat and tectonic pressure)"),
    dict(name="melting", frm="any rock heated beyond its melting point", to="magma", energy="internal (Earth's heat, decompression or added water)"),
    dict(name="crystallization (solidification)", frm="magma or lava", to="igneous rock", energy="internal (cooling of melt)"),
    dict(name="uplift", frm="deeply buried rock", to="rock raised toward the surface", energy="internal (tectonic forces)"),
]

WEATHER = [
    dict(name="frost wedging", kind="mechanical", mech="water expands about 9% as it freezes in cracks, prying rock apart", climate="climates with frequent freeze-thaw cycles"),
    dict(name="exfoliation (unloading)", kind="mechanical", mech="rock expands and peels in sheets as overlying rock is eroded away", climate="any; common in granite domes",
         sp=["granite"]),
    dict(name="salt wedging", kind="mechanical", mech="growing salt crystals in pores force grains apart", climate="arid and coastal climates"),
    dict(name="biological (root) wedging", kind="mechanical", mech="plant roots grow into cracks and widen them", climate="vegetated regions"),
    dict(name="abrasion", kind="mechanical", mech="grinding by particles carried in water, wind or ice", climate="rivers, deserts and glaciers"),
    dict(name="thermal expansion", kind="mechanical", mech="repeated heating and cooling stresses the outer layers of rock", climate="hot deserts with large daily temperature swings"),
    dict(name="dissolution", kind="chemical", mech="minerals dissolve directly in water or weak acid", climate="humid climates, especially on limestone", sp=["halite", "calcite"]),
    dict(name="carbonation", kind="chemical", mech="carbonic acid (CO2 + water) reacts with minerals such as calcite", climate="humid climates", sp=["fossil-limestone"]),
    dict(name="hydrolysis", kind="chemical", mech="water reacts with silicates such as feldspar to form clay", climate="warm, humid climates", sp=["kaolinite"]),
    dict(name="oxidation", kind="chemical", mech="oxygen reacts with iron-bearing minerals to form iron oxides (rust)", climate="humid, oxygen-rich settings",
         sp=["goethite-limonite", "hematite"]),
    dict(name="hydration", kind="chemical", mech="water molecules are incorporated into a mineral's structure, as anhydrite becomes gypsum", climate="humid climates"),
]

OPTICS = [
    dict(name="microcline (thin section)", ppl="colorless, often cloudy from alteration", xpl="low first-order gray with cross-hatched 'tartan' twinning",
         relief="low", cleavage="two at about 90°", sp=["orthoclase-microcline"]),
    dict(name="plagioclase (thin section)", ppl="colorless", xpl="first-order gray-white with parallel polysynthetic (albite) twin stripes",
         relief="low", cleavage="two at about 90°", sp=["albite", "labradorite"]),
    dict(name="calcite (thin section)", ppl="colorless; relief changes ('twinkles') as the stage rotates", xpl="very high-order pastel creamy colors",
         relief="variable, low to high", cleavage="rhombohedral, two sets crossing at about 75°/105°", sp=["calcite"]),
    dict(name="augite (thin section)", ppl="pale green to brownish, weakly pleochroic", xpl="bright second-order colors with inclined extinction",
         relief="high", cleavage="two at about 87°/93°", sp=["augite"]),
    dict(name="garnet (thin section)", ppl="pale pink to colorless, often fractured", xpl="black at all rotations (isotropic)",
         relief="very high", cleavage="none", sp=["almandine"]),
    dict(name="quartz (thin section)", ppl="colorless and clear, no alteration", xpl="low first-order gray to white, often with wavy (undulose) extinction",
         relief="low", cleavage="none"),
]

TS_TEXTURES = [
    dict(name="basalt (thin section)", look="small interlocking plagioclase laths and pyroxene, sometimes olivine phenocrysts", group="igneous - holocrystalline, fine-grained",
         sp=["basalt"]),
    dict(name="pumice (thin section)", look="mostly glass full of stretched bubbles (vesicles) with few crystals", group="igneous - glassy and vesicular", sp=["pumice"]),
    dict(name="porphyritic andesite (thin section)", look="large zoned plagioclase phenocrysts in a fine groundmass", group="igneous - porphyritic", sp=["andesite"]),
    dict(name="obsidian (thin section)", look="clear glass that is isotropic in cross-polarized light, perhaps with tiny crystallites", group="igneous - glassy",
         sp=["obsidian"]),
    dict(name="granite (thin section)", look="large interlocking quartz, microcline and plagioclase with biotite", group="igneous - phaneritic, holocrystalline",
         sp=["granite"]),
    dict(name="quartz sandstone (thin section)", look="well-rounded, well-sorted quartz grains with cement between them", group="sedimentary - mature clastic",
         sp=["quartz-sandstone"]),
    dict(name="arkose (thin section)", look="angular quartz and abundant twinned or cloudy feldspar grains", group="sedimentary - immature clastic", sp=["arkose"]),
    dict(name="oolitic limestone (thin section)", look="round grains with concentric layers around a nucleus in calcite cement", group="sedimentary - chemical carbonate",
         sp=["oolitic-limestone"]),
    dict(name="fossiliferous limestone (thin section)", look="shell and skeletal fragments in fine calcite (micrite) or sparry cement", group="sedimentary - bioclastic",
         sp=["fossil-limestone"]),
    dict(name="greywacke (thin section)", look="angular grains of quartz, feldspar and rock fragments floating in muddy matrix", group="sedimentary - poorly sorted clastic",
         sp=["greywacke"]),
]

DIFF_EVID = [
    dict(name="fractional crystallization", evidence="cumulate layers of olivine, pyroxene or chromite at the base of an intrusion",
         effect="drives the remaining melt toward higher silica and incompatible elements", example="the Skaergaard and Stillwater intrusions"),
    dict(name="assimilation", evidence="partly melted xenoliths of country rock and crust-like isotope ratios",
         effect="adds silica and crustal elements, making the magma more felsic", example="continental-arc magmas of the Andes"),
    dict(name="magma mixing", evidence="mafic enclaves in a felsic host, reverse-zoned or resorbed phenocrysts and banded lava",
         effect="produces intermediate compositions and can trigger eruptions", example="the 1991 Pinatubo eruption"),
    dict(name="partial melting", evidence="melt richer in silica than its source, leaving a refractory residue",
         effect="creates basalt from peridotite or granite from crust", example="basalt formed at mid-ocean ridges"),
    dict(name="crystal settling", evidence="dense early crystals concentrated at the floor of a sill or chamber",
         effect="physically separates crystals from the melt", example="the olivine-rich base of the Palisades Sill"),
]

INCOMP = [
    dict(name="lithium", reason="small Li+ ion with a low charge is a poor fit in common silicate sites", host="spodumene and lepidolite", use="batteries",
         sp=["spodumene", "lepidolite"]),
    dict(name="beryllium", reason="tiny Be2+ ion fits few common minerals", host="beryl", use="lightweight aerospace alloys and X-ray windows", sp=["beryl"]),
    dict(name="boron", reason="forms small BO3 groups that rarely enter rock-forming minerals", host="tourmaline", use="borosilicate glass and fiberglass",
         sp=["tourmaline"]),
    dict(name="cesium", reason="very large Cs+ ion is too big for most sites", host="pollucite (and lepidolite)", use="atomic clocks"),
    dict(name="rubidium", reason="large Rb+ ion only partly substitutes for K+", host="lepidolite and K-feldspar", use="Rb-Sr dating and research", sp=["lepidolite"]),
    dict(name="tantalum", reason="high charge (Ta5+) does not fit common mineral sites", host="columbite-tantalite", use="capacitors in electronics"),
    dict(name="uranium", reason="large, highly charged U4+ ion stays in the melt", host="zircon and uraninite", use="nuclear fuel and dating", sp=["zircon"]),
    dict(name="fluorine", reason="volatile and concentrated in late fluids", host="topaz, fluorite and lepidolite", use="fluorine chemicals", sp=["topaz", "fluorite"]),
]

FORMATION = [
    dict(name="crystallization from magma", desc="minerals growing as molten rock cools", examples="olivine, augite, plagioclase and quartz in igneous rocks",
         sp=["olivine", "augite"]),
    dict(name="hydrothermal deposition", desc="minerals precipitating from hot water moving through fractures", examples="galena, sphalerite, chalcopyrite and gold in quartz veins",
         sp=["galena", "chalcopyrite"]),
    dict(name="evaporation", desc="minerals precipitating as salty water evaporates", examples="halite, gypsum and ulexite", sp=["halite", "selenite", "ulexite"]),
    dict(name="chemical precipitation", desc="minerals crystallizing directly from supersaturated water", examples="calcite in caves and hot springs", sp=["calcite", "travertine"]),
    dict(name="chemical weathering", desc="new minerals forming as older minerals break down at the surface", examples="kaolinite from feldspar and goethite from iron minerals",
         sp=["kaolinite", "goethite-limonite"]),
    dict(name="metamorphism (heat and pressure)", desc="minerals recrystallizing in the solid state under heat and pressure", examples="garnet, kyanite and staurolite in schist",
         sp=["almandine", "kyanite", "staurolite"]),
    dict(name="biological activity", desc="organisms building mineral skeletons or shells", examples="aragonite in mollusk shells and calcite in coccoliths", sp=["aragonite"]),
    dict(name="supergene oxidation", desc="near-surface groundwater altering primary ore minerals", examples="malachite, azurite and chrysocolla above copper deposits",
         sp=["malachite", "azurite", "chrysocolla"]),
]

IGN_TEX_ENV = [
    dict(name="glassy texture", cooling="extremely rapid quenching", where="the surface of lava flows and explosive ejecta", example="obsidian", sp=["obsidian"]),
    dict(name="vesicular texture", cooling="rapid cooling while gases escape", where="the tops of lava flows and frothy ejecta", example="pumice and scoria",
         sp=["pumice", "scoria"]),
    dict(name="aphanitic texture", cooling="rapid cooling", where="lava flows and thin dikes", example="basalt and rhyolite", sp=["basalt", "rhyolite"]),
    dict(name="phaneritic texture", cooling="slow cooling", where="deep plutons and batholiths", example="granite and gabbro", sp=["granite", "gabbro"]),
    dict(name="porphyritic texture", cooling="slow cooling followed by faster cooling", where="magma that began crystallizing at depth then rose or erupted",
         example="porphyritic andesite", sp=["andesite"]),
    dict(name="pegmatitic texture", cooling="crystallization from a water-rich residual melt", where="dikes and pods at the margins of granite plutons",
         example="pegmatite", sp=["pegmatite"]),
    dict(name="pyroclastic texture", cooling="explosive fragmentation, then deposition", where="ash falls and pyroclastic flows", example="tuff and tuff breccia",
         sp=["tuff", "tuff-breccia"]),
]


def run():
    emit(META_TYPES, [("cause", "3i.vi.5", "What causes {name}?", "Which type of metamorphism is caused by {value}?", True, "{name} is caused by {value}."),
                      ("fabric", "3i.vi.1", "What rock fabric does {name} typically produce?", None, False, "{name} typically produces {value}."),
                      ("rocks", "3i.vi.5", "Which rocks are typical products of {name}?", "Which type of metamorphism typically produces {value}?", True,
                       "{name} typically produces {value}."),
                      ("setting", "3i.vi.8", "Where does {name} typically occur?", "Which type of metamorphism occurs at {value}?", True, "{name} typically occurs at {value}."),
                      ("scale", "3i.vi.5", "Over what area does {name} act?", None, False, None)],
         "metamorphism type")
    emit(FACIES_T, [("pt", "3i.vi.7", "What pressure-temperature conditions define the {name}?", "Which facies represents {value}?", True,
                     "The {name} represents {value}."),
                    ("minerals", "3i.vi.7", "Which minerals are diagnostic of the {name}?", "Which facies is identified by {value}?", True,
                     "Diagnostic minerals of the {name} include {value}."),
                    ("setting", "3i.vi.8", "In what setting does the {name} typically develop?", "Which facies typically develops in {value}?", True,
                     "The {name} typically develops in {value}.")],
         "facies")
    emit(PROCESSES, [("to", "3i.vii", "In the rock cycle, what does {name} produce?", "Which rock-cycle process produces {value}?", True,
                      "In the rock cycle, {name} produces {value}."),
                     ("frm", "3i.vii", "In the rock cycle, what material does {name} act on?", None, False, None),
                     ("energy", "3i.vii", "What energy source drives {name}?", None, False, "{name} is driven by {value}.")],
         "rock cycle")
    emit(WEATHER, [("kind", "3i.vii", "Is {name} mechanical or chemical weathering?", None, False, "{name} is a form of {value} weathering."),
                   ("mech", "3i.vii", "How does {name} break down rock?", "Which weathering process works by: {value}?", True, "In {name}, {value}."),
                   ("climate", "3i.vii", "Where is {name} most effective?", None, False, None)],
         "weathering")
    emit(OPTICS, [("ppl", "3i.ix", "What does {name} look like in plane-polarized light?", "Which mineral in thin section is {value} in PPL?", True, None),
                  ("xpl", "3i.ix", "What does {name} look like in cross-polarized light?", "Which mineral in thin section shows {value} in XPL?", True,
                   "In cross-polarized light, {name} shows {value}."),
                  ("relief", "3i.ix", "What relief does {name} show?", None, False, None),
                  ("cleavage", "3i.ix", "What cleavage is visible in {name}?", "Which thin-section mineral shows cleavage: {value}?", True, None)],
         "optical mineralogy")
    emit(TS_TEXTURES, [("look", "3i.ix", "What would you expect to see in {name}?", "A photomicrograph shows {value}. Which rock is it?", True,
                        "{name} shows {value}."),
                       ("group", "3i.ix", "How would you classify the texture of {name}?", None, False, None)],
         "thin section texture")
    emit(DIFF_EVID, [("evidence", "3i.iv.6", "What evidence in rocks points to {name}?", "Which process is indicated by {value}?", True,
                      "Evidence for {name} includes {value}."),
                     ("effect", "3i.iv.6", "How does {name} change a magma or produce magma?", "Which process {value}?", True, None),
                     ("example", "3i.iv.6", "Which is a classic example of {name}?", "{value} is a classic example of which process?", True, None)],
         "magma evolution")
    emit(INCOMP, [("reason", "3i.iv.6b", "Why is {name} an incompatible element?", None, False, None),
                  ("host", "3i.iv.6b", "In which pegmatite mineral is {name} concentrated?", "Which incompatible element is hosted by {value}?", True,
                   "{name} is concentrated in {value}."),
                  ("use", "3i.iv.6b", "What is a major use of {name} mined from pegmatites?", "Which pegmatite element is used for {value}?", True, None)],
         "incompatible element", diff=3)
    emit(FORMATION, [("desc", "3h.ix", "What does mineral formation by {name} involve?", "Which mineral-forming process involves {value}?", True, None),
                     ("examples", "3h.ix", "Which minerals form by {name}?", "Which process forms {value}?", True, "{value} form by {name}.")],
         "mineral formation")
    emit(IGN_TEX_ENV, [("cooling", "3i.iv.4", "What cooling history produces a {name}?", "Which texture results from {value}?", True,
                        "A {name} results from {value}."),
                       ("where", "3i.iv.4", "Where does a {name} typically form?", "Which texture typically forms in {value}?", True,
                        "A {name} typically forms in {value}."),
                       ("example", "3i.iv.1", "Which rock shows a {name}?", "Which texture do {value} show?", True, None)],
         "igneous texture")


META_MIN = [
    dict(name="garnet", forms="medium- to high-grade metamorphism of shale (almandine) or contact metamorphism of limestone (grossular)",
         rock="garnet schist, gneiss and skarn", grade="medium to high", sp=["almandine", "grossular", "garnet-schist"]),
    dict(name="corundum", forms="metamorphism of aluminum-rich, silica-poor rocks", rock="marble (rubies) and emery", grade="medium to high", sp=["corundum", "marble"]),
    dict(name="kyanite", forms="medium- to high-pressure metamorphism of aluminum-rich shale", rock="kyanite schist and gneiss", grade="medium to high (high pressure)",
         sp=["kyanite"]),
    dict(name="staurolite", forms="medium-grade metamorphism of iron- and aluminum-rich shale", rock="staurolite-mica schist", grade="medium", sp=["staurolite"]),
    dict(name="epidote", forms="low-grade metamorphism and hydrothermal alteration of basalt", rock="greenschist and greenstone", grade="low", sp=["epidote"]),
    dict(name="andalusite", forms="low-pressure, moderate-temperature (contact) metamorphism of shale", rock="hornfels and spotted slate", grade="low to medium (low pressure)"),
    dict(name="sillimanite", forms="high-temperature metamorphism of aluminum-rich shale", rock="high-grade gneiss and schist", grade="high (high temperature)"),
    dict(name="chlorite", forms="low-grade metamorphism of shale or basalt", rock="slate, phyllite and greenschist", grade="low"),
    dict(name="muscovite", forms="low- to medium-grade metamorphism of shale", rock="phyllite and mica schist", grade="low to medium", sp=["muscovite", "mica-schist"]),
    dict(name="biotite", forms="low- to medium-grade metamorphism of shale, after chlorite", rock="biotite schist", grade="low to medium", sp=["biotite"]),
    dict(name="talc", forms="metamorphism of ultramafic rock or siliceous dolomite", rock="talc schist (soapstone)", grade="low to medium", sp=["talc", "talc-schist"]),
    dict(name="serpentine", forms="hydration of olivine and pyroxene in peridotite", rock="serpentinite", grade="low", sp=["serpentinite"]),
    dict(name="wollastonite", forms="contact metamorphism of siliceous limestone (calcite + quartz)", rock="skarn and marble", grade="medium to high (contact)",
         sp=["wollastonite"]),
    dict(name="tremolite", forms="metamorphism of siliceous dolomite (dolomite + quartz + water)", rock="tremolite marble", grade="low to medium", sp=["tremolite"]),
    dict(name="graphite", forms="metamorphism of organic matter in sediments", rock="graphitic schist and marble", grade="medium to high", sp=["graphite"]),
]

POLY = [
    dict(name="calcite", formula="CaCO3", partner="aragonite", control="calcite is stable at surface conditions; aragonite is the high-pressure form",
         sp=["calcite", "aragonite"]),
    dict(name="diamond", formula="C", partner="graphite", control="diamond needs mantle pressures; graphite is stable near the surface", sp=["diamond", "graphite"]),
    dict(name="kyanite", formula="Al2SiO5", partner="andalusite and sillimanite", control="kyanite = high pressure, andalusite = low pressure, sillimanite = high temperature",
         sp=["kyanite"]),
    dict(name="orthoclase", formula="KAlSi3O8", partner="microcline and sanidine", control="sanidine forms at high temperature, orthoclase at intermediate, microcline at low",
         sp=["orthoclase-microcline", "amazonite"]),
    dict(name="rutile", formula="TiO2", partner="anatase and brookite", control="rutile is the stable high-temperature TiO2 polymorph", sp=["rutile"]),
    dict(name="alpha (low) quartz", formula="SiO2", partner="beta quartz, tridymite, cristobalite, coesite and stishovite",
         control="coesite and stishovite form at very high (impact) pressures; tridymite and cristobalite at high temperature", sp=["rock-crystal"]),
    dict(name="pyrite", formula="FeS2", partner="marcasite", control="marcasite forms at low temperature in acidic conditions", sp=["pyrite"]),
    dict(name="sphalerite", formula="ZnS", partner="wurtzite", control="wurtzite is the higher-temperature hexagonal form", sp=["sphalerite"]),
]


def run_extra():
    emit(META_MIN, [("forms", "3i.vi.3", "How does {name} form in metamorphic rocks?", "Which metamorphic mineral forms by {value}?", True,
                     "In metamorphic rocks, {name} forms by {value}."),
                    ("rock", "3i.vi.2", "In which metamorphic rocks is {name} characteristic?", "Which mineral is characteristic of {value}?", True,
                     "{name} is characteristic of {value}."),
                    ("grade", "3i.vi.6", "What metamorphic grade does {name} usually indicate?", None, False, None)],
         "metamorphic mineral")
    emit(POLY, [("formula", "3h.vii", "What composition do {name} and its polymorphs share?", None, False, "{name} and its polymorphs share the composition {value}."),
                ("partner", "3h.vii", "Name the polymorph(s) of {name}.", "Which mineral is a polymorph of {value}?", True, "{name} is polymorphous with {value}."),
                ("control", "3h.vii", "What controls which polymorph forms for {name}?", None, False, None)],
         "polymorph")


_run = run


def run():  # noqa: F811
    _run()
    run_extra()
