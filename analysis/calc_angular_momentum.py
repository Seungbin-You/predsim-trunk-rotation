# analysis/calc_angular_momentum.py
import numpy as np
import opensim as osim
import matplotlib.pyplot as plt

MODEL = 'OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim'
CASE  = '0'
SPEED = 1.33      # m/s
HEIGHT = 1.80     # m — 실제 모델 신장으로 교체하십시오

model = osim.Model(MODEL)
state = model.initSystem()
mass  = model.getTotalMass(state)
smss  = model.getMatterSubsystem()

cs = model.getCoordinateSet()
coords = [cs.get(i) for i in range(cs.getSize())]

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
r = d[CASE]
joints = list(r['joints'])
q, qd, gc = r['coordinate_values'], r['coordinate_speeds'], r['GC_percent']
nT = q.shape[1]

Lz = np.zeros(nT)
for k in range(nT):
    for c in coords:
        name = c.getName()
        i = joints.index(name)
        rot = (c.getMotionType() == 1)       # 1 = Rotational
        val = np.deg2rad(q[i, k])  if rot else q[i, k]
        spd = np.deg2rad(qd[i, k]) if rot else qd[i, k]
        c.setValue(state, val, False)
        c.setSpeedValue(state, spd)
    model.assemble(state)
    model.realizeVelocity(state)
    mom = smss.calcSystemCentralMomentum(state)
    Lz[k] = mom.get(0).get(1)                # 각운동량 벡터의 y성분(수직축)

Lz_n = Lz / (mass * SPEED * HEIGHT)

print(f"mass = {mass:.2f} kg")
print(f"Lz  range : {Lz.min():+.3f} ~ {Lz.max():+.3f} kg m^2/s")
print(f"Lz~ range : {Lz_n.min():+.5f} ~ {Lz_n.max():+.5f} (normalized)")
print(f"Lz~ RMS   : {np.sqrt(np.mean(Lz_n**2)):.5f}")

plt.figure(figsize=(8,4))
plt.plot(gc, Lz_n, lw=2)
plt.axhline(0, color='k', lw=.5)
plt.xlabel('Gait cycle (%)'); plt.ylabel(r'$L_z / (M V H)$')
plt.title('Normalized vertical-axis whole-body angular momentum')
plt.grid(alpha=.3); plt.tight_layout(); plt.show()