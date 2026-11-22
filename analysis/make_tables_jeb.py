"""Supplementary Tables S4 (additions) and S10-S13 of the JEB manuscript.

Usage (from the repository root):  python analysis/make_tables_jeb.py
Rows: case, condition, speed, stride time, stride length, pelvis/thorax/lumbar ROM,
thorax-pelvis phase (first harmonic), peak stance free moment, COT, objective.
Output: analysis/out/tables_S10_S13.tex, analysis/out/table_S4_additions.tex
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'analysis', 'out')
import numpy as np
D=np.load(os.path.join(ROOT,'Results','optimaltrajectories.npy'),allow_pickle=True).item()
h1=lambda x: np.fft.rfft(np.asarray(x,float)-np.mean(x))[1]
def vals(c):
    r=D[c]; J=list(r['joints']); Q=np.asarray(r['coordinate_values']); g=lambda j:Q[J.index(j)]
    t=np.asarray(r['time']).ravel(); n=len(t); T=t[-1]*n/(n-1)
    pel=g('pelvis_rotation'); lum=g('lumbar_rotation'); tho=pel+lum
    F=np.asarray(r['GRF']); G=np.asarray(r['GRM']); m=min(F.shape[1],Q.shape[1]); fm=0
    for k in (0,3):
        Fv=F[k:k+3,:m]; Mv=G[k:k+3,:m]; Tq=(Mv*Fv).sum(0)/(Fv[1]+10); st=Fv[1]>50; fm=max(fm,np.max(np.abs(Tq[st])))
    v=float(np.squeeze(r.get('targetSpeed', np.nan))) if 'targetSpeed' in r else None
    L=float(r['stride_length'])
    return dict(T=T,L=L,pel=np.ptp(pel),tho=np.ptp(tho),lum=np.ptp(lum),ph=abs(np.degrees(np.angle(h1(tho)/h1(pel)))),FM=fm,COT=float(r['COT']),J=float(np.squeeze(r['objective'])),arm=np.ptp(g('arm_flex_r')))
def row(c,lab,v,extra=None):
    x=vals(c)
    s=f"{c} & {lab} & {v:g} & {x['T']:.3f} & {x['L']:.2f} & {x['pel']:.1f} & {x['tho']:.1f} & {x['lum']:.1f} & {x['ph']:.0f} & {x['FM']:.1f} & {x['COT']:.2f} & {x['J']:.1f}"
    if extra is not None: s+=f" & {extra(x)}"
    return s+r" \\"


HEAD=r"""\centering\footnotesize
\begin{tabular}{@{}rlrrrrrrrrrr@{}}
\toprule
Case & Condition & $v$ & $T$ & $L$ & Pel. & Tho. & Lum. & $\varphi$ & FM & COT & $J$ \\
 & & (m\,s$^{-1}$) & (s) & (m) & (deg) & (deg) & (deg) & (deg) & (N\,m) & (J\,kg$^{-1}$\,m$^{-1}$) & \\
