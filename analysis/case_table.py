"""
All-case summary for the Supplementary Material (Tables S1 and S5).

For every case in Results/optimaltrajectories.npy:
  settings  : w_acc, w_pel, added-term mode and weight, speed, N, initial guess
  solution  : solver status, iterations, objective, COT
  kinematics: ROM pelvis/thorax/lumbar, first-harmonic thorax-pelvis and lumbar-pelvis phase,
              thorax first-harmonic peak-to-peak, E_phase (as in the manuscript)

Settings are read from settings.py (the npy does not store weights), so a case whose settings
entry was edited after it was run will be reported with the edited values -> check flagged rows.
Cases 116-124 are forced to 'sum' (origin): their settings say pelvis_* but main.py had no
pelvis branch when they ran (handover 6-3).

Run from project root:  python analysis\\case_table.py
Output: analysis\\out\\case_table.csv, analysis\\out\\tableS1_origin_rows.tex, analysis\\out\\tableS5_rows.tex
"""
import os
import sys
import csv
import numpy as np
sys.path.insert(0, os.getcwd())
from settings import getSettings

EXP = {'pel': 6.38, 'tho': 11.70, 'lum': 14.78, 'phase': 95.8}
FORCE_ORIGIN_SUM = {str(c) for c in range(116, 125)}
DEFAULT = {'jointAccelerationTerm': 50000, 'pelvisRotTerm': 0, 'GRMzTerm': 0, 'GRMzMode': 'sum',
           'targetSpeed': 1.33, 'N': 50, 'guessType': 'hotStart',
           'metabolicEnergyRateTerm': 500, 'armExcitationTerm': 1e6}
MODE_LABEL = {'sum': 'origin sum', 'each': 'origin each', 'free': 'free moment',
              'pelvis_sum': 'pelvis sum (AM)', 'pelvis_each': 'pelvis each'}

S = getSettings()
d = np.load('Results/optimaltrajectories.npy', allow_pickle=True).item()
os.makedirs(os.path.join('analysis', 'out'), exist_ok=True)


def h1(x):
    x = np.asarray(x, float).ravel(); n = x.size
    return np.sum((x - x.mean()) * np.exp(-2j * np.pi * np.arange(n) / n)), n


def status_of(r):
    for k in ('unified_return_status', 'return_status'):
        if k in r: return str(r[k])
    st = r.get('stats', None)
    if isinstance(st, dict) and 'return_status' in st: return str(st['return_status'])
    return 'n/a'


def key(c):
    try: return (0, float(c))
    except ValueError: return (1, c)


rows = []
for c in sorted(d.keys(), key=key):
    r = d[c]; s = {**DEFAULT, **S.get(int(c) if str(c).isdigit() else c, S.get(c, {}))}
    flag = []
    if not S.get(int(c) if str(c).isdigit() else c, S.get(c, None)):
        flag.append('no settings entry')
    mode = s['GRMzMode']
    if str(c) in FORCE_ORIGIN_SUM and s['GRMzTerm']:
        if mode != 'sum': flag.append(f'settings say {mode}; ran as origin sum')
        mode = 'sum'
    w_add = s['GRMzTerm']
    try:
        J = list(r['joints']); Q = np.asarray(r['coordinate_values'])
        pel, lum = Q[J.index('pelvis_rotation')], Q[J.index('lumbar_rotation')]
    except Exception as ex:
        print(f'{c}: kinematics not readable ({ex})'); continue
    tho = pel + lum
    rom = lambda x: float(np.max(x) - np.min(x))
    (cp, n), (ct, _), (cl, _) = h1(pel), h1(tho), h1(lum)
    ph_tp = abs(np.degrees(np.angle(ct / cp)))
    ph_lp = abs(np.degrees(np.angle(cl / cp)))
    a_tho = 4 * np.abs(ct) / n                 # peak-to-peak of first harmonic
    e_phase = np.mean([abs(rom(pel) - EXP['pel']) / EXP['pel'],
                       abs(rom(tho) - EXP['tho']) / EXP['tho'],
                       abs(rom(lum) - EXP['lum']) / EXP['lum'],
                       abs(ph_tp - EXP['phase']) / 180])
    rows.append(dict(case=c, w_acc=s['jointAccelerationTerm'], w_pel=s['pelvisRotTerm'],
                     term=(MODE_LABEL.get(mode, mode) if w_add else '--'), w_term=(w_add or ''),
                     w_met=s['metabolicEnergyRateTerm'], w_arm=s['armExcitationTerm'],
                     speed=s['targetSpeed'], N=s['N'], guess=s['guessType'].replace('Start', ''),
                     status=status_of(r), iter=r.get('iter_count', ''), obj=r.get('objective', np.nan),
                     COT=r.get('COT', np.nan), pel=rom(pel), tho=rom(tho), lum=rom(lum),
                     ph_tp=ph_tp, ph_lp=ph_lp, a_tho=a_tho, E_phase=e_phase, flag='; '.join(flag)))

cols = list(rows[0].keys())
with open(os.path.join('analysis', 'out', 'case_table.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

hdr = (f"{'case':>5} {'w_acc':>7} {'w_pel':>6} {'term':>15} {'w':>6} {'v':>5} {'N':>3} {'guess':>5} "
       f"{'status':>12} {'obj':>8} {'COT':>6} | {'pel':>6} {'tho':>6} {'lum':>6} {'th-pel':>6} "
       f"{'lum-pel':>7} {'A_tho':>6} {'E_ph':>6}  flag")
print(hdr); print('-' * len(hdr))
for q in rows:
    print(f"{q['case']:>5} {q['w_acc']:>7g} {q['w_pel']:>6g} {q['term']:>15} {str(q['w_term']):>6} "
          f"{q['speed']:>5g} {q['N']:>3} {q['guess']:>5} {('ok' if 'SUCC' in q['status'].upper() else q['status'][:12]):>12} {q['obj']:>8.2f} "
          f"{q['COT']:>6.3f} | {q['pel']:6.2f} {q['tho']:6.2f} {q['lum']:6.2f} {q['ph_tp']:6.1f} "
          f"{q['ph_lp']:7.1f} {q['a_tho']:6.2f} {q['E_phase']:6.3f}  {q['flag']}")


def tex_row(q):
    num = lambda v, f: (f.format(v) if isinstance(v, (int, float, np.floating)) and np.isfinite(v) else '--')
    return (f"{q['case']} & {q['w_acc']:g} & {q['w_pel']:g} & {q['term']} & {q['w_term']} & "
            f"{q['speed']:g} & {q['N']} & {q['guess']} & {num(q['obj'], '{:.2f}')} & {num(q['COT'], '{:.3f}')} & "
            f"{q['pel']:.2f} & {q['tho']:.2f} & {q['lum']:.2f} & {q['ph_tp']:.1f} & {q['ph_lp']:.1f} & "
            f"{q['E_phase']:.3f} \\\\")


with open(os.path.join('analysis', 'out', 'tableS5_rows.tex'), 'w') as f:
    f.write('\n'.join(tex_row(q) for q in rows) + '\n')
with open(os.path.join('analysis', 'out', 'tableS1_origin_rows.tex'), 'w') as f:
    f.write('\n'.join(tex_row(q) for q in rows if q['term'].startswith('origin')) + '\n')
print(f"\n{len(rows)} cases -> analysis\\out\\case_table.csv, tableS5_rows.tex, tableS1_origin_rows.tex")
print("A_tho = peak-to-peak of thorax first harmonic [deg]; phases in deg (0 in phase, 180 anti-phase).")
print("Rows with a flag need checking against the handover before use.")
