# RP-Stockalike build tools

Python 3 scripts used to generate the tech tree and contract balance configs in
`GameData/RP-Stock`. They are not needed to play; they're here so the generated configs can be
rebuilt or tweaked. Needs Python 3.8+ (`tree_poster.py` also needs Pillow, `tree_preview.py` matplotlib).

## Inputs
- **RP-1 source** - clone https://github.com/KSP-RO/RP-1 (the tree layout, node icons and
  contract programs come from it). Set `RP1=<clone>/GameData/RP-1`.
- **parts.json** - a dump of every installed part (name, title, mod, cost, category, tags) from
  your own GameData. Set `PARTS=<path>/parts.json`.
- **overrides.csv** - hand-reviewed placements (`part,node,reason`). These always win over the
  automatic year/type matching.

## Pipeline
```bash
export RP1=/path/to/RP-1/GameData/RP-1 PARTS=/path/to/parts.json
# 1. place every part by real-world year and build the tree
PRUNE=1 OVERRIDES=overrides.csv python3 treebuild.py "$RP1" "$PARTS" build_tree/TechTree
# 2. tidy the layout (one lane per branch, year columns) and set node science costs per era
python3 tree_polish.py build_tree/TechTree/RP0TechTree.cfg
# 3. contract science + funds per era (reads the converted contracts, writes Balance/*.cfg)
python3 contract_science.py <folder with Contracts/ and Spacelines/> build_tree/tree_polish.json build_balance
```
Copy `build_tree/TechTree/*` to `GameData/RP-Stock/TechTree` and `build_balance/*` to
`GameData/RP-Stock/Balance`.

## Script overview
| Script | Purpose |
|---|---|
| `kspcfg.py` | Minimal KSP ConfigNode parser/writer used by everything else |
| `treelib.py` | Shared tree helpers: branch detection, `pick(branch, year)` node lookup |
| `treebuild.py` | Places parts on the RP-0 tree by real-world year (family year table, analogues, overrides) and splits busy 1970s nodes by year |
| `seventies.py` | Extra 1970s nodes and re-dated nodes, applied by `treebuild.py` |
| `tree_polish.py` | Layout + science cost curve (1945: 5 sci ... 2051: 480 sci) |
| `start_cleanup.py` | Keeps only sounding-rocket hardware in the start node, moves the rest to its year |
| `contract_science.py` | Contract funds from estimated mission cost, science from each era's node costs (100% sliders, prestige/body multipliers cancelled) |
| `balance_stats.py` | Prints per-era totals to check the balance |
| `merge.py`, `fold_spacelines.py` | Merge Career Evolution / History of NASA / Spacelines into `rp-contracts`, removing duplicates and re-linking requirements |
| `analogue.py`, `stock_review.py`, `batch2_review.py`, `bluedog_review.py` | Helpers used while reviewing part placements (write review CSVs) |
| `tree_preview.py`, `tree_poster.py` | Quick preview and the high-res poster image of the tree |

The calendar plugin source is in `Source/RPStockCalendar` (build with
`dotnet build -p:KSPREF=<KSP>/KSP_x64_Data/Managed`).
