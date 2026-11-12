"""Integrated catalog-part chassis prototype. Conceptual mounts are flagged.
This is not a part-by-part verified complete robot or an instruction-book release.
"""
import json,struct,math,csv,hashlib,zipfile
from pathlib import Path
from collections import Counter
import numpy as np
from build_lift import build,LOW,HIGH,RBEAM,RAXLE,RSHAFT,ry
from ldraw_geometry import part,mesh,geometry,find,metadata,axis_present,export_ldr
from render_model import blob,rgb
from package_model import dependencies,STOCK
from custom_chassis import build_chassis
from functools import lru_cache

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'integrated'
OUT.mkdir(exist_ok=True)
LIB=ROOT/'library'/'subset'/'parts'
I=np.eye(3)

# The socket hole center is 16 mm above its ball center. Nominally that puts
# the 18 mm ball 3 mm above the floor in a level frame. Pitch the rigid body
# about the drive axle so the two tires and the caster ball actually contact.
_a,_b=-.1,0.
for _ in range(50):
    _mid=(_a+_b)/2
    if 28+144*math.sin(_mid)-16*math.cos(_mid)>9:_b=_mid
    else:_a=_mid
BODY_PITCH=(_a+_b)/2
PITCH_R=ry(BODY_PITCH)
AXLE_ORIGIN=np.array([64.,0,28.])

def body_point(v):return PITCH_R@(np.array(v)-AXLE_ORIGIN)+AXLE_ORIGIN

@lru_cache(None)
def fork_bounds(theta):
    p=next(p for p in build(float(theta)) if p['id']=='FORK-R')
    v=mesh(p)[0].reshape(-1,3)+np.array([96,0,4])
    v=(v-AXLE_ORIGIN)@PITCH_R.T+AXLE_ORIGIN
    return float(v[:,0].max()),float(v[:,2].min()),float(v[:,2].max())

_a,_b=-.4,LOW
for _ in range(40):
    _mid=(_a+_b)/2
    if fork_bounds(_mid)[2]>11.6:_b=_mid
    else:_a=_mid
INTEGRATED_LOW=(_a+_b)/2

def project_box(name,size):
    x,y,z=np.array(size)/2
    v=np.array([[-x,-y,-z],[x,-y,-z],[x,y,-z],[-x,y,-z],[-x,-y,z],[x,-y,z],[x,y,z],[-x,y,z]])*2.5
    faces=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
    lines=[f'0 Project envelope / fixture: {name}',f'0 Name: {name}.dat','0 Author: EV3 project','0 !LICENSE CC BY 4.0. Original project envelope, not a LEGO part.']
    lines+=['4 16 '+' '.join(f'{a:g}' for a in v[face].reshape(-1)) for face in faces]
    (LIB/(name+'.dat')).write_text('\n'.join(lines)+'\n')

