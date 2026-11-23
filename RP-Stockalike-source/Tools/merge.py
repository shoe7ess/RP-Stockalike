# Merge Career Evolution + History of NASA into the RP0Standalone pack.
#  - RP-0 has priority: any CE/NASA contract that is the FIRST of a milestone RP-0 already has is removed.
#  - CE vs NASA: History of NASA wins.
#  - History of NASA is converted from Real Solar System to stock Kerbol + OPM (bodies, altitudes, speeds, downrange).
#  - Requirements pointing at removed contracts are re-pointed at the contract that replaced them.
import sys, os, re, glob, shutil, math, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K

PACKS = sys.argv[1]          # extracted ContractPacks folder (CEContracts, HistoryofNASA)
RP0 = sys.argv[2]            # GameData/RP0Standalone (already built) - output is written into it
REPORT = sys.argv[3]

# ------------------------------------------------------------------ removals
# name -> (replacement contract that now plays its role, reason)
CE_DROP = {
 # early program
 'FirstLaunch': ('first_FirstFlight', 'RP-0 First Launch'),
 'UpperAtmo': ('SoundingIntermediate', 'RP-0 altitude sounding rockets'),
 'KarmanLine': ('KarmanLine', 'RP-0 Karman Line'),
 'SuborbitalReturn': ('SuborbitalReturn', 'RP-0 Suborbital Return'),
 'OrbitReturn': ('first_OrbitRecover', 'RP-0 Reach Orbital Speed & Return'),
 # satellites
 'FirstSat': ('FirstSatellite', 'RP-0 First Artificial Satellite'),
 'PolarSat': ('FirstPolarSat', 'RP-0 First Polar Orbit Satellite'),
 'Geostationary': ('FirstGEOSat', 'RP-0 Geostationary Test Satellite'),
 'ScientificSat': ('FirstScienceSat', 'RP-0 First Scientific Satellite'),
 'SunSyncSat': ('FirstSunSyncSat', 'RP-0 First Sun-Synchronous Satellite'),
 'MolniyaSat': ('FirstMolniyaSat', 'RP-0 First Molniya Orbit Satellite'),
 'MEOSat': ('FirstNavSat', 'RP-0 First Navigational Satellite'),
 'TundraSat': ('FirstTundraSat', 'RP-0 Tundra Orbit Test Satellite'),
 # Mun (Minmus is kept - RP-0 has no Minmus)
 'MoonFlyby': ('LunarFlyby', 'RP-0 Munar Flyby'), 'MoonImpact': ('LunarImpactor', 'RP-0 First Munar Impactor'),
 'MoonSat': ('LunarOrbiter', 'RP-0 First Munar Orbiter'), 'MoonLanding': ('MoonLanding', 'RP-0 First Munar Landing'),
 'MoonReturn': ('MoonLandingReturn', 'RP-0 Munar Landing & Sample Return'), 'MoonRover': ('MoonRover', 'RP-0 Munar Rover'),
 # crewed milestones
 'SoundBarrier': ('BreakSoundBarrier', 'RP-0 Break the Sound Barrier'),
 'UpperAtmo-Crew': ('XPlanesHighAltitude', 'RP-0 X-Planes (High Altitude)'),
 'KarmanLine-Crew': ('XPlanesKarman', 'RP-0 X-Planes (Karman Line)'),
 'Orbit-Crew': ('first_OrbitCrewed', 'RP-0 First Orbital Flight (Crewed)'),
 'TwoCrew': ('OrbitalFlight2', 'RP-0 Orbital Flight with 2+ Crew'),
 'ThreeCrew': ('OrbitalFlight3', 'RP-0 Orbital Flight with 3 Crew'),
 'CrewEVA': ('first_EVA', 'RP-0 First EVA'), 'Rendezvous': ('Rendezvous', 'RP-0 First Rendezvous'),
 'FirstDocking': ('first_Docking', 'RP-0 First Docking'),
 'MoonOrbit': ('FirstCrewedLunarOrbit', 'RP-0 First Crewed Munar Orbit'),
 'MoonLanding-Crew': ('first_MoonLandingCrewed', 'RP-0 First Human Mun Landing'),
 'MoonLandingStay': ('MoonLandingCrew2Week', 'RP-0 Two-week Crewed Munar Stay'),
 # covered by History of NASA (NASA wins over CE)
 'OrbitOneDay': ('Faith-7', 'NASA Faith 7 (first day+ in orbit)'),
 'OrbitOneWeek': ('Gemini-V', 'NASA Gemini V (8 days)'),
 'OrbitTwoWeeks': ('Gemini-VII', 'NASA Gemini VII (14 days)'),
 'DockedManeuver': ('Gemini-X', 'NASA Gemini X (docked Agena burn)'),
 'HighOrbit-Crew': ('Gemini-XI', 'NASA Gemini XI (high-apogee record)'),
 'SSThreeMonths': ('Skylab-4', 'NASA Skylab 4 (84 days)'),
 'AsteroidLanding': ('NEAR-Shoemaker', 'NASA NEAR-Shoemaker (first asteroid landing)'),
 # interplanetary uncrewed
 'FlybyEve': ('flybyVenus', 'RP-0 Eve Flyby'), 'FlybyEveMoons': ('flybyVesta', 'RP-0 Gilly Flyby'),
 'FlybyDuna': ('flybyMars', 'RP-0 Duna Flyby'), 'FlybyDunaMoons': ('flybyPhobos', 'RP-0 Ike Flyby'),
 'FlybyJool': ('flybyJupiter', 'RP-0 Jool Flyby'), 'FlybyMoho': ('flybyMercury', 'RP-0 Moho Flyby'),
 'FlybyDres': ('flybyCeres', 'RP-0 Dres Flyby'), 'FlybyCeres': ('flybyCeres', 'RP-0 Dres Flyby'),
 'FlybyJoolMoons': ('flybyIo', 'RP-0 Jool moon flybys'),
 'FlybySaturn': ('flybySaturn', 'RP-0 Sarnus Flyby'), 'FlybyUranus': ('flybyUranus', 'RP-0 Urlum Flyby'),
 'FlybyNeptune': ('flybyNeptune', 'RP-0 Neidon Flyby'), 'FlybyPluto': ('flybyPluto', 'RP-0 Plock Flyby'),
 'FlybySaturnMoons': ('flybyTitan', 'RP-0 Sarnus moon flybys'), 'FlybyUranusMoons': ('flybyTitania', 'RP-0 Urlum moon flybys'),
 'FlybyNeptuneMoons': ('flybyTriton', 'RP-0 Thatmo Flyby'), 'FlybyPlutoMoons': ('flybyCharon', 'RP-0 Karen Flyby'),
 'OrbitEve': ('orbitVenus', 'RP-0 Eve Orbit'), 'OrbitEveMoons': ('orbitVesta', 'RP-0 Gilly Orbit'),
 'OrbitDuna': ('orbitMars', 'RP-0 Duna Orbit'), 'OrbitJool': ('orbitJupiter', 'RP-0 Jool Orbit'),
 'OrbitMoho': ('orbitMercury', 'RP-0 Moho Orbit'), 'OrbitDres': ('orbitCeres', 'RP-0 Dres Orbit'),
 'OrbitCeres': ('orbitCeres', 'RP-0 Dres Orbit'), 'OrbitSaturn': ('orbitSaturn', 'RP-0 Sarnus Orbit'),
 'OrbitUranus': ('orbitUranus', 'RP-0 Urlum Orbit'), 'OrbitNeptune': ('orbitNeptune', 'RP-0 Neidon Orbit'),
 'OrbitPluto': ('orbitPluto', 'RP-0 Plock Orbit'),
 'EveLanding': ('landingVenus', 'RP-0 Eve Landing'), 'EveMoonsLanding': ('landingVesta', 'RP-0 Gilly Landing'),
 'DunaLanding': ('landingMars', 'RP-0 Duna Landing'), 'DunaMoonsLanding': ('landingPhobos', 'RP-0 Ike Landing'),
 'MohoLanding': ('landingMercury', 'RP-0 Moho Landing'), 'DresLanding': ('landingCeres', 'RP-0 Dres Landing'),
 'CeresLanding': ('landingCeres', 'RP-0 Dres Landing'), 'JoolMoonsLanding': ('landingIo', 'RP-0 Jool moon landings'),
 'EelooLanding': ('landingIapetus', 'RP-0 Eeloo Landing'), 'SaturnMoonsLanding': ('landingTitan', 'RP-0 Sarnus moon landings'),
 'UranusMoonsLanding': ('landingTitania', 'RP-0 Urlum moon landings'), 'NeptuneMoonsLanding': ('landingTriton', 'RP-0 Thatmo Landing'),
 'PlutoLanding': ('landingPluto', 'RP-0 Plock Landing'), 'PlutoMoonsLanding': ('landingCharon', 'RP-0 Karen Landing'),
 'DunaRover': ('roverMars', 'RP-0 Duna Rover'), 'DunaRoverDrive': ('roverMars', 'RP-0 Duna Rover'),
 'MohoRover': ('roverMercury', 'RP-0 Moho Rover'), 'MohoRoverDrive': ('roverMercury', 'RP-0 Moho Rover'),
 'PlutoRover': ('roverPluto', 'RP-0 Plock Rover'), 'PlutoRoverDrive': ('roverPluto', 'RP-0 Plock Rover'),
 # stations
 'FirstSpaceStation': ('first_spaceStation', 'RP-0 First Space Station'),
 'SSFirstCrew': ('first_spaceStation', 'RP-0 First Space Station'),
 # crewed interplanetary
 'FlybyEve-Crew': ('MarsVenusFlybyCrewed', 'RP-0 Duna Opposition Eve Flyby (Crewed)'),
 'FlybyDuna-Crew': ('first_MarsFlybyCrewed', 'RP-0 Flyby Duna (Crewed)'),
 'DunaLanding-Crew': ('FirstCrewedMarsLanding', 'RP-0 First Crewed Duna Landing'),
 'DunaMoonsLanding-Crew': ('PhobosLandingCrew', 'RP-0 Ike Landing (Crewed)'),
}
NASA_DROP = {
 'TinyTim': ('first_FirstFlight', 'RP-0 First Launch'),
 'V-2 No 1': ('KarmanLine', 'RP-0 Karman Line (first rocket into space)'),
 'X003': ('BreakSoundBarrier', 'RP-0 Break the Sound Barrier'),
 'X006': ('XPlanesSupersonicMach2', 'RP-0 X-Planes (Mach 2)'),
 'X012': ('XPlanesHypersonic', 'RP-0 X-Planes (Hypersonic)'),
 'X014': ('XPlanesKarman', 'RP-0 X-Planes (Karman Line)'),
 'Explorer-1': ('FirstSatellite', 'RP-0 First Artificial Satellite'),
 'Vanguard-1': ('FirstSolarSat', 'RP-0 First Solar-Powered Satellite'),
 'Mercury-Atlas-4': ('OrbitalTestFlight', 'RP-0 Orbital Test Flight (Uncrewed)'),
 'Mercury-Atlas-5': ('OrbitalTestFlightAnimal', 'RP-0 Orbital Test Flight (Animal Crew)'),
 'Freedom-7': ('CrewedSuborbital', 'RP-0 Suborbital Flight (Crewed)'),
 'Friendship-7': ('first_OrbitCrewed', 'RP-0 First Orbital Flight (Crewed)'),
 'Gemini-III': ('OrbitalFlight2', 'RP-0 Orbital Flight with 2+ Crew'),
 'Gemini-IV': ('first_EVA', 'RP-0 First EVA'),
 'Gemini-VI-A': ('Rendezvous', 'RP-0 First Rendezvous'),
 'Gemini-VIII': ('first_Docking', 'RP-0 First Docking'),
 'Gemini-VIII-ATV': ('first_Docking', 'RP-0 First Docking (its docking target)'),
 'Apollo-VII': ('OrbitalFlight3', 'RP-0 Orbital Flight with 3 Crew'),
 'Apollo-VIII': ('FirstCrewedLunarOrbit', 'RP-0 First Crewed Munar Orbit'),
 'Apollo-XI': ('first_MoonLandingCrewed', 'RP-0 First Human Mun Landing'),
 'Apollo-XV': ('MoonExtendedStayCrew', 'RP-0 Crewed Mun Landing & Rover Exploration'),
 'Skylab-1': ('first_spaceStation', 'RP-0 First Space Station'),
 'Skylab-2': ('first_spaceStation', 'RP-0 First Space Station'),
 'STS-1': ('first_SpaceplaneOrbit', 'RP-0 First Orbital Spaceplane Flight'),
 'Pioneer-4': ('LunarFlyby', 'RP-0 Munar Flyby'),
 'Ranger-4': ('LunarImpactor', 'RP-0 First Munar Impactor'),
 'Surveyor-1': ('MoonLanding', 'RP-0 First Munar Landing'),
 'Lunar-Orbiter-1': ('LunarOrbiter', 'RP-0 First Munar Orbiter'),
 'Mariner-2': ('flybyVenus', 'RP-0 Eve Flyby'),
 'Mariner-4': ('flybyMars', 'RP-0 Duna Flyby'),
 'Mariner-9': ('orbitMars', 'RP-0 Duna Orbit'),
 'Mariner-10': ('flybyMercury', 'RP-0 Moho Flyby'),
 'Viking-1': ('landingMars', 'RP-0 Duna Landing'),
 'Pioneer-10': ('flybyJupiter', 'RP-0 Jool Flyby'),
 'Pioneer-11': ('flybySaturn', 'RP-0 Sarnus Flyby'),
 'Pioneer-12': ('orbitVenus', 'RP-0 Eve Orbit'),
 'Pioneer-13': ('probeVenus', 'RP-0 Eve Atmospheric Probe'),
 'Voyager-2': ('flybyUranus', 'RP-0 Urlum & Neidon Flybys'),
 'Galileo': ('probeJupiter', 'RP-0 Jool Orbit & Atmospheric Probe'),
 'Cassini-Huygens': ('landingTitan', 'RP-0 Sarnus Orbit & Tekto Landing'),
 'MESSENGER': ('orbitMercury', 'RP-0 Moho Orbit'),
 'Dawn': ('orbitVesta', 'RP-0 Gilly & Dres Orbits'),
 'New Horizons': ('flybyPluto', 'RP-0 Plock Flyby'),
}

