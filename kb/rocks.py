"""Rock knowledge base for the Science Olympiad Rocks & Minerals list.

Fields
  slug, name, type ('igneous' | 'sedimentary' | 'metamorphic')
  sub        igneous: 'intrusive' | 'extrusive' | 'pyroclastic'
             sedimentary: 'clastic' | 'chemical' | 'biochemical'
             metamorphic: 'foliated' | 'non-foliated'
  texture    list of texture terms (rulebook vocabulary)
  comp       igneous: felsic | intermediate | mafic | ultramafic
  minerals   essential / typical minerals (list order = most abundant first)
  grain      grain size description
  env        environments of formation
  plate      plate-tectonic setting (if meaningful)
  protolith  metamorphic parent rock(s)
  grade      metamorphic grade; facies  typical facies
  equiv      intrusive/extrusive equivalent or other key relationship
  uses       economic uses
  acid       reaction with dilute HCl
  clue       distinctive identification clue
  level      'regional' | 'state'
"""

R = []


def rock(**k):
    for f in ("comp", "protolith", "grade", "facies", "equiv", "plate", "acid", "etym", "other"):
        k.setdefault(f, None)
    k.setdefault("level", "regional")
    k.setdefault("group", None)
    k.setdefault("texture", [])
    R.append(k)


# ------------------------------------------------------------------ igneous
rock(slug="andesite", name="Andesite", type="igneous", sub="extrusive", texture=["aphanitic", "porphyritic"],
     comp="intermediate", minerals=["plagioclase (andesine)", "hornblende", "pyroxene", "biotite"],
     grain="fine-grained, often with plagioclase or hornblende phenocrysts",
     env=["stratovolcanoes in volcanic arcs"], plate="ocean-continent subduction zones (Andes, Cascades)",
     equiv="diorite", silica="about 52-63% SiO2",
     uses=["crushed stone and road aggregate"],
     clue="medium-gray fine-grained volcanic rock, often with light plagioclase or dark hornblende phenocrysts",
     etym="named for the Andes Mountains")
rock(slug="basalt", name="Basalt", type="igneous", sub="extrusive", texture=["aphanitic", "vesicular", "porphyritic"],
     comp="mafic", minerals=["calcium-rich plagioclase", "pyroxene (augite)", "olivine"],
     grain="fine-grained; may have olivine phenocrysts or gas vesicles",
     env=["lava flows", "oceanic crust", "flood basalts (Columbia River, Deccan Traps)", "shield volcanoes"],
     plate="mid-ocean ridges (divergent boundaries) and hotspots (Hawaii)",
     equiv="gabbro", silica="about 45-52% SiO2",
     uses=["crushed stone and railroad ballast", "rock wool insulation", "cast basalt tiles"],
     clue="dark, dense, fine-grained volcanic rock; may contain vesicles or green olivine crystals",
     other="cools into columnar joints on land and pillow lava under water; the most common volcanic rock on Earth")
rock(slug="diorite", name="Diorite", type="igneous", sub="intrusive", texture=["phaneritic"],
     comp="intermediate", minerals=["plagioclase (sodium-calcium)", "hornblende", "biotite", "little or no quartz"],
     grain="coarse-grained with a 'salt-and-pepper' look",
     env=["plutons and batholiths beneath volcanic arcs"], plate="subduction zones",
     equiv="andesite", silica="about 52-63% SiO2",
     uses=["dimension and building stone", "crushed stone"],
     clue="coarse-grained 'salt-and-pepper' rock of roughly equal white plagioclase and black hornblende, with little quartz")
rock(slug="gabbro", name="Gabbro", type="igneous", sub="intrusive", texture=["phaneritic"],
     comp="mafic", minerals=["calcium-rich plagioclase", "pyroxene (augite)", "olivine"],
     grain="coarse-grained, dark",
     env=["lower oceanic crust", "layered intrusions (Stillwater, Bushveld)", "sills and lopoliths"],
     plate="mid-ocean ridges (lower oceanic crust)",
     equiv="basalt", silica="about 45-52% SiO2",
     uses=["'black granite' countertops and monuments", "crushed stone"],
     clue="dark, coarse-grained rock of gray plagioclase and black pyroxene with no quartz")
