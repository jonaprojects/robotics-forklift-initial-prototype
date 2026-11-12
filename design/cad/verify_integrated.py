"""Targeted forward-layout checks; explicitly not full mechanical validation."""
import json,sys,numpy as np
from build_integrated import assembly,OUT,body_point
from ldraw_geometry import mesh,axis_present
from check_clearances import tooth_overlap

def run():
    checks=[];pp={p['id']:p for p in assembly(0)[0]}
    for side,sgn in [('L',1),('R',-1)]:
        checks.append(dict(check='Raised input frame bore '+side,status='PASS' if axis_present(pp['FRAME-'+side],body_point([64,16*sgn,84]),[0,1,0]) else 'FAIL'))
    gap=float(mesh(pp['LIFT-MOTOR-BODY'])[0][:,:,2].min()-mesh(pp['TIRE-R'])[0][:,:,2].max())
    checks.append(dict(check='Lift motor / tire vertical clearance',status='PASS' if gap>10 else 'FAIL',gap_mm=gap))
    gear=[]
    for i in range(14,29):
        p={p['id']:p for p in assembly(i)[0]}
        count,area=tooth_overlap(p['RAISED-INPUT-40T'],p['INPUT-INNER-BUSH'],4)
        gear.append(dict(pose=i,overlap_samples=count,area_mm2=area))
    checks.append(dict(check='New 40T/24T stage center-plane sections',status='PASS' if all(x['overlap_samples']==0 for x in gear) else 'REVIEW',samples=gear))
    floors=[]
    for i in [0,14,28,49,63,70]:
        for p in assembly(i)[0]:
            z=float(mesh(p)[0][:,:,2].min())
            if z<-.05:floors.append(dict(pose=i,part=p['id'],z=z))
    checks.append(dict(check='Six-pose floor intrusion audit',status='PASS' if not floors else 'FAIL',intrusions=floors))
    load_x=[]
    for i in range(14,64):
        parts,m=assembly(i)
        load=next(p for p in parts if p['id']=='LOAD-CUBE')
        load_x.append(load['position'][0]-m['robot_x'])
    cg=max(load_x)
    # Sensitivity case only. Correct chassis CG for two 80g motors moved 64mm.
    chassis_cg=-50+.16*64/.85
    rear=.85*(64-chassis_cg)/1000
    front=(.18*(76-64)+.08*(161-64)+.10*(cg-64))/1000
    balance=dict(status='HISTORICAL ASSUMPTION CASE ONLY - not valid mass data for custom chassis I0.3',drive_axle_x_mm=64,chassis_mass_kg=.85,chassis_cg_x_mm=chassis_cg,
        fixed_lift_mass_kg=.18,fixed_lift_cg_x_mm=76,moving_lift_mass_kg=.08,moving_lift_cg_x_mm=161,
        pallet_load_mass_kg=.10,pallet_load_cg_x_mm=cg,restoring_kg_m=rear,overturning_kg_m=front,moment_ratio=rear/front,target_ratio=1.5,measured=False)
    result=dict(checks=checks,balance=balance,overall='HOLD - mounting, complete stock and full-body verification remain open')
    (OUT/'forward-layout-checks.json').write_text(json.dumps(result,indent=2))
    for c in checks:print(c['status'],c['check'],c.get('gap_mm',''))
    print('Illustrative static moment ratio:',rear/front,'(not measured)')
    if any(c['status']!='PASS' for c in checks):sys.exit(2)

if __name__=='__main__':run()
