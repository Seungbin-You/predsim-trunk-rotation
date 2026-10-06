"""
How good is the pelvis origin as a proxy for the centre of mass (COM)?

For each case, over the reconstructed gait cycle:
  1. horizontal pelvis-COM offset (cm)
  2. total vertical ground-reaction moment about the pelvis origin  M_P  (what the penalty used)
     and about the COM                                              M_G  (= dLy/dt exactly)
  3. dLy/dt from OpenSim's whole-body central angular momentum (numerical derivative)
     -> M_G vs dLy/dt checks the computation (should agree closely)
     -> M_P vs M_G quantifies the proxy error

  M_X = sum_feet [ My_O - z_X*Fx + x_X*Fz ]   (y vertical; GRM about ground origin O)

Run from project root, env predsim_tutorial (OpenSim 4.4):
    python analysis\\com_vs_pelvis.py 0 114 138
"""
import sys
import numpy as np
import opensim

cases = sys.argv[1:] or ['0', '114', '138']
MODEL = 'OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim'

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
model = opensim.Model(MODEL)
state = model.initSystem()
cs = model.getCoordinateSet()
coord = {cs.get(i).getName(): cs.get(i) for i in range(cs.getSize())}
TRANSL = 2   # opensim.Coordinate.Translational
rms = lambda x: np.sqrt(np.mean(np.asarray(x) ** 2))


def eval_case(c):
    r = d[c]
    J = list(r['joints'])
    Q = np.asarray(r['coordinate_values'], float)       # rotations in deg, translations in m
    Qd = np.asarray(r['coordinate_speeds'], float)
    GRF, GRM = np.asarray(r['GRF'], float), np.asarray(r['GRM'], float)
    t = np.asarray(r['time'], float).ravel()
    n = Q.shape[1]
    t = t[:n]
    missing = [j for j in J if j not in coord]
    if missing:
        print(f'  [warn] not in model, skipped: {missing}')

    com = np.zeros((3, n)); Ly = np.zeros(n)
    for k in range(n):
        for i, j in enumerate(J):
            if j not in coord:
                continue
            cobj = coord[j]
            conv = 1.0 if cobj.getMotionType() == TRANSL else np.pi / 180
            cobj.setValue(state, Q[i, k] * conv, False)
            cobj.setSpeedValue(state, Qd[i, k] * conv)
        model.realizeVelocity(state)
        p = model.calcMassCenterPosition(state)
        com[:, k] = [p.get(0), p.get(1), p.get(2)]
        Ly[k] = model.getMatterSubsystem().calcSystemCentralMomentum(state).get(0).get(1)

    xp, zp = Q[J.index('pelvis_tx')], Q[J.index('pelvis_tz')]
    xg, zg = com[0], com[2]
    Fx = GRF[0] + GRF[3]; Fz = GRF[2] + GRF[5]; MyO = GRM[1] + GRM[4]
    MP = MyO - zp * Fx + xp * Fz
    MG = MyO - zg * Fx + xg * Fz

    # periodic central difference of Ly (uniform mesh assumed; reconstructed cycle is periodic)
    dt = np.median(np.diff(t))
    dLy = (np.roll(Ly, -1) - np.roll(Ly, 1)) / (2 * dt)

    off = np.hypot(xp - xg, zp - zg) * 100
    return dict(off_mean=off.mean(), off_max=off.max(),
                dx=np.mean(xp - xg) * 100, dz=np.mean(zp - zg) * 100,
                MP=rms(MP), MG=rms(MG), dL=rms(dLy),
                r_GL=np.corrcoef(MG, dLy)[0, 1], err_GL=rms(MG - dLy),
                r_PG=np.corrcoef(MP, MG)[0, 1], err_PG=rms(MP - MG), Ly=rms(Ly))


print(f"{'case':>4} | {'offset mean/max (cm)':>20} | {'mean dx/dz (cm)':>15} | "
      f"{'RMS M_P':>7} {'M_G':>6} {'dL/dt':>6} | {'r(MG,dL)':>8} {'err':>5} | "
      f"{'r(MP,MG)':>8} {'err':>5}")
print('-' * 112)
res = {}
for c in cases:
    if c not in d:
        print(f'{c:>4} missing'); continue
    m = res[c] = eval_case(c)
    print(f"{c:>4} | {m['off_mean']:8.2f} / {m['off_max']:6.2f}     | {m['dx']:6.2f} / {m['dz']:6.2f} | "
          f"{m['MP']:7.2f} {m['MG']:6.2f} {m['dL']:6.2f} | {m['r_GL']:8.3f} {m['err_GL']:5.2f} | "
          f"{m['r_PG']:8.3f} {m['err_PG']:5.2f}")

if '114' in res and '138' in res:
    for k, lab in (('MP', 'about pelvis'), ('MG', 'about COM (= dL/dt)')):
        a, b = res['114'][k], res['138'][k]
        print(f"114 -> 138 vertical moment {lab}: {a:.2f} -> {b:.2f} N m ({(b / a - 1) * 100:+.0f}%)")

print("\nM in N m (RMS over gait cycle). r(MG,dL) ~ 1 validates the computation;"
      "\nr(MP,MG) and err(MP-MG) quantify the pelvis-as-COM proxy error.")
