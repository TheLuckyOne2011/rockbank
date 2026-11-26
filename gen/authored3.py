"""Scenario and reasoning questions (concept-heavy sections), in the style of Div C invitational stations."""
from authored import M, T, S, F

# ---------------------------------------------------------------- igneous reasoning
M("3i.iv.4", 2, "A hiker finds a dark rock with tiny crystals and many round holes near an old cinder cone. What can she conclude?",
  "it is an extrusive mafic rock that cooled quickly while gas escaped (scoria or vesicular basalt)",
  ["it is an intrusive felsic rock", "it is a metamorphic rock", "it is a clastic sedimentary rock"], sp=["scoria", "basalt"])
M("3i.iv.4", 2, "A rock has large pink feldspar crystals up to 30 cm long with quartz and books of muscovite. It most likely formed:",
  "from a water-rich residual melt at the edge of a granite pluton (pegmatite)", ["by rapid cooling of lava", "in a desert dune", "from metamorphism of shale"],
  sp=["pegmatite"])
M("3i.iv.4", 2, "A basalt sample has large green olivine crystals in a dark, fine matrix. Its cooling history was:",
  "olivine grew slowly at depth, then the magma erupted and the rest cooled quickly", ["it cooled slowly the whole time",
  "it cooled quickly the whole time", "it was metamorphosed after cooling"], sp=["basalt", "olivine"])
M("3i.iv.4", 3, "Two dikes of identical composition are found: one 20 cm wide and one 20 m wide. Which is likely coarser-grained in its center and why?",
  "the 20 m dike, because its larger volume cooled more slowly", ["the 20 cm dike, because it cooled faster", "both are the same",
  "neither - dikes are always glassy"])
M("3i.iv.4", 2, "Why does the chilled margin of an intrusion have finer grains than its interior?", "magma at the contact lost heat quickly to cold country rock",
  ["the margin was metamorphosed", "the margin has a different composition", "the interior cooled first"])
M("3i.iv.2", 2, "A coarse-grained rock is about 70% dark minerals (pyroxene and olivine) and 30% calcium plagioclase. Name it.", "gabbro",
  ["granite", "diorite", "syenite"], sp=["gabbro"])
M("3i.iv.2", 2, "A fine-grained light pink volcanic rock with small quartz phenocrysts and flow banding is most likely:", "rhyolite",
  ["basalt", "andesite", "scoria"], sp=["rhyolite"])
M("3i.iv.2", 2, "A rock looks like granite but contains almost no quartz and is mostly pink K-feldspar. It is:", "syenite", ["diorite", "gabbro", "pegmatite"],
  sp=["syenite"])
M("3i.iv.2", 2, "Which observation would best distinguish diorite from granite in hand sample?", "diorite has little or no quartz and more dark minerals",
  ["diorite is finer-grained", "granite fizzes in acid", "diorite is foliated"], sp=["diorite", "granite"])
M("3i.iv.2", 2, "Two rocks have the same mineralogy, but one has crystals 5 mm across and the other microscopic. They are best described as:",
  "intrusive and extrusive equivalents", ["polymorphs", "a protolith and its metamorphic product", "unrelated rocks"])
M("3i.iv.2", 3, "Why does basaltic lava usually erupt more gently than rhyolitic lava?", "it is hotter and lower in silica, so it is less viscous and gas escapes easily",
  ["it contains more water", "it is cooler", "it has more silica"], sp=["basalt", "rhyolite"])
M("3i.iv.2", 2, "A volcano produces thick, sticky lava domes, pumice and ash. Its magma is most likely:", "felsic", ["mafic", "ultramafic", "carbonatitic"],
  sp=["pumice", "rhyolite"])
M("3i.iv.3", 2, "A layer of igneous rock lies between two sandstone beds. Pieces of the overlying sandstone are baked, but the underlying sandstone is too. It is most likely a:",
  "sill (intruded between the layers)", ["buried lava flow", "dike", "batholith"])
M("3i.iv.3", 3, "How could you tell a buried lava flow from a sill?", "a lava flow bakes only the rock beneath it and may have a weathered or vesicular top; a sill bakes rock above and below",
  ["a sill is always vesicular", "a lava flow is always coarser", "they cannot be distinguished"])
M("3i.iv.3", 2, "Wavy basalt with tube-shaped, rounded lobes found in a mountain belt suggests the basalt:", "erupted underwater (pillow lava) and was later uplifted",
  ["formed in a desert", "is a metamorphic rock", "formed from a glacier"], sp=["basalt"])
