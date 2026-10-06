import numpy as np, sys
sys.path.insert(0, '.')

CASES = sys.argv[1:] or ['0', '114', '138']   # e.g. python analysis\check_other_planes.py 0 114 138
JOINTS = ['pelvis_tilt', 'pelvis_list', 'pelvis_rotation',
          'hip_flexion_r', 'hip_adduction_r', 'hip_rotation_r',
          'knee_angle_r', 'ankle_angle_r', 'subtalar_angle_r',
          'lumbar_extension', 'lumbar_bending', 'lumbar_rotation',
          'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r']
BW = 62.0 * 9.81

res = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
exp = np.load('OpenSimModel/Hamner_modified/experimentalData.npy',
              allow_pickle=True).item()['Hamner_modified']
pos  = exp['kinematics']['positions']
gc_e = np.asarray(pos['GC_percent']).ravel()

def ecurve(stat, j):
    return np.asarray(pos[stat][j]).ravel()

def mcurve(r, j):
    joints = list(r['joints'])
    q  = np.asarray(r['coordinate_values'])[joints.index(j), :]
    gc = np.asarray(r['GC_percent']).ravel()
    o  = np.argsort(gc)
    return np.interp(gc_e, gc[o], q[o], period=100)

print(f"{'joint':18s}" + ''.join(
    f"|{'RMSE':>7s}{'RMSEc':>7s}{'off':>7s}{'inB':>6s}{'r':>7s} [case {c}] " for c in CASES))
for j in JOINTS:
    try:
        m, s = ecurve('mean', j), ecurve('std', j)
    except (KeyError, IndexError):
        print(f"{j:18s}| 실측 없음"); continue
    row = f"{j:18s}"
    for c in CASES:
        q     = mcurve(res[c], j)
        d     = q - m
        off   = d.mean()
        rmse  = np.sqrt(np.mean(d**2))
        rmsec = np.sqrt(np.mean((d - off)**2))
        inb   = np.mean(np.abs(d) <= 2*s) * 100
        rr    = np.corrcoef(q, m)[0, 1]
        row += f"|{rmse:7.2f}{rmsec:7.2f}{off:+7.2f}{inb:5.0f}%{rr:7.3f}          "
    print(row)

print()
for c in CASES:
    r = res[c]
    grf = np.asarray(r['GRF'])
    print(f"case {c}: COT {float(r['COT']):.3f}  stride {float(r['stride_length']):.3f}  "
          f"iter {r.get('iter_count','?')}  vGRF_r max {grf[1].max()/BW:.2f} BW")