"""Second authored set: fills thin rulebook areas and in-scope terms found in archive tests but missing from the bank."""
from common import add
from authored import M, T, S, F, ITEMS
import authored

START = len(ITEMS)

# --- rock definition (3i.i)
M("3i.i", 1, "Which is a rock rather than a mineral?", "basalt", ["olivine", "quartz", "calcite"], sp=["basalt"])
M("3i.i", 1, "Which is a mineral rather than a rock?", "halite", ["rock salt", "granite", "slate"], sp=["halite"])
T("3i.i", 2, "Rock salt (the rock) and halite (the mineral) can describe the same material at different scales.", True, sp=["rock-salt", "halite"])
M("3i.i", 2, "Coal is classified as a rock rather than a mineral because:", "it is made of organic matter of variable composition",
  ["it is too soft", "it burns", "it is black"], sp=["bituminous"])
M("3i.i", 2, "Obsidian is a rock even though it contains no minerals because:", "rocks can be made of mineraloids such as volcanic glass",
  ["obsidian is crystalline", "it is a mineral", "it is organic"], sp=["obsidian"])
M("3i.i", 2, "Which rock on the list is made mostly of a mineraloid?", "obsidian", ["granite", "marble", "quartzite"], sp=["obsidian"])
M("3i.i", 2, "Which rock on the list is made mostly of organic matter?", "lignite", ["chalk", "shale", "chert"], sp=["lignite"])

# --- evolution of melts (3i.iv.6)
M("3i.iv.6", 2, "Concentric compositional zoning in a plagioclase crystal (Ca-rich core, Na-rich rim) records:", "changing melt composition as the crystal grew",
  ["metamorphism", "weathering", "twinning"], sp=["labradorite"])
M("3i.iv.6", 3, "Reverse zoning in plagioclase (a more Ca-rich rim) can indicate:", "injection of hotter, more mafic magma (magma mixing)",
  ["slow cooling only", "weathering", "metamorphism"])
M("3i.iv.6", 2, "A reaction rim of pyroxene around an olivine crystal shows:", "olivine reacting with the melt as it cooled (Bowen's discontinuous series)",
  ["weathering", "sedimentary cement", "radiation damage"], sp=["olivine", "augite"])
M("3i.iv.6", 2, "Melting a mantle peridotite partially produces a melt of what composition?", "basaltic (mafic)", ["granitic", "ultramafic", "carbonate"],
  sp=["peridotite", "basalt"])
M("3i.iv.6", 2, "Partial melting of continental crust tends to produce magma of what composition?", "felsic (granitic)", ["ultramafic", "mafic", "carbonatite"],
  sp=["granite"])
M("3i.iv.6", 2, "Calc-alkaline magmas such as andesite are characteristic of:", "subduction zones", ["mid-ocean ridges", "transform faults", "abyssal plains"],
  sp=["andesite"])
M("3i.iv.6", 2, "Why are andesites so common at subduction zones?", "basalt from the mantle wedge evolves by fractional crystallization and crustal assimilation",
  ["andesite melts directly from peridotite only", "sea water turns basalt into andesite", "they are metamorphic"], sp=["andesite"])
M("3i.iv.6", 2, "Blocks of country rock that sink into a magma chamber, a process that helps magma rise, is called:", "stoping", ["assimilation", "zoning", "exsolution"])
F("3i.iv.6", 3, "Give two pieces of evidence that a volcanic rock formed by magma mixing.",
  "Possible evidence: disequilibrium phenocrysts (e.g., quartz with olivine), resorbed or reverse-zoned crystals, mafic enclaves (blobs) in a felsic host, banded or streaked mixed lava.",
  ["disequilibrium crystals", "reverse zoning/resorption", "mafic enclaves or banding"])

# --- incompatible elements (3i.iv.6b)
M("3i.iv.6b", 2, "As a magma crystallizes, the concentration of incompatible elements in the remaining melt:", "increases", ["decreases", "stays the same", "drops to zero"],
  sp=["pegmatite"])