# ------------------------------------------------------------------ RSS -> Kerbol for History of NASA
BODY = {'Earth': ('Kerbin', 6371, 600), 'Moon': ('Mun', 1737.4, 200), 'Mercury': ('Moho', 2439.7, 250),
        'Venus': ('Eve', 6051.8, 700), 'Mars': ('Duna', 3389.5, 320), 'Phobos': ('Ike', 11.1, 130),
        'Ceres': ('Dres', 470, 138), 'Vesta': ('Gilly', 263, 13), 'Jupiter': ('Jool', 69911, 6000),
        'Io': ('Laythe', 1821.6, 500), 'Europa': ('Vall', 1560.8, 300), 'Ganymede': ('Tylo', 2634.1, 600),
        'Callisto': ('Bop', 2410.3, 65), 'Saturn': ('Sarnus', 58232, 5300), 'Titan': ('Tekto', 2574.7, 280),
        'Uranus': ('Urlum', 25362, 2177), 'Neptune': ('Neidon', 24622, 2145), 'Triton': ('Thatmo', 1353.4, 286),
        'Pluto': ('Plock', 1188.3, 189), 'Charon': ('Karen', 606, 85.05)}
def alt_home(h): return h * 0.7 if h <= 100000 else 70000 + (h - 100000) * 0.07827
def speed_home(v): return v if v <= 1000 else 1000 + (v - 1000) * 0.25
def rnd(x): return str(int(round(x, -2 if abs(x) >= 100000 else 0))) if abs(x) >= 1000 else f'{x:.4g}'
def isnum(v):
    try: float(v); return True
    except: return False
