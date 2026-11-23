# Build a "kerbal RP-0" tech tree: RP-0's node layout + every installed part placed on it.
import sys, os, re, json, collections, shutil, math
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K

RP1 = sys.argv[1]            # .../GameData/RP-1
PARTS = sys.argv[2]          # parts.json from the user's PC
OUT = sys.argv[3]            # output folder (becomes GameData/RP-Stock/TechTree)
TARGET_TOTAL = 55000.0
MOD = 'RP-Stock/TechTree'

# ------------------------------------------------------------------ RP-0 nodes
tree = K.parse(open(os.path.join(RP1, 'Tree', 'RP0TechTree.cfg'), encoding='utf-8-sig').read())
tt = tree.nodes()[0]
nodes = {}
for n in tt.nodes('RDNode'):
    x, y = [float(v) for v in n.get('pos').split(',')[:2]]
    nodes[n.get('id')] = dict(node=n, x=x, cost=float(n.get('cost')))
raw_total = sum(v['cost'] for k, v in nodes.items() if k not in ('unlockParts', 'orphanParts', 'ORPHANS'))
SCALE = TARGET_TOTAL / raw_total

# year <-> x from the dated rocketry nodes
anchors = sorted((int(m.group(1)), v['x']) for k, v in nodes.items() for m in [re.fullmatch(r'orbitalRocketry(\d{4})', k)] if m)
anchors = [(1945, nodes['start']['x']), (1949, nodes['rocketryTesting']['x']), (1951, nodes['earlyRocketry']['x']),
           (1954, nodes['basicRocketryRP0']['x'])] + anchors + [(2051, nodes['colonization2051Flight']['x'])]
def year_to_x(y):
    for (y0, x0), (y1, x1) in zip(anchors, anchors[1:]):
        if y <= y1: return x0 + (x1 - x0) * max(0, (y - y0)) / max(1, (y1 - y0))
    return anchors[-1][1] + (y - anchors[-1][0]) * 8
import seventies
seventies.apply(nodes, tt, year_to_x)

