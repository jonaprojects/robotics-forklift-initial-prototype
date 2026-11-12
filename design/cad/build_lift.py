"""Build a real-part digital lift module. See generated review for its scope."""
import json,math,csv
from collections import Counter
from pathlib import Path
import numpy as np
from ldraw_geometry import part,mesh,export_ldr,metadata,axis_present,world_holes

ROOT=Path(__file__).resolve().parent
I=np.eye(3)
RFRAME=np.array([[0,0,1],[0,1,0],[-1,0,0]])
# Parts whose native shaft is Z, into world Y. Native Y becomes -Z.
RSHAFT=np.array([[1,0,0],[0,0,1],[0,-1,0]])
RAXLE=np.array([[0,0,-1],[1,0,0],[0,-1,0]])
RBEAM=np.array([[0,0,1],[0,1,0],[-1,0,0]])

def ry(a):
    c,s=math.cos(a),math.sin(a)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def rz(a):
    c,s=math.cos(a),math.sin(a)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def beam_rotation(theta):
    c,s=math.cos(theta),math.sin(theta)
    return np.array([[s,0,c],[0,1,0],[-c,0,s]])

LOW=-math.asin(1/6)
HIGH=math.radians(25)

def build(theta=LOW):
    parts=[]
    def add(*args,**kw):
        p=part(*args,**kw);parts.append(p);return p
    for side,sgn in [('L',1),('R',-1)]:
        add(f'FRAME-{side}','64179',71,[-24,16*sgn,64],RFRAME,'01 Fixed frames')
    # Lower pivot is 48 mm above the floor. Actual frame top = 80 mm.
    phase_out=-theta
    phase_mid=math.pi/8+3*theta
    phase_in=-math.pi/4-9*theta
    add('INPUT-AXLE','60485',71,[-32,-8,48],ry(phase_in)@RAXLE,'02 Gearbox')
    add('INTERMEDIATE-AXLE','44294',71,[-16,0,48],ry(phase_mid)@RAXLE,'02 Gearbox')
    add('OUTPUT-AXLE','3708',0,[0,0,48],ry(phase_out)@RAXLE,'02 Gearbox')
    for name,file,x,y,phase in [('GEAR-8-A','3647',-32,-4,phase_in),('GEAR-24-A','3648',-16,-4,phase_mid),
                               ('GEAR-8-B','3647',-16,4,phase_mid),('GEAR-24-B','3648',0,4,phase_out)]:
        add(name,file,72,[x,y,48],RSHAFT@rz(phase),'02 Gearbox')
    # Retaining collars. Additional stage spacers are NOT silently invented.
    for name,x,ys in [('INPUT',-32,[-24,24]),('INTERMEDIATE',-16,[-24,24]),('OUTPUT',0,[-40,40])]:
        phase={'INPUT':phase_in,'INTERMEDIATE':phase_mid,'OUTPUT':phase_out}[name]
        for j,y in enumerate(ys):add(f'{name}-COLLAR-{j}','3713',71,[x,y,48],ry(phase)@RSHAFT,'02 Gearbox')
    for name,xx,phase in [('INPUT',-32,phase_in),('INTERMEDIATE',-16,phase_mid),('OUTPUT',0,phase_out)]:
        for yy in [-10,10]:
            add(f'{name}-INNER-HALF-{yy}','4265c',14,[xx,yy,48],ry(phase)@RSHAFT,'02 Gearbox')
    add('INPUT-INNER-BUSH','3713',71,[-32,4,48],ry(phase_in)@RSHAFT,'02 Gearbox')
    add('OUTPUT-INNER-BUSH','3713',71,[0,-4,48],ry(phase_out)@RSHAFT,'02 Gearbox')
    add('UPPER-PIVOT-AXLE','3707',0,[0,0,80],RAXLE,'03 Moving links')
    for side,sgn in [('L',1),('R',-1)]:
        y=24*sgn
        for name,z in [('LOWER',48),('UPPER',80)]:
            add(f'{name}-LINK-{side}','32524',71,[24*math.cos(theta),y,z+24*math.sin(theta)],
                beam_rotation(theta),'03 Moving links',motion='link',pivot_z=z)
        add(f'DRIVE-COUPLER-{side}','60483',0,[0,32*sgn,48],beam_rotation(theta),'03 Moving links',motion='coupler')
        # 2L pin centered between the adjacent link and coupler layers.
        add(f'COUPLER-PIN-{side}','2780',0,[8*math.cos(theta),28*sgn,48+8*math.sin(theta)],
            RAXLE,'03 Moving links',motion='coupler-pin')
        add(f'UPPER-COLLAR-{side}','4265c',14,[0,30*sgn,80],RSHAFT,'03 Moving links')
    x,z=48*math.cos(theta),48+48*math.sin(theta)
    for side,sgn in [('L',1),('R',-1)]:
        # Carriage H1 is 32 mm below lower moving pivot, H5 at lower,
        # H9 at upper. A 5L carriage from P1 is too short for this stack.
        add(f'CARRIAGE-{side}','40490',71,[x,16*sgn,z],I,'04 Fork carriage',motion='carriage')
        for name,height in [('LOWER',0),('UPPER',32)]:
            add(f'CARRIAGE-PIVOT-{name}-{side}','3673',7,[x,20*sgn,z+height],RAXLE,
                '04 Fork carriage',motion='carriage')
        # 32526 native long leg: (0,0,0) to (0,0,32); short branch:
        # (0,0,32) to (16,0,32). Map long leg to +X and short to +Z.
        # Corner native (0,0,32) maps to carriage bottom; long leg goes FORWARD
        # by taking native -Z; short native +X maps +Z.
        rb=np.array([[0,0,-1],[0,1,0],[1,0,0]])
        add(f'FORK-BRACKET-{side}','32526',15,[x+32,24*sgn,z-32],rb,
            '04 Fork carriage',motion='carriage')
        add(f'FORK-{side}','40490',71,[x+48,16*sgn,z-32],RBEAM,
            '04 Fork carriage',motion='carriage')
        for j,(dx,dz) in enumerate([(0,0),(0,16),(16,0),(32,0)]):
            add(f'BRACKET-PIN-{side}-{j}','2780',0,[x+dx,20*sgn,z-32+dz],RAXLE,
                '04 Fork carriage',motion='carriage')
    # Three cross-tie axles triangulate the relative frame positions. Each tie
    # needs a 24 mm internal spacer stack and two outside half bushes.
    # One 16 mm hollow pin-joiner tube + one 8 mm bush provides that stack.
    # An axle joiner with a center stop CANNOT serve as a through-spacer.
    for j,(xx,zz) in enumerate([(-48,48),(-48,80),(-16,80),(x,z-24),(x,z+16)]):
        group='05 Fixed frame cross ties' if j<3 else '05b Moving carriage cross ties'
        add(f'TIE-AXLE-{j}','3707' if j==3 else '3706',0,[xx,0,zz],RAXLE,group)
        add(f'TIE-SPACER-{j}','62462',71,[xx,-4,zz],RAXLE,group)
        add(f'TIE-BUSH-{j}','3713',71,[xx,8,zz],RSHAFT,group)
        for sgn in [-1,1]:
            add(f'TIE-RETAINER-{j}-{sgn}','4265c',14,[xx,(30 if j==3 else 22)*sgn,zz],RSHAFT,group)
    # Motor bracket: 9L vertical spine; two front pins on motor face; top
    # 3L pin through spine, 2L spacer's round hole and fixed frame. The input
    # shaft provides the second separated axis constraining bracket rotation.
    add('MOTOR-BRACKET-SPINE','40490',71,[-32,-32,48],I,'06 Motor bracket')
    add('MOTOR-BRACKET-SPACER','60483',0,[-32,-24,72],I,'06 Motor bracket')
    # 6558 native axial range is -12..12 mm, center shoulder at -4 mm.
    # Native negative end points toward the spine's outer face (-36 mm).
    add('MOTOR-BRACKET-TOP-PIN','6558',1,[-32,-24,80],RAXLE,'06 Motor bracket')
    for zz in [40,56]:
        add(f'MOTOR-FACE-PIN-{zz}','2780',0,[-32,-36,zz],RAXLE,'06 Motor bracket')
    rm=np.array([[1,0,0],[0,0,-1],[0,1,0]])
    add('LIFT-MOTOR-BODY','99535c01',15,[-32,-36,48],rm,'06 Motor bracket',physical_assembly='99455')
    add('LIFT-MOTOR-ROTOR','99543',4,[-32,-36,48],rm@rz(-phase_in),'06 Motor bracket',physical_assembly='99455')
    return parts

