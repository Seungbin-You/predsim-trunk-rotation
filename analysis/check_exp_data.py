# analysis/check_exp_data.py
import numpy as np, glob
hits = glob.glob('**/experimentalData.npy', recursive=True)
print("found:", hits)
d = np.load(hits[0], allow_pickle=True).item()

print("keys:", list(d.keys()))
k = list(d.keys())[0]
print("categories:", list(d[k].keys()))
p = d[k]['kinematics']['positions']
print("joints:", list(p['mean'].keys()))

for j in ['pelvis_rotation', 'lumbar_rotation', 'lumbar_bending', 'lumbar_extension']:
    if j not in p['mean']:
        print(f"{j}: (없음)"); continue
    m, s = np.asarray(p['mean'][j]), np.asarray(p['std'][j])
    print(f"{j:18s} ROM(mean) = {np.ptp(m):6.2f} deg   "
          f"mean range = {m.min():+6.2f} ~ {m.max():+6.2f}   "
          f"평균 SD = {s.mean():5.2f}")


p = d['Hamner_modified']['kinematics']['positions']
pel = np.asarray(p['mean']['pelvis_rotation'])
lum = np.asarray(p['mean']['lumbar_rotation'])
tho = pel + lum

print(f"\n[experimental]")
print(f"pelvis ROM  : {np.ptp(pel):6.2f}")
print(f"thorax ROM  : {np.ptp(tho):6.2f}")
print(f"lumbar ROM  : {np.ptp(lum):6.2f}")
r = np.corrcoef(pel-pel.mean(), tho-tho.mean())[0,1]
print(f"pelvis-thorax corr : {r:+.3f}")

n = len(pel)
xc = np.correlate(pel-pel.mean(), tho-tho.mean(), 'full')
print(f"lag : {(np.argmax(xc)-(n-1))/n*100:+.1f} % of cycle")


# 실측 대비 정규화 오차
targets = {'pelvis': 6.38, 'thorax': 11.70, 'lumbar': 14.78, 'corr': -0.044}

def agreement(case):
    r = d[case]; j = list(r['joints']); q = r['coordinate_values']
    pel = q[j.index('pelvis_rotation'),:]; lum = q[j.index('lumbar_rotation'),:]
    tho = pel + lum
    e_pel = abs(np.ptp(pel)-targets['pelvis'])/targets['pelvis']
    e_tho = abs(np.ptp(tho)-targets['thorax'])/targets['thorax']
    e_lum = abs(np.ptp(lum)-targets['lumbar'])/targets['lumbar']
    corr  = np.corrcoef(pel-pel.mean(), tho-tho.mean())[0,1]
    e_cor = abs(corr-targets['corr'])/2
    return e_pel, e_tho, e_lum, e_cor, (e_pel+e_tho+e_lum+e_cor)/4


print(d['Hamner_modified'].keys())
print(d['Hamner_modified']['kinematics'].keys())
print(d['Hamner_modified']['GRF'].keys())