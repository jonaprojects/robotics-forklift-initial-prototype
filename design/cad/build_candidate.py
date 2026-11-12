"""Separate B0.1 mechanical build candidate; I0.3 source/export stays intact."""
import json,math,csv,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
from build_integrated import assembly as previous,state,PITCH_R,AXLE_ORIGIN,project_box,INTEGRATED_LOW
from build_lift import RAXLE,RSHAFT,ry,beam_rotation
from ldraw_geometry import part,mesh,geometry,export_ldr,find,axis_present
from render_model import blob,rgb
from package_model import dependencies
from candidate_steps import STEPS,stage

ROOT=Path(__file__).resolve().parent;OUT=ROOT.parent/'build_candidate';OUT.mkdir(exist_ok=True)
I=np.eye(3)
RZ=np.array([[0,1,0],[0,0,1],[1,0,0]]) # native axial X -> world Z
BLOCK=np.array([[0,1,0],[0,0,1],[1,0,0]]) # 6536: bush Z, pin Y at X+8
ANCHOR=np.array([[0,-1,0],[0,0,-1],[1,0,0]]) # bush Z, pin Y at X-8
BEAMZ=np.array([[0,0,1],[1,0,0],[0,1,0]]) # beam longitudinal X, holes Z
KEYR=BEAMZ@np.diag([-1,1,-1])
CARRIER=np.array([[0,1,0],[1,0,0],[0,0,-1]]) # bush Y, pin Z at X+8
MID_CLOCK=math.radians(-1.5) # common intermediate-shaft clock, adjusted using tooth surfaces

