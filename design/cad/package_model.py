"""Package the verified-scope digital module and write an honest review."""
import json,csv,zipfile,hashlib,math
from pathlib import Path
from collections import Counter
import numpy as np
from ldraw_geometry import find,metadata,mesh
from build_lift import build,LOW,HIGH

ROOT=Path(__file__).resolve().parent
STOCK={
 '2780.dat':('4121715',60,'black 2L friction pin'),
 '32524.dat':('4495930',4,'gray 7L beam'),
 '32526.dat':('4585040',4,'white 3x5 right-angle beam'),
 '3647.dat':('4514559',4,'dark-gray 8T gear'),
 '3648.dat':('4514558',4,'dark-gray 24T gear'),
 '3673.dat':('4211807',10,'gray 2L low-friction pin'),
 '3706.dat':('370626',4,'black 6L axle'),
 '3707.dat':('370726',2,'black 8L axle'),
 '3708.dat':('370826',2,'black 12L axle'),
 '3713.dat':('4211622',10,'gray full bush'),
 '40490.dat':('4211866',6,'gray 9L beam'),
 '4265c.dat':('4239601',10,'yellow half bush'),
 '44294.dat':('4211805',5,'gray 7L axle'),
 '60483.dat':('6006140',4,'black 2L axle-hole/round-hole liftarm'),
 '60485.dat':('4535768',2,'gray 9L axle'),
 '62462.dat':('4526985',4,'gray 2L pin-joiner tube'),
 '64179.dat':('4539880',3,'gray 5x7 open frame'),
 '6558.dat':('4514553',30,'blue 3L friction pin'),
 '99455.dat':('6008577',1,'EV3 medium motor')}

def dependencies(parts):
    files=set()
    def visit(name):
        name=name.lower().replace('\\','/')
        if name in files:return
        files.add(name)
        for line in find(name).read_text(encoding='utf-8-sig',errors='replace').splitlines():
            t=line.split()
            if t and t[0]=='1':visit(' '.join(t[14:]))
    for p in parts:visit(p['file'])
    return files