B = collections.OrderedDict()
def branch(name, pred): B[name] = [k for k in nodes if pred(k)]
ids = list(nodes)
col = lambda k, *s: k.startswith('colonization') and any(k.endswith(x) for x in s)
branch('flight', lambda k: k in ('supersonicDev', 'supersonicFlightRP0', 'matureSupersonic', 'highSpeedFlight', 'advancedJetEngines', 'efficientSupersonic', 'matureTurbofans', 'refinedTurbofans', 'scramjetEngines', 'advancedTurbofans', 'experimentalAircraft') or col(k, 'Flight'))
branch('spaceplanes', lambda k: k in ('hypersonicFlightRP0', 'prototypeSpaceplanes', 'effectiveSpaceplanes', 'spaceShuttles', 'improvedSpaceplanes', 'advancedSpaceplanes', 'highTechSpaceplanes', 'commercialSpaceplanes', 'experimentalSpaceplanes', 'sstoSpaceplanes') or col(k, 'Spaceplanes'))
branch('capsules', lambda k: k.endswith('Capsules') and 'materials' not in k and 'electronics' not in k and 'science' not in k or k == 'capsulesNF' or col(k, 'Command'))
branch('stations', lambda k: k in seventies.STATIONS or k in ('spaceStationPrototypes', 'spaceStationDev', 'earlySpaceStations', 'modularSpaceStations', 'largeScaleOrbitalCon', 'improvedOrbitalConstruction', 'inflatableHabitats', 'improvedHabitats', 'advancedHabitats', 'largeScaleHabitats') or col(k, 'SpaceStations'))
branch('control', lambda k: k in ('earlyFlightControl', 'stabilityRP0', 'improvedFlightControl', 'spaceStationControl', 'largeSpaceplaneControl', 'largeStationControl', 'gridFins', 'reusableControl', 'flightControlNF') or col(k, 'Control'))
branch('docking', lambda k: k in ('earlyDocking', 'dockingCrewTransfer', 'standardDockingPorts', 'largeDockingPorts'))
branch('edl', lambda k: k in ('entryDescentLanding', 'humanRatedEDL', 'lunarRatedHeatshields', 'SIAD', 'HIAD') or col(k, 'EDL'))
branch('landing', lambda k: k in ('earlyLanding', 'lunarLanding', 'improvedLandingEngines', 'advancedUncrewedLanding', 'reusability', 'advancedLanding'))
branch('rovers', lambda k: k in ('interplanetaryRovers', 'largeRoverDesigns'))
branch('hydrolox', lambda k: 'ydrolox' in k)
branch('rocketry', lambda k: k in ('rocketryTesting', 'earlyRocketry', 'basicRocketryRP0') or k.startswith('orbitalRocketry') or col(k, 'Orbital'))
branch('staged', lambda k: k.startswith('firstStaged') or k.startswith('stagedCombustion') or col(k, 'Staged') or k.startswith('FRSC') or k == 'prototypeFRSC')
branch('solids', lambda k: k in ('earlySolids', 'basicSolids') or k.startswith('solids') or col(k, 'Solid'))
branch('elec', lambda k: 'lecProp' in k)
branch('nuclearProp', lambda k: 'uclearProp' in k)
branch('lifesupport', lambda k: k == 'crewSurvivability' or 'ifeSupport' in k)
branch('materials', lambda k: k == 'postWarMaterialsScience' or k.startswith('earlyMaterials') or k.startswith('materialsScience'))
branch('electronics', lambda k: k.startswith('electronics'))
branch('rtg', lambda k: k in seventies.RTG or k in ('firstRTG', 'earlyRTG', 'improvedRTG', 'multihundredWattRTG', 'gphsRTG'))
branch('fission', lambda k: k in ('nuclearFissionReactors', 'improvedNuclearPower', 'advancedNuclearPower', 'modernNuclearPower', 'advModernNuclearPower', 'nuclearPowerNF') or col(k, 'NuclearPower'))
branch('solar', lambda k: k in seventies.SOLAR or k in ('primitiveSolarPanels', 'earlyPower', 'basicPower', 'improvedPower', 'lunarRatedPower', 'spaceStationSolarPanels', 'maturePower', 'largeScaleSolarArrays', 'advancedPower', 'modernPower', 'advModernPower', 'powerNF') or col(k, 'Power') and 'Nuclear' not in k)
branch('comms', lambda k: k.endswith('Comms') or k == 'commsNF')
branch('avionics', lambda k: k.endswith('Avionics') or k in ('avionicsPrototypes', 'interplanetaryProbes', 'avionicsNF'))
branch('science', lambda k: k.endswith('Science') and not k.startswith('materials') and 'MaterialsScience' not in k or k in ('scienceSatellite', 'scienceHuman', 'scienceAdvCapsules', 'scienceLunar', 'scienceExploration', 'scienceNF'))
for b in B: B[b].sort(key=lambda k: nodes[k]['x'])

SPECIAL_IDS = ('unlockParts', 'orphanParts', 'ORPHANS')
def x_to_year_local(x):
    for (y0, x0), (y1, x1) in zip(anchors, anchors[1:]):
        if x <= x1: return y0 + (y1 - y0) * (x - x0) / max(1, (x1 - x0))
    return 2051
def node_branch(node):
    return next((b for b, lst in B.items() if node in lst), None)
def pick(br, year):
    x = year_to_x(year); cand = B[br]
    best = None
    for k in cand:
        if nodes[k]['x'] <= x + 1: best = k
    return best or cand[0]

# ------------------------------------------------------------------ old tree tiers -> year
data = json.load(open(PARTS))
P = data['parts']
oldcost = {}
for tree_name in ('Squad', 'CommunityTechTree', 'zzGPTT'):
    for k, v in data['trees'].get(tree_name, {}).items():
        try: oldcost.setdefault(k, float(v['cost']))
        except: pass
COST_YEAR = [(0, 1945), (5, 1950), (18, 1954), (45, 1957), (90, 1960), (160, 1963), (300, 1967), (550, 1972),
             (1000, 1980), (1500, 1990), (2250, 2000), (3000, 2010), (4000, 2020), (6000, 2035), (10000, 2051)]
def cost_year(c):
    if c is None: return 1965
    for (c0, y0), (c1, y1) in zip(COST_YEAR, COST_YEAR[1:]):
        if c <= c1: return y0 + (y1 - y0) * (c - c0) / (c1 - c0)
    return 2060

