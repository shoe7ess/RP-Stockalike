# Post-process the generated RP-Stock tree:
#  1. science cost from a smooth year curve (stock-like early game, steady ramp after)
#  2. clean layout: one horizontal lane per branch (extra sub-lanes only where two nodes share a column),
#     lanes ordered so connected branches sit next to each other
#  3. parents trimmed to: previous node in the same branch + at most one cross-branch prerequisite
# usage: RP1=... PARTS=... python3 tools/tree_polish.py build_tree/TechTree/RP0TechTree.cfg
import sys, os, re, json, math, random, collections
sys.path.insert(0, os.path.dirname(__file__))
import treelib as TL, kspcfg as K

path = sys.argv[1]
src = open(path, encoding='utf-8').read()
tree = K.parse(src)
root = [n for n in tree.nodes() if n.name.startswith('@TechTree')][0]
R = {n.get('id'): n for n in root.nodes('RDNode')}

COST = [(1945, 5), (1950, 10), (1955, 20), (1958, 35), (1961, 55), (1964, 80), (1967, 110), (1970, 140),
        (1975, 175), (1980, 210), (1990, 260), (2000, 310), (2010, 360), (2025, 420), (2051, 480)]
def cost_at(y):
    for (y0, c0), (y1, c1) in zip(COST, COST[1:]):
        if y <= y1:
            t = max(0.0, (y - y0) / (y1 - y0))
            return c0 * (c1 / c0) ** t          # geometric between anchors
    return COST[-1][1]

info = {}
for k, n in R.items():
    x, y = [float(v) for v in n.get('pos').split(',')[:2]]
    br = TL.node_branch(k) or TL.node_branch(re.sub(r'Y\d{4}$', '', k)) or 'start'
    info[k] = dict(x=x, y=y, br=br, yr=TL.x_to_year(x), par=[p.get('parentID') for p in n.nodes('Parent') if p.get('parentID') in R])

# ---- 1. costs
def nice(c):
    if c < 20: return int(round(c))
    if c < 100: return int(round(c / 5) * 5)
    return int(round(c / 10) * 10)
for k, n in R.items():
    n.set('cost', '0' if k == 'start' else str(nice(cost_at(info[k]['yr']))))

# ---- 3. parents (done before layout so lane ordering uses the final edges)
bybr = collections.defaultdict(list)
for k, v in info.items(): bybr[v['br']].append(k)
for b in bybr: bybr[b].sort(key=lambda k: (info[k]['x'], k))
newpar = {}
for k, v in info.items():
    if k == 'start': newpar[k] = []; continue
    lst = bybr[v['br']]; i = lst.index(k)
    same = [p for p in lst[:i] if info[p]['x'] < v['x'] - 44]
    prev = same[-1] if same else None
    cross = [p for p in v['par'] if info[p]['br'] != v['br'] and info[p]['x'] < v['x'] - 44]
    # keep the most recent cross-branch prerequisite (it implies the older ones in its own branch)
    cross.sort(key=lambda p: info[p]['x'])
    ps = ([prev] if prev else []) + (cross[-1:] if cross else [])
    if not ps:  # first node of a branch with no usable parent: hang it off the latest earlier node it listed, else start
        ps = [max((p for p in v['par'] if info[p]['x'] < v['x']), key=lambda p: info[p]['x'], default='start')]
    newpar[k] = list(dict.fromkeys(ps))

# ---- 2. layout
COLW = 90.0; LANE = 80.0
# compact columns: merge x values closer than 45, then put columns on an even 90-unit grid (keeps year order)
xs = sorted(set(round(v['x']) for v in info.values())); colof = {}; ci = -1; last = None
for x in xs:
    if last is None or x - last >= 45: ci += 1
    colof[x] = ci; last = x
# one lane per branch: a node that would share a column with an earlier node of its branch (or sit left of a
# parent) slides right one column at a time, so every line runs left-to-right and no two icons touch
lastcol = {}
for k in sorted(info, key=lambda k: (info[k]['x'], k)):
    v = info[k]; c = colof[round(v['x'])]
    c = max([c] + [info[p]['col'] + 1 for p in newpar[k]] + ([lastcol[v['br']] + 1] if v['br'] in lastcol else []))
    v['col'] = c; lastcol[v['br']] = c; v['gx'] = xs[0] + c * COLW
