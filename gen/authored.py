"""Hand-written concept questions, modeled on Division C invitational tests (scio.ly archive, 2014-2026).

Compact forms:
  M(topic, diff, prompt, correct, [distractors], explanation, specimens)  multiple choice
  T(topic, diff, statement, truth, explanation, specimens)                true/false
  S(topic, diff, prompt, answer, [also accept], explanation, specimens)   short answer
  F(topic, diff, prompt, model answer, [key points], specimens)           free response
"""
from common import add, mcq, tf, short

ITEMS = []


def M(t, d, p, c, ds, e="", sp=()):
    ITEMS.append(("M", t, d, p, c, ds, e, sp))


def T(t, d, p, v, e="", sp=()):
    ITEMS.append(("T", t, d, p, v, None, e, sp))


def S(t, d, p, a, acc=(), e="", sp=()):
    ITEMS.append(("S", t, d, p, a, acc, e, sp))


def F(t, d, p, a, kp=(), sp=()):
    ITEMS.append(("F", t, d, p, a, kp, "", sp))


# =====================================================================  MINERALS
# --- definition & basics
M("3h.i", 1, "Which property is NOT required for a substance to be a mineral?", "it must be metallic",
  ["it must be naturally occurring", "it must be a solid", "it must have an ordered crystal structure"])
M("3h.i", 2, "Why is obsidian not considered a mineral?", "it has no ordered crystalline structure",
  ["it is organic", "it is not naturally occurring", "it has no definite chemical formula at all"], sp=["obsidian"])
M("3h.i", 2, "A naturally occurring solid that lacks a crystal structure, such as opal, is called a:", "mineraloid",
  ["polymorph", "pseudomorph", "protolith"], sp=["opal"])
M("3h.i", 2, "A mineral that has replaced another while keeping the original's outward shape is a:", "pseudomorph",
  ["polymorph", "mineraloid", "porphyroblast"])
S("3h.i", 2, "What term describes a mineral that takes the external form of a different mineral it replaced?", "pseudomorph", ["pseudomorph"])
T("3h.i", 1, "Minerals can be made by living organisms and still count as minerals under the Science Olympiad definition.", False,
  "The SO definition requires minerals to be inorganic; biogenic materials such as pearl or amber are excluded.")
T("3h.i", 2, "A single mineral species can have a range of compositions, such as olivine between forsterite and fayalite.", True,
  "Solid solutions vary in composition within fixed limits.")
M("3h.i", 1, "About how many mineral species are currently recognized by the IMA?", "about 6,000", ["about 50", "about 500", "about 1 million"])
M("3h.i", 2, "Which two elements make up most of Earth's crust by mass?", "oxygen and silicon",
  ["iron and magnesium", "aluminum and calcium", "carbon and hydrogen"], "O ~46%, Si ~28% - which is why silicates dominate.")
M("3h.i", 2, "Which mineral group makes up the largest share of Earth's crust?", "feldspars", ["quartz", "micas", "carbonates"],
  "Feldspars make up roughly half of the crust.")

# --- physical properties concepts
M("3h.iii", 1, "Which is the LEAST reliable property for identifying most minerals?", "color", ["streak", "hardness", "cleavage"],
  "Trace impurities change color easily; streak is far more consistent.")
M("3h.iii", 1, "What is streak?", "the color of a mineral's powder", ["the color of a fresh surface", "the way light reflects from a surface",
  "the pattern left by cleavage"])
M("3h.iii", 2, "Why do minerals harder than about 6.5-7 not leave a streak on an unglazed porcelain plate?", "they are harder than the plate and scratch it instead",
  ["they are always colorless", "they dissolve in the plate", "they have no cleavage"])
M("3h.iii", 1, "Luster describes:", "how a mineral's surface reflects light", ["the color of its powder", "its resistance to scratching", "how it breaks"])
M("3h.iii", 1, "The tendency of a mineral to break along flat planes of weakness is:", "cleavage", ["fracture", "parting", "tenacity"])
M("3h.iii", 2, "How does parting differ from cleavage?", "parting follows planes of weakness from twinning or inclusions, not the basic structure",
  ["parting is curved", "parting only occurs in metals", "parting is the same as fracture"], sp=["corundum", "magnetite"])
M("3h.iii", 1, "Smooth, curved, shell-like breakage, as in quartz and obsidian, is called:", "conchoidal fracture",
  ["hackly fracture", "splintery fracture", "uneven fracture"])
M("3h.iii", 1, "Tenacity describes:", "a mineral's resistance to breaking, bending or crushing", ["its density", "its luster", "its crystal system"])
M("3h.iii", 2, "A mineral that can be cut into thin shavings with a knife is:", "sectile", ["brittle", "elastic", "ductile"])
M("3h.iii", 2, "A mineral that bends and springs back to its original shape is:", "elastic", ["flexible but inelastic", "malleable", "brittle"],
  sp=["muscovite", "biotite"])
M("3h.iii", 2, "A mineral that can be hammered into thin sheets is:", "malleable", ["sectile", "brittle", "elastic"], sp=["gold", "copper", "silver"])
M("3h.iii", 1, "Specific gravity is:", "the ratio of a mineral's density to the density of water", ["its mass in grams",
  "its hardness compared to diamond", "its weight in water only"])
M("3h.iii", 2, "Heft refers to:", "how heavy a specimen feels for its size", ["how hard it is", "its luster", "how it breaks"])
M("3h.iii", 2, "Which mineral on the list has the highest specific gravity?", "gold", ["galena", "silver", "copper"], "Gold SG ~19.3.", ["gold"])
M("3h.iii", 2, "Why are metallic minerals generally heavier than non-metallic ones?", "they contain heavy metal atoms packed closely",
  ["they contain more water", "they are always cubic", "they have no cleavage"])
M("3h.iii", 1, "A mineral that lets light pass through but you cannot see clearly through it is:", "translucent", ["transparent", "opaque", "adamantine"])
M("3h.iii", 1, "Diaphaneity describes:", "how well light passes through a mineral", ["its hardness", "its streak", "its smell"])
M("3h.iii", 2, "What is the Mohs scale?", "a relative (ordinal) scale of scratch hardness", ["an absolute linear scale of hardness",
  "a scale of density", "a scale of melting points"], "Diamond (10) is roughly 4x harder than corundum (9) in absolute terms.")
T("3h.iii", 2, "The Mohs scale is linear, so diamond (10) is about 10% harder than corundum (9).", False,
  "It is ordinal; absolute hardness jumps enormously from 9 to 10.")
M("3h.iii", 1, "A steel knife blade or a glass plate has a Mohs hardness of about:", "5.5", ["2.5", "3.5", "7"])
M("3h.iii", 1, "A fingernail has a Mohs hardness of about:", "2.5", ["1", "4", "5.5"])
M("3h.iii", 1, "A copper penny has a Mohs hardness of about:", "3.5", ["2", "5.5", "6.5"])
M("3h.iii", 1, "An unglazed porcelain streak plate has a hardness of about:", "6.5-7", ["3", "4.5", "9"])
M("3h.iii", 2, "Adamantine luster is typical of minerals with:", "a very high refractive index (e.g., diamond, zircon)",
  ["metallic bonding", "fibrous habits", "high water content"])
M("3h.iii", 2, "A silky luster usually indicates:", "a fibrous structure", ["a metallic composition", "high density", "cubic crystals"],
  sp=["satin-spar", "tigers-eye"])
M("3h.iii", 2, "A pearly luster is most often seen on:", "cleavage surfaces of sheet-like minerals", ["metallic sulfides", "glass", "earthy clays"])
M("3h.iii", 3, "Kyanite has hardness of about 4.5-5 along its length and 6.5-7 across it. This direction-dependence is called:",
  "hardness anisotropy", ["pleochroism", "birefringence", "chatoyancy"], sp=["kyanite"])
M("3h.iii", 2, "Which crystal faces are LEAST affected when measuring hardness?", "none - hardness should be tested on a fresh, clean surface",
  ["weathered surfaces give the best results", "only cleavage faces work", "only fracture surfaces work"])
F("3h.iii", 2, "A student scratches a mineral with a steel nail and leaves a powdery line. How can she tell whether the mineral was scratched or the nail left a metal streak?",
  "Rub the line with a finger: a metal streak from the nail rubs off, while a true scratch leaves a groove that remains (check with a hand lens).",
  ["rub to see if it wipes off", "true scratch is a groove", "use a hand lens"])

# --- other properties
M("3h.iv", 1, "Fluorescence is:", "emission of visible light while a mineral is exposed to ultraviolet light", ["glowing after UV is turned off",
  "color change in sunlight", "sparkling from inclusions"])
M("3h.iv", 2, "Phosphorescence is:", "continued glowing after the UV light is turned off", ["glowing only under UV", "producing a charge under pressure",
  "light from heating"])
M("3h.iv", 2, "Light emitted when a mineral is heated is called:", "thermoluminescence", ["triboluminescence", "phosphorescence", "piezoelectricity"], sp=["fluorite"])
M("3h.iv", 2, "Light emitted when a mineral is scratched or crushed is called:", "triboluminescence", ["thermoluminescence", "fluorescence", "chatoyancy"],
  sp=["sphalerite"])
M("3h.iv", 3, "Why is fluorescent light emitted at a longer wavelength than the UV that excites it?", "some absorbed energy is lost as heat before emission",
  ["the mineral adds energy", "UV light has a longer wavelength than visible light", "fluorescence is caused by reflection"])
M("3h.iv", 2, "Elements such as manganese that trigger fluorescence in small amounts are called:", "activators", ["quenchers", "chromophores", "inhibitors"],
  sp=["willemite", "calcite"])
M("3h.iv", 2, "Why does some fluorite fluoresce while other fluorite does not?", "fluorescence depends on trace impurities (activators)",
  ["only cubic crystals fluoresce", "only purple fluorite contains calcium", "fluorescence depends on crystal size"], sp=["fluorite"])
M("3h.iv", 1, "Piezoelectricity is:", "an electric charge produced when a crystal is squeezed", ["attraction to a magnet", "glowing under UV",
  "conducting heat"], sp=["rock-crystal", "tourmaline"])
M("3h.iv", 2, "Why is quartz used in watches and clocks?", "its piezoelectric vibration has a very stable frequency", ["it is magnetic",
  "it fluoresces", "it is radioactive"], sp=["rock-crystal"])
M("3h.iv", 2, "Pyroelectricity is:", "an electric charge that develops when a crystal is heated or cooled", ["melting in a flame", "glowing when heated",
  "loss of water on heating"], sp=["tourmaline"])
M("3h.iv", 1, "Double refraction makes a single line viewed through the mineral appear as:", "two lines", ["a blur", "a rainbow", "no line at all"],
  sp=["calcite"])
M("3h.iv", 2, "Which crystal system's minerals cannot show double refraction?", "cubic (isometric)", ["hexagonal", "monoclinic", "trigonal"])
M("3h.iv", 2, "The play of color in precious opal is caused by:", "diffraction of light by regularly stacked silica spheres",
  ["chromium impurities", "thin films of oil", "fluorescence"], sp=["opal"])
M("3h.iv", 2, "Labradorescence is caused by:", "light interference in thin exsolution layers", ["fluorescence", "radioactivity", "iron staining"],
  sp=["labradorite"])