rock(slug="granite", name="Granite", type="igneous", sub="intrusive", texture=["phaneritic", "porphyritic"],
     comp="felsic", minerals=["quartz", "potassium feldspar", "sodium plagioclase", "biotite", "muscovite", "hornblende"],
     grain="coarse-grained, light colored (pink, white or gray)",
     env=["batholiths and plutons in continental crust"],
     plate="continental crust at convergent boundaries (continental arcs and collisions)",
     equiv="rhyolite", silica="over 69% SiO2 (felsic: over ~63%)",
     uses=["dimension stone, countertops and monuments", "crushed stone"],
     clue="light-colored coarse-grained rock with glassy gray quartz, pink or white feldspar and black mica or hornblende")
rock(slug="obsidian", name="Obsidian", type="igneous", sub="extrusive", texture=["glassy"],
     comp="felsic", minerals=["volcanic glass (no crystals)"],
     grain="no grains - natural glass",
     env=["rhyolitic lava flows and domes that cooled too quickly for crystals to form"],
     plate="continental volcanism (Yellowstone, Cascades)",
     equiv="rhyolite (same composition, but glassy)", silica="about 70-75% SiO2",
     uses=["arrowheads, blades and tools (historic)", "surgical scalpels", "ornamental"],
     clue="black glassy rock with conchoidal fracture and razor-sharp edges",
     other="dark despite being felsic because tiny amounts of iron-titanium oxides color the glass; varieties include snowflake (cristobalite spherulites) and mahogany (hematite)")
rock(slug="pegmatite", name="Pegmatite", type="igneous", sub="intrusive", texture=["pegmatitic"],
     comp="felsic", minerals=["quartz", "potassium feldspar", "sodium plagioclase", "muscovite", "tourmaline, beryl, spodumene and lepidolite (in some)"],
     grain="extremely coarse - crystals over 1 cm, sometimes meters long",
     env=["dikes and veins at the margins of granite plutons, from the last water-rich melt"],
     plate="continental crust (with granite batholiths)",
     equiv=None, silica="felsic (granitic)",
     uses=["source of lithium, beryllium, cesium, tantalum and rare-earth elements", "gemstones (tourmaline, beryl, topaz)", "feldspar and mica"],
     clue="granite-like rock with enormous interlocking crystals",
     other="crystals grow huge because water and incompatible elements concentrated in the last melt lower its viscosity and speed diffusion")
rock(slug="peridotite", name="Peridotite", type="igneous", sub="intrusive", texture=["phaneritic"],
     comp="ultramafic", minerals=["olivine", "pyroxene", "garnet or spinel (minor)"],
     grain="coarse-grained, green to dark green",
     env=["upper mantle", "base of ophiolites", "xenoliths in kimberlite and basalt"],
     plate="mantle exposed in ophiolites along obducted oceanic crust",
     equiv="komatiite (rare ultramafic lava)", silica="under 45% SiO2",
     uses=["source of chromite, nickel and platinum (associated deposits)", "peridot gems", "proposed carbon capture"],
     clue="dense, green, coarse-grained rock made mostly of olivine",
     other="dunite is a peridotite with over 90% olivine; hydration turns peridotite into serpentinite")
rock(slug="pumice", name="Pumice", type="igneous", sub="extrusive", texture=["vesicular", "glassy"],
     comp="felsic", minerals=["volcanic glass full of gas bubbles"],
     grain="frothy glass - no visible crystals",
     env=["explosive eruptions of gas-rich, viscous felsic magma"],
     plate="subduction-zone and continental volcanoes",
     equiv=None, silica="felsic to intermediate",
     uses=["abrasive (pumice stones, stonewashed jeans)", "lightweight concrete aggregate", "horticulture and cat litter"],
     clue="very light, pale, frothy volcanic glass that floats on water")
