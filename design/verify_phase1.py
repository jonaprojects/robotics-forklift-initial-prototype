"""Engineering checks for the proposed forklift. No CAD/physical-fit claims.

Run from any directory: python path/to/design/verify_phase1.py
Writes a factual report and exits 2 while exact-assembly release is blocked.
"""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / 'phase1-model.json').read_text(encoding='utf-8'))
l, p = d['lift'], d['pallet']
results = []

def record(name, ok, evidence):
    results.append({'check': name, 'status': 'PASS' if ok else 'FAIL', 'evidence': evidence})

lo, hi = map(math.radians, [l['angle_low_degrees'], l['angle_high_degrees']])
length = l['link_length']
low_x, high_x = length*math.cos(lo), length*math.cos(hi)
rise = length*(math.sin(hi)-math.sin(lo))
record('Lift target', 25 <= rise <= 30, f'{rise:.3f} mm rise')
record('Endpoint fore-aft shift', abs(high_x-low_x) < 5,
       f'{high_x-low_x:.3f} mm; not the full swept excursion')

# Include the interior extremum at zero degrees, not just the endpoints.
angles = [lo + (hi-lo)*i/350 for i in range(351)]
xs = [length*math.cos(a) for a in angles]
record('Full fore-aft excursion', max(xs)-min(xs) < 5,
       f'{max(xs)-min(xs):.3f} mm; carriage initially moves forward, then rearward')
residual = 0
for a in angles:
    lower = (length*math.cos(a),length*math.sin(a))
    upper = (lower[0], lower[1]+l['carriage_pivot_separation'])
    residual = max(residual,abs(math.dist(l['fixed_lower'], lower)-length),
                   abs(math.dist(l['fixed_upper'], upper)-length),
                   abs(math.dist(lower, upper)-l['carriage_pivot_separation']))
record('Ideal parallelogram closure', residual < 1e-9, f'maximum residual {residual:.3g} mm over 351 positions')

ratio = math.prod(b/a for a,b in l['gear_teeth'])
record('Gear reduction', ratio == 9, f'{ratio:g}:1; motor travel {(l["angle_high_degrees"]-l["angle_low_degrees"])*ratio:g} degrees')
for i,(small,large) in enumerate(l['gear_teeth']):
    expected = l['gear_module_assumption']*(small+large)/2
    actual = l['gear_axle_x'][i+1]-l['gear_axle_x'][i]
    record(f'Gear stage {i+1} nominal pitch spacing', actual==expected,
           f'{actual:g} mm shaft spacing vs {expected:g} mm pitch requirement; tooth solids/hubs not checked')

record('Fork and pallet channel alignment', l['fork_centers_y']==p['channel_centers_y'], str(l['fork_centers_y']))
side_clearance = (p['channel_width']-l['fork_width'])/2
top_clearance = p['deck_underside_height']-l['fork_bottom_at_low']-l['fork_thickness']
record('Nominal insertion clearances', side_clearance>=4 and top_clearance>=4,
       f'{side_clearance:g} mm per side; {top_clearance:g} mm above fork; {l["fork_bottom_at_low"]:g} mm below fork')
deck_raised = p['deck_underside_height']+p['deck_thickness']+rise-top_clearance
record('Pallet floor clearance after pickup', rise-top_clearance>20,
       f'{rise-top_clearance:.3f} mm; initial empty fork-to-deck gap consumes {top_clearance:g} mm of stroke')
record('Insertion behind pallet center', l['usable_insertion']>p['depth']/2,
       f'{l["usable_insertion"]:g} mm insertion vs {p["depth"]/2:g} mm center depth; assumes centered load')

used_width = 2*max(abs(v) for v in l['outer_bush_y'])+l['assumed_beam_and_bush_width']
record('Nominal output axle stack length', used_width<=l['output_axle_length'],
       f'{used_width:g} mm outer-to-outer nominal stack in {l["output_axle_length"]:g} mm axle; real hubs/spacers not checked')

required = l['moving_mass_assumption_kg']*9.81*length/1000
available = l['motor_running_torque_Nm']*ratio*l['assumed_transmission_efficiency']
record('Illustrative gravity torque budget', available>required,
       f'{required:.4f} Nm ideal peak requirement vs {available:.4f} Nm modeled output; mass/efficiency assumptions only, no capacity certification')

bad = [r['element'] for r in d['candidate_lift_stock'] if r['quantity']>r['available']]
record('Listed lift subset vs official stock', not bad,
       f'{len(d["candidate_lift_stock"])} listed element types checked; excludes chassis use and unresolved hardware')

report = [
    '# Phase 1 verification report - P1-R1', '',
    '**Release status: HOLD. Phase 1 is not fully complete.**', '',
    'Analytical checks below apply to an idealized candidate. They do not verify an assembled LEGO model.', '',
    '| Check | Result | Evidence |', '|---|---|---|'
]
for r in results:
    report.append(f'| {r["check"]} | {r["status"]} | {r["evidence"]} |')
report += ['', '## Completion blockers', '',
           'The exact connection list is incomplete. The following are requirements to resolve, not hidden assumptions:', '']
for u in d['unresolved_connections']:
    report.append(f'- **{u["id"]}: {u["interface"]}.** {u["required"]}.')
report += ['', '## What has not been verified', '',
           '- Full base-plus-lift inventory consumption and connector quantities.',
           '- Real part solids, gear hubs, collision sweeps, clutch/holding behavior or illegal connections.',
           '- Motor housing orientation, sensor/camera mounts and cable access.',
           '- Robot center of mass, tipping margin, drive traction and lifting capacity.',
           '- Physical operation. No assembled prototype has been observed.', '',
           'The earlier V0.1 proposal and concept drawing are superseded where this review identifies gaps. Do not use either as pin-by-pin instructions.', '',
           '## Reference integrity', '']
for pdf in sorted((ROOT/'sources').glob('*.pdf')):
    report.append(f'- {pdf.name}: SHA-256 `{hashlib.sha256(pdf.read_bytes()).hexdigest()}`')
(ROOT/'Phase-1-Verification.md').write_text('\n'.join(report)+'\n', encoding='utf-8')
(ROOT/'checks'/'verification-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
for r in results:
    print(f'{r["status"]}: {r["check"]}: {r["evidence"]}')
print(f'RELEASE HOLD: {len(d["unresolved_connections"])} unresolved interfaces. Report: {ROOT / "Phase-1-Verification.md"}')
raise SystemExit(2 if d['unresolved_connections'] or any(r['status']=='FAIL' for r in results) else 0)
