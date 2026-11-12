import sys,math,copy,numpy as np,json
sys.path.insert(0,'design/cad')
from verify_candidate import raw_scene
from build_lift import ry
from check_clearances import tooth_overlap
samples=[raw_scene(i)[0] for i in range(14,29)];result=[]
for deg in [-4,-3.5,-3,-2.5,-2,-1.5,-1,-.5,0,.5,1]:
 worst=0;total=0
 for pp in samples:
  p=copy.deepcopy(pp['GEAR-8-B']);p['rotation']=(ry(math.radians(deg))@p['rotation']).tolist()
  n,a=tooth_overlap(p,pp['GEAR-24-B'],4,spacing=.05);worst=max(worst,n);total+=n
 result.append([deg,worst,total]);print(result[-1],flush=True)
 if worst==0:break
from pathlib import Path
Path('design/build_candidate/gear-clock-search.json').write_text(json.dumps(result,indent=2))
