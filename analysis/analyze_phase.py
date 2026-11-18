# analyze_phase.py
import numpy as np
import matplotlib.pyplot as plt

d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
cases = ['23','24','0','25',           # w=0 대조군 (0.8/1.0/1.33/1.6)
         '20','21','16','22',           # w=30 sum
         '111','112','110','113']  
PLOT_CASES = ['63','70']

# ---------- 요약 표 ----------
hdr = (f"{'case':>5} {'corr':>8} {'pelROM':>8} {'thoROM':>8} {'lumROM':>8} "
       f"{'armROM':>8} {'stride':>8} {'COT':>8} {'obj':>10}")
print(hdr); print('-'*len(hdr))

for c in cases:
    if c not in d:
        print(f"{c:>5}   (not found)")
        continue
    r = d[c]
    j = list(r['joints']); q = r['coordinate_values']
    pel = q[j.index('pelvis_rotation'), :]
    lum = q[j.index('lumbar_rotation'), :]
    arm = q[j.index('arm_flex_r'), :]
    tho = pel + lum
    corr = np.corrcoef(pel-pel.mean(), tho-tho.mean())[0, 1]
    print(f"{c:>5} {corr:>+8.3f} {np.ptp(pel):>8.2f} {np.ptp(tho):>8.2f} "
          f"{np.ptp(lum):>8.2f} {np.ptp(arm):>8.2f} "
          f"{float(r['stride_length']):>8.3f} {float(r['COT']):>8.3f} "
          f"{float(r['objective']):>10.2f}")

# ---------- 파형 비교 ----------
fig, axes = plt.subplots(1, len(PLOT_CASES), figsize=(6*len(PLOT_CASES), 4),
                         sharey=True, squeeze=False)
for ax, c in zip(axes[0], PLOT_CASES):
    if c not in d:
        continue
    r = d[c]
    j = list(r['joints']); q = r['coordinate_values']; gc = r['GC_percent']
    pel = q[j.index('pelvis_rotation'), :]
    lum = q[j.index('lumbar_rotation'), :]
    tho = pel + lum
    ax.plot(gc, pel-pel.mean(), label='pelvis (abs)', lw=2)
    ax.plot(gc, tho-tho.mean(), label='thorax (abs)', lw=2)
    ax.plot(gc, lum-lum.mean(), label='lumbar (rel)', ls='--')
    ax.axhline(0, color='k', lw=.5)
    ax.set_title(f'case {c}')
    ax.set_xlabel('Gait cycle (%)'); ax.grid(alpha=.3)
axes[0][0].set_ylabel('Yaw (deg)'); axes[0][0].legend()
plt.tight_layout(); plt.show()