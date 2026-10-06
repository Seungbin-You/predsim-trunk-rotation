"""
Pelvis-thorax relative phase from the first (stride-frequency) harmonic,
in degrees, for model cases and the experimental mean.

Why: Pearson corr cannot tell "90 deg phase shift with full thorax amplitude"
from "thorax nearly still" (both give corr ~ 0). The first-harmonic phase and
amplitude separate the two, and the harmonic power fraction shows how much of
each signal is stride-frequency (cf. Lamoth et al. 2002 on higher harmonics
in pelvis rotation).

  relphase = angle(H1_thorax / H1_pelvis)   [deg, 0 = in-phase, 180 = anti-phase]
  thorax   = pelvis_rotation + lumbar_rotation

Run from project root:  python analysis\\phase_harmonic.py 0 114 130 131 132 133
"""
import sys
import numpy as np

cases = sys.argv[1:] or ['0', '114', '110', '130', '131', '132', '133', '134',
                         '135', '136', '137']
EXP = 'OpenSimModel/Hamner_modified/experimentalData.npy'


def periodic(x, gc=None):
    x = np.asarray(x, dtype=float).ravel()
    if gc is not None:
        gc = np.asarray(gc, dtype=float).ravel()
        if gc.size == x.size and gc[-1] >= 99.999 and gc[0] <= 0.001:
            x = x[:-1]                      # drop duplicated 100% sample
    return x


def h1(x):
    n = x.size
    c = np.sum((x - x.mean()) * np.exp(-2j * np.pi * np.arange(n) / n))
    amp = 2 * np.abs(c) / n                 # half peak-to-peak of 1st harmonic
    frac = (2 * np.abs(c) ** 2 / n ** 2) / np.mean((x - x.mean()) ** 2)
    return c, amp, frac


def report(name, pel, lum):
    tho = pel + lum
    cp, ap, fp = h1(pel)
    ct, at, ft = h1(tho)
    cl, al, fl = h1(lum)
    rel = np.degrees(np.angle(ct / cp))
    rel_lp = np.degrees(np.angle(cl / cp))
    corr = np.corrcoef(pel, tho)[0, 1]
    print(f"{name:>5} | {2*ap:6.2f} {2*at:6.2f} {2*al:6.2f} | "
          f"{fp:5.2f} {ft:5.2f} | {abs(rel):6.1f} | {abs(rel_lp):6.1f} | {corr:+6.3f}")


print(f"{'case':>5} | {'2A1 pel':>6} {'tho':>6} {'lum':>6} | {'P1 pel':>5} {'tho':>5} | "
      f"{'|dphi|':>6} | {'lum-pel':>7} | {'corr':>6}")
print('-' * 72)
try:
    e = np.load(EXP, allow_pickle=True).item()
    pos = e['Hamner_modified']['kinematics']['positions']
    gc = pos.get('GC_percent', None)
    report('EXP', periodic(pos['mean']['pelvis_rotation'], gc),
           periodic(pos['mean']['lumbar_rotation'], gc))
except Exception as ex:
    print(f"  EXP not loaded ({ex})")

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
for c in cases:
    if c not in d:
        print(f'{c:>5} missing'); continue
    J = list(d[c]['joints']); Q = np.asarray(d[c]['coordinate_values'])
    report(c, Q[J.index('pelvis_rotation')], Q[J.index('lumbar_rotation')])

print("\n2A1 = peak-to-peak of the 1st harmonic [deg]; P1 = fraction of variance in the"
      " 1st harmonic;\n|dphi| = thorax-pelvis relative phase [deg] (literature at ~1.33 m/s:"
      " Bruijn 2008 ~110, Lamoth 2002 ~100-149);\nlum-pel = lumbar-pelvis relative phase [deg]"
      " (180 = lumbar exactly opposes pelvis).")