rock(slug="rhyolite", name="Rhyolite", type="igneous", sub="extrusive", texture=["aphanitic", "porphyritic"],
     comp="felsic", minerals=["quartz", "potassium feldspar (sanidine)", "sodium plagioclase", "biotite"],
     grain="fine-grained, often flow-banded, pink to light gray",
     env=["viscous lava domes and explosive continental eruptions (Yellowstone)"],
     plate="continental volcanism, continental rifts and hotspots",
     equiv="granite", silica="over 69% SiO2",
     uses=["crushed stone", "historic tool stone"],
     clue="light-colored (pink or pale gray), fine-grained volcanic rock, often flow-banded with small quartz or feldspar phenocrysts")
rock(slug="scoria", name="Scoria", type="igneous", sub="extrusive", texture=["vesicular"],
     comp="mafic", minerals=["basaltic glass and microcrystals (plagioclase, pyroxene, olivine)"],
     grain="highly vesicular, dark red to black",
     env=["cinder cones and the gassy tops of basaltic lava flows"],
     plate="hotspots and rifts",
     equiv=None, silica="mafic (basaltic)",
     uses=["landscaping 'lava rock'", "gas-grill briquettes", "road grit and drainage"],
     clue="dark red or black vesicular basalt; too dense to float, unlike pumice",
     other="vesicles are larger with thicker walls than pumice, so it sinks")
rock(slug="syenite", name="Syenite", type="igneous", sub="intrusive", texture=["phaneritic"], level="state",
     comp="intermediate", minerals=["potassium (alkali) feldspar", "hornblende", "biotite", "little or no quartz (under 5%)", "may contain nepheline or sodalite"],
     grain="coarse-grained, usually pink to gray",
     env=["alkaline plutons in continental rifts"], plate="continental rifts",
     equiv="trachyte", silica="about 55-65% SiO2",
     uses=["dimension stone (larvikite)", "nepheline syenite for glass and ceramics"],
     clue="coarse-grained rock that looks like granite but has little or no quartz",
     etym="named for Syene (Aswan), Egypt")
rock(slug="tuff", name="Tuff", type="igneous", sub="pyroclastic", texture=["pyroclastic"], level="state",
     comp="usually felsic", minerals=["volcanic ash (glass shards)", "crystal fragments", "rock fragments"],
     grain="fine-grained consolidated ash (fragments under 2 mm), may include lapilli",
     env=["ash falls and pyroclastic flows from explosive eruptions"],
     plate="subduction-zone and continental volcanoes",
     equiv=None, silica="usually felsic",
     uses=["lightweight building stone (Rome; Easter Island moai)", "Yucca Mountain nuclear-waste studies"],
     clue="light, porous rock of compacted or welded volcanic ash",
     other="welded tuff (ignimbrite) forms when hot pyroclastic-flow deposits fuse together")
rock(slug="tuff-breccia", name="Tuff Breccia", type="igneous", sub="pyroclastic", texture=["pyroclastic"], level="state",
     comp="variable", minerals=["angular volcanic blocks (over 64 mm)", "ash matrix"],
     grain="large angular volcanic fragments in a fine ash matrix",
     env=["near-vent pyroclastic deposits, block-and-ash flows and lahars"],
     plate="explosive volcanoes",
     equiv=None, silica="variable",
     uses=["local building stone"],
     clue="angular volcanic blocks set in a matrix of volcanic ash")

