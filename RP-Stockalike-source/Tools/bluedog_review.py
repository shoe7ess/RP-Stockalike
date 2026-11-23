# Bluedog pass: re-date sub-generations inside multi-decade families (Thor/Delta/Titan/Centaur/Atlas),
# the un-familied Solids/Engines folders, and a few spot fixes. Appends to overrides.csv, writes bluedog_review.csv
import sys, os, re, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL

P = json.load(open('rp1/parts.json'))['parts']
place = {r['part']: r for r in csv.DictReader(open('build_tree/TechTree/part_placement.csv'))}
old = {r['part']: r for r in csv.DictReader(open('overrides.csv'))}

Y = [  # (regex on name without bluedog. prefix, year, why) -- first match wins
    # Redstone family: mostly Mercury-Redstone, plus Juno I and the later Sparta
    (r'^Redstone\.', 1960, 'Mercury-Redstone (1960-61)'), (r'^(Juno1|Sergeant|Beacon1)', 1958, 'Juno I / Explorer 1 (1958)'),
    (r'^Sparta', 1966, 'Sparta (1966)'), (r'^WRESAT', 1967, 'WRESAT (1967)'), (r'^ThorAble', 1958, 'Thor-Able (1958)'),
    # Thor / Delta
    (r'^Thor\.AbleAdapter', 1958, 'Thor-Able (1958)'), (r'^Ablestar', 1960, 'Thor-Ablestar (1960)'),
    (r'^Thor\.', 1957, 'Thor IRBM (1957)'), (r'^Delta\.(DoubleBarrel|Fin|Interstage|Avionics|Miniskirt)', 1960, 'Thor-Delta (1960)'),
    (r'^DeltaE', 1965, 'Delta E (1965)'), (r'^HOSS', 1970, 'Delta upper stage concept (~1970)'), (r'^DeltaIII', 1998, 'Delta III (1998)'),
    (r'^DeltaP', 1972, 'Delta-P second stage (1972)'), (r'^TR\.201', 1972, 'TR-201 (1972)'), (r'^AJ10\.118F', 1972, 'AJ10-118F (1972)'),
    (r'^AJ10\.118X', 1975, 'AJ10-118X'), (r'^(AJ10\.118K|DeltaK)', 1982, 'Delta K stage (1982)'),
    (r'^Delta2', 1989, 'Delta II (1989)'), (r'^Delta\.GEM40', 1990, 'GEM-40 (1990)'), (r'^Delta\.GEM46', 1998, 'GEM-46 (1998)'),
    (r'^Delta\.GEM60', 2002, 'GEM-60 (2002)'), (r'^(Delta4|DeltaIV|DCSS)', 2002, 'Delta IV / DCSS (2002)'),
    # Titan
    (r'^Titan1\.', 1959, 'Titan I (1959)'), (r'^LR(87|91)$', 1959, 'Titan I engine (1959)'),
    (r'^LR(87|91)\.3', 1962, 'Titan II engine (1962)'), (r'^LR87\.(Single|11\.Single)', 1965, 'single-chamber LR87 variant'),
    (r'^LR(87|91)\.5', 1965, 'Titan III engine (1965)'), (r'^LR(87|91)\.11', 1989, 'Titan IV engine (1989)'),
    (r'^LR87\.LH2', 1962, 'LR87 hydrogen test variant (early 60s)'),
    (r'^Titan23G', 1988, 'Titan 23G (1988)'), (r'^Titan3E', 1974, 'Titan IIIE (1974)'), (r'^Titan4', 1989, 'Titan IV (1989)'),
    (r'^Titan3', 1965, 'Titan III (1965)'), (r'^Titan2\.', 1962, 'Titan II (1962)'), (r'^Titan\.S[12]\.', 1962, 'Titan II core (1962)'),
    (r'^Titan\.(Transtage|SRB)', 1965, 'Titan III Transtage/SRB (1965)'), (r'^UA120[2-5]?$', 1965, 'UA1205 SRM (1965)'),
    (r'^UA1206', 1982, 'UA1206 (Titan 34D, 1982)'), (r'^UA120[78]', 1989, 'UA1207 (Titan IV, 1989)'), (r'^SRMU', 1997, 'SRMU (1997)'),
    (r'^1875\.', 1965, 'Titan III SRB fittings (1965)'), (r'^IDCSP\.Truss', 1966, 'IDCSP (1966)'),
    # Centaur / Atlas
    (r'^CentaurD\.FuelTank', 1965, 'Centaur D (1965)'), (r'^CentaurT', 1994, 'Centaur-T (1994)'), (r'^CentaurIII', 2002, 'Centaur III (2002)'),
    (r'^CELV', 1990, 'Atlas I/II-era tankage (1990)'), (r'^Atlas2\.', 1991, 'Atlas II (1991)'), (r'^Atlas\.CELV', 1990, 'Atlas I/II-era'),
    # Saturn / Apollo fixes
    (r'^Saturn\.S1\.(Large|Small)Fin', 1961, 'Saturn I (1961)'), (r'^Saturn\.AJ260', 1965, 'AJ-260 test firings (1965)'),
    (r'^ALSEP\.', 1969, 'ALSEP (1969-72)'), (r'^Apollo\.Block1', 1966, 'Apollo Block I (1966)'),
    # Solids folder
    (r'^Scout\.', 1960, 'Scout (1960)'), (r'^Minuteman\.', 1962, 'Minuteman (1962)'), (r'^Castor2', 1964, 'Castor II (1964)'),
    (r'^Castor\.RadialDecoupler', 1964, 'Castor strap-on (1964)'), (r'^Castor4XL', 1989, 'Castor IVA-XL (1989)'), (r'^Castor4', 1971, 'Castor IV (1971)'),
    (r'^Burner2', 1966, 'Burner II (1966)'), (r'^IUS\.', 1982, 'IUS (1982)'), (r'^Peacekeeper\.', 1986, 'Peacekeeper (1986)'),
    (r'^Pegasus\.(Avionics|Decoupler|Fin|Orion|Strongback)', 1990, 'Pegasus (1990)'), (r'^HAPS', 1991, 'HAPS (1991)'),
    (r'^TOS\.', 1992, 'TOS (1992)'), (r'^Taurus\.', 1994, 'Taurus (1994)'), (r'^Athena\.Castor30XL', 2013, 'Castor 30XL (2013)'),
    (r'^Athena\.Castor30', 2009, 'Castor 30 (2009)'), (r'^Athena3', 2020, 'Athena III'), (r'^Athena\.', 1995, 'Athena (1995)'),
    (r'^Minotaur', 2000, 'Minotaur (2000)'), (r'^UpperSolids\.Altair', 1958, 'Altair (1958)'), (r'^UpperSolids\.BE3', 1960, 'BE-3 (1960)'),
    (r'^UpperSolids\.Star37B$', 1966, 'Surveyor retro motor (1966)'), (r'^UpperSolids\.Star24', 1967, 'Star 24'),
    (r'^UpperSolids\.Star37', 1980, 'Star 37 family'), (r'^UpperSolids\.Star48', 1982, 'Star 48 (PAM-D, 1982)'),
    # Engines folder
    (r'^E1\.engine', 1958, 'Rocketdyne E-1 (1958)'), (r'^M1$', 1965, 'M-1 (1965)'), (r'^MB60', 2009, 'MB-60 (2000s)'),
    (r'^XLR129', 1970, 'XLR-129 (1970)'), (r'^NERVA\.FF', 1972, 'NERVA flight engine'), (r'^NERVA\.XE', 1969, 'NERVA XE (1969)'),
    (r'^NERVA\.II', 1972, 'NERVA II'),
]
FIX = {'bluedog.Athena.OAM': ('largeSpaceplaneControl', 'Athena orbit-adjust module (hydrazine), 1995'), 'bluedog.LRV.Wheel': ('advancedUncrewedLanding', 'LRV (1971); the rover branch starts in 1992')}

out = []
for n, r in place.items():
    if r['mod'] != 'Bluedog_DB' or r['how placed'] == 'RP-1 database': continue
    if n in old and not old[n]['reason'].startswith('bluedog'): continue
    short = re.sub(r'^[Bb]luedog\.', '', n)
    node = why = None
    if n in FIX: node, why = FIX[n]
    else:
        for rx, yr, w in Y:
            if re.search(rx, short):
                b = r['branch']; node = 'start' if b not in TL.B else TL.pick(b, yr); why = w; break
    if node and node != r['RP-0 node']:
        old[n] = dict(part=n, node=node, reason=f'bluedog review: {why}')
        out.append(dict(part=n, title=P[n]['title'], before=r['RP-0 node'], after=node, reason=why))
with open('overrides.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['part', 'node', 'reason']); w.writeheader(); w.writerows(old.values())
with open('bluedog_review.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['part', 'title', 'before', 'after', 'reason']); w.writeheader(); w.writerows(out)
print('changed', len(out), 'overrides', len(old))