M("3i.iv.5", 2, "A chain of andesite stratovolcanoes runs parallel to an ocean trench. What plate boundary is this?", "ocean-continent subduction zone",
  ["mid-ocean ridge", "transform boundary", "continental rift"], sp=["andesite"])
M("3i.iv.5", 2, "A line of basalt volcanoes gets progressively older away from an active volcano in the middle of a plate. This records:",
  "a plate moving over a stationary hotspot", ["a mid-ocean ridge", "subduction", "a transform fault"], sp=["basalt"])
M("3i.iv.5", 2, "Why are granitic batholiths common in continents but rare in ocean basins?", "they form by melting and differentiation within thick, silica-rich continental crust",
  ["oceans are too cold", "granite sinks in the mantle", "ocean crust is too young for magma"], sp=["granite"])
M("3i.iv.5", 2, "Iceland has abundant basalt and rifts because it sits on:", "a mid-ocean ridge with a hotspot", ["a subduction zone", "a continental collision",
  "a transform fault"], sp=["basalt"])
F("3i.iv.5", 3, "Explain why subduction-zone volcanoes erupt more explosively than mid-ocean ridge volcanoes.",
  "Subduction magmas form by flux melting (water from the slab) and become more silica-rich through differentiation and crustal assimilation, so they are viscous and gas-rich; ridge magmas are hot, dry, low-silica basalts whose gas escapes easily.",
  ["water/flux melting adds gas", "higher silica = higher viscosity", "ridge basalt is hot and fluid"])
F("3i.iv.6", 3, "A single magma chamber erupts basalt early and rhyolite years later. Propose an explanation.",
  "Fractional crystallization removed early mafic minerals (olivine, pyroxene, Ca-plagioclase) from the basaltic magma, enriching the remaining melt in silica until it was rhyolitic; assimilation of crust could also contribute.",
  ["fractional crystallization", "melt enriched in silica", "possible assimilation"])
M("3i.iv.6", 2, "Granite xenoliths partly melted inside a basalt flow are evidence of:", "assimilation", ["fractional crystallization", "metamorphism", "weathering"])
M("3i.iv.6", 2, "In a cooling magma, which element is removed early by olivine crystallization, depleting the melt?", "magnesium", ["potassium", "sodium", "silicon"],
  sp=["olivine"])
M("3i.iv.6", 2, "As fractional crystallization proceeds, the ratio of iron to magnesium in the remaining melt:", "increases", ["decreases", "stays constant",
  "drops to zero"])
M("3i.iv.6b", 3, "A pegmatite contains pink tourmaline, lepidolite and spodumene. What does this tell you about the melt it formed from?",
  "it was highly evolved and enriched in incompatible elements such as Li and B", ["it was ultramafic", "it formed from seawater", "it formed during metamorphism of limestone"],
  sp=["pegmatite", "tourmaline", "lepidolite", "spodumene"])
M("3i.iv.6b", 2, "Why are pegmatites, not basalts, mined for lithium?", "lithium is incompatible and concentrates in the last, granitic melts",
  ["basalt contains no metal", "lithium is compatible in olivine", "lithium evaporates from basalt"], sp=["pegmatite", "spodumene"])
F("3i.iv.6b", 3, "Why do pegmatites often contain unusual minerals and gemstones not found in the main granite body?",
  "Incompatible elements (Li, Be, B, Cs, Ta, F) cannot enter early granite minerals, so they and water become concentrated in the final melt; that fluid-rich melt crystallizes as pegmatite, forming rare minerals like beryl, tourmaline, topaz and spodumene with large crystals.",
  ["incompatible elements concentrate late", "water-rich melt", "rare minerals and large crystals"])

# ---------------------------------------------------------------- sedimentary reasoning
M("3i.v.4", 2, "A sandstone contains angular feldspar grains, mica flakes and poorly sorted grains. Compared with a beach sandstone, it was:",
  "transported a shorter distance and buried quickly", ["transported much farther", "deposited in deep water by settling", "chemically precipitated"], sp=["arkose"])
M("3i.v.4", 2, "A rock is made of well-rounded cobbles of quartzite and granite in a sandy matrix. The cobbles were most likely shaped by:",
  "abrasion during long transport in a fast river", ["wind", "evaporation", "deep-sea settling"], sp=["conglomerate"])