def run():
    parts=build();counts=Counter(p['file'] for p in parts)
    counts.pop('99535c01.dat');counts.pop('99543.dat');counts['99455.dat']=1
    stock_rows=[]
    for file,count in sorted(counts.items()):
        element,stock,name=STOCK[file]
        stock_rows.append(dict(design_file=file,element_id=element,description=name,module_required=count,
                               core_set_total=stock,minimum_extra_for_module=max(0,count-stock)))
    with (ROOT/'stock-ledger.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(stock_rows[0]));w.writeheader();w.writerows(stock_rows)
    files=dependencies(parts)
    for state in ['low','raised']:
        main=(ROOT/f'lift-{state}.ldr').read_text()
        text=[f'0 FILE lift-{state}.ldr',main,'0 NOFILE']
        for name in sorted(files):
            text.extend(['0 FILE '+name,find(name).read_text(encoding='utf-8-sig',errors='replace'),'0 NOFILE'])
        (ROOT/f'lift-{state}-self-contained.mpd').write_text('\n'.join(text)+'\n',encoding='utf-8')
    v=json.loads((ROOT/'verification.json').read_text());c=json.loads((ROOT/'clearance-results.json').read_text())
    passed=sum(r['status']=='PASS' for r in v['checks']);failed=len(v['checks'])-passed
    vv=np.concatenate([mesh(p)[0].reshape(-1,3) for p in parts]);dims=vv.max(0)-vv.min(0)
    rise=48*(math.sin(HIGH)-math.sin(LOW));fork=next(p for p in parts if p['id']=='FORK-L');fm,_=mesh(fork)
    underside=fm[:,:,2].min();top=fm[:,:,2].max();width=fm[:,:,1].max()-fm[:,:,1].min()
    extras=[r for r in stock_rows if r['minimum_extra_for_module']]
    review=[
      '# EV3 lift: digital model review P2-R1','',
      '**Scope: a real-part lift subassembly with motor bracket. The whole forklift and phase 2 are not complete.**','',
      'This advances the mechanism from idealized beam lines to placed LDraw part geometry. It does not certify that a complete forklift can be built from a single core set. Chassis integration and sensing hardware remain open. No physical build has been observed.','',
      '## Open the result','',
      '- Open `EV3-Lift-Viewer.html` in a browser. It works offline; drag to orbit, scroll to zoom, move the lift-position slider or separate the layers.',
      '- Open either self-contained `.mpd` file in a compatible LDraw CAD application. Its referenced geometry is embedded, including the original part attribution headers.',
      '- The PNG views are in `renders/`. `assembly-low.json` and `assembly-raised.json` record every part placement in mm.',
      '- `stock-ledger.csv` counts physical pieces and maps design files to official element IDs. `lift-parts.csv` lists digital references; its motor body and rotor together represent ONE medium motor.','',
      '## What was modeled','',
      f'{len(parts)} digital instances represent {sum(counts.values())} physical pieces, counting the medium motor as one supplied assembly. There are {len(counts)} physical stock types. All displayed structural parts use actual LDraw surface geometry; no beam or gear is stretched to force a connection.','',
      'Two 5x7 frames support the three gearbox shafts. A compound 8T/24T spur train drives a shared lower-link axle. Four 7L links connect to two 9L carriage beams. Two white 3x5 right-angle beams attach the forks at two pin positions each. Cross ties brace both fixed frames and the moving carriage. A 9L spine connects the medium motor to a fixed frame, with the input shaft providing a second separated bearing axis.','',
      '## Changes since phase 1','',
      '1. **Gearbox corrected:** the actual 5x7 frame has no transverse bearing hole at the proposed X=-24 position. Two 8T/24T pairs use existing holes at X=-32, -16 and 0 mm and retain 9:1 reduction.',
      '2. **Carriage length corrected:** 9L vertical beams replace the 5L candidates. Their lower pivot is H5 and upper pivot H9. The carriage extends 32 mm below the lower pivot so the forks can approach the floor.',
      '3. **Fork mounting specified:** a 3x5 right-angle beam on each outer side attaches to carriage H1/H3, and to fork H1/H3. The fork starts 16 mm forward of the carriage centerline.',
      '4. **Motor bracket specified:** the vertical 9L spine is centered at X=-32, Y=-32, Z=48 mm. Its H4/H6 receive the two motor-face pins; H5 carries the input axle. H9 connects to the frame through a 2L liftarm used as a spacer and a 3L pin. The long pin spans exactly Y=-36 to -12 mm.',
      '5. **Through-spacers corrected:** hollow pin-joiner tubes are used on cross shafts. A stopped axle joiner is unsuitable for an uninterrupted shaft.',
      '6. **Axle and gear clocking specified:** the output follows the links, the intermediate shaft follows the 3:1 relation and the input follows 9:1. Each shaft, its gears and keyed collars rotate together; gears are not independently turned inside fixed cross axles.',
      '7. **Low angle adjusted:** -9.594 degrees, with the fixed lower pivot at Z=48 mm, places the fork center at Z=8 mm on an 8 mm grid. Upper angle remains +25 degrees.','',
      '## Refined dimensions','',
      '| Quantity | Digital value |','|---|---|',
      f'| Lowered module bounding box, including motor and axle ends | {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm (X/Y/Z) |',
      '| Fork center spacing | 32 mm |',
      f'| Actual fork profile width / thickness | {width:.1f} / 7.2 mm |',
      f'| Lowered fork underside / top | {underside:.1f} / {top:.1f} mm above the design floor |',
      f'| Carriage lift travel | {rise:.2f} mm |',
      f'| Pallet-floor clearance, with deck underside at 16 mm | {rise-(16-top):.2f} mm, ideal rigid pickup |',
      f'| Medium-motor rotation for full stroke | {9*math.degrees(HIGH-LOW):.2f} degrees, before backlash/calibration |',
      '| Clear forward fork portion beyond the bracket | About 48 mm; use 40 mm insertion for the first approach trial |','',
      'The module bounding box is not the whole robot footprint. A 40 mm insertion reaches beyond the 32 mm depth-center of a 64 mm pallet, assuming the load is centered and the station is correctly aligned. Lift strength and stability are still unmeasured.','',
      '## Verification performed','',
      f'- **{passed}/{len(v["checks"])} geometry checks pass; {failed} fail.** Includes proper rigid transforms, primitive-derived bearing and pin axes, fork brackets at three poses, actual pin stack length and a floor sweep through 71 poses.',
    ]
    for r in c['checks']:review.append(f'- **{r["status"]}: {r["check"]}.** {r["evidence"]}')
    browser_path=ROOT/'browser-checks.json'
    if browser_path.exists():
        browser=json.loads(browser_path.read_text(encoding='utf-8-sig'))
        actual_hash=hashlib.sha256((ROOT/'EV3-Lift-Viewer.html').read_bytes()).hexdigest()
        if isinstance(browser,dict) and browser.get('viewerSha256','').lower()==actual_hash:
            assert all(t['status']=='PASS' for t in browser['checks'])
            review.append('- **Browser smoke checks pass for this exact viewer file:** lowered, raised and gearbox-only views render in headless Chrome with WebGL error code 0. The viewer hash and observations are in `browser-checks.json`.')
    review += ['',
      'These checks are targeted engineering checks. Bounding boxes reject separated parts; the link/bracket cases use conservative profile envelopes. The gear test samples actual center-plane sections; it does not check every tooth surface in 3D. Pins, axle keys, friction-fit deformations and internal motor contacts are not covered by the structural sweep. A matching hole axis alone is not proof of an accessible insertion path or correct pin retention.','',
      '## Stock shortfalls','',
      'Compared with the official inventory, the standalone lift already needs these extras:','',
      '| Element ID | Item | Lift needs | Core set has | Minimum extra |','|---|---|---|---|---|']
    for r in extras:review.append(f'| {r["element_id"]} | {r["description"]} | {r["module_required"]} | {r["core_set_total"]} | {r["minimum_extra_for_module"]} |')
    review += ['',
      'These are lower bounds. The driving base also consumes parts from the same kit; its requirements must be added before deciding what the complete robot needs. In particular, using the kit\'s axle supply for the lift can leave too few for the chassis. No extras have been purchased. A later simplification can reduce spacer demand if keeping strictly to one kit becomes a requirement.','',
      '## Remaining work before instruction-book release','',
      '| Interface | Status |','|---|---|',
      '| Lift-to-chassis attachment | Open: exact bracket, hole mapping and full assembly clearance |',
      '| Motor bracket | Digitally specified; physical rigidity and pin insertion/retention need checking |',
      '| Fixed frame cross-bracing | Digitally specified; physical play needs checking |',
      '| Fork brackets and moving cross-bracing | Digitally specified; insertion and loaded stiffness need checking |',
      '| Lower-limit switch and independent hard stops | Open |',
      '| Color sensor and camera mounting | Open; camera model/interface unknown |',
      '| Combined chassis/lift/sensor parts allocation | Open |',
      '| Full collision, assembly-path and balance validation | Open |','',
      'The immediate next engineering work is to integrate this module with the chosen chassis. The final instruction booklet should be generated only from a completed assembly sequence, with the unresolved items closed or explicitly scoped out.','',
      '## Reproduce the checks','',
      'Python dependencies: numpy and matplotlib. From this directory run:','',
      '```text','python build_lift.py','python check_clearances.py','python render_model.py','python package_model.py','```','',
      'The HTML viewer itself needs no Python or network access. Source-part geometry is stored under `library/subset/`.','',
      '## Sources','',
      '- Geometry: https://library.ldraw.org/ . The project downloaded individual official part ZIPs including their subparts/primitives. `ATTRIBUTION.md` records all used contributors and licenses.',
      '- Core-set stock: LEGO official Element Survey 45544, saved at `../sources/inventory.pdf`: https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltd9e811d9ff83b385/5f8801d5887a311d8fa19812/45544_element_survey.pdf?locale=en-gb .',
      '- The stock Driving Base remains an external reference (`../sources/driving-base.pdf`); it is not included in this module CAD file.','']
    (ROOT/'Phase-2-Review.md').write_text('\n'.join(review),encoding='utf-8')
    manifest=[]
    for state in ['low','raised']:
        f=ROOT/f'lift-{state}-self-contained.mpd'
        manifest.append(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    f=ROOT/'EV3-Lift-Viewer.html'
    manifest.append(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    (ROOT/'model-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    destination=ROOT.parent/'EV3-Digital-Lift-P2-R1.zip'
    deliverables=['EV3-Lift-Viewer.html','lift-low-self-contained.mpd','lift-raised-self-contained.mpd','lift-low.ldr','lift-raised.ldr',
       'stock-ledger.csv','lift-parts.csv','Phase-2-Review.md','ATTRIBUTION.md','model-manifest.json','verification.json','clearance-results.json',
       'assembly-low.json','assembly-raised.json','ldraw_geometry.py','build_lift.py','check_clearances.py','render_model.py','package_model.py','viewer-template.html','verify_viewer.ps1']
    if (ROOT/'browser-checks.json').exists():deliverables.append('browser-checks.json')
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for name in deliverables:z.write(ROOT/name,name)
        for f in (ROOT/'renders').glob('*.png'):z.write(f,'renders/'+f.name)
        for name in files:
            f=find(name);z.write(f,str(f.relative_to(ROOT)).replace('\\','/'))
    print('Physical pieces:',sum(counts.values()),'minimum extra stock types:',len(extras))
    print('Review:',ROOT/'Phase-2-Review.md')
    print('Package:',destination,destination.stat().st_size,'bytes')

if __name__=='__main__':run()
