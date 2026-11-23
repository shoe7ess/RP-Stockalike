# RP-Stock
**A stock-scale "mashup" career for Kerbal Space Program 1.12: RP-0's tech tree and historical-spaceflight contracts, rebalanced for Kerbol.**

Author: **shoe7ess**. License: CC BY-NC-SA 4.0. This is a free, non-commercial project.

> ⚠️ **AI-GENERATED CONTENT.** This mod's configs, patches and tools were written by an AI assistant (Claude), directed and reviewed by shoe7ess over many rounds of refinement prompts, and tested in game by shoe7ess. Please judge it with that in mind, and report problems as GitHub issues.

## What it does
- **One tech tree for the whole space age.** RP-0's tech tree, laid out on a real timeline (1945–2050s) and rescaled for stock science. Every installed part is placed by when its real-world counterpart flew. You start with sounding rockets (WAC Corporal / Aerobee class), then the V-2, then Redstone, Mercury, Gemini, Apollo, and on through Shuttle, ISS and beyond. The 1970s are split year by year so research keeps pace with the contracts.
- **rp-contracts: one contract group from several historical packs.** RP-0/RP-1's career programs, Career Evolution, History of NASA and Spacelines Progression are merged into a single Contract Configurator group, converted to Kerbol (+ Outer Planets Mod), with duplicate missions removed.
- **Payouts balanced era by era.** At the default 100% funds and science sliders:
  - each contract's advance and reward come from the estimated cost of flying that mission with the installed parts;
  - each era's contracts pay science in proportion to what that era's tech nodes cost.
  The sliders scale everything from there.

- **The calendar starts in 1945.** A small plugin (`Plugins/RPStock.dll`, source in `Source/`) shows stock Year 1 as 1945, so the date matches the tree's first era. With **Show as Earth time** turned on (main menu Settings), dates appear as real calendar dates starting 1 Jan 1945, for example "4 Oct 1957", so they can be compared directly with the historical dates in contract descriptions. It only changes the date display; the game clock, orbits and contract timers are untouched. Change the start year in `Calendar.cfg`. The plugin stays out of the way if Kronometer or another calendar mod is installed.

## Dependencies
**Required**
- Kerbal Space Program 1.12.x
- ModuleManager
- Contract Configurator

**Strongly recommended**
- Bluedog Design Bureau. Much of the tree's history and many contract part/experiment options are built around it.
- Outer Planets Mod. Enables the Sarnus/Urlum/Neidon/Plock contracts. Without it, stock-body versions are used.

**Optional (picked up automatically when installed)**
- Science: DMagic Orbital Science, SCANsat, Station Science, Coatl Aerospace (Probes Plus)
- Parts placed on the timeline: Tantares, TantaresLV, TantaresSP, Taerobee, Wacapella + Completely Non-Aggressive Rocketry, ReStock / ReStock+, Near Future (Electrical, Solar, Propulsion, Spacecraft, Construction, Launch Vehicles, Aeronautics), Kerbal Atomics, Cryo Engines, Far Future Technologies, USI, Firespitter, Modular Launch Pads, and any other part mod (unknown parts are placed by type and era)
- Procedural Parts: adds Sounding/Payload tank types used by payload contracts
- Life support (one of): TAC Life Support, USI Life Support, Snacks, IFI, or Kerbalism. Station-resupply variants switch automatically.

**Not compatible**
- RP-0 / RP-1. RP-Stock switches itself off if either is installed.
- Rescaled systems: RSS, KSRSS, JNSQ, GPP. RP-Stock is built for stock scale.

## Install
Copy `GameData/RP-Stock` into your KSP `GameData` folder and start a **new** career. In Difficulty Options → Contract Configurator, the **rp-contracts** group is on and replaces most stock contract types. Turn it off there to go back to stock contracts.

## Feedback
Balancing is tricky. Some missions or eras will pay too much or too little. Please open a **GitHub issue** (not a forum or Reddit comment) with:
- the contract name;
- what you paid to fly it and what it paid you;
- your mod list, or a suggested refinement prompt if you have one.