M("3i.v.4", 2, "A rock unit fines upward from conglomerate to sandstone to shale. This records:", "decreasing flow energy over time (for example, a migrating river channel)",
  ["increasing energy", "a glacier advancing", "evaporation of a lake"])
M("3i.v.4", 2, "A rock unit coarsens upward from shale to sandstone. This most likely records:", "a delta or shoreline building outward into the sea",
  ["a river channel filling with mud", "deepening water", "a turbidity current"])
M("3i.v.4", 3, "Why do evaporite sequences often show limestone at the base, then gypsum, then halite?", "minerals precipitate in order of increasing solubility as the water evaporates",
  ["halite is heaviest", "gypsum forms from halite", "limestone forms last"], sp=["rock-gypsum", "rock-salt"])
M("3i.v.5", 2, "Marine fossils and limestone are found high in the Himalayas. This shows that:", "rocks deposited in an ancient ocean were later uplifted by collision",
  ["the sea was once 8 km deep", "fossils were carried up by birds", "the limestone formed on land"], sp=["fossil-limestone"])
M("3i.v.5", 2, "A coal seam overlain by marine shale suggests that:", "a coastal swamp was flooded as sea level rose", ["the swamp dried into a desert",
  "a volcano buried the swamp", "the coal formed in deep ocean"], sp=["bituminous", "shale"])
M("3i.v.5", 2, "Chert beds rich in radiolarian fossils most likely accumulated:", "in the deep ocean below the carbonate compensation depth",
  ["on a beach", "in a swamp", "in a desert"], sp=["chert-flint"])
M("3i.v.5", 2, "Red sandstone with mud cracks, raindrop prints and reptile tracks most likely formed:", "on an arid floodplain exposed to air",
  ["in the deep sea", "under a glacier", "on a coral reef"])
M("3i.v.5", 2, "A sandstone with large cross-beds, frosted grains and no mud most likely formed in a:", "desert dune field", ["delta", "deep-sea fan", "lagoon"],
  sp=["quartz-sandstone"])
M("3i.v.5", 2, "A layer of chalk overlain by sandstone records the sea becoming:", "shallower (regression)", ["deeper (transgression)", "warmer only", "saltier only"],
  sp=["chalk"])
M("3i.v.5", 2, "A vertical sequence of beach sand overlain by shelf mud and then limestone records:", "a rising sea level (transgression)",
  ["a falling sea level", "a glacier", "a volcanic eruption"])
M("3i.v.3", 2, "A river slows from 100 cm/s to 10 cm/s as it enters a lake. What happens to its sediment?", "coarse grains drop first and progressively finer grains settle farther out",
  ["all grains drop at once", "only clay drops", "nothing drops until the water stops"])
M("3i.v.3", 3, "On the Hjulström curve, a 0.01 mm silt grain resting on a stream bed needs a high velocity to erode but stays suspended at low velocity. Why?",
  "fine particles are cohesive and sit in a smooth layer, but once lifted they settle extremely slowly", ["silt is denser than gravel", "silt dissolves",
  "silt is magnetic"])
M("3i.v.3", 2, "A sediment of mixed boulders, sand and clay with scratched (striated) clasts was most likely deposited by:", "a glacier", ["wind", "a beach", "a lake"])
M("3i.v.3", 2, "Why are quartz grains in beach sand usually well rounded?", "waves move them back and forth for a long time, abrading their edges",
  ["they crystallized round", "they were rounded by acid", "quartz is soft"])
M("3i.v.6", 2, "In a cliff, cross-beds in a sandstone all dip toward the east. The ancient current or wind flowed toward the:", "east", ["west", "north", "it cannot be determined"])
M("3i.v.6", 2, "Graded beds in a tilted rock sequence have coarse grains at the top of each bed. What does this indicate?", "the sequence is overturned (upside down)",
  ["the beds are right-side up", "the beds are metamorphic", "the beds are evaporites"])
M("3i.v.6", 2, "Asymmetrical ripples with steep sides facing south were formed by a current flowing toward the:", "south", ["north", "east", "west"])
M("3i.v.6", 2, "Mud cracks in a shale between two marine limestones suggest:", "a brief period when the seafloor was exposed and dried", ["a deep-water event",
  "a volcanic eruption", "metamorphism"])