# Bluedog families: (first year, last year)
BDB = {'Able': (1958, 1960), 'Agena': (1959, 1968), 'Apollo': (1966, 1975), 'Atlas': (1957, 1966), 'AtlasV': (2002, 2020),
       'Centaur': (1962, 1980), 'Delta': (1960, 1990), 'Gemini': (1964, 1966), 'Hexagon': (1971, 1986), 'Jupiter': (1957, 1958),
       'LDC': (1968, 1972), 'MOL': (1966, 1969), 'Mercury': (1959, 1963), 'Redstone': (1953, 1961), 'Saturn': (1961, 1973),
       'Skylab': (1973, 1979), 'Thor': (1957, 1970), 'Titan': (1959, 1997), 'Vanguard': (1957, 1959), 'Vega': (1959, 1960),
       'X15': (1959, 1968), 'Timberwind': (1990, 1995), 'APAS': (1975, 1995),
       'AIMP': (1966, 1973), 'Alouette': (1962, 1965), 'Biosat': (1966, 1969), 'Clementine': (1994, 1994), 'EarlyComsats': (1960, 1964),
       'Explorer': (1958, 1962), 'Helios': (1974, 1976), 'Hughes': (1963, 1970), 'IDCSP': (1966, 1968), 'IonThrusters': (1970, 1998),
       'JunoProbes': (1958, 1959), 'Kepler': (2009, 2009), 'LunarOrbiter': (1966, 1967), 'Mariner': (1962, 1971), 'Mariner10': (1973, 1973),
       'Nimbus': (1964, 1978), 'OAO': (1966, 1972), 'OFO': (1970, 1970), 'OGO': (1964, 1969), 'OSO': (1962, 1975), 'OV1': (1965, 1971),
       'Pioneer': (1958, 1978), 'Pioneer6': (1965, 1969), 'PioneerAble': (1959, 1960), 'RTGs': (1961, 1977), 'Ranger': (1961, 1965),
       'SolarBattery': (1958, 1958), 'Surveyor': (1966, 1968), 'TIROS': (1960, 1965), 'Transit': (1960, 1988), 'Viking': (1975, 1976),
       'VoyagerMars': (1966, 1969), 'YoYoDespin': (1959, 1959)}

def bdb_family(p):
    f = p['file'].split('/')
    for i, seg in enumerate(f):
        if seg in ('Parts', 'OldParts') and i + 1 < len(f):
            fam = f[i + 1]
            if fam == 'ProbeExpansion' and i + 2 < len(f): fam = f[i + 2]
            return fam
    return None