ALT = {'minAltitude', 'maxAltitude', 'minTerrainAltitude', 'maxTerrainAltitude', 'minPeA', 'maxPeA', 'minApA', 'maxApA'}
SPD = {'minSpeed', 'maxSpeed'}
TEXTKEYS = {'title', 'description', 'synopsis', 'completedMessage', 'notes', 'genericDescription', 'genericTitle',
            'preWaitText', 'waitingText', 'completionText', 'message', 'text'}
log = collections.defaultdict(list)

def body_of(node, ct):
    b = node.get('targetBody') or ct.get('targetBody') or 'HomeWorld()'
    return b.strip()
def scale(body):
    b = BODY.get(body)
    if body in ('HomeWorld()', 'Earth', 'Kerbin') or b is None: return None
    return b[2] / b[1]
def nasa_text(t):
    t = re.sub(r'\bthe Moon\b', 'the Mun', t); t = re.sub(r'\bMoon\b', 'Mun', t)
    t = re.sub(r'\bEarth\b', 'Kerbin', t); t = re.sub(r'\bMars\b', 'Duna', t); t = re.sub(r'\bVenus\b', 'Eve', t)
    t = re.sub(r'\b(L|l)unar\b', lambda m: 'Munar' if m.group(1) == 'L' else 'munar', t)
    t = re.sub(r'\bPluto\b', 'Plock', t)
    t = re.sub(r'(?<![\w.@])(\d[\d,]*(?:\.\d+)?)(\s?)km\b',
               lambda m: f'{alt_home(float(m.group(1).replace(",", "")) * 1000) / 1000:,.0f}{m.group(2)}km', t)
    return t