F("3i.v.6", 2, "Describe two sedimentary structures that indicate shallow water or exposure, and explain what each tells you.",
  "Mud cracks show wet sediment dried out in air; symmetrical ripple marks show wave action in shallow water; raindrop impressions also show exposure to air.",
  ["mud cracks = drying/exposure", "symmetrical ripples = shallow waves", "raindrop impressions"])
M("3i.v.2", 2, "A white, earthy rock writes on a board and fizzes strongly in acid. A similar white rock writes on a board but does not fizz. The second is most likely:",
  "diatomite", ["chalk", "travertine", "marble"], sp=["diatomite", "chalk"])
M("3i.v.2", 2, "A limestone shows concentric banding, irregular holes and was collected at a hot spring. It is:", "travertine", ["chalk", "coquina", "oolitic limestone"],
  sp=["travertine"])
M("3i.v.2", 2, "Why does lignite contain more water than anthracite?", "lignite was buried less deeply, so less water was squeezed and driven out",
  ["lignite formed underwater", "anthracite absorbs water", "lignite contains clay"], sp=["lignite", "anthracite"])
M("3i.v.2", 2, "A coal is shiny, hard, breaks with conchoidal fracture and leaves no black smudge on fingers. It is:", "anthracite", ["lignite", "bituminous coal", "peat"],
  sp=["anthracite"])
M("3i.v.1", 2, "Which is the best way to tell a clastic rock from a crystalline chemical sedimentary rock with a hand lens?", "look for separate cemented grains versus interlocking crystals",
  ["check its color", "check for foliation", "check its magnetism"])

# ---------------------------------------------------------------- metamorphic reasoning
M("3i.vi.5", 2, "A shale next to a granite intrusion has been turned into a hard, fine-grained, non-foliated rock. What happened?",
  "contact metamorphism produced hornfels", ["regional metamorphism produced slate", "weathering produced clay", "melting produced obsidian"], sp=["granite", "shale"])
M("3i.vi.5", 2, "Moving toward a granite pluton, a geologist finds shale, then spotted slate, then hornfels. What controls this pattern?",
  "temperature increasing toward the intrusion", ["pressure decreasing toward the intrusion", "water depth", "distance from the ocean"])
M("3i.vi.5", 2, "Slate found across hundreds of square kilometers of a mountain belt formed by:", "regional metamorphism", ["contact metamorphism", "impact metamorphism",
  "weathering"], sp=["slate"])
M("3i.vi.5", 2, "Why is marble from a contact aureole usually not foliated?", "heat dominated with little directed stress, so crystals grew without alignment",
  ["marble cannot be foliated under any conditions", "it was never heated", "it melted"], sp=["marble"])
M("3i.vi.4", 2, "A foliated rock contains abundant muscovite, garnet and quartz. Its protolith was most likely:", "shale", ["limestone", "basalt", "peridotite"],
  sp=["garnet-schist", "shale"])
M("3i.vi.4", 2, "A dark rock of aligned hornblende and plagioclase most likely formed from:", "basalt or gabbro", ["shale", "sandstone", "limestone"], sp=["amphibolite"])
M("3i.vi.4", 2, "A non-foliated rock that fizzes in acid and has interlocking crystals formed from:", "limestone", ["sandstone", "shale", "granite"], sp=["marble"])
M("3i.vi.4", 2, "A green, waxy rock with a slippery feel, found in an ophiolite, formed from:", "peridotite", ["shale", "limestone", "granite"], sp=["serpentinite"])
M("3i.vi.4", 2, "A hard, non-foliated rock that breaks through its grains and does not fizz formed from:", "quartz sandstone", ["limestone", "shale", "basalt"],
  sp=["quartzite"])
M("3i.vi.6", 2, "A schist contains biotite and garnet but no staurolite. A schist farther east contains kyanite. Which direction did metamorphic grade increase?",
  "toward the east", ["toward the west", "grade was the same", "cannot be determined"])
M("3i.vi.6", 2, "Why does slate have microscopic grains while schist has visible mica?", "higher temperatures in schist let crystals grow larger",
  ["slate formed from different minerals", "schist cooled faster", "slate formed at higher temperature"], sp=["slate", "mica-schist"])
M("3i.vi.6", 2, "Why does foliation become coarser from slate to phyllite to schist to gneiss?", "rising temperature and pressure cause recrystallization into larger grains and eventually banding",
  ["each rock has a different protolith", "weathering increases", "the rocks are younger"])
