# High-resolution, presentable render of the RP-Stock tech tree (for sharing).
import sys, os, re, json, collections, textwrap
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K
from PIL import Image, ImageDraw, ImageFont

TREE, POLISH, ICONS, OUT = sys.argv[1:5]
t = K.parse(open(TREE).read()); root = [n for n in t.nodes() if n.name.startswith('@TechTree')][0]
N = {n.get('id'): n for n in root.nodes('RDNode')}
pol = json.load(open(POLISH))
lanes = pol['lanes']
import treelib as TL
def br(k): return TL.node_branch(k) or TL.node_branch(re.sub(r'Y\d{4}$', '', k)) or 'start'

F = '/usr/share/fonts/opentype/inter/Inter-'
f_title = ImageFont.truetype(F + 'Bold.otf', 64); f_sub = ImageFont.truetype(F + 'Regular.otf', 30)
f_lane = ImageFont.truetype(F + 'SemiBold.otf', 24); f_node = ImageFont.truetype(F + 'SemiBold.otf', 17)
f_cost = ImageFont.truetype(F + 'Medium.otf', 15); f_year = ImageFont.truetype(F + 'SemiBold.otf', 20)
f_era = ImageFont.truetype(F + 'Bold.otf', 22); f_foot = ImageFont.truetype(F + 'Regular.otf', 22)

LABEL = {'rocketry': 'Orbital Rocketry', 'staged': 'Staged Combustion', 'hydrolox': 'Hydrolox Engines', 'solids': 'Solid Rockets',
         'elec': 'Electric Propulsion', 'nuclearProp': 'Nuclear Propulsion', 'flight': 'Aircraft', 'spaceplanes': 'Spaceplanes',
         'capsules': 'Crew Capsules', 'control': 'Flight Control', 'docking': 'Docking', 'edl': 'Entry & Descent', 'landing': 'Landing',
         'rovers': 'Rovers', 'stations': 'Space Stations', 'lifesupport': 'Life Support & ISRU', 'materials': 'Materials Science',
         'electronics': 'Electronics', 'avionics': 'Avionics & Probes', 'comms': 'Communications', 'science': 'Science Instruments',
         'solar': 'Solar Power', 'rtg': 'RTGs', 'fission': 'Fission Power'}
FAM = {'rocketry': 0, 'staged': 0, 'hydrolox': 0, 'solids': 0, 'elec': 0, 'nuclearProp': 0, 'flight': 1, 'spaceplanes': 1,
       'capsules': 2, 'control': 2, 'docking': 2, 'edl': 2, 'landing': 2, 'rovers': 2, 'stations': 2, 'lifesupport': 2,
       'materials': 3, 'electronics': 3, 'avionics': 3, 'comms': 3, 'science': 3, 'solar': 4, 'rtg': 4, 'fission': 4}
COL = [(232, 120, 52), (38, 166, 154), (66, 133, 244), (156, 101, 222), (214, 172, 38)]   # propulsion, aero, crew, avionics/science, power
FAMNAME = ['Propulsion', 'Aircraft & Spaceplanes', 'Crew & Stations', 'Avionics, Comms & Science', 'Power']
BG, PANEL, INK, MUTED, GRID = (17, 20, 27), (28, 32, 42), (236, 239, 244), (150, 158, 172), (40, 45, 57)

pos = {k: tuple(int(v) for v in n.get('pos').split(',')[:2]) for k, n in N.items()}
xs = sorted({p[0] for p in pos.values()}); colix = {x: i for i, x in enumerate(xs)}
laneix = {}
ys = sorted({p[1] for p in pos.values()}, reverse=True)      # KSP y grows upward
yix = {y: i for i, y in enumerate(ys)}
CW, CH, BW, BH = 250, 150, 214, 104            # column/lane pitch and node box size (px)
LEFT, TOP, BOTTOM, RIGHT = 330, 330, 150, 60
W = LEFT + len(xs) * CW + RIGHT; H = TOP + len(ys) * CH + BOTTOM
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
def cx(k): return LEFT + colix[pos[k][0]] * CW + CW // 2
def cy(k): return TOP + yix[pos[k][1]] * CH + CH // 2