KSC_LAT, KSC_LON, KERBIN_R = -0.0972, -74.5577, 600000.0

def convert_nasa(ct):
    name = ct.get('name')
    wps = []
    for n in list(K.walk(ct)):
        # bodies in any *Body* key
        for i, it in enumerate(n.items):
            if it[0] != 'v': continue
            k, v = it[1], it[2]
            if k in TEXTKEYS: n.items[i] = ('v', k, nasa_text(v)); continue
            if ('Body' in k or k == 'targetBody') and v.strip() in BODY:
                n.items[i] = ('v', k, BODY[v.strip()][0])
            elif re.search(r'\b(Moon|Mars|Venus|Jupiter|Saturn|Titan|Ganymede|Pluto|Mercury)\b', v) and n.name == 'DATA' and k != 'title':
                log['DATA values with real body names (check)'].append(f'{name}: {k} = {v}')
        if not n.name.startswith('PARAMETER'): continue
        t = n.get('type'); body = body_of(n, ct); sc = scale(body)
        for i, it in enumerate(n.items):
            if it[0] != 'v' or not isnum(it[2]): continue
            k, v = it[1], float(it[2])
            if k in ALT and t in ('ReachState', 'Orbit'):
                n.items[i] = ('v', k, rnd(alt_home(v) if sc is None else v * sc))
            elif k in SPD and t == 'ReachState':
                n.items[i] = ('v', k, rnd(speed_home(v) if sc is None else v * math.sqrt(sc)))
        if t == 'DownrangeDistance':
            d = alt_home(float(n.get('distance', '100000')))
            n.set('type', 'VisitWaypoint'); n.delkey('distance')
            n.set('index', str(100 + len(wps))); n.set('horizontalDistance', rnd(max(d * 0.15, 5000)))
            if not n.get('title'): n.set('title', f'Fly over the downrange target {d/1000:,.0f} km east of KSC')
            wp = K.Node('WAYPOINT'); wp.set('name', 'Downrange Target'); wp.set('icon', 'thermometer')
            wp.set('targetBody', 'HomeWorld()'); wp.set('latitude', str(KSC_LAT))
            wp.set('longitude', f'{KSC_LON + math.degrees(d / KERBIN_R):.4f}'); wp.set('altitude', '0')
            wps.append(wp); log['NASA downrange -> waypoint'].append(f'{name}: {d/1000:.0f} km')
    if wps:
        # waypoint indices must be contiguous after existing generators; put them in their own generator
        existing = sum(len(b.nodes('WAYPOINT')) + len(b.nodes('RANDOM_WAYPOINT')) + len(b.nodes('RANDOM_WAYPOINT_NEAR'))
                       for b in ct.nodes() if b.name.startswith('BEHAVIOUR') and b.get('type') == 'WaypointGenerator')
        for idx, n in enumerate([n for n in K.walk(ct) if n.name.startswith('PARAMETER') and n.get('index', '').startswith('1') and n.get('type') == 'VisitWaypoint' and int(n.get('index')) >= 100]):
            n.set('index', str(existing + idx))
        g = K.Node('BEHAVIOUR'); g.set('name', 'DownrangeWaypoints'); g.set('type', 'WaypointGenerator')
        for w in wps: g.items.append(('n', w))
        ct.items.append(('n', g))

