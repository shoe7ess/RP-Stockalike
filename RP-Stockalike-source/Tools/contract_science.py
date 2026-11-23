# Re-base every RP-Stock contract's science reward on the tech tree:
# each contract gets a historical year (from its program group), contracts are bucketed into the same eras as the tree,
# and an era's contracts together pay SHARE x (science cost of that era's tech nodes), split by mission difficulty.
import os, re, sys, json, csv, collections
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K

SRC = sys.argv[1]            # folder holding Contracts/ and Spacelines/
POLISH = sys.argv[2]         # tree_polish.json
OUT = sys.argv[3]            # output folder (ContractScience.cfg + report csv)
SHARE = 0.40                 # contracts cover ~40% of each era's research; experiments do the rest

G = {  # group -> (first year, last year)
 'SuborbRocketDev': (1945, 1952), 'SuborbRocketResearch': (1946, 1955), 'SL_SuborbRocketResearch': (1946, 1955),
 'USA_Early_Missions': (1946, 1958), 'USAaeroMission': (1946, 1968), 'EarlyXPlanes': (1947, 1962), 'Records': (1957, 1970),
 'EarlySatellites': (1957, 1962), 'EarlySatellites-Heavy': (1958, 1963), 'SL_EarlySatellites': (1957, 1960),
 'LauncherMissions': (1953, 1967), 'ProbeMission': (1958, 1966), 'PioneerMission': (1958, 1973), 'SL_ScienceSatellites': (1958, 1966),
 'EarlyLunarProbes': (1959, 1966), 'SL_EarlyLunarProbes': (1959, 1966), 'RangerMission': (1961, 1965), 'MercuryMission': (1959, 1963),
 'EOS': (1959, 1965), 'Surveillance': (1959, 1976), 'TargetedSats': (1962, 1965), 'CommNetwork': (1963, 1966),
 'CrewedOrbit': (1961, 1965), 'HumanRecords': (1961, 1990), 'MarinerMission': (1962, 1973), 'EarlyInnerPlanetProbes': (1961, 1970),
 'SL_EarlyInnerPlanetProbes': (1961, 1972), 'CommApp': (1963, 1970), 'CommercialApplications': (1965, 1975), 'EarlySpacePlanes': (1963, 1981),
 'SL_EarlySpacePlanes': (1963, 1981), 'GeminiMission': (1965, 1966), 'CrewedOrbitAdv': (1965, 1970), 'EOS2': (1964, 1972),
 'UncrewedOrbits': (1959, 1975), 'UncrewedLunarSurface': (1964, 1976), 'SL_UncrewedLunarSurface': (1964, 1976),
 'SurveyorMissions': (1966, 1968), 'LunarOrbiterMission': (1966, 1967), 'MinmusExploration': (1966, 1975),
 'CrewedMilestones': (1965, 1975), 'ApolloMission': (1967, 1972), 'CrewedLunar': (1967, 1972), 'SL_CrewedLunar': (1967, 1972),
 'VenusSurfaceExp': (1967, 1985), 'SL_VenusSurfaceExp': (1967, 1985), 'Rovers': (1970, 1997), 'CommApp2': (1970, 1985),
 'EarlyEarthSpaceStation': (1971, 1986), 'SpaceStations': (1971, 2000), 'MartianSurfaceExploration': (1971, 2005),
 'SL_MartianSurfaceExploration': (1971, 2005), 'EOS3': (1972, 1985), 'OuterPlanetFlyby': (1972, 1989), 'SkylabMission': (1973, 1973),
 'JupiterObservation': (1973, 1995), 'MercuryExploration': (1973, 2011), 'HeliosMission': (1974, 1976), 'VikingMission': (1975, 1975),
 'EarlyLunarHabitation': (1975, 1995), 'SurfaceBases': (1975, 2030), 'VoyagerMission': (1977, 1977), 'USAMiscMissions': (1960, 1980),
 'SaturnObservation': (1979, 2004), 'SpaceShuttleMission': (1981, 2011), 'SmallBodiesFlyby': (1986, 2006),
 'OuterGasGiantSurvey': (1986, 2015), 'ISSMission': (1998, 2011), 'AsteroidExploration': (2000, 2020),
 'SaturnMoonLandings': (2005, 2035), 'JupiterMoonLandings': (2015, 2035), 'PlutoLandings': (2015, 2040),
 'CrewedFlybys': (2020, 2040), 'ArtemisMission': (2022, 2030), 'UranusMoonLandings': (2030, 2045),
 'NeptuneMoonLandings': (2035, 2045), 'CrewedMarsExp': (2030, 2045), 'CrewedLanding': (2030, 2045),
}
TIER = {'Kerbin': 1, 'HomeWorld()': 1, 'Mun': 2, 'Moon': 2, 'Minmus': 2, 'Eve': 3, 'Venus': 3, 'Duna': 3, 'Mars': 3, 'Ike': 3, 'Gilly': 3,
        'Moho': 3.5, 'Mercury': 3.5, 'Dres': 3.5, 'Ceres': 3.5, 'Vesta': 3.5, 'Jool': 4, 'Jupiter': 4, 'Laythe': 4.3, 'Vall': 4.3,
        'Tylo': 4.3, 'Bop': 4.3, 'Pol': 4.3, 'Sarnus': 4.5, 'Saturn': 4.5, 'Hale': 4.7, 'Ovok': 4.7, 'Eeloo': 5, 'Slate': 4.7,
        'Tekto': 4.7, 'Urlum': 5, 'Uranus': 5, 'Polta': 5.2, 'Priax': 5.2, 'Wal': 5.2, 'Tal': 5.2, 'Neidon': 5.3, 'Neptune': 5.3,
        'Thatmo': 5.5, 'Nissee': 5.5, 'Plock': 5.5, 'Pluto': 5.5, 'Karen': 5.5, 'Kerbol': 3, 'Sun': 3}