# ------------------------------------------------------------------ sedimentary
rock(slug="banded-iron-formation", name="Banded Iron Formation", type="sedimentary", sub="chemical", texture=["crystalline", "banded"],
     minerals=["hematite", "magnetite", "chert / jasper"],
     grain="fine-grained alternating layers",
     env=["Precambrian oceans (about 3.8-1.8 billion years ago)"],
     uses=["the world's main source of iron ore (Lake Superior 'taconite', Pilbara, Brazil)"],
     acid="none",
     clue="alternating red/black bands of iron oxides (hematite, magnetite) and chert or jasper",
     other="formed when oxygen from photosynthesizing cyanobacteria oxidized dissolved Fe2+, precipitating iron oxides; records the Great Oxidation Event")
rock(slug="bauxite", name="Bauxite", type="sedimentary", sub="chemical", texture=["pisolitic", "earthy"],
     minerals=["gibbsite", "boehmite", "diaspore", "kaolinite", "iron oxides"],
     grain="earthy, often pisolitic (pea-sized round grains)",
     env=["intense chemical weathering in hot, wet tropical climates (residual laterite soils)"],
     uses=["the main ore of aluminum (Bayer process, then Hall-Heroult electrolysis)", "abrasives and refractories"],
     acid="none",
     clue="reddish-brown to cream, earthy rock with pea-sized rounded pisoliths",
     other="silica and soluble cations are leached away, leaving aluminum hydroxides behind")
rock(slug="breccia", name="Breccia", type="sedimentary", sub="clastic", texture=["clastic"],
     minerals=["angular rock fragments of any composition", "sand/silt matrix", "cement"],
     grain="angular gravel-size clasts (over 2 mm), poorly sorted",
     env=["talus slopes at the base of cliffs", "fault zones", "collapse breccias", "proximal alluvial fans"],
     uses=["decorative stone"],
     clue="large angular fragments cemented in a finer matrix",
     other="angular clasts mean little transport - the sediment source was close by")
rock(slug="chert-flint", name="Chert / Flint", type="sedimentary", sub="chemical", texture=["crystalline", "microcrystalline"],
     minerals=["microcrystalline quartz (chalcedony)"],
     grain="very fine (microcrystalline); breaks with conchoidal fracture",
     env=["nodules in chalk and limestone (flint)", "deep-sea beds of radiolarian or diatom ooze (bedded chert)"],
     uses=["stone tools and arrowheads", "fire-starting (sparks against steel)", "abrasives"],
     acid="none",
     clue="hard (~7), dense, waxy microcrystalline quartz with conchoidal fracture; flint is the dark variety",
     other="can be chemical or biochemical (silica from radiolarians, diatoms and sponge spicules)")
rock(slug="conglomerate", name="Conglomerate", type="sedimentary", sub="clastic", texture=["clastic"],
     minerals=["rounded pebbles (often quartz, quartzite, chert)", "sand matrix", "cement (silica, calcite, iron oxide)"],
     grain="rounded gravel-size clasts (over 2 mm)",
     env=["river channels", "beaches", "alluvial fans"],
     uses=["decorative stone", "some host placer gold (Witwatersrand)"],
     clue="rounded pebbles and cobbles cemented in a finer matrix ('puddingstone')",
     other="rounded clasts indicate long transport in high-energy water")
rock(slug="diatomite", name="Diatomite", type="sedimentary", sub="biochemical", texture=["bioclastic", "earthy"], level="state",
     minerals=["opal-A silica from diatom frustules (shells)"],
     grain="extremely fine, very light, chalky and porous",
     env=["lakes (lacustrine) and quiet marine basins with diatom blooms"],
     uses=["filtration (pools, beer, sugar)", "mild abrasive and polish", "insulation", "absorbent and natural insecticide", "stabilizer in Nobel's dynamite"],
     acid="does not fizz (silica, not calcite)",
     clue="white, extremely light, chalk-like rock that does NOT fizz in acid",
     aka=["diatomaceous earth", "kieselguhr"])
