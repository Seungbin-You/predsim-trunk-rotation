"""Run from project root (env with OpenSim):  python analysis\\segment_momentum.py 114 138 148

Additive segmental decomposition of whole-body vertical angular momentum about the COM:
L_y = sum_b [ (R_b I_b R_b^T w_b)_y + m_b ((r_b - r_G) x (v_b - v_G))_y ].
Checks that the sum equals OpenSim's calcSystemCentralMomentum."""
import sys, numpy as np, opensim as osim
REPO = '.'; CASES = sys.argv[1:] or ['0', '114', '138']
sys.path.insert(0, REPO); from settings import getSettings
S = getSettings(); H = 1.70
model = osim.Model(REPO + '/OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim')
st = model.initSystem(); Mtot = model.getTotalMass(st); sm = model.getMatterSubsystem()
cs = model.getCoordinateSet(); coords = [cs.get(i) for i in range(cs.getSize())]
bodies = [model.getBodySet().get(i) for i in range(model.getBodySet().getSize())]
names = [b.getName() for b in bodies]
grp = {}
for n in names:
    g = ('arms' if n.startswith(('humerus', 'ulna', 'radius', 'hand')) else
         'torso' if n == 'torso' else 'pelvis' if n == 'pelvis' else 'legs')
    grp[n] = g
v3 = lambda v: np.array([v.get(0), v.get(1), v.get(2)])
def mat33(m): return np.array([[m.get(i, j) for j in range(3)] for i in range(3)])
d = np.load(REPO + '/Results/optimaltrajectories.npy', allow_pickle=True).item()
G = ['legs', 'pelvis', 'torso', 'arms']
print(f"{'case':>5} {'L RMS e-3':>9} {'sumErr':>7} | " + " ".join(f"{g+' RMS':>10}" for g in G) + " | " +
      " ".join(f"{g+' H1':>9}" for g in G) + " | phase of groups vs legs (deg)")
for C in CASES:
    r = d[C]; J = list(r['joints']); q = r['coordinate_values']; qd = r['coordinate_speeds']; nT = q.shape[1]
    norm = Mtot*S[C].get('targetSpeed', 1.33)*H
    Lg = {g: np.zeros(nT) for g in G}; Ltot = np.zeros(nT)
    for k in range(nT):
        for c in coords:
            i = J.index(c.getName()); conv = 1.0 if c.getMotionType() == osim.Coordinate.Translational else np.pi/180
            c.setValue(st, q[i, k]*conv, False); c.setSpeedValue(st, qd[i, k]*conv)
        model.realizeVelocity(st)
        rG = v3(model.calcMassCenterPosition(st)); vG = v3(model.calcMassCenterVelocity(st))
        for b in bodies:
            m = b.getMass()
            if m == 0: continue
            c_loc = b.getMassCenter()
            rb = v3(b.findStationLocationInGround(st, c_loc)); vb = v3(b.findStationVelocityInGround(st, c_loc))
            R = mat33(b.getTransformInGround(st).R().asMat33())
            Ic = b.getInertia(); Iloc = np.diag(v3(Ic.getMoments()))
            p = v3(Ic.getProducts()); Iloc[0,1]=Iloc[1,0]=p[0]; Iloc[0,2]=Iloc[2,0]=p[1]; Iloc[1,2]=Iloc[2,1]=p[2]
            w = v3(b.getAngularVelocityInGround(st))
            L = R @ Iloc @ R.T @ w + m*np.cross(rb - rG, vb - vG)
            Lg[grp[b.getName()]][k] += L[1]
        mom = sm.calcSystemCentralMomentum(st); a = mom.get(0); Ltot[k] = float(a.get(1))
    s = sum(Lg.values()); err = np.max(np.abs(s - Ltot))/np.max(np.abs(Ltot))
    rms = lambda x: np.sqrt(np.mean(x**2))/norm*1e3
    c1 = {g: np.fft.rfft(Lg[g])[1] for g in G}
    print(f"{C:>5} {rms(Ltot):9.2f} {err:7.1e} | " + " ".join(f"{rms(Lg[g]):10.2f}" for g in G) + " | " +
          " ".join(f"{2*abs(c1[g])/nT/norm*1e3:9.2f}" for g in G) + " | " +
          " ".join(f"{g}:{np.degrees(np.angle(c1[g]/c1['legs'])):+.0f}" for g in G[1:]))
    # share of the leg first harmonic cancelled by each group (projection onto -legs)
    canc = {g: -np.real(c1[g]*np.conj(c1['legs']))/abs(c1['legs'])**2*100 for g in G[1:]}
    tot = sum(rms(Lg[g]) for g in G)
    print(f"      RMS share (%): " + " ".join(f"{g} {rms(Lg[g])/tot*100:.1f}" for g in G) +
          " | leg H1 cancelled by (%): " + " ".join(f"{g} {canc[g]:+.0f}" for g in G[1:]) +
          f" | net/legs H1 {abs(sum(c1.values()))/abs(c1['legs'])*100:.0f}%")
