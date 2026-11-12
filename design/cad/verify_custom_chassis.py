"""Connection-center and explicit-inventory audit of custom chassis I0.3."""
import json,csv,math,sys
from collections import Counter
import numpy as np
from build_integrated import assembly,OUT,body_point,BODY_PITCH,INTEGRATED_LOW,fork_bounds,PITCH_R,AXLE_ORIGIN
from custom_chassis import build_chassis
from ldraw_geometry import mesh,axis_present

def run():
    parts,meta=assembly(0);pp={p['id']:p for p in parts};_,joints=build_chassis()
    results=[]
    for j in joints:
        point=body_point(j['point'])
        ok=axis_present(pp[j['a']],point,j['axis']) and axis_present(pp[j['b']],point,j['axis'])
        results.append(dict(check=j['id'],status='PASS' if ok else 'FAIL',parts=[j['a'],j['b']],point_mm=point.tolist(),connection=j['kind']))
    for side,s in [('L',1),('R',-1)]:
        pairs=[]
        for x in [48,80]:
            pairs.append((f'bridge-frame-{side}-{x}','ADAPTER-RAIL-'+side,'FRAME-'+side,[x,0,84]))
            pairs.append((f'bridge-upper-{side}-{x}',f'BRIDGE-POST-{side}-{x}','BRIDGE-SIDE-'+side,[x,0,116]))
        pairs.append(('bridge-lock-'+side,'ADAPTER-RAIL-'+side,f'BRIDGE-POST-{side}-48',[48,0,100]))
        for x in [0,8]:pairs.append((f'bridge-body-{side}-{x}','BRIDGE-SIDE-'+side,'BRICK-RAIL-'+side,[x,0,116]))
        for name,a,b,point in pairs:
            world=body_point(point)
            ok=axis_present(pp[a],world,[0,1,0]) and axis_present(pp[b],world,[0,1,0])
            results.append(dict(check=name,status='PASS' if ok else 'FAIL',parts=[a,b],point_mm=world.tolist()))
    for name in ['TIRE-L','TIRE-R','CASTER-BALL']:
        bottom=float(mesh(pp[name])[0][:,:,2].min())
        results.append(dict(check=name+' floor contact',status='PASS' if abs(bottom)<.05 else 'FAIL',bottom_mm=bottom))
    results.append(dict(check='Fork entry height after stance pitch',status='PASS' if abs(fork_bounds(INTEGRATED_LOW)[2]-11.6)<.01 else 'FAIL',bounds=fork_bounds(INTEGRATED_LOW)))
    results.append(dict(check='No opaque chassis proxy',status='PASS' if not any(p.get('reference') for p in parts) else 'FAIL'))
    def local_vertices(name):
        return (mesh(pp[name])[0].reshape(-1,3)-AXLE_ORIGIN)@PITCH_R+AXLE_ORIGIN
    for side,s in [('L',1),('R',-1)]:
        rail=local_vertices('CHASSIS-LOWER-'+side);motor=local_vertices('DRIVE-MOTOR-'+side)
        gap=float((rail[:,1]*s).min()-(motor[:,1]*s).max())
        results.append(dict(check='Main rail / motor side clearance '+side,status='PASS' if gap>=3.9 else 'FAIL',gap_mm=gap))
    bridge=local_vertices('BRIDGE-SIDE-R');motor=local_vertices('LIFT-MOTOR-BODY')
    gap=float(bridge[:,2].min()-motor[:,2].max())
    results.append(dict(check='Side bridge / raised motor height clearance',status='PASS' if gap>8 else 'FAIL',gap_mm=gap))
    # Check exact long-pin stack spans from actual meshes, in unpitched frame.
    unrot=np.array([[math.cos(BODY_PITCH),0,-math.sin(BODY_PITCH)],[0,1,0],[math.sin(BODY_PITCH),0,math.cos(BODY_PITCH)]])
    for p in parts:
        if p['id'].startswith('TOP-TOWER-PIN-'):
            vertices=mesh(p)[0].reshape(-1,3)
            yy=vertices[:,1];bounds=sorted(abs(x) for x in [yy.min(),yy.max()])
            results.append(dict(check=p['id']+' 24mm stack span',status='PASS' if np.allclose(bounds,[52,76],atol=.01) else 'FAIL',span_mm=bounds))
    counts=Counter((p['file'],p['color']) for p in parts if not p.get('fixture') and not p.get('placeholder'))
    counts.pop(('99535c01.dat',15),None);counts.pop(('99543.dat',4),None);counts[('99455.dat',15)]+=1
    # Core-stock counts by design/color. Additional colors accept no silent substitution.
    stock={('32278.dat',15):6,('32017.dat',0):0,('32526.dat',15):4,('32526.dat',71):2,
      ('95658.dat',15):2,('95646.dat',15):1,('95650.dat',15):1,('95648.dat',15):2,
      ('92911.dat',72):1,('99948.dat',71):1,('56908.dat',71):2,('41897.dat',0):2,
      ('59443.dat',4):6,('32073.dat',71):6}
    stock[('32524.dat',71)]=4
    stock[('32526.dat',1)]=0
    stock[('32524.dat',1)]=0
    from package_model import STOCK
    for file,(element,n,name) in STOCK.items():
        # Original lift stock uses specific colors selected in build_lift.
        matching=[key for key in counts if key[0]==file]
        if len(matching)==1 and matching[0] not in stock:stock[matching[0]]=n
    # Remaining known kit entries / exact aliases.
    stock[('3737.dat',0)]=2;stock[('3649.dat',71)]=2
    with (OUT/'catalog-parts.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['Design file','LDraw color','Placed physical quantity','Core stock used for comparison','Minimum extra','Scope'])
        for key,n in sorted(counts.items()):
            available=stock.get(key)
            w.writerow([key[0],key[1],n,'' if available is None else available,'' if available is None else max(0,n-available),'All placed LEGO parts; future brackets and actual camera not yet included'])
    out=dict(revision='I0.3',status='HOLD - lift/chassis bridge and sensing/stop brackets still open',checks=results,
      stance_pitch_degrees=math.degrees(BODY_PITCH),low_linkage_degrees=math.degrees(INTEGRATED_LOW),
      explicit_physical_lego_pieces=sum(counts.values()),catalog_color_types=len(counts),
      notes=['Axes are necessary checks, not complete fit/insertion proof.','Pin engagement and friction-stack stiffness require physical testing.',
      'Old 0.85kg chassis balance estimate is invalidated by the new chassis. Recalculate with measured weights/CG.',
      'Brick represented by stock LDraw configuration; battery variant/cable access not verified.'])
    (OUT/'custom-chassis-checks.json').write_text(json.dumps(out,indent=2))
    print('Chassis checks:',Counter(r['status'] for r in results),'pieces',sum(counts.values()))
    for r in results:
        if r['status']!='PASS':print(r)
    if any(r['status']!='PASS' for r in results):sys.exit(2)

if __name__=='__main__':run()