M("3i.vi.7", 2, "A rock with glaucophane found next to an ancient trench indicates:", "high pressure at low temperature in a subduction zone",
  ["high temperature at low pressure", "contact with magma", "surface weathering"])
M("3i.vi.7", 2, "Eclogite found in the Alps tells geologists that some rocks there were:", "subducted to depths over ~50-70 km and returned to the surface",
  ["formed in lava flows", "deposited in lakes", "never buried"])
M("3i.vi.7", 3, "Why does blueschist require unusual tectonic conditions?", "rocks must reach high pressure while staying cold, which happens only when cold slabs sink quickly",
  ["it needs very high temperature", "it forms at the surface", "it needs evaporites"])
F("3i.vi.7", 3, "Compare the conditions that produce hornfels-facies and blueschist-facies rocks.",
  "Hornfels facies forms at high temperature and low pressure next to shallow intrusions (contact metamorphism). Blueschist facies forms at high pressure and low temperature where cold oceanic crust is rapidly subducted.",
  ["hornfels: high T, low P, contact", "blueschist: high P, low T, subduction"])
F("3i.vi.8", 3, "Explain how paired metamorphic belts form at a subduction zone.",
  "Near the trench, cold subducting crust reaches high pressure at low temperature, producing blueschist and eclogite. Farther inland beneath the volcanic arc, rising magma adds heat, producing high-temperature, lower-pressure metamorphism (greenschist to amphibolite).",
  ["trench side: high P / low T", "arc side: high T / lower P", "two parallel belts"])
M("3i.vi.3", 2, "In a metamorphosed siliceous limestone, calcite reacts with quartz. Which list mineral forms?", "wollastonite", ["kyanite", "staurolite", "biotite"],
  sp=["wollastonite"])
M("3i.vi.3", 2, "Which mineral would form in a metamorphosed coal-bearing shale but not in a clean quartzite?", "graphite", ["quartz", "magnetite only", "halite"],
  sp=["graphite"])
M("3i.vi.3", 2, "Chlorite gives way to biotite and then garnet as grade increases. What drives these changes?", "rising temperature makes new minerals more stable",
  ["weathering", "falling temperature", "evaporation"])
M("3i.vi.1", 2, "A metamorphic rock splits into flat, smooth sheets but its minerals are too small to see. It is:", "slate", ["gneiss", "schist", "marble"], sp=["slate"])
M("3i.vi.1", 2, "A metamorphic rock has a satiny sheen and wavy foliation but no visible mineral grains. It is:", "phyllite", ["slate", "gneiss", "quartzite"], sp=["phyllite"])
M("3i.vi.1", 2, "A metamorphic rock has distinct light and dark bands of coarse minerals. It is:", "gneiss", ["slate", "phyllite", "hornfels"], sp=["gneiss"])
M("3i.vi.1", 2, "All gneissic banding is foliation, but is all foliation banding?", "no - slaty cleavage and schistosity are foliation without banding",
  ["yes", "no - banding is not foliation", "only in marble"])

# ---------------------------------------------------------------- rock cycle reasoning
M("3i.vii", 2, "A sandstone is buried 20 km deep in a collision zone, then partly melts. Which rocks could form in sequence?", "quartzite or gneiss, then migmatite, then granite",
  ["shale, then coal", "basalt, then pumice", "limestone, then chalk"])
M("3i.vii", 2, "Which energy source drives weathering and erosion in the rock cycle?", "the Sun (through the water cycle and atmosphere) and gravity",
  ["Earth's internal heat only", "radioactive decay only", "the Moon's tides only"])
M("3i.vii", 2, "Which energy source drives melting and metamorphism in the rock cycle?", "Earth's internal heat", ["sunlight", "wind", "ocean waves"])
M("3i.vii", 2, "Why is the rock cycle called a cycle?", "rock material is continuously recycled among igneous, sedimentary and metamorphic forms",
  ["rocks always return to the same type", "it repeats every year", "it only applies to igneous rocks"])
M("3i.vii", 2, "Which process in the rock cycle is the slowest step for a granite to become a sandstone?", "weathering and erosion after uplift", ["melting", "lava cooling", "metamorphism"],
  sp=["granite"])
M("3i.vii", 2, "Weathering happens in situ, meaning:", "in place, without the material being moved", ["after transport", "only underwater", "only in deserts"])
M("3i.vii", 2, "Why does chemical weathering dominate in the tropics?", "warmth and abundant water speed chemical reactions", ["there is little rain", "freezing is common",
  "rocks are softer there"])
