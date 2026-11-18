"""Export selected cases from Results/optimaltrajectories.npy into a small file.
Usage (project root):  python analysis\\export_cases.py 248 249 250 251 252 253 254 255
Output: Results/export_cases.npy
"""
import sys
import numpy as np
d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
cases = sys.argv[1:]
out = {c: d[c] for c in cases if c in d}
missing = [c for c in cases if c not in d]
np.save('Results/export_cases.npy', out)
print('exported', list(out.keys()), 'missing', missing)
