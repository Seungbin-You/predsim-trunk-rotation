# analysis/analyze_grm.py
import sys
sys.path.insert(0, '.')

import numpy as np
import matplotlib.pyplot as plt
from settings import getSettings

d  = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
st = getSettings()

cases = ['0', '96', '102', '106', '107', '108', '109', '110']
labels = {c: st[c].get('GRMzTerm', 0) for c in cases}

print(f"{'case':>5} {'w':>6} {'Mz_sum_RMS':>12} {'Mz_sum_max':>12} {'Mz_r_max':>10} {'Mz_l_max':>10}")
print('-'*60)
curves = {}
for c in cases:
    if c not in d or 'GRM' not in d[c]:
        print(f"{c:>5}   (no GRM)"); continue
    G = d[c]['GRM']                 # (6, nT): r-xyz, l-xyz
    mzr, mzl = G[1,:], G[4,:]
    s = mzr + mzl
    print(f"{c:>5} {labels[c]:>6} {np.sqrt((s**2).mean()):>12.3f} "
          f"{np.abs(s).max():>12.3f} {np.abs(mzr).max():>10.3f} {np.abs(mzl).max():>10.3f}")
    curves[c] = (d[c]['GC_percent'], s)

plt.figure(figsize=(9,5))
for c,(gc,s) in curves.items():
    plt.plot(gc, s, lw=2, label=f"w={labels[c]}")
plt.axhline(0, color='k', lw=.5)
plt.xlabel('Gait cycle (%)'); plt.ylabel(r'$M_{z,r}+M_{z,l}$ (Nm)')
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()