M("3h.iv", 2, "Chatoyancy (a cat's-eye effect) is caused by:", "light reflecting from many parallel fibers or needles", ["dispersion",
  "phosphorescence", "magnetism"], sp=["tigers-eye"])
M("3h.iv", 2, "Asterism (a star effect) in star sapphires is caused by:", "aligned needles of rutile", ["play-of-color", "dendrites", "gas bubbles"],
  sp=["corundum", "rutile"])
M("3h.iv", 2, "Tenebrescence is:", "a reversible color change caused by exposure to light", ["glowing when heated", "a cat's-eye effect", "sparkle from mica"],
  sp=["sodalite"])
M("3h.iv", 2, "Pleochroism is:", "showing different colors when viewed from different directions", ["glowing under UV", "two images through a crystal",
  "iridescent tarnish"], sp=["tourmaline", "epidote", "kyanite"])
M("3h.iv", 2, "Why is zircon slightly radioactive?", "it contains trace uranium and thorium substituting for zirconium", ["it contains radium",
  "zirconium is radioactive", "it absorbs cosmic rays"], sp=["zircon"])
M("3h.iv", 2, "Radiation damage that destroys a crystal's structure over time, as in some zircons, is called:", "metamictization",
  ["exsolution", "dolomitization", "twinning"], sp=["zircon"])
M("3h.iv", 2, "Which acid test result distinguishes calcite from dolomite?", "calcite fizzes in cold dilute HCl; dolomite fizzes only when powdered",
  ["dolomite fizzes more strongly", "neither reacts", "only dolomite turns red"], sp=["calcite", "dolomite"])
M("3h.iv", 2, "Carbonate minerals fizz in HCl because they release:", "carbon dioxide gas", ["hydrogen gas", "chlorine gas", "oxygen gas"])
S("3h.iv", 2, "Write the balanced reaction for calcite with hydrochloric acid.", "CaCO3 + 2HCl -> CaCl2 + H2O + CO2",
  ["caco3 + 2hcl -> cacl2 + h2o + co2", "caco3+2hcl->cacl2+h2o+co2"], sp=["calcite"])
M("3h.iv", 2, "Which gas causes the rotten-egg smell when sphalerite powder is placed in HCl?", "hydrogen sulfide (H2S)",
  ["carbon dioxide", "sulfur dioxide", "chlorine"], sp=["sphalerite"])
M("3h.iv", 2, "Which list mineral has a salty taste? (Taste tests are not allowed in competition.)", "halite", ["sylvite", "ulexite", "gypsum"], sp=["halite"])
M("3h.iv", 2, "Which mineral, besides magnetite, becomes magnetic after heating in a flame?", "siderite", ["calcite", "quartz", "galena"], sp=["siderite"])
M("3h.iv", 3, "Magnetite is described as ferrimagnetic because:", "Fe ions on two kinds of sites have opposed but unequal magnetic moments",
  ["all Fe ions align in parallel", "it contains nickel", "it is a native element"], sp=["magnetite"])

# --- habits & twinning
M("3h.v", 2, "Swallowtail twins are characteristic of:", "gypsum (selenite)", ["quartz", "pyrite", "staurolite"], sp=["selenite"])
M("3h.v", 2, "'Iron cross' penetration twins are characteristic of:", "pyrite", ["galena", "magnetite", "fluorite"], sp=["pyrite"])
M("3h.v", 2, "'Fairy cross' twins that intersect at 90° are characteristic of:", "staurolite", ["kyanite", "tourmaline", "aragonite"], sp=["staurolite"])
M("3h.v", 2, "Carlsbad twinning is common in:", "orthoclase", ["quartz", "calcite", "garnet"], sp=["orthoclase-microcline"])
M("3h.v", 2, "Fine parallel striations on the cleavage faces of plagioclase are caused by:", "polysynthetic (albite) twinning",
  ["contact twinning", "Carlsbad twinning", "dendritic growth"], sp=["albite", "labradorite"])
M("3h.v", 2, "Elbow-shaped (geniculate) twins are typical of:", "rutile", ["halite", "beryl", "talc"], sp=["rutile"])
M("3h.v", 2, "Cross-hatched 'tartan' twinning seen in thin section identifies:", "microcline", ["orthoclase", "quartz", "calcite"],
  sp=["orthoclase-microcline"])
M("3h.v", 2, "Hopper crystals have hollow, stepped faces because:", "the edges grew faster than the face centers", ["they dissolved partly",
  "they are pseudomorphs", "they formed by twinning"], sp=["halite"])
M("3h.v", 2, "Pisolitic habit refers to grains that are:", "pea-sized and rounded", ["needle-like", "flat and platy", "tree-like"], sp=["bauxite"])
M("3h.v", 2, "Ooids differ from pisoids mainly by:", "size - ooids are under 2 mm, pisoids over 2 mm", ["composition", "color", "crystal system"],
  sp=["oolitic-limestone"])
M("3h.v", 2, "Dendrites of manganese oxide on rock surfaces are often mistaken for:", "plant fossils", ["gold veins", "fossil bones", "worm tracks"],
  sp=["pyrolusite"])
M("3h.v", 2, "A crystal with faces at both ends because it grew without being attached to a surface is:", "doubly terminated",
  ["druzy", "massive", "geodic"], sp=["rock-crystal"])
M("3h.v", 1, "A hollow rock lined with inward-pointing crystals is a:", "geode", ["nodule", "concretion", "vesicle"], sp=["amethyst", "celestite"])
M("3h.v", 2, "A crystal-lined cavity in a vein or rock (not necessarily a round nodule) is a:", "vug", ["dike", "amygdule", "ooid"])
M("3h.v", 2, "A vesicle in volcanic rock that has been filled with secondary minerals is an:", "amygdule", ["ooid", "phenocryst", "xenolith"])
M("3h.v", 2, "Barite and gypsum 'desert roses' form when crystals grow:", "as rosettes in sand, trapping sand grains", ["in caves as stalactites",
  "from lava", "in coral reefs"], sp=["barite"])
M("3h.v", 2, "Acicular means:", "needle-like", ["leaf-like", "grape-like", "cube-shaped"])
M("3h.v", 2, "Botryoidal means:", "grape-like rounded masses", ["needle-like", "tree-like", "tablet-shaped"])

# --- chemistry
M("3h.vi", 2, "Minerals are classified into chemical classes based mainly on their:", "dominant anion or anion group",
  ["dominant cation", "color", "crystal system"])
M("3h.vi", 1, "Which anion group defines the carbonates?", "CO3 2-", ["SO4 2-", "SiO4 4-", "PO4 3-"])
M("3h.vi", 1, "Which anion group defines the sulfates?", "SO4 2-", ["S 2-", "CO3 2-", "PO4 3-"])
M("3h.vi", 1, "Which anion defines the sulfides?", "S 2-", ["SO4 2-", "O 2-", "Cl -"])
M("3h.vi", 1, "Which anion group defines the phosphates?", "PO4 3-", ["SO4 2-", "CO3 2-", "BO3 3-"])
M("3h.vi", 1, "Halides contain which kind of anion?", "a halogen such as F- or Cl-", ["O 2-", "S 2-", "CO3 2-"])
M("3h.vi", 2, "The basic building block of all silicate minerals is:", "the SiO4 tetrahedron", ["the CO3 triangle", "the SO4 tetrahedron", "the AlO6 octahedron"])
M("3h.vi", 2, "What is the net charge of a single SiO4 tetrahedron?", "-4", ["-2", "0", "+4"])
M("3h.vi", 2, "What is the oxidation state of iron in hematite (Fe2O3)?", "+3", ["+2", "+1", "a mix of +2 and +3"], sp=["hematite"])
M("3h.vi", 3, "Magnetite (Fe3O4) contains iron in which oxidation state(s)?", "both +2 and +3 (one Fe2+ and two Fe3+)", ["only +2", "only +3", "+4"],
  sp=["magnetite"])
M("3h.vi", 3, "In pyrite (FeS2), iron is +2. What is the charge on the S2 unit?", "-2 (a disulfide ion)", ["-4", "-1", "0"], sp=["pyrite"])
M("3h.vi", 3, "In chalcopyrite (CuFeS2), copper is usually assigned +1. What charge does that leave for iron?", "+3", ["+2", "+1", "+4"],
  sp=["chalcopyrite"])
M("3h.vi", 2, "The blue of azurite and the green of malachite both come from:", "Cu2+", ["Fe3+", "Cr3+", "Mn2+"], sp=["azurite", "malachite"])
M("3h.vi", 2, "When azurite weathers to malachite, what is gained and what is lost?", "water is gained and carbon dioxide is lost",
  ["CO2 is gained and water lost", "oxygen is lost", "copper is lost"], sp=["azurite", "malachite"])
M("3h.vi", 2, "Minerals whose color comes from an essential element are called:", "idiochromatic", ["allochromatic", "pseudochromatic", "achromatic"])
M("3h.vi", 2, "Minerals colored by trace impurities are called:", "allochromatic", ["idiochromatic", "pleochroic", "metamict"])
M("3h.vi", 2, "Color caused by structural defects such as missing electrons (e.g., smoky quartz) arises from:", "color centers",
  ["charge-transfer bands", "play-of-color", "exsolution"], sp=["smoky-quartz", "amethyst"])
M("3h.vi", 2, "Ions can substitute for each other in a crystal most easily when they have:", "similar size and charge",
  ["the same atomic mass", "opposite charges", "the same color"])
M("3h.vi", 2, "Water written as '·nH2O' at the end of a formula (e.g., gypsum CaSO4·2H2O) indicates:", "water of hydration bound in the structure",
  ["dissolved water impurity", "an acid", "hydroxyl ions"], sp=["selenite"])
M("3h.vi", 2, "Heating gypsum drives off water to make:", "plaster of Paris (bassanite, CaSO4·0.5H2O)", ["quicklime", "cement clinker", "anhydrous halite"],
  sp=["selenite", "alabaster"])
M("3h.vi", 2, "What gives Mohs hardness its link to chemistry?", "stronger and denser bonding produces harder minerals", ["heavier elements always make minerals harder",
  "color", "number of cleavage planes only"])
M("3h.vi", 3, "Why are many native metals soft and malleable?", "metallic bonds let layers of atoms slide without breaking", ["they contain water",
  "they have ionic bonds", "they are amorphous"])
M("3h.vi", 3, "Why does graphite cleave easily into sheets while diamond does not?", "graphite has weak van der Waals bonds between strongly bonded carbon sheets",
  ["graphite contains impurities", "diamond is amorphous", "graphite is ionic"], sp=["graphite", "diamond"])
M("3h.vi", 3, "Why is ice less dense than liquid water, a property shared by few solids?", "hydrogen bonds hold molecules in an open hexagonal framework",
  ["ice contains air", "ice is amorphous", "ice is metallic"])
M("3h.vi", 2, "Which property of galena makes it heavy?", "it contains lead, a heavy element", ["it has many cleavages", "it is cubic", "it is metallic"],
  sp=["galena"])

# --- polymorphs
M("3h.vii", 1, "Polymorphs are minerals with:", "the same composition but different crystal structures", ["different compositions but the same structure",
  "the same color", "the same hardness"])
M("3h.vii", 2, "Which CaCO3 polymorph is stable at Earth's surface?", "calcite", ["aragonite", "vaterite", "dolomite"], sp=["calcite", "aragonite"])
M("3h.vii", 2, "Aragonite is denser than calcite. This fits with aragonite being the:", "high-pressure polymorph",
  ["high-temperature polymorph", "low-pressure polymorph", "hydrated form"], sp=["aragonite"])