M("3i.iv.6b", 2, "Which list mineral from pegmatites is a major source of the incompatible element cesium and rubidium?", "lepidolite", ["olivine", "augite", "magnetite"],
  sp=["lepidolite"])
M("3i.iv.6b", 2, "Tantalum and niobium, used in electronics, are mined largely from:", "pegmatites", ["basalts", "evaporites", "coal seams"], sp=["pegmatite"])
M("3i.iv.6b", 2, "Rare-earth elements are generally:", "incompatible, concentrating in late melts and certain accessory minerals", ["compatible in olivine",
  "concentrated in the core", "only found in meteorites"])
M("3i.iv.6b", 3, "Why is zircon able to host uranium even though uranium is an incompatible element?", "U4+ is similar in size and charge to Zr4+, so it substitutes in zircon",
  ["zircon is radioactive by itself", "uranium fits in any mineral", "uranium bonds to silicon"], sp=["zircon"])
T("3i.iv.6b", 2, "Compatible elements such as Ni and Cr are enriched in pegmatites.", False,
  "They enter early mafic minerals; pegmatites are enriched in incompatible elements.", sp=["pegmatite"])
T("3i.iv.6b", 2, "Large-ion lithophile elements (such as K, Rb, Cs, Ba) are incompatible because their ions are too large for most mineral sites.", True)

# --- sedimentary texture vs environment (3i.v.4)
M("3i.v.4", 2, "A sandstone with frosted, well-rounded, well-sorted grains and large cross-beds most likely formed in a:", "desert dune field",
  ["deep-sea fan", "glacial moraine", "swamp"], sp=["quartz-sandstone"])
M("3i.v.4", 2, "Conglomerate with imbricated (shingled) pebbles indicates:", "deposition by a strong one-directional current such as a river",
  ["deep calm water", "wind", "evaporation"], sp=["conglomerate"])
M("3i.v.4", 2, "An arkose with angular feldspar grains indicates:", "rapid erosion and short transport from a granitic source", ["long transport",
  "deep marine settling", "intense chemical weathering"], sp=["arkose"])
M("3i.v.4", 2, "Thinly laminated black shale with no burrows suggests:", "quiet, oxygen-poor water", ["a high-energy beach", "a desert", "a glacier"], sp=["shale"])
M("3i.v.4", 2, "Coquina made of broken, abraded shells indicates:", "a high-energy surf zone", ["a deep calm basin", "a lake", "a glacier"], sp=["coquina"])
M("3i.v.4", 2, "Chalk made of microscopic coccoliths indicates deposition in:", "calm, open marine water above the CCD", ["a river channel", "a beach", "a desert"],
  sp=["chalk"])
M("3i.v.4", 2, "Breccia at the base of a cliff most likely formed from:", "rockfall (talus) with little transport", ["river transport", "wind", "turbidity currents"],
  sp=["breccia"])
M("3i.v.4", 2, "Greywacke's poor sorting and muddy matrix indicate:", "rapid deposition from dense turbidity currents", ["slow settling in a lake",
  "wind transport", "evaporation"], sp=["greywacke"])
M("3i.v.4", 2, "Thick rock salt deposits indicate:", "a restricted basin where evaporation exceeded inflow", ["a deep open ocean", "a glacier", "a fast river"],
  sp=["rock-salt"])
M("3i.v.4", 2, "Oolitic limestone indicates:", "warm, shallow, agitated water saturated in calcium carbonate", ["cold deep water", "a desert dune", "a swamp"],
  sp=["oolitic-limestone"])
M("3i.v.3", 2, "Large grains rolling and sliding along a stream bed move by:", "traction", ["suspension", "solution", "saltation"])
M("3i.v.3", 2, "Sand grains bouncing along a stream bed or desert floor move by:", "saltation", ["traction", "suspension", "solution"])
M("3i.v.3", 2, "Clay and silt carried within the water column move by:", "suspension", ["traction", "saltation", "solution"])
M("3i.v.3", 2, "The largest grain size a stream can carry is its:", "competence", ["capacity", "discharge", "gradient"])
M("3i.v.3", 2, "The total amount of sediment a stream can carry is its:", "capacity", ["competence", "velocity", "sorting"])
M("3i.v.3", 3, "Stokes' law states that the settling velocity of a small grain in still water increases with:", "the square of the grain diameter",
  ["the cube of grain diameter", "water depth", "grain angularity only"])
