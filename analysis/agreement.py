# analysis/agreement.py
import sys; sys.path.insert(0, '.')
import numpy as np
from settings import getSettings

d  = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
st = getSettings()

TARGET = {'pelvis': 6.38, 'thorax': 11.70, 'lumbar': 14.78, 'corr': -0.044}

cases = ['23','24','0','25',           # w=0 대조군 (0.8/1.0/1.33/1.6)
         '20','21','16','22',           # w=30 sum
         '111','112','110','113']  

hdr = (f"{'case':>5} {'w':>5} {'pelROM':>8} {'thoROM':>8} {'lumROM':>8} "
       f"{'corr':>8} | {'e_pel':>7} {'e_tho':>7} {'e_lum':>7} {'e_cor':>7} {'E':>7}")
print(hdr); print('-'*len(hdr))

for c in cases:
    if c not in d: 
        print(f"{c:>5}  (not found)"); continue
    r = d[c]; j = list(r['joints']); q = r['coordinate_values']
    pel = q[j.index('pelvis_rotation'), :]
    lum = q[j.index('lumbar_rotation'), :]
    tho = pel + lum
    m = {'pelvis': np.ptp(pel), 'thorax': np.ptp(tho), 'lumbar': np.ptp(lum),
         'corr': np.corrcoef(pel-pel.mean(), tho-tho.mean())[0,1]}
    e = {k: abs(m[k]-TARGET[k])/TARGET[k] for k in ['pelvis','thorax','lumbar']}
    e['corr'] = abs(m['corr']-TARGET['corr'])/2      # corr는 [-1,1] 범위로 정규화
    E = np.mean(list(e.values()))
    w = st[c].get('GRMzTerm', 0)
    print(f"{c:>5} {w:>5} {m['pelvis']:>8.2f} {m['thorax']:>8.2f} {m['lumbar']:>8.2f} "
          f"{m['corr']:>+8.3f} | {e['pelvis']:>7.2f} {e['thorax']:>7.2f} "
          f"{e['lumbar']:>7.2f} {e['corr']:>7.2f} {E:>7.3f}")

print(f"\n[target] pelvis {TARGET['pelvis']}, thorax {TARGET['thorax']}, "
      f"lumbar {TARGET['lumbar']}, corr {TARGET['corr']}")