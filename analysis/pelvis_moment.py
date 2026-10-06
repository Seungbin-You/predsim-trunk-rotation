"""
Vertical ground reaction moment about the PELVIS vertical axis (origin-independent),
compared with the moment about the ground origin (what 'each'/'sum' GRMzTerm penalised).

  My_P = My_O - z_p*Fx + x_p*Fz      (y vertical; P = pelvis origin, horizontal coords)
       = T_free + (z_cop - z_p)*Fx - (x_cop - x_p)*Fz
  Sum over both feet about P ~ rate of change of whole-body vertical angular
  momentum if P were the COM (pelvis used as a proxy).

GRM/GRF in the npy come from F evaluated on the reconstructed gait-cycle
trajectory (main.py F1_GC), so they share the frame of coordinate_values.

Run from project root:  python analysis\\pelvis_moment.py
"""
import sys
import numpy as np

cases = sys.argv[1:] or ['0', '95', '110', '114', '115']   # e.g. python analysis\\x.py 114 133
W_REF, REF_CASE = 20, '0'          # 110 used each-origin w=20

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
rms = lambda x: np.sqrt(np.mean(x ** 2))
ms = lambda x: np.mean(x ** 2)

res = {}
print(f"{'case':>4} | {'origin each r/l':>16} | {'pelvis each r/l':>16} | "
      f"{'pelvis sum':>10} | {'origin sum':>10}")
for c in cases:
    if c not in d or 'GRM' not in d[c]:
        print(f'{c:>4} missing'); continue
    r = d[c]
    J = list(r['joints']); Q = np.asarray(r['coordinate_values'])
    xp, zp = Q[J.index('pelvis_tx')], Q[J.index('pelvis_tz')]   # metres
    GRF, GRM = np.asarray(r['GRF']), np.asarray(r['GRM'])
    MyO = [GRM[1], GRM[4]]
    MyP = [GRM[1] - zp * GRF[0] + xp * GRF[2],
           GRM[4] - zp * GRF[3] + xp * GRF[5]]
    res[c] = (MyO, MyP)
    print(f"{c:>4} | {rms(MyO[0]):7.2f} {rms(MyO[1]):8.2f} | "
          f"{rms(MyP[0]):7.2f} {rms(MyP[1]):8.2f} | {rms(MyP[0] + MyP[1]):10.2f} | "
          f"{rms(MyO[0] + MyO[1]):10.2f}")

if REF_CASE in res:
    MyO, MyP = res[REF_CASE]
    ms_o = ms(MyO[0]) + ms(MyO[1])
    print(f"\nWeights giving the same penalty magnitude as each-origin w={W_REF} "
          f"at case {REF_CASE}:")
    print(f"  pelvis_each : {W_REF * ms_o / (ms(MyP[0]) + ms(MyP[1])):.1f}")
    print(f"  pelvis_sum  : {W_REF * ms_o / ms(MyP[0] + MyP[1]):.1f}")