M("3i.v.5", 2, "A river with many interwoven channels separated by gravel bars, common near glaciers, is:", "braided", ["meandering", "straight", "deltaic"])
M("3i.v.5", 2, "Point bars of sand form on the:", "inside bend of a meandering river", ["outside bend", "delta front", "abyssal plain"])
M("3i.v.5", 2, "An abandoned meander cut off from a river forms an:", "oxbow lake", ["alluvial fan", "esker", "tombolo"])
M("3i.v.5", 2, "Natural levees form when floods deposit:", "coarser sediment right beside the channel", ["clay far from the channel", "evaporites", "coal"])
M("3i.v.5", 2, "A shallow marine shelf typically accumulates:", "sand near shore grading to mud and carbonate offshore", ["only gravel", "only evaporites", "only volcanic ash"])
M("3i.v.5", 2, "Varves (paired light/dark annual layers) form in:", "glacial lakes", ["deserts", "coral reefs", "deep-sea trenches"])

# --- sedimentary structures (3i.v.6)
M("3i.v.6", 2, "Herringbone cross-bedding (cross-beds dipping in opposite directions) indicates:", "tidal currents that reverse direction",
  ["wind only", "deep calm water", "glaciers"])
M("3i.v.6", 2, "Which structure would you expect in desert dune sandstones?", "large-scale cross-bedding", ["graded bedding", "pillow structures", "varves"],
  sp=["quartz-sandstone"])
M("3i.v.6", 2, "Which structure is most diagnostic of turbidites?", "graded bedding", ["mud cracks", "large dune cross-beds", "salt casts"], sp=["greywacke"])
M("3i.v.6", 2, "Salt crystal casts (hopper-shaped impressions) in mudstone indicate:", "evaporation in a shallow, drying basin", ["deep marine water", "glaciation",
  "lava flows"], sp=["halite"])
M("3i.v.6", 2, "Stromatolites are layered structures built by:", "mats of cyanobacteria trapping sediment", ["corals", "worm burrows", "wind ripples"])
M("3i.v.6", 2, "Which sedimentary structure forms only on bedding surfaces exposed to air?", "mud cracks", ["graded bedding", "cross-bedding", "flute casts"])
M("3i.v.6", 2, "Flute casts on the bottom of a sandstone bed indicate:", "scouring by a current, showing flow direction", ["drying", "evaporation", "volcanic ash"])
S("3i.v.6", 2, "Name the sedimentary structure made of inclined layers within a horizontal bed.", "cross-bedding", ["cross-bedding", "cross bedding", "crossbedding", "cross-beds"])
S("3i.v.6", 2, "Name the sedimentary structure in which grain size decreases upward through a single bed.", "graded bedding", ["graded bedding", "graded bed", "normal grading"])

# --- metamorphic composition & minerals (3i.vi.2, 3i.vi.3)
M("3i.vi.2", 2, "Which elements are typically lost from rocks during prograde metamorphism?", "water and carbon dioxide", ["silicon and oxygen", "iron and magnesium",
  "aluminum and potassium"])
M("3i.vi.2", 2, "Pelitic rocks (metamorphosed shales) are rich in:", "aluminum, producing micas, garnet, staurolite and Al2SiO5 minerals", ["calcium carbonate",
  "magnesium and iron only", "silica only"], sp=["mica-schist", "garnet-schist"])
M("3i.vi.2", 2, "Metamorphosed mafic rocks (metabasites) contain mainly:", "chlorite, epidote, actinolite, hornblende and plagioclase", ["calcite and dolomite",
  "quartz only", "micas and kyanite"], sp=["amphibolite"])
