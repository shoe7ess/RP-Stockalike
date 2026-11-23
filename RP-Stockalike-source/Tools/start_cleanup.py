# Start node = sounding rockets only (WAC Corporal / Aerobee class), their launch stands and the basic sensors they flew.
# Everything else that was sitting in Start moves to the node for the year it belongs to (V-2 testing, early aviation, ...).
import csv, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL

place = list(csv.DictReader(open('build_tree/TechTree/part_placement.csv')))
ovr = {r['part']: r for r in csv.DictReader(open('overrides.csv'))}

KEEP = [r'^tbee-taerobee-', r'^Capella', r'^CapellaParachute', r'^sensorThermometer$', r'^sensorBarometer$', r'^ca\.(thermometer|barometer)$',
        r'^basicFin$', r'^noseCone$', r'^launchClamp1$', r'^SR\.LaunchStick$', r'^TacSelfDestruct$', r'^Engineer(7500|Chip)$', r'^NodeHelper$',
        r'^fs(infopopup|trimgadget)$', r'^procedural(TankLiquid|TankSRB|StackDecoupler)$',
        r'^AM\.MLP\.(AerobeeLaunchStand|LaunchRailMini|LaunchRailSmall|MilkstoolLaunchStand1|MilkstoolMini1S|SmallLaunchStand|SmallLaunchStandRect|LaunchPlateRnd1|FlatLaunchBaseMini|GenBaseMicro)$']
# (regex, node or (branch, year), why) - first match wins
MOVE = [
    (r'^(FS|fs)', 'supersonicDev', 'pre-jet aviation, first flight node'),
    (r'^(GearFixed|GearFree|StandardCtrlSrf|smallCtrlSrf|elevon\d|structuralWing\d?|wingConnector\d?|winglet\d?|navLight1)$', 'supersonicDev', 'aircraft structure, first flight node'),
    (r'^(tailfin|standardNoseCone|Decoupler\.0|radialDecoupler|restock-decoupler-radial-tiny-1|bluedog\.Decoupler\.0p625m|ReleaseValve|parachuteSingle|fireworksLauncherSmall|SurfAntenna|sensorAccelerometer|ca\.accelerometer|bluedog\.cameraLowTech)$',
     'rocketryTesting', 'V-2 test era (1946): staging, recovery, telemetry, film'),
    (r'^castor\.decoupler\.s0(p5)?\.1$', 'rocketryTesting', 'small decoupler, V-2 era'),
    (r'^RC\.', ('edl', 1955), 'RealChute, early recovery systems'),
    (r'^proceduralHeatshield$', ('edl', 1958), 'heat shields arrive with reentry work'),
    (r'^proceduralBattery$', ('electronics', 1955), 'batteries with early electronics'),
    (r'^indicatorLightSmall$', ('electronics', 1955), 'indicator lights'),
    (r'^USI\.DeomlitionBlock$', ('materials', 1960), 'demolition charge'),
    (r'^AM\.MLP\.(RedstoneLaunchStand|LaunchRailMedium)$', ('materials', 1953), 'Redstone era pad hardware (1953)'),
    (r'^AM\.MLP\.(LaunchRailLarge)$', ('materials', 1955), 'large launch rail (Nike-Hercules, 1955)'),
    (r'^AM\.MLP\.(JupiterPetalCover|ThorLaunchStand|ThorServiceTowerFallback|GeneralFallbackUmbilicalTower|GeneralUmbilicalDroopB|LaunchStandServiceTower1|LaunchStandServiceTower4)$', ('materials', 1957), 'IRBM pad hardware (1957)'),
    (r'^AM\.MLP\.(AtlasLaunchStand|AtlasUmbilicalArmAgena)$', ('materials', 1959), 'Atlas pad (1959)'),
    (r'^AM\.MLP\.(LaunchStandCrewElevatorMercury)$', ('materials', 1960), 'Mercury-Redstone crew access (1960)'),
    (r'^AM\.MLP\.(AtlasUmbilicalArmCentaur|CrewElevatorAtlasUmbilical|LaunchStandCrewElevatorAtlas|LaunchStandCrewWalkwayMercury|TitanIILaunchStand|TitanIIServiceTowerMast|TitanIIServiceTowerSingle|TitanIIServiceTowerUmbilical2)$', ('materials', 1962), 'Mercury-Atlas / Titan II pads (1962)'),
    (r'^AM\.MLP\.(LaunchStandCrewElevatorGemini|TitanIIServiceTowerUmbilicalGem2)$', ('materials', 1964), 'Gemini crew access (1964)'),
    (r'^canopus\.(basic\.fin|fairing\.s(0p5|1))\.', None, 1957, 'Tantares LV small fairings/fins (1957)'),
    (r'^canopus\.fairing\.s1p5\.', None, 1960, 'Tantares LV fairing (1960)'),
    (r'^canopus\.fairing\.s2\.', None, 1965, 'Tantares LV fairing (1965)'),
    (r'^canopus\.fairing\.s3\.', None, 1967, 'Tantares LV fairing (1967)'),
    (r'^castor\.decoupler\.s1(p5)?\.', None, 1957, 'Tantares decoupler (1957)'),
    (r'^castor\.decoupler\.s2\.', None, 1965, 'Tantares decoupler (1965)'),
    (r'^castor\.decoupler\.s3\.', None, 1967, 'Tantares decoupler (1967)'),
    (r'^castor\.decoupler\.s[46]\.', None, 1969, 'Tantares decoupler (N1, 1969)'),
    (r'^andromeda\.', None, 1961, 'Tantares Vostok-era hardware (1961)'),
    (r'^petra\.', None, 1967, 'Soyuz-era docking (1967)'),
    (r'^hydra\.', None, 1967, 'Proton hardware (1967)'),
    (r'^(lk|libra)\.', None, 1969, 'N1-L3 / LK hardware (1969)'),
]
moved = []
for r in place:
    if r['RP-0 node'] != 'start': continue
    n = r['part']
    if any(re.search(rx, n) for rx in KEEP): continue
    hit = None
    for m in MOVE:
        if re.search(m[0], n): hit = m; break
    if not hit:
        print('UNHANDLED', n, r['title'], r['branch']); continue
    if len(hit) == 3:
        tgt, why = hit[1], hit[2]
        node = tgt if isinstance(tgt, str) else TL.pick(*tgt)
    else:
        node = TL.pick(r['branch'], hit[2]); why = hit[3]
    ovr[n] = dict(part=n, node=node, reason=f'start cleanup: {why}')
    moved.append((n, node))
with open('overrides.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['part', 'node', 'reason']); w.writeheader(); w.writerows(ovr.values())
print('moved', len(moved))
import collections; print(collections.Counter(n for _, n in moved))
