"""Recorded geometry checks, not a physical certification or general contact solver."""
import json,math,sys
from collections import Counter
import numpy as np
from build_candidate import scene,OUT
from build_integrated import AXLE_ORIGIN,PITCH_R,INTEGRATED_LOW,fork_bounds
from build_lift import beam_rotation,RAXLE
from ldraw_geometry import mesh,axis_present,part
from check_clearances import tooth_overlap
from custom_chassis import build_chassis

def raw_scene(i=0):
    pp,m=scene(i);pivot=AXLE_ORIGIN+[m['robot_x'],0,0]
    for p in pp:
        if p.get('fixture'):continue
        p['position']=(PITCH_R.T@(np.array(p['position'])-pivot)+AXLE_ORIGIN).tolist()
        p['rotation']=(PITCH_R.T@np.array(p['rotation'])).tolist()
    return {p['id']:p for p in pp},m

def run():
    checks=[];pp,m=raw_scene()
    def ck(name,ok,**evidence):checks.append(dict(check=name,status='PASS' if bool(ok) else 'FAIL',**evidence))
    def joint(name,a,b,pt,axis=(0,1,0)):
        ck(name,axis_present(pp[a],pt,axis) and axis_present(pp[b],pt,axis),parts=[a,b],point_mm=pt,axis=list(axis))
    for j in build_chassis()[1]:joint('Inherited frame: '+j['id'],j['a'],j['b'],j['point'])
    for s in [-1,1]:
        side='L' if s==1 else 'R'
        for x in [48,80]:
            joint(f'Adapter {side}/{x}','ADAPTER-RAIL-'+side,'FRAME-'+side,[x,0,84])
            joint(f'Bridge upper {side}/{x}',f'BRIDGE-POST-{side}-{x}','BRIDGE-SIDE-'+side,[x,0,116])
        joint('Bridge corner '+side,'ADAPTER-RAIL-'+side,f'BRIDGE-POST-{side}-48',[48,0,100])
        for x in [0,8]:joint(f'Bridge body {side}/{x}','BRIDGE-SIDE-'+side,'BRICK-RAIL-'+side,[x,0,116])
    for z in [28,44]:joint('Sensor side pin '+str(z),'COLOR-SENSOR','COLOR-BRACKET',[-44,0,z],(1,0,0))
    for z in [28,68]:
        bz=36 if z==28 else 60
        joint('Color crossblock pin '+str(z),'COLOR-BRACKET','COLOR-BLOCK-'+str(z),[-36,0,bz],(1,0,0))
        for s in [-1,1]:
            joint(f'Color crossshaft tower {z}/{s}','COLOR-BLOCK-'+str(z),'CHASSIS-TOWER-'+('L' if s==1 else 'R')+'--32',[-32,0,z])
    for z in [4,20]:
        joint('Touch clamp '+str(z),'TOUCH-SENSOR','TOUCH-MOUNT-BEAM',[120,0,z])
        joint('Touch brace '+str(z),'TOUCH-LOWER-L' if z==4 else 'TOUCH-UPPER-L','TOUCH-MOUNT-BEAM',[120,0,z])
        ck('Touch unused brace-layer filler '+str(z),axis_present(pp['TOUCH-CLAMP-FILL-'+str(z)],[120,0,z],[0,1,0]))
    joint('Touch rear lower','TOUCH-STAND','TOUCH-LOWER-L',[96,0,4])
    joint('Touch rear upper','TOUCH-STAND','TOUCH-UPPER-L',[96,0,20])
    for z in [52,84]:
        joint('Touch stand shaft '+str(z),'TOUCH-STAND','FRAME-R',[96,0,z])
        joint('Stop anchor bore '+str(z),'STOP-COLUMN-ANCHOR-'+str(z),'FRAME-L',[96,0,z])
        ck('Stop anchor vertical axis '+str(z),axis_present(pp['STOP-COLUMN-ANCHOR-'+str(z)],[104,40,z],[0,0,1]))
    for name,beamz,keyz,blockz in [('LOW',32.2,24.2,40.2),('HIGH',76,68,68)]:
        joint('Stop key '+name,'STOP-BEAM-'+name,'STOP-KEY-'+name,[96,40,beamz],(0,0,1))
        joint('Stop rod support '+name,'STOP-BEAM-'+name,'STOP-ROD-BLOCK-'+name,[120,40,beamz],(0,0,1))
        ck('Stop rod axial alignment '+name,axis_present(pp['STOP-ROD-BLOCK-'+name],[112,32,blockz],[0,1,0]))
    ck('All new rigid transforms',all(np.allclose(np.array(p['rotation']).T@p['rotation'],np.eye(3),atol=1e-8) and abs(np.linalg.det(p['rotation'])-1)<1e-8 for p in pp.values()))
    # The motor flange's actual outer surface, not its hole primitive origin.
    for s in [-1,1]:
        side='L' if s==1 else 'R'
        motor=mesh(pp['DRIVE-MOTOR-'+side])[0].reshape(-1,3)
        v=motor[(abs(motor[:,0]+8)<4)&(abs(motor[:,2]-28)<4)]
        face=float((v[:,1]*s).max())
        tube=mesh(pp['MOTOR-STANDOFF-'+side+'--8'])[0].reshape(-1,3)
        start=float((tube[:,1]*s).min())
        ck('Corrected flange / stand-off '+side,abs(face-start)<.01,motor_flange_face_mm=face,tube_inner_face_mm=start)
    floors=[];trigger=[];poses=[]
    for i in range(71):
        p,m=scene(i);poses.append(p)
        for a in p:
            if a.get('fixture'):continue
            if float(mesh(a)[0][:,:,2].min())<-.05:floors.append([i,a['id']])
        raw,_=raw_scene(i);theta=math.radians(m['angle_degrees'])
        for t in [16,32]:
            point=[96+t*math.cos(theta),0,52+t*math.sin(theta)]
            trigger.append(axis_present(raw['TOUCH-TRIGGER'],point,[0,1,0]) and axis_present(raw['LOWER-LINK-R'],point,[0,1,0]))
    ck('No below-floor robot surfaces in 71 poses',not floors,intrusions=floors)
    ck('Trigger two pin axes across 71 poses',all(trigger),tested_axes=len(trigger))
    ck('Part identity/order constant in animation',all([p['id'] for p in pps]==[p['id'] for p in poses[0]] for pps in poses))
    gears=[]
    for i in range(14,29):
        raw,_=raw_scene(i)
        for a,b,y in [('GEAR-8-A','GEAR-24-A',-4),('GEAR-8-B','GEAR-24-B',4),('RAISED-INPUT-40T','LOWER-EXTERNAL-24T',44)]:
            count,area=tooth_overlap(raw[a],raw[b],y,spacing=.05)
            gears.append(dict(pose=i,pair=[a,b],overlap_samples=count,area_mm2=area))
    ck('Three gear meshes across 15 unique linkage angles',all(g['overlap_samples']==0 for g in gears),grid_mm=.05,samples=gears)
    for name in ['TIRE-L','TIRE-R','CASTER-BALL']:
        p=next(x for x in poses[0] if x['id']==name);z=float(mesh(p)[0][:,:,2].min())
        ck(name+' floor contact',abs(z)<.05,bottom_mm=z)
    # Find first sampled solid contact at each overtravel stop, center plane.
    def overlaps(deg,rod):
        a=math.radians(deg)
        link=part('test-link','32524',71,[96+24*math.cos(a),24,52+24*math.sin(a)],beam_rotation(a),'test')
        return tooth_overlap(link,pp[rod],24,spacing=.05)[0]>0
    contacts={}
    for name,lo,hi in [('LOW',-25,math.degrees(INTEGRATED_LOW)),('HIGH',25,38)]:
        rod='STOP-ROD-'+name
        for _ in range(14):
            mid=(lo+hi)/2;hit=overlaps(mid,rod)
            if (name=='LOW' and hit) or (name=='HIGH' and not hit):lo=mid
            else:hi=mid
        deg=(lo+hi)/2;contacts[name]=deg
        ck(name+' stop lies outside normal stroke',not overlaps(math.degrees(INTEGRATED_LOW) if name=='LOW' else 25,rod) and overlaps(-25 if name=='LOW' else 38,rod),sampled_contact_degrees=deg,resolution_mm=.05)
    lowfloor=fork_bounds(math.radians(contacts['LOW']))[1]
    ck('Fork clears floor at sampled lower stop',lowfloor>1,minimum_fork_surface_mm=lowfloor)
    # Cross-sectional solid checks: ignore only the supplied switch's own body/button.
    audit=json.loads((OUT/'whole-structure-audit.json').read_text())
    internal=[x for x in audit if {x['a'],x['b']}=={'TOUCH-SENSOR','TOUCH-BUTTON'}]
    external=[x for x in audit if x not in internal]
    ck('Selected structural sections at low/mid/high',not external,unresolved_pairs=external,excluded_supplied_switch_internal_pairs=len(internal),grid_mm=.4)
    out=dict(revision='B0.1',status='FIRST PHYSICAL BUILD CANDIDATE - camera identity and lab acceptance open',checks=checks,
        summary=dict(Counter(c['status'] for c in checks)),normal_low_degrees=math.degrees(INTEGRATED_LOW),normal_high_degrees=25,
        nominal_motor_stroke_degrees=5.4*(25-math.degrees(INTEGRATED_LOW)),stop_contacts_degrees=contacts,
        verification_limits=['Section sampling is not full 3D collision/contact certification; fastener interference fits and motor internals excluded.',
         'Only 15 unique normal linkage angles occur in the 71-pose demonstration; structural audit covers three poses.',
         'Switch compression is illustrated at 1.8 mm maximum; actual electrical trip and travel must be measured.',
         'Camera dimensions, mass, connector clearance and interface are assumptions.',
         'Cable routes are assembly instructions, not a modeled swept cable volume.',
         'Payload rating, loaded stability, connection stiffness and assembly access need physical bench validation.'])
    (OUT/'verification.json').write_text(json.dumps(out,indent=2))
    print(out['summary']);print('Stop contacts:',contacts,'lower-stop fork clearance:',lowfloor)
    for c in checks:
        if c['status']!='PASS':print(c)
    if any(c['status']=='FAIL' for c in checks):sys.exit(2)

if __name__=='__main__':run()
