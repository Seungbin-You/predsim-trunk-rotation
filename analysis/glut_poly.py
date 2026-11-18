"""Gluteal (abductor) lever-arm variants: recompute MTU length / moment arms of
glut_med1-3 and glut_min1-3 (both sides) with OpenSim and refit the polynomial
approximations used by main.py.  All other muscles keep the baseline fit.

usage: python glut_poly.py <project_root> <k> [<k> ...]   (k = 1.0 -> validation)
Insertion (femur) points are moved laterally: z_ins -> k * z_ins (femur frame,
origin = hip joint centre).  MTU length is offset so that the length in the
neutral posture is unchanged (equivalent to re-tuning tendon slack length).
"""
import os, sys, copy
import numpy as np
import opensim

ROOT = sys.argv[1]
KS = [float(k) for k in sys.argv[2:]]
MODEL_DIR = os.path.join(ROOT, 'OpenSimModel', 'Hamner_modified', 'Model')
OSIM = os.path.join(MODEL_DIR, 'Hamner_modified_scaled.osim')
MOT = os.path.join(ROOT, 'OpenSimModel', 'templates', 'MuscleAnalysis', 'dummy_motion.mot')
OUT = os.environ.get('OUT', os.path.join(os.getcwd(), 'out'))
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, ROOT)
from polynomials import getPolynomialCoefficients  # noqa: E402

GLUTS = ['glut_med1', 'glut_med2', 'glut_med3', 'glut_min1', 'glut_min2', 'glut_min3']
JOINTS = {s: ['hip_flexion_' + s, 'hip_adduction_' + s, 'hip_rotation_' + s, 'knee_angle_' + s,
              'ankle_angle_' + s, 'subtalar_angle_' + s, 'mtp_angle_' + s] for s in 'rl'}
HIP = {s: ['hip_flexion_' + s, 'hip_adduction_' + s, 'hip_rotation_' + s] for s in 'rl'}
opensim.Logger.setLevelString('error')


def make_model(k):
    model = opensim.Model(OSIM)
    for s in 'rl':
        for g in GLUTS:
            m = opensim.Muscle.safeDownCast(model.getForceSet().get(g + '_' + s))
            pps = m.getGeometryPath().getPathPointSet()
            p = opensim.PathPoint.safeDownCast(pps.get(pps.getSize() - 1))   # insertion on femur
            assert 'femur' in p.getParentFrame().getName(), p.getParentFrame().getName()
            loc = p.get_location()
            p.set_location(opensim.Vec3(loc.get(0), loc.get(1), k * loc.get(2)))
    model.finalizeConnections()
    model.initSystem()
    return model


def mtu(model, data, labels):
    state = model.initSystem()
    cs = model.getCoordinateSet()
    short = [l.split('/')[-2] for l in labels]
    coords = [cs.get(c) for c in short]
    beta = {s: (cs.get('knee_angle_%s_beta' % s) if cs.contains('knee_angle_%s_beta' % s) else None)
            for s in 'rl'}
    names = [g + '_' + s for s in 'rl' for g in GLUTS]
    musc = [opensim.Muscle.safeDownCast(model.getForceSet().get(n)) for n in names]
    L = np.zeros((data.shape[0], len(names)))
    D = np.zeros((data.shape[0], len(names), len(short)))
    for i in range(data.shape[0]):
        for c, co in enumerate(coords):
            co.setValue(state, np.radians(data[i, c]), False)
        for s in 'rl':
            if beta[s] is not None:
                beta[s].setValue(state, np.radians(data[i, short.index('knee_angle_' + s)]), False)
        model.realizePosition(state)
        for j, (n, m) in enumerate(zip(names, musc)):
            L[i, j] = m.getLength(state)
            for c, coord in enumerate(short):
                if coord in HIP[n[-1]]:
                    D[i, j, c] = m.computeMomentArm(state, coords[c])
    return names, L, D


tab = opensim.TimeSeriesTable(MOT)
labels = list(tab.getColumnLabels())
data = tab.getMatrix().to_numpy()
NMAX = int(os.environ.get('NMAX', data.shape[0]))
data = data[:NMAX]
short = [l.split('/')[-2] for l in labels]
neutral = np.zeros((1, data.shape[1]))
base = {s: np.load(os.path.join(MODEL_DIR, 'Hamner_modified_scaled_polynomial_%s.npy' % s),
                   allow_pickle=True).item() for s in 'rl'}

for k in KS:
    model = make_model(k)
    names, L, D = mtu(model, data, labels)
    _, L0, D0 = mtu(make_model(1.0), neutral, labels) if k != 1.0 else (None, None, None)
    _, Lk0, Dk0 = mtu(model, neutral, labels)
    if k != 1.0:
        L = L - (Lk0 - L0)                         # keep neutral MTU length (tendon slack re-tuned)
    d4 = dict(mtu_lengths=L, mtu_moment_arms=D, muscle_names=names, coordinate_names=short,
              coordinate_values=data)
    tag = 'abd%03d' % round(100 * k)
    hip_add = {}
    for s in 'rl':
        musc = [g + '_' + s for g in GLUTS]
        fit = getPolynomialCoefficients(d4, JOINTS[s], musc, side=s)
        new = copy.deepcopy(base[s])
        for m in musc:
            new[m] = fit[m]
        np.save(os.path.join(OUT, 'Hamner_modified_scaled_%s_polynomial_%s.npy' % (tag, s)), new)
        # JSON copy for main.py (polynomialTag), readable from NumPy 1.x and 2.x alike
        import json
        with open(os.path.join(OUT, 'Hamner_modified_scaled_%s_polynomial_%s.json' % (tag, s)), 'w') as f:
            json.dump({m: {'dimension': int(v['dimension']), 'order': int(v['order']),
                           'coefficients': [float(x) for x in np.ravel(v['coefficients'])],
                           'spanning': [int(x) for x in np.ravel(v['spanning'])]}
                       for m, v in new.items()}, f)
        ia = short.index('hip_adduction_' + s)
        hip_add[s] = Dk0[0, [names.index(m) for m in musc], ia]
    print('k=%.2f  neutral hip-adduction moment arm (m), right:' % k, np.round(hip_add['r'], 4))
    np.save(os.path.join(OUT, 'd4_%s.npy' % tag), d4)
print('done')