# column years (median year of the nodes in that column)
cyear = collections.defaultdict(list)
for k in N: cyear[colix[pos[k][0]]].append(pol['node_year'].get(k, 1945))
colyear = {c: sorted(v)[len(v) // 2] for c, v in cyear.items()}
ERAS = [(1945, 1952, 'Sounding rockets & X-planes'), (1953, 1957, 'Missiles & IRBMs'), (1958, 1962, 'First satellites & Mercury'),
        (1963, 1967, 'Gemini & early probes'), (1968, 1972, 'Apollo'), (1973, 1980, 'Stations & planetary probes'),
        (1981, 1990, 'Shuttle era'), (1991, 2000, 'ISS & robotic exploration'), (2001, 2010, 'Modern era'), (2011, 2060, 'Near future')]
# era bands
for i, (a, b, name) in enumerate(ERAS):
    cs = [c for c, y in colyear.items() if a <= round(y) <= b]
    if not cs: continue
    x0 = LEFT + min(cs) * CW; x1 = LEFT + (max(cs) + 1) * CW
    if i % 2 == 0: d.rectangle([x0, TOP - 70, x1, H - BOTTOM + 10], fill=(22, 26, 34))
    label = f'{a}–{b if b < 2060 else ""}'.rstrip('–') if b < 2060 else f'{a}+'
    d.text(((x0 + x1) // 2, TOP - 58), name, font=f_era, fill=INK, anchor='mt')
    d.text(((x0 + x1) // 2, TOP - 30), label if b < 2060 else f'{a}+', font=f_year, fill=MUTED, anchor='mt')
# lane stripes + labels
lane_of_y = {}
for k in N:
    b = br(k)
    if b != 'start': lane_of_y[yix[pos[k][1]]] = b
for i in range(len(ys)):
    y0 = TOP + i * CH
    if i % 2: d.rectangle([LEFT - 10, y0, W - RIGHT, y0 + CH], fill=(20, 24, 31))
    b = lane_of_y.get(i)
    if b:
        c = COL[FAM[b]]
        d.rectangle([24, y0 + CH // 2 - 22, 30, y0 + CH // 2 + 22], fill=c)
        d.text((44, y0 + CH // 2), LABEL.get(b, b), font=f_lane, fill=INK, anchor='lm')

# edges (KSP style elbows), drawn under the nodes
for k, n in N.items():
    for p in n.nodes('Parent'):
        a = p.get('parentID')
        if a not in N: continue
        x1, y1 = cx(a) + BW // 2, cy(a); x2, y2 = cx(k) - BW // 2, cy(k)
        same = br(a) == br(k)
        col = tuple(int(v * 0.75) for v in COL[FAM.get(br(k), 2)]) if same else (88, 96, 112)
        w = 4 if same else 2
        mx = x2 - 18 if not same else (x1 + x2) // 2
        d.line([(x1, y1), (mx, y1), (mx, y2), (x2, y2)], fill=col, width=w, joint='curve')

# nodes
icon_cache = {}
def icon(name):
    if name not in icon_cache:
        p = os.path.join(ICONS, os.path.basename(name) + '.truecolor')
        icon_cache[name] = Image.open(p).convert('RGBA').resize((48, 48), Image.LANCZOS) if os.path.exists(p) else None
    return icon_cache[name]
for k, n in N.items():
    b = br(k); c = COL[FAM.get(b, 2)] if b != 'start' else (220, 220, 220)
    x, y = cx(k), cy(k)
    box = [x - BW // 2, y - BH // 2, x + BW // 2, y + BH // 2]
    d.rounded_rectangle(box, radius=12, fill=PANEL, outline=c, width=3)
    d.rounded_rectangle([box[0], box[1], box[0] + 8, box[3]], radius=4, fill=c)
    ic = icon(n.get('icon') or '')
    if ic: img.paste(ic, (box[0] + 16, box[1] + 10), ic)
    title = n.get('title') or k
    title = re.sub(r'\s*\((\d{4})\)$', r' \1', title)
    # wrap by pixel width: first two lines sit beside the icon, the third spans the box
    words = title.split(); lines = []; cur = ''
    def maxw(i): return BW - (70 if (i < 2 and ic) else 16) - 10
    for wd in words:
        trial = (cur + ' ' + wd).strip()
        if d.textlength(trial, font=f_node) <= maxw(len(lines)): cur = trial
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    if len(lines) > 3: lines = lines[:2] + [' '.join(lines[2:])]
    while d.textlength(lines[-1], font=f_node) > maxw(len(lines) - 1) and len(lines[-1]) > 3: lines[-1] = lines[-1][:-2] + '…'
    ty = box[1] + 12
    for i, ln in enumerate(lines):
        indent = 70 if i < 2 and ic else 16
        d.text((box[0] + indent, ty), ln, font=f_node, fill=INK); ty += 21
    cost = n.get('cost')
    if k != 'start':
        d.text((box[2] - 12, box[3] - 10), f'{int(cost):,} sci', font=f_cost, fill=MUTED, anchor='rb')
    yr = pol['node_year'].get(k)
    if yr and k != 'start': d.text((box[0] + 16, box[3] - 10), str(round(yr)), font=f_cost, fill=c, anchor='lb')

# title + legend + footer
d.text((LEFT, 46), 'RP-Stock Tech Tree', font=f_title, fill=INK)
tot = sum(int(n.get('cost')) for n in N.values())
d.text((LEFT, 122), f'{len(N)} nodes · {tot:,} science · parts placed by the year their real-world counterpart flew', font=f_sub, fill=MUTED)
lx = LEFT + 1500
for i, name in enumerate(FAMNAME):
    d.rounded_rectangle([lx, 62, lx + 34, 96], radius=6, fill=COL[i]); d.text((lx + 46, 79), name, font=f_sub, fill=INK, anchor='lm')
    lx += 60 + int(d.textlength(name, font=f_sub)) + 40
d.text((LEFT, H - 60), 'RP-Stock by shoe7ess · AI-generated mod · tree layout & icons from RP-0/RP-1 (KSP-RO team), CC BY-NC-SA 4.0 · lines run left to right: a node needs the node(s) it is connected from',
       font=f_foot, fill=MUTED)
img.save(OUT, optimize=True)
print(W, H, os.path.getsize(OUT) // 1024, 'KB')
