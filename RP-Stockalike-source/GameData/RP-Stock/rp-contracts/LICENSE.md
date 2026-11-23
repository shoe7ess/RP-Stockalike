# rp-contracts: license and credits

**rp-contracts** is the single Contract Configurator group inside the RP-Stock mod. It merges
four contract packs into one stock-scale (Kerbol + Outer Planets Mod) career with no duplicate
missions. Every pack it draws on is licensed under **Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**, so this combined
work is released under the same license.

- License summary: https://creativecommons.org/licenses/by-nc-sa/4.0/
- Full legal text: `LICENSE-CC-BY-NC-SA-4.0.txt` in this folder.

You may share and adapt this pack for **non-commercial** purposes. You must give credit to the
authors below, note that changes were made, and release your changes under CC BY-NC-SA 4.0.

## Included works

| Part of rp-contracts | Original work | Authors | License | Source |
|---|---|---|---|---|
| The program folders (Sounding Rockets, X-Plane Research, Earth Crewed, Lunar, Mars, Outer Planets, etc.) and `Groups.cfg` | RP-0 / RP-1 career contracts (Realistic Progression One) | The KSP-RO team and RP-0/RP-1 contributors | CC BY-NC-SA 4.0 | https://github.com/KSP-RO/RP-1 (contributors: https://github.com/KSP-RO/RP-1/graphs/contributors) |
| `CareerEvolution/` | Career Evolution Contract Pack | Pap, maintained by linuxgurugamer | CC BY-NC-SA 4.0 | https://spacedock.info/mod/1418 |
| `HistoryofNASA/` and `../HistoryofNASA/Logo` | History of NASA (1946–2036) Contract Pack | Dixiecapt. Based on Contract Pack: History of Spaceflight (Morphisor / Frylovespi, CC BY-NC-SA 4.0) and Contract Pack: Historic Missions (hitecat106) | CC BY-NC-SA 4.0, inherited from History of Spaceflight | https://forum.kerbalspaceprogram.com/topic/229235-contract-pack-history-of-nasa-1946-2036/ and https://spacedock.info/mod/1812 |
| `Spacelines/` | Spacelines Progression | Gupyzer0 | CC BY-NC-SA 4.0 (stated in its README) | https://github.com/Gupyzer0/Spacelines-Progression |

Contract Configurator (by nightingale, now maintained by the community) is a separate
dependency. It is not included here.

## Changes made (as required by the license)

- RP-0/RP-1 contracts were converted from Real Solar System to stock Kerbol + Outer Planets Mod.
  Bodies were renamed, altitudes and periods rescaled, and RP-1-only systems were removed: Programs,
  Confidence, KCT/training notes, RealAntennas and Skopos contracts. They also run without RP-1 installed.
- History of NASA was converted from Real Solar System / Sol to Kerbol. Its broken requirement
  chains were re-linked.
- All four packs were merged under one group with no duplicate missions. When two packs had the
  same mission, one copy was kept, in this order of priority: RP-0 first, then History of NASA,
  then Spacelines, then Career Evolution. Contracts that required a removed duplicate now require
  the copy that was kept.
- Spacelines contracts that only load on JNSQ, KSRSS or RSS were removed, because this pack targets
  stock and OPM. The originals are kept outside GameData in `Mod Staging/rp-contracts-sources`.
- Rewards were re-based for RP-Stock: funds come from estimated mission cost, and science from the
  tech tree's cost per era. These live in `RP-Stock/Balance/ContractFunds.cfg` and `ContractScience.cfg`.
- Text that referred to RP-1-only mechanics was removed or rewritten.

## Attribution line for redistribution

> rp-contracts (part of RP-Stock) — contracts from RP-0/RP-1 (KSP-RO team), Career Evolution
> (Pap, linuxgurugamer), History of NASA (Dixiecapt; after History of Spaceflight by Morphisor and
> Historic Missions by hitecat106) and Spacelines Progression (Gupyzer0), converted and merged.
> CC BY-NC-SA 4.0.