M("3i.vii", 2, "Why does physical weathering speed up chemical weathering?", "breaking rock into smaller pieces increases the surface area exposed to reactions",
  ["it adds acid", "it raises temperature", "it removes water"])
M("3i.vii", 2, "Which mineral weathers into kaolinite clay?", "feldspar", ["quartz", "calcite", "halite"], sp=["kaolinite"])
M("3i.vii", 2, "Which mineral survives weathering of granite to become sand?", "quartz", ["feldspar", "biotite", "hornblende"], sp=["granite", "quartz-sandstone"])
M("3i.vii", 2, "Why are very old obsidian samples rare?", "volcanic glass slowly devitrifies (crystallizes) and hydrates over millions of years",
  ["obsidian evaporates", "obsidian melts at room temperature", "obsidian turns into limestone"], sp=["obsidian"])
M("3i.vii", 2, "A conglomerate contains pebbles of basalt, gneiss and limestone. What does this reveal?", "the source area exposed all three rock types",
  ["the conglomerate is igneous", "the pebbles formed in place", "the conglomerate is metamorphic"], sp=["conglomerate"])
F("3i.vii", 2, "Trace a path through the rock cycle from basalt to marble.",
  "Basalt weathers; its calcium is released into solution and carried to the sea, where organisms and chemical precipitation form limestone; the limestone is buried and metamorphosed into marble.",
  ["weathering releases Ca", "limestone forms in sea", "metamorphism to marble"], sp=["basalt", "marble"])
F("3i.vii", 2, "Explain the difference between weathering and erosion.",
  "Weathering breaks rock down in place (mechanically or chemically); erosion removes and transports the weathered material by water, wind, ice or gravity.",
  ["weathering in place", "erosion transports"])

# ---------------------------------------------------------------- mineral concept reasoning
M("3h.xi", 2, "Is the upper part of Bowen's reaction series (olivine, Ca-plagioclase) found mainly in mafic or felsic rocks?", "mafic", ["felsic", "neither", "evaporites"])
M("3h.xi", 3, "Why do minerals near the top of Bowen's series weather fastest at Earth's surface?", "they formed at conditions most different from surface conditions, with less-polymerized structures",
  ["they are softest", "they contain water", "they are always the largest crystals"])
M("3h.xi", 2, "Which branch of Bowen's series involves a change in crystal structure from one mineral to the next?", "the discontinuous branch", ["the continuous branch",
  "both", "neither"])
M("3h.xi", 2, "What changes along the continuous branch of Bowen's series?", "plagioclase composition shifts from Ca-rich to Na-rich", ["the crystal structure changes",
  "olivine becomes pyroxene", "quartz becomes feldspar"])
M("3h.xi", 3, "Why do quartz and K-feldspar crystallize last from a magma?", "they form from the silica- and potassium-rich melt left after early minerals are removed",
  ["they are the densest minerals", "they need the highest temperatures", "they form from water only"])
F("3h.xi", 3, "Using Bowen's reaction series, explain why basalt and granite contain different minerals.",
  "Basalt crystallizes from hot mafic magma, so it contains high-temperature minerals at the top of the series (olivine, pyroxene, Ca-plagioclase). Granite crystallizes from cooler, silica-rich melt and contains low-temperature minerals (quartz, K-feldspar, muscovite, Na-plagioclase, biotite).",
  ["basalt = high-T minerals", "granite = low-T minerals", "magma composition and temperature"])
M("3h.vi.2", 3, "On a plagioclase melting diagram, a melt of An60 begins to crystallize. The first crystals are:", "more calcium-rich than An60", ["exactly An60",
  "more sodium-rich than An60", "pure albite"], sp=["labradorite"])
M("3h.vi.2", 3, "If early plagioclase crystals are not removed and the system stays in equilibrium, the final rock's plagioclase will be:", "the same composition as the original melt",
  ["pure anorthite", "pure albite", "zoned from An100 to An0"])
M("3h.vi.2", 3, "Zoned plagioclase with Ca-rich cores and Na-rich rims shows crystallization was:", "too fast for the crystals to re-equilibrate with the melt",
  ["perfectly at equilibrium", "caused by metamorphism", "caused by weathering"])