M("3i.vi.2", 2, "Which minerals would you expect in a marble formed from an impure (siliceous) dolomite?", "tremolite, diopside or wollastonite with calcite",
  ["kyanite and staurolite", "olivine only", "halite and gypsum"], sp=["marble", "tremolite", "wollastonite"])
M("3i.vi.2", 2, "Quartzite is almost pure quartz because its protolith was:", "a mature quartz sandstone", ["shale", "basalt", "limestone"], sp=["quartzite"])
M("3i.vi.2", 2, "Gneiss formed from granite (orthogneiss) contains:", "quartz, feldspar and biotite or hornblende", ["calcite and dolomite", "talc and serpentine",
  "halite and gypsum"], sp=["gneiss"])
M("3i.vi.2", 2, "Serpentinite is dominated by serpentine minerals with which common accessory oxide?", "magnetite", ["hematite", "corundum", "rutile"], sp=["serpentinite"])
M("3i.vi.3", 2, "Which metamorphic mineral is the key indicator of high-pressure regional metamorphism among the Al2SiO5 polymorphs?", "kyanite",
  ["andalusite", "sillimanite", "staurolite"], sp=["kyanite"])
M("3i.vi.3", 2, "Which list mineral forms during greenschist-facies metamorphism of basalt?", "epidote", ["sillimanite", "olivine", "sanidine"], sp=["epidote"])
M("3i.vi.3", 2, "Many gem rubies (such as those from Myanmar) formed by metamorphism within which rock?", "marble",
  ["quartzite", "sandstone", "coal"], sp=["corundum", "marble"])
M("3i.vi.3", 2, "Graphite in marble or schist forms from:", "metamorphosed organic matter", ["volcanic gas", "evaporation", "weathering of feldspar"], sp=["graphite"])
M("3i.vi.3", 2, "Staurolite forms in which metamorphic rock type?", "medium-grade pelitic schist", ["marble", "quartzite", "serpentinite"], sp=["staurolite"])
M("3i.vi.3", 2, "Which mineral forms when dolomite and quartz react during metamorphism?", "tremolite", ["kyanite", "garnet", "biotite"], sp=["tremolite"])

# --- metamorphism and plate tectonics (3i.vi.8)
M("3i.vi.8", 2, "Blueschist-facies rocks are found in the accretionary wedge because:", "scraped-off sediment and crust are carried quickly to high pressure while staying cold",
  ["magma heats them", "they formed at ridges", "they were never buried"])
M("3i.vi.8", 2, "An accretionary wedge (prism) forms at:", "subduction-zone trenches, from material scraped off the downgoing plate", ["mid-ocean ridges",
  "continental rifts", "hotspots"])
M("3i.vi.8", 2, "Eclogite exposed at the surface tells geologists that:", "rocks were subducted to great depth and then exhumed", ["the rock was a lava flow",
  "it formed in a lake", "it formed in a contact aureole"])
M("3i.vi.8", 2, "Regional metamorphism in the Appalachians occurred mainly during:", "continental collisions that built the mountains", ["sea-floor spreading",
  "glaciation", "meteorite impacts"])
M("3i.vi.8", 2, "Rocks along transform faults such as the San Andreas commonly undergo:", "dynamic (cataclastic) metamorphism, forming mylonite or fault breccia",
  ["eclogite-facies metamorphism", "contact metamorphism only", "no change"])
M("3i.vi.8", 2, "Greenstone belts in Archean cratons are interpreted as:", "metamorphosed ancient oceanic crust and volcanic arcs", ["metamorphosed limestone",
  "glacial deposits", "impact craters"])
M("3i.vi.8", 2, "Why do hornfels form around plutons at volcanic arcs?", "rising magma bakes the surrounding rock at shallow depth (contact metamorphism)",
  ["subduction carries them deep", "they are weathered", "they are evaporites"])
M("3i.vi.5", 2, "Metamorphism caused by mechanical deformation along fault zones is called:", "dynamic (cataclastic) metamorphism", ["contact metamorphism",
  "burial metamorphism", "hydrothermal metamorphism"])
