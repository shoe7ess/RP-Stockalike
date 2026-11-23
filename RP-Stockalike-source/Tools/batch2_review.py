# Batch 2: hand review of every remaining non-Bluedog part pack.
# Reads batch2.csv (analogue pass), applies reviewed rules, appends to overrides.csv, writes batch2_review.csv
import sys, os, re, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL

P = json.load(open('rp1/parts.json'))['parts']
rows = list(csv.DictReader(open('batch2.csv')))
pick = TL.pick

SIZE_YEAR = {'0.625': 1958, '1.25': 1960, '1.875': 1961, '2.5': 1962, '3.75': 1965, '5': 1967, '7.5': 2019, '10': 2035}
def size_of(n):
    s = n.lower()
    for pat, v in [(r'(^|[-_.])(0625|0m625)($|[-_.])', '0.625'), (r'size1p5|1p5|(^|[-_.])1875($|[-_.])|1m875', '1.875'),
                   (r'(^|[-_.])(125|1m25)($|[-_.])|size1([^p0-9]|$)', '1.25'), (r'(^|[-_.])(375|3m75)($|[-_.])|size3', '3.75'),
                   (r'(^|[-_.])(25|2m50|250)($|[-_.])|size2', '2.5'), (r'(^|[-_.])75($|[-_.])', '7.5'),
                   (r'(^|[-_.])(5|5m00|500)($|[-_.])|size4', '5'), (r'(^|[-_.])10($|[-_.])|10m', '10')]:
        if re.search(pat, s): return v
    return None
def by_size(n, branch, default=1960):
    return pick(branch, SIZE_YEAR.get(size_of(n), default))

R = []   # (mod-prefix, regex on part name, node or callable(name)->node, reason)
def rule(mod, rx, node, why): R.append((mod, re.compile(rx), node, why))

