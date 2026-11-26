"""Hand-written reasoning scenarios (batch 2). Every answer follows from a principle, not a memorized fact."""
from common import mcq, tf, add

TAGS = ["authored", "scenario"]


def M(t, d, p, c, ds, e="", sp=()):
    mcq(t, p, c, ds, n=min(3, len(ds)), diff=d, explanation=e, specimens=list(sp), tags=TAGS, source="authored")


def T(t, d, p, v, e="", sp=()):
    tf(t, p, v, diff=d, explanation=e, specimens=list(sp), tags=TAGS, source="authored")


def F(t, d, p, a, kp, sp=()):
    add("frq", t, p, a, keypoints=list(kp), diff=d, specimens=list(sp), tags=TAGS, source="authored")


def run():
    # ---------- mineral properties as reasoning
    M("3h.iii", 2, "An unknown mineral scratches glass but is scratched by a piece of topaz. What range must its hardness be in?",
      "between about 5.5 and 8", ["below 2.5", "between 2.5 and 3.5", "above 9"], "Glass ~5.5 < mineral < topaz 8.")
    M("3h.iii", 2, "A white mineral can be scratched by a copper coin but not by a fingernail. Its hardness is about:", "between 2.5 and 3.5",
      ["below 2.5", "between 5.5 and 7", "above 7"])
    M("3h.iii", 2, "Two minerals are the same size, but one feels about twice as heavy. What property differs most?", "specific gravity (density)",
      ["hardness", "luster", "cleavage"])
    M("3h.iii", 2, "A metallic-looking mineral leaves a reddish-brown streak. What can you conclude?", "it is likely hematite, whatever its surface color",
      ["it must be magnetite", "it must be pyrite", "the streak test failed"], sp=["hematite"])
    M("3h.iii", 3, "A mineral leaves no streak and scratches the streak plate. What does that tell you?", "its hardness is above about 6.5-7",
      ["it is metallic", "it is a carbonate", "it is magnetic"])
    M("3h.iii", 2, "A mineral breaks into perfect cubes no matter how you hit it. What does this reveal about its structure?",
      "it has three planes of weakness at 90° to each other", ["it has no planes of weakness", "it is amorphous", "it has one cleavage"],
      sp=["halite", "galena"])
    M("3h.iii", 2, "A sheet of a mineral bends and springs back when released. Which group is it most likely from?", "micas",
      ["feldspars", "carbonates", "garnets"], sp=["muscovite", "biotite"])
    M("3h.iii", 2, "A clear crystal makes a single line look doubled when placed on it. What property is this and which list mineral shows it best?",
      "double refraction - calcite", ["fluorescence - fluorite", "pleochroism - tourmaline", "chatoyancy - tiger's eye"], sp=["calcite"])
    M("3h.iv", 2, "Two white minerals look alike. One fizzes in cold dilute HCl; the other only fizzes after you scratch it into powder. Which is which?",
      "the first is calcite, the second dolomite", ["the first is dolomite, the second calcite", "both are gypsum", "the first is quartz"],
      sp=["calcite", "dolomite"])
    M("3h.iv", 2, "A black mineral sticks to a magnet and leaves a black streak. What is it most likely?", "magnetite",
      ["hematite", "graphite", "galena"], sp=["magnetite"])
    M("3h.iv", 3, "Why do some specimens of the same mineral fluoresce while others don't?", "fluorescence depends on trace activator elements and defects",
      ["only large crystals fluoresce", "fluorescence depends on hardness", "only cubic crystals fluoresce"])
    M("3h.vi", 2, "Two specimens have identical formulas but one is hexagonal and much denser. What is their relationship?", "they are polymorphs",
      ["they are a solid solution", "they are pseudomorphs", "they are the same mineral"])
    M("3h.vi", 3, "Why is pure quartz colorless while amethyst is purple?", "amethyst has trace iron plus radiation-induced color centers",
      ["amethyst has a different formula", "amethyst contains copper", "amethyst is a different crystal system"], sp=["amethyst"])
    M("3h.vi", 2, "Azurite and malachite are both copper carbonates. Why are they different colors?", "different structures and water/carbonate content change how Cu2+ absorbs light",
      ["one contains iron", "one contains chromium", "one is a sulfide"], sp=["azurite", "malachite"])
    M("3h.vi.1", 2, "An olivine is darker green and denser than another olivine. Which is closer to fayalite?", "the darker, denser one",
      ["the lighter, less dense one", "neither - color doesn't change", "both equally"], sp=["olivine"])
    M("3h.vi.1", 2, "A plagioclase crystal is Ca-rich in its core and Na-rich at its rim. What happened during its growth?",
      "the melt became more sodium-rich as it cooled", ["the melt got hotter", "it was weathered", "it was metamorphosed"], sp=["labradorite"])
    M("3h.vi.2", 3, "On the Al2SiO5 diagram, a rock contains kyanite that has been partly replaced by sillimanite. What changed?",
      "temperature increased", ["pressure dropped to near zero", "the rock was weathered", "temperature decreased at high pressure"], sp=["kyanite"])
    M("3h.vi.2", 3, "A rock contains andalusite and no kyanite or sillimanite. What does that suggest?", "it formed at low pressure",
      ["it formed at very high pressure", "it formed at the highest temperatures", "it formed at the triple point"], sp=["kyanite"])
    M("3h.vii", 2, "Diamonds found in a riverbed did not form there. Why?", "diamond forms only at mantle pressures; rivers carried it from eroded kimberlite",
      ["rivers create diamonds", "diamond forms in sand", "diamond forms at low pressure"], sp=["diamond"])
    M("3h.vii", 2, "A mollusk shell made of aragonite slowly turns to calcite over millions of years. Why?", "aragonite is metastable at surface conditions; calcite is the stable form",
      ["calcite is the high-pressure form", "the shell absorbs magnesium", "aragonite contains water"], sp=["aragonite", "calcite"])
    M("3h.viii.2", 2, "Mica peels into sheets, quartz breaks in curved surfaces, and pyroxene cleaves at ~90°. What explains all three?",
      "the way their silicate tetrahedra are linked (sheets, framework, chains)", ["their colors", "their densities", "their ages"])
    M("3h.viii.2", 3, "Why do sheet and framework silicates dominate the continental crust's late-forming minerals?",
      "silica-rich late melts favor highly polymerized structures", ["they form first from magma", "they are the densest minerals", "they contain the most iron"])
    M("3h.viii.3", 2, "A crystal looks the same after rotating it 90° about three perpendicular axes. Which crystal system?", "cubic",
      ["triclinic", "monoclinic", "hexagonal"])
    M("3h.viii.3", 2, "A prism has a six-sided cross-section but only three-fold symmetry. Which crystal system?", "trigonal",
      ["cubic", "orthorhombic", "triclinic"])
    M("3h.ix", 2, "Large galena and sphalerite crystals line fractures in a limestone. How did they likely form?",
      "precipitation from hot, metal-bearing fluids (hydrothermal)", ["evaporation of seawater", "weathering of the limestone", "crystallization from lava"],
      sp=["galena", "sphalerite"])
    M("3h.ix", 2, "Gold flakes are concentrated on the inside bends of a stream. Why?", "gold is very dense, so it drops out where the water slows",
      ["gold floats", "gold dissolves there", "gold grows there"], sp=["gold"])
    M("3h.ix", 2, "Bright green malachite stains the surface of an outcrop, but drilling hits brassy chalcopyrite below. Why the difference?",
      "near-surface oxidation converted sulfides to carbonates; below the water table sulfides survive", ["the malachite is older", "the chalcopyrite fell from above",
      "they formed from different magmas"], sp=["malachite", "chalcopyrite"])
    M("3h.x", 2, "A rock contains quartz, K-feldspar, muscovite and tourmaline in huge crystals. What environment formed it?", "a granite pegmatite",
      ["a mid-ocean ridge", "an evaporite basin", "a coral reef"], sp=["pegmatite"])
    M("3h.x", 2, "A rock contains glaucophane and lawsonite. In what setting did it form?", "a subduction zone at high pressure and low temperature",
      ["a contact aureole", "a desert", "a mid-ocean ridge at high temperature"])
    M("3h.xi", 2, "Olivine crystals in a basalt have rims of pyroxene. What does Bowen's series say happened?",
      "olivine reacted with the cooling melt to form pyroxene", ["the olivine was weathered", "pyroxene formed first", "the basalt was metamorphosed"],
      sp=["olivine", "augite"])
    M("3h.xii.1", 2, "Why is barite, not galena, used to weight drilling mud even though galena is denser?",
      "barite is non-toxic, chemically inert and cheap", ["barite is harder", "galena floats", "barite is magnetic"], sp=["barite", "galena"])
    M("3h.xii.1", 2, "Why is native gold used in electrical contacts despite its cost?", "it conducts well and never tarnishes or corrodes",
      ["it is the hardest metal", "it is magnetic", "it is the lightest metal"], sp=["gold"])
    M("3h.xii.1", 3, "Why is chalcopyrite the main copper ore even though malachite has a higher percent copper?",
      "chalcopyrite deposits are far larger and more abundant", ["malachite contains no copper", "chalcopyrite is softer", "malachite is radioactive"],
      sp=["chalcopyrite", "malachite"])

    # ---------- igneous reasoning
    M("3i.iv.4", 2, "Two granites have identical mineralogy, but one has 2 mm crystals and the other 2 cm crystals. What differs?",
      "cooling rate (the coarse one cooled more slowly or had more water)", ["chemical composition", "age only", "the number of minerals"], sp=["granite"])
    M("3i.iv.4", 2, "A lava flow has a glassy top, a fine-grained middle and slightly coarser crystals near its base. Why?",
      "the top cooled fastest against air; the interior stayed hot longest", ["the base erupted first", "the top is a different magma", "the flow was metamorphosed"])
    M("3i.iv.4", 2, "Why might a rhyolite contain both obsidian bands and tiny crystals?", "parts cooled too fast to crystallize while others had time",
      ["it is metamorphic", "it contains limestone", "it formed underwater only"], sp=["rhyolite", "obsidian"])
    M("3i.iv.4", 3, "A porphyritic basalt has large olivine phenocrysts. What can you infer about where crystallization started?",
      "olivine began crystallizing in a magma chamber before eruption", ["olivine grew after eruption", "the olivine is a xenolith from the crust",
      "it formed by weathering"], sp=["basalt", "olivine"])
    M("3i.iv.2", 2, "A volcanic rock floats on water. What two things can you infer?", "it is very vesicular and probably felsic (pumice)",
      ["it is dense and mafic", "it is metamorphic", "it contains no gas bubbles"], sp=["pumice"])
    M("3i.iv.2", 2, "A coarse rock contains 60% olivine and 40% pyroxene. What composition and setting does this suggest?",
      "ultramafic; the upper mantle", ["felsic; continental crust", "intermediate; a volcanic arc", "sedimentary; a beach"], sp=["peridotite"])
    M("3i.iv.2", 2, "As you move from basalt to andesite to rhyolite, what happens to color and density?", "they get lighter in color and less dense",
      ["they get darker and denser", "nothing changes", "they get darker but less dense"])
    M("3i.iv.3", 2, "A dike of basalt cuts through a granite. Which rock is older?", "the granite (the dike had to cut through existing rock)",
      ["the basalt dike", "they are the same age", "cannot be determined"], sp=["granite", "basalt"])
    M("3i.iv.3", 2, "A volcano produces mostly ash, pumice and violent eruptions. What does that say about its magma?",
      "it is viscous and gas-rich (felsic to intermediate)", ["it is fluid basalt", "it has no gas", "it is ultramafic"])
    M("3i.iv.5", 2, "Why do mid-ocean ridges produce basalt rather than granite?", "decompression melting of peridotite mantle yields mafic melt",
      ["seawater adds silica", "there is continental crust there", "the magma is very cold"], sp=["basalt"])
    M("3i.iv.5", 2, "Why is andesite common at ocean-continent subduction zones but rare at mid-ocean ridges?",
      "slab water causes melting, and the magma evolves and assimilates crust as it rises", ["ridges are too cold", "andesite forms from limestone",
      "ridges have no magma"], sp=["andesite"])
    M("3i.iv.6", 2, "A granite contains rounded, dark blobs of fine-grained diorite. What process do they suggest?", "magma mixing (mafic enclaves)",
      ["weathering", "metamorphism", "evaporation"], sp=["granite", "diorite"])
    M("3i.iv.6", 2, "Partially melted chunks of quartzite are found inside a basalt flow. What does this suggest?", "the magma assimilated country rock as it rose",
      ["the quartzite formed in the lava", "the basalt is metamorphic", "the quartzite is a phenocryst"], sp=["quartzite", "basalt"])
    M("3i.iv.6", 3, "Why does fractional crystallization of basalt eventually produce small volumes of granite-like melt?",
      "removing Mg-Fe minerals and Ca-plagioclase leaves the remaining melt enriched in silica, K and Na", ["granite forms first", "basalt melts the crust only",
      "water converts basalt to granite"])
    M("3i.iv.6b", 2, "Why would you look for lithium and tantalum at the margins of a granite pluton rather than its center?",
      "the last, incompatible-element-rich melt collects at the margins and forms pegmatites", ["the center is hotter", "lithium sinks to the bottom",
      "margins are always younger"], sp=["pegmatite"])
    M("3i.iv.6b", 2, "Why are olivine-rich rocks poor in lithium and beryllium?", "those incompatible elements don't fit in early mafic minerals and stay in the melt",
      ["olivine dissolves them", "they evaporate", "they are compatible in olivine"], sp=["olivine"])

    # ---------- sedimentary reasoning
    M("3i.v.3", 2, "Sediment A is well sorted and rounded; sediment B is poorly sorted and angular. Which traveled farther?", "sediment A",
      ["sediment B", "both traveled equally", "cannot tell"])
    M("3i.v.3", 2, "Why does feldspar disappear from sand as it is transported a long way?", "feldspar weathers to clay and breaks along cleavage",
      ["feldspar is denser", "feldspar dissolves instantly", "feldspar becomes quartz"])
    M("3i.v.3", 2, "A river carries boulders during floods but only sand in summer. What controls this?", "flow velocity (competence)",
      ["water temperature", "salinity", "the color of the water"])
    M("3i.v.4", 2, "A shale contains well-preserved fish fossils and fine laminations with no burrows. What can you infer?",
      "quiet, oxygen-poor bottom water", ["a high-energy beach", "a desert", "a glacier"], sp=["shale"])
    M("3i.v.4", 2, "A limestone made of whole, unbroken shells in fine mud suggests what kind of energy?", "low energy - shells were not broken or sorted",
      ["very high energy", "wind transport", "glacial transport"], sp=["fossil-limestone"])
    M("3i.v.4", 2, "A sandstone has red hematite coatings and mud cracks. What does that indicate?", "an oxidizing, periodically dry continental environment",
      ["a deep oxygen-free ocean", "a glacier", "a coral reef"])
    M("3i.v.5", 2, "Going up through a sequence, coal is followed by marine limestone. What happened?", "sea level rose and flooded a coastal swamp",
      ["the sea retreated", "a volcano erupted", "a glacier advanced"], sp=["bituminous", "fossil-limestone"])
    M("3i.v.5", 2, "Why are thick salt deposits rare in the open ocean?", "open ocean water is constantly replenished, so it never evaporates enough",
      ["salt sinks to the mantle", "salt is eaten by organisms", "salt forms only on land"], sp=["rock-salt"])
    M("3i.v.5", 2, "Why does chalk accumulate in some deep basins but not in the deepest ocean trenches?", "below the CCD, calcite coccoliths dissolve",
      ["trenches are too warm", "coccoliths can't sink", "chalk melts at depth"], sp=["chalk"])
    M("3i.v.5", 3, "Why does arkose often form in rift basins next to granite mountains?", "rapid erosion and short transport keep feldspar from weathering away",
      ["rifts are cold", "arkose forms from limestone", "rifts are underwater"], sp=["arkose"])
    M("3i.v.6", 2, "Ripple marks on a rock surface are symmetrical. What moved the water?", "back-and-forth wave action", ["a one-way river current",
      "wind only", "a glacier"])
    M("3i.v.6", 2, "A sandstone shows cross-beds dipping in opposite directions in alternating sets. What does this suggest?", "reversing tidal currents",
      ["a single river current", "deep calm water", "a lava flow"])
    M("3i.v.6", 2, "A single bed goes from coarse sand at the base to mud at the top, and this repeats dozens of times. What does that record?",
      "repeated turbidity currents on a deep-sea fan", ["daily tides", "desert winds", "a glacier"], sp=["greywacke"])
    M("3i.v.1", 2, "Why is oolitic limestone classified as chemical rather than clastic?", "its ooids grew by precipitation of calcium carbonate in place",
      ["it is made of broken shells", "it is made of rock fragments", "it formed from magma"], sp=["oolitic-limestone"])
    M("3i.v.2", 2, "Why does dolostone fizz much less than limestone in acid?", "dolomite reacts more slowly with HCl than calcite",
      ["dolostone contains no carbonate", "dolostone is metamorphic", "dolostone is harder than quartz"], sp=["dolostone"])

    # ---------- metamorphic reasoning
    M("3i.vi.1", 2, "Mica flakes in a schist are all aligned east-west. What direction was the maximum squeezing?", "north-south (perpendicular to the micas)",
      ["east-west", "vertical only", "it cannot be determined"], sp=["mica-schist"])
    M("3i.vi.1", 2, "Why does slate split along planes that cut across the original bedding?", "slaty cleavage forms perpendicular to compression, not along bedding",
      ["slate has no bedding", "bedding is always vertical", "slate is igneous"], sp=["slate"])
    M("3i.vi.2", 2, "A marble contains tremolite and diopside. What does that say about its protolith?", "it was an impure (silica-bearing) dolomitic limestone",
      ["it was pure quartz sandstone", "it was granite", "it was shale"], sp=["marble", "tremolite"])
    M("3i.vi.4", 2, "A gneiss contains rounded zircons and layers rich in aluminum minerals like kyanite. Was its protolith igneous or sedimentary?",
      "sedimentary (a paragneiss from shale)", ["igneous (granite)", "a lava flow", "cannot tell"], sp=["gneiss", "kyanite"])
    M("3i.vi.5", 2, "Marble is found in a narrow ring around a granite pluton but limestone farther out. What type of metamorphism?", "contact metamorphism",
      ["regional metamorphism", "burial metamorphism", "impact metamorphism"], sp=["marble"])
    M("3i.vi.5", 2, "Why are contact aureoles only meters to kilometers wide?", "heat from an intrusion dies off quickly with distance",
      ["contact metamorphism needs pressure", "the magma is cold", "aureoles are eroded immediately"])
    M("3i.vi.6", 2, "A slate and a gneiss came from the same shale. What was different about their histories?", "the gneiss reached much higher temperature and pressure",
      ["the slate was hotter", "the gneiss was weathered", "the slate formed from magma"], sp=["slate", "gneiss"])
    M("3i.vi.7", 2, "A basalt was metamorphosed into a green rock with chlorite and epidote. What facies?", "greenschist facies",
      ["eclogite facies", "granulite facies", "hornfels facies"], sp=["epidote"])
    M("3i.vi.7", 3, "Why don't granulite-facies rocks contain much mica or amphibole?", "those hydrous minerals break down and lose water at very high temperatures",
      ["they formed underwater", "granulites are sedimentary", "micas need high pressure"])
    M("3i.vi.8", 2, "Why is regional metamorphism concentrated along convergent plate boundaries?", "colliding plates thicken and heat the crust over large areas",
      ["divergent boundaries are hotter", "there is no pressure elsewhere", "magma only exists there"])

    # ---------- rock cycle reasoning
    M("3i.vii", 2, "Which sequence correctly turns a basalt into a sandstone?", "uplift, weathering, erosion, deposition, burial and cementation",
      ["melting then cooling", "heat and pressure without melting", "cementation then melting"], sp=["basalt"])
    M("3i.vii", 2, "Why is quartz sandstone common but olivine sandstone very rare?", "olivine weathers quickly while quartz survives transport",
      ["olivine is too light", "quartz forms in rivers", "olivine dissolves in air"], sp=["quartz-sandstone", "olivine"])
    M("3i.vii", 2, "A rock is mostly calcite with fossils. If it were buried 15 km deep in a mountain belt, what would it likely become?", "marble",
      ["quartzite", "slate", "granite"], sp=["fossil-limestone", "marble"])
    M("3i.vii", 2, "Why does limestone form cliffs in deserts but valleys in humid regions?", "limestone dissolves easily where water is abundant",
      ["deserts are colder", "limestone is harder in deserts", "wind deposits limestone"])
    M("3i.vii", 2, "Which rock type forms ridges in the Appalachian Valley and Ridge province?", "resistant quartzite and sandstone",
      ["soft shale", "soluble limestone", "loose sand"], sp=["quartzite"])

    # ---------- free response (one sentence)
    F("3i.iv.4", 2, "In one sentence, explain why obsidian has no crystals.", "It cooled so quickly that atoms could not arrange into crystals.",
      ["cooled very quickly", "no time for crystals"], sp=["obsidian"])
    F("3i.v.3", 2, "In one sentence, explain why beach sand is usually well sorted.", "Constant wave action carries away fine grains and leaves similar-sized sand.",
      ["waves remove fine grains", "constant energy sorts grains"])
    F("3i.vi.1", 2, "In one sentence, explain why marble is not foliated.", "Calcite grains are equant, so they recrystallize into interlocking grains without aligning.",
      ["calcite grains equant", "no platy minerals to align"], sp=["marble"])
    F("3i.vii", 2, "In one sentence, explain why rocks in a desert are often angular.", "Mechanical weathering dominates and there is little chemical weathering or water transport to round them.",
      ["mechanical weathering", "little chemical weathering or transport"])
    F("3h.iii", 2, "In one sentence, explain why color is an unreliable property for identifying minerals.",
      "Trace impurities and defects can change a mineral's color, so one mineral can have many colors.", ["impurities change color", "same mineral many colors"])
    F("3h.xi", 2, "In one sentence, explain why olivine weathers faster than quartz.",
      "Olivine formed at high temperature with isolated tetrahedra, so it is less stable at surface conditions than quartz's framework.",
      ["formed at high temperature", "less stable at the surface"], sp=["olivine"])
    F("3i.iv.5", 2, "In one sentence, explain why basalt is the main rock of ocean crust.",
      "Ocean crust forms at mid-ocean ridges where decompression melting of the mantle produces basaltic magma.",
      ["mid-ocean ridges", "decompression melting of mantle"], sp=["basalt"])
    F("3i.v.5", 2, "In one sentence, explain how coal indicates an ancient swamp.",
      "Coal forms from thick accumulations of plant material preserved in waterlogged, oxygen-poor swamps.", ["plant material", "waterlogged oxygen-poor swamp"],
      sp=["bituminous"])
