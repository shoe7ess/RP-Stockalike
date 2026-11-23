# RP-Stockalike

**A historically grounded career for stock-scale Kerbal Space Program 1.12.**
RP-Stockalike combines RP-0's tech tree with contracts from several historical spaceflight packs, and rebalances the result for the stock Kerbol system.
The aim is to play through the real space age at stock scale, without needing Realism Overhaul.

> ⚠️ **AI-generated content.** The configs, patches and tools in this mod were written by an AI assistant (Claude). shoe7ess directed and reviewed the work over many rounds and tested it in game. Please report problems as GitHub issues.

## Features

- **A custom tech tree on a real timeline.** The tree is RP-0's, laid out by year from 1945 to the 2050s and rescaled for stock science.
  - Every installed part goes in the year its real-world counterpart first flew.
  - You start with sounding rockets, then move through the V-2, Redstone, Mercury, Gemini and Apollo, and on to the Shuttle, the ISS and beyond.
  - Part mods the tree doesn't recognise are placed by part type and era.
- **Custom historical contracts.** These all live in one Contract Configurator group, `rp-contracts`, with duplicate missions removed. It merges:
  - RP-0/RP-1's career programs,
  - Career Evolution,
  - History of NASA,
  - Spacelines Progression.

  The real missions are adapted to Kerbol: the Moon becomes the Mun, Mars becomes Duna, and so on, with altitudes and orbits rescaled to match. Outer Planets Mod is supported.
- **Payouts balanced by era.** At the default 100% funds and science settings:
  - a contract's funds are based on what the mission costs to fly with the parts available at that point;
  - each era's science rewards are set by how much that era's tech nodes cost.

  The difficulty sliders scale everything from there.
- **A realistic start date.** The calendar starts in 1945. With *Show as Earth time* turned on, dates appear as real calendar dates such as "4 Oct 1957", so you can compare your progress with history. This only changes how dates are displayed, not the game clock.
- **Real satellites as payloads.** Satellite contracts count the mass of your actual probe hardware, so you don't need dummy payload parts.
- **Flexible science.** A contract that needs an experiment accepts any matching instrument you have installed: stock, DMagic, Bluedog Design Bureau, Station Science or SCANsat.

## Requirements
- Kerbal Space Program 1.12.x
- ModuleManager
- Contract Configurator

**Recommended:** Bluedog Design Bureau and Outer Planets Mod.

**Optional:** Tantares, ReStock, the Near Future mods, Procedural Parts, DMagic Orbital Science, SCANsat, Station Science, and a life support mod. These are picked up automatically when installed.

**Not compatible:**
- RP-0 / RP-1. RP-Stockalike switches itself off if either is installed.
- Rescaled solar systems (RSS, KSRSS, JNSQ).

## Installation
1. Copy the mod's folder from `GameData` into your KSP `GameData` folder.
2. Start a **new** career.
3. The `rp-contracts` group is on by default and replaces most stock contracts. You can switch it off under Difficulty Options → Contract Configurator.

## Feedback
Balancing is never perfect, so some eras or missions will probably pay too much or too little. Please open a GitHub issue with:
- the contract name;
- what the mission cost you and what it paid;
- your mod list.

Suggested refinement prompts are also welcome.

## Credits & license
RP-Stockalike is a free, non-commercial fan project by **shoe7ess**, released under **CC BY-NC-SA 4.0**. It builds on:
- RP-0/RP-1 contracts, tech tree layout and icons by the KSP-RO team
- Career Evolution by Pap & linuxgurugamer
- History of NASA by Dixiecapt (built on History of Spaceflight by Morphisor/Frylovespi and Historic Missions by hitecat106)
- Spacelines Progression by Gupyzer0

See `LICENSE.md` and `rp-contracts/LICENSE.md` for the full credits. If any original author would like their work removed or credited differently, please open an issue and it will be changed.

## Repository layout
- `GameData/RP-Stock/` - the mod as installed (copy this folder into your KSP `GameData`).
- `Source/RPStockCalendar/` - C# source for `RPStock.dll` (the 1945 calendar). Build with
  `dotnet build -p:KSPREF=<your KSP>/KSP_x64_Data/Managed`.
- `Tools/` - Python scripts that generated the tech tree and balance configs (see `Tools/README.md`).