\midrule
"""
FOOT="\\bottomrule\n\\end{tabular}\n\\end{table}\n"
def block(title,items):
    out=[r"\multicolumn{12}{@{}l}{\textit{%s}}\\"%title]+[row(c,l,v) for c,l,v in items]
    return "\n".join(out)+"\n"
def table(label,caption,blocks):
    s="\\begin{table}[!ht]\n\\caption{%s}\n\\label{%s}\n"%(caption,label)+HEAD
    s+="\\addlinespace\n".join(block(t,i) for t,i in blocks)
    return s+FOOT
V=[0.8,1.0,1.33,1.45,1.6]
s4_add = ("\\addlinespace\n"+block('TR+C (without AM)',[(c,'TR+C',v) for c,v in zip(['383','384','214','385','386'],V)]),
          row('391','TR+C+AM',1.52))
S10=table('tab:S10',r"Speed dependence of pelvic rotation (nominal model). C only, imposed stride time; sweep, stride time varied at 1.6\,m\,s$^{-1}$ (0.931, 0.970, 1.000 and 1.040\,s); scaled $w_\mathrm{acc}$, joint-acceleration weight scaled so that its penalty on a given amplitude of rotation equals that at 1.33\,m\,s$^{-1}$; scaled $w_\mathrm{AM}$, $w_\mathrm{AM} = 3(1.33/v)^2$.",
 [('C only',[(c,'C',v) for c,v in zip(['252','253','212','254','255'],V)]+[('372','C, from 296',1.6)]),
  ('C, stride-time sweep at 1.6\\,m\\,s$^{-1}$',[('372','$T$ 0.931',1.6),('378','$T$ 0.970',1.6),('373','$T$ 1.000',1.6),('374','$T$ 1.040',1.6)]),
  ('Scaled $w_\\mathrm{acc}$',[('375','C, $w_\\mathrm{acc}$ 39\\,000',1.6),('376','TR+C+AM, $w_\\mathrm{acc}$ 39\\,000',1.6),('377','TR+C+AM, $w_\\mathrm{acc}$ 44\\,500',1.45)]),
  ('TR+C+AM at 1.6\\,m\\,s$^{-1}$, other initial guess',[('321','TR+C+AM, exp. guess',1.6)]),
  ('Scaled $w_\\mathrm{AM}$ (TR+C+AM)',[('379','$w_\\mathrm{AM}$ 8.29',0.8),('380','$w_\\mathrm{AM}$ 5.31',1.0),('381','$w_\\mathrm{AM}$ 2.52',1.45),('382','$w_\\mathrm{AM}$ 2.07',1.6)]),
  ('Factor combinations at other speeds',[('387','C+AM',1.0),('388','TR+AM',1.0),('389','C+AM',1.45),('390','TR+AM',1.45)])])
S11=table('tab:S11',r"Robustness of TR+C+AM at 1.33\,m\,s$^{-1}$ (nominal model): torsional resistance at one joint only, lumbar rotation spring, and weight of the arm actuators ($w_4$, factor relative to nominal). The tenfold arm weight was solved from three initial guesses (395, from 302; 401, continuation from 400; 402, from the arms-locked solution 303).",
 [('Torsional resistance and lumbar spring',[('302','TR+C+AM',1.33),('392','TR hip only +C+AM',1.33),('393','TR subtalar only +C+AM',1.33),('397','TR+C+AM, lumbar 20\\,N\\,m\\,rad$^{-1}$',1.33),('398','TR+C+AM, lumbar 50\\,N\\,m\\,rad$^{-1}$',1.33)]),
  ('Arm actuator weight, TR+C+AM',[('394','$w_4\\times0.1$',1.33),('302','$w_4\\times1$',1.33),('399','$w_4\\times2$',1.33),('400','$w_4\\times4$',1.33),('395','$w_4\\times10$',1.33),('401','$w_4\\times10$',1.33),('402','$w_4\\times10$',1.33)]),
  ('Arm actuator weight, TR+C (without AM)',[('396','$w_4\\times0.1$',1.33),('214','$w_4\\times1$',1.33),('403','$w_4\\times10$',1.33)])])
S12=table('tab:S12',r"Arm-matched model ($w_4\times2$) at 1.33\,m\,s$^{-1}$: factorial design, angular momentum weight, free-moment tests and the energetic analysis (penalty $w_\mathrm{pel}$ on pelvic rotation).",
 [('Factorial',[('404','none',1.33),('405','TR',1.33),('406','C',1.33),('407','TR+C',1.33),('408','AM',1.33),('409','TR+AM',1.33),('410','C+AM',1.33),('399','TR+C+AM',1.33)]),
  ('TR+C, $w_\\mathrm{AM}$',[('407','0',1.33),('429','1',1.33),('399','3',1.33),('430','10',1.33),('431','30',1.33)]),
  ('Free moment',[('432','TR+FM+C+AM',1.33),('433','TR+FM+C',1.33)]),
  ('Effort-minimising, $w_\\mathrm{pel}$',[('404','0',1.33),('434','1000',1.33),('435','3000',1.33),('436','10\\,000',1.33),('437','30\\,000',1.33)])])
S13=table('tab:S13',r"Arm-matched model ($w_4\times2$): walking speed.",
 [('Effort-minimising',[(c,'none',v) for c,v in zip(['411','412','404','413','414'],V)]),
  ('TR+C (without AM)',[(c,'TR+C',v) for c,v in zip(['425','426','407','427','428'],V)]),
  ('C+AM',[(c,'C+AM',v) for c,v in zip(['420','421','410','422','423','424'],[0.8,1.0,1.33,1.45,1.52,1.6])]),
  ('TR+C+AM',[(c,'TR+C+AM',v) for c,v in zip(['415','416','399','417','418','419'],[0.8,1.0,1.33,1.45,1.52,1.6])])])
os.makedirs(OUT,exist_ok=True)
open(os.path.join(OUT,'tables_S10_S13.tex'),'w').write(S10+"\n"+S11+"\n"+S12+"\n"+S13)
open(os.path.join(OUT,'table_S4_additions.tex'),'w').write(s4_add[0]+"\n"+s4_add[1]+"\n")
print('written to', OUT)