F("3h.vii", 3, "Aragonite is metastable at Earth's surface. Why do aragonite shells and cave deposits still form and persist?",
  "Organisms and certain water chemistries (e.g., Mg-rich water, which inhibits calcite) favor aragonite growth kinetically; the conversion to calcite is very slow at low temperature, so it persists for long periods.",
  ["biological/kinetic control", "Mg inhibits calcite", "slow conversion at low T"], sp=["aragonite"])
M("3h.vii", 2, "Diamond survives at Earth's surface although graphite is the stable form because:", "the conversion is extremely slow at low temperature",
  ["diamond is stable at the surface", "diamond is coated by graphite", "the conversion requires pressure"], sp=["diamond"])
M("3h.vii", 2, "Which KAlSi3O8 polymorph forms at the highest temperature (e.g., in rhyolite)?", "sanidine", ["orthoclase", "microcline", "albite"],
  sp=["orthoclase-microcline"])
M("3h.vii", 2, "The quartz that forms above 573 °C (at 1 atm) and inverts on cooling is called:", "beta (high) quartz", ["alpha (low) quartz", "tridymite", "coesite"])
M("3h.vii", 3, "Which SiO2 polymorph forms at very high pressures, such as in meteorite impacts?", "coesite (and stishovite)",
  ["tridymite", "cristobalite", "opal"])
M("3h.vii", 2, "Andalusite, kyanite and sillimanite all have the formula:", "Al2SiO5", ["Al2O3", "KAlSi3O8", "Al2Si2O5(OH)4"], sp=["kyanite"])

# --- groups and families
M("3h.viii.1", 2, "Garnets are divided into the pyralspite and ugrandite series. Almandine belongs to:", "pyralspite (Al-rich)",
  ["ugrandite (Ca-rich)", "neither", "both"], sp=["almandine"])
M("3h.viii.1", 2, "Grossular belongs to which garnet series?", "ugrandite (Ca garnets: uvarovite, grossular, andradite)",
  ["pyralspite", "spinel", "epidote"], sp=["grossular"])
M("3h.viii.1", 2, "Feldspathoids such as sodalite form instead of feldspars when a magma is:", "poor in silica (silica-undersaturated)",
  ["rich in silica", "rich in water", "very cold"], sp=["sodalite"])
F("3h.viii.1", 3, "Explain why quartz and feldspathoids (like sodalite or nepheline) are not found together in the same igneous rock.",
  "Feldspathoids form only in silica-poor magmas. If quartz (free silica) were present, it would react with the feldspathoid to make feldspar, so the two are chemically incompatible.",
  ["feldspathoid + silica -> feldspar", "silica-undersaturated magma"], sp=["sodalite"])
M("3h.viii.1", 2, "Micas, talc and kaolinite all share which property due to their structure?", "perfect cleavage in one direction (sheets)",
  ["conchoidal fracture", "cubic cleavage", "high hardness"])
M("3h.viii.1", 2, "Which pair are both amphiboles?", "tremolite and hornblende", ["augite and hornblende", "biotite and actinolite", "olivine and tremolite"])
M("3h.viii.1", 2, "Which pair are both pyroxenes?", "augite and spodumene", ["augite and hornblende", "spodumene and lepidolite", "olivine and augite"])
M("3h.viii.1", 2, "Zeolites such as stilbite have open frameworks with channels that:", "hold water and exchangeable cations", ["hold oil",
  "contain sulfur", "make them magnetic"], sp=["stilbite"])
M("3h.viii.1", 2, "The apatite group includes fluorapatite, pyromorphite and vanadinite. What do they share?", "the same hexagonal crystal structure (A5(XO4)3Z)",
  ["the same color", "the same cation", "no common features"], sp=["fluorapatite", "pyromorphite", "vanadinite"])
M("3h.viii.1", 2, "Which of these is a phyllosilicate but NOT a mica?", "talc", ["muscovite", "biotite", "lepidolite"])
M("3h.viii.1", 2, "Clay minerals like kaolinite belong to which silicate class?", "phyllosilicates", ["tectosilicates", "nesosilicates", "inosilicates"],
  sp=["kaolinite"])
M("3h.viii.1", 1, "Under the Dana system, which class would contain native copper?", "native elements", ["oxides", "sulfides", "halides"], sp=["copper"])
M("3h.viii.1", 2, "Tourmaline is technically both a silicate and a:", "borate-bearing mineral (it contains BO3 groups)", ["carbonate", "sulfide", "halide"],
  sp=["tourmaline"])
M("3h.viii.1", 2, "Vanadinite is a vanadate, but it is grouped with phosphates because:", "VO4 groups occupy the same structural sites as PO4",
  ["it contains phosphorus", "it is green", "it is a sulfide"], sp=["vanadinite"])

# --- silicate structure reasoning
M("3h.viii.2", 2, "Why do framework silicates like quartz tend to be hard and lack cleavage?", "strong Si-O bonds extend in all three directions",
  ["they contain water", "they are amorphous", "their bonds are weak in one plane"])
M("3h.viii.2", 2, "Why do sheet silicates cleave in one direction?", "bonds between the sheets are much weaker than bonds within them",
  ["they are hexagonal", "they contain iron", "they are ductile"])
M("3h.viii.2", 2, "Why do chain silicates (pyroxenes, amphiboles) have two cleavage directions?", "breaks occur between the chains, parallel to their length",
  ["they are cubic", "they are sheet-like", "they have no bonds between chains"])
M("3h.viii.2", 2, "In which silicate group do tetrahedra share all four oxygens?", "tectosilicates", ["phyllosilicates", "nesosilicates", "inosilicates"])
M("3h.viii.2", 2, "In which silicate group do tetrahedra share no oxygens?", "nesosilicates", ["sorosilicates", "cyclosilicates", "tectosilicates"])
M("3h.viii.2", 2, "Which silicate structure consists of pairs of tetrahedra sharing one oxygen?", "sorosilicate", ["nesosilicate", "cyclosilicate", "phyllosilicate"])
M("3h.viii.2", 2, "Beryl's six-membered rings stack to form channels. This makes beryl a:", "cyclosilicate", ["inosilicate", "tectosilicate", "nesosilicate"],
  sp=["beryl"])
M("3h.viii.2", 3, "Why can aluminum substitute for silicon in many silicate tetrahedra?", "Al3+ is small enough to fit in tetrahedral sites; charge is balanced by extra cations",
  ["Al and Si have the same charge", "Al is larger than Si", "Al only goes in octahedral sites"])
M("3h.viii.2", 2, "As silicates become more polymerized (more shared oxygens), the Si:O ratio:", "increases toward 1:2", ["decreases toward 1:4",
  "stays 1:4", "becomes 1:1"])

# --- crystal systems & physical properties
M("3h.viii.3", 2, "Halite and galena cleave into cubes because:", "their cubic structures have planes of weakness parallel to cube faces",
  ["they are metallic", "they are soft", "they are hexagonal"], sp=["halite", "galena"])
M("3h.viii.3", 2, "How many crystal systems are recognized in Science Olympiad (counting trigonal separately)?", "7", ["5", "6", "32"])
M("3h.viii.3", 2, "Which of these minerals is NOT cubic?", "quartz", ["garnet", "pyrite", "fluorite"])
M("3h.viii.3", 2, "A mineral with six-sided prisms could belong to which systems?", "hexagonal or trigonal", ["cubic or tetragonal", "monoclinic only", "triclinic only"])
M("3h.viii.3", 3, "Which crystal system has the lowest symmetry?", "triclinic", ["monoclinic", "orthorhombic", "cubic"])
M("3h.viii.3", 3, "Which crystal system has the highest symmetry?", "cubic", ["hexagonal", "tetragonal", "orthorhombic"])
M("3h.viii.3", 2, "Cubic, octahedral and dodecahedral crystals all belong to which system?", "cubic (isometric)", ["tetragonal", "trigonal", "orthorhombic"])
M("3h.viii.3", 2, "An 'interfacial angle' is constant for a mineral because:", "it reflects the regular internal arrangement of atoms (Steno's law of constant angles)",
  ["all crystals are cubic", "crystals grow at the same speed", "it depends on crystal size"])

# --- formation environments
M("3h.ix", 1, "Minerals that precipitate as water evaporates from salty lakes or seas are called:", "evaporites", ["placers", "pegmatites", "skarns"])
M("3h.ix", 2, "As seawater evaporates, which mineral precipitates first?", "calcite (carbonates)", ["halite", "gypsum", "sylvite"],
  "Order: carbonates -> gypsum/anhydrite -> halite -> K-Mg salts.")
add("order", "3h.ix", "Order these evaporite minerals by when they precipitate from evaporating seawater (first to last): gypsum, halite, calcite.",
    ["calcite", "gypsum", "halite"], specimens=["calcite", "selenite", "halite"], tags=["evaporite"], diff=2, source="authored",
    explanation="Least soluble precipitates first.")
M("3h.ix", 2, "Hot, mineral-rich water that deposits minerals in fractures produces:", "hydrothermal veins", ["evaporites", "placers", "laterites"])
M("3h.ix", 2, "Heavy, weathering-resistant minerals concentrated by flowing water form:", "placer deposits", ["skarns", "hydrothermal veins", "evaporites"],
  sp=["gold", "zircon", "rutile"])
M("3h.ix", 2, "Which minerals are commonly found in placer deposits?", "gold, zircon, rutile and magnetite", ["halite, gypsum and sylvite",
  "calcite and dolomite", "muscovite and talc"])
M("3h.ix", 2, "Metamorphic rock formed where magma contacts limestone, rich in garnet and wollastonite, is a:", "skarn", ["hornfels", "pegmatite", "laterite"],
  sp=["grossular", "wollastonite"])
M("3h.ix", 2, "The zone where descending groundwater oxidizes sulfide ore, forming minerals like malachite and azurite, is the:", "oxidized (supergene) zone",
  ["primary (hypogene) zone", "contact aureole", "mantle wedge"], sp=["malachite", "azurite"])
M("3h.ix", 3, "Below the oxidized zone of a copper deposit, copper carried down by groundwater is redeposited in the:", "supergene enrichment zone",
  ["gossan", "leached cap", "contact aureole"])
M("3h.ix", 2, "A rusty, iron-oxide-stained cap of weathered rock above a sulfide deposit is a:", "gossan", ["skarn", "kimberlite", "evaporite"],
  sp=["goethite-limonite"])
M("3h.ix", 2, "Diamonds reach the surface through:", "kimberlite pipes", ["basalt dikes", "rhyolite flows", "hot springs"], sp=["diamond"])
M("3h.ix", 2, "Native sulfur often forms:", "around volcanic fumaroles and in salt-dome caprocks", ["in pegmatites", "in banded iron formations", "in placers"],
  sp=["sulfur"])
M("3h.ix", 2, "Mississippi Valley-type deposits host which minerals in limestone and dolostone?", "galena, sphalerite, fluorite and barite",
  ["gold and quartz", "olivine and pyroxene", "halite and gypsum"], sp=["galena", "sphalerite"])
M("3h.ix", 2, "Laterite and bauxite form by:", "intense chemical weathering in hot, wet climates", ["evaporation", "contact metamorphism", "volcanic eruption"],
  sp=["bauxite"])
