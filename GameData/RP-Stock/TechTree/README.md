# Kerbal RP-0 Tech Tree (part of RP-Stock)

RP-0's tech tree (layout, node names, prerequisites, chronological order 1945 -> 2150) with every
part you have installed placed on it. Only the tree follows RP-0 - part costs, engines and
everything else stay stock.

- Science costs: RP-0's node costs x0.48, about 55,000 science for the whole tree.
- Part placement (see part_placement.csv - one row per part, with the reason):
  * RP-1 database (724 parts): RP-1's own placement for stock, Restock+, Near Future, SSPXr...
  * Bluedog history (1241 parts): each Bluedog family is dated to its real program (Redstone 1953,
    Mercury 1959-63, Gemini 1964-66, Saturn 1961-73, Skylab 1973-79, Mariner 1962-71...) and each
    part goes into the matching RP-0 branch at that year.
  * Part type + old tier (1328 parts): branch from what the part is (engine by propellant, capsule,
    probe core, antenna, solar, RTG, reactor, science, heat shield, parachute, legs, wheels, wings,
    life support/ISRU, tanks...), era from how deep it was in your old tree.
  * Hidden/unresearchable parts are left alone.
- Part upgrades that pointed at old tree nodes are moved to the equivalent RP-0 node.
- Edit PartPlacement.cfg to move a part: change the node after TechRequired.
