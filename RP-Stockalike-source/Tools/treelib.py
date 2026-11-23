# Build a "kerbal RP-0" tech tree: RP-0's node layout + every installed part placed on it.
import sys, os, re, json, collections, shutil, math
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K

RP1 = os.environ['RP1']; PARTS = os.environ['PARTS']; OUT = None
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


def node_branch(node):
    for b, lst in B.items():
        if node in lst: return b
    return None
def x_to_year(x):
    for (y0, x0), (y1, x1) in zip(anchors, anchors[1:]):
        if x <= x1: return y0 + (y1 - y0) * (x - x0) / max(1, (x1 - x0))
    return 2051
