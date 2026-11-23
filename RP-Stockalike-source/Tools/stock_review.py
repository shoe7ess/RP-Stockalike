# Stock + Making History + ReStock+ pass. ReStock re-models the vanilla parts in place, and ReStock+ fills the gaps,
# so these get hand-placed as one family: each vanilla part by its real-world analogue, each ReStock+ part next to
# the vanilla/MH part it extends. Values are a node name, or (branch, year) -> TL.pick.
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL

P = json.load(open('rp1/parts.json'))['parts']
old = {r['part']: r for r in csv.DictReader(open('overrides.csv'))}

S = {  # ---------------- vanilla (Squad)
 # engines
 'liquidEngine': (('rocketry', 1949), 'Reliant ~ first liquid booster engine'),
 'liquidEngine.v2': (('rocketry', 1949), 'Reliant ~ first liquid booster engine'),
 'liquidEngine2': (('rocketry', 1954), 'Swivel: first gimballed engine'),
 'liquidEngine2.v2': (('rocketry', 1954), 'Swivel: first gimballed engine'),
 'liquidEngine3.v2': (('rocketry', 1959), 'Terrier ~ Able/AJ10 upper stage'),
 'liquidEngine2-2.v2': (('rocketry', 1963), 'Poodle ~ 2.5 m upper stage'),
 'engineLargeSkipper.v2': (('rocketry', 1964), 'Skipper ~ S-IV era'),
 'liquidEngineMainsail.v2': (('rocketry', 1965), 'Mainsail ~ H-1/F-1 era'),
 'Size3AdvancedEngine': (('rocketry', 1967), 'Rhino ~ Saturn era'),
 'Size3EngineCluster': (('rocketry', 1967), 'Mammoth ~ F-1 cluster (kerolox, not methalox)'),
 'Size2LFB': (('rocketry', 1986), 'Twin-Boar ~ RD-170 era'), 'Size2LFB.v2': (('rocketry', 1986), 'Twin-Boar ~ RD-170 era'),
 'microEngine.v2': (('rocketry', 1961), 'Ant: tiny vacuum engine'),
 'liquidEngineMini.v2': (('rocketry', 1962), 'Spark: small probe engine'),
 'radialLiquidEngine1-2': (('rocketry', 1962), 'Twitch'),
 'smallRadialEngine': (('rocketry', 1963), 'Thud'), 'smallRadialEngine.v2': (('rocketry', 1963), 'Thud'),
 'toroidalAerospike': (('rocketry', 1998), 'Dart ~ X-33 aerospike (1998)'),
 'nuclearEngine': ('earlyNuclearPropulsion', 'Nerv ~ NERVA'),
 'JetEngine': (('flight', 1958), 'Wheesley ~ early turbofan'), 'turboJet': (('flight', 1964), 'Whiplash ~ J58 (1962)'),
 'turboFanEngine': (('flight', 1970), 'Panther: afterburning turbofan'), 'miniJetEngine': (('flight', 1949), 'Juno: small turbojet'),
 'solidBooster.sm.v2': ('earlySolids', 'Flea'), 'solidBooster.v2': ('basicSolids', 'Hammer'),
 'solidBooster1-1': ('solids1958', 'Thumper'), 'MassiveBooster': ('solids1964', 'Kickback ~ Titan III SRM'),
 'Shrimp': ('solids1958', 'Shrimp: small SRB'), 'Mite': ('solids1956', 'Mite: tiny SRB'),
 'Thoroughbred': ('solids1981', 'Thoroughbred ~ Shuttle SRB'), 'Clydesdale': ('solids1981', 'Clydesdale ~ Shuttle SRB'),
 'LaunchEscapeSystem': ('basicCapsules', 'LES ~ Mercury (1961)'),
 # tanks
 'fuelTankSmallFlat': ('rocketryTesting', 'FL-T100'), 'fuelTankSmall': ('rocketryTesting', 'FL-T200'),
 'fuelTank': ('earlyRocketry', 'FL-T400'), 'fuelTank.long': ('basicRocketryRP0', 'FL-T800'),
 'externalTankCapsule': (('rocketry', 1961), 'Dumpling probe tank'), 'externalTankRound': (('rocketry', 1961), 'Baguette probe tank'),
 'externalTankToroid': (('rocketry', 1961), 'Doughnut probe tank'),
 'adapterSize2-Size1': (('rocketry', 1961), '2.5-1.25 tank adapter'), 'adapterSize2-Size1Slant': (('rocketry', 1961), '2.5-1.25 tank adapter'),
 'Size3SmallTank': (('rocketry', 1965), 'Kerbodyne 3.75 m ~ Saturn'), 'Size3MediumTank': (('rocketry', 1965), 'Kerbodyne 3.75 m ~ Saturn'),
 'Size3LargeTank': (('rocketry', 1965), 'Kerbodyne 3.75 m ~ Saturn'), 'Size3To2Adapter.v2': (('rocketry', 1965), '3.75-2.5 adapter'),
 'rcsTankMini': ('earlyFlightControl', 'small RCS tank'), 'radialRCSTank': ('earlyFlightControl', 'radial RCS tank'),
 'rcsTankRadialLong': ('stabilityRP0', 'radial RCS tank'), 'RCSFuelTank': ('stabilityRP0', '1.25 m RCS tank'),
 'RCSTank1-2': ('improvedFlightControl', '2.5 m RCS tank'),
 # command / probes
 'landerCabinSmall': ('lunarLanding', 'Mk1 lander can ~ LM'), 'mk2LanderCabin': ('lunarLanding', 'Mk2 lander can ~ LM'),
 'mk2LanderCabin.v2': ('lunarLanding', 'Mk2 lander can ~ LM'),
 'probeCoreSphere.v2': ('earlyAvionics', 'Stayputnik ~ Sputnik (1957)'), 'probeCoreOcto2.v2': ('matureAvionics', 'OKTO2'),
 'probeCoreCube': ('internationalAvionics', 'QBE ~ CubeSat (2003)'), 'probeStackSmall': ('largeScaleAvionics', 'RC-001S'),
 'probeStackLarge': ('advancedAvionics', 'RC-L01'), 'MpoProbe': ('advModernAvionics', 'BepiColombo MPO (2018)'),
 'MtmStage': ('advModernAvionics', 'BepiColombo MTM (2018)'),
 # control / docking
 'sasModule': ('stabilityRP0', 'small reaction wheel'), 'advSasModule': ('improvedFlightControl', '1.25 m reaction wheel'),
 'asasmodule1-2': ('spaceStationControl', '2.5 m reaction wheel'),
 'dockingPort2': ('dockingCrewTransfer', 'Clamp-O-Tron ~ Apollo probe/drogue'), 'dockingPort1': ('dockingCrewTransfer', 'shielded Clamp-O-Tron'),
 'dockingPortLarge': ('standardDockingPorts', 'Clamp-O-Tron Sr.'), 'dockingPortLateral': ('standardDockingPorts', 'inline Clamp-O-Tron'),
 # EDL / landing / rovers
 'HeatShield0': ('entryDescentLanding', '0.625 m heat shield'), 'HeatShield1': ('humanRatedEDL', '1.25 m heat shield, needed by the Mk1 pod'),
 'InflatableHeatShield': ('HIAD', 'inflatable heat shield ~ HIAD'),
 'parachuteRadial': ('entryDescentLanding', 'radial chute'), 'parachuteDrogue': ('entryDescentLanding', 'drogue chute'),
 'parachuteLarge': ('humanRatedEDL', 'large chute'), 'radialDrogue': ('entryDescentLanding', 'radial drogue'),
 'landingLeg1': ('earlyLanding', 'LT-1 leg'), 'miniLandingLeg': ('earlyLanding', 'LT-05 leg ~ Surveyor'),
 'roverWheel1': ('advancedUncrewedLanding', 'RoveMax M1 ~ LRV (1971)'), 'roverWheel2': ('advancedUncrewedLanding', 'RoveMax S2 ~ Lunokhod'),
 'wheelMed': ('interplanetaryRovers', 'TR-2L wheel'),
 # power / comms / science
 'batteryBankLarge': ('electronicsHuman', 'Z-4K battery'), 'solarPanels5': ('primitiveSolarPanels', 'OX-STAT ~ Vanguard (1958)'),
 'rtg': ('earlyRTG', 'PB-NUK ~ SNAP-9'),
 'HighGainAntenna': ('advancedComms', 'HG-55'), 'RelayAntenna5': ('improvedComms', 'RA-2 relay ~ Syncom'),
 'RelayAntenna50': ('advancedComms', 'RA-15 relay'), 'RelayAntenna100': ('deepSpaceComms', 'RA-100 relay'),
 'GooExperiment': ('earlyScience', 'Mystery Goo'), 'science.module': ('scienceSatellite', 'Materials Bay'),
}
MH = {  # ---------------- Making History
 'LiquidEngineRK-7': (('rocketry', 1957), 'Kodiak ~ RD-107'), 'LiquidEngineKE-1': (('rocketry', 1965), 'Mastodon'),
 'LiquidEngineLV-T91': (('rocketry', 1963), 'Cheetah'), 'LiquidEngineLV-TX87': (('rocketry', 1961), 'Bobcat'),
 'LiquidEngineRE-I2': (('rocketry', 1965), 'Skiff'), 'LiquidEngineRE-J10': (('rocketry', 1966), 'Wolfhound ~ J-2 class'),
 'LiquidEngineRV-1': ('earlyFlightControl', 'Cub vernier (was mis-sorted as nuclear)'), 'Pollux': ('solids1966', 'Pollux 1.875 m SRB'),
}
RS = {  # ---------------- ReStock+ next to their vanilla / MH counterparts
 'restock-engine-125-valiant': (('rocketry', 1949), 'LV-T15: precedes the Reliant'),
 'restock-engine-torch': (('rocketry', 1958), 'Torch: small booster'),
 'restock-engine-125-pug': (('rocketry', 1959), 'Pug: small upper stage, with the Terrier'),
 'restock-engine-375-corgi': (('rocketry', 1967), 'Corgi cluster, with the Rhino'),
 'restock-engine-boar': (('rocketry', 1986), 'single Boar, with the Twin-Boar'),
 'restock-engine-ursa-1': (('rocketry', 1957), 'Ursa ~ Kodiak'), 'restock-engine-galleon-1': (('rocketry', 1965), 'Galleon ~ Mastodon'),
 'restock-engine-caravel-1': (('rocketry', 1966), 'Caravel ~ Wolfhound'), 'restock-engine-schnauzer-1': (('rocketry', 1965), 'Schnauzer ~ Skiff'),
 'restock-engine-panda-1': ('earlyFlightControl', 'vernier, with the Cub'),
 'restock-engine-les-2': ('basicCapsules', 'small LES, with the LES'),
 'restock-srb-mallet-1': ('basicSolids', 'Mallet, with the Hammer'), 'restock-srb-striker-1': ('solids1958', 'Striker, with the Thumper'),
 'restock-srb-castor-1': ('solids1966', 'Castor, with the Pollux'),
 'restock-reactionwheel-radial-1': ('stabilityRP0', 'small radial reaction wheel'),
 'restock-reactionwheel-1875-1': ('improvedFlightControl', '1.875 m reaction wheel, between 1.25 and 2.5'),
 'restock-rcs-block-dual-mini-1': ('earlyFlightControl', 'mini RCS'), 'restock-rcs-block-multi-mini-2': ('earlyFlightControl', 'mini RCS'),
 'restock-rcs-block-quad-angled-mini-1': ('earlyFlightControl', 'mini RCS'), 'restock-rcs-block-quad-mini-1': ('earlyFlightControl', 'mini RCS'),
 'restock-rcs-block-qunit-mini-1': ('earlyFlightControl', 'mini RCS'), 'restock-rcs-block-triple-angled-mini-1': ('earlyFlightControl', 'mini RCS'),
 'restock-rcs-single-mini-1': ('earlyFlightControl', 'mini RCS'),
 'restock-battery-1875-1': ('electronicsHuman', 'Z-2.5K, between Z-1K and Z-4K'), 'restock-battery-375-1': ('electronicsSpaceStation', 'Z-10K'),
 'restock-drone-core-0625-1': ('matureAvionics', 'RC-XS1'), 'restock-drone-core-1875-1': ('largeScaleAvionics', 'RC-M001, with RC-001S'),
 'restock-drone-core-375-1': ('advancedAvionics', 'RC-XL001, with RC-L01'),
 'restock-antenna-stack-2': ('improvedComms', 'fixed DTS-M1'), 'restock-antenna-stack-3': ('advancedComms', 'budget HG-55'),
 'restock-relay-radial-2': ('improvedComms', 'long-range HG-5 relay'), 'restock-relay-radial-2.v2': ('improvedComms', 'long-range HG-5 relay'),
 'restock-docking-375-1': ('largeDockingPorts', "Clamp-O-Tron 'Grande', after the Sr."),
 'restock-claw-625-1': ('spaceStationControl', 'small claw, with the Klaw'),
 'restock-pod-sphere-1': ('basicCapsules', 'Vostok-style, like kv1'), 'restock-pod-sphere-2': ('secondGenCapsules', 'like kv2'),
 'restock-pod-sphere-3': ('secondGenCapsules', 'like kv3'), 'restock-mk2-pod': ('secondGenCapsules', 'like MH Mk2 pod'),
 'restock-decoupler-1875-1': (('materials', 1961), '1.875 m decoupler'), 'restock-separator-1875-1': (('materials', 1961), '1.875 m separator'),
 'restock-nosecone-1875-1': (('rocketry', 1961), '1.875 m nose'),
 'restock-adapter-hollow-25-375-1': (('materials', 1965), '2.5-3.75 adapter'), 'restock-adapter-skeletal-25-375-1': (('materials', 1965), '2.5-3.75 adapter'),
 'restock-service-bay-1875-1': ('materialsScienceHuman', '1.875 m service bay'), 'restock-service-module-1875-1': ('materialsScienceHuman', '1.875 m service module'),
 'restock-service-module-125-625-1': ('materialsScienceSatellite', 'small service module, with the 1.25 m bay'),
 'restock-goocanister-625-1': ('earlyScience', 'with Mystery Goo'), 'restock-materialbay-radial-1': ('scienceSatellite', 'with the Materials Bay'),
 'restock-sciencebox-stack-1': ('scienceHuman', 'with Experiment Storage'),
 'restock-fueltank-saturn-engine-1': (('rocketry', 1967), '5 m engine adapter tank'),
 'restock-wheel-1-T': ('advancedUncrewedLanding', 'with RoveMax M1'), 'restock-wheel-4': ('advancedUncrewedLanding', 'with the M1-F wheel'),
 'restock-truss-3': ('start', 'with the stock girders'), 'restock-truss-hub-1': ('start', 'with the stock girders'),
 'restock-truss-adapter-0625-1': ('start', 'with the stock girders'),
}
MH['roverWheelM1-F'] = ('advancedUncrewedLanding', 'RoveMax M1-F ~ LRV')

n_ch = 0
for table in (S, MH, RS):
    for part, (tgt, why) in table.items():
        if part not in P: print('not installed:', part); continue
        node = TL.pick(*tgt) if isinstance(tgt, tuple) else tgt
        assert node == 'start' or node in TL.nodes, (part, node)
        old[part] = dict(part=part, node=node, reason=f'stock/restock review: {why}'); n_ch += 1
with open('overrides.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['part', 'node', 'reason']); w.writeheader(); w.writerows(old.values())
print('set', n_ch, 'overrides', len(old))
