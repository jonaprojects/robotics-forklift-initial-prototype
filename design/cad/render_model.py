"""Render engineering views and a self-contained WebGL inspection viewer."""
import base64,json,math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from ldraw_geometry import geometry,mesh,metadata,find
from build_lift import build,LOW,HIGH

ROOT=Path(__file__).resolve().parent
PALETTE={0:'#263140',1:'#1c66ab',4:'#bd342e',7:'#a0a5a9',14:'#e5b83b',15:'#e4e7e8',
         16:'#a0a5a9',71:'#a0a5a9',72:'#62686c',79:'#848993',24:'#252c33',256:'#242424',
         273:'#213b59',320:'#8d352f'}
def rgb(c):
    s=PALETTE.get(int(c),'#a0a5a9').lstrip('#')
    return np.array([int(s[i:i+2],16)/255 for i in [0,2,4]])

def picture(parts,path,title,subtitle,elev=24,azim=-55,explode=0,gearbox=False,annotations=None):
    fig=plt.figure(figsize=(13,9),dpi=150,facecolor='#f4f7fa')
    ax=fig.add_axes([.025,.10,.95,.76],projection='3d',computed_zorder=True)
    ax.set_facecolor('#f4f7fa');ax.set_proj_type('ortho')
    verts=[];colors=[]
    for p in parts:
        if gearbox and not (p['group'].startswith('01') or p['group'].startswith('02')):continue
        v,c=mesh(p)
        if explode:
            v=v.copy();v[:,:,1]+=np.sign(np.mean(v[:,:,1]))*explode
        ns=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0])
        norms=np.linalg.norm(ns,axis=1);ns=ns/np.maximum(norms[:,None],1e-12)
        shade=.57+.43*np.abs(ns@np.array([.3,-.4,.866]))
        color=np.array([rgb(code) for code in c])*shade[:,None]
        verts.extend(v);colors.extend(np.clip(color,0,1))
    vv=np.array(verts)
    pc=Poly3DCollection(vv,facecolors=colors,edgecolors='none',zsort='average')
    ax.add_collection3d(pc)
    lo=vv.reshape(-1,3).min(0);hi=vv.reshape(-1,3).max(0)
    ax.set_xlim(lo[0]-7,hi[0]+7)
    ax.set_ylim(lo[1]-7,hi[1]+7)
    ax.set_zlim(lo[2]-7,hi[2]+7)
    ax.set_box_aspect(hi-lo+14,zoom=1.25);ax.view_init(elev=elev,azim=azim);ax.set_axis_off()
    fig.text(.045,.94,title,fontsize=23,color='#183047',weight='bold')
    fig.text(.045,.895,subtitle,fontsize=11,color='#526477')
    fig.text(.045,.055,'P2-R1 | Actual LDraw part surfaces | Digital prototype; chassis, sensors and camera not included',fontsize=10,color='#526477')
    fig.text(.045,.029,'Parts: LDraw contributors, CC BY 2.0 / 4.0. See ATTRIBUTION.md. No physical build validation.',fontsize=8,color='#526477')
    if annotations:
        from mpl_toolkits.mplot3d import proj3d
        fig.canvas.draw()
        for note in annotations:
            xx,yy,_=proj3d.proj_transform(*note['point'],ax.get_proj())
            ax.annotate(note['text'],xy=(xx,yy),xycoords='data',xytext=note['label'],
                textcoords=fig.transFigure,ha='left',va='center',fontsize=11.2,
                color='#183047',linespacing=1.5,
                bbox=dict(boxstyle='round,pad=.6',facecolor='white',edgecolor='#c5d5e1',linewidth=1),
                arrowprops=dict(arrowstyle='->',color='#167b9a',linewidth=1.5,
                    shrinkA=6,shrinkB=1,connectionstyle='arc3,rad=0'),
                annotation_clip=False,zorder=100)
    fig.savefig(path,dpi=150,facecolor=fig.get_facecolor());plt.close(fig)

def blob(a):return base64.b64encode(np.ascontiguousarray(a,dtype=np.float32).tobytes()).decode()

def viewer():
    low=build();files=sorted(set(p['file'] for p in low))
    geoms={}
    for f in files:
        t,c=geometry(f);t=t*.4
        normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
        cc=np.array([rgb(code) if code!=16 else [-1,-1,-1] for code in c])
        geoms[f]=dict(v=blob(t.reshape(-1,3)),n=blob(np.repeat(normals,3,axis=0)),c=blob(np.repeat(cc,3,axis=0)),count=len(t)*3)
    # Exact forward kinematics on 71 sample poses, with rigid matrices rather
    # than interpolating endpoints. Slider chooses one of these checked poses.
    poses=[]
    for theta in np.linspace(LOW,HIGH,71):
        poses.append([np.r_[np.array(p['rotation']).reshape(-1),p['position']].round(6).tolist() for p in build(float(theta))])
    model=dict(parts=low,geometries=geoms,poses=poses,palette={str(k):rgb(k).tolist() for k in PALETTE},
               low=math.degrees(LOW),high=25)
    template=(ROOT/'viewer-template.html').read_text(encoding='utf-8')
    (ROOT/'EV3-Lift-Viewer.html').write_text(template.replace('__MODEL_DATA__',json.dumps(model,separators=(',',':'))),encoding='utf-8')
    files_used=set()
    def refs(name):
        name=name.lower().replace('\\','/')
        if name in files_used:return
        files_used.add(name)
        for line in find(name).read_text(encoding='utf-8-sig',errors='replace').splitlines():
            t=line.split()
            if t and t[0]=='1':refs(' '.join(t[14:]))
    for f in files:refs(f)
    lines=['# LDraw attribution and provenance','','The source files retain their original author and license headers. Rendered images and the viewer derive from these files.',
           '', 'Library: https://library.ldraw.org/ . Licenses: https://creativecommons.org/licenses/by/4.0/ and https://creativecommons.org/licenses/by/2.0/ .',
           '', 'Original assembly and inspection code: this EV3 project. These are unofficial models and are not endorsed by LEGO or LDraw.', '',
           '## Files used (including subparts and primitives)','', '| File | Author | License |','|---|---|---|']
    for f in sorted(files_used):
        m=metadata(f);lines.append(f'| {f} | {m["author"]} | {m["license"]} |')
    (ROOT/'ATTRIBUTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':
    picture(build(),ROOT/'renders'/'lift-lowered.png','EV3 forklift: digital lift module','Lowered position | Forks remain level | 9:1 geared medium motor')
    picture(build(HIGH),ROOT/'renders'/'lift-raised.png','EV3 forklift: raised position','About 28.3 mm carriage travel | About 24 mm pallet clearance after taking up the entry gap')
    picture(build(),ROOT/'renders'/'gearbox-inspection.png','Revised gearbox: real part geometry','8T -> 24T, then 8T -> 24T | Shafts use existing transverse frame holes',elev=28,azim=-60,gearbox=True)
    viewer()
    print('Rendered 3 views and generated the offline WebGL viewer.')
