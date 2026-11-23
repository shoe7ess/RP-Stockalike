import json, statistics as st, collections
d=json.load(open('part_costs.json')); rows=json.load(open('cost_rows.json'))
modof={r[2]:r[0] for r in rows}; br={r[2]:r[1] for r in rows}
DEN={'LiquidFuel':.005,'Oxidizer':.005,'MonoPropellant':.004,'SolidFuel':.0075,'XenonGas':.0001,'Ablator':.001,'LqdHydrogen':.00007085,'LqdMethane':.00042,'Ore':.01,'ElectricCharge':0}
UC={'LiquidFuel':.8,'Oxidizer':.18,'MonoPropellant':1.2,'SolidFuel':.6,'XenonGas':4,'Ore':.02,'Ablator':.5,'LqdHydrogen':.03,'LqdMethane':.2}
agg=collections.defaultdict(lambda:[0,0,0])
for n,p in d.items():
    if p['cat'] not in ('FuelTank','Engine','Propulsion'): continue
    try: c=float(p['cost']); m=float(p['mass'])
    except: continue
    wet=m+sum(float(v)*DEN.get(k,0) for k,v in p['res'].items())
    m0=modof.get(n,'?'); a=agg[m0]; a[0]+=c; a[1]+=wet; a[2]+=1
for k,(c,w,n) in sorted(agg.items(), key=lambda x:-x[1][2])[:20]:
    if w: print(f'{k:28s} n={n:4d} cost/wet-ton={c/w:8.0f}')
