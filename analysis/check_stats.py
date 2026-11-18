# analysis\check_stats.py
import numpy as np
res = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
for c in ['0','6','55','61','63','70','84','95','96','102','106','107','108','109','110']:
    if c not in res: print(f"{c}: 없음"); continue
    r = res[c]
    print(f"{c:>4s} | success={r.get('stats','MISSING')} | "
          f"ret={r.get('return_status','')!r} | "
          f"uni={r.get('unified_return_status','')!r} | "
          f"iter={r.get('iter_count','?')}")