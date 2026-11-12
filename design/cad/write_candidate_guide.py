"""Generate a readable assembly guide alongside exact offline step geometry."""
import csv,json,html,hashlib,zipfile,re
from collections import Counter
from pathlib import Path
import numpy as np
from build_candidate import scene,OUT
from candidate_steps import STEPS
from build_integrated import PITCH_R,AXLE_ORIGIN
from ldraw_geometry import metadata,mesh

def run():
    pp,m=scene(0);checks=json.loads((OUT/'verification.json').read_text())
    esc=html.escape
    root=OUT.parent.parent
    old=root/'design/saved/EV3-I0.3-preserved.zip'
    saved=dict(version='I0.3',archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),note='Preserved before B0.1 development. Historical design; superseded fit corrections are documented in B0.1.')
    (old.parent/'I0.3-manifest.json').write_text(json.dumps(saved,indent=2))
    rows=[]
    for p in pp:
        if p.get('fixture'):continue
        rawpos=PITCH_R.T@(np.array(p['position'])-AXLE_ORIGIN)+AXLE_ORIGIN
        rawrot=PITCH_R.T@np.array(p['rotation'])
        rows.append(dict(step=p['build_step'],id=p['id'],design_file=p['file'],color=p['color'],external=bool(p.get('external')),
            x_mm=round(rawpos[0],5),y_mm=round(rawpos[1],5),z_mm=round(rawpos[2],5),
            **{f'R{i+1}{j+1}':round(rawrot[i,j],7) for i in range(3) for j in range(3)}))
    with (OUT/'placements.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(sorted(rows,key=lambda x:x['step']))
    lego=list(csv.DictReader((OUT/'parts.csv').open()));total=sum(int(r['Physical quantity']) for r in lego)
    robot=[p for p in pp if not p.get('fixture')];v=np.concatenate([mesh(p)[0].reshape(-1,3) for p in robot]);dims=v.max(0)-v.min(0)
    intro=f'''# EV3 forklift B0.1: first physical build candidate

Saved predecessor: `../saved/EV3-I0.3-preserved.zip` (SHA-256 recorded in `../saved/I0.3-manifest.json`). B0.1 is separate; do not mix its motor spacing and sensor brackets with I0.3.

This package gives the team a defined mechanical model to attempt in the lab: {total} physical LEGO pieces, complete sensor brackets, independent adjustable mechanical stops and a removable camera holder. It is a first-build candidate, not a physically proven robot or a finished navigation system. The actual extended-kit contents and camera model have not been confirmed.

Open `EV3-Build-Candidate.html` in a browser. Choose an assembly step; new parts appear blue. Use "Only parts added in this step" to inspect a subassembly, and drag to see both sides. For close fitting, use the exact self-contained `build-candidate.mpd` in an LDraw-compatible CAD program. No CAD software or network is needed for the HTML viewer. The animation illustrates pickup/delivery; it does not simulate navigation, contact, friction or loads.

## Specifications

| Item | B0.1 definition |
|---|---|
| Controller | One EV3 brick |
| Motors | Two large drive motors, one medium lift motor; port D spare |
| Steering | Differential drive; two 56 mm tires and rear ball caster |
| Lift | Four 7L parallel links; two 9L forks; 5.4:1 motor reduction |
| Nominal linkage stroke | -18.574 to +25 degrees; about 235.3 motor degrees before calibration |
| Fork entry | Lowest surface about 3.07 mm; highest surface 11.6 mm above floor |
| Pallet | 64 mm forward x 80 mm wide; deck underside 16 mm above floor |
| Ideal final pallet rise | 31.13 mm; illustrative rigid geometry |
| Low-pose overall robot envelope | Approximately {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm, including assumed camera |
| Camera allowance | 40 x 30 x 24 mm, lens toward front; interface and mass unconfirmed |
| Payload rating | Unassigned until measured balance and loaded tests pass |

The four-bar carriage remains parallel to the chassis. The assembled chassis rests about 1.195 degrees nose-up from its construction coordinate frame to put the caster and both tires on the floor. Do not try to force all beam axes level with the floor.

## Read the geometry

All construction dimensions below are millimeters before the stance rotation. X is forward, Y is left, Z is up. Positive and negative Y are mirror images except for the medium motor, touch switch and stop column. One LEGO hole pitch is 8 mm; L is a hole-count/nominal axle-length convention, not a dimension in millimeters. H1..H7 numbers refer to successive beam holes from the end identified in that instruction. Coordinates refer to hole centers or the source LDraw part origin; a sensor or motor origin is not its center of mass.

`placements.csv` contains every part's exact construction origin and 3x3 rotation matrix. It is an engineering supplement to the visual steps. `parts.csv` counts physical parts: split medium-motor and touch-switch meshes each count as one supplied device. Structural colors in the model are identification aids; compare actual part shapes and quantities in the lab. Station blocks, camera envelope, foam, straps and cables are excluded from the LEGO count. The expanded kit is not presumed to contain all extras.

## Extra equipment and wiring

| Equipment | Quantity / requirement |
|---|---|
| Camera | One fitting the assumed envelope; identify its interface before connection |
| Foam pads | Two, 40 x 30 x 2 mm; lower one on brick, upper one on tray |
| Camera straps | Two reusable ties >=200 mm, about 2.5 mm wide |
| Tray straps | Two reusable ties >=350 mm; keep battery release accessible |
| Cable ties | Small reusable ties as needed on stationary rails |
| EV3 leads | Five: 250 mm lift, 350 mm left, 350 mm right, 250 mm color, 500 mm touch proposed; verify actual reach |
| Target | A raised pallet; a solid cube flat on the floor cannot be entered by these forks |

| Port | Connection | Route |
|---|---|---|
| A | Medium lift motor | Along right fixed bridge, never through gears |
| B | Left large drive motor | Up left tower to brick |
| C | Right large drive motor | Up right tower to brick |
| 1 | Downward color sensor | Behind fixed rear frame to brick |
| 2 | Touch reference switch | Up right fixed stand/bridge with a port service loop |
| D, 3, 4 | Spare | Camera use depends on its actual interface |

A generic USB/web camera needs a compatible host/interface; it cannot be assumed to work in an EV3 sensor socket. Choose an EV3-compatible vision device or an external computer link after identifying the camera. A second EV3 brick is not mechanically required. The camera looks forward from the rear tray; check for lift/brick occlusion using the real camera. No visual-navigation software or camera compatibility is certified by this model.

## Assembly order

Build with power off. Assemble both mirrored sides where indicated. Keep the stated shafts partially withdrawable until their inner spacers and mounting beams are in place. Tighten bushes only enough to locate parts without binding moving links. Do not force a pin if alignment is wrong.
'''
    md=[intro]
    sections=[]
    for i,(title,text) in enumerate(STEPS,1):
        md += [f'### {i}. {title}',text,f'[Inspect step {i} in 3D](EV3-Build-Candidate.html?step={i})','']
        ps=[p for p in pp if p.get('build_step')==i];ct=Counter(p['file'] for p in ps if not p.get('external'))
        lis=''.join(f'<tr><td>{esc(k[:-4])}</td><td>{n}</td><td>{esc(metadata(k)["description"])}</td></tr>' for k,n in sorted(ct.items()))
        parts_table=('<details><summary>Parts added in this step (digital device subparts shown separately)</summary><table><tr><th>Design</th><th>Qty</th><th>Description</th></tr>'+lis+'</table><p class="small">'+', '.join(esc(p['id']) for p in ps)+'</p></details>') if ps else ''
        sections.append(f'<section id="step-{i}"><div class="step">{i:02}</div><h2>{esc(title)}</h2><p>{esc(text)}</p><a class="button" href="EV3-Build-Candidate.html?step={i}">Inspect exact 3D step</a>{parts_table}</section>')
    limitations='''## Verification and release gate

The recorded checks are in `verification.json`, browser checks in `browser-checks.json`, and selected whole-structure section samples in `whole-structure-audit.json`. The section audit compares actual LDraw surfaces at three poses on a 0.4 mm grid in three transverse planes per overlapping pair. It omits fasteners, flexible consumables and detailed gear contact. The only recorded overlap flags left in that audit belong to the supplied touch sensor's own body/button; these are not external structural clashes. This is a useful sampled check, not a complete 3D collision proof.

The 71 animation poses contain only 15 distinct linkage angles. Checks cover floor clearance in all 71, source-hole alignment for the mounts, the trigger's two pin axes, motor flange spacing and sampled mechanical-stop contact. The camera and flexible cables require real equipment for fit validation. The stop-contact search uses a 0.05 mm section grid, not a strength calculation.

Before releasing this as a proven build, record these lab results:

1. Count the actual core plus extended inventory against `parts.csv` and list substitutions.
2. Check all pins seat fully and all axles are retained; gently twist the chassis and bridge to identify loose stand-offs.
3. Turn the complete lift by hand with cables installed; it must move freely without touching tires, sensor housing or cable loops.
4. Read the real touch input while lowering by hand. It must trip before the lower mechanical stop and release on ascent; avoid using the motor to force an uncalibrated switch.
5. Confirm the hard stops limit overtravel and the forks remain clear of the floor. Stop assemblies rely on sliding bushes; check that they do not migrate under gentle manual force.
6. Check camera fit, view and connection; secure the cable and confirm the brick controls and battery remain accessible.
7. Raise wheels for the first motor-direction test. Use low lift power, encoder bounds and a timeout; a software stop must precede a mechanical stop in normal use.
8. Measure mass and balance with the actual battery/camera. At maximum reach, require a chosen restoring/overturning moment margin (for example 1.5) before increasing load. This model supplies no measured payload rating.
9. Run repeated empty-pallet cycles and turns, then add load gradually. Record payload, cycle count, binding, tipping, slipping and structural changes. Accept a payload only after these tests.

## Changes from the saved version

- Corrected the large-motor flange spacing by moving each motor 4 mm inward; axle and wheel centers remain as specified.
- Moved the raised 40T/24T stage outboard to clear the fixed cross ties. Replaced unsupported sensor placements with actual pinned brackets and a two-pin lift trigger.
- Moved the upper color cross brace clear of the drive motors.
- Replaced stop boxes with a fixed column, keyed beam assemblies and retained transverse stop axles.
- Added a removable camera tray, pads and explicit reusable straps, using a stated camera envelope.
- Added a step-selectable offline viewer, exact part placements, a combined physical bill and wiring/calibration instructions.

## Provenance and reproduction

Structural surfaces are from the official LDraw library, https://library.ldraw.org/ . Authors and CC BY 2.0/4.0 license headers are preserved inside `build-candidate.mpd`; see also `ATTRIBUTION.md`. Original assembly, fixtures and guides are authored by this project. This is an unofficial design.

From the workspace, regenerate in order: `python design/cad/build_candidate.py`; `python design/cad/audit_structure.py`; `python design/cad/verify_candidate.py`; `python design/cad/write_candidate_guide.py`; then run `design/build_candidate/verify_viewer.ps1`. The first-build package contains the required Python sources and LDraw subset. The viewer and MPD are independently usable offline.
'''
    md.append(limitations)
    (OUT/'BUILD-GUIDE.md').write_text('\n\n'.join(md),encoding='utf-8')
    # A compact dimensioned construction sketch: true X/Z hole-center positions.
    def line(x1,z1,x2,z2,color='#47627c',width=5):return f'<line x1="{x1}" y1="{-z1}" x2="{x2}" y2="{-z2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    svg='<svg viewBox="-130 -165 380 190" role="img" aria-label="Dimensioned side construction layout"><g>'+line(-96,28,16,28)+line(-104,116,8,116)
    for x in [-88,-32]:svg+=line(x,28,x,140)
    for z in [52,84]:svg+=line(96,z,141.5,z-15.3,'#c07929')
    svg+=line(141.5,4.7,141.5,68.7)+line(157.5,4.7,221.5,4.7,'#178caa')+line(48,84,80,84,'#178caa')+line(48,68,48,132,'#178caa')+line(80,68,80,132,'#178caa')+line(-40,20,-40,68,'#c33d36')
    for x,z,label in [(-88,28,'rear post -88'),(-32,140,'front post -32'),(64,28,'drive axle X64 / Z28'),(96,84,'pivots X96 / Z52,84'),(-104,116,'brick rail Z116')]:
        svg+=f'<circle cx="{x}" cy="{-z}" r="2" fill="white" stroke="#183047" stroke-width="1"/><text x="{x}" y="{-z-7}" font-size="5" fill="#183047">{label}</text>'
    svg+='</g><text x="-125" y="18" font-size="6" fill="#526477">Construction X/Z centers in mm. Side layers superposed; assembled stance adds 1.195 degrees pitch.</text></svg>'
    # Keep the guide usable without dependencies or a Markdown renderer.
    table=''.join(f'<tr><td>{esc(r["LEGO design file"][:-4])}</td><td>{r["Physical quantity"]}</td><td>{esc(r["Description"])}</td></tr>' for r in lego)
    def format_blocks(text):
        def inline(s):return re.sub(r'`([^`]+)`',r'<code>\1</code>',esc(s))
        output=[]
        for block in text.strip().split('\n\n'):
            if block.startswith('# '):continue
            if block.startswith('## '):output.append('<h2>'+inline(block[3:])+'</h2>')
            elif block.startswith('|'):
                rr=[line.split('|')[1:-1] for line in block.splitlines()]
                output.append('<table>'+''.join('<tr>'+''.join(('<th>' if i==0 else '<td>')+inline(v.strip())+('</th>' if i==0 else '</td>') for v in row)+'</tr>' for i,row in enumerate(rr) if i!=1)+'</table>')
            elif re.match(r'^\d+\. ',block):
                output.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>' for line in block.splitlines())+'</ol>')
            else:output.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
        return ''.join(output)
    intro_html=format_blocks(intro)
    page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EV3 forklift B0.1 assembly guide</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#edf2f6;color:#183047;font:16px/1.65 system-ui,Arial}}main{{max-width:1050px;margin:auto;background:white;padding:40px}}h1{{font-size:34px;line-height:1.2}}h2{{font-size:24px;line-height:1.3}}h3{{margin-top:30px}}p{{color:#344e64}}a{{color:#126e91}}.button{{display:inline-block;padding:10px 16px;border-radius:5px;background:#e5f3f8;text-decoration:none;margin:8px 0}}section{{border-top:1px solid #c9d8e2;padding:28px 0}}.step{{float:right;color:#b2c6d4;font-size:42px;font-weight:bold}}table{{width:100%;border-collapse:collapse;font-size:13px}}td,th{{border-bottom:1px solid #dbe3ea;text-align:left;padding:8px;vertical-align:top}}th{{background:#eef4f7}}.small{{font-size:12px;overflow-wrap:anywhere}}details{{margin-top:15px}}summary{{cursor:pointer;font-weight:600}}svg{{width:100%;background:#f6f9fc;border:1px solid #d6e1e9}}pre{{white-space:pre-wrap;font:13px/1.6 system-ui}}.badge{{background:#fff0d3;padding:8px 12px;display:inline-block}}@media print{{body{{background:white}}main{{padding:10px}}section{{break-inside:avoid}}details{{display:none}}a{{color:inherit}}}}</style><main><h1>EV3 forklift B0.1</h1><p class="badge">First physical build candidate - bench validation required</p>{intro_html}<a class="button" href="EV3-Build-Candidate.html">Open interactive assembly viewer</a> <a class="button" href="build-candidate.mpd">Download self-contained CAD</a><h2>Construction layout</h2>{svg}<p>All step coordinates use X forward, Y left, Z up before stance rotation. Hole pitch is 8 mm. Dimensions and limits are fully specified in the <a href="BUILD-GUIDE.md">text specification</a>; exact placements are in <a href="placements.csv">placements.csv</a>.</p><h2>Start here</h2><p>Use one EV3 brick, two large motors and one medium motor. Wire A=lift, B=left, C=right, 1=color, 2=touch. Extra standard Technic pieces are required. The orange camera is an assumed 40 x 30 x 24 mm envelope. Add two 40 x 30 x 2 mm foam pads, two 200 mm camera ties and two 350 mm tray ties. Identify the real camera before choosing its electrical connection. The target needs an elevated pallet deck; these forks cannot enter a solid cube lying flat on the floor.</p><p>Build both mirrored sides where stated. New components are blue in the viewer; use the isolate checkbox and rotate the model. Assemble inner spacers and mounting beams before closing axle ends. Every step lists source-part IDs; the BOM below combines the supplied device assemblies.</p>{''.join(sections)}<section><h2>Physical LEGO bill</h2><p>{total} pieces; {len(lego)} design types. Kit availability is unconfirmed. Colors may be substituted with the same part geometry.</p><table><tr><th>Design</th><th>Qty</th><th>Description</th></tr>{table}</table></section><section><h2>Verification and remaining lab work</h2><p>{checks['summary'].get('PASS',0)} recorded geometry checks pass. Read <a href="verification.json">the exact scope and results</a>. No payload or camera compatibility has been established. Full assembly access, switch travel, stiffness, flexible cable sweep and load stability require bench checks.</p>{format_blocks(limitations)}</section></main></html>'''
    (OUT/'BUILD-GUIDE.html').write_text(page,encoding='utf-8')
    print('Wrote guide, exact placements and preservation manifest;',total,'physical LEGO pieces')

if __name__=='__main__':run()