PRESTIGE = {'trivial': 0.8, 'significant': 1.0, 'exceptional': 1.3}
ERAS = [(1945, 1952), (1953, 1957), (1958, 1962), (1963, 1967), (1968, 1972), (1973, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2051)]

pol = json.load(open(POLISH)); era_cost = {e: c for e, (n, c) in pol['era_cost'].items()}
def era_of(y): return next(f'{a}-{b}' for a, b in ERAS if y <= b)

cons = []
for top in ('Contracts', 'Spacelines'):
    for r, _, fs in os.walk(os.path.join(SRC, top)):
        for f in sorted(fs):
            if not f.endswith('.cfg'): continue
            s = open(os.path.join(r, f), encoding='utf-8-sig', errors='ignore').read()
            if 'CONTRACT_TYPE' not in s: continue
            for c in K.parse(s).nodes():
                if not c.name.startswith('CONTRACT_TYPE') or '!OPM' in c.name: continue
                txt = '\n'.join(K.dump(c))
                tb = c.get('targetBody') or ''
                body = re.sub(r'.*:', '', tb).strip() or 'Kerbin'
                body = {'Moon': 'Mun', 'Mars': 'Duna', 'Venus': 'Eve', 'Jupiter': 'Jool'}.get(body, body)
                tier = TIER.get(body, 2.5 if tb.startswith('@') else 1)
                if tier <= 1:   # contract-level target is the home world: look at where the parameters actually send you
                    pb = [re.sub(r'.*:', '', x).strip() for x in re.findall(r'targetBody\s*=\s*(\S+)', txt)]
                    pb = [{'Moon': 'Mun', 'Mars': 'Duna', 'Venus': 'Eve', 'Jupiter': 'Jool'}.get(x, x) for x in pb]
                    deep = max(pb, key=lambda x: TIER.get(x, 0), default=body)
                    if TIER.get(deep, 0) > tier: body, tier = deep, TIER[deep]
                crewed = any(int(float(m)) > 0 for m in re.findall(r'minCrew\s*=\s*([\d.]+)', txt))
                landed = bool(re.search(r'situation\s*=\s*(LANDED|SPLASHED|SrfLanded|SrfSplashed)', txt))
                ret = 'ReturnHome' in txt or 'RecoverKerbal' in txt
                pres = PRESTIGE.get((c.get('prestige') or 'significant').lower(), 1.0)
                unlimited = (c.get('maxCompletions') or '0') in ('0', '')
                repeat = unlimited or int(float(c.get('maxCompletions') or 0)) > 1
                w = tier ** 1.3 * (2 if crewed else 1) * (1.5 if landed else 1) * (1.3 if ret else 1) * pres * (0.6 if unlimited else 1)
                orbit = bool(re.search(r'type\s*=\s*Orbit\b|situation\s*=\s*ORBITING|InSpace', txt))
                flying = bool(re.search(r'situation\s*=\s*FLYING|ReachSpeed|Mach', txt))
                pr = [x.strip().lower() for x in (c.get('prestige') or '').split(',') if x.strip()] if c.get('prestige') else []
                pfac = {'trivial': 1.0, 'significant': 1.25, 'exceptional': 1.5}
                pf = sum(pfac.get(x, 1.25) for x in pr) / len(pr) if pr else 1.25
                cons.append(dict(repeat=repeat, orbit=orbit, flying=flying, pf=pf, oldf=(c.get('advanceFunds'), c.get('rewardFunds')),
                                 name=c.get('name'), group=c.get('group'), sort=float(c.get('sortKey') or 0), file=os.path.join(r, f)[len(SRC) + 1:],
                                 hdr=c.name, tb=bool(tb), body=body, crewed=crewed, landed=landed, ret=ret, w=w, old=c.get('rewardScience')))