sublanes = {b: (1, {k: 0 for k in lst}) for b, lst in bybr.items()}
branches = [b for b in bybr if b != 'start']
w = collections.Counter()
for k, ps in newpar.items():
    for p in ps:
        a, b = info[k]['br'], info[p]['br']
        if a != b and 'start' not in (a, b): w[tuple(sorted((a, b)))] += 1
def lane_pos(order):
    pos = {}; y = 0
    for b in order: pos[b] = y + (sublanes[b][0] - 1) / 2; y += sublanes[b][0]
    return pos
def score(order):
    pos = lane_pos(order); return sum(c * abs(pos[a] - pos[b]) for (a, b), c in w.items())
random.seed(7)
best = sorted(branches, key=lambda b: -len(bybr[b])); bs = score(best)
for it in range(60000):
    o = best[:]; i, j = random.sample(range(len(o)), 2)
    if random.random() < 0.5: o[i], o[j] = o[j], o[i]
    else: o.insert(j, o.pop(i))
    s = score(o)
    T = max(0.01, 2.0 * (1 - it / 60000))
    if s < bs or random.random() < math.exp((bs - s) / T): best, bs = o, s
order = best
top = 300.0; laneidx = {}; y = 0
for b in order:
    laneidx[b] = y; y += sublanes[b][0]
total_lanes = y
for k, v in info.items():
    n = R[k]
    if k == 'start':
        ly = (total_lanes - 1) / 2
    else:
        ly = laneidx[v['br']] + sublanes[v['br']][1][k]
    n.set('pos', f"{int(round(v['gx']))},{int(round(top + (total_lanes - 1 - ly) * LANE))},-1")
    n.set('scale', '0.6' if k != 'start' else '1')
    # rewrite parents
    n.items = [i for i in n.items if not (i[0] == 'n' and i[1].name == 'Parent')]
    for p in newpar[k]:
        pn = K.Node('Parent'); pn.items = [('v', 'parentID', p), ('v', 'lineFrom', 'RIGHT'), ('v', 'lineTo', 'LEFT')]
        n.items.append(('n', pn))
    n.set('anyToUnlock', 'False')

# sanity: every node reachable from start
kids = collections.defaultdict(list)
for k, ps in newpar.items():
    for p in ps: kids[p].append(k)
seen = {'start'}; st = ['start']
while st:
    for c in kids[st.pop()]:
        if c not in seen: seen.add(c); st.append(c)
assert len(seen) == len(R), f'unreachable: {set(R) - seen}'

hdr = src.split('@TechTree')[0]
open(path, 'w', encoding='utf-8').write(hdr.replace('scaled to ~55,000 total', 'on a smooth year curve') + '\n'.join(K.dump(tree)) + '\n')
eras = [(1945, 1952), (1953, 1957), (1958, 1962), (1963, 1967), (1968, 1972), (1973, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2051)]
era_cost = {}
for a, b in eras:
    ks = [k for k in info if a <= round(info[k]['yr']) <= b and k != 'start']
    era_cost[f'{a}-{b}'] = (len(ks), sum(int(R[k].get('cost')) for k in ks))
json.dump(dict(era_cost=era_cost, node_year={k: info[k]['yr'] for k in info}, node_cost={k: int(R[k].get('cost')) for k in R},
               lanes=order, cross_edges=sum(w.values()), score=bs), open(os.path.join(os.path.dirname(path), 'tree_polish.json'), 'w'), indent=1)
print('total cost', sum(int(R[k].get('cost')) for k in R), 'edges', sum(len(p) for p in newpar.values()), 'cross', sum(w.values()), 'lanes', total_lanes, 'score', round(bs, 1))
for e, (n, c) in era_cost.items(): print(f'  {e}: {n:3d} nodes, {c:6d} science')
print('lane order:', order)