M("3h.vi.2", 2, "On a P-T phase diagram for Al2SiO5, a rock that crossed from the kyanite field into the sillimanite field experienced:", "an increase in temperature",
  ["a decrease in temperature only", "weathering", "a decrease in pressure into the andalusite field"], sp=["kyanite"])
M("3h.vii", 2, "Why might a rock contain both andalusite and kyanite in different layers?", "it experienced changing pressure-temperature conditions over time",
  ["they have different compositions", "one is igneous", "they formed from different magmas"], sp=["kyanite"])
M("3h.vi.1", 2, "Why can Fe2+ replace Mg2+ in olivine but K+ cannot?", "Fe2+ has the same charge and a similar size to Mg2+; K+ is much larger with a different charge",
  ["K+ is heavier", "K+ is magnetic", "Fe is more common"], sp=["olivine"])
M("3h.vi.1", 2, "How does increasing iron content change olivine's specific gravity and color?", "SG increases and the color darkens", ["SG decreases and color lightens",
  "no change", "SG increases and it turns blue"], sp=["olivine"])
M("3h.vi.1", 3, "In plagioclase, why must Al3+ replace Si4+ when Ca2+ replaces Na+?", "to keep the crystal electrically neutral (coupled substitution)",
  ["because Al is larger", "because Ca is smaller", "it does not have to"], sp=["albite", "labradorite"])
M("3h.viii.2", 3, "Why does olivine (a nesosilicate) have no good cleavage?", "its isolated tetrahedra are linked in all directions by strong ionic bonds to Mg and Fe",
  ["it is amorphous", "it is a sheet silicate", "it contains water"], sp=["olivine"])
M("3h.viii.2", 2, "Mica sheets peel apart easily because:", "the sheets are held together only by weak bonds to potassium ions", ["mica contains no oxygen",
  "the sheets are metallic", "mica is amorphous"], sp=["muscovite", "biotite"])
M("3h.viii.3", 2, "Why does halite cleave into cubes while quartz breaks with conchoidal fracture?", "halite has planes of weak ionic bonding; quartz has strong Si-O bonds in all directions",
  ["halite is harder", "quartz is cubic", "halite is amorphous"], sp=["halite", "rock-crystal"])
M("3h.ix", 2, "A cave contains stalactites of calcite and a few needle-like crystals of aragonite. What might favor the aragonite?", "magnesium-rich drip water",
  ["very low pressure", "high temperature only", "the absence of water"], sp=["aragonite"])
M("3h.ix", 2, "Why are malachite and azurite found near the surface above copper deposits but not deep down?", "they form by oxidation of primary copper sulfides by oxygen-rich groundwater",
  ["they crystallize from magma", "they form at high pressure", "they are carried up by volcanoes"], sp=["malachite", "azurite"])
M("3h.ix", 2, "Why do gold and zircon accumulate in placer deposits?", "they are dense and resist weathering, so water concentrates them", ["they are soluble",
  "they are light and float", "they form in streams"], sp=["gold", "zircon"])
M("3h.ix", 2, "Why are evaporites like halite rarely preserved in humid climates?", "rainwater dissolves them", ["they melt", "they oxidize", "they are eaten by organisms"],
  sp=["halite", "rock-salt"])
M("3h.x", 2, "Which mineral pair would you expect in a mid-ocean ridge gabbro?", "Ca-plagioclase and augite", ["quartz and muscovite", "halite and gypsum",
  "kyanite and staurolite"], sp=["gabbro", "augite"])
M("3h.x", 2, "Which mineral pair would you expect in a granite pegmatite?", "beryl and tourmaline", ["olivine and augite", "halite and gypsum", "glaucophane and lawsonite"],
  sp=["beryl", "tourmaline"])
M("3h.x", 2, "Which mineral pair would you expect in an evaporite basin?", "halite and gypsum", ["olivine and augite", "kyanite and staurolite", "beryl and topaz"],
  sp=["halite", "selenite"])
M("3h.x", 2, "Which mineral pair would you expect in a medium-grade pelitic schist?", "garnet and staurolite", ["olivine and augite", "halite and gypsum",
  "sodalite and nepheline"], sp=["almandine", "staurolite"])
M("3h.x", 2, "Which mineral pair would you expect in a nepheline syenite?", "sodalite and K-feldspar", ["quartz and olivine", "halite and calcite", "kyanite and garnet"],
  sp=["sodalite", "syenite"])
def run():
    """Items are emitted by authored.run()."""