# ------------------------------------------------------------------ helpers
def load(path):
    return K.parse(open(path, encoding='utf-8-sig', errors='ignore').read())
def write(path, root, header):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(header + '\n'.join(K.dump(root)) + '\n')

rp0_names = set()
for f in glob.glob(RP0 + '/Contracts/**/*.cfg', recursive=True):
    for ct in load(f).nodes():
        if ct.name.startswith('CONTRACT_TYPE'): rp0_names.add(ct.get('name'))
for name, (rep, _) in list(CE_DROP.items()) + list(NASA_DROP.items()):
    pass
missing_rep = sorted({rep for rep, _ in list(CE_DROP.values()) + list(NASA_DROP.values())} - rp0_names
                     - {'Faith-7', 'Gemini-V', 'Gemini-VII', 'Gemini-X', 'Gemini-XI', 'Skylab-4', 'NEAR-Shoemaker'})
if missing_rep: print('WARNING replacements not in RP-0:', missing_rep)
REPLACE = {k: v[0] for k, v in list(CE_DROP.items()) + list(NASA_DROP.items())}
# History of NASA requires several missions that were never included in the pack, which locked
# whole chains (e.g. Artemis needs STS-135). Point each at the previous mission that does exist.
MISSING_IN_NASA = {'STS-61-C': 'STS-51-F', 'STS-36': 'STS-34', 'STS-82': 'STS-61', 'STS-89': 'STS-83',
    'STS-95': 'STS-90', 'STS-106': 'STS-88', 'STS-102': 'STS-98', 'STS-109': 'STS-105', 'STS-111': 'STS-110',
    'STS-121': 'STS-113', 'STS-126': 'STS-122', 'STS-129': 'STS-125', 'STS-131': 'STS-130', 'STS-135': 'STS-133',
    'Soyuz-18': 'Apollo-XVII', 'Sakigake': 'Helios-2'}
