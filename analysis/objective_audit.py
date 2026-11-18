"""
Objective audit: how large are the added penalty terms at the optimum?

  residual = objective (IPOPT) - sum(objective_terms)   # objective_terms = base terms only
           = pelvisRotTerm + GRMzTerm contributions seen by the solver

Also prints post-hoc predictions of those two terms from the saved gait-cycle data:
  term ~= w * mean_GC(x^2) * T_GC / d_GC     (J is integrated over time and divided by distance)
Frame-invariant modes only ('free', 'pelvis_*'); origin modes ('each'/'sum') are
frame-dependent, so their prediction is marked approximate.

Run from project root:  python analysis\\objective_audit.py
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.getcwd())   # project root (script lives in analysis\)
from settings import getSettings

cases = sys.argv[1:] or ['0', '95', '110', '114', '115', '118', '119', '121', '122']   # e.g. python analysis\\x.py 114 133
FY_MIN = 30.0

S = getSettings()
d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()


def term_series(r, mode):
    GRF, GRM = np.asarray(r['GRF']), np.asarray(r['GRM'])
    J = list(r['joints']); Q = np.asarray(r['coordinate_values'])
    xp, zp = Q[J.index('pelvis_tx')], Q[J.index('pelvis_tz')]
    if mode in ('each', 'sum'):
        a, b = GRM[1], GRM[4]
    elif mode == 'free':
        out = []
        for sl in (slice(0, 3), slice(3, 6)):
            F, M = GRF[sl], GRM[sl]
            T = np.sum(M * F, axis=0) / (F[1] + 10.0)
            out.append(T)
        a, b = out
    else:  # pelvis_each / pelvis_sum
        a = GRM[1] - zp * GRF[0] + xp * GRF[2]
        b = GRM[4] - zp * GRF[3] + xp * GRF[5]
    if mode in ('sum', 'pelvis_sum'):
        return (a + b) ** 2
    return a ** 2 + b ** 2


print(f"{'case':>4} {'obj':>8} {'base':>8} {'resid':>7} | {'pred_pel':>8} {'pred_grm':>9} "
      f"| {'acc':>6} {'met':>6} {'act':>6} {'arm':>6} {'pas':>6}")
for c in cases:
    if c not in d:
        print(f'{c:>4} missing'); continue
    r = d[c]; s = S.get(c, {})
    terms = {k: float(np.squeeze(v)) for k, v in r['objective_terms'].items()}
    base = sum(terms.values())
    obj = float(r['objective'])
    t = np.asarray(r['time']).ravel()
    T_GC = t[-1] - t[0] if t.size > 1 else np.nan
    dGC = float(r['stride_length'])
    J = list(r['joints']); Q = np.asarray(r['coordinate_values'])
    pel_rad = np.deg2rad(Q[J.index('pelvis_rotation')])
    w_pel = s.get('pelvisRotTerm', 0)
    pred_pel = w_pel * np.mean(pel_rad ** 2) * T_GC / dGC
    w_g, mode = s.get('GRMzTerm', 0), s.get('GRMzMode', 'sum')
    pred_g = (w_g * np.mean(term_series(r, mode)) * T_GC / dGC) if (w_g and 'GRM' in r) else 0.0
    flag = '~' if mode in ('each', 'sum') and w_g else ' '
    print(f"{c:>4} {obj:8.2f} {base:8.2f} {obj - base:7.2f} | {pred_pel:8.2f} {pred_g:8.2f}{flag} "
          f"| {terms.get('jointAccelerationTerm', 0):6.1f} {terms.get('metabolicEnergyRateTerm', 0):6.1f} "
          f"{terms.get('activationTerm', 0):6.1f} {terms.get('armExcitationTerm', 0):6.1f} "
          f"{terms.get('passiveTorqueTerm', 0):6.1f}")
print("\nresid should ~= pred_pel + pred_grm if the penalties act as intended ('~' = origin-frame approx).")