rock(slug="dolostone", name="Dolostone", type="sedimentary", sub="chemical", texture=["crystalline"],
     minerals=["dolomite"],
     grain="fine to medium crystalline, often sugary; may weather tan",
     env=["dolomitization of limestone by magnesium-rich brines (tidal flats, lagoons)"],
     uses=["construction aggregate", "building stone", "magnesium source and steel flux", "oil and gas reservoir rock"],
     acid="fizzes only when powdered",
     clue="limestone-like rock that fizzes only when scratched into powder")
rock(slug="rock-salt", name="Rock Salt", type="sedimentary", sub="chemical", texture=["crystalline"],
     minerals=["halite"],
     grain="coarsely crystalline, interlocking cubes",
     env=["evaporation of seawater in restricted basins, lagoons and sabkhas", "salt domes"],
     uses=["table salt", "road de-icing", "chemical industry (chlorine, sodium hydroxide)", "underground storage caverns"],
     acid="none (dissolves in water)",
     clue="crystalline evaporite of halite that tastes salty")
rock(slug="rock-gypsum", name="Rock Gypsum", type="sedimentary", sub="chemical", texture=["crystalline"],
     minerals=["gypsum", "anhydrite"],
     grain="fine to coarse crystalline, soft",
     env=["evaporation of seawater (precipitates before halite)"],
     uses=["drywall and plaster", "cement additive", "soil conditioner"],
     acid="none",
     clue="soft (scratched by a fingernail) white to gray crystalline evaporite")
rock(slug="shale", name="Shale", type="sedimentary", sub="clastic", texture=["clastic", "fissile"],
     minerals=["clay minerals", "quartz silt", "organic matter (black shale)"],
     grain="clay-sized (under 1/256 mm); fissile - splits into thin layers",
     env=["low-energy water: lakes, lagoons, deep marine, floodplains"],
     uses=["bricks, tiles and cement", "source rock for oil and natural gas (black shale)", "oil shale"],
     acid="none (unless calcareous)",
     clue="fine-grained, smooth, fissile rock that splits into thin layers",
     other="the protolith of slate, phyllite and mica schist")
rock(slug="anthracite", name="Anthracite", type="sedimentary", sub="biochemical", texture=["organic"], group="Coal varieties",
     minerals=["carbon (organic matter)"],
     grain="hard, shiny, submetallic; conchoidal fracture",
     env=["coal swamps buried and then heated/compressed during mountain building (Appalachians, Pennsylvania)"],
     uses=["clean-burning home heating fuel", "water filtration", "steelmaking"],
     rank=4, carbon="about 86-97% fixed carbon",
     clue="shiny, hard, black coal with conchoidal fracture that does not soil the hands",
     other="the highest rank of coal; often classed as metamorphic. Burns hot with a short blue flame and little smoke")
rock(slug="bituminous", name="Bituminous Coal", type="sedimentary", sub="biochemical", texture=["organic"], group="Coal varieties",
     minerals=["carbon (organic matter)", "volatile hydrocarbons"],
     grain="black, banded dull and bright layers, blocky",
     env=["burial of peat/lignite from ancient swamps (Carboniferous)"],
     uses=["electricity generation (steam coal)", "coke for steelmaking (metallurgical coal)"],
     rank=3, carbon="about 45-86% fixed carbon",
     clue="black, banded coal with dull and shiny layers that soils the fingers",
     other="the most abundant rank of coal; burns with a smoky yellow flame")
rock(slug="lignite", name="Lignite", type="sedimentary", sub="biochemical", texture=["organic"], group="Coal varieties",
     minerals=["carbon (organic matter)", "water"],
     grain="brown, soft, crumbly; plant (woody) texture may be visible",
     env=["shallow burial of peat from swamps"],
     uses=["electricity generation (near the mine)"],
     rank=2, carbon="about 25-35% fixed carbon",
     clue="soft, crumbly, brownish-black coal with visible woody plant material",
     other="the lowest rank of coal, with the highest moisture content (up to ~45%)", aka=["brown coal"])