def scene(i=0):
    old,meta=previous(i);dx=meta['robot_x'];theta=math.radians(meta['angle_degrees']);pivot=AXLE_ORIGIN+[dx,0,0]
    fixed=[];fixtures=[]
    for p in old:
        p=json.loads(json.dumps(p))
        if p.get('fixture'):fixtures.append(p);continue
        if p.get('placeholder') or p['id'] in ['COLOR-SENSOR','TOUCH-SENSOR','OUTPUT-COLLAR-0','OUTPUT-COLLAR-1']:continue
        if p['id'].startswith('CORNER-LONG-PIN-') and p['id'].endswith('--32--32'):continue
        p['position']=(PITCH_R.T@(np.array(p['position'])-pivot)+pivot-[dx,0,0]).tolist()
        p['rotation']=(PITCH_R.T@np.array(p['rotation'])).tolist()
        n=p['id'];clock=0.
        if n.startswith(('INTERMEDIATE-','GEAR-24-A','GEAR-8-B')):clock=MID_CLOCK
        elif n.startswith(('INPUT-','GEAR-8-A','LOWER-INPUT-')):clock=-3*MID_CLOCK
        elif n.startswith(('RAISED-INPUT-','UPPER-INPUT-','LIFT-MOTOR-ROTOR')):clock=1.8*MID_CLOCK
        if clock:p['rotation']=(ry(clock)@np.array(p['rotation'])).tolist()
        # Rear flange is 12 mm outboard of the motor origin, not 8 mm.
        # Moving the motors 4 mm inward makes the 16 mm stand-off fit exactly.
        if p['id'].startswith('DRIVE-MOTOR-'):p['position'][1]=28 if p['id'].endswith('L') else -28
        if p['id']=='UPPER-PIVOT-AXLE':p['file']='3708.dat'
        if p['id']=='INPUT-AXLE':p['position'][1]=4
        if p['id']=='RAISED-INPUT-SHAFT':p['file']='3708.dat';p['position'][1]=4
        if p['id']=='RAISED-INPUT-40T':p['position'][1]=44
        if p['id']=='INPUT-INNER-BUSH':p['file']='3713.dat';p['color']=71
        fixed.append(p)
    def add(name,file,col,pos,rot=I,group='B0.1 mounts',**kw):
        p=part(name,file,col,pos,rot,group,**kw);fixed.append(p);return p
    lower_phase=-math.pi/4-9*theta-3*MID_CLOCK
    upper_phase=(math.pi-24*lower_phase)/40
    add('LOWER-EXTERNAL-24T','3648',72,[64,44,52],ry(lower_phase)@RSHAFT,group='06b Raised lift input')
    add('LOWER-EXTERNAL-FULL-SPACER','3713',71,[64,32,52],ry(lower_phase)@RSHAFT,group='06b Raised lift input')
    for name,z,ph in [('LOWER',52,lower_phase),('UPPER',84,upper_phase)]:
        for y in [38,50]:add(f'{name}-EXTERNAL-HALF-{y}','4265c',14,[64,y,z],ry(ph)@RSHAFT,group='06b Raised lift input')
    # Color sensor -Z optical face points at floor, connector bores run X.
    add('COLOR-SENSOR','95650',15,[-48,0,36])
    add('COLOR-BRACKET','32524',71,[-40,0,44],np.array([[0,1,0],[-1,0,0],[0,0,1]]))
    for z in [28,44]:add(f'COLOR-FACE-PIN-{z}','2780',0,[-44,0,z])
    rblock=np.array([[0,0,1],[1,0,0],[0,1,0]])
    for z in [28,68]:
        rb=rblock if z==28 else np.array([[0,0,-1],[1,0,0],[0,-1,0]])
        add(f'COLOR-BLOCK-{z}','6536',71,[-32,0,z],rb)
        add(f'COLOR-BRACKET-PIN-{z}','2780',0,[-36,0,z+8 if z==28 else z-8])
        add(f'COLOR-CROSS-CENTER-{z}','3707',0,[-32,0,z],RAXLE)
        for s in [-1,1]:
            add(f'COLOR-CROSS-OUTER-{z}-{s}','44294',71,[-32,60*s,z],RAXLE)
            add(f'COLOR-CROSS-JOINER-{z}-{s}','59443',4,[-32,32*s,z],RSHAFT)
            for y in [12,48]:add(f'COLOR-CROSS-TUBE-{z}-{s}-{y}','62462',71,[-32,y*s,z],RAXLE)
            for y in [22,82]:add(f'COLOR-CROSS-RETAINER-{z}-{s}-{y}','4265c',14,[-32,y*s,z],RSHAFT)
            if z==68:
                for y in [60,76]:add(f'COLOR-CROSS-SPACE-{s}-{y}','3713',71,[-32,y*s,z],RSHAFT)
    # Touch sensor, two L brackets and a stand fixed at two existing shaft axes.
    rt=np.array([[0,1,0],[1,0,0],[0,0,-1]])
    add('TOUCH-SENSOR','99385c01',15,[120,-56,12],rt,physical_assembly='95648')
    compression=max(0,1.8-(theta-INTEGRATED_LOW)*30)
    add('TOUCH-BUTTON','99386',4,[104,-56,44-compression],rt,physical_assembly='95648')
    add('TOUCH-MOUNT-BEAM','32523',4,[120,-48,12])
    add('TOUCH-STAND','32525',71,[96,-40,44])
    for z in [52,84]:add(f'TOUCH-STAND-OUTER-{z}','4265c',14,[96,-46,z],RSHAFT)
    add('TOUCH-STAND-UPPER-INNER','4265c',14,[96,-34,84],RSHAFT)
    add('TOUCH-LOWER-L','32526',71,[96,-32,4],np.array([[0,0,1],[0,1,0],[1,0,0]]))
    # Reflection above is unnecessary for a symmetric thickness; use a proper rotation.
    fixed[-1]['rotation']=np.array([[0,0,1],[0,-1,0],[1,0,0]]).tolist()
    add('TOUCH-UPPER-L','32526',71,[96,-24,20],np.array([[0,0,1],[0,1,0],[-1,0,0]]))
    add('TOUCH-UPPER-SPACER','60483',0,[96,-32,12])
    add('TOUCH-REAR-LOW-PIN','2780',0,[96,-36,4],RAXLE)
    add('TOUCH-REAR-HIGH-PIN','6558',1,[96,-32,20],RAXLE)
    for z in [4,20]:
        add(f'TOUCH-CLAMP-AXLE-{z}','3706',0,[120,-40,z],RAXLE)
        add(f'TOUCH-CLAMP-SPACE-{z}','3713',71,[120,-40,z],RSHAFT)
        add(f'TOUCH-CLAMP-FILL-{z}','3713',71,[120,-24 if z==4 else -32,z],RSHAFT)
        for y in [-62,-18]:add(f'TOUCH-CLAMP-HALF-{z}-{y}','4265c',14,[120,y,z],RSHAFT)
    phase=-theta
    add('TOUCH-TRIGGER','32523',4,[96+24*math.cos(theta),-48,52+24*math.sin(theta)],beam_rotation(theta))
    for t in [16,32]:
        x,z=96+t*math.cos(theta),52+t*math.sin(theta)
        add(f'TOUCH-TRIGGER-PIN-{t}','2780',0,[x,-28,z],RAXLE)
        add(f'TOUCH-TRIGGER-TUBE-{t}','62462',71,[x,-36,z],RAXLE)
        add(f'TOUCH-TRIGGER-OUTER-PIN-{t}','2780',0,[x,-44,z],RAXLE)
    # Stop column: existing output and upper pivot shafts locate two keyed blocks.
    for z in [52,84]:
        add(f'STOP-COLUMN-ANCHOR-{z}','6536',71,[104,40,z],ANCHOR)
        add(f'STOP-ANCHOR-OUTER-{z}','4265c',14,[96,46,z],RSHAFT)
    add('STOP-UPPER-ANCHOR-SPACER','4265c',14,[96,34,84],RSHAFT)
    add('STOP-COLUMN','3708',0,[104,40,60],RZ)
    for z in [46,90]:add(f'STOP-COLUMN-LOCATOR-{z}','4265c',14,[104,40,z])
    for name,beam_z,block_z,coupler_z in [('LOW',32.2,40.2,24.2),('HIGH',76,68,68)]:
        add('STOP-BEAM-'+name,'32316',4,[112,40,beam_z],BEAMZ)
        add('STOP-KEY-'+name,'60483',0,[104,40,coupler_z],KEYR)
        add('STOP-KEY-PIN-'+name,'2780',0,[96,40,(beam_z+coupler_z)/2],RZ)
        for z in ([18.2,38.2] if name=='LOW' else [62]):add(f'STOP-CAM-RETAINER-{name}-{z}','4265c',14,[104,40,z])
        add('STOP-ROD-BLOCK-'+name,'6536',71,[112,40,block_z],CARRIER)
        add('STOP-ROD-BLOCK-PIN-'+name,'2780',0,[120,40,(beam_z+block_z)/2],RZ)
        add('STOP-ROD-'+name,'32073',71,[112,32,block_z],RAXLE)
        for y in [34,46]:add(f'STOP-ROD-RETAINER-{name}-{y}','4265c',14,[112,y,block_z],RSHAFT)
    # Universal camera holder. Foam and four straps are explicitly external consumables.
    trayrot=np.array([[1,0,0],[0,0,-1],[0,1,0]])
    add('CAMERA-TRAY','64179',71,[-80,0,129.6],trayrot)
    add('CAMERA-PAD','candidate-pad',0,[-80,0,124.6],external=True)
    add('CAMERA-TOP-PAD','candidate-top-pad',0,[-80,0,134.6],external=True)
    add('CAMERA-FIT-ENVELOPE','candidate-camera',14,[-80,0,147.6],external=True,assumed_camera=True)
    # Visualize straps with rectangular strips; exact lengths and threading in guide.
    for x in [-92,-68]:
        for y in [-18,18]:add(f'CAMERA-STRAP-SIDE-{x}-{y}','candidate-strap-side',0,[x,y,143.1],external=True)
        for z in [126.1,160.1]:add(f'CAMERA-STRAP-CROSS-{x}-{z}','candidate-strap-cross',0,[x,0,z],external=True)
    for x in [-96,-64]:
        for y in [-40,40]:add(f'TRAY-TIE-SIDE-{x}-{y}','candidate-tray-tie-side',0,[x,y,105.8],external=True)
        for z in [78,133.6]:add(f'TRAY-TIE-CROSS-{x}-{z}','candidate-tray-tie-cross',0,[x,0,z],external=True)
    # Stance transform applies to every newly mounted part as a rigid group.
    result=[]
    for p in fixed:
        p['build_step']=stage(p)
        p['position']=(PITCH_R@(np.array(p['position'])-AXLE_ORIGIN)+AXLE_ORIGIN+[dx,0,0]).tolist()
        p['rotation']=(PITCH_R@np.array(p['rotation'])).tolist();result.append(p)
    return result+fixtures,meta