# ---------------- UmbraSpaceIndustries ----------------
U = 'UmbraSpaceIndustries'
rule(U, r'WarpDrive', 'colonization2150ElecProp', 'Alcubierre drive: far-future endgame')
rule(U, r'^USI\.(ORION|MEDUSA|ORIONTank)', 'nuclearPropulsionNF2', 'nuclear pulse propulsion: post-2035 concept')
rule(U, r'^USI\.BNTR', 'nuclearPropulsionNF', 'bimodal NTR (power + thrust): 2020s concept')
rule(U, r'^USI\.Nuke\.(625|125)', 'advModernNuclearPower', 'small fission reactor ~ Kilopower (2018)')
rule(U, r'^USI\.Nuke\.', 'nuclearPowerNF', 'large surface fission reactor: near-future')
rule(U, r'^C3\.(NukeFuelTank|DepletedFuelTank)', 'advModernNuclearPower', 'reactor fuel storage, with the USI reactors')
rule(U, r'^(C3\.|Mountable|Radial(Lqd|Sup)|StowPak)', 'materialsScienceHuman', 'generic cargo Kontainer, early storage')
rule(U, r'^USILS\.(Cryo|Coolant)', 'lifeSupportNF', 'Kerbcicle cryo-sleep: speculative tech')
rule(U, r'Greenhouse\.MiniCupola', 'efficientLifeSupport', 'small greenhouse ~ Veggie (2014)')
rule(U, r'Greenhouse', 'commercialLifeSupport', 'large greenhouse: after Veggie')
rule(U, r'^USILS\.LgRecycler', 'longTermLifeSupport', 'large recycler ~ Mir/ISS ECLSS')
rule(U, r'^USILS\.Recycler', 'basicLifeSupport', 'recycler ~ Skylab/Salyut era')
rule(U, r'^USILS\.(Sm|Viewing)Cupola', 'improvedOrbitalConstruction', 'cupola, same node as stock cupola')
rule(U, r'^(LS\.Tank|Fert\.Tank|.*MiniPack)', 'earlyLifeSupport', 'consumables storage, Gemini-era')
rule(U, r'^KA\.Engine\.\d+\.0[23]$|^KA\.Engine\.(125|250)\.03|^KA\.Engine\.(375|500)\.01', 'colonization2051NuclearProp', 'Karborundum fusion/torch drive: 2050s')
rule(U, r'^KA\.Engine\.(125|250|625)\.01', 'orbitalRocketry1967', 'Karbonite-fuelled rocket, after Karbonite mining')
rule(U, r'^LFKA\.Engine\.125', 'orbitalRocketry1964', 'conventional LF engine')
rule(U, r'^LFKA\.Engine\.250', 'orbitalRocketry1967', 'conventional LF engine, larger')
rule(U, r'^(LF)?KA\.Jet\.PropFan', 'matureTurbofans', 'propfan ~ 1980s UDF')
rule(U, r'^(LF)?KA\.Jet\.', 'matureSupersonic', 'turbojet')
rule(U, r'^KA\.SRB', 'solids1962', 'small SRB')
rule(U, r'^KA\.(LandingFrame|.*Leg)|^kaRadialLeg', 'lunarLanding', 'landing legs/frames')
rule(U, r'^KA\.(Scanner|DetectionArray)', 'scienceExploration', 'orbital resource scanner, same node as stock SurveyScanner')
rule(U, r'^KA\.Analyzer', 'scienceLunar', 'surface sample kit')
rule(U, r'^KA\.(SolarCollector|ParticleCollector)', 'advancedLifeSupport', 'particle collector: Genesis-era (2001)')
rule(U, r'^(KA\.|ORE\.DRILL)', 'basicLifeSupport', 'Karbonite ISRU, just after stock ISRU')
rule(U, r'^KER\.SABRE', 'scramjetEngines', 'air-breathing hybrid')
rule(U, r'^KER\.VTOL', 'improvedLandingEngines', 'VTOL descent engine')
rule(U, r'^KER\.RadialProbe', 'improvedAvionics', 'radial probe core')
rule(U, r'^KER\.Wheel', 'interplanetaryRovers', 'rover wheel')
rule(U, r'^KER\.', 'largeRoverDesigns', 'Karibou expedition rover system')
rule(U, r'^Akita', 'interplanetaryRovers', 'small Akita rover kit')
rule(U, r'^ConstructionPort', 'largeScaleOrbitalCon', 'construction (weld) ports: ISS-assembly era')
rule(U, r'^PAL\.(Mini)?Wheel', 'largeRoverDesigns', 'construction vehicle wheels')
rule(U, r'^Konstruction\.Orbital\.Shipyard', 'largeScaleHabitats', 'orbital shipyard')
rule(U, r'^(Kosntruction|Konstruction)\.Workshop', 'advancedHabitats', 'in-situ fabricator')
rule(U, r'^PAL\.', 'improvedOrbitalConstruction', 'construction/manipulator kit')
rule(U, r'^WOLF\.', 'colonization2051LifeSupport', 'WOLF interplanetary logistics: colonisation era')
rule(U, r'^MKS\.Drill\.0[12]', 'longTermLifeSupport', 'pulse drills')
rule(U, r'^(MKS\.Drill\.03|ATLAS\.Harvester)', 'advancedHabitats', 'industrial strip miners/harvesters')
rule(U, r'^Atlas\.', 'largeScaleHabitats', "MKS 'Atlas' 10-20 m colony modules")
rule(U, r'^Duna\.', 'advancedHabitats', "MKS 'Duna' large base modules")
rule(U, r'^Ranger\.(ISM|Workshop|HabModule|AgModule|MiniHab)', 'inflatableHabitats', "MKS 'Ranger' inflatables ~ BEAM (2016)")
rule(U, r'^(Ranger\.|MKS\.FlexOTube)', 'inflatableHabitats', "MKS 'Ranger' small base kit")
rule(U, r'^(Tundra\.|MKS\.Processor|UKS\.|Tundra\.Mini|Tundra\.Multi)', 'improvedHabitats', "MKS 'Tundra' base modules")
rule(U, r'^(MKS\.LandingLeg|WideLeg)', 'advancedLanding', 'heavy base landing legs')
rule(U, r'^MKS\.SkyCrane', 'reusability', 'sky crane ~ Curiosity (2012)')
rule(U, r'^MKS\.LandingWheel', 'largeRoverDesigns', 'base wheels')
rule(U, r'^MKS\.InflationTank', 'orbitalRocketry2014', 'inflatable propellant tank')
rule(U, r'^(SalamanderPod|ScoutLanderMk2)', 'advancedLanding', 'small crewed lander pods')
rule(U, r'^MKS\.LightGlobe', 'electronicsCommercial', 'portable light kit')
rule(U, r'^(NodeHelper|USI\.DeomlitionBlock)', 'start', 'utility part')

