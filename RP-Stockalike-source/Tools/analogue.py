# Place parts RP-1 doesn't know by finding their closest analogue among parts RP-1 DOES place.
# usage: analogue.py parts.json part_placement.csv out.csv MOD [MOD...]
import sys, os, re, json, csv, math, difflib, collections
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL

P = json.load(open(sys.argv[1]))['parts']
rows = {r['part']: r for r in csv.DictReader(open(sys.argv[2]))}
OUT = sys.argv[3]; MODS = set(sys.argv[4:])

IGNORE_MODS = {'TweakScale', 'KSPeVA', 'ModuleTestSubject', 'ModulePartVariants', 'ModuleCargoPart', 'FlagDecal', 'ModuleB9PartSwitch',
               'ModuleTripLogger', 'ModuleConductionMultiplier', 'ModuleColorChanger', 'ModuleAnimateGeneric', 'ModuleLight',
               'KSPWheelBase', 'ModuleSurfaceFX', 'FXModuleAnimateThrottle', 'ModuleJettison', 'ModuleDragModifier',
               'ModuleCoreHeat', 'ModuleKerbNetAccess', 'ModuleProbeControlPoint', 'ModuleInventoryPart', 'ModuleToggleCrossfeed',
               'ModuleTagList', 'ModuleSimpleAdjustableFairing', 'ModuleRestockModifyFairingMaterials', None}
def mods(p): return {m for m in p['mods'] if m not in IGNORE_MODS}
def toks(s): return {t for t in re.split(r'[^a-z0-9]+', (s or '').lower()) if t and not t.isdigit() and len(t) > 1}
def sizes(p): return {t.strip() for t in (p['size'] or '').split(',') if t.strip()}
def mass(p):
    try: return max(float(p['mass']), 1e-4)
    except: return None
def norm(n): return re.sub(r'\.v\d+$|\.\d+$', '', n.lower())

ref = [(n, P[n], rows[n]) for n in rows if rows[n]['how placed'] == 'RP-1 database' and n in P]

def score(a, pa, b, pb, branch_a, branch_b):
    s = 0.0; why = []
    if branch_a == branch_b: s += 3; why.append('same type')
    ma, mb = mods(pa), mods(pb)
    if ma or mb:
        j = len(ma & mb) / len(ma | mb); s += 2 * j
    ta, tb = toks(pa['title']), toks(pb['title'])
    if ta and tb:
        j = len(ta & tb) / len(ta | tb); s += 1.5 * j
        if j > .4: why.append('similar name')
    r = difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(); s += 1.5 * r
    if norm(a) == norm(b): s += 4; why.append('same part, other version')
    sa, sb = sizes(pa), sizes(pb)
    if sa and sb and sa & sb: s += 1; why.append('same size')
    m1, m2 = mass(pa), mass(pb)
    if m1 and m2: s += 1.0 / (1 + abs(math.log(m1 / m2)))
    if pa['mod'] == pb['mod']: s += 1
    if pa['file'].rsplit('/', 1)[0] == pb['file'].rsplit('/', 1)[0]: s += .5; why.append('same folder')
    if (pa['res'] and set(pa['res']) == set(pb['res'])): s += .5
    if pa['props'] and set(pa['props']) == set(pb['props']): s += 1; why.append('same propellants')
    return s, why

out = []
for n, r in rows.items():
    if r['mod'] not in MODS or r['how placed'] == 'RP-1 database' or n not in P: continue
    pa = P[n]; ba = r['branch']
    best = sorted(((*score(n, pa, m, pm, ba, rm['branch']), m, rm) for m, pm, rm in ref if m != n), key=lambda x: -x[0])[:3]
    s, why, m, rm = best[0]
    conf = 'high' if s >= 9 else 'medium' if s >= 7 else 'low'
    an = rm['RP-0 node']
    if conf == 'low':
        new = r['RP-0 node']; how = 'kept rule placement (no good analogue)'
    elif an == 'start' or TL.node_branch(an) == ba:
        new = an; how = 'same node as analogue'
    else:
        yr = TL.x_to_year(TL.nodes[an]['x']); new = TL.pick(ba, yr); how = f'analogue era ({yr:.0f}) in its own branch'
    out.append(dict(mod=r['mod'], part=n, title=pa['title'], branch=ba, rule_node=r['RP-0 node'], new_node=new,
                    analogue=m, analogue_title=P[m]['title'], analogue_mod=P[m]['mod'], score=round(s, 1), confidence=conf, method=how,
                    why=', '.join(why), runner_up=f"{best[1][2]} ({best[1][3]['RP-0 node']})" if len(best) > 1 else ''))
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(sorted(out, key=lambda x: (x['mod'], -x['score'])))
c = collections.Counter((o['mod'], o['confidence']) for o in out)
for k in sorted(c): print(k, c[k])