def run():
    for n,size in [('candidate-pad',[40,30,2]),('candidate-top-pad',[40,30,2]),('candidate-camera',[40,30,24]),('candidate-strap-side',[2.5,1,34]),
        ('candidate-strap-cross',[2.5,36,1]),('candidate-tray-tie-side',[2.5,1,55.6]),('candidate-tray-tie-cross',[2.5,80,1])]:project_box(n,size)
    poses=[scene(i) for i in range(71)];parts=poses[0][0]
    geoms={}
    for file in sorted({p['file'] for p in parts}):
        t,c=geometry(file);t=t*.4
        ns=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);ns/=np.maximum(np.linalg.norm(ns,axis=1)[:,None],1e-12)
        cc=np.array([rgb(k) if k!=16 else [-1,-1,-1] for k in c])
        geoms[file]=dict(v=blob(t.reshape(-1,3)),n=blob(np.repeat(ns,3,axis=0)),c=blob(np.repeat(cc,3,axis=0)),count=len(t)*3)
    data=dict(parts=parts,steps=STEPS,geometries=geoms,poses=[[np.r_[np.array(p['rotation']).reshape(-1),p['position']].round(6).tolist() for p in pp] for pp,m in poses],
      pose_meta=[m for pp,m in poses],palette={str(k):rgb(k).tolist() for k in [0,1,4,7,14,15,16,71,72,79,24]},low=math.degrees(INTEGRATED_LOW),high=25)
    old=(ROOT/'candidate-template.html').read_text(encoding='utf-8')
    start=old.index("'use strict';const D=")+len("'use strict';const D=");end=old.index(';\nconst canvas=',start)
    html=old[:start]+json.dumps(data,separators=(',',':'))+old[end:]
    html=html.replace('EV3 forklift: integrated layout','EV3 forklift: B0.1 first-build candidate').replace('EV3 integrated spatial prototype','EV3 B0.1 assembly viewer').replace('Custom-Chassis-Review.md','BUILD-GUIDE.html').replace('catalog-parts.csv','parts.csv').replace('robot-station.mpd','build-candidate.mpd')
    html=html.replace('Custom part-by-part chassis and lift; camera/stop envelopes are provisional.','Mechanical candidate with sensor brackets, adjustable stops and an assumed-size camera holder.')
    html=html.replace('Prototype - whole robot not released','B0.1 - bench validation required')
    a=html.index('<h2>Spatial integration study</h2>');b=html.index('</aside>',a)
    html=html[:a]+'''<h2>Assembly instructions</h2><label for="build">Show assembly step</label><select id="build" style="max-width:100%;width:100%;padding:8px"><option value="0">Complete robot and station</option></select><label><input id="isolate" type="checkbox"> Only parts added in this step</label><div id="stepText" class="small"></div><details><summary>Parts in this step</summary><div id="stepParts" class="small"></div></details><h2>Build status</h2><p class="small">First physical build candidate. Camera envelope: 40 x 30 x 24 mm. Camera interface, measured payload and physical switch calibration require lab confirmation. Motion is an illustration.</p><p class="small"><a href="BUILD-GUIDE.html">Assembly guide and acceptance checks</a><br><a href="build-candidate.mpd">Self-contained CAD</a><br><a href="parts.csv">Physical LEGO quantities</a><br><a href="verification.json">Recorded checks and limits</a></p><p class="small">Geometry: LDraw contributors, CC BY 2.0 / 4.0. Source license headers embedded in CAD.</p>'''+html[b:]
    html=html.replace("const p=D.parts[i];if(onlyGears", "const p=D.parts[i];const bs=Number(document.getElementById('build').value);if(bs&&(p.fixture||p.build_step>bs||(document.getElementById('isolate').checked&&p.build_step!==bs)))continue;if(onlyGears")
    html=html.replace("D.palette[String(p.color)]||D.palette['71']", "(bs&&p.build_step===bs&&!p.external?[.18,.65,.82]:(D.palette[String(p.color)]||D.palette['71']))")
    html=html.replace("document.body.dataset.render='ok';", "document.body.dataset.build=String(document.getElementById('build').value);document.body.dataset.render='ok';")
    hook="""const buildSelect=document.getElementById('build');
D.steps.forEach((s,i)=>{const o=document.createElement('option');o.value=i+1;o.textContent=(i+1)+'. '+s[0];buildSelect.appendChild(o);});
function showStep(){
const n=Number(buildSelect.value);document.getElementById('stepText').textContent=n?D.steps[n-1][1]:'Choose a step. Blue marks new parts; drag to inspect both sides.';
const list=document.getElementById('stepParts');list.textContent='';
if(n){for(const p of D.parts.filter(p=>p.build_step===n)){const row=document.createElement('div');row.textContent=p.id+' | '+p.file.replace('.dat','');list.appendChild(row);}document.getElementById('pose').value=0;onlyGears=false;distance=640;target.splice(0,3,25,0,75);
if(document.getElementById('isolate').checked){const pts=D.parts.map((p,i)=>p.build_step===n?D.poses[0][i].slice(9):null).filter(Boolean);if(pts.length){const lo=[0,1,2].map(k=>Math.min(...pts.map(v=>v[k]))),hi=[0,1,2].map(k=>Math.max(...pts.map(v=>v[k])));target.splice(0,3,...lo.map((v,k)=>(v+hi[k])/2));distance=Math.max(180,3*Math.max(...hi.map((v,k)=>v-lo[k]))+100);}}}
else{target.splice(0,3,100,0,75);distance=850;}redraw();}
buildSelect.onchange=showStep;document.getElementById('isolate').onchange=showStep;
document.getElementById('all').onclick=()=>{buildSelect.value=0;document.getElementById('isolate').checked=false;onlyGears=false;showStep();};
document.getElementById('gears').onclick=()=>{buildSelect.value=0;showStep();onlyGears=true;redraw();};
document.getElementById('reset').onclick=()=>{buildSelect.value=0;showStep();yaw=-.9;pitch=.43;onlyGears=false;document.getElementById('explode').value=0;redraw();};
""".replace('\n+','\n')
    html=html.replace('const params=new URLSearchParams(location.search);',hook+'const params=new URLSearchParams(location.search);')
    html=html.replace("if(params.get('mode')==='gears')onlyGears=true;draw();", "if(params.get('mode')==='gears')onlyGears=true;if(params.get('isolate')==='1')document.getElementById('isolate').checked=true;if(params.has('step')){buildSelect.value=params.get('step');showStep();}draw();")
    (OUT/'EV3-Build-Candidate.html').write_text(html,encoding='utf-8')
    (OUT/'assembly.json').write_text(json.dumps(parts,indent=2))
    export_parts=[]
    for p in sorted(parts,key=lambda p:p.get('build_step',99)):
        q=dict(p);s=q.get('build_step',99)
        q['group']=f'{s:02} '+(STEPS[s-1][0] if s<=len(STEPS) else 'Pallet and station fixtures')
        export_parts.append(q)
    export_ldr(export_parts,OUT/'build-candidate.ldr','B0.1 first-build candidate - read BUILD-GUIDE.html and verification before building')
    ldr=(OUT/'build-candidate.ldr').read_text().replace('0 // PROTOTYPE. Unmounted interfaces and remaining checks are documented in Phase-2-Review.md.','0 // B0.1 FIRST BUILD CANDIDATE. Physical validation and camera identity remain open. See BUILD-GUIDE.html.')
    (OUT/'build-candidate.ldr').write_text(ldr)
    content=['0 FILE build-candidate.ldr',(OUT/'build-candidate.ldr').read_text(),'0 NOFILE']
    for f in sorted(dependencies(parts)):content+=['0 FILE '+f,find(f).read_text(encoding='utf-8-sig',errors='replace'),'0 NOFILE']
    (OUT/'build-candidate.mpd').write_text('\n'.join(content),encoding='utf-8')
    counts=Counter(p['file'] for p in parts if not p.get('fixture') and not p.get('external'))
    counts.pop('99535c01.dat');counts.pop('99543.dat');counts['99455.dat']=1
    counts.pop('99385c01.dat');counts.pop('99386.dat');counts['95648.dat']=1
    with (OUT/'parts.csv').open('w',newline='') as f:
        from ldraw_geometry import metadata
        w=csv.writer(f);w.writerow(['LEGO design file','Physical quantity','Description'])
        names={'3648.dat':'Technic Gear 24 Tooth (3648b alias)','4265c.dat':'Technic Half Bush (32123 alias)'}
        for file,n in sorted(counts.items()):w.writerow([file,n,names.get(file,metadata(file)['description'])])
    print('B0.1 candidate written:',len(parts),'digital instances;',sum(counts.values()),'LEGO pieces')

if __name__=='__main__':run()