rock(slug="chalk", name="Chalk", type="sedimentary", sub="biochemical", texture=["bioclastic"], group="Limestone varieties",
     minerals=["calcite from coccoliths (microscopic algae plates) and foraminifera"],
     grain="very fine-grained, soft, porous, white",
     env=["calm, warm, relatively deep marine shelves (Cretaceous seas)"],
     uses=["lime and cement", "agricultural lime", "filler"],
     acid="fizzes vigorously",
     clue="soft, white, powdery limestone that fizzes strongly and writes on a board",
     other="the White Cliffs of Dover; the Cretaceous period is named from Latin creta, 'chalk'")
rock(slug="coquina", name="Coquina", type="sedimentary", sub="biochemical", texture=["bioclastic"], group="Limestone varieties",
     minerals=["shell fragments of calcite and aragonite"],
     grain="coarse, loosely cemented shell hash, very porous",
     env=["high-energy beaches and nearshore bars"],
     uses=["building stone (Castillo de San Marcos, St. Augustine, Florida)", "road base"],
     acid="fizzes vigorously",
     clue="a mass of whole and broken shells weakly cemented together",
     etym="Spanish 'cockle shell'")
rock(slug="fossil-limestone", name="Fossil Limestone", type="sedimentary", sub="biochemical", texture=["bioclastic"], group="Limestone varieties",
     minerals=["calcite", "visible fossils (brachiopods, crinoids, corals, bryozoans)"],
     grain="fossils in a fine-grained calcite matrix",
     env=["warm, shallow marine shelves and reefs"],
     uses=["building stone", "cement and lime", "crushed stone"],
     acid="fizzes vigorously",
     clue="gray limestone packed with visible fossils that fizzes in acid")
rock(slug="oolitic-limestone", name="Oolitic Limestone", type="sedimentary", sub="chemical", texture=["oolitic", "crystalline"], group="Limestone varieties",
     minerals=["calcite ooids (concentrically layered spheres)"],
     grain="sand-sized spheres (ooids, 0.25-2 mm) cemented together",
     env=["warm, shallow, agitated water supersaturated in CaCO3 (Bahamas, Great Salt Lake)"],
     uses=["building stone (Bath stone, Portland stone)"],
     acid="fizzes vigorously",
     clue="limestone made of tiny round 'fish-egg' grains (ooids)",
     other="ooids grow concentric layers as waves roll them around a nucleus; spheres over 2 mm are pisoids", aka=["oolite"])
rock(slug="travertine", name="Travertine", type="sedimentary", sub="chemical", texture=["crystalline", "banded"], group="Limestone varieties",
     minerals=["calcite", "aragonite"],
     grain="banded, crystalline, with irregular pores (vugs)",
     env=["hot springs (Mammoth Hot Springs, Yellowstone; Pamukkale)", "caves (stalactites and stalagmites)"],
     uses=["building and flooring stone (the Colosseum, the Getty Center)"],
     acid="fizzes vigorously",
     clue="banded, porous limestone deposited by hot springs or in caves",
     other="precipitates when CO2 degasses from spring or cave water; spongy, cool-water deposits are called tufa")
rock(slug="arkose", name="Arkose", type="sedimentary", sub="clastic", texture=["clastic"], group="Sandstone varieties",
     minerals=["quartz", "potassium feldspar (25% or more)", "some mica and rock fragments"],
     grain="sand-sized, angular to subangular, poorly to moderately sorted; pinkish",
     env=["alluvial fans and rift basins near eroding granite, often in arid climates"],
     uses=["building stone"],
     clue="pinkish sandstone with abundant angular feldspar grains",
     other="immature: feldspar survives only with rapid erosion and short transport")
rock(slug="greywacke", name="Greywacke", type="sedimentary", sub="clastic", texture=["clastic"], group="Sandstone varieties", level="state",
     minerals=["quartz", "feldspar", "rock fragments", "over 15% clay/silt matrix"],
     grain="sand-sized angular grains in a muddy matrix, poorly sorted",
     env=["turbidity currents on deep-sea fans and trenches"],
     plate="active margins (subduction-zone trenches and forearcs)",
     uses=["road aggregate"],
     clue="dark, hard 'dirty sandstone' of angular grains in a clay matrix",
     aka=["graywacke", "wacke"])