def reference_base():
    data=(ROOT.parent/'sources'/'reference-base.glb').read_bytes()
    n,_=struct.unpack_from('<I4s',data,12);doc=json.loads(data[20:20+n])
    offset=20+n;size,kind=struct.unpack_from('<I4s',data,offset);buf=data[offset+8:offset+8+size]
    def accessor(i):
        a=doc['accessors'][i];b=doc['bufferViews'][a['bufferView']]
        dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
        width={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
        start=b.get('byteOffset',0)+a.get('byteOffset',0)
        if 'byteStride' in b:
            return np.ndarray((a['count'],width),dtype=dtype,buffer=buf,offset=start,strides=(b['byteStride'],np.dtype(dtype).itemsize)).copy()
        return np.frombuffer(buf,dtype=dtype,count=a['count']*width,offset=start).reshape(-1,width)
    lines=['0 MERGED REFERENCE CHASSIS - not a single LEGO part or verified part list',
           '0 Name: project-reference-base.dat','0 Author: RobotDSL Team after LEGO Education; LDraw contributors',
           '0 !LICENSE Derived mesh: CC BY 2.0 AND CC BY 4.0. See Integrated-Review.md.',
           '0 // Source: https://huggingface.co/datasets/Aki-Frank/robotdsl-library-assets/resolve/main/parts/lego_45544_driving_base_chassis/assets/model.glb']
    for m in doc['meshes']:
        for p in m['primitives']:
            vertices=accessor(p['attributes']['POSITION'])*2500 # meters -> LDU
            ix=accessor(p['indices']).reshape(-1,3)
            col=doc.get('materials',[{}])[p.get('material',0)].get('pbrMetallicRoughness',{}).get('baseColorFactor',[.63,.65,.67,1])[:3]
            codes=[0,1,4,7,14,15,71,72]
            color=min(codes,key=lambda c:np.linalg.norm(rgb(c)-col))
            for face in vertices[ix]:lines.append('3 '+str(color)+' '+' '.join(f'{v:.5f}' for v in face.reshape(-1)))
    (LIB/'project-reference-base.dat').write_text('\n'.join(lines)+'\n')

def state(i):
    t=i/70
    if t<=.2:return 40*t/.2,INTEGRATED_LOW,0,'Approach (open-loop illustration)'
    if t<=.4:
        theta=INTEGRATED_LOW+(HIGH-INTEGRATED_LOW)*(t-.2)/.2
        return 40,theta,max(0,fork_bounds(theta)[2]-11.6-4.4),'Lift and take up entry clearance'
    if t<=.7:return 40-120*(t-.4)/.3,HIGH,fork_bounds(HIGH)[2]-16,'Reverse carrying pallet'
    if t<=.9:
        theta=HIGH-(HIGH-INTEGRATED_LOW)*(t-.7)/.2
        return -80,theta,max(0,fork_bounds(theta)[2]-16),'Lower at delivery location'
    return -80-50*(t-.9)/.1,INTEGRATED_LOW,0,'Withdraw forks'

def assembly(i=0):
    dx,theta,pallet_z,stage=state(i)
    pp=build(theta)
    # Forward-axle variant: lift input is raised to clear the front tires.
    # New 40T -> 24T stage is a speed increase; total reduction is 9*24/40=5.4.
    lower_phase=-math.pi/4-9*theta
    upper_phase=(math.pi-24*lower_phase)/40
    pp=[p for p in pp if p['id'] not in ['MOTOR-BRACKET-SPACER','MOTOR-BRACKET-TOP-PIN']]
    for p in pp:
        if p['id']=='INPUT-AXLE':p['file']='3708.dat';p['color']=0;p['position'][1]=0
        if p['id']=='INPUT-INNER-BUSH':p['file']='3648.dat';p['color']=72;p['rotation']=(ry(lower_phase)@RSHAFT).tolist()
        if p['id'] in ['MOTOR-BRACKET-SPINE','LIFT-MOTOR-BODY','LIFT-MOTOR-ROTOR'] or p['id'].startswith('MOTOR-FACE-PIN-'):
            p['position'][2]+=32
        if p['id']=='LIFT-MOTOR-ROTOR':
            rm=np.array([[1,0,0],[0,0,-1],[0,1,0]])
            a=-upper_phase;rz=np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
            p['rotation']=(rm@rz).tolist()
    pp.append(part('RAISED-INPUT-SHAFT','3737',0,[-32,-4,80],ry(upper_phase)@RAXLE,'06b Raised lift input'))
    pp.append(part('RAISED-INPUT-40T','3649',71,[-32,4,80],ry(upper_phase)@RSHAFT,'06b Raised lift input'))
    for name,file,pos in [('UPPER-INPUT-INNER-BUSH','3713',[-32,-4,80]),('UPPER-INPUT-HALF-L','4265c',[-32,-10,80]),
                          ('UPPER-INPUT-HALF-R','4265c',[-32,10,80]),('UPPER-INPUT-OUTER-BUSH','3713',[-32,32,80])]:
        pp.append(part(name,file,14 if file=='4265c' else 71,pos,ry(upper_phase)@RSHAFT,'06b Raised lift input'))
    pp.append(part('LOWER-INPUT-OUTER-BUSH','3713',71,[-32,-40,48],ry(lower_phase)@RSHAFT,'06b Raised lift input'))
    for p in pp:p['position'][0]+=96+dx;p['position'][2]+=4
    # Replace the rear/top cross-tie axles so the two adapter rails fit on them.
    for p in pp:
        if p['id'] in ['TIE-AXLE-1','TIE-AXLE-2']:p['file']='3737.dat'
        if p['id'].startswith(('TIE-RETAINER-1-','TIE-RETAINER-2-')):p['position'][1]=38*np.sign(p['position'][1])
    def add(name,file,color,pos,rot=I,group='07 Robot layout',**kw):
        pos=np.array(pos,float);pos[0]+=dx
        pp.append(part(name,file,color,pos,rot,group,**kw))
    chassis,joints=build_chassis()
    for p in chassis:p['position'][0]+=dx;pp.append(p)
    rm=np.array([[0,0,1],[-1,0,0],[0,-1,0]])
    for side,sgn in [('L',1),('R',-1)]:
        add('DRIVE-MOTOR-'+side,'95658',15,[64,32*sgn,28],rm,group='08 Drive layout',mount_status='custom forward mounting required')
        add('WHEEL-HUB-'+side,'56908',71,[64,64*sgn,28],ry(-dx/28)@RSHAFT,group='08 Drive layout')
        add('TIRE-'+side,'41897',0,[64,64*sgn,28],ry(-dx/28)@RSHAFT,group='08 Drive layout')
        add('DRIVE-AXLE-'+side,'60485',71,[64,52*sgn,28],ry(-dx/28)@RAXLE,group='08 Drive layout')
        add('WHEEL-COLLAR-'+side,'3713',71,[64,82*sgn,28],ry(-dx/28)@RSHAFT,group='08 Drive layout')
        # Lower L adapter locks a vertical post to the fixed frame at two
        # cross-shaft positions. Its short upright leg pins to the rear post.
        rb=np.array([[0,0,-1],[0,1,0],[1,0,0]])
        add('ADAPTER-RAIL-'+side,'32526',1,[80,24*sgn,84],rb,group='09 Chassis/lift bridge')
        for xx in [48,80]:
            add(f'BRIDGE-POST-{side}-{xx}','40490',71,[xx,32*sgn,100],group='09 Chassis/lift bridge')
            add(f'BRIDGE-TOP-AXLE-{side}-{xx}','60485',71,[xx,60*sgn,116],RAXLE,group='09 Chassis/lift bridge')
            for yy in [44,60]:add(f'BRIDGE-TUBE-{side}-{xx}-{yy}','62462',71,[xx,yy*sgn,116],RAXLE,group='09 Chassis/lift bridge')
            add(f'BRIDGE-SPACER-{side}-{xx}','3713',71,[xx,72*sgn,116],RSHAFT,group='09 Chassis/lift bridge')
            for yy in [26,88]:
                add(f'BRIDGE-RETAINER-{side}-{xx}-{yy}','4265c' if yy==26 else '3713',14 if yy==26 else 71,[xx,yy*sgn,116],RSHAFT,group='09 Chassis/lift bridge')
        add('BRIDGE-CORNER-PIN-'+side,'2780',0,[48,28*sgn,100],RAXLE,group='09 Chassis/lift bridge')
        add('BRIDGE-SIDE-'+side,'32278',15,[32,80*sgn,116],RBEAM,group='09 Chassis/lift bridge')
        for xx in [0,8]:
            add(f'BRIDGE-BODY-INNER-PIN-{side}-{xx}','2780',0,[xx,60*sgn,116],RAXLE,group='09 Chassis/lift bridge')
            add(f'BRIDGE-BODY-TUBE-{side}-{xx}','62462',71,[xx,68*sgn,116],RAXLE,group='09 Chassis/lift bridge')
            add(f'BRIDGE-BODY-OUTER-PIN-{side}-{xx}','2780',0,[xx,76*sgn,116],RAXLE,group='09 Chassis/lift bridge')
    add('COLOR-SENSOR','95650',15,[36,0,32],np.array([[0,0,1],[1,0,0],[0,1,0]]),group='10 Sensors',mount_status='bracket open; optical orientation to confirm')
    add('TOUCH-SENSOR','95648',15,[110,-56,64],np.array([[0,0,1],[1,0,0],[0,1,0]]),group='10 Sensors',mount_status='trigger and bracket open')
    add('CAMERA-ENVELOPE','project-camera',14,[-8,0,156],group='11 Concept envelopes',placeholder=True)
    add('CAMERA-SUPPORT-ENVELOPE','project-camera-support',1,[-8,0,133],group='11 Concept envelopes',placeholder=True)
    for name,z in [('LOWER-STOP-ENVELOPE',40),('UPPER-STOP-ENVELOPE',66)]:
        add(name,'project-stop',4,[111,-24,z],group='11 Concept envelopes',placeholder=True)
    # Rigid stance transform: preserve every connection while seating caster.
    pivot=AXLE_ORIGIN+np.array([dx,0,0])
    for p in pp:
        p['position']=(PITCH_R@(np.array(p['position'])-pivot)+pivot).tolist()
        p['rotation']=(PITCH_R@np.array(p['rotation'])).tolist()
    # Station pallet is stationary until supported, then follows the carriage
    # horizontally, including its small fore-aft arc. No friction simulation.
    carried = i>=14 and i<=63
    pallet_x=fork_bounds(INTEGRATED_LOW)[0]+32
    if carried:pallet_x=fork_bounds(theta)[0]+dx-8
    elif i>63:pallet_x+=-120
    def fixture(name,file,col,pos,group='12 Pallet and station'):
        pp.append(part(name,file,col,pos,I,group,fixture=True))
    fixture('PALLET-DECK','project-pallet-deck',7,[pallet_x,0,20+pallet_z])
    for yy in [-32,0,32]:fixture(f'PALLET-RUNNER-{yy}','project-runner',7,[pallet_x,yy,8+pallet_z])
    fixture('LOAD-CUBE','project-cube',14,[pallet_x,0,44+pallet_z])
    fixture('STATION-TARGET','project-target',4,[314,0,72])
    return pp,dict(stage=stage,robot_x=dx,angle_degrees=math.degrees(theta),pallet_rise=pallet_z)

def run():
    for name,size in [('project-camera',[40,30,24]),('project-camera-support',[12,12,22]),('project-stop',[6,8,4]),
                      ('project-pallet-deck',[64,80,8]),('project-runner',[64,16,16]),('project-cube',[40,40,40]),('project-target',[4,40,64])]:project_box(name,size)
    all_poses=[assembly(i) for i in range(71)]
    parts=all_poses[0][0];names=sorted({p['file'] for p in parts})
    geoms={}
    for f in names:
        t,c=geometry(f);t=t*.4
        ns=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);ns/=np.maximum(np.linalg.norm(ns,axis=1)[:,None],1e-12)
        cc=np.array([rgb(k) if k!=16 else [-1,-1,-1] for k in c])
        geoms[f]=dict(v=blob(t.reshape(-1,3)),n=blob(np.repeat(ns,3,axis=0)),c=blob(np.repeat(cc,3,axis=0)),count=len(t)*3)
    data=dict(parts=parts,geometries=geoms,poses=[[np.r_[np.array(p['rotation']).reshape(-1),p['position']].round(6).tolist() for p in pp] for pp,meta in all_poses],
              pose_meta=[meta for pp,meta in all_poses],palette={str(k):rgb(k).tolist() for k in [0,1,4,7,14,15,16,71,72,79,24]},low=math.degrees(INTEGRATED_LOW),high=25)
    template=(ROOT/'viewer-template.html').read_text(encoding='utf-8')
    start=template.index('<h2>What this model contains</h2>');end=template.index('</aside>',start)
    template=template[:start]+'''<h2>Spatial integration study</h2><p class="small">Gray: LEGO geometry / reference base. Blue: proposed adapter rails and camera support. Orange: assumed camera envelope and load. Red: proposed stop envelopes and station target.</p><h2>Scope</h2><p class="small">The lift-side adapter axes are checked. The chassis-side adapter, motor/wheel layout, sensor mounts, switch trigger, stops, cables and camera remain unverified. Animation illustrates a sequence; it is not a navigation or contact simulation.</p><p class="small"><a href="Integrated-Review.md">Review and open issues</a><br><a href="robot-station.mpd">Self-contained CAD scene</a><br><a href="layout-parts.csv">Added-component list</a></p><p class="small">Base reconstruction: RobotDSL Team after LEGO Education, with LDraw geometry. See attribution in the review.</p>'''+template[end:]
    template=template.replace('EV3 forklift: digital lift module','EV3 forklift: integrated layout').replace('EV3 lift - digital prototype','EV3 integrated spatial prototype').replace('Real LEGO part geometry.','Reference chassis + real-part lift + explicit concept envelopes.').replace('Lift position','Pickup / delivery sequence').replace('>Lower</button>','>Start</button>').replace('>Raise</button>','>End</button>').replace('Whole module','Whole scene')
    template=template.replace('distance=310','distance=850').replace('target=[3,-24,46]','target=[100,0,75]').replace('distance=310;','distance=850;')
    template=template.replace('Reference chassis + real-part lift + explicit concept envelopes.','Custom part-by-part chassis and lift; camera/stop envelopes are provisional.').replace('Gray: LEGO geometry / reference base.','Gray: individual LEGO parts.').replace('Base reconstruction: RobotDSL Team after LEGO Education, with LDraw geometry.','Individual chassis geometry: LDraw contributors; custom assembly by this project.').replace('the chassis-side adapter, motor/wheel layout, sensor mounts','the lift-to-chassis adapter, motor mount engagement, sensor mounts')
    template=template.replace('The lift-side adapter axes are checked. The chassis-side adapter, motor/wheel layout, sensor mounts, switch trigger, stops, cables and camera remain unverified.',
        'Chassis, brick, caster, motor and bridge connection axes are defined. Pin engagement, stiffness, full interference, sensor brackets, stops, cables and camera remain unverified.')
    template=template.replace('Integrated-Review.md','Custom-Chassis-Review.md').replace('layout-parts.csv','catalog-parts.csv').replace('Added-component list','Catalog parts and stock comparison')
    old="document.getElementById('angle').textContent=theta.toFixed(1)+'° linkage angle';document.getElementById('travel').textContent='Carriage rise: '+rise.toFixed(1)+' mm';"
    new="document.getElementById('angle').textContent=D.pose_meta[pose].stage;document.getElementById('travel').textContent='Pallet rise: '+D.pose_meta[pose].pallet_rise.toFixed(1)+' mm';"
    assert old in template;template=template.replace(old,new).replace('complete lift module','integrated spatial scene')
    template=template.replace("if(params.get('mode')==='gears')onlyGears=true;draw();",
        "if(params.get('pose')==='carry')document.getElementById('pose').value=38;if(params.get('mode')==='gears')onlyGears=true;draw();")
    template=template.replace("!p.group.startsWith('02'))continue", "!p.group.startsWith('02')&&!p.group.startsWith('06b'))continue")
    (OUT/'EV3-Integrated-Viewer.html').write_text(template.replace('__MODEL_DATA__',json.dumps(data,separators=(',',':'))),encoding='utf-8')
    (OUT/'assembly-initial.json').write_text(json.dumps(parts,indent=2))
    (OUT/'sequence.json').write_text(json.dumps(data['pose_meta'],indent=2))
    export_ldr(parts,OUT/'robot-station.ldr','EV3 integrated spatial study - NOT build-released')
    files=dependencies(parts)
    content=['0 FILE robot-station.ldr',(OUT/'robot-station.ldr').read_text(),'0 NOFILE']
    for f in sorted(files):content+=['0 FILE '+f,find(f).read_text(encoding='utf-8-sig',errors='replace'),'0 NOFILE']
    (OUT/'robot-station.mpd').write_text('\n'.join(content),encoding='utf-8')
    rows=Counter(p['file'] for p in parts if not p.get('fixture') and not p.get('placeholder') and not p.get('reference'))
    with (OUT/'layout-parts.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['Design file','Placed instances','Note'])
        for file,n in sorted(rows.items()):w.writerow([file,n,'Excludes parts inside merged reference chassis; motor body/rotor counted separately'])
    checks=[]
    def ck(name,ok,evidence):checks.append(dict(check=name,status='PASS' if ok else 'FAIL',evidence=evidence))
    for side,sgn in [('L',1),('R',-1)]:
        rail=next(p for p in parts if p['id']=='ADAPTER-RAIL-'+side)
        frame=next(p for p in parts if p['id']==('FRAME-L' if sgn>0 else 'FRAME-R'))
        for xx in [48,80]:ck(f'Lift adapter hole {side} at X={xx}',axis_present(rail,body_point([xx,24*sgn,84]),[0,1,0]) and axis_present(frame,body_point([xx,16*sgn,84]),[0,1,0]),'Real part bore axes coincide after stance rotation.')
    ck('Sequence part order stable',all([p['id'] for p in pp]==[p['id'] for p in parts] for pp,meta in all_poses),'71 poses have identical part IDs and rigid placements.')
    ck('Tire ground contact',abs(mesh(next(p for p in parts if p['id']=='TIRE-L'))[0][:,:,2].min())<.01,'56 mm tire diameter and 28 mm axle height.')
    ck('Pallet pickup clearance',25<data['pose_meta'][28]['pallet_rise']<35,'Recalculated after stance pitch; initial fork-to-pallet gap is 4.4 mm.')
    ck('Proper rotations',all(abs(np.linalg.det(p['rotation'])-1)<1e-8 for pp,m in all_poses for p in pp),'No non-rigid scaling in component placements.')
    (OUT/'integration-checks.json').write_text(json.dumps(checks,indent=2))
    print(len(parts),'placed scene instances;',len(files),'embedded geometry files')
    print('Checks',[(c['check'],c['status']) for c in checks])
    print('Status: integrated spatial study; complete connection model NOT achieved.')

if __name__=='__main__':run()