## Credits & license
All included work is CC BY-NC-SA 4.0; see `LICENSE.md` and `rp-contracts/LICENSE.md` for full credits:
- RP-0/RP-1 contracts, tech tree layout and icons by the KSP-RO team
- Career Evolution by Pap & linuxgurugamer
- History of NASA by Dixiecapt (after History of Spaceflight and Historic Missions)
- Spacelines Progression by Gupyzer0

RP-Stock is a free, non-commercial fan project. If any original author would rather not be included, or would like the attribution changed, open an issue and it will be fixed or removed. shoe7ess's handle will also be removed on request.

---
# Technical notes
## rp-contracts (folder `rp-contracts/`)
One Contract Configurator group, **rp-contracts**, holding every career contract with no duplicate missions:
RP-0/RP-1's programs, plus Career Evolution, History of NASA and Spacelines Progression folded in as
sub-groups. Licenses and credits: `rp-contracts/LICENSE.md` (all CC BY-NC-SA 4.0). The packs as they were
before the merge are kept outside GameData in `Mod Staging/rp-contracts-sources`.
- Duplicate priority: RP-0, then History of NASA, then Spacelines, then Career Evolution.
- Spacelines contracts that only load on JNSQ/KSRSS/RSS were removed (this pack targets stock + OPM);
  13 Spacelines contracts that repeated an RP-0 mission were removed and anything requiring them re-linked.
- When a CE or NASA contract was the FIRST of a milestone RP-0 already has (first satellite,
  first EVA, Apollo 11, Mariner 2...), it was removed and RP-0's version (and reward) is used.
  Later historical missions (Apollo 12-17, Shuttle/ISS flights, Gemini durations...) stay.
- If CE and NASA overlapped, the History of NASA mission was kept.
- Anything that required a removed contract now requires its replacement instead.
- History of NASA was converted from Real Solar System to Kerbol (Moon -> Mun, Mars -> Duna,
  Venus -> Eve, ...; altitudes, speeds and downrange distances scaled to Kerbin).
  Several of its missions required flights that were never in the pack (e.g. Artemis needed
  STS-135); they now follow the previous flight that does exist.