M("3h.ix", 2, "Most large crystals of beryl, tourmaline and spodumene form in:", "pegmatites", ["basalt flows", "shale", "evaporites"])
M("3h.ix", 2, "Zeolites, apophyllite and prehnite commonly form in:", "gas cavities in basalt", ["salt domes", "coal seams", "kimberlite"])
M("3h.ix", 2, "Chemical weathering of feldspar by water and carbonic acid produces:", "clay minerals such as kaolinite", ["quartz", "olivine", "calcite"],
  sp=["kaolinite"])
M("3h.ix", 2, "The cave formations stalactites and stalagmites are mostly made of:", "calcite", ["halite", "gypsum", "quartz"], sp=["calcite", "travertine"])
F("3h.ix", 3, "Explain how stalactites form in limestone caves.",
  "Rainwater absorbs CO2, forming carbonic acid that dissolves limestone. When this water drips into an air-filled cave, CO2 degasses, lowering calcite solubility so calcite precipitates, building icicle-shaped stalactites.",
  ["carbonic acid dissolves calcite", "CO2 degassing in the cave", "calcite precipitates"], sp=["calcite", "travertine"])
M("3h.x", 2, "Which mineral is most typical of oceanic crust?", "calcium-rich plagioclase", ["potassium feldspar", "muscovite", "quartz"])
M("3h.x", 2, "Which minerals dominate continental crust?", "quartz and feldspars", ["olivine and pyroxene", "halite and gypsum", "garnet and kyanite"])
M("3h.x", 2, "Which mineral dominates Earth's upper mantle?", "olivine", ["quartz", "feldspar", "calcite"], sp=["olivine"])
M("3h.x", 2, "Chlorite, epidote and actinolite together indicate:", "low-grade (greenschist) metamorphism", ["evaporite deposition", "mantle conditions",
  "a pegmatite"], sp=["epidote", "actinolite"])
M("3h.x", 2, "Glaucophane (a blue amphibole) is the key mineral of which facies?", "blueschist", ["greenschist", "granulite", "hornfels"])
M("3h.x", 2, "Omphacite (a green pyroxene) and garnet together make up:", "eclogite", ["amphibolite", "gneiss", "slate"])
M("3h.x", 2, "Which mineral is the most common cement in sandstones besides quartz?", "calcite", ["halite", "olivine", "graphite"])

# --- uses
M("3h.xii.1", 2, "Which mineral is the main aluminum-bearing mineral in bauxite?", "gibbsite", ["corundum", "kyanite", "muscovite"], sp=["bauxite"])
M("3h.xii.1", 2, "Which mineral was used as 'isinglass' windows in stoves?", "muscovite", ["selenite", "calcite", "quartz"], sp=["muscovite"])
M("3h.xii.1", 2, "Which mineral is used to make drywall?", "gypsum", ["talc", "halite", "barite"], sp=["selenite", "alabaster"])
M("3h.xii.1", 2, "Which mineral is used as a weighting agent in oil-well drilling mud?", "barite", ["celestite", "galena", "fluorite"], sp=["barite"])
M("3h.xii.1", 2, "Which mineral gives fireworks a bright red color?", "celestite (strontium)", ["barite (barium)", "halite (sodium)", "malachite (copper)"],
  sp=["celestite"])
M("3h.xii.1", 2, "Barium compounds (from barite) give fireworks which color?", "green", ["red", "yellow", "blue"], sp=["barite"])
M("3h.xii.1", 2, "Copper compounds give fireworks which color?", "blue to green", ["red", "yellow", "white"])
M("3h.xii.1", 2, "Sodium compounds give fireworks which color?", "yellow-orange", ["red", "green", "violet"], sp=["halite"])
M("3h.xii.1", 2, "Which mineral is the main source of lithium in hard-rock mining?", "spodumene", ["lepidolite", "halite", "beryl"], sp=["spodumene"])
M("3h.xii.1", 2, "Which mineral is used as a flux in steelmaking and to make hydrofluoric acid?", "fluorite", ["calcite", "barite", "talc"], sp=["fluorite"])
M("3h.xii.1", 2, "Which mineral is used to make porcelain and coat glossy paper?", "kaolinite", ["talc", "gypsum", "muscovite"], sp=["kaolinite"])
M("3h.xii.1", 2, "Which mineral is ground into baby powder?", "talc", ["kaolinite", "gypsum", "calcite"], sp=["talc"])
M("3h.xii.1", 2, "Which mineral provides most of the world's titanium dioxide pigment (with ilmenite)?", "rutile", ["zircon", "corundum", "hematite"],
  sp=["rutile"])
M("3h.xii.1", 2, "Which mineral is used in spark-plug insulators and other refractories?", "kyanite", ["talc", "halite", "graphite"], sp=["kyanite"])
M("3h.xii.1", 2, "Which mineral is used for lubricants and battery anodes?", "graphite", ["talc", "molybdenite", "galena"], sp=["graphite"])
M("3h.xii.1", 2, "Which mineral is used in radiation shielding and lead-acid batteries via its metal?", "galena", ["sphalerite", "barite", "stibnite"],
  sp=["galena"])
M("3h.xii.1", 2, "Which mineral is the main ore of zinc, used for galvanizing steel?", "sphalerite", ["zincite", "willemite", "galena"], sp=["sphalerite"])
M("3h.xii.1", 2, "Which mineral is the main ore of antimony, used in flame retardants?", "stibnite", ["galena", "bornite", "rutile"], sp=["stibnite"])
M("3h.xii.1", 2, "Which mineral is the main ore of manganese?", "pyrolusite", ["rhodonite", "magnetite", "hematite"], sp=["pyrolusite"])
M("3h.xii.1", 2, "Which mineral is used for U-Pb geochronology?", "zircon", ["calcite", "halite", "olivine"], sp=["zircon"])
M("3h.xii.1", 2, "Which mineral is used in phosphate fertilizers?", "fluorapatite", ["fluorite", "gypsum", "halite"], sp=["fluorapatite"])
M("3h.xii.1", 2, "Which mineral was used for the first commercial fluorescent-lamp phosphors?", "willemite", ["fluorite", "calcite", "scheelite"],
  sp=["willemite"])
M("3h.xii.1", 2, "Which mineral is the major ore of beryllium?", "beryl", ["chrysoberyl", "topaz", "spodumene"], sp=["beryl"])
M("3h.xii.1", 2, "Garnet's main industrial use is as:", "an abrasive (sandpaper, waterjet cutting)", ["a fertilizer", "a pigment", "a lubricant"],
  sp=["almandine"])
M("3h.xii.1", 2, "Why is corundum (emery) a good abrasive?", "it is very hard (9)", ["it is soft and slippery", "it is magnetic", "it dissolves in water"],
  sp=["corundum"])
M("3h.xii.1", 2, "Which mineral was historically used as a pigment called 'red ochre'?", "hematite", ["malachite", "azurite", "pyrolusite"], sp=["hematite"])
M("3h.xii.1", 2, "Which mineral was ground for a blue pigment in medieval paintings, besides lapis lazuli?", "azurite", ["malachite", "sodalite", "turquoise"],
  sp=["azurite"])
M("3h.xii.1", 2, "What is acid mine drainage, and which mineral causes it?", "acidic runoff from oxidation of pyrite", ["alkaline runoff from calcite",
  "salty runoff from halite", "radioactive runoff from zircon"], sp=["pyrite"])
M("3h.xii.1", 2, "Which mineral's dust is used in toothpaste as a source of fluoride (historically)?", "fluorite (via fluoride compounds)",
  ["halite", "talc", "barite"], sp=["fluorite"])
M("3h.xii.1", 2, "Most of the world's iron comes from which rock type?", "banded iron formation", ["basalt", "granite", "limestone"],
  sp=["banded-iron-formation", "hematite", "magnetite"])
F("3h.xii.1", 2, "Why is native copper relatively rare compared with copper ore minerals such as chalcopyrite?",
  "Copper is reactive: in most environments it combines with sulfur (in reducing settings) or oxygen and carbonate (in oxidizing settings), so it rarely stays as the uncombined element.",
  ["copper reacts with sulfur/oxygen", "native elements need special conditions"], sp=["copper"])
M("3h.xii.2", 2, "What gives emerald its green color?", "chromium or vanadium", ["iron", "copper", "nickel"], sp=["beryl"])
M("3h.xii.2", 2, "Most commercial blue topaz is produced by:", "irradiating and heating colorless topaz", ["dyeing", "adding copper", "polishing"],
  sp=["topaz"])
M("3h.xii.2", 2, "Most commercial citrine is produced by:", "heating amethyst", ["irradiating rose quartz", "dyeing milky quartz", "heating smoky quartz to 1000 °C"],
  sp=["citrine", "amethyst"])
M("3h.xii.2", 2, "Watermelon tourmaline has a pink core and green rim because:", "the composition of the fluid changed as the crystal grew",
  ["it was dyed", "it is two different minerals", "it was heated"], sp=["tourmaline"])
M("3h.xii.2", 2, "Which gem is organic, made of fossilized tree resin?", "amber", ["jet", "pearl", "coral"])
M("3h.xii.2", 2, "Pearls form when a mollusk:", "coats an irritant with layers of nacre (aragonite)", ["swallows sand", "crystallizes calcite from seawater",
  "fossilizes"], sp=["aragonite"])
M("3h.xii.2", 2, "Which gem is the national gem of Scotland ('cairngorm')?", "smoky quartz", ["amethyst", "citrine", "rose quartz"], sp=["smoky-quartz"])
M("3h.xii.2", 2, "Tanzanite, a December birthstone, is a variety of which mineral (not on the list)?", "zoisite", ["beryl", "corundum", "spodumene"])
M("3h.xii.2", 2, "Which variety of corundum is red?", "ruby", ["sapphire", "padparadscha", "emerald"], sp=["corundum"])
M("3h.xii.2", 2, "Padparadscha is a pink-orange variety of:", "corundum (sapphire)", ["spodumene", "topaz", "beryl"], sp=["corundum"])

# =====================================================================  ROCKS
M("3i.i", 1, "Which best describes a rock?", "a naturally occurring solid aggregate of one or more minerals, mineraloids or organic matter",
  ["a single crystal with a definite formula", "any solid made in a factory", "a liquid that hardens"])
T("3i.i", 1, "A rock can be made of a single mineral.", True, "Monomineralic rocks include marble (calcite), quartzite (quartz) and rock salt (halite).")
T("3i.i", 1, "Unlike minerals, rocks can contain organic matter.", True, "Coal is made largely of plant-derived organic material.", ["bituminous"])
M("3i.i", 2, "Which of these is a monomineralic rock?", "quartzite", ["granite", "gneiss", "conglomerate"], sp=["quartzite"])
M("3i.i", 2, "Which of these is a polymineralic rock?", "granite", ["marble", "rock salt", "quartzite"], sp=["granite"])
M("3i.i", 2, "Which rock is made mostly of non-crystalline glass?", "obsidian", ["granite", "marble", "slate"], sp=["obsidian"])
M("3i.iii", 1, "Rocks are classified into igneous, sedimentary and metamorphic based on:", "how they formed", ["their color", "their age", "where they are found today"])
M("3i.iii", 2, "Which feature most strongly suggests a rock is sedimentary?", "rounded grains, fossils or layering", ["interlocking crystals and vesicles",
  "foliation", "glassy texture"])
