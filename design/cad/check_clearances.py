"""Targeted checks on actual meshes and conservative link envelopes.

Not a general-purpose LEGO collision solver. Fastener interference fits, motor
internals and full chassis integration remain outside this check's scope.
"""
import json,math
from pathlib import Path
from itertools import combinations
import numpy as np
from build_lift import build,bounds,LOW,HIGH
from ldraw_geometry import mesh

ROOT=Path(__file__).resolve().parent

def section(tris,y):
    segs=[]
    for tri in tris:
        hits=[]
        for a,b in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:
            if (a[1]>y)!=(b[1]>y):
                t=(y-a[1])/(b[1]-a[1]);p=a+t*(b-a);hits.append(p[[0,2]])
        if len(hits)==2 and np.linalg.norm(hits[0]-hits[1])>1e-7:
            aa,bb=sorted([tuple(np.round(hits[0],6)),tuple(np.round(hits[1],6))])
            segs.append((aa,bb))
    return np.array(sorted(set(segs)))

def inside(points,segs):
    a,b=segs[:,0],segs[:,1]
    out=[]
    for start in range(0,len(points),256):
        pp=points[start:start+256]
        zz=pp[:,1,None];xx=pp[:,0,None]
        crossing=(a[:,1]>zz)!=(b[:,1]>zz)
        denom=b[:,1]-a[:,1]
        xhit=a[:,0]+(zz-a[:,1])*(b[:,0]-a[:,0])/np.where(abs(denom)>1e-10,denom,1e-10)
        out.extend((np.sum(crossing & (xhit>xx),axis=1)%2)==1)
    return np.array(out)

def tooth_overlap(p,q,y,spacing=.04):
    a,_=mesh(p);b,_=mesh(q)
    sa,sb=section(a,y),section(b,y)
    lo=np.maximum(sa.reshape(-1,2).min(0),sb.reshape(-1,2).min(0))
    hi=np.minimum(sa.reshape(-1,2).max(0),sb.reshape(-1,2).max(0))
    xs=np.arange(lo[0]+spacing/2,hi[0],spacing)
    zs=np.arange(lo[1]+spacing/2,hi[1],spacing)
    pts=np.stack(np.meshgrid(xs,zs),axis=-1).reshape(-1,2)
    if not len(pts):return 0,0
    both=inside(pts,sa)&inside(pts,sb)
    return int(both.sum()),float(both.sum()*spacing*spacing)

def pt_seg(p,a,b):
    ab=b-a;t=np.clip(np.dot(p-a,ab)/np.dot(ab,ab),0,1)
    return np.linalg.norm(p-a-t*ab)

def segment_distance(a,b,c,d):
    # Here the bracket and link segments do not cross, checked separately.
    def orient(p,q,r):
        a,b=q-p,r-p
        return a[0]*b[1]-a[1]*b[0]
    if orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0:return 0.
    return min(pt_seg(a,c,d),pt_seg(b,c,d),pt_seg(c,a,b),pt_seg(d,a,b))

def run():
    checks=[];unresolved=[];minimum=1e9
    mating={frozenset(['GEAR-8-A','GEAR-24-A']),frozenset(['GEAR-8-B','GEAR-24-B'])}
    selected={'64179','32524','60483','40490','32526','3647','3648','99535c01'}
    nposes=71;tests=0
    for theta in np.linspace(LOW,HIGH,nposes):
        pp=[p for p in build(float(theta)) if p['file'].split('.')[0] in selected]
        bb={p['id']:bounds(p) for p in pp}
        for p,q in combinations(pp,2):
            tests+=1
            ap,bp=bb[p['id']];aq,bq=bb[q['id']]
            overlap=np.minimum(bp,bq)-np.maximum(ap,aq)
            if not np.all(overlap>.05):continue
            names={p['id'],q['id']}
            if frozenset(names) in mating:continue
            if any(n.startswith('LOWER-LINK') for n in names) and any(n.startswith('FORK-BRACKET') for n in names):
                a=np.array([0.,48.]);b=np.array([48*math.cos(theta),48+48*math.sin(theta)])
                corner=b-np.array([0,32]);long_end=corner+np.array([32,0]);short_end=corner+np.array([0,16])
                # 4.1 mm radius exceeds the 3.6 mm measured profile half-width.
                clearance=min(segment_distance(a,b,corner,long_end),segment_distance(a,b,corner,short_end))-8.2
                minimum=min(minimum,clearance)
                if clearance<1:unresolved.append([float(theta),sorted(names),float(clearance)])
            else:unresolved.append([float(theta),sorted(names),overlap.tolist()])
    checks.append({'check':'Selected structural parts across 71 poses','status':'PASS' if not unresolved else 'REVIEW',
                   'evidence':f'{tests} pair/pose bounding-box checks; {len(unresolved)} unresolved pairs. Gear meshes and fasteners excluded. Lower-link/bracket broad overlaps resolved with conservative 4.1 mm profile-radius envelopes; minimum clearance {minimum:.3f} mm.'})
    gear_results=[]
    for theta in np.linspace(LOW,HIGH,15):
        pp={p['id']:p for p in build(float(theta))}
        for aa,bb,yy in [('GEAR-8-A','GEAR-24-A',-4),('GEAR-8-B','GEAR-24-B',4)]:
            count,area=tooth_overlap(pp[aa],pp[bb],yy)
            gear_results.append(dict(angle_degrees=math.degrees(theta),pair=[aa,bb],overlap_samples=count,estimated_overlap_area_mm2=area))
    worst=max(gear_results,key=lambda r:r['estimated_overlap_area_mm2'])
    checks.append({'check':'Gear tooth center-plane section test','status':'PASS' if worst['overlap_samples']==0 else 'REVIEW',
                   'evidence':f'30 center-plane tests at 0.04 mm grid spacing. Maximum estimated overlap area {worst["estimated_overlap_area_mm2"]:.4f} mm^2. This does not test all axial sections or certify real tooth contact.'})
    report=dict(checks=checks,unresolved_structural_pairs=unresolved,gear_section_results=gear_results,
                excluded='Full robot; all pin/axle/hub interferences; friction fits; motor interior; switch/stops; camera; full 3D gear collision/contact.')
    (ROOT/'clearance-results.json').write_text(json.dumps(report,indent=2)+'\n')
    for c in checks:print(c['status'],c['check'],c['evidence'])

if __name__=='__main__':run()