def bounds(p):
    v,_=mesh(p);v=v.reshape(-1,3);return v.min(0),v.max(0)

def run():
    low=build();high=build(HIGH)
    export_ldr(low,ROOT/'lift-low.ldr','EV3 low-lift module P2-R1 / lowered / incomplete mounting')
    export_ldr(high,ROOT/'lift-raised.ldr','EV3 low-lift module P2-R1 / raised / incomplete mounting')
    (ROOT/'assembly-low.json').write_text(json.dumps(low,indent=2)+'\n')
    (ROOT/'assembly-raised.json').write_text(json.dumps(high,indent=2)+'\n')
    counts=Counter(p['file'] for p in low)
    with (ROOT/'lift-parts.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['LDraw design file','Quantity','Description'])
        for name,count in sorted(counts.items()):w.writerow([name,count,metadata(name)['description']])
    checks=[]
    def check(name,ok,detail):checks.append(dict(check=name,status='PASS' if ok else 'FAIL',detail=detail))
    check('Rigid part transforms only',all(np.allclose(np.array(p['rotation']).T@np.array(p['rotation']),np.eye(3),atol=1e-9) and
          abs(np.linalg.det(p['rotation'])-1)<1e-9 for p in low+high),
          'Every placed part has unit scale and a proper rotation; no stretched or mirrored replacement parts.')
    left=next(p for p in low if p['id']=='FRAME-L')
    check('Reject invalid P1 middle shaft location',not axis_present(left,[-24,16,48],[0,1,0]),
          'Regression check: P1 required a transverse hole at X=-24. The actual frame does not have that hole, so that layout is rejected.')
    for x in [-32,-16,0]:
        for y in [-16,16]:
            f=next(p for p in low if p['id']==('FRAME-L' if y>0 else 'FRAME-R'))
            check(f'Revised bearing X={x}, Y={y}',axis_present(f,[x,y,48],[0,1,0]),'Hole axis extracted from actual LDraw primitives.')
    # Detect intended alignment from actual part primitives, not ideal beam boxes.
    for theta,label in [(LOW,'low'),(0.,'horizontal'),(HIGH,'raised')]:
        pp={p['id']:p for p in build(theta)}
        x,z=48*math.cos(theta),48+48*math.sin(theta)
        for side,sgn in [('L',1),('R',-1)]:
            for name,h in [('LOWER',0),('UPPER',32)]:
                check(f'{label} moving pivot {name}-{side}',
                      axis_present(pp[f'{name}-LINK-{side}'],[x,24*sgn,z+h],[0,1,0]) and
                      axis_present(pp[f'CARRIAGE-{side}'],[x,16*sgn,z+h],[0,1,0]),
                      'Matching round-hole axes in link and carriage.')
            for j,(dx,dz) in enumerate([(0,0),(0,16),(16,0),(32,0)]):
                p=pp[f'FORK-BRACKET-{side}'];point=[x+dx,24*sgn,z-32+dz]
                mate=pp[f'CARRIAGE-{side}'] if dx==0 else pp[f'FORK-{side}']
                check(f'{label} fork bracket {side} joint {j}',axis_present(p,point,[0,1,0]) and
                      axis_present(mate,point,[0,1,0]),'Both real parts have the required pin axis.')
    # Ground check over the complete angular range, using actual meshes.
    minima={}
    for theta in np.linspace(LOW,HIGH,71):
        for p in build(float(theta)):
            b,_=bounds(p);minima[p['id']]=min(minima.get(p['id'],1e9),float(b[2]))
    worst=min(minima,key=minima.get)
    check('No floor penetration in 71 sampled positions',minima[worst]>=0,
          f'Lowest actual surface: {minima[worst]:.3f} mm, part {worst}. No inter-part collision claim.')
    for side in ['L','R']:
        p=next(p for p in low if p['id']==f'FORK-{side}');a,b=bounds(p)
        check(f'Low fork underside {side}',a[2]>=3.5 and a[2]<=4.5,
              f'Actual mesh bottom {a[2]:.3f} mm; actual width {b[1]-a[1]:.3f} mm.')
    for side,sgn in [('L',1),('R',-1)]:
        for z in [40,56]:
            body=next(p for p in low if p['id']=='LIFT-MOTOR-BODY')
            spine=next(p for p in low if p['id']=='MOTOR-BRACKET-SPINE')
            check(f'Motor face mounting hole Z={z}',axis_present(body,[-32,-36,z],[0,1,0]) and
                  axis_present(spine,[-32,-32,z],[0,1,0]),'Actual motor and spine hole axes coincide; two 2L pins.')
        break
    top_pin=next(p for p in low if p['id']=='MOTOR-BRACKET-TOP-PIN')
    a,b=bounds(top_pin)
    check('Three-layer motor bracket pin spans the stack',abs(a[1]+36)<.01 and abs(b[1]+12)<.01,
          f'Actual pin spans Y={a[1]:g} to {b[1]:g} mm, matching the three 8 mm layers at -32, -24 and -16 mm.')
    for p in low:
        if p['id'].startswith('TIE-SPACER-'):
            check('Actual hollow spacer axis '+p['id'],axis_present(p,p['position'],[0,1,0]),
                  'The tube uses native X as its bore axis; that real primitive axis must align with the transverse shaft.')
    axial_native={name:[1,0,0] for name in ['3706.dat','3707.dat','3708.dat','44294.dat','60485.dat','2780.dat','3673.dat','6558.dat','62462.dat']}
    axial_native.update({name:[0,0,1] for name in ['3647.dat','3648.dat','3713.dat','4265c.dat','99543.dat']})
    axial_ok=all(abs((np.array(p['rotation'])@np.array(axial_native[p['file']]))[1])>1-1e-9
                 for p in low+high if p['file'] in axial_native)
    check('Fastener, tube, shaft and gear axial orientation',axial_ok,
          'Native axes are part-specific: X for pins/axles/tubes, Z for gears/bushes/rotor. All align with world Y.')
    data=dict(revision='P2-R1',status='digital lift module only; whole robot not released',
              parts=len(low),unique_parts=len(counts),low_angle_degrees=math.degrees(LOW),
              high_angle_degrees=25,checks=checks,minimum_surface_z=minima,
              unresolved=['chassis attachment','limit switch and hard stops','color and camera mounts',
                          'full inventory reconciliation','comprehensive inter-part collision check'])
    (ROOT/'verification.json').write_text(json.dumps(data,indent=2)+'\n')
    print(f'{len(low)} real-part instances; {len(counts)} types; {len(checks)} checks')
    for c in checks:
        if c['status']=='FAIL':print('FAIL:',c['check'],c['detail'])
    print('Scope: lift module with motor bracket. Chassis and sensing assemblies are not included.')

if __name__=='__main__':run()