# ---------------- Firespitter ----------------
F = 'Firespitter'
rule(F, r'^(FSbattery)$', None, '')
rule(F, r'^(fsgyroscope|FSapacheNoseASAS)$', 'earlyFlightControl', 'gyro/ASAS')
rule(F, r'Electric', 'advancedTurbofans', 'electric aviation: 2000s+')
rule(F, r'VTOL', 'efficientSupersonic', 'VTOL fans ~ Harrier era')
rule(F, r'apache', 'matureTurbofans', 'attack-helicopter parts ~ 1980s')
rule(F, r'copter|Rotor|landingPads|tailBoom', 'matureSupersonic', 'helicopter parts ~ 1950s')
rule(F, r'(?i)biplane|float|swamp|^FSPROpeller$|strutConnector|gadget|popup|jerrycan', 'start', 'pre-jet aviation / utility')
rule(F, r'airBrake', 'supersonicFlightRP0', 'air brake')
rule(F, r'.*', 'supersonicDev', 'WWII/early-jet airframe parts')

# ---------------- MagicSmokeIndustries (Infernal Robotics) ----------------
M = 'MagicSmokeIndustries'
rule(M, r'^IR\.(Camera|SurfaceSampler)', 'surfaceScience', 'robotic sampler/camera')
rule(M, r'^IR\.(SmallSuspension|LargeSuspension|LandingFoot)', 'interplanetaryRovers', 'rover suspension')
rule(M, r'^IR\.DockingPort', 'standardDockingPorts', 'robotic docking mechanism')
rule(M, r'^IR\.(Rail|.*Gantry|Foldatron)', 'electronicsSpaceplanes', 'robotic arm joints ~ Canadarm (1981)')
rule(M, r'^IR\.(Rotatron|Pivotron|Extendatron|Adaptron)', 'electronicsSpaceStation', 'basic servo/rotator')
rule(M, r'^IR\.', 'materialsScienceSpaceStation', 'robotics structure')

# ---------------- Near Future ----------------
N = 'NearFuture'
rule(N, r'^battery-0625$', 'electronicsHuman', 'small battery')
rule(N, r'^battery-125$', 'electronicsLunar', 'battery')
rule(N, r'^lithium-', 'elecPropulsion1986', 'lithium tank, same node as first MPD thruster (mpdt-0625)')
rule(N, r'^nfex-fueltank', 'orbitalRocketry1963', 'small probe propellant tank')
rule(N, r'^nflv-engine-rutherford', 'orbitalRocketry2014', 'Rutherford (2017)')
rule(N, r'^nflv-.*-75-|^nflv-.*-75$', lambda n, b: pick(b, 2019) if b in TL.B else 'orbitalRocketry2019', '7.5 m heavy-lift ~ SLS/Starship era')
rule(N, r'^nflv-(fueltank|skeletal|cluster|nflv-fueltank).*-5-', 'orbitalRocketry1967', '5 m tankage ~ Saturn V')
rule(N, r'^nflv-(cargo|fairing|decoupler|separator).*-5-', 'materialsScienceSpaceStation', '5 m cargo/structure')
rule(N, r'^command-mk3-9', 'spaceShuttles', 'Mk3 spaceplane cockpit')
rule(N, r'^command-mk4-1', 'modernCapsules', 'Orion-class capsule')
rule(N, r'^command-375-biconic', 'commercialCapsules', 'large biconic capsule')
rule(N, r'^command-(125|25)-landing', 'lunarLanding', 'lander can ~ LM')
rule(N, r'^command-(125|25)-1$', 'improvedCapsules', 'utility command can')
rule(N, r'^(command-ppd-1|utility-pod-25)', 'earlySpaceStations', 'station utility module')

