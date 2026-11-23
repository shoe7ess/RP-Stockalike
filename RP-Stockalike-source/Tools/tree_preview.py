import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import kspcfg as K, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
t = K.parse(open(sys.argv[1]).read()); root = [n for n in t.nodes() if n.name.startswith('@TechTree')][0]
N = {n.get('id'): n for n in root.nodes('RDNode')}
P = {k: tuple(float(v) for v in n.get('pos').split(',')[:2]) for k, n in N.items()}
fig, ax = plt.subplots(figsize=(40, 14))
for k, n in N.items():
    for p in n.nodes('Parent'):
        a = P[p.get('parentID')]; b = P[k]; mx = (a[0] + b[0]) / 2
        ax.plot([a[0], mx, mx, b[0]], [a[1], a[1], b[1], b[1]], lw=0.7, color='#888' if a[1] != b[1] else '#2a6', zorder=1)
for k, (x, y) in P.items():
    ax.add_patch(plt.Rectangle((x - 22, y - 22), 44, 44, color='#357', zorder=2))
    ax.text(x, y - 32, k[:18], fontsize=5, ha='center', va='top', zorder=3)
ax.set_aspect('equal'); ax.autoscale(); ax.axis('off'); plt.tight_layout(); plt.savefig(sys.argv[2], dpi=70)