M("3i.iii", 2, "Which feature most strongly suggests a rock is metamorphic?", "foliation or banding", ["vesicles", "fossils", "rounded pebbles"])
M("3i.iii", 2, "Which feature most strongly suggests a rock is igneous?", "interlocking crystals, glass or vesicles", ["fossils", "cross-bedding", "slaty cleavage"])

# --- igneous
M("3i.iv.1", 1, "Aphanitic texture means:", "crystals too small to see without magnification", ["visible crystals", "no crystals (glass)", "very large crystals"])
M("3i.iv.1", 1, "Phaneritic texture means:", "crystals large enough to see with the naked eye", ["microscopic crystals", "glassy", "full of holes"])
M("3i.iv.1", 1, "Large crystals set in a finer-grained groundmass describe a:", "porphyritic texture", ["vesicular texture", "glassy texture", "pegmatitic texture"])
M("3i.iv.1", 2, "The large crystals in a porphyritic rock are called:", "phenocrysts", ["porphyroblasts", "xenoliths", "clasts"])
M("3i.iv.1", 2, "Large crystals that grew within a metamorphic rock (e.g., garnet in schist) are called:", "porphyroblasts", ["phenocrysts", "xenocrysts", "ooids"],
  sp=["garnet-schist"])
M("3i.iv.1", 2, "A fragment of foreign rock enclosed in an igneous rock is a:", "xenolith", ["phenocryst", "amygdule", "porphyroblast"])
M("3i.iv.1", 1, "Rocks full of gas holes have a texture called:", "vesicular", ["porphyritic", "aphanitic", "foliated"])
M("3i.iv.1", 2, "Ash under 2 mm, lapilli 2-64 mm, and blocks/bombs over 64 mm are all:", "pyroclasts (tephra)", ["phenocrysts", "clasts of sedimentary rock", "xenoliths"])
M("3i.iv.1", 2, "Volcanic bombs differ from blocks in that bombs:", "were ejected molten and became rounded or streamlined in flight",
  ["are always larger", "are made of glass only", "are sedimentary"])
M("3i.iv.1", 2, "Pumice floats but scoria sinks because:", "pumice has thin-walled, abundant vesicles and lower-density felsic glass",
  ["scoria contains more gas", "pumice is crystalline", "scoria is felsic"], sp=["pumice", "scoria"])
F("3i.iv.1", 2, "Describe the difference between pumice and scoria in composition and appearance.",
  "Pumice is felsic (silica-rich), light-colored, frothy glass with tiny thin-walled vesicles and floats; scoria is mafic (basaltic), dark red to black, with larger, thicker-walled vesicles, and sinks.",
  ["pumice felsic, scoria mafic", "pumice light/floats", "scoria dark/sinks"], sp=["pumice", "scoria"])
M("3i.iv.2", 1, "Felsic rocks are rich in:", "silica, feldspar and quartz", ["iron and magnesium", "olivine", "calcium carbonate"])
M("3i.iv.2", 1, "Mafic rocks are rich in:", "magnesium and iron", ["potassium and sodium", "quartz", "carbonate"])
M("3i.iv.2", 1, "Compared with felsic rocks, mafic rocks are generally:", "darker and denser", ["lighter and less dense", "always glassy", "richer in quartz"])
M("3i.iv.2", 2, "Approximately what silica content separates felsic from intermediate igneous rocks?", "about 63-65% SiO2", ["about 25%", "about 45%", "about 90%"])
M("3i.iv.2", 2, "Ultramafic rocks contain less than about how much silica?", "45% SiO2", ["63%", "52%", "70%"], sp=["peridotite"])
M("3i.iv.2", 2, "The color index of an igneous rock is:", "the percentage of dark (mafic) minerals", ["its silica percentage", "its grain size", "its density"])
M("3i.iv.2", 2, "Why is obsidian dark even though it is felsic?", "tiny amounts of iron-titanium oxides color the glass", ["it is mafic",
  "it contains carbon", "it is coated by soot"], sp=["obsidian"])
M("3i.iv.2", 2, "QAPF diagrams classify plutonic rocks by proportions of:", "quartz, alkali feldspar, plagioclase and feldspathoids",
  ["quartz, apatite, pyroxene, fluorite", "olivine, pyroxene, amphibole", "clay, silt, sand"])
M("3i.iv.2", 3, "On a QAPF diagram, a rock with no quartz and mostly alkali feldspar plots as:", "syenite", ["granite", "diorite", "gabbro"], sp=["syenite"])
M("3i.iv.2", 2, "Which igneous rock has the highest density?", "peridotite", ["granite", "rhyolite", "pumice"], sp=["peridotite"])
M("3i.iv.2", 2, "Komatiite is a rare ultramafic lava, mostly from the Archean, because:", "the early mantle was hotter, allowing very high-temperature melts",
  ["oxygen was absent", "there was no crust", "it only forms on the Moon"])
M("3i.iv.3", 1, "Rocks that cool from magma underground are called:", "intrusive (plutonic)", ["extrusive", "pyroclastic", "volcanic"])
M("3i.iv.3", 1, "Rocks that cool from lava at the surface are called:", "extrusive (volcanic)", ["intrusive", "plutonic", "hypabyssal"])
M("3i.iv.3", 2, "A large intrusive body with over 100 km² of surface exposure is a:", "batholith", ["stock", "dike", "sill"])
M("3i.iv.3", 2, "A sheet-like intrusion that cuts across rock layers is a:", "dike", ["sill", "laccolith", "batholith"])
M("3i.iv.3", 2, "A sheet-like intrusion that runs parallel to rock layers is a:", "sill", ["dike", "stock", "volcanic neck"])
M("3i.iv.3", 2, "A mushroom-shaped intrusion that domes up overlying layers is a:", "laccolith", ["lopolith", "dike", "batholith"])
M("3i.iv.3", 2, "A saucer-shaped intrusion that sags downward, often mafic and layered, is a:", "lopolith", ["laccolith", "sill", "stock"])
M("3i.iv.3", 2, "A small intrusion like a batholith but under 100 km² in exposure is a:", "stock", ["dike", "sill", "pipe"])
M("3i.iv.3", 2, "The solidified magma in the conduit of an extinct volcano, exposed by erosion (e.g., Shiprock), is a:", "volcanic neck",
  ["batholith", "laccolith", "caldera"])
M("3i.iv.3", 2, "A lava flow with a smooth, ropy surface is called:", "pahoehoe", ["aa", "pillow lava", "ignimbrite"], sp=["basalt"])
M("3i.iv.3", 2, "A lava flow with a rough, jagged, clinkery surface is called:", "aa", ["pahoehoe", "pillow lava", "tuff"], sp=["basalt"])
M("3i.iv.3", 2, "Pillow lavas form when:", "lava erupts underwater and quickly chills", ["ash falls into lakes", "lava cools slowly underground", "lava flows on ice only"],
  sp=["basalt"])
M("3i.iv.3", 2, "Columnar jointing in basalt forms because:", "the lava contracts as it cools, cracking into polygonal columns", ["of wind erosion",
  "of crystal growth", "of earthquakes"], sp=["basalt"])
M("3i.iv.3", 2, "A pyroclastic flow is:", "a fast, ground-hugging avalanche of hot gas, ash and rock", ["a slow lava flow", "a mudflow only", "a gas cloud above a volcano"],
  sp=["tuff"])
M("3i.iv.3", 2, "A volcanic mudflow is called a:", "lahar", ["nuée ardente", "tephra", "caldera"])
M("3i.iv.3", 2, "Welded tuff deposited by a hot pyroclastic flow is also called:", "ignimbrite", ["scoria", "breccia", "andesite"], sp=["tuff"])
M("3i.iv.3", 2, "Which volcano type is built mostly of fluid basalt flows?", "shield volcano", ["stratovolcano", "cinder cone", "lava dome"], sp=["basalt"])
M("3i.iv.3", 2, "Which volcano type has alternating lava and pyroclastic layers and is typical of subduction zones?", "stratovolcano (composite)",
  ["shield volcano", "cinder cone", "fissure"], sp=["andesite"])
M("3i.iv.3", 2, "Which volcano type is a small, steep cone of loose scoria?", "cinder cone", ["shield volcano", "stratovolcano", "caldera"], sp=["scoria"])
M("3i.iv.3", 2, "A large basin formed by collapse after a magma chamber empties is a:", "caldera", ["crater", "maar", "graben"])
M("3i.iv.4", 2, "Why do intrusive rocks have larger crystals than extrusive rocks?", "they cool slowly, giving atoms time to form large crystals",
  ["they contain more water", "they are older", "they are under less pressure"])
M("3i.iv.4", 2, "A porphyritic andesite with large plagioclase phenocrysts most likely experienced:", "slow cooling at depth followed by eruption and rapid cooling",
  ["only rapid cooling", "only slow cooling", "metamorphism"], sp=["andesite"])
M("3i.iv.4", 2, "Glassy rocks indicate:", "cooling so fast crystals could not form", ["slow cooling", "metamorphism", "sedimentation"])
M("3i.iv.4", 2, "A basalt dike's edges are finer-grained than its center because:", "the edges chilled quickly against cold country rock",
  ["the center is older", "the edges were metamorphosed", "the center contains more water"])
M("3i.iv.4", 3, "Why can water-rich magma form very coarse pegmatites?", "water lowers viscosity and improves ion diffusion, allowing crystals to grow large",
  ["water cools the magma quickly", "water forms glass", "water adds iron"], sp=["pegmatite"])
M("3i.iv.5", 2, "Which rock is most typical of mid-ocean ridges?", "basalt", ["granite", "andesite", "rhyolite"], sp=["basalt"])
M("3i.iv.5", 2, "Which rocks are most typical of ocean-continent subduction zones?", "andesite and diorite", ["basalt and gabbro only", "peridotite", "rock salt"],
  sp=["andesite", "diorite"])
M("3i.iv.5", 2, "Granite batholiths form mostly at:", "convergent boundaries in continental crust", ["mid-ocean ridges", "transform faults", "abyssal plains"],
  sp=["granite"])
M("3i.iv.5", 2, "Hawaiian volcanoes are made mostly of basalt because they form over:", "a mantle hotspot under oceanic crust", ["a subduction zone",
  "a continental collision", "a transform fault"], sp=["basalt"])
M("3i.iv.5", 2, "Yellowstone's eruptions produce rhyolite because:", "the hotspot melts silica-rich continental crust", ["it is a mid-ocean ridge",
  "it lies on oceanic crust", "it is a subduction zone"], sp=["rhyolite"])
M("3i.iv.5", 2, "At subduction zones, mantle melting is triggered mainly by:", "water released from the subducting slab (flux melting)",
  ["decompression only", "friction", "radioactive heating"])
M("3i.iv.5", 2, "At mid-ocean ridges, mantle melting is caused mainly by:", "decompression as mantle rises", ["addition of water", "friction", "meteorite impacts"])
M("3i.iv.5", 2, "The Ring of Fire is a belt of volcanoes and earthquakes associated with:", "subduction zones around the Pacific", ["mid-ocean ridges",
  "hotspots", "continental rifts"])
M("3i.iv.5", 2, "A sequence of oceanic crust and upper mantle thrust onto land (pillow basalt, sheeted dikes, gabbro, peridotite) is an:", "ophiolite",
  ["obduction", "orogen", "isograd"], sp=["peridotite", "gabbro", "basalt"])
