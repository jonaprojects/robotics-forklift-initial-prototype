"""Catalog-part rear frame, motor stand-offs, brick rails and caster.

All dimensions are mm. Connection centers are recorded, not inferred from a
merged visual mesh. Motor engagement, stiffness and full interference remain
verification tasks; this file does not certify a build.
"""
import numpy as np
from ldraw_geometry import part
from build_lift import RAXLE,RSHAFT,RBEAM

def build_chassis():
    parts=[];joints=[]
    def add(name,file,color,pos,rot=np.eye(3)):
        p=part(name,file,color,pos,rot,'07 Custom chassis');parts.append(p);return p
    def joint(name,a,b,point,kind='round pin axis'):
        joints.append(dict(id=name,a=a,b=b,point=point,axis=[0,1,0],kind=kind))
    for side,s in [('L',1),('R',-1)]:
        pinrot=RAXLE if s>0 else RAXLE@np.diag([-1,-1,1])
        add('CHASSIS-LOWER-'+side,'32278',15,[-40,60*s,28],RBEAM)
        add('BRICK-RAIL-'+side,'32278',15,[-48,56*s,116],RBEAM)
        for x in [-8,8]:
            suffix=f'{side}-{x}'
            add('MOTOR-INNER-PIN-'+suffix,'2780',0,[x,40*s,28],pinrot)
            add('MOTOR-STANDOFF-'+suffix,'62462',71,[x,48*s,28],RAXLE)
            add('MOTOR-OUTER-PIN-'+suffix,'2780',0,[x,56*s,28],pinrot)
            joint('motor-rail-'+suffix,'DRIVE-MOTOR-'+side,'CHASSIS-LOWER-'+side,[x,0,28],
                  'coaxial stand-off: inner pin -> 2L pin-joiner -> outer pin')
        for x in [-88,-32]:
            suffix=f'{side}-{x}'
            add('CHASSIS-TOWER-'+suffix,'32278',15,[x,68*s,84])
            rb=np.array([[0,0,-1],[0,1,0],[1,0,0]])
            add('LOWER-CORNER-'+suffix,'32526',15 if x==-88 else 71,[x+32,76*s,28],rb)
            add('CORNER-SPACER-'+suffix,'60483',0,[x+16,68*s,20])
            # Rear two corner joints are occupied by the caster cross shafts.
            if x!=-88:
                for xx in [x,x+16]:add(f'CORNER-LONG-PIN-{suffix}-{xx}','6558',1,[xx,68*s,28],pinrot)
            add('CORNER-UPPER-PIN-'+suffix,'2780',0,[x,72*s,44],pinrot)
            joint('corner-post-'+suffix,'LOWER-CORNER-'+suffix,'CHASSIS-TOWER-'+suffix,[x,0,44])
            joint('corner-rail-'+suffix,'LOWER-CORNER-'+suffix,'CHASSIS-LOWER-'+side,[x+16,0,28])
            # 8+4+8+4 = 24 mm stack; long pin's collar falls after first 8 mm.
            add('TOP-INNER-HALFBEAM-'+suffix,'32017',0,[x,62*s,100])
            add('TOP-OUTER-HALFBEAM-'+suffix,'32017',0,[x,74*s,100])
            add('TOP-TOWER-PIN-'+suffix,'6558',1,[x,64*s,116],pinrot)
            joint('tower-brickrail-'+suffix,'CHASSIS-TOWER-'+suffix,'BRICK-RAIL-'+side,[x,0,116],
                  '3L pin through 8/4/8/4 mm stack')
        # Brick side face is at Y=36. Two 2L pins and a 2L tube bridge to rail.
        for x in [-80,-16]:
            suffix=f'{side}-{x}'
            add('BRICK-INNER-PIN-'+suffix,'2780',0,[x,36*s,116],pinrot)
            add('BRICK-STANDOFF-'+suffix,'62462',71,[x,44*s,116],RAXLE)
            add('BRICK-OUTER-PIN-'+suffix,'2780',0,[x,52*s,116],pinrot)
            joint('brick-rail-'+suffix,'EV3-BRICK','BRICK-RAIL-'+side,[x,0,116],
                  'coaxial stand-off: inner pin -> 2L pin-joiner -> outer pin')
    # Two cross shafts also use the socket's actual mounting holes 16 mm apart.
    for x in [-88,-72]:
        add(f'CASTER-CENTER-AXLE-{x}','3707',0,[x,0,28],RAXLE)
        for side,s in [('L',1),('R',-1)]:
            suffix=f'{x}-{side}'
            add('CASTER-OUTER-AXLE-'+suffix,'44294',71,[x,60*s,28],RAXLE)
            add('CASTER-SHAFT-COUPLER-'+suffix,'59443',4,[x,32*s,28],RSHAFT)
            for y in [12,48]:add(f'CASTER-TUBE-{suffix}-{y}','62462',71,[x,y*s,28],RAXLE)
            for y in [22,82]:add(f'CASTER-RETAINER-{suffix}-{y}','4265c',14,[x,y*s,28],RSHAFT)
            joint('caster-crossshaft-'+suffix,'CASTER-SOCKET','CHASSIS-LOWER-'+side,[x,0,28],
                  '8L center axle + stopped joiner + 7L outer axle; through braced rail stack')
    motor_rot=np.array([[0,0,1],[-1,0,0],[0,-1,0]])
    add('EV3-BRICK','95646',15,[-48,0,116],motor_rot)
    add('CASTER-SOCKET','92911',72,[-80,0,12])
    add('CASTER-BALL','99948',71,[-80,0,12])
    return parts,joints
