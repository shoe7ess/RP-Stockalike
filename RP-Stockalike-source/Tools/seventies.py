# Fill RP-0's 1970s gap (it jumps 1972 -> 1976 -> 1981) with per-year nodes, and re-date a few existing nodes to the
# year their namesake actually flew, so every year 1970-1980 has research to do. Called from treelib and treebuild
# right after year_to_x() exists; new nodes then pick up parts through the normal year-based placement.
import kspcfg as K

# new node id: (year, branch neighbour it is cloned from, title, icon)
NEW = {
    'orbitalRocketry1974': (1974, 'orbitalRocketry1972', '1974 Orbital Rocketry', 'rp0_icon_RS27'),
    'orbitalRocketry1978': (1978, 'orbitalRocketry1976', '1978 Orbital Rocketry', 'rp0_icon_RD170'),
    'orbitalRocketry1980': (1980, 'orbitalRocketry1976', '1980 Orbital Rocketry', 'rp0_icon_RS27'),
    'solids1974': (1974, 'solids1972', '1974 Solid Rocketry', None),
    'solids1978': (1978, 'solids1976', '1978 Solid Rocketry', None),
    'hydrolox1975': (1975, 'hydrolox1969', '1975 Hydrolox Engines', 'rp0_icon_RL10'),
    'hydrolox1978': (1978, 'hydrolox1969', '1978 Hydrolox Engines', 'rp0_icon_SSME'),
    'stagedCombustion1974': (1974, 'stagedCombustion1969', '1974 Staged Combustion', 'rp0_icon_NK33'),
    'stagedCombustion1977': (1977, 'stagedCombustion1969', '1977 Staged Combustion', 'rp0_icon_RD0212'),
    'elecPropulsion1976': (1976, 'earlyElecPropulsion', '1976 Electric Propulsion', None),
    'orbitalStationModules': (1977, 'earlySpaceStations', 'Second-Generation Stations', 'rp0_icon_salyut1'),
    'stationResupply': (1979, 'earlySpaceStations', 'Station Resupply', 'rp0_icon_salyut1'),
    'lifeSupport1977': (1977, 'basicLifeSupport', 'Extended Life Support', 'rp0_icon_life_support'),
    'probeAutomationAvionics': (1976, 'advancedAvionics', 'Probe Automation', None),
    'outerPlanetScience': (1979, 'deepSpaceScience', 'Outer Planet Science', None),
    'improvedStationPower': (1977, 'spaceStationSolarPanels', 'Improved Station Power', None),
    'improvedRTG1975': (1975, 'improvedRTG', 'SNAP-19 Class RTGs', None),
}
# existing node -> year it really belongs to
REDATE = {
    'earlySpaceStations': 1973, 'spaceStationControl': 1973, 'basicLifeSupport': 1973, 'spaceStationSolarPanels': 1973,
    'advancedAvionics': 1974, 'advancedUncrewedLanding': 1975, 'deepSpaceComms': 1977, 'deepSpaceScience': 1977,
    'multihundredWattRTG': 1977, 'highDataRateComms': 1978, 'improvedCapsules': 1979,
    'materialsScienceSpaceplanes': 1979, 'electronicsSpaceplanes': 1980,
}
STATIONS = ('orbitalStationModules', 'stationResupply')
SOLAR = ('improvedStationPower',)
RTG = ('improvedRTG1975',)

def apply(nodes, tt, year_to_x):
    for k, yr in REDATE.items():
        if k not in nodes: continue
        x = year_to_x(yr); n = nodes[k]['node']
        y = n.get('pos').split(',')[1]
        n.set('pos', f'{int(round(x))},{y},-1'); nodes[k]['x'] = x
        d = n.get('description') or ''
        if '(' not in d: n.set('description', f'{d} ({yr})')
    for k, (yr, src, title, icon) in NEW.items():
        if k in nodes or src not in nodes: continue
        s = nodes[src]['node']; x = year_to_x(yr)
        n = K.Node('RDNode')
        n.items = [('v', 'id', k), ('v', 'title', title), ('v', 'description', f'{title} ({yr})'), ('v', 'cost', '1'),
                   ('v', 'hideEmpty', 'False'), ('v', 'nodeName', k), ('v', 'anyToUnlock', 'False'),
                   ('v', 'icon', ('RP-1/Tree/Icons/' + icon) if icon else s.get('icon')),
                   ('v', 'pos', f"{int(round(x))},{s.get('pos').split(',')[1]},-1"), ('v', 'scale', '0.6')]
        pn = K.Node('Parent'); pn.items = [('v', 'parentID', src), ('v', 'lineFrom', 'RIGHT'), ('v', 'lineTo', 'LEFT')]
        n.items.append(('n', pn))
        tt.items.append(('n', n))
        nodes[k] = dict(node=n, x=x, cost=nodes[src]['cost'])
