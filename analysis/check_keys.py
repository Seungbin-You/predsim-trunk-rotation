# analysis\check_keys.py
import numpy as np
res = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
print(sorted(res['0'].keys()))
print()
print('총 case 수:', len(res))
print(sorted(res.keys(), key=lambda x: int(x)))