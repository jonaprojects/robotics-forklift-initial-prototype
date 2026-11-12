"""Annotate the complete existing lift CAD assembly, using its real surfaces."""
from pathlib import Path
import json,math
import numpy as np
from build_lift import build,HIGH
from ldraw_geometry import mesh
from render_model import picture

ROOT=Path(__file__).resolve().parent
parts=build(HIGH)
by_id={p['id']:p for p in parts}
x,z=48*math.cos(HIGH),48+48*math.sin(HIGH)

def surface(part_id,desired):
    triangles,_=mesh(by_id[part_id])
    v=triangles.reshape(-1,3)
    return v[np.argmin(np.linalg.norm(v-np.array(desired),axis=1))].tolist()

notes=[
 dict(text='1  FIXED SUPPORT FRAMES\nTwo 5 x 7 frames + cross ties\nKeep the gearbox rigid',point=surface('FRAME-R',[-24,-20,80]),label=(.035,.77)),
 dict(text='2  MOTOR BRACKET\n9L spine, pins and spacer\nHolds the motor on the frame',point=surface('MOTOR-BRACKET-SPINE',[-32,-36,64]),label=(.035,.59)),
 dict(text='3  EV3 MEDIUM MOTOR\nPowers the fork-lifting motion\nOne motor for the complete lift',point=surface('LIFT-MOTOR-BODY',[-38,-85,55]),label=(.035,.41)),
 dict(text='4  REDUCTION GEARBOX\nTwo 8T-to-24T stages = 9:1\nSlower motion, greater torque',point=surface('GEAR-24-A',[-16,-7.8,58]),label=(.035,.23)),
 dict(text='5  PARALLEL LIFT ARMS\nFour 7L beams, two per side\nKeep the forks level as they rise',point=surface('UPPER-LINK-R',[24*math.cos(HIGH),-28,80+24*math.sin(HIGH)]),label=(.77,.77)),
 dict(text='6  MOVING CARRIAGE\nTwo upright 9L beams + ties\nCarry the forks up and down',point=surface('CARRIAGE-R',[x,-20,z+16]),label=(.77,.59)),
 dict(text='7  FORK BRACKETS\nWhite 3 x 5 right-angle beams\nJoin each fork to the carriage',point=surface('FORK-BRACKET-R',[x+16,-28,z-32]),label=(.77,.41)),
 dict(text='8  FORKS\nTwo forward-facing 9L beams\nSlide under and lift a pallet',point=surface('FORK-R',[x+72,-20,z-32]),label=(.77,.23)),
 dict(text='9  DRIVE AXLE + COUPLERS\nTurn both lower arms together',point=surface('DRIVE-COUPLER-R',[0,-36,48]),label=(.39,.125)),
]
picture(parts,ROOT/'renders'/'whole-mechanism-labeled.png',
 'EV3 lifting mechanism: annotated overview',
 'Raised position | Forks stay level | Lift module only; chassis and camera are not included',
 elev=24,azim=-55,annotations=notes)
(ROOT/'whole-mechanism-labels.json').write_text(json.dumps(notes,indent=2)+'\n')
print(ROOT/'renders'/'whole-mechanism-labeled.png')