# ---------------- ReStock+ ----------------
RS = 'ReStockPlus'
rule(RS, r'oretank', 'lifeSupportISRU', 'ore tank, with stock ISRU')
rule(RS, r'^restock-(fueltank|fuel-tank)-(rcs)', lambda n, b: by_size(n, 'control'), 'RCS tank by diameter')
rule(RS, r'^restock-(fueltank|fuel-tank)-probe', 'orbitalRocketry1963', 'probe tank')
rule(RS, r'^restock-(fueltank|fuel-tank)-(?!adapter)', lambda n, b: by_size(n, 'rocketry'), 'LFO tank dated by diameter')
rule(RS, r'^restock-fueltank-adapter', lambda n, b: by_size(n, 'rocketry'), 'adapter tank dated by larger diameter')
rule(RS, r'^restock-(structural-tube|engineplate|adapter|node|truss|decoupler|separator)', lambda n, b: by_size(n, 'materials'), 'structure dated by diameter')
rule(RS, r'^restock-heatshield-1875', 'humanRatedEDL', '1.875 m heat shield')
rule(RS, r'^restock-nosecone', lambda n, b: by_size(n, 'rocketry'), 'nosecone by diameter')
rule(RS, r'^restock-(goocanister|materialbay|sciencebox)', 'scienceSatellite', 'early experiment')
rule(RS, r'^restock-airlock', 'inflatableHabitats', 'inflatable airlock')
rule(RS, r'^restock-claw', 'improvedOrbitalConstruction', 'small grapple')

# ---------------- Squad Expansion ----------------
S = 'SquadExpansion'
rule(S, r'^Deployed', 'surfaceScience', 'Breaking Ground deployable science ~ ALSEP (1969)')
rule(S, r'^RobotArmScanner\.S1', 'surfaceScience', 'robotic arm scanner')
rule(S, r'^RobotArmScanner\.S2', 'scienceExploration', 'robotic arm scanner')
rule(S, r'^RobotArmScanner\.S3', 'sampleReturnScience', 'robotic arm scanner')
rule(S, r'^kv1Pod', 'basicCapsules', 'Vostok-style 1-seat')
rule(S, r'^(kv2Pod|kv3Pod|Mk2Pod)', 'secondGenCapsules', 'Voskhod/Gemini-era pod')
rule(S, r'^(Size1p5|Size4|Size3\.Size4)\.(Tank|Size|EngineAdapter|Adapter)', lambda n, b: by_size(n, 'rocketry'), 'tank dated by diameter (1.875 m ~ 1961, 5 m ~ 1967)')
rule(S, r'^Size1p5\.Monoprop', 'improvedFlightControl', '1.875 m monoprop')
MH_SZ = {'0': 1958, '1': 1960, '1p5': 1961, '2': 1962, '3': 1965, '4': 1967}
def mh_struct(n, b):
    m = re.search(r'(\d(?:p5)?)$', n.replace('.', ''))
    return pick('materials', MH_SZ.get(m.group(1) if m else '', 1958))
