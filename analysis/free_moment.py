"""
Recompute the true free moment (vertical twisting moment about the COP)
from saved GRF/GRM, and compare with the vertical GRM about the ground origin
that GRMzTerm actually penalises.

Run from project root (env: predsim):  python analysis\\free_moment.py

Background (verified in opensimAD/utilities.py and the generated .cpp):
  GRM_i = r_CP_i(ground) x F_i  -> moments are about the GROUND ORIGIN.
  Free moment is origin-invariant:  T_free = (M_O . F) / F_y   (y = vertical)
  because M_O = r_COP x F + T_free*y  and (r_COP x F) . F = 0.
"""
import sys
import numpy as np

cases = sys.argv[1:] or ['0', '55', '95', '110']   # e.g. python analysis\\x.py 114 133   # edit as needed
FY_MIN = 30.0                      # N, same stance threshold as main.py

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
rms = lambda x: np.sqrt(np.mean(x ** 2))

print(f"{'case':>5} | {'My_origin RMS r/l':>18} | {'Tfree RMS r/l':>14} | "
      f"{'Tfree max r/l':>14} | {'Tfree sum RMS':>13}")
for c in cases:
    if c not in d or 'GRM' not in d[c]:
        print(f'{c:>5} | missing case or GRM key'); continue
    GRF, GRM = np.asarray(d[c]['GRF']), np.asarray(d[c]['GRM'])  # 6xN: r xyz, l xyz
    out = {}
    for s, sl in (('r', slice(0, 3)), ('l', slice(3, 6))):
        F, M = GRF[sl], GRM[sl]
        stance = F[1] > FY_MIN
        T = np.zeros(F.shape[1])
        T[stance] = np.sum(M[:, stance] * F[:, stance], axis=0) / F[1, stance]
        out[s] = (M[1], T)
    Tsum = out['r'][1] + out['l'][1]
    print(f"{c:>5} | {rms(out['r'][0]):8.2f} {rms(out['l'][0]):8.2f} | "
          f"{rms(out['r'][1]):6.2f} {rms(out['l'][1]):6.2f} | "
          f"{abs(out['r'][1]).max():6.2f} {abs(out['l'][1]).max():6.2f} | "
          f"{rms(Tsum):13.2f}")
# Plausibility reference: Li et al. 2001, peak free moment ~3-9 N m for 62 kg.