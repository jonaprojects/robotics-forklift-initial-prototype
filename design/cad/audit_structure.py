import sys,json,numpy as np
from itertools import combinations
sys.path.insert(0,'design/cad')
from build_candidate import scene,OUT
from build_integrated import PITCH_R,AXLE_ORIGIN
from ldraw_geometry import mesh
from check_clearances import section,inside
chosen={'64179.dat','32316.dat','32523.dat','32525.dat','32526.dat','60483.dat','6536.dat','95648.dat','99385c01.dat','99386.dat','95650.dat','32278.dat','32524.dat','40490.dat','95646.dat','99535c01.dat','95658.dat','62462.dat','92911.dat','99948.dat','56908.dat','41897.dat','3647.dat','3648.dat','3649.dat'}
issues=[]
for pose in [0,20,28]:
 pp,m=scene(pose);dx=m['robot_x'];pivot=AXLE_ORIGIN+[dx,0,0];cache={}
 for p in pp:
  if p.get('fixture') or p.get('external') or p['file'] not in chosen:continue
  p['position']=(PITCH_R.T@(np.array(p['position'])-pivot)+AXLE_ORIGIN).tolist();p['rotation']=(PITCH_R.T@np.array(p['rotation'])).tolist()
  t,c=mesh(p);cache[p['id']]=(t,t.reshape(-1,3).min(0),t.reshape(-1,3).max(0),p)
 for (name,(a,al,ah,p)),(other,(b,bl,bh,q)) in combinations(cache.items(),2):
  # Audit every selected structure pair, including inherited chassis.
  lo=np.maximum(al,bl);hi=np.minimum(ah,bh)
  if not np.all(hi-lo>.18):continue
  maxarea=0;besty=0
  for y in np.linspace(lo[1]+.1,hi[1]-.1,3):
   sa=section(a,y);sb=section(b,y)
   if not len(sa) or not len(sb):continue
   xs=np.arange(lo[0]+.2,hi[0],.4);zs=np.arange(lo[2]+.2,hi[2],.4)
   pts=np.stack(np.meshgrid(xs,zs),axis=-1).reshape(-1,2)
   area=(inside(pts,sa)&inside(pts,sb)).sum()*.16
   if area>maxarea:maxarea=area;besty=y
  if maxarea>.32:issues.append(dict(pose=pose,a=name,b=other,area=round(maxarea,2),y=round(besty,2)))
(OUT/'whole-structure-audit.json').write_text(json.dumps(issues,indent=2))
for x in issues:print(x)
print('FLAGS',len(issues))