add("order", "3i.iv.5", "In an ophiolite, order these layers from top to bottom: gabbro, peridotite, pillow basalt, sheeted dikes.",
    ["pillow basalt", "sheeted dikes", "gabbro", "peridotite"], specimens=["basalt", "gabbro", "peridotite"], tags=["ophiolite"], diff=2, source="authored")
M("3i.iv.5", 2, "Flood basalts like the Deccan Traps and Columbia River Basalts are associated with:", "mantle plumes (large igneous provinces)",
  ["subduction", "continental collision", "transform faults"], sp=["basalt"])
M("3i.iv.6", 2, "Magmatic differentiation by removal of early-formed crystals from a melt is called:", "fractional crystallization",
  ["assimilation", "magma mixing", "partial melting"])
M("3i.iv.6", 2, "When rising magma melts and incorporates surrounding country rock, the process is:", "assimilation", ["fractional crystallization", "magma mixing",
  "exsolution"])
M("3i.iv.6", 2, "When two magmas of different compositions combine, the process is:", "magma mixing", ["assimilation", "fractional crystallization", "stoping"])
M("3i.iv.6", 2, "Fractional crystallization of a basaltic magma drives the remaining melt toward:", "higher silica (more felsic) compositions",
  ["higher magnesium", "lower silica", "pure olivine"])
M("3i.iv.6", 2, "Assimilation of continental crust generally makes a magma:", "more felsic", ["more mafic", "ultramafic", "unchanged"])
M("3i.iv.6", 2, "Layers of olivine and pyroxene at the bottom of the Palisades Sill or Stillwater Complex formed by:", "crystal settling during fractional crystallization",
  ["sedimentation", "metamorphism", "magma mixing"], sp=["gabbro", "olivine"])
M("3i.iv.6", 2, "Which evidence in a rock suggests magma mixing?", "phenocrysts that are out of equilibrium, e.g. resorbed or reverse-zoned crystals",
  ["fossils", "rounded pebbles", "slaty cleavage"])
M("3i.iv.6", 2, "Melting only part of a rock, producing a melt richer in silica than the source, is:", "partial melting", ["total melting", "assimilation", "lithification"])
F("3i.iv.6", 3, "How do layered intrusions such as the Bushveld or Skaergaard provide evidence for fractional crystallization?",
  "Dense early-formed crystals (olivine, pyroxene, chromite) settled to the floor of the magma chamber, forming layers that change upward to later, more evolved minerals - recording the progressive removal of crystals and changing melt composition.",
  ["crystal settling", "layers change upward", "melt evolves"], sp=["gabbro", "peridotite"])
M("3i.iv.6b", 2, "Incompatible elements are elements that:", "do not fit easily into common rock-forming minerals and stay in the melt",
  ["crystallize first", "are always radioactive", "are only found in the mantle"])
M("3i.iv.6b", 2, "Incompatible elements are excluded from crystals mainly because of:", "unusual ionic size or charge", ["low atomic mass", "color", "magnetism"])
M("3i.iv.6b", 2, "Which of these is an incompatible element that concentrates in pegmatites?", "lithium", ["magnesium", "iron", "calcium"],
  sp=["pegmatite", "spodumene", "lepidolite"])
M("3i.iv.6b", 2, "Which set lists incompatible elements enriched in granite pegmatites?", "Li, Be, B, Cs, Ta, Nb and rare-earth elements",
  ["Mg, Fe, Ni, Cr", "Ca, Na, Si, O", "Fe, Mn, Ti, Al"], sp=["pegmatite"])
M("3i.iv.6b", 2, "Beryllium (in beryl) and boron (in tourmaline) are concentrated in pegmatites because they are:", "incompatible elements left in the final melt",
  ["compatible elements", "abundant in olivine", "volatile gases"], sp=["beryl", "tourmaline", "pegmatite"])
M("3i.iv.6b", 2, "Nickel and chromium are 'compatible' in mafic magmas because they:", "readily substitute into early minerals such as olivine and pyroxene",
  ["remain in the melt", "form pegmatites", "escape as gases"])
M("3i.iv.6b", 3, "Why are the last melts of a granite rich in water?", "water is excluded from most early anhydrous minerals and builds up in the melt",
  ["water is added from the surface", "olivine releases water", "quartz contains water"], sp=["pegmatite"])
F("3i.iv.6b", 3, "Explain why pegmatites are important sources of gemstones and rare metals.",
  "As a granite magma crystallizes, incompatible elements (Li, Be, B, Cs, Ta, Nb, REE) and water become concentrated in the last melt. This water-rich, low-viscosity residual melt crystallizes as pegmatite, producing very large crystals and unusual minerals such as beryl, tourmaline, spodumene and lepidolite.",
  ["incompatible elements concentrate in last melt", "water lowers viscosity", "large crystals and exotic minerals"], sp=["pegmatite"])
T("3i.iv.6b", 2, "Potassium, rubidium and uranium are incompatible elements that are enriched in continental crust relative to the mantle.", True)

# --- sedimentary
M("3i.v.1", 1, "Clastic (detrital) sedimentary rocks are made of:", "fragments of pre-existing rocks and minerals", ["crystals precipitated from water",
  "the remains of organisms only", "volcanic glass"])
M("3i.v.1", 1, "Chemical sedimentary rocks form by:", "precipitation of minerals from solution", ["compaction of rock fragments", "cooling of magma", "heat and pressure"])
M("3i.v.1", 1, "Biochemical sedimentary rocks form from:", "material produced by organisms (shells, skeletons, plant matter)", ["lava", "wind-blown sand only",
  "evaporating lakes only"])
M("3i.v.1", 2, "Lithification of sediment involves:", "compaction and cementation", ["melting and cooling", "foliation", "weathering only"])
M("3i.v.1", 2, "Which minerals most commonly cement sandstone grains?", "quartz, calcite and iron oxides", ["olivine and pyroxene", "halite and sylvite", "mica and talc"])
M("3i.v.2", 2, "Which mineral is most abundant in sandstone because it resists weathering?", "quartz", ["feldspar", "olivine", "calcite"])
M("3i.v.2", 2, "Which sedimentary rock does NOT fizz in acid despite looking like chalk?", "diatomite", ["chalk", "coquina", "travertine"], sp=["diatomite"])
M("3i.v.2", 2, "Chert is composed of:", "microcrystalline quartz", ["calcite", "dolomite", "halite"], sp=["chert-flint"])
M("3i.v.2", 2, "Coccoliths, the main component of chalk, are produced by:", "marine algae (coccolithophores)", ["corals", "diatoms", "radiolarians"],
  sp=["chalk"])
M("3i.v.2", 2, "Diatomite is made from the silica shells of:", "diatoms (single-celled algae)", ["foraminifera", "coccolithophores", "clams"], sp=["diatomite"])
M("3i.v.2", 2, "Black shale gets its color from:", "organic matter preserved in oxygen-poor water", ["iron oxides", "manganese", "volcanic glass"], sp=["shale"])
M("3i.v.2", 2, "Red sandstones and shales ('red beds') are colored by:", "hematite coatings formed in oxidizing environments", ["copper", "organic matter", "glauconite"])
M("3i.v.2", 2, "Which gas is released when shale is fractured to produce natural gas?", "methane", ["carbon dioxide", "hydrogen sulfide", "radon"], sp=["shale"])
M("3i.v.3", 2, "Sorting describes:", "how uniform the grain sizes are", ["how round the grains are", "the mineral composition", "the color of the rock"])
M("3i.v.3", 2, "Rounding of grains increases mainly with:", "longer transport and abrasion", ["deeper burial", "higher temperature", "faster cementation"])
M("3i.v.3", 2, "A sediment that is well sorted, well rounded and nearly all quartz is described as:", "mature", ["immature", "poorly sorted", "angular"],
  sp=["quartz-sandstone"])
M("3i.v.3", 2, "Frosted, well-rounded, well-sorted sand grains suggest transport by:", "wind", ["glaciers", "mudflows", "rivers near their source"])
M("3i.v.3", 2, "A glacier deposits sediment that is typically:", "very poorly sorted with angular clasts (till)", ["well sorted and rounded", "only clay", "only sand"])
M("3i.v.3", 2, "Which mineral would you expect to survive longest during transport and weathering?", "quartz", ["olivine", "feldspar", "pyroxene"])
M("3i.v.3", 2, "The ZTR index (zircon + tourmaline + rutile) is used to measure:", "the mineralogical maturity of sandstones", ["metamorphic grade",
  "magma temperature", "coal rank"], sp=["zircon", "tourmaline", "rutile"])
M("3i.v.4", 2, "Coarse, angular, poorly sorted sediment most likely accumulated:", "close to its source with little transport", ["far from its source",
  "in deep ocean water", "on a calm beach"])
M("3i.v.4", 2, "A fining-upward sequence (coarse at the base, fine at the top) commonly forms in:", "river channels and point bars", ["evaporite basins",
  "coral reefs", "sand dunes"])
M("3i.v.5", 2, "Alluvial fans form:", "where a steep mountain stream reaches a flat valley and suddenly slows", ["at river mouths in the sea", "in deep ocean trenches",
  "on coral reefs"], sp=["arkose", "breccia", "conglomerate"])
M("3i.v.5", 2, "A delta forms where:", "a river enters a standing body of water and drops its sediment", ["a glacier melts", "wind piles up sand",
  "a lake evaporates"])
M("3i.v.5", 2, "Lacustrine deposits form in:", "lakes", ["deserts", "the deep ocean", "glaciers"])
M("3i.v.5", 2, "Aeolian deposits are transported by:", "wind", ["rivers", "glaciers", "ocean currents"])
M("3i.v.5", 2, "Fine-grained laminated muds deposited on a river's floodplain indicate:", "low-energy overbank flooding", ["high-energy channels",
  "glacial deposition", "reef growth"], sp=["shale"])
M("3i.v.5", 2, "Coal forms from plant material that accumulated in:", "swamps", ["deserts", "deep ocean basins", "glaciers"], sp=["bituminous", "lignite"])
M("3i.v.5", 2, "Which depositional environment produces turbidites and greywacke?", "deep-sea fans at the base of continental slopes", ["beaches",
  "desert dunes", "tidal flats"], sp=["greywacke"])
M("3i.v.5", 2, "The deep-ocean (abyssal) plain is dominated by:", "fine clay and microfossil ooze", ["coarse gravel", "cross-bedded sand", "coal"])
M("3i.v.5", 2, "Below the carbonate compensation depth (CCD), calcite shells:", "dissolve, so seafloor sediment is siliceous ooze or clay",
  ["accumulate as chalk", "turn into dolomite", "become oolites"], sp=["chalk", "chert-flint"])
M("3i.v.5", 2, "Coral reefs and fossiliferous limestone form best in:", "warm, clear, shallow marine water", ["cold deep water", "lakes", "deserts"],
  sp=["fossil-limestone"])
M("3i.v.5", 2, "A sabkha is:", "a coastal salt flat where evaporites form", ["a coral reef", "a glacial lake", "a deep-sea trench"], sp=["rock-gypsum", "rock-salt"])
M("3i.v.5", 2, "Where would you most likely find oolitic limestone forming today?", "the Bahamas Banks", ["the Gulf of Alaska", "the Mississippi Delta mud",
  "the Mariana Trench"], sp=["oolitic-limestone"])
