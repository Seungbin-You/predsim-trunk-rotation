# analysis\convergence_table.py
import numpy as np, sys
sys.path.insert(0, '.')
from settings import getSettings

res = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
st  = getSettings()

def g(c, k, d):
    s = st.get(c, {})
    return s.get(k, d)

print(f"{'case':>5s} {'w_acc':>7s} {'w_pel':>7s} {'GRMz':>6s} {'mode':>5s} "
      f"{'iter':>6s} {'obj':>10s} {'COT':>7s}")
for c in sorted(res.keys(), key=int):
    r = res[c]
    print(f"{c:>5s} {g(c,'jointAccelerationTerm',50000):>7} "
          f"{g(c,'pelvisRotTerm',0):>7} {g(c,'GRMzTerm',0):>6} "
          f"{str(g(c,'GRMzMode','-')):>5s} {r.get('iter_count','?'):>6} "
          f"{float(r['objective']):>10.2f} {float(r['COT']):>7.3f}")