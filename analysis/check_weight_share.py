# analysis/check_weight_share.py
import numpy as np
d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
SP = {'20':0.8,'21':1.0,'16':1.33,'22':1.6,'23':0.8,'24':1.0,'0':1.33,'25':1.6}
print(f"{'case':>5} {'v':>5} {'obj':>10} {'GRMz':>10} {'share%':>8}")
for c in ['23','24','0','25','20','21','16','22']:
    r = d[c]
    g = float(np.array(r['objective_terms'].get('GRMzTerm', 0)).ravel()[0])
    o = float(r['objective'])
    print(f"{c:>5} {SP[c]:>5.2f} {o:>10.2f} {g:>10.2f} {100*g/o:>8.2f}")