M("3i.v.5", 2, "Cross-bedded, well-sorted, frosted quartz sandstone most likely formed in:", "desert sand dunes", ["a swamp", "a deep ocean", "a glacier"],
  sp=["quartz-sandstone"])
M("3i.v.5", 2, "Graded beds in greywacke form from:", "turbidity currents", ["wind", "evaporation", "glacial melting"], sp=["greywacke"])
add("order", "3i.v.5", "Moving from a beach out to the deep ocean, order the sediments typically deposited: clay/ooze, sand, silt/mud.",
    ["sand", "silt/mud", "clay/ooze"], tags=["environment"], diff=2, source="authored", explanation="Energy decreases offshore.")
M("3i.v.6", 1, "Inclined layers within a sedimentary bed, formed by migrating dunes or ripples, are called:", "cross-bedding", ["graded bedding", "mud cracks", "ripple marks"])
M("3i.v.6", 1, "Polygonal cracks in fine sediment that formed as it dried are:", "mud cracks", ["ripple marks", "cross-beds", "graded beds"])
M("3i.v.6", 2, "Mud cracks indicate:", "alternating wetting and drying (exposure to air)", ["deep marine deposition", "glacial transport", "hot springs"])
M("3i.v.6", 2, "A bed that grades from coarse at the bottom to fine at the top is:", "graded bedding", ["cross-bedding", "plane bedding", "ripple marks"])
M("3i.v.6", 2, "Symmetrical ripple marks form from:", "back-and-forth wave motion", ["one-way currents", "wind only", "glaciers"])
M("3i.v.6", 2, "Asymmetrical ripple marks form from:", "currents flowing in one direction", ["waves", "drying", "burrowing organisms"])
M("3i.v.6", 2, "In asymmetrical ripples, the current flowed toward:", "the steep (lee) side", ["the gentle (stoss) side", "either side", "upward"])
M("3i.v.6", 2, "How can graded bedding show which way is 'up' in folded rocks?", "the coarse grains are at the bottom of each bed", ["fine grains are at the bottom",
  "fossils always point up", "it cannot"])
M("3i.v.6", 2, "Fossil tracks, trails and burrows are called:", "trace fossils (ichnofossils)", ["body fossils", "pseudofossils", "concretions"])
M("3i.v.6", 2, "Mixing of sediment layers by burrowing organisms is called:", "bioturbation", ["diagenesis", "compaction", "cementation"])
M("3i.v.6", 2, "Raindrop impressions and mud cracks together suggest a:", "subaerially exposed mudflat or floodplain", ["deep-sea fan", "coral reef", "glacier"])
M("3i.v.6", 2, "Plane (horizontal) bedding generally forms when sediment settles:", "in calm water or under steady flow", ["in a pyroclastic flow", "in a fault zone", "during folding"])
F("3i.v.6", 2, "Explain how cross-bedding can be used to determine the direction of an ancient current or wind.",
  "Cross-beds form on the downstream (lee) faces of migrating ripples and dunes, so the layers dip in the direction the current or wind was flowing.",
  ["layers dip downstream", "lee faces of dunes/ripples"])

# --- metamorphic
M("3i.vi.1", 1, "Foliation is:", "a planar alignment of minerals or bands in a metamorphic rock", ["layering of sediments", "gas bubbles", "rounded grains"])
M("3i.vi.1", 2, "Foliation forms when platy minerals grow:", "perpendicular to the direction of maximum stress", ["parallel to maximum stress", "randomly", "only near magma"])
M("3i.vi.1", 2, "Contact metamorphism usually produces non-foliated rocks because:", "heat dominates and there is little directed pressure",
  ["it happens at the surface", "it melts the rock", "it adds water"])
M("3i.vi.1", 2, "Gneissic banding forms by:", "segregation of light and dark minerals into separate layers at high grade", ["deposition of layers in water",
  "lava flows", "cross-bedding"], sp=["gneiss"])
M("3i.vi.1", 2, "The silky sheen of phyllite comes from:", "microscopic aligned mica and chlorite", ["glass", "graphite", "pyrite"], sp=["phyllite"])
M("3i.vi.1", 2, "Lineation in a metamorphic rock is:", "a linear alignment of elongate minerals", ["a planar fabric", "a gas bubble trail", "a fossil trail"],
  sp=["amphibolite"])
M("3i.vi.1", 2, "Granoblastic texture describes:", "equal-sized, interlocking crystals with no preferred orientation", ["aligned micas", "large porphyroblasts",
  "glassy groundmass"], sp=["marble", "quartzite"])
M("3i.vi.1", 2, "How does quartzite break differently from sandstone?", "quartzite breaks through the grains; sandstone breaks around them",
  ["quartzite breaks around grains", "both break around grains", "both break through grains"], sp=["quartzite", "quartz-sandstone"])
M("3i.vi.1", 2, "A rock that is part metamorphic and part igneous because of partial melting is a:", "migmatite", ["mylonite", "hornfels", "skarn"])
M("3i.vi.1", 2, "A fine-grained, non-foliated rock formed by contact metamorphism of shale is:", "hornfels", ["slate", "phyllite", "quartzite"])
M("3i.vi.1", 2, "A rock produced by intense shearing along a fault zone is a:", "mylonite", ["migmatite", "hornfels", "skarn"])
M("3i.vi.2", 2, "In metamorphism, the chemical composition of the rock usually stays roughly the same except for:", "volatiles such as H2O and CO2",
  ["silicon", "aluminum", "iron"])
M("3i.vi.2", 2, "Metamorphism that changes a rock's bulk composition through hot fluids is called:", "metasomatism", ["recrystallization", "diagenesis", "lithification"])
M("3i.vi.3", 2, "Which mineral would you most expect to form in a metamorphosed shale?", "garnet", ["olivine", "halite", "sanidine"])
M("3i.vi.3", 2, "Wollastonite forms by the reaction:", "calcite + quartz -> wollastonite + CO2", ["dolomite + water -> talc", "feldspar + water -> kaolinite",
  "olivine + water -> serpentine"], sp=["wollastonite"])
M("3i.vi.3", 2, "Serpentine minerals form from olivine by adding:", "water (hydration)", ["CO2", "silica only", "heat with no water"], sp=["serpentinite", "olivine"])
M("3i.vi.3", 2, "Talc forms from the metamorphism of:", "magnesium-rich rocks such as dolomite or ultramafic rocks", ["granite", "quartz sandstone", "halite"],
  sp=["talc", "talc-schist"])
M("3i.vi.3", 2, "Chlorite gives low-grade metamorphic rocks what color?", "green", ["red", "white", "black"])
M("3i.vi.5", 1, "Regional metamorphism is caused mainly by:", "high pressure and temperature over large areas during mountain building",
  ["heat from a nearby intrusion", "meteorite impacts", "weathering"])
M("3i.vi.5", 1, "Contact metamorphism is caused mainly by:", "heat from a nearby magma body", ["mountain building", "burial alone", "shearing on faults"])
M("3i.vi.5", 2, "The zone of altered rock surrounding an intrusion is called a:", "contact aureole", ["batholith", "facies", "isograd"])
M("3i.vi.5", 2, "A line on a map connecting points where an index mineral first appears is an:", "isograd", ["isotherm", "isopach", "isobar"])
M("3i.vi.5", 2, "Hydrothermal metamorphism of seafloor basalt at mid-ocean ridges commonly produces:", "greenstone with chlorite and epidote",
  ["eclogite", "marble", "gneiss"], sp=["epidote"])
M("3i.vi.5", 2, "Shocked quartz and coesite are evidence of:", "impact (shock) metamorphism", ["contact metamorphism", "burial metamorphism", "hydrothermal metamorphism"])
M("3i.vi.5", 2, "Under the Himalayas, which type of metamorphism dominates?", "regional", ["contact", "impact", "hydrothermal"])
M("3i.vi.5", 2, "Next to a dike that intruded limestone, which type of metamorphism occurs?", "contact", ["regional", "impact", "burial"])
M("3i.vi.5", 2, "Which type of metamorphism produces marble at Carrara, Italy (during the Alpine orogeny)?", "regional", ["contact", "impact", "hydrothermal"],
  sp=["marble"])
M("3i.vi.6", 2, "Barrovian metamorphic zones were first mapped in:", "the Scottish Highlands", ["the Alps", "the Appalachians", "the Himalayas"])
M("3i.vi.6", 2, "Index minerals are useful because each:", "forms within a particular range of temperature and pressure", ["is found only in one rock",
  "is radioactive", "is magnetic"])
M("3i.vi.6", 2, "As grade increases, the grain size of metamorphic rocks generally:", "increases", ["decreases", "stays the same", "becomes glassy"])
M("3i.vi.6", 2, "As metamorphic grade increases, hydrous minerals like chlorite and micas tend to:", "break down, releasing water", ["increase", "dissolve in acid",
  "turn into clay"])
M("3i.vi.7", 2, "Metamorphic facies are defined by:", "mineral assemblages that form within particular pressure-temperature ranges", ["rock color",
  "grain size alone", "the protolith alone"])
M("3i.vi.7", 2, "Which facies represents high temperature at LOW pressure?", "hornfels", ["blueschist", "eclogite", "granulite"])
M("3i.vi.7", 2, "Which facies represents high pressure at LOW temperature?", "blueschist", ["hornfels", "granulite", "amphibolite"])
M("3i.vi.7", 2, "Which facies represents the highest pressures?", "eclogite", ["greenschist", "zeolite", "hornfels"])
M("3i.vi.7", 2, "Which facies represents the lowest grade of metamorphism?", "zeolite", ["greenschist", "amphibolite", "granulite"])
M("3i.vi.7", 2, "Granulite facies rocks lack hydrous minerals because:", "very high temperatures drive water out", ["they formed underwater", "they are igneous",
  "they formed at low temperature"])
M("3i.vi.7", 2, "Which facies would basalt pass through in a normal geothermal gradient as temperature rises?", "zeolite -> greenschist -> amphibolite -> granulite",
  ["blueschist -> eclogite", "hornfels only", "granulite -> greenschist -> zeolite"])
M("3i.vi.7", 2, "Blueschist is unusual because subducting slabs stay:", "cold while being pushed to high pressure", ["hot at low pressure",
  "at the surface", "in the mantle permanently"])
M("3i.vi.8", 2, "Paired metamorphic belts form at subduction zones with:", "high-P/low-T (blueschist) near the trench and high-T (greenschist/amphibolite) near the arc",
  ["only contact metamorphism", "eclogite at the surface", "no metamorphism"])
M("3i.vi.8", 2, "Greenstone belts are typically metamorphosed:", "basalt and gabbro (oceanic crust)", ["granite", "limestone", "evaporites"])
M("3i.vi.8", 2, "Continental collision zones like the Himalayas mainly produce:", "regional metamorphism (schist, gneiss)", ["contact metamorphism only",
  "blueschist only", "no metamorphism"])

# --- rock cycle
M("3i.vii", 1, "Which process turns sediment into sedimentary rock?", "compaction and cementation (lithification)", ["melting", "crystallization from magma",
  "metamorphism"])