# ------------------------------------------------------------------ part type -> branch
def has(p, *names): return any(any(m == n or (n.endswith('*') and m.startswith(n[:-1])) for n in names) for m in p['mods'] if m)
def classify(n, p):
    props = set(x for x in p['props'] if x); res = set(x for x in p['res'] if x)
    crew = int(float(p['crew'] or 0)) if (p['crew'] or '0').replace('.', '').isdigit() else 0
    low = (n + ' ' + (p['title'] or '')).lower()
    if has(p, 'ModuleEngines*', 'ModuleEnginesFX', 'ModuleEnginesRF', 'MultiModeEngine'):
        if 'IntakeAir' in props or 'IntakeAtm' in props: return 'flight'
        if props & {'XenonGas', 'ArgonGas', 'Lithium', 'LqdArgon', 'ElectricCharge'} and not props & {'Oxidizer', 'LqdOxygen'}: return 'elec'
        if 'SolidFuel' in props: return 'solids'
        if 'LqdHydrogen' in props and props & {'Oxidizer', 'LqdOxygen'}: return 'hydrolox'
        if ('nuclear' in low or 'ntr' in low or 'nerv' in low) or (props == {'LiquidFuel'} or props == {'LqdHydrogen'}): return 'nuclearProp'
        if props == {'MonoPropellant'}: return 'control'
        return 'rocketry'
    if has(p, 'ModuleCommand'):
        if crew > 0: return 'spaceplanes' if ('cockpit' in low or p['cat'] == 'Aero') else 'capsules'
        return 'avionics'
    if has(p, 'ModuleRCS*'): return 'control'
    if has(p, 'ModuleDockingNode'): return 'docking'
    if has(p, 'ModuleScienceLab', 'StationScienceModule'): return 'science'
    if has(p, 'ModuleScienceExperiment', 'DMModuleScience*', 'DMSeismic*', 'StationExperiment', 'SampleAnalyzer', 'SCANsat', 'ModuleSCAN*', 'ModuleGroundExperiment', 'ModuleGroundSciencePart', 'ModuleOrbitalSurveyor'): return 'science'
    if has(p, 'ModuleDataTransmitter', 'ModuleRTAntenna*', 'ModuleRealAntenna'): return 'comms'
    if has(p, 'ModuleDeployableSolarPanel', 'ModuleCurvedSolarPanel', 'ModuleROSolar'): return 'solar'
    if has(p, 'FissionReactor', 'ModuleSystemHeatFissionReactor', 'FissionGenerator') or 'reactor' in low: return 'fission'
    if has(p, 'ModuleGenerator') and ('rtg' in low or 'radioisotope' in low or 'thermoelectric' in low): return 'rtg'
    if has(p, 'ModuleAblator') or 'heatshield' in low or 'heat shield' in low: return 'edl'
    if has(p, 'ModuleParachute', 'RealChuteModule', 'ModuleRealChute'): return 'edl'
    if has(p, 'ModuleWheelBase'):
        return 'landing' if ('leg' in low or 'lander' in low) else 'rovers'
    if has(p, 'ModuleLiftingSurface', 'ModuleControlSurface', 'ModuleResourceIntake', 'FARControllableSurface') or p['cat'] == 'Aero': return 'flight'
    if has(p, 'ModuleReactionWheel', 'ModuleSAS'): return 'control'
    if has(p, 'ModuleResourceHarvester', 'ModuleResourceConverter', 'ModuleAsteroidDrill', 'USI_*', 'ModuleLifeSupport*', 'ModuleHabitation', 'USILS_*', 'MKS*', 'WOLF*') or res & {'Supplies', 'Mulch', 'Food', 'Water', 'Oxygen'}: return 'lifesupport'
    if crew > 0: return 'stations'
    if res & {'LqdHydrogen'} and res & {'Oxidizer', 'LqdOxygen'}: return 'hydrolox'
    if res & {'XenonGas', 'ArgonGas', 'Lithium'}: return 'elec'
    if res & {'LiquidFuel', 'Oxidizer', 'SolidFuel'}: return 'rocketry'
    if res & {'MonoPropellant'}: return 'control'
    if res == {'ElectricCharge'} or 'battery' in low: return 'electronics'
    if has(p, 'ModuleRobotic*', 'ModuleRoboticServo*', 'ModuleRoboticRotationServo', 'ModuleRoboticServoHinge', 'ModuleRoboticServoPiston', 'ModuleRoboticServoRotor', 'MuMechToggle', 'ModuleIRServo*'): return 'electronics'
    if has(p, 'ModuleLight', 'ModuleColorChanger', 'ModuleKerbNetAccess'): return 'electronics'
    return 'materials'

# ------------------------------------------------------------------ RP-1 database
db = {}
t = open(os.path.join(RP1, 'Tree', 'TREE-Parts.cfg'), encoding='utf-8-sig').read()
for m in re.finditer(r'@PART\[([^\]]+)\][^\n]*\n\{(.*?)\n\}', t, re.S):
    tr = re.search(r'%TechRequired = (\S+)', m.group(2))
    if tr: db[m.group(1).replace('_', '.')] = tr.group(1)

# ------------------------------------------------------------------ place every part
placed = {}; how = collections.Counter(); per_node = collections.Counter(); detail = []; pyear = {}
OVR = {}
ovr_path = os.environ.get('OVERRIDES')
if ovr_path and os.path.exists(ovr_path):
    import csv as _csv
    for r in _csv.DictReader(open(ovr_path)): OVR[r['part']] = (r['node'], r['reason'])
# launcher / spacecraft families with a known first-flight year (TantaresLV etc.)
FAMILY_YEAR = [(r'hydra\.lv|proton\.v2', 1967), (r'libra\.lv', 1969), (r'berehynia\.lv', 1977), (r'rotanev', 1987),
               (r'blok\.d', 1967), (r'tantares\.lv', 1966), (r'chara\.lv', 1967), (r'aquila', 1977), (r'mira', 1986)]