REPLACE.update(MISSING_IN_NASA)

def resolve(name):
    seen = set()
    while name in REPLACE and name not in seen:
        seen.add(name); name = REPLACE[name]
    return name

def fix_requirements(ct, pack):
    for n in K.walk(ct):
        if not n.name.startswith('REQUIREMENT'): continue
        c = n.get('contractType')
        if c and c in REPLACE:
            new = resolve(c)
            n.set('contractType', new); log['requirements re-pointed'].append(f'[{pack}] {ct.get("name")}: {c} -> {new}')

def process(pack, src_dir, dst_sub, drops, convert=None, skip=lambda rel: False):
    kept = removed = 0
    for f in sorted(glob.glob(src_dir + '/**/*.cfg', recursive=True)):
        rel = os.path.relpath(f, src_dir)
        if skip(rel): continue
        root = load(f)
        new_items = []
        for it in root.items:
            if it[0] == 'n' and it[1].name.startswith('CONTRACT_TYPE'):
                ct = it[1]; nm = ct.get('name')
                if nm in drops:
                    removed += 1; log[f'{pack}: removed (duplicate)'].append(f'{nm} ({ct.get("title")}) -> {drops[nm][1]}'); continue
                if nm in rp0_names:
                    ct.set('name', f'{pack}_{nm}'); log['renamed (name clash with RP-0)'].append(f'{nm} -> {pack}_{nm}')
                if convert: convert(ct)
                fix_requirements(ct, pack)
                kept += 1
            new_items.append(it)
        root.items = new_items
        if any(i[0] == 'n' for i in root.items):
            write(os.path.join(RP0, 'Contracts', dst_sub, rel), root, f'// Merged into RP-Stock from {pack}. Original authors credited in README.\n')
    return kept, removed