missing = sorted({c['group'] for c in cons if c['group'] not in G})
if missing: sys.exit(f'groups without a year range: {missing}')
by = collections.defaultdict(list)
for c in cons: by[c['group']].append(c)
for g, lst in by.items():
    lst.sort(key=lambda c: (c['sort'], c['file'], c['name'])); y0, y1 = G[g]
    for i, c in enumerate(lst): c['year'] = y0 + (y1 - y0) * (i / max(1, len(lst) - 1))
for c in cons: c['era'] = era_of(round(c['year']))
# smooth version of "era cost / era contracts": a +-5-year window around each contract, so a thin stretch of the tree
# (e.g. the 1970s) doesn't make rewards jump at era boundaries; then scaled so the whole set pays SHARE of the tree.
W = 5
ny, nc = pol['node_year'], pol['node_cost']
for c in cons:
    sci_win = sum(nc[k] for k in ny if k != 'start' and abs(ny[k] - c['year']) <= W)
    w_win = sum(d['w'] for d in cons if abs(d['year'] - c['year']) <= W)
    c['raw'] = sci_win * c['w'] / w_win
k = SHARE * sum(v for n, v in nc.items() if n != 'start') / sum(c['raw'] for c in cons)
for c in cons: c['sci'] = max(1, round(c['raw'] * k))

os.makedirs(OUT, exist_ok=True)
L = ['// RP-Stock balance: contract science rewards re-based on the tech tree (generated by contract_science.py).',
     f'// Each era\'s contracts together pay about {int(SHARE*100)}% of the science that era\'s tech nodes cost, split by mission difficulty',
     '// (destination, crewed, landing, return, prestige). The divisions cancel KSP\'s prestige factor and per-body weighting, so at the 100% science slider the number here is the number paid.', '']
for c in sorted(cons, key=lambda c: (c['year'], c['name'])):
    nm = re.sub(r'[ \[\]=]', '?', c['name'])
    base = f"{c['sci']} * Max(@rewardFactor, 0.25)" if 'rewardFactor' in (c['old'] or '') else str(c['sci'])   # keep the anti-grind ramp
    v = f"({base}) / {c['pf']:g} / @/targetBody.Multiplier()" if c['tb'] else f"({base}) / {c['pf']:g}"
    L.append(f"@CONTRACT_TYPE[{nm}]:FINAL {{ %rewardScience = {v} }}  // {c['group']}, ~{round(c['year'])}, was {c['old']}")