M("3i.vi.5", 2, "Metamorphism caused only by deep burial in a sedimentary basin is called:", "burial metamorphism", ["contact metamorphism", "impact metamorphism",
  "dynamic metamorphism"])
M("3i.vi.7", 2, "Prograde metamorphism refers to changes that occur as:", "temperature and pressure increase", ["a rock cools and decompresses", "a rock weathers",
  "a rock melts entirely"])
M("3i.vi.7", 2, "Retrograde metamorphism refers to changes as:", "a rock cools and decompresses, often adding water", ["temperature rises", "a rock melts", "sediment is buried"])
T("3i.vi.7", 3, "High-grade metamorphic rocks often preserve their peak mineral assemblage because retrograde reactions are slowed by a lack of water.", True)

# --- porosity, permeability, karst, uses (3i.viii / 3i.vii)
M("3i.viii", 2, "Porosity is:", "the percentage of a rock's volume that is open space", ["the ability of fluid to flow through a rock", "the rock's density",
  "the size of its grains"])
M("3i.viii", 2, "Permeability is:", "how easily fluids flow through connected pores", ["the percentage of open space", "how hard the rock is", "its grain size"])
M("3i.viii", 2, "Which rock makes the best aquifer or oil reservoir?", "well-sorted sandstone", ["shale", "granite", "slate"], sp=["quartz-sandstone"])
M("3i.viii", 2, "Shale has high porosity but very low permeability because:", "its pores are tiny and poorly connected", ["it has no pores", "it is crystalline",
  "it dissolves"], sp=["shale"])
M("3i.viii", 2, "In a petroleum system, what is the role of a cap rock such as shale or rock salt?", "it seals the reservoir and traps oil and gas", ["it generates the oil",
  "it is the reservoir", "it heats the oil"], sp=["shale", "rock-salt"])
M("3i.viii", 2, "Why does poor sorting lower a sandstone's porosity?", "small grains fill the spaces between large grains", ["large grains dissolve",
  "poorly sorted rocks are always cemented", "sorting has no effect"])
M("3i.vii", 2, "Karst landscapes with sinkholes and caves develop on:", "limestone and other soluble rocks", ["granite", "basalt", "quartzite"], sp=["fossil-limestone"])
M("3i.vii", 2, "A sinkhole forms when:", "the roof of an underground cavity dissolved in limestone collapses", ["a volcano erupts", "a glacier melts", "a fault moves"])
M("3i.vii", 2, "Spheroidal weathering rounds the corners of jointed granite blocks because:", "corners are attacked from more sides than flat faces",
  ["granite is soft", "wind abrades it", "it melts"], sp=["granite"])
M("3i.vii", 2, "Chemical weathering by CO2 dissolved in water reacting with minerals is called:", "carbonation", ["hydration", "oxidation", "abrasion"])
M("3i.vii", 2, "Which mineral weathers fastest in a warm, humid climate?", "olivine", ["quartz", "muscovite", "zircon"], sp=["olivine"])
M("3i.vii", 2, "An erosional surface representing missing time in the rock record is an:", "unconformity", ["isograd", "facies", "aureole"])
M("3i.vii", 2, "Sedimentary rock deposited directly on eroded igneous or metamorphic rock forms a:", "nonconformity", ["disconformity", "angular unconformity", "fault"])
M("3i.vii", 2, "Tilted layers truncated by erosion and overlain by flat layers form an:", "angular unconformity", ["disconformity", "nonconformity", "sill"])
M("3i.vii", 2, "A dike that cuts through sedimentary layers must be younger than those layers. This is the principle of:", "cross-cutting relationships",
  ["superposition", "original horizontality", "faunal succession"])
M("3i.vii", 2, "In undisturbed layers, the oldest rocks are at the bottom. This is the principle of:", "superposition", ["cross-cutting relationships",
  "inclusions", "uniformitarianism"])
