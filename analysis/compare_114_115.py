"""
GRMz re-test: 110 (origin-moment penalty) vs 114 (no GRMz) vs 115 (true free moment).
Cases 0/95/110 are included as a self-check against handover values
(case 0: pelROM 18.22, lumROM 3.83, corr +0.998, E 0.841;
 case 110: pelROM 6.73, thoROM 11.71, lumROM 14.26, corr -0.180, E 0.040).

Run from project root (env: predsim):  python analysis\\compare_114_115.py
"""
import sys
import numpy as np

cases = sys.argv[1:] or ['0', '95', '110', '114', '115']   # e.g. python analysis\\x.py 114 133
TARGET = {'pelvis': 6.38, 'thorax': 11.70, 'lumbar': 14.78, 'corr': -0.044}
FY_MIN = 30.0

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
rms = lambda x: np.sqrt(np.mean(x ** 2))
rom = lambda x: np.max(x) - np.min(x)


def free_moment(GRF, GRM):
    out = []
    for sl in (slice(0, 3), slice(3, 6)):
        F, M = GRF[sl], GRM[sl]
        st = F[1] > FY_MIN
        T = np.zeros(F.shape[1])
        T[st] = np.sum(M[:, st] * F[:, st], axis=0) / F[1, st]
        out.append(T)
    return out  # [T_r, T_l]


hdr = (f"{'case':>4} {'status':>16} {'iter':>5} {'obj':>8} | {'pel':>6} {'tho':>6} "
       f"{'lum':>6} {'corr':>7} {'E':>6} | {'Tf_rms':>6} {'Tf_max':>6} {'Myo_rms':>7} | "
       f"{'COT':>6} {'stride':>6} {'arm':>6}")
print(hdr); print('-' * len(hdr))
for c in cases:
    if c not in d:
        print(f'{c:>4} missing'); continue
    r = d[c]
    Q = np.asarray(r['coordinate_values'])          # deg for rotations
    J = list(r['joints'])
    pel = Q[J.index('pelvis_rotation')]
    lum = Q[J.index('lumbar_rotation')]
    tho = pel + lum
    corr = np.corrcoef(pel, tho)[0, 1]
    e = [abs(rom(pel) - TARGET['pelvis']) / TARGET['pelvis'],
         abs(rom(tho) - TARGET['thorax']) / TARGET['thorax'],
         abs(rom(lum) - TARGET['lumbar']) / TARGET['lumbar'],
         abs(corr - TARGET['corr']) / 2]
    E = np.mean(e)
    status = str(r.get('unified_return_status', r.get('return_status', '?')))[:16]
    if 'GRM' in r:
        GRF, GRM = np.asarray(r['GRF']), np.asarray(r['GRM'])
        Tr, Tl = free_moment(GRF, GRM)
        tf_rms, tf_max = rms(Tr), max(abs(Tr).max(), abs(Tl).max())
        myo = rms(GRM[1])
    else:
        tf_rms = tf_max = myo = np.nan
    arm = rom(Q[J.index('arm_flex_r')]) if 'arm_flex_r' in J else np.nan
    print(f"{c:>4} {status:>16} {r['iter_count']:>5} {r['objective']:>8.2f} | "
          f"{rom(pel):6.2f} {rom(tho):6.2f} {rom(lum):6.2f} {corr:+7.3f} {E:6.3f} | "
          f"{tf_rms:6.2f} {tf_max:6.2f} {myo:7.2f} | "
          f"{r['COT']:6.3f} {r['stride_length']:6.3f} {arm:6.2f}")
print("\nTf = true free moment per foot [N m]; Myo = vertical GRM about ground origin (right) [N m]")