rule(S, r'^(Tube|Panel|Triangle|EquiTriangle|EnginePlate|Decoupler|Separator)', mh_struct, 'structure dated by size (1.875 m ~ 1961, 5 m ~ 1967)')
rule(S, r'^(rocketNoseConeSize4|flagPartSize4|fairingSize4)', 'orbitalRocketry1967', '5 m part')
rule(S, r'^HeatShield1p5', 'humanRatedEDL', '1.875 m heat shield')
rule(S, r'^InflatableAirlock', 'inflatableHabitats', 'inflatable airlock')

rule(S, r'^small(Propeller|HeliBlade|FanBlade)|^FanShroud\.01', 'materialsScienceSatellite', 'with the small electric rotor (RP-1 places rotor.01 here)')
rule(S, r'(Propeller|HeliBlade|FanBlade)$|^FanShroud', 'materialsScienceAdvCapsules', 'with the larger rotors (RP-1 places rotor.02/03 here)')
rule(S, r'^ServiceModule25', 'materialsScienceLunar', '2.5 m service module')
rule(S, r'^Size\.1\.5\.Cone', 'orbitalRocketry1961', '1.875 m nose cone')
rule(N, r'^nfe-nuclearfuel', 'advancedNuclearPower', 'reactor fuel container')
rule(N, r'^nfe-nuclear-recycler', 'modernNuclearPower', 'fuel reprocessor')
rule(N, r'^rcsblock-pulsedplasma', 'earlyElecPropulsion', 'pulsed-plasma RCS')
rule(N, r'^rcsblock-hall', 'elecPropulsion1981', 'Hall RCS')
rule(N, r'^rcsblock-gridded', 'elecPropulsion1998', 'gridded-ion RCS ~ DS1')
rule(N, r'^rcsblock-mpdt', 'elecPropulsion2009', 'MPD RCS')
rule('RemoteTech', r'.*', 'lunarRangeComms', 'passive antenna tech')
# ---------------- small mods ----------------
rule('CryoTanks', r'radial', 'earlyHydrolox', 'radial LH2 tank')
rule('CryoTanks', r'^hydrogen-', lambda n, b: {'1.25': 'earlyHydrolox', '2.5': 'improvedHydrolox', '3.75': 'largeHydrolox', '5': 'hydrolox1981', '10': 'hydroloxNF'}.get(size_of(n), 'earlyHydrolox'), 'LH2 tank by diameter (Centaur, S-IVB, S-II, Shuttle ET)')
D = 'DMagicOrbitalScience'
for rx, node, why in [(r'^(dmUS2)?[Mm]ag[Bb]oom|^dmmagBoom', 'scienceSatellite', 'magnetometer boom (1958)'),
                      (r'RPWS|^rpwsAnt', 'deepSpaceScience', 'plasma-wave antenna ~ Voyager'),
                      (r'[Ss]cope$', 'scienceExploration', 'orbital telescope'),
                      (r'SoilMoisture', 'advancedSurfaceScience', 'soil-moisture radiometer ~ SMOS (2009)'),
                      (r'ImagingPlatform', 'deepSpaceScience', 'multispectral imager ~ Landsat (1972)'),
                      (r'GoreSat', 'advModernScience', 'Earth radiometer ~ DSCOVR (2015)'),
                      (r'[Aa][Ss][Ee][Rr][Tt]', 'scienceLunar', 'atmospheric sounder'),
                      (r'^dmRover(Goo|Mat)', 'surfaceScience', 'rover-mounted experiment'),
                      (r'^dmXRay|^dmDAN|^dmsurfacelaser', 'advancedSurfaceScience', 'Curiosity-era instrument (2012)'),
                      (r'SolarCollector|SolarParticles', 'advancedScience', 'solar-wind collector ~ Genesis (2001)'),
                      (r'AnomScanner', 'scienceExploration', 'anomaly scanner'),
                      (r'Bathymetry', 'advancedScience', 'bathymetry'),
                      (r'^dmReconSmall', 'scienceSatellite', 'recon camera ~ Corona (1960)'),
                      (r'^dmReconLarge', 'scienceHuman', 'large recon camera'),
                      (r'^dmSeismic', 'surfaceScience', 'seismometer ~ ALSEP'),
                      (r'^dmbioDrill', 'deepSpaceScience', 'biology drill ~ Viking (1976)'),
                      (r'^dmSIGINT\.Small', 'digitalComms', 'SIGINT ~ GRAB (1960)')]:
    rule(D, rx, node, why)
