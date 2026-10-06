import sys
sys.path.insert(0, '.')

import numpy as np
import opensim as osim
import matplotlib.pyplot as plt
from settings import getSettings

MODEL  = 'OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim'
CASES = ['114', '138']    # momentum_contribution.py — 대문자
HEIGHT = 1.70

st     = getSettings()
SPEEDS = {c: st[c].get('targetSpeed', 1.33) for c in CASES}

model = osim.Model(MODEL)
state = model.initSystem()
mass  = model.getTotalMass(state)
smss  = model.getMatterSubsystem()
cs = model.getCoordinateSet()
coords = [cs.get(i) for i in range(cs.getSize())]

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()

def Lz_zeroed(state_data, k, zero_names):
    joints, q, qd = state_data
    for c in coords:
        n = c.getName()
        i = joints.index(n)
        rot = not n.startswith('pelvis_t')
        c.setValue(state, np.deg2rad(q[i,k]) if rot else q[i,k], False)
        raw = np.deg2rad(qd[i,k]) if rot else qd[i,k]
        c.setSpeedValue(state, 0.0 if n in zero_names else raw)
    model.realizeVelocity(state)
    return smss.calcSystemCentralMomentum(state).get(0).get(1)

hdr = (f"{'case':>5} {'v':>5} {'full':>9} {'noArms':>9} {'noLegs':>9} "
       f"{'noLumbar':>9} {'noPelYaw':>9}")
print(hdr); print('-'*len(hdr))

curves = {}
for CASE in CASES:
    if CASE not in d:
        print(f"{CASE:>5}   (not found)"); continue
    r = d[CASE]
    joints = list(r['joints'])
    sd = (joints, r['coordinate_values'], r['coordinate_speeds'])
    nT = r['coordinate_values'].shape[1]
    norm = mass * SPEEDS[CASE] * HEIGHT  

    arms = [n for n in joints if n.startswith('arm_') or n.startswith('elbow_')]
    legs = [n for n in joints if any(n.startswith(s) for s in
            ['hip_','knee_','ankle_','subtalar_','mtp_'])]
    lumb = [n for n in joints if n.startswith('lumbar_')]
    pelv = ['pelvis_rotation']
    sets = {'full': [], 'noArms': arms, 'noLegs': legs,
            'noLumbar': lumb, 'noPelYaw': pelv}

    rms = {}
    for lab, zs in sets.items():
        a = np.array([Lz_zeroed(sd, k, zs) for k in range(nT)])
        rms[lab] = np.sqrt((a**2).mean())/norm
        if lab == 'full':
            curves[CASE] = (r['GC_percent'], a/norm)
    print(f"{CASE:>5} " + " ".join(f"{rms[l]:>9.5f}" for l in sets))

plt.figure(figsize=(9,5))
for CASE, (gc, a) in curves.items():
    plt.plot(gc, a, lw=2, label=f'case {CASE}')
plt.axhline(0, color='k', lw=.5)
plt.xlabel('Gait cycle (%)'); plt.ylabel(r'$L_z/(MVH)$')
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()