open(os.path.join(OUT, 'ContractScience.cfg'), 'w').write('\n'.join(L) + '\n')
with open(os.path.join(OUT, 'contract_science.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['contract', 'group', 'year', 'era', 'body', 'crewed', 'landed', 'return', 'weight', 'science', 'was'])
    for c in sorted(cons, key=lambda c: c['year']): wr.writerow([c['name'], c['group'], round(c['year']), c['era'], c['body'], c['crewed'], c['landed'], c['ret'], round(c['w'], 2), c['sci'], c['old']])
# ------------------------------------------------------------------ funds
# Mission cost (funds) by destination and mission type, calibrated on stock-scale craft built from the installed parts
# (V-2 ~2k, R-7/Vostok ~30k, Proton ~75k, Saturn IB ~55k, N1-L3 ~250k, Energia ~250k).
COST = {  # tier band -> {mode: cost}
    1: dict(aero=8000, sub=3000, sub_crew=10000, orbit=25000, orbit_crew=35000, station=90000, station_crew=120000),
    2: dict(flyby=35000, orbit=45000, land=90000, orbit_crew=120000, land_crew=300000, flyby_crew=100000),
    3: dict(flyby=50000, orbit=70000, land=100000, orbit_crew=700000, land_crew=1200000, flyby_crew=600000),
    4: dict(flyby=90000, orbit=140000, land=200000, orbit_crew=2000000, land_crew=2500000, flyby_crew=1800000),
    5: dict(flyby=110000, orbit=170000, land=250000, orbit_crew=2500000, land_crew=3000000, flyby_crew=2200000),
}
SUB_GROUPS = {'SuborbRocketDev', 'SuborbRocketResearch', 'SL_SuborbRocketResearch', 'USA_Early_Missions'}
AERO_GROUPS = {'EarlyXPlanes', 'USAaeroMission'}
PLANE_GROUPS = {'EarlySpacePlanes', 'SL_EarlySpacePlanes'}
def band(t): return 1 if t < 1.5 else 2 if t < 2.5 else 3 if t < 3.9 else 4 if t < 4.9 else 5
ADV, REW_FIRST, REW_REPEAT = 0.35, 1.65, 1.25
for c in cons:
    b = band(TIER.get(c['body'], 1)); T = COST[b]; g = c['group'] or ''
    stationish = any(w in g for w in ('Station', 'ISS', 'Skylab'))
    if b == 1:
        if g in SUB_GROUPS: mode = 'sub_crew' if c['crewed'] else 'sub'
        elif g in AERO_GROUPS or (c['flying'] and not c['orbit']): mode = 'aero'
        elif g in PLANE_GROUPS: mode = 'orbit_crew' if c['orbit'] else 'sub_crew'
        elif stationish: mode = 'station_crew' if c['crewed'] else 'station'
        elif g in SUB_GROUPS or not c['orbit']: mode = 'sub_crew' if c['crewed'] else 'sub'
        else: mode = 'orbit_crew' if c['crewed'] else 'orbit'
    else:
        kind = 'land' if c['landed'] else 'orbit' if c['orbit'] else 'flyby'
        mode = kind + ('_crew' if c['crewed'] else '')
    cost = T[mode] * (1.4 if c['ret'] and not c['crewed'] and b > 1 else 1)
    cost *= 1 + 0.01 * max(0, c['year'] - 1960)            # payloads grow with the era
    if 'Habitation' in g or 'SurfaceBases' in g: cost *= 1.5
    c['mode'] = mode; c['cost'] = cost
F = ['// RP-Stock balance: contract funds re-based on what the mission costs to fly with the installed parts (generated).',
     '// advance = 35% of the estimated mission cost; completion = 165% (one-off contracts) or 125% (repeatable),',
     '// so a contract returns about 2x its cost, leaving profit for facility upgrades and hiring. Failure costs the advance.',
     '// Divisions cancel KSP\'s prestige factor and per-body weighting: at the 100% funds slider these are the numbers paid.', '']
for c in sorted(cons, key=lambda c: (c['year'], c['name'])):
    nm = re.sub(r'[ \[\]=]', '?', c['name'])
    rep = c['repeat']
    adv = round(c['cost'] * ADV, -2); rew = round(c['cost'] * (REW_REPEAT if rep else REW_FIRST), -2)
    c['adv'], c['rew'] = adv, rew
    div = f" / {c['pf']:g}" + (" / @/targetBody.Multiplier()" if c['tb'] else '')
    ag = ' * Max(@rewardFactor, 0.25)' if any('rewardFactor' in (x or '') for x in c['oldf']) else ''   # keep the anti-grind ramp
    F.append(f"@CONTRACT_TYPE[{nm}]:FINAL {{ %advanceFunds = ({adv:.0f}{ag}){div}\n\t%rewardFunds = ({rew:.0f}{ag}){div}\n\t%failureFunds = ({adv:.0f}){div} }}  // {c['group']}, ~{round(c['year'])}, {c['mode']}, est. cost {c['cost']:.0f}; was {c['oldf'][0]} / {c['oldf'][1]}")
open(os.path.join(OUT, 'ContractFunds.cfg'), 'w').write('\n'.join(F) + '\n')
with open(os.path.join(OUT, 'contract_funds.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['contract', 'group', 'year', 'body', 'mode', 'repeatable', 'est_cost', 'advance', 'reward', 'old_advance', 'old_reward'])
    for c in sorted(cons, key=lambda c: c['year']): wr.writerow([c['name'], c['group'], round(c['year']), c['body'], c['mode'], c['repeat'], round(c['cost']), c['adv'], c['rew'], c['oldf'][0], c['oldf'][1]])
print('contracts', len(cons))
for e in era_cost:
    lst = [c for c in cons if c['era'] == e]
    if lst: print(f"  {e}: tree {era_cost[e]:6d}  contracts {len(lst):3d}  pay {sum(c['sci'] for c in lst):6d}  range {min(c['sci'] for c in lst)}-{max(c['sci'] for c in lst)}")
