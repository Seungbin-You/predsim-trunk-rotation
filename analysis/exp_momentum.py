"""Segmental decomposition of whole-body vertical angular momentum for the
experimental mean kinematics, in the same model as the simulations
(same quantities as segment_momentum.py). Velocities by central differences
(periodic, except pelvis_tx).

Run from project root (env with OpenSim):  python analysis\\exp_momentum.py
"""
import numpy as np, opensim as osim
e=np.load('OpenSimModel/Hamner_modified/experimentalData.npy',allow_pickle=True).item()['Hamner_modified']
df=e['kinematics']['positions']['mean']; t=df['time'].to_numpy(); n=len(t)
T=(t[-1]-t[0])*n/(n-1); dt=T/n
model=osim.Model('OpenSimModel/Hamner_modified/Model/Hamner_modified_scaled.osim'); st=model.initSystem()
M=model.getTotalMass(st); sm=model.getMatterSubsystem()
cs=model.getCoordinateSet(); coords=[cs.get(i) for i in range(cs.getSize())]
bodies=[model.getBodySet().get(i) for i in range(model.getBodySet().getSize())]
grp=lambda nm: 'arms' if nm.startswith(('humerus','ulna','radius','hand')) else nm if nm in ('torso','pelvis') else 'legs'
v3=lambda v: np.array([v.get(0),v.get(1),v.get(2)])
def deriv(x, periodic):
    if periodic: return (np.roll(x,-1)-np.roll(x,1))/(2*dt)
    return np.gradient(x, dt)
Q={}; Qd={}
for c in coords:
    nm=c.getName(); x=df[nm].to_numpy().astype(float)
    tr=c.getMotionType()==osim.Coordinate.Translational
    x = x if tr else np.deg2rad(x)
    Q[nm]=x; Qd[nm]=deriv(x, periodic=(nm!='pelvis_tx'))
speed=(Q['pelvis_tx'][-1]-Q['pelvis_tx'][0])/(t[-1]-t[0])
G=['legs','pelvis','torso','arms']; Lg={g:np.zeros(n) for g in G}; Lt=np.zeros(n)
for k in range(n):
    for c in coords:
        c.setValue(st,Q[c.getName()][k],False); c.setSpeedValue(st,Qd[c.getName()][k])
    model.realizeVelocity(st)
    rG=v3(model.calcMassCenterPosition(st)); vG=v3(model.calcMassCenterVelocity(st))
    for b in bodies:
        m=b.getMass(); cl=b.getMassCenter()
        rb=v3(b.findStationLocationInGround(st,cl)); vb=v3(b.findStationVelocityInGround(st,cl))
        R=np.array([[b.getTransformInGround(st).R().asMat33().get(i,j) for j in range(3)] for i in range(3)])
        I=b.getInertia(); Il=np.diag(v3(I.getMoments())); p=v3(I.getProducts())
        Il[0,1]=Il[1,0]=p[0]; Il[0,2]=Il[2,0]=p[1]; Il[1,2]=Il[2,1]=p[2]
        w=v3(b.getAngularVelocityInGround(st))
        Lg[grp(b.getName())][k]+=(R@Il@R.T@w + m*np.cross(rb-rG,vb-vG))[1]
    mom=sm.calcSystemCentralMomentum(st); a=mom.get(0); Lt[k]=float(a.get(1))
norm=M*speed*1.70; rms=lambda x: np.sqrt(np.mean(x**2))/norm*1e3
c1={g:np.fft.rfft(Lg[g])[1] for g in G}
tot=sum(rms(Lg[g]) for g in G)
print(f"EXP speed {speed:.2f} T {T:.3f} | L RMS {rms(Lt):.2f}e-3 H1 {2*abs(np.fft.rfft(Lt)[1])/n/norm*1e3:.2f}e-3 | sum err {np.max(abs(sum(Lg.values())-Lt))/np.max(abs(Lt)):.1e}")
print("  RMS share (%): "+" ".join(f"{g} {rms(Lg[g])/tot*100:.1f}" for g in G))
print("  leg H1 cancelled by (%): "+" ".join(f"{g} {-np.real(c1[g]*np.conj(c1['legs']))/abs(c1['legs'])**2*100:+.0f}" for g in G[1:])+
      f" | net/legs {abs(sum(c1.values()))/abs(c1['legs'])*100:.0f}% | phase vs legs: "+" ".join(f"{g} {np.degrees(np.angle(c1[g]/c1['legs'])):+.0f}" for g in G[1:]))
print("  H1 amp e-3: "+" ".join(f"{g} {2*abs(c1[g])/n/norm*1e3:.2f}" for g in G))