rock(slug="quartz-sandstone", name="Quartz Sandstone", type="sedimentary", sub="clastic", texture=["clastic"], group="Sandstone varieties",
     minerals=["quartz (over 90%)", "silica or calcite cement"],
     grain="sand-sized (1/16-2 mm), well sorted, well rounded",
     env=["beaches", "desert dunes (aeolian)", "shallow marine shelves"],
     plate="passive margins and stable cratons",
     uses=["glass making (silica sand)", "building stone", "aquifer and oil reservoir rock"],
     clue="light-colored, gritty sandstone of well-sorted, rounded quartz grains",
     other="mature: long transport and weathering removed everything but quartz; protolith of quartzite", aka=["quartz arenite"])

# ------------------------------------------------------------------ metamorphic
rock(slug="amphibolite", name="Amphibolite", type="metamorphic", sub="foliated", texture=["weakly foliated", "lineated"], level="state",
     minerals=["hornblende", "plagioclase", "garnet (sometimes)"],
     grain="medium to coarse, dark green to black, often lineated",
     env=["medium- to high-grade regional metamorphism"],
     protolith="basalt or gabbro (mafic igneous rock)", grade="medium to high", facies="amphibolite",
     uses=["dimension stone and crushed stone"],
     clue="dark, coarse-grained rock of aligned hornblende and plagioclase")
rock(slug="gneiss", name="Gneiss", type="metamorphic", sub="foliated", texture=["gneissic banding"],
     minerals=["quartz", "feldspar", "biotite", "hornblende", "garnet"],
     grain="medium to coarse, with alternating light and dark bands",
     env=["high-grade regional metamorphism deep in mountain belts"],
     plate="continental-continental collision",
     protolith="granite (orthogneiss) or shale and other sediments (paragneiss)", grade="high", facies="amphibolite to granulite",
     uses=["dimension stone, countertops and flooring"],
     clue="coarse, banded rock of alternating light (quartz, feldspar) and dark (biotite, hornblende) layers",
     other="the Acasta Gneiss of Canada (~4.0 billion years) is among the oldest known rocks")
rock(slug="marble", name="Marble", type="metamorphic", sub="non-foliated", texture=["granoblastic", "non-foliated"],
     minerals=["calcite", "dolomite"],
     grain="interlocking recrystallized crystals, often sugary",
     env=["contact or regional metamorphism"],
     protolith="limestone or dolostone", grade="low to high", facies="any",
     uses=["sculpture (Carrara marble, Michelangelo's David)", "monuments and buildings (Lincoln Memorial)", "countertops", "crushed lime"],
     acid="fizzes (calcite marble); dolomitic marble only when powdered",
     clue="sugary, interlocking crystals of calcite that fizz in acid; softer than glass")
rock(slug="phyllite", name="Phyllite", type="metamorphic", sub="foliated", texture=["phyllitic", "foliated"],
     minerals=["fine-grained muscovite (sericite)", "chlorite", "quartz"],
     grain="very fine, with a silky sheen; often crinkled (crenulated)",
     env=["low-grade regional metamorphism"],
     protolith="shale (via slate)", grade="low (between slate and schist)", facies="greenschist",
     uses=["decorative and flooring stone"],
     clue="fine-grained foliated rock with a silky, satiny sheen from microscopic mica",
     etym="Greek phyllon, 'leaf'")
rock(slug="quartzite", name="Quartzite", type="metamorphic", sub="non-foliated", texture=["granoblastic", "non-foliated"],
     minerals=["quartz"],
     grain="fused, interlocking quartz grains; breaks through the grains, not around them",
     env=["contact or regional metamorphism"],
     protolith="quartz sandstone", grade="low to high", facies="any",
     uses=["construction aggregate and railroad ballast", "countertops", "silica for glass and silicon"],
     acid="none",
     clue="very hard (~7), sugary rock of fused quartz that breaks through grains",
     other="highly resistant to weathering, so it forms ridges")