M("3i.vii", 1, "Which process forms igneous rock?", "cooling and crystallization of magma or lava", ["weathering", "compaction", "heat and pressure without melting"])
M("3i.vii", 1, "Which process forms metamorphic rock?", "heat and pressure changing a rock without melting it", ["erosion", "cementation", "cooling of lava"])
M("3i.vii", 1, "What process breaks rocks down into sediment?", "weathering and erosion", ["metamorphism", "crystallization", "subduction only"])
M("3i.vii", 2, "Which rock type can form from any other rock type?", "all three - any rock can become igneous, sedimentary or metamorphic",
  ["only igneous", "only sedimentary", "only metamorphic"])
M("3i.vii", 2, "What must happen to a metamorphic rock before it can become igneous?", "it must melt", ["it must be weathered", "it must be cemented", "it must be uplifted"])
M("3i.vii", 2, "What process brings deeply buried rocks to the surface?", "uplift and erosion", ["subduction", "deposition", "compaction"])
M("3i.vii", 2, "Mechanical weathering by water freezing in cracks is called:", "frost wedging", ["hydrolysis", "oxidation", "exfoliation"])
M("3i.vii", 2, "Rusting of iron minerals is a type of:", "chemical weathering (oxidation)", ["mechanical weathering", "metamorphism", "lithification"])
M("3i.vii", 2, "Feldspar turning into clay is an example of:", "chemical weathering (hydrolysis)", ["frost wedging", "abrasion", "metamorphism"], sp=["kaolinite"])
M("3i.vii", 2, "Limestone caves form mainly by:", "dissolution by carbonic acid", ["frost wedging", "wind abrasion", "oxidation"])
M("3i.vii", 2, "Exfoliation domes (sheet joints) form when:", "overlying rock is removed and the granite expands", ["lava cools", "sediment is compacted",
  "acid dissolves the rock"], sp=["granite"])
M("3i.vii", 2, "Which plate-tectonic setting connects all parts of the rock cycle?", "subduction zones (melting, metamorphism, uplift and erosion)",
  ["only transform faults", "only hotspots", "only abyssal plains"])
M("3i.vii", 2, "Physical changes to sediment after deposition, including compaction and cementation, are called:", "diagenesis", ["metamorphism", "anatexis", "metasomatism"])
F("3i.vii", 2, "Describe one path through the rock cycle from granite to schist.",
  "Granite is uplifted and weathered into sediment (quartz sand, clay); the sediment is eroded, deposited, buried and lithified into sandstone or shale; deep burial during mountain building metamorphoses shale into schist.",
  ["weathering/erosion", "deposition and lithification", "burial and metamorphism"], sp=["granite", "mica-schist"])

# --- economic uses of rocks
M("3i.viii", 2, "Which rock is the main raw material for Portland cement?", "limestone", ["granite", "basalt", "slate"], sp=["fossil-limestone", "chalk"])
M("3i.viii", 2, "Which rock is preferred for roofing tiles because it splits into thin, durable sheets?", "slate", ["shale", "phyllite", "marble"], sp=["slate"])
M("3i.viii", 2, "Which rock is famous for sculpture because it is soft, uniform and takes a polish?", "marble", ["granite", "basalt", "quartzite"], sp=["marble"])
M("3i.viii", 2, "Which rock is the main source of aluminum?", "bauxite", ["granite", "kaolinite clay", "basalt"], sp=["bauxite"])
M("3i.viii", 2, "Which rock is used as a source of silica sand for glass?", "quartz sandstone", ["arkose", "shale", "basalt"], sp=["quartz-sandstone"])
M("3i.viii", 2, "Which rock is used for pool and beer filtration?", "diatomite", ["chalk", "pumice", "coquina"], sp=["diatomite"])
M("3i.viii", 2, "Which rock is used in lab countertops and carved bowls for its heat and acid resistance?", "soapstone (talc schist)", ["marble", "chalk", "shale"],
  sp=["talc-schist"])
M("3i.viii", 2, "Which rock is the main source rock for shale gas and oil?", "black shale", ["granite", "marble", "pumice"], sp=["shale"])
M("3i.viii", 2, "Which coal is used to make coke for steelmaking?", "bituminous coal", ["lignite", "peat", "anthracite only"], sp=["bituminous"])
M("3i.viii", 2, "Why is marble a poor choice for outdoor statues in polluted cities?", "acid rain dissolves calcite", ["it is magnetic", "it is too hard to carve",
  "it absorbs radiation"], sp=["marble"])
M("3i.viii", 2, "Why are salt domes important to the petroleum industry?", "impermeable salt traps oil and gas against it", ["salt is a fuel", "salt makes oil",
  "salt removes sulfur"], sp=["rock-salt"])
M("3i.viii", 2, "Which rock was used to build the Castillo de San Marcos in Florida and absorbed cannonballs?", "coquina", ["chalk", "travertine", "granite"],
  sp=["coquina"])
M("3i.viii", 2, "The Lincoln Memorial's exterior is made of which rock?", "marble", ["granite", "limestone", "sandstone"], sp=["marble"])
M("3i.viii", 2, "Which rock is crushed for railroad ballast because it is hard and resistant?", "quartzite", ["shale", "chalk", "rock gypsum"], sp=["quartzite"])
M("3i.viii", 2, "Why is serpentinite sometimes regulated in construction?", "it can contain chrysotile asbestos", ["it is radioactive", "it explodes when heated",
  "it dissolves in rain"], sp=["serpentinite"])

# --- thin sections (State/Nationals)
M("3i.ix", 2, "A petrographic microscope uses two polarizers. Viewing with only the lower polarizer is called:", "plane-polarized light (PPL)",
  ["cross-polarized light (XPL)", "reflected light", "UV light"])
M("3i.ix", 2, "With both polarizers inserted, the view is called:", "cross-polarized light (XPL)", ["plane-polarized light", "reflected light", "darkfield"])
M("3i.ix", 2, "Interference colors in cross-polarized light result from:", "birefringence (double refraction) of the mineral", ["the mineral's body color",
  "fluorescence", "magnetism"])
M("3i.ix", 2, "A mineral that goes completely dark in XPL and stays dark on rotation is:", "isotropic (e.g., garnet or glass)", ["anisotropic", "pleochroic", "twinned"],
  sp=["almandine", "obsidian"])
M("3i.ix", 2, "Garnet in thin section appears in cross-polarized light as:", "black (isotropic) at all rotations", ["bright pink and green", "striped", "cross-hatched"],
  sp=["almandine"])
M("3i.ix", 2, "Extinction is when:", "an anisotropic mineral goes dark at certain rotation angles in XPL", ["a mineral disappears in PPL", "a mineral glows",
  "a mineral shatters"])
M("3i.ix", 2, "Which mineral shows very high-order 'pearly' pastel interference colors and twinkles when rotated in PPL?", "calcite", ["quartz", "garnet", "plagioclase"],
  sp=["calcite"])
M("3i.ix", 2, "Calcite's extreme 'twinkling' (change in relief) on stage rotation is due to:", "its very high birefringence", ["its cleavage", "its color", "isotropy"],
  sp=["calcite"])
M("3i.ix", 2, "Plagioclase is recognized in XPL by:", "parallel bands of alternating light and dark (polysynthetic twinning)", ["cross-hatched twinning",
  "isotropic black", "high-order colors"], sp=["albite", "labradorite"])
M("3i.ix", 2, "Microcline is recognized in XPL by:", "cross-hatched 'tartan' twinning", ["parallel albite twins", "isotropic black", "radiating fibers"],
  sp=["orthoclase-microcline"])
M("3i.ix", 2, "Augite in thin section typically shows:", "two cleavages at nearly 90° and bright second-order interference colors",
  ["isotropic black", "tartan twinning", "no cleavage and gray colors"], sp=["augite"])
M("3i.ix", 2, "Quartz in XPL typically shows:", "low first-order gray to white colors with no cleavage or twinning", ["bright high-order colors",
  "tartan twinning", "isotropic black"])
M("3i.ix", 2, "Relief in thin section describes:", "how strongly a mineral's outline stands out, based on refractive index", ["its color", "its hardness",
  "its interference color"])
M("3i.ix", 2, "Which mineral has high relief and isotropic behavior in thin section?", "garnet", ["quartz", "plagioclase", "microcline"], sp=["almandine"])
M("3i.ix", 2, "In a photomicrograph, a rock with crystals all touching and no glass is described as:", "holocrystalline", ["hypocrystalline", "holohyaline", "vesicular"])
M("3i.ix", 2, "In thin section, basalt differs from pumice in that basalt shows:", "small interlocking crystals (and maybe phenocrysts), while pumice is mostly glass with bubbles",
  ["only glass", "rounded grains", "foliation"], sp=["basalt", "pumice"])
M("3i.ix", 2, "In thin section, arkose is distinguished from quartz sandstone by:", "abundant feldspar grains (twinning, cloudy alteration)", ["rounded quartz only",
  "glass", "foliation"], sp=["arkose", "quartz-sandstone"])
M("3i.ix", 2, "Concentric layered spheres with a central nucleus seen in a thin section of limestone are:", "ooids", ["vesicles", "phenocrysts", "porphyroblasts"],
  sp=["oolitic-limestone"])
M("3i.ix", 2, "Well-sorted, rounded grains in thin section suggest:", "long transport (mature sediment)", ["little transport", "volcanic origin", "metamorphism"])
M("3i.ix", 2, "Skeletal fragments visible in a thin section indicate a:", "biochemical (bioclastic) sedimentary rock", ["volcanic rock", "metamorphic rock", "evaporite"])
M("3i.ix", 2, "A porphyritic texture in thin section shows:", "large phenocrysts in a fine-grained or glassy groundmass", ["uniform grains", "rounded clasts", "foliation"])
M("3i.ix", 2, "The standard thickness of a petrographic thin section is:", "30 micrometers", ["3 millimeters", "300 micrometers", "3 micrometers"])
M("3i.ix", 2, "Interference color charts (Michel-Lévy) relate interference color to:", "birefringence and thin-section thickness", ["hardness", "density", "age"])
M("3i.ix", 2, "Pleochroism in thin section is observed:", "in plane-polarized light while rotating the stage", ["only in XPL", "only with UV", "only in reflected light"])
M("3i.ix", 2, "Which listed thin-section mineral has inclined extinction and two near-90° cleavages?", "augite", ["garnet", "calcite", "microcline"], sp=["augite"])
M("3i.ix", 2, "Calcite cleavage in thin section appears as:", "two sets of lines crossing at about 75°/105° (rhombohedral)", ["one set of lines", "no cleavage", "90° cubes"],
  sp=["calcite"])
M("3i.ix", 2, "Sandstone vs. arkose vs. greywacke in thin section are distinguished mainly by:", "proportions of quartz, feldspar, rock fragments and matrix",
  ["color under UV", "the presence of glass", "foliation"])
M("3i.ix", 3, "Exsolution lamellae in a pyroxene appear in thin section as:", "thin parallel stripes of a second pyroxene along crystallographic planes",
  ["random blobs", "vesicles", "growth rings"], sp=["augite"])


def run():
    for kind, t, d, p, c, extra, e, sp in ITEMS:
        kw = dict(diff=d, explanation=e, specimens=list(sp), tags=["authored"], source="authored")
        if kind == "M":
            mcq(t, p, c, extra, n=min(3, len(extra)), **kw)
        elif kind == "T":
            tf(t, p, c, **kw)
        elif kind == "S":
            short(t, p, c, list(extra), **kw)
        else:
            kw.pop("explanation")
            add("frq", t, p, c, keypoints=list(extra), **kw)
