# Fold Spacelines-Progression into RP-Stock as its own toggleable top-level group.
import os, re, sys, shutil
SRC, OUT, OURS = sys.argv[1], sys.argv[2], sys.argv[3]
ours = {l.strip() for l in open(OURS) if l.strip() and not l.startswith('GROUP:')}
our_groups = {l.strip()[6:] for l in open(OURS) if l.startswith('GROUP:')}
AGENT = {'fai': 'Federation Aeronautique Internationale', 'nasa': 'NASA', 'Exploration': 'JPL', 'Satellites': 'DOD', 'Stations': 'NASA'}
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)

def blocks(L):
    i = 0
    while i < len(L):
        if re.match(r'^CONTRACT_TYPE\b', L[i]):
            d = 0; j = i
            while j < len(L):
                d += L[j].count('{') - L[j].count('}')
                if d == 0 and '{' in ''.join(L[i:j+1]): break
                j += 1
            yield i, j; i = j + 1
        else: i += 1

# subgroups declared by Spacelines
top = open(os.path.join(SRC, 'SpacelinesContracts.cfg'), encoding='utf-8-sig').read()
sub = re.findall(r'^\tCONTRACT_GROUP\s*\n\s*\{\s*\n\s*name\s*=\s*(\S+)', top, re.M)
ren = {g: 'SL_' + g for g in sub}
stats = dict(dropped=0, kept=0, files=0)
dropped = []
for root, _, fs in os.walk(os.path.join(SRC, 'Contracts')):
    for f in fs:
        if not f.endswith('.cfg'): continue
        p = os.path.join(root, f); L = open(p, encoding='utf-8-sig', errors='surrogateescape').read().split('\n')
        out = []; last = 0
        for s, e in blocks(L):
            out += L[last:s]; blk = L[s:e+1]; last = e + 1
            name = next((re.search(r'=\s*(\S+)', x).group(1) for x in blk if re.match(r'^\s*name\s*=', x)), None)
            if name in ours:
                stats['dropped'] += 1; dropped.append(name)
                out.append(f'// {name}: dropped - RP-Stock already has this mission (RP-0 takes priority)')
                continue
            hdr = blk[0]
            hdr = re.sub(r'NEEDS\[([^\]]*)\]', r'NEEDS[\1,!RP-0,!RP-1]', hdr) if 'NEEDS[' in hdr else hdr.rstrip() + ':NEEDS[!RP-0,!RP-1]'
            blk[0] = hdr
            for i, x in enumerate(blk):
                m = re.match(r'^(\s*group\s*=\s*)(\S+)\s*$', x)
                if m and m.group(2) in ren: blk[i] = m.group(1) + ren[m.group(2)]
                m = re.match(r'^(\s*agent\s*=\s*)(.+?)\s*$', x)
                if m and m.group(2) in AGENT: blk[i] = m.group(1) + AGENT[m.group(2)]
            out += blk; stats['kept'] += 1
        out += L[last:]
        rel = os.path.relpath(p, SRC); q = os.path.join(OUT, rel); os.makedirs(os.path.dirname(q), exist_ok=True)
        open(q, 'w', encoding='utf-8', errors='surrogateescape').write('// Spacelines Progression by Gupyzer0 (CC BY-NC-SA 4.0), folded into RP-Stock.\n' + '\n'.join(out))
        stats['files'] += 1
# group file
t = top.replace('CONTRACT_GROUP\n{\n\tname = SpacelinesContracts', 'CONTRACT_GROUP:NEEDS[!RP-0,!RP-1]\n{\n\tname = SpacelinesContracts', 1)
t = t.replace('displayName = Spacelines Contracts', 'displayName = RP-Stock: Spacelines Progression', 1)
for g, n in ren.items():
    t = re.sub(r'(\tCONTRACT_GROUP\s*\n\s*\{\s*\n\s*name\s*=\s*)%s\b' % re.escape(g), r'\g<1>' + n, t)
for a, b in AGENT.items():
    t = re.sub(r'(agent\s*=\s*)%s\s*$' % re.escape(a), r'\g<1>' + b, t, flags=re.M)
open(os.path.join(OUT, 'SpacelinesContracts.cfg'), 'w', encoding='utf-8').write(t)
shutil.copytree(os.path.join(SRC, 'Compatibility'), os.path.join(OUT, 'Compatibility'))
open(os.path.join(OUT, 'README.md'), 'w').write(open(os.path.join(SRC, 'README.md'), encoding='utf-8').read() +
 '\n\n---\nFolded into RP-Stock: missions RP-Stock already has were dropped (RP-0 priority), sub-groups prefixed SL_, '
 'agents mapped to RP-Stock agencies. Stock-contract disabling is done through Contract Configurator settings instead of stockContracts.cfg.\n')
print(stats, 'subgroups renamed', len(ren))
open(os.path.join(OUT, '..', 'spacelines_dropped.txt'), 'w').write('\n'.join(sorted(dropped)))
