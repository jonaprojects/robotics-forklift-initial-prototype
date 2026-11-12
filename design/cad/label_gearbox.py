"""Label the third render directly from the existing CAD part positions."""
from pathlib import Path
import json
import numpy as np
from build_lift import build
from ldraw_geometry import mesh
from render_model import picture

ROOT=Path(__file__).resolve().parent
parts=build()
by_id={p['id']:p for p in parts}

def on_surface(part_id,desired):
    triangles,_=mesh(by_id[part_id])
    vertices=triangles.reshape(-1,3)
    return vertices[np.argmin(np.linalg.norm(vertices-np.array(desired),axis=1))].tolist()

notes=[
    dict(text='1  SUPPORT FRAMES\nTwo Technic 5 x 7 frames\nHold the shafts in alignment',point=on_surface('FRAME-R',[-24,-20,80]),label=(.045,.76)),
    dict(text='2  INPUT SHAFT\n9L axle - connects to motor\nTurns the first small gear',point=on_surface('INPUT-AXLE',[-32,-43,48]),label=(.045,.58)),
    dict(text='3  INTERMEDIATE SHAFT\n7L axle - carries a 24T gear\nand an 8T gear together',point=on_surface('INTERMEDIATE-AXLE',[-16,-27,48]),label=(.045,.40)),
    dict(text='4  GRAY FULL BUSHES\n8 shown - axle collars / spacers\nLimit sideways movement',point=on_surface('OUTPUT-COLLAR-0',[0,-40,51]),label=(.045,.22)),
    dict(text='5  OUTPUT SHAFT\n12L axle - drives the lift links\nTurns slower with more torque',point=on_surface('OUTPUT-AXLE',[0,46,48]),label=(.76,.76)),
    dict(text='6  SMALL GEARS - 8 TEETH\n2 gears: input and middle shaft\nOne is partly hidden in this view',point=on_surface('GEAR-8-A',[-32,-7.8,53]),label=(.76,.58)),
    dict(text='7  LARGE GEARS - 24 TEETH\n2 gears: middle and output shaft\nEach pair gives 3:1 reduction',point=on_surface('GEAR-24-B',[9,.15,55]),label=(.76,.40)),
    dict(text='8  YELLOW HALF BUSHES\n6 shown - thin axle spacers\nSome sit behind the front frame',point=on_surface('INPUT-INNER-HALF--10',[-32,-10,51]),label=(.76,.22)),
]
picture(parts,ROOT/'renders'/'gearbox-labeled.png',
    'EV3 gearbox: what each part does',
    'Same third-render view | 8T = 8 teeth | 24T = 24 teeth | Overall reduction: 3 x 3 = 9:1',
    elev=28,azim=-60,gearbox=True,annotations=notes)
(ROOT/'gearbox-labels.json').write_text(json.dumps(notes,indent=2)+'\n')
print(ROOT/'renders'/'gearbox-labeled.png')