rock(slug="serpentinite", name="Serpentinite", type="metamorphic", sub="non-foliated", texture=["non-foliated", "massive"], level="state",
     minerals=["serpentine-group minerals (antigorite, lizardite, chrysotile)", "magnetite"],
     grain="fine-grained, mottled green, waxy to greasy, slippery feel",
     env=["hydration of mantle rock at mid-ocean ridges and subduction zones", "ophiolites"],
     plate="oceanic lithosphere (divergent boundaries) and subduction zones",
     protolith="peridotite (or dunite)", grade="low to medium (hydrothermal)", facies="greenschist",
     uses=["decorative stone ('verde antique')", "chrysotile asbestos (historic)"],
     clue="mottled green, waxy, slippery-feeling rock",
     other="California's state rock; serpentine soils are low in calcium and high in nickel and chromium, hosting specialized plants")
rock(slug="slate", name="Slate", type="metamorphic", sub="foliated", texture=["slaty cleavage", "foliated"],
     minerals=["microscopic clay and mica (muscovite, chlorite)", "quartz"],
     grain="very fine-grained, dull; splits into flat sheets",
     env=["low-grade regional metamorphism"],
     protolith="shale or mudstone", grade="low", facies="greenschist (lower)",
     uses=["roofing tiles", "flooring", "chalkboards", "pool-table beds", "gravestones"],
     clue="dull, very fine-grained rock that splits into flat, hard sheets and 'rings' when tapped",
     other="slaty cleavage forms perpendicular to the squeezing direction and need not follow original bedding")
rock(slug="garnet-schist", name="Garnet Schist", type="metamorphic", sub="foliated", texture=["schistose", "porphyroblastic"], group="Schist varieties",
     minerals=["muscovite", "biotite", "quartz", "almandine garnet porphyroblasts"],
     grain="medium to coarse, sparkly mica with red garnet crystals",
     env=["medium- to high-grade regional metamorphism"],
     plate="continental collision zones",
     protolith="shale", grade="medium to high", facies="amphibolite",
     uses=["garnet abrasive", "decorative stone"],
     clue="sparkly mica schist studded with red garnet crystals")
rock(slug="mica-schist", name="Mica Schist", type="metamorphic", sub="foliated", texture=["schistose"], group="Schist varieties",
     minerals=["muscovite", "biotite", "quartz"],
     grain="medium-grained, visibly sparkly aligned mica flakes",
     env=["medium-grade regional metamorphism"],
     plate="convergent boundaries (mountain building)",
     protolith="shale (via slate and phyllite)", grade="medium", facies="greenschist to amphibolite",
     uses=["decorative stone"],
     clue="sparkly, flaky rock of visible aligned mica")
rock(slug="talc-schist", name="Talc Schist (Soapstone)", type="metamorphic", sub="foliated", texture=["schistose", "massive"], group="Schist varieties", level="state",
     minerals=["talc", "chlorite", "magnesite", "serpentine"],
     grain="soft, soapy, gray-green; carvable with a knife",
     env=["metamorphism and hydrothermal alteration of ultramafic rock"],
     protolith="peridotite or serpentinite (ultramafic rock), or siliceous dolomite", grade="low to medium", facies="greenschist",
     uses=["carvings and sculpture", "countertops, lab benches and sinks (heat- and acid-resistant)", "woodstoves (holds heat)"],
     clue="very soft, soapy-feeling rock that can be scratched with a fingernail")

for r in R:
    r.setdefault("aka", [])
    r.setdefault("silica", None)
    r.setdefault("rank", None)
    r.setdefault("carbon", None)
    r.setdefault("etym", None)

ROCKS = {r["slug"]: r for r in R}