SS = 'StationScience'
for rx, node, why in [(r'^StnSciLab|^StnSciKib', 'earlySpaceStations', 'station lab ~ Skylab'),
                      (r'^StnSciExperiment[12]$', 'deepSpaceScience', 'station experiment'),
                      (r'^StnSciExperiment[34]$', 'scienceExploration', 'station experiment'),
                      (r'^StnSciExperiment[56]$', 'sampleReturnScience', 'station experiment'),
                      (r'^StnSciExperiment[78]$', 'advancedScience', 'station experiment'),
                      (r'^StnSci(Zoo|Spectro|Cyclo)', 'modularSpaceStations', 'large station facility ~ Mir')]:
    rule(SS, rx, node, why)
rule('DockingPortNext', r'.*', 'standardDockingPorts', 'APAS-style androgynous port')
rule('IndicatorLights', r'.*', 'start', 'cosmetic light')
rule('SurfaceLights', r'.*', 'start', 'cosmetic light')
rule('KerbalEngineer', r'.*', 'start', 'readout part')
rule('PWBFuelBalancer', r'.*', 'improvedFlightControl', 'automatic CoM balancer')
rule('ProceduralParts', r'.*', 'start', 'procedural parts available from start (your rule)')
rule('RestockRigidLegs', r'-1-', 'earlyLanding', 'rigid lander leg')
rule('RestockRigidLegs', r'-2-', 'lunarLanding', 'rigid lander leg')
rule('RestockRigidLegs', r'-3-', 'advancedUncrewedLanding', 'rigid lander leg')
rule('SystemHeat', r'.*', 'nuclearFissionReactors', 'reactor cooling loop')
for i, node in enumerate(['basicAvionics', 'improvedAvionics', 'matureAvionics', 'advancedAvionics'], 1):
    rule('MechJeb2', rf'features{i}$', node, f'MechJeb feature tier {i}')
rule('MechJeb2', r'AR202$', 'earlyAvionics', 'MechJeb core')

BAD_ANALOGUE = {'FSnoseEngineElectric'}  # handled by rules anyway

out, ovr = [], []
for r in rows:
    n, mod, b = r['part'], r['mod'], r['branch']
    final, why, src = None, '', ''
    for m, rx, node, w in R:
        if mod.startswith(m) and rx.search(n):
            if node is None: break
            final = node(n, b) if callable(node) else node; why = w; src = 'reviewed rule'; break
    if final is None:
        if r['confidence'] in ('high', 'medium') and n not in BAD_ANALOGUE:
            final, why, src = r['new_node'], f"like {r['analogue']} ({r['analogue_mod']})", 'analogue (checked)'
        else:
            final, why, src = r['rule_node'], 'kept type + old-tier rule', 'rule'
    assert final == 'start' or final in TL.nodes, (n, final)
    yr = 'start' if final == 'start' else round(TL.x_to_year(TL.nodes[final]['x']))
    out.append(dict(mod=mod, part=n, title=P[n]['title'], before=r['rule_node'], after=final, year=yr, source=src, reason=why))
    if final != r['rule_node'] or src != 'rule':
        ovr.append((n, final, f'batch2 {src}: {why}'))

with open('batch2_review.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
old = {r['part']: r for r in csv.DictReader(open('overrides.csv'))}
for n, node, why in ovr: old[n] = dict(part=n, node=node, reason=why)
with open('overrides.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['part', 'node', 'reason']); w.writeheader(); w.writerows(old.values())
import collections
print(collections.Counter(o['source'] for o in out)); print('overrides now', len(old))
