# analysis/momentum_breakdown.py
import numpy as np
import opensim as osim
import matplotlib.pyplot as plt

MODEL = 'OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim'
CASE  = '0'
MASS_NORM, SPEED, HEIGHT = None, 1.33, 1.80

model = osim.Model(MODEL)
state = model.initSystem()
mass  = model.getTotalMass(state)
bs = model.getBodySet()
bodies = [bs.get(i) for i in range(bs.getSize())]
cs = model.getCoordinateSet()
coords = [cs.get(i) for i in range(cs.getSize())]

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
r = d[CASE]
joints, q, qd, gc = list(r['joints']), r['coordinate_values'], r['coordinate_speeds'], r['GC_percent']
nT = q.shape[1]

def set_state(k):
    for c in coords:
        i = joints.index(c.getName())
        rot = not c.getName().startswith('pelvis_t')
        c.setValue(state, np.deg2rad(q[i,k]) if rot else q[i,k], False)
        c.setSpeedValue(state, np.deg2rad(qd[i,k]) if rot else qd[i,k])
    model.realizeVelocity(state)

names = [b.getName() for b in bodies]
Lspin = np.zeros((len(bodies), nT))
Lorb  = np.zeros((len(bodies), nT))

for k in range(nT):
    set_state(k)
    # set_state(k) 이후에

    com  = model.calcMassCenterPosition(state)
    vcom = model.calcMassCenterVelocity(state)
    for bi, b in enumerate(bodies):
        m = b.getMass()
        if m <= 0: continue
        Lspin_vec = b.calcAngularMomentumAboutMassCenter(state)
        Lspin_g = b.expressVectorInGround(state, Lspin_vec)
        Lspin[bi,k] = Lspin_g.get(1)
        p = b.findStationLocationInGround(state, b.getMassCenter())
        v = b.findStationVelocityInGround(state, b.getMassCenter())
        rx, rz = p.get(0)-com.get(0), p.get(2)-com.get(2)
        vx, vz = v.get(0)-vcom.get(0), v.get(2)-vcom.get(2)
        Lorb[bi,k] = m*(rz*vx - rx*vz)

Ltot = (Lspin + Lorb).sum(axis=0)
print(f"sum of segments : {Ltot.min():+.4f} ~ {Ltot.max():+.4f}")
print(f"reference       : -1.232 ~ +1.232")


print(f"spin only   : {Lspin.sum(axis=0).min():+.4f} ~ {Lspin.sum(axis=0).max():+.4f}")
print(f"orbit only  : {Lorb.sum(axis=0).min():+.4f} ~ {Lorb.sum(axis=0).max():+.4f}")
print(f"spin+orbit  : {Ltot.min():+.4f} ~ {Ltot.max():+.4f}")
print(f"spin-orbit  : {(Lspin-Lorb).sum(axis=0).min():+.4f} ~ {(Lspin-Lorb).sum(axis=0).max():+.4f}")

print([(b.getName(), round(b.getMass(),3)) for b in bodies])
print("sum of body masses:", sum(b.getMass() for b in bodies))
print("model total mass  :", mass)