"""Read LDraw's actual surface primitives. Units exposed by this module: mm.

This is a geometry reader, not a LEGO connection solver. Type 2/5 edge lines and
textures are omitted from surfaces. Type 1 transforms and type 3/4 faces retained.
"""
from pathlib import Path
from functools import lru_cache
import numpy as np

ROOT = Path(__file__).resolve().parent
LIB = ROOT/'library'/'subset'

def find(name):
    name=name.lower().replace('\\','/')
    for parent in [LIB/'parts',LIB/'p',LIB]:
        p=parent/name
        if p.is_file(): return p
    raise FileNotFoundError(name)

@lru_cache(None)
def geometry(name):
    """Return triangle array (F,3,3) and LDraw face colors, still in LDU."""
    tris=[];colors=[]
    for line in find(name).read_text(encoding='utf-8-sig',errors='replace').splitlines():
        t=line.split()
        if not t or t[0] not in ['1','3','4']:continue
        kind,col=int(t[0]),int(t[1])
        if kind==1:
            v=np.array(list(map(float,t[2:14])))
            child,c=geometry(' '.join(t[14:]))
            if not len(child):continue
            transformed=child@v[3:].reshape(3,3).T+v[:3]
            tris.extend(transformed);colors.extend(np.where(c==16,col,c))
        else:
            v=np.array(list(map(float,t[2:]))).reshape(-1,3)
            tris.append(v[[0,1,2]]);colors.append(col)
            if kind==4:tris.append(v[[0,2,3]]);colors.append(col)
    return np.array(tris,dtype=float).reshape(-1,3,3),np.array(colors,dtype=int)

@lru_cache(None)
def holes(name):
    """Primitive-derived hole-axis lines (location, unit direction, primitive).

    Lines are de-duplicated. An axis record does not imply axle/pin legality;
    crossholes and round holes still need different connection rules.
    """
    all_holes=[]
    for line in find(name).read_text(encoding='utf-8-sig',errors='replace').splitlines():
        t=line.split()
        if not t or t[0]!='1':continue
        v=np.array(list(map(float,t[2:14])));rot=v[3:].reshape(3,3);pos=v[:3]
        child=' '.join(t[14:]).lower().replace('\\','/')
        if child in ['connhole.dat','connhol2.dat','beamhole.dat','peghole.dat','axlehole.dat','axlehol4.dat','bush0.dat']:
            # bush0 is a complete cross-bore primitive on native Z. Unlike
            # axlehol4 it does not recurse to a separately named hole surface.
            axis=rot@np.array([0.,0.,1.] if child=='bush0.dat' else [0.,1.,0.]);axis/=np.linalg.norm(axis)
            all_holes.append((pos,axis,child))
        else:
            for p,a,k in holes(child):all_holes.append((rot@p+pos,rot@a,k))
    unique={}
    for p,a,k in all_holes:
        a=a/np.linalg.norm(a)
        for val in a:
            if abs(val)>1e-6:
                if val<0:a=-a
                break
        foot=p-a*np.dot(p,a)
        key=tuple(np.round(np.r_[foot,a],4))
        unique[key]=(p,a,k)
    return list(unique.values())

def world_holes(part):
    r=np.array(part['rotation']);t=np.array(part['position'])
    return [(r@(p*.4)+t,r@a,k) for p,a,k in holes(part['file'])]

def axis_present(part,point,axis,tolerance=.03):
    pt=np.array(point);a=np.array(axis,dtype=float);a/=np.linalg.norm(a)
    return any(np.linalg.norm(np.cross(a,b))<1e-5 and
               np.linalg.norm(np.cross(pt-p,a))<tolerance
               for p,b,_ in world_holes(part))

def mesh(part):
    v,c=geometry(part['file'])
    return (v*.4)@np.array(part['rotation']).T+np.array(part['position']), np.where(c==16,part['color'],c)

def metadata(name):
    lines=find(name).read_text(encoding='utf-8-sig',errors='replace').splitlines()
    return {'description':lines[0][2:],
            'author':next((s[9:] for s in lines if s.startswith('0 Author:')),''),
            'license':next((s[11:] for s in lines if s.startswith('0 !LICENSE')),'')}

def part(name,file,color,position,rotation,group,**extra):
    return dict(id=name,file=file+'.dat',color=color,position=list(map(float,position)),
                rotation=np.asarray(rotation,dtype=float).tolist(),group=group,**extra)

def export_ldr(parts,path,title):
    # Global X forward, Y left, Z up -> conventional LDraw Y down.
    q=np.array([[1,0,0],[0,0,-1],[0,1,0]])
    lines=[f'0 {title}','0 Author: Custom EV3 project','0 !LICENSE CC BY 4.0 for original assembly; source parts retain their licenses.',
           '0 // PROTOTYPE. Unmounted interfaces and remaining checks are documented in Phase-2-Review.md.']
    group=None
    for p in parts:
        if p['group']!=group:
            if group:lines.append('0 STEP')
            lines.append('0 // '+p['group']);group=p['group']
        values=np.r_[q@p['position']*2.5,(q@np.array(p['rotation'])).reshape(-1)]
        lines.append('0 // '+p['id'])
        lines.append('1 '+str(p['color'])+' '+' '.join(f'{v:.7g}' for v in values)+' '+p['file'])
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