fam_parts = collections.defaultdict(list)
for n, p in P.items():
    if p['mod'] == 'Bluedog_DB':
        fam = bdb_family(p)
        if fam in BDB: fam_parts[fam].append(n)
fam_year = {}
for fam, lst in fam_parts.items():
    y0, y1 = BDB[fam]
    lst.sort(key=lambda n: (oldcost.get(P[n]['tech'] or '', 0), n))
    for i, n in enumerate(lst):
        fam_year[n] = y0 + (y1 - y0) * (i / max(1, len(lst) - 1))
for n, p in P.items():
    old = p['tech']
    if old in ('HIDDEN', 'Unresearcheable', 'Unresearchable', None) or (old and old.lower() in ('hidden', 'unresearcheable')):
        how['left hidden/unresearchable'] += 1; continue
    br = classify(n, p)
    if n in OVR and OVR[n][0] in nodes:
        node, src = OVR[n][0], 'matched: ' + OVR[n][1]
        # 1970s: the override's own reason usually names the real year; re-pick inside the same branch so the
        # per-year 1970s nodes (seventies.py) get the parts that belong to them
        ys = [int(y) for y in re.findall(r'\b(19[6-8]\d)\b', OVR[n][1])]
        obr = node_branch(node)
        if ys: pyear[n] = ys[-1]
        if ys and 1970 <= ys[-1] <= 1981 and obr and node != 'start':
            node = pick(obr, ys[-1]); src += ' [re-picked by year]'
    elif n in db and db[n] in nodes and db[n] not in ('orphanParts', 'ORPHANS'):
        node = 'start' if db[n] == 'unlockParts' else db[n]; src = 'RP-1 database'
    else:
        if n in fam_year: year, src = fam_year[n], 'Bluedog history'; pyear[n] = year
        else:
            year, src = cost_year(oldcost.get(old)), 'part type + old tier'
            fy = next((y for rx, y in FAMILY_YEAR if re.match(rx, n)), None)
            if fy: year, src = fy, 'family year'; pyear[n] = fy
        node = 'start' if year <= 1946 else pick(br, year)
        if old == 'start' and n not in fam_year: node = 'start'
    placed[n] = node; how[src] += 1; per_node[node] += 1
    detail.append((p['mod'], n, p['title'] or '', old or '', br, node, src))

# ------------------------------------------------------------------ split broad 1970s nodes into per-year nodes
# RP-0 lumps 1972-1980 into single nodes; break each into up to four dated nodes and hand out its parts by their
# known year, or (no year known) by price order, cheapest first.
import json as _json
PCOST = {k: float(v.get('cost') or 0) for k, v in _json.load(open(os.path.join(os.path.dirname(PARTS), '..', 'part_costs.json'))).items()} \
    if os.path.exists(os.path.join(os.path.dirname(PARTS), '..', 'part_costs.json')) else {}