# ------------------------------------------------------------------ Career Evolution
ce_src = os.path.join(PACKS, 'CEContracts')
for d in (os.path.join(RP0, 'Contracts', 'CareerEvolution'), os.path.join(RP0, 'Contracts', 'HistoryofNASA'), os.path.join(RP0, 'HistoryofNASA')):
    if os.path.exists(d): shutil.rmtree(d)
# group file: nest under the RP0 group
grp_root = load(os.path.join(ce_src, 'CEContracts', 'CareerEvolutionContracts.cfg'))
ce_group = [n for n in grp_root.nodes() if n.name.startswith('CONTRACT_GROUP')][0]
ce_group.name = 'CONTRACT_GROUP'
ce_kept, ce_removed = process('CE', os.path.join(ce_src, 'CEContracts', 'Contracts'), 'CareerEvolution', CE_DROP)

# ------------------------------------------------------------------ History of NASA
nasa_src = os.path.join(PACKS, 'HistoryofNASA')
nroot = load(os.path.join(nasa_src, 'HistoryofNASA.cfg'))
nasa_group = [n for n in nroot.nodes() if n.name.startswith('CONTRACT_GROUP')][0]
nasa_group.name = 'CONTRACT_GROUP'
agents = [n for n in nroot.nodes() if n.name.startswith('AGENT')]
for a in agents:
    for k in ('logoURL', 'logoScaledURL'):
        v = a.get(k)
        if v: a.set(k, v.replace('ContractPacks/HistoryofNASA/', 'RP-Stock/HistoryofNASA/'))
    if a.get('name') == 'USARMY':      # duplicate title in the original
        seen = False; items = []
        for it in a.items:
            if it[0] == 'v' and it[1] == 'title':
                if seen: continue
                seen = True
            items.append(it)
        a.items = items
    if a.get('name') == 'USNavy':
        a.set('description', 'United States Navy')
nasa_kept, nasa_removed = process('NASA', os.path.join(nasa_src, 'Missions'), 'HistoryofNASA', NASA_DROP, convert=convert_nasa)
if os.path.isdir(os.path.join(nasa_src, 'Logo')):
    shutil.copytree(os.path.join(nasa_src, 'Logo'), os.path.join(RP0, 'HistoryofNASA', 'Logo'))
agent_root = K.Node('root'); agent_root.items = [('n', a) for a in agents]
for a in agents: a.name = 'AGENT'
write(os.path.join(RP0, 'Agencies', 'HistoryofNASA_Agents.cfg'), agent_root, '// Agents from the History of NASA contract pack\n')

# ------------------------------------------------------------------ groups: nest CE + NASA under the RP0 root group
gpath = os.path.join(RP0, 'Contracts', 'Groups.cfg')
g = load(gpath)
rp0g = [n for n in g.nodes() if n.name.startswith('CONTRACT_GROUP')][0]
rp0g.items = [it for it in rp0g.items if not (it[0] == 'n' and it[1].get('name') in ('CareerEvolution', 'HistoryofNASA'))]
for sub in (ce_group, nasa_group):
    for n in K.walk(sub):
        for i, it in enumerate(n.items):
            if it[0] == 'v' and it[1] == 'minVersion': n.items[i] = ('v', 'minVersion', '1.12.2')
    rp0g.items.append(('n', sub))
rp0g.set('displayName', 'RP-0 + Career Evolution + History of NASA')
write(gpath, g, '')

with open(REPORT, 'w') as fh:
    fh.write(f'Career Evolution: kept {ce_kept}, removed {ce_removed}\nHistory of NASA: kept {nasa_kept}, removed {nasa_removed}\n')
    for cat, items in sorted(log.items()):
        fh.write(f'\n== {cat} ({len(items)})\n' + '\n'.join(items) + '\n')
print(f'CE kept {ce_kept} removed {ce_removed}; NASA kept {nasa_kept} removed {nasa_removed}')
for cat, items in sorted(log.items()): print(f'{len(items):4d} {cat}')