M("3i.vii", 2, "Pebbles of granite inside a conglomerate mean the granite is:", "older than the conglomerate (principle of inclusions)", ["younger than the conglomerate",
  "the same age", "metamorphic"], sp=["conglomerate", "granite"])

# --- classification systems, gem trade (3h.viii.1 / 3h.xii.2)
M("3h.viii.1", 2, "The two main mineral classification systems, both based on chemistry and structure, are:", "Dana and Nickel-Strunz", ["Mohs and Dana",
  "Bowen and Goldich", "Wentworth and Folk"])
M("3h.viii.1", 2, "In the Nickel-Strunz system, which class number contains the silicates?", "9", ["1", "4", "7"])
M("3h.viii.1", 2, "In the Nickel-Strunz system, class 1 contains:", "native elements", ["silicates", "halides", "carbonates"])
M("3h.xii.2", 2, "The unit of weight used for gemstones, equal to 0.2 grams, is the:", "carat", ["karat", "troy ounce", "grain"])
M("3h.xii.2", 2, "'Karat' (with a K) measures:", "the purity of gold (24 karat = pure)", ["gem weight", "diamond color", "hardness"], sp=["gold"])
M("3h.xii.2", 2, "A gem cut with a smooth, domed, unfaceted top is a:", "cabochon", ["brilliant", "baguette", "emerald cut"])
M("3h.xii.2", 2, "Why are opaque or chatoyant gems like tiger's eye usually cut as cabochons?", "a domed surface displays the optical effect best",
  ["they are too hard to facet", "they cleave into domes", "facets would make them magnetic"], sp=["tigers-eye"])
M("3h.xii.2", 2, "Diamond's 'fire' (flashes of spectral colors) comes from its high:", "dispersion", ["hardness", "density", "cleavage"], sp=["diamond"])
M("3h.xii.2", 2, "Adularescence, a soft billowy glow, is characteristic of which feldspar gem (not on the list)?", "moonstone", ["sunstone", "amazonite", "labradorite"])
M("3h.iv", 2, "Iridescence on the surface of bornite and chalcopyrite is caused by:", "thin-film interference in a surface tarnish layer", ["fluorescence",
  "play-of-color", "chromium impurities"], sp=["bornite", "chalcopyrite"])

# --- extra mineral concept coverage
M("3h.ii", 2, "Which test best distinguishes gold from pyrite in the field?", "streak (yellow for gold, greenish-black for pyrite)", ["color", "luster", "magnetism"],
  sp=["gold", "pyrite"])
M("3h.ii", 2, "Which test best distinguishes hematite from magnetite?", "streak (reddish-brown vs. black) and magnetism", ["luster only", "hardness only", "acid test"],
  sp=["hematite", "magnetite"])
M("3h.ii", 2, "Which property quickly distinguishes calcite from quartz?", "hardness (calcite is scratched by a knife; quartz is not)", ["color", "luster", "streak"],
  sp=["calcite", "rock-crystal"])
M("3h.ii", 2, "Which property quickly distinguishes halite from calcite?", "cleavage angle (90° in halite vs. rhombohedral in calcite)", ["color", "streak", "luster"],
  sp=["halite", "calcite"])
M("3h.ii", 2, "Which property best distinguishes muscovite from biotite?", "color (muscovite light, biotite dark)", ["cleavage", "luster", "hardness"],
  sp=["muscovite", "biotite"])
M("3h.ii", 2, "Which property best distinguishes plagioclase from potassium feldspar in hand sample?", "striations on cleavage faces (plagioclase)",
  ["hardness", "streak", "luster"], sp=["albite", "orthoclase-microcline"])
M("3h.ii", 2, "Which property best distinguishes barite from other white minerals?", "its unusually high specific gravity", ["its streak", "its luster", "its hardness"],
  sp=["barite"])
M("3h.ii", 2, "Which property best distinguishes galena from other gray metallic minerals?", "cubic cleavage and very high specific gravity", ["green streak",
  "conchoidal fracture", "magnetism"], sp=["galena"])



def run():
    """Items were appended to authored.ITEMS at import time; authored.run() emits them."""