SPLIT_MIN_PARTS = 12
split_made = {}; _phase = 0
for k in list(nodes):
    if k in ('start',) or k in SPECIAL_IDS: continue
    d = nodes[k]['node'].get('description') or ''
    m = re.search(r'\((19\d\d)-(19\d\d)\)', d) or re.match(r'(19\d\d)-(19\d\d)', d)
    if not m: continue
    y0, y1 = int(m.group(1)), int(m.group(2))
    if not (y0 <= 1979 and y1 >= 1972 and y1 - y0 >= 3): continue
    mine = [n for n, nd in placed.items() if nd == k]
    if len(mine) < SPLIT_MIN_PARTS: continue
    y0 = max(y0, 1970); y1 = min(y1, 1981)
    chunks = max(2, min(3, len(mine) // 6))
    first = max(y0, round(x_to_year_local(nodes[k]['x'])))
    ph = _phase % 3; _phase += 1     # stagger nodes so the new ones land on different years
    years = [first] + [min(y1, max(first + 1, round(first + (y1 - first) * i / (chunks - 1)) - ph)) for i in range(1, chunks)]
    years = sorted(set(years))
    if len(years) < 2: continue
    ids = [k] + [f'{k}Y{y}' for y in years[1:]]
    src = nodes[k]['node']
    for nid, y in zip(ids[1:], years[1:]):
        nn = K.Node('RDNode')
        title = f"{src.get('title')} ({y})"
        nn.items = [('v', 'id', nid), ('v', 'title', title), ('v', 'description', f"{src.get('title')}, {y} developments"),
                    ('v', 'cost', '1'), ('v', 'hideEmpty', 'False'), ('v', 'nodeName', nid), ('v', 'anyToUnlock', 'False'),
                    ('v', 'icon', src.get('icon')), ('v', 'pos', f"{int(round(year_to_x(y)))},{src.get('pos').split(',')[1]},-1"), ('v', 'scale', '0.6')]
        pn = K.Node('Parent'); pn.items = [('v', 'parentID', k), ('v', 'lineFrom', 'RIGHT'), ('v', 'lineTo', 'LEFT')]
        nn.items.append(('n', pn)); tt.items.append(('n', nn))
        nodes[nid] = dict(node=nn, x=year_to_x(y), cost=nodes[k]['cost'])
    known = sorted([n for n in mine if n in pyear], key=lambda n: pyear[n])
    unknown = sorted([n for n in mine if n not in pyear], key=lambda n: (PCOST.get(n, 0), n))
    for n in known:
        idx = max(i for i, y in enumerate(years) if y <= max(years[0], pyear[n]))
        placed[n] = ids[idx]
    for i, n in enumerate(unknown):
        placed[n] = ids[min(len(ids) - 1, i * len(ids) // max(1, len(unknown)))]
    split_made[k] = list(zip(ids, years))
per_node = collections.Counter(placed.values())
detail = [(a, n, t, o, b, placed.get(n, nd), sr + (' [1970s split]' if placed.get(n, nd) != nd else '')) for (a, n, t, o, b, nd, sr) in detail]
open(os.path.join(OUT if False else os.path.dirname(OUT) or '.', 'split_nodes.json'), 'w').write(_json.dumps(split_made, indent=1))

# ------------------------------------------------------------------ PARTUPGRADE / generic old-node remap
OLD_BRANCH = [(r'rocketry|propulsion|fuel|engine', 'rocketry'), (r'nuclear', 'nuclearProp'), (r'ion', 'elec'),
              (r'electric|power|solar', 'solar'), (r'science|exploration|survey', 'science'), (r'unmanned|automation|avionic|probe', 'avionics'),
              (r'command|crew|survivab', 'capsules'), (r'control|stability|flight', 'control'), (r'aero|aviation|supersonic|hypersonic|altitude', 'flight'),
              (r'landing', 'landing'), (r'comm|antenna|telemetr', 'comms'), (r'construct|metal|composite|material|structur|nano|engineering', 'materials')]
def remap_old(old):
    if old == 'start': return 'start'
    br = next((b for rx, b in OLD_BRANCH if re.search(rx, old, re.I)), 'materials')
    y = cost_year(oldcost.get(old))
    return 'start' if y <= 1946 else pick(br, y)

# ------------------------------------------------------------------ write
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'Icons'))
for f in os.listdir(os.path.join(RP1, 'Tree', 'Icons')):
    shutil.copy(os.path.join(RP1, 'Tree', 'Icons', f), os.path.join(OUT, 'Icons', f))
tt.name = '@TechTree:FOR[ZZZZZ-RP-Stock]:NEEDS[!RP-0,!RP-1]'
# ---- prune nodes that hold no parts: children inherit the removed node's parents
SPECIAL = ('unlockParts', 'orphanParts', 'ORPHANS')
remap_targets = {}
for o in sorted({p['tech'] for p in P.values() if p['tech']} | set(oldcost)):
    if o in nodes or o.lower() in ('hidden', 'unresearcheable', 'unresearchable'): continue
    remap_targets[o] = remap_old(o)
PRUNE = os.environ.get('PRUNE') == '1'
removed = set()
if PRUNE:
    removed = {k for k in nodes if k != 'start' and k not in SPECIAL and per_node[k] == 0}
def parents_of(nid):
    return [x for x in nodes[nid]['node'].nodes('Parent') if x.get('parentID') not in SPECIAL]
def live_parents(nid, seen=None):
    seen = seen or set(); out = []
    for pr in parents_of(nid):
        pid = pr.get('parentID')
        if pid in seen: continue
        seen.add(pid)
        if pid in removed: out += live_parents(pid, seen)
        else: out.append(pr)
    return out
def live_node(nid):
    # nearest surviving ancestor for things pointing at a removed node
    while nid in removed:
        ps = parents_of(nid)
        nid = ps[0].get('parentID') if ps else 'start'
    return nid
if PRUNE:
    for k in nodes:
        if k in removed or k in SPECIAL: continue
        n = nodes[k]['node']
        if any(x.get('parentID') in removed for x in n.nodes('Parent')):
            newp = []; ids = set()
            for pr in live_parents(k):
                if pr.get('parentID') not in ids: ids.add(pr.get('parentID')); newp.append(pr)
            n.items = [x for x in n.items if not (x[0] == 'n' and x[1].name == 'Parent')] + [('n', pr) for pr in newp]
            n.set('anyToUnlock', 'True')  # re-linked: any one surviving parent unlocks it
    kept_total = sum(v['cost'] for k, v in nodes.items() if k not in SPECIAL and k not in removed)
    pass  # keep per-node costs as they were; the pruned nodes were mostly far-future ones
    remap_targets = {o: live_node(t) for o, t in remap_targets.items()}
    open(os.path.join(OUT, 'removed_nodes.txt'), 'w').write('\n'.join(sorted(removed)) + '\n')
keep = []
for it in tt.items:
    if it[0] == 'n' and it[1].name == 'RDNode':
        n = it[1]
        if n.get('id') in ('unlockParts', 'orphanParts', 'ORPHANS') or n.get('id') in removed: continue
        c = nodes[n.get('id')]['cost']
        n.set('cost', '0' if n.get('id') == 'start' else str(max(1, int(round(c * SCALE)))))
        ic = n.get('icon')
        if ic and ic.startswith('RP-1/Tree/Icons/'): n.set('icon', ic.replace('RP-1/Tree/Icons/', MOD + '/Icons/'))
        n.items = [x for x in n.items if not (x[0] == 'n' and x[1].name == 'Parent' and x[1].get('parentID') in ('unlockParts', 'orphanParts', 'ORPHANS'))]
    keep.append(it)
tt.items = keep
open(os.path.join(OUT, 'RP0TechTree.cfg'), 'w').write(
    '// RP-0 tech tree layout (KSP-RO, CC BY-NC-SA 4.0), science costs scaled to ~55,000 total for stock science.\n' + '\n'.join(K.dump(tree)) + '\n')

lines = ['// Every installed part placed on the RP-0 tree. Generated; see part_placement.csv.', '']
for n, node in sorted(placed.items()):
    lines.append(f'@PART[{n.replace(".", "?")}]:NEEDS[!RP-0,!RP-1]:FINAL {{ %TechRequired = {node} }}')
lines += ['', '// part upgrades and anything left on an old-tree node']
olds = sorted({p['tech'] for p in P.values() if p['tech']} | set(oldcost))
for o in olds:
    if o in nodes or o.lower() in ('hidden', 'unresearcheable', 'unresearchable'): continue
    new = remap_targets.get(o) or remap_old(o)
    lines.append(f'@PARTUPGRADE[*]:HAS[#techRequired[{o}]]:NEEDS[!RP-0,!RP-1]:FINAL {{ @techRequired = {new} }}')
    lines.append(f'@PART[*]:HAS[#TechRequired[{o}]]:NEEDS[!RP-0,!RP-1]:FINAL {{ @TechRequired = {new} }}')
open(os.path.join(OUT, 'PartPlacement.cfg'), 'w').write('\n'.join(lines) + '\n')

import csv
with open(os.path.join(OUT, 'part_placement.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['mod', 'part', 'title', 'old node', 'branch', 'RP-0 node', 'how placed'])
    for r in sorted(detail): w.writerow(r)
print('placed', len(placed), dict(how)); print('scale', round(SCALE, 4))
print('busiest nodes', per_node.most_common(12))
print('removed', len(removed), 'scale', round(SCALE, 4)); print('empty nodes', sum(1 for k in nodes if per_node[k] == 0 and k not in ('unlockParts', 'orphanParts', 'ORPHANS')))
