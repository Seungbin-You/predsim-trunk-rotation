"""Lumbar load proxies per case: lumbar joint torques (inverse dynamics) and
trunk muscle forces (DeGroote-Fregly 2016 fiber force from saved a, l, v).
Run from project root:  python analysis\\lumbar_load.py 114 138 160
"""
import numpy as np, sys
R='.'   # run from project root
d=np.load(R+'/Results/optimaltrajectories.npy',allow_pickle=True).item()
mt=np.load(R+'/OpenSimModel/Hamner_modified/Model/mtParameters_Hamner_modified_scaled.npy',allow_pickle=True)
cases=sys.argv[1:]
FLa=[0.814483478343008,1.05503342897057,0.162384573599574,0.0633034484654646,0.433004984392647,0.716775413397760,-0.0299471169706956,0.200356847296188]
FV=[-0.318323436899127,-8.14915604347525,-0.374121508647863,0.885644059915004]
def fl(l):
    b11,b21,b31,b41,b12,b22,b32,b42=FLa
    g=lambda b1,b2,b3,b4: b1*np.exp(-0.5*((l-b2)/(b3+b4*l))**2)
    return g(b11,b21,b31,b41)+g(b12,b22,b32,b42)+g(0.1,1,0.5*np.sqrt(0.5),0)
def fv(v): e1,e2,e3,e4=FV; return e1*np.log((e2*v+e3)+np.sqrt((e2*v+e3)**2+1))+e4
def fp(l): return ((np.exp(4*(l-1)/0.6)-1)-(-0.995172050006169))/53.5981500331442
rms=lambda x: np.sqrt(np.mean(np.asarray(x)**2))
print(f"{'case':>5} | lumbar torque RMS/p2p (Nm): rot | ext | bend || trunk act mean/peak | trunk force sum mean/peak (N) | per side peak  | rot-muscle (obl) force mean")
first=True
for c in cases:
    r=d[c]; J=list(r['joints']); T=np.asarray(r['joint_torques']); M=list(r['muscles'])
    A=np.asarray(r['muscle_activations']); L=np.asarray(r['norm_fiber_lengths']); V=np.asarray(r['fiber_velocity'])
    tr=[i for i,m in enumerate(M) if m[:-2] in ('ercspn','intobl','extobl')]
    if first:
        vmax=mt[4,tr]; print('  check fiber_velocity range', V[tr].min(), V[tr].max(), 'vmax', vmax[:3], 'pennation', mt[3,tr][:3]); first=False
    Fmax=mt[0,tr][:,None]; vn=V[tr]/mt[4,tr][:,None]
    if np.abs(V[tr]).max()<1.2: vn=V[tr]   # already normalized
    F=Fmax*(A[tr]*fl(L[tr])*fv(vn)+0.01*vn+fp(L[tr]))*np.cos(mt[3,tr])[:,None]
    S=F.sum(0); obl=[k for k,i in enumerate(tr) if 'obl' in M[i]]
    tq={j:T[J.index('lumbar_'+j)] for j in ('rotation','extension','bending')}
    print(f"{c:>5} | {rms(tq['rotation']):5.1f}/{np.ptp(tq['rotation']):5.1f} | {rms(tq['extension']):5.1f}/{np.ptp(tq['extension']):5.1f} | {rms(tq['bending']):5.1f}/{np.ptp(tq['bending']):5.1f} || {A[tr].mean():.3f}/{A[tr].max():.3f} | {S.mean():6.0f}/{S.max():6.0f} | {F.max():5.0f} | {F[obl].sum(0).mean():6.0f}")