- CE and NASA keep their own rewards (both already scale to your home planet's size).
See merge_report.txt for every removal and re-link.

The career contracts from Realistic Progression One (RP-0/RP-1, by the KSP-RO team),
converted to run on plain Contract Configurator in a stock-scale solar system with
Outer Planets Mod. RP-0 itself is NOT required (and this pack disables itself if RP-0 is installed).

## Requires
- Contract Configurator
- ModuleManager
- Outer Planets Mod (for Sarnus/Urlum/Neidon/Plock contracts; the rest work without it)
- Procedural Parts (optional) - adds "Payload" tank types as a dummy payload

## How it maps
- Earth -> Kerbin, Moon -> Mun, Mars -> Duna (Phobos -> Ike), Venus -> Eve, Mercury -> Moho,
  Ceres -> Dres, Vesta -> Gilly, Jupiter -> Jool (Io/Europa/Ganymede/Callisto -> Laythe/Vall/Tylo/Bop),
  Saturn -> Sarnus (Titan/Rhea/Iapetus/Dione/Enceladus -> Tekto/Slate/Eeloo/Ovok/Hale),
  Uranus -> Urlum (Titania/Oberon/Ariel/Umbriel -> Wal/Tal/Polta/Priax), Neptune -> Neidon (Triton -> Thatmo),
  Pluto -> Plock (Charon -> Karen). Deimos, Mimas, Tethys and Miranda contracts are removed.
- Altitudes: up to 100 km x0.7 (Karman line -> 70 km); above that, scaled so GEO lands on Kerbin's
  2,863 km synchronous orbit. Orbital periods x0.25 (Kerbin's day). Other bodies scale by radius.
- RP-0 "programs" become contract prerequisites: a program's contracts unlock once the
  contracts that RP-0 requires to start that program are complete.
- Rewards are fixed numbers on stock's scale (see reward_table.csv for every contract).
  They start from RP-0's real money for each contract (a required contract's share of its
  program's funding; optional work = the Confidence it earns x the program's $/Confidence,
  capped at half a typical required contract) and compress it onto stock's scale with
  funds = RP0^0.88. Examples: Karman line 7.3k, first satellite 34k, Mun flyby 46k,
  Mun landing 96k, Duna orbit 120k, crewed Mun landing ~0.7-1M.
  (Superseded: rewards are now set by RP-Stock/Balance - see the Balance section.)
  Science reward is small and finite: ~1-2 for sounding rockets, 4-5 for the first satellites,
  ~11 for an uncrewed Mun landing, ~50-70 for crewed Mun landings, ~140 for crewed Duna.
- Science: each RP-0 instrument becomes a choice. The contract accepts ANY installed experiment of
  the same kind that works in the required situation - stock is always one option, and
  DMagic Orbital Science, Bluedog Design Bureau, Station Science and SCANsat experiments are added
  automatically when those mods are installed. Examples: magnetometer -> Thermometer, DMagic
  Magnetometer, BDB magScan; radiation -> Goo, BDB Geiger/cosmic-ray/trapped-radiation/gamma,
  DMagic solar particles; imaging -> BDB cameras/scopes, DMagic imaging platform & telescope,
  SCANsat visual/altimetry; materials -> Materials Bay, Station Science fuel & kuarq experiments.
  See conversion_report.txt for the full list per contract.
- Skopos commercial contracts are not included (they need Skopos/RealAntennas ground stations).

## Payloads
Satellite and sounding contracts ask for payload units (ComSat, NavSat, WeatherSat, Research,
Sounding). Your real satellite IS the payload: every uncrewed probe core, antenna, solar panel,
battery and science instrument carries payload units equal to its mass (1 unit per kg;
WeatherSat 1.25/kg, Sounding 2/kg). Contract amounts are RP-0's divided by 4 for kerbal-sized
hardware, so the first comsat wants 20 units (about a 20 kg satellite) and the biggest
early comsats about 75-125 kg.
Crewed parts, fuel tanks and engines never count. If you'd rather fly a dummy mass, set a
Procedural Parts tank to one of the Payload tank types.

## License
CC BY-NC-SA 4.0, same as RP-0 (see LICENSE.md). Original contracts by the RP-0/RP-1 contributors:
https://github.com/KSP-RO/RP-1


## Folder layout (RP-Stock)
- Contracts/, Agencies/, HistoryofNASA/ - RP-0 contracts converted to stock Kerbol + OPM, merged with Career Evolution and History of NASA.
- Resources/, Patches/PayloadTanks.cfg, Patches/SatellitePayloads.cfg - payload resources for the contracts.
- TechTree/ - RP-0 tree layout scaled to ~55k science; PartPlacement.cfg places every installed part by real-world date
  (overrides.csv = hand-reviewed placements, part_placement.csv = full list).
Everything is disabled automatically if real RP-0/RP-1 is installed.


## Choosing what you play (Contract Configurator settings)
Each pack is its own top-level contract group, so it can be switched on/off per save in the
Contract Configurator difficulty settings (new game > Difficulty Options, or the CC settings in an existing save):
- RP-Stock: RP-0 Programs
- RP-Stock: Career Evolution
- RP-Stock: History of NASA
- RP-Stock: Spacelines Progression (Spacelines/ - missions RP-Stock already has were dropped, RP-0 keeps priority)
Stock contract types (part tests, flag planting, rescue, science, satellite, station, base, asteroid, grand tour,
tourism, exploration) start disabled and can be turned back on in CC's "Stock Contracts" settings page.
Survey and ISRU contracts stay enabled by default.

## Tech tree
Nodes that would hold no parts with the installed mods are pruned (TechTree/removed_nodes.txt); their children
are re-attached to the removed node's parents. Per-node science costs are unchanged.

## Balance (folder `Balance/`)
Balanced for the 100% science and 100% funds sliders; the sliders scale everything from there.
- `ContractFunds.cfg`: advance 35% / completion 165% (one-off) or 125% (repeatable) of the estimated
  cost of flying the mission with the installed parts; failure costs the advance. `contract_funds.csv` lists every estimate.
- `ContractScience.cfg`: contracts in each era pay ~40% of what that era's tech nodes cost, split by difficulty.
- Both cancel KSP's prestige and per-body reward weighting, so the number in the file is the number paid.
