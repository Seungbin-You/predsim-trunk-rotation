"""
Data figures for the J Exp Biol (Theory & Modelling) version of the manuscript.
Fig. 1 (model / objective schematic) is drawn separately.

Run from project root:   python analysis\\make_figures_paper.py [output_dir]
Output (default 'figures'):  fig2_overrotation, fig3_mechanism, fig4_constraints,
                                  fig5_coordination, fig6_speed  (.pdf + .png)

Journal style: Arial, 6-8 pt text, upper-case bold panel letters, colour-blind-safe
(Okabe-Ito) palette with redundant line style / marker, width <= 180 mm.
Every simulated condition is a single deterministic optimum (N = 1).

Case map (see settings.py / handover.md)
  w_acc sweep (no constraints) .... 61 83 82 60 81 80 0 84  (500 ... 100 000)
  pelvis-rotation suppression ..... continuation sweeps 0/90/275/91/276/92/277 (nominal),
                                    82/278/279/280/281/282 (w_acc 2000); pairs 0->91, 0->92, 82->281
  2x2x2 factorial, w_acc 50 000 ... 0, A 203, B 213, C 212, AB 198, AC 214, BC 215, ABC 211
                    w_acc 10 000 ... 0 81, A 232, B 233, C 234, ABC 235
                    w_acc  1 000 ... 0 83, A 228, B 229, C 230, ABC 231
  ABC + angular-momentum term ..... 216 (w_acc 50 000), 220 (30 000), 221 (22 000), 217 (15 000)
  free-moment term dose (on 221) .. 223 (0), 221 (1), 224 (10), 225 (100)
  speed 0.8/1.0/1.33/1.45/1.6 ..... baseline 294 24 0 292 296 (lowest-cost after cross-speed warm starts)
                                    | ABC 236 237 211 244 301
                                    ABC+AM 239 240 216 245 246
  speed hypotheses (optional) ..... H1 w_acc 10 000: 248 249 81 250 251
                                    H2 C only:      252 253 212 254 255
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

RES = 'Results/optimaltrajectories.npy'
EXP = 'OpenSimModel/Hamner_modified/experimentalData.npy'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'figures'
os.makedirs(OUT, exist_ok=True)
d = np.load(RES, allow_pickle=True).item()
E = np.load(EXP, allow_pickle=True).item()['Hamner_modified']

# ── style ───────────────────────────────────────────────────────────────
# Okabe-Ito; validated (no adjacent pair below dE 7.6 under deutan) - every
# series also differs in line style or marker, so colour is never the only cue.
C0, CA, CB, CC = '#0072B2', '#E69F00', '#009E73', '#CC79A7'   # baseline, ABC, ABC+AM, extra
CV, CS = '#D55E00', '#56B4E9'                                  # vermillion, sky blue (factor / pair colours)
INK, MUTED, BAND = '#000000', '#6b6b6b', '#d9d9d9'
MM = 1 / 25.4
W1, W15, W2 = 85 * MM, 114 * MM, 180 * MM
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Liberation Sans', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7, 'axes.titlesize': 7, 'axes.labelsize': 7,
    'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'legend.fontsize': 6.5,
    'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': False,
    'lines.linewidth': 1.2, 'lines.markersize': 4,
    'legend.frameon': False, 'legend.handlelength': 2.0,
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'savefig.dpi': 600,
    'mathtext.default': 'regular',   # math (subscripts) in the text font, no DejaVu fallback
})


def save(fig, name):
    for ext, dpi in (('pdf', None), ('png', 300)):
        fig.savefig(os.path.join(OUT, '%s.%s' % (name, ext)), bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    print('saved', name)


def letter(ax, s, dx=-0.16, dy=1.04):
    ax.text(dx, dy, s, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom', ha='right')


def have(*cs):
    return all(c in d for c in cs)


# ── metrics ─────────────────────────────────────────────────────────────
def h1(x):
    x = np.asarray(x, float).ravel()
    return np.fft.rfft(x - x.mean())[1]


def ph(x, y):
    """Phase of x relative to y at the stride frequency (deg, -180..180)."""
    return float(np.degrees(np.angle(h1(x) / h1(y))))


def Q(c, j):
    r = d[c]
    return np.asarray(r['coordinate_values'])[list(r['joints']).index(j)]


def Qd(c, j):
    r = d[c]
    return np.asarray(r['coordinate_speeds'])[list(r['joints']).index(j)]


def T(c, j):
    r = d[c]
    return np.asarray(r['joint_torques'])[list(r['joints']).index(j)]


def gc(c):
    return np.asarray(d[c]['GC_percent'], float).ravel()


def stride_time(c):
    t = np.asarray(d[c]['time'], float).ravel()
    return (t[-1] - t[0]) * t.size / (t.size - 1)


def free_moment(c):
    """Free (torsional) moment about the vertical, right foot, stance only (N m)."""
    F, G = np.asarray(d[c]['GRF']), np.asarray(d[c]['GRM'])
    Tz = (G[0] * F[0] + G[1] * F[1] + G[2] * F[2]) / (F[1] + 10)
    return Tz[F[1] > 20]


def M(c):
    pel, lum = Q(c, 'pelvis_rotation'), Q(c, 'lumbar_rotation')
    tho = pel + lum
    fm = free_moment(c)
    return dict(pel=np.ptp(pel), tho=np.ptp(tho), lum=np.ptp(lum),
                tp=abs(ph(tho, pel)), lp=abs(ph(lum, pel)),
                ph_hip=ph(pel, Q(c, 'hip_flexion_r')),
                cot=float(d[c]['COT']), fm_peak=np.abs(fm).max(), fm_rms=np.sqrt(np.mean(fm ** 2)),
                stride=float(d[c]['stride_length']), T=stride_time(c))


# experiment (Hamner et al. 2010 data set, same model)
kin = E['kinematics']['positions']
gcE = np.asarray(kin['GC_percent'], float).ravel()
pelE, lumE = np.asarray(kin['mean']['pelvis_rotation']), np.asarray(kin['mean']['lumbar_rotation'])
sdP, sdL = np.asarray(kin['std']['pelvis_rotation']), np.asarray(kin['std']['lumbar_rotation'])
choE = pelE + lumE
kinT = E['kinetics']
gcT = np.asarray(kinT['GC_percent'], float).ravel()
mE = dict(pel=np.ptp(pelE), tho=np.ptp(choE), lum=np.ptp(lumE), tp=abs(ph(choE, pelE)),
          lp=abs(ph(lumE, pelE)))
print('EXP check: pelvis %.2f thorax %.2f lumbar %.2f deg, tho-pel %.1f deg (6.38/11.70/14.78, 95.8)'
      % (mE['pel'], mE['tho'], mE['lum'], mE['tp']))

# Lamoth et al. (2002) Gait Posture 16:101, Table 3 (RFP, 10 subjects, treadmill)
LAM_V = np.array([1.4, 2.2, 3.0, 3.8, 4.6, 5.4]) / 3.6
LAM = np.array([[3, 7, 47, 151, 165, 142], [107, 128, 175, 160, 179, 166], [51, 22, 20, 71, 134, 136],
                [1, 1, 3, 11, 137, 129], [7, 12, 4, 4, 153, 172], [35, 42, 75, 87, 92, 102],
                [4, 7, 16, 121, 145, 162], [3, 21, 42, 140, 149, 166], [1, 15, 22, 144, 164, 168],
                [5, 11, 4, 162, 148, 169]], float)


def exp_line(ax, y, **kw):
    ax.axhline(y, color=INK, lw=0.8, ls=(0, (3, 2)), zorder=1, **kw)


# ═══ Fig. 2 — the effort-minimising solution over-rotates ════════════════
def fig2():
    fig = plt.figure(figsize=(W2, 95 * MM))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], hspace=0.65, wspace=0.42)
    titles = ['Pelvis', 'Thorax (pelvis + lumbar)', 'Lumbar (thorax re pelvis)']
    ys = [(pelE, sdP), (choE, None), (lumE, sdL)]
    mod = [Q('0', 'pelvis_rotation'), Q('0', 'pelvis_rotation') + Q('0', 'lumbar_rotation'),
           Q('0', 'lumbar_rotation')]
    for k in range(3):
        ax = fig.add_subplot(gs[0, k])
        m, s = ys[k]
        if s is not None:
            ax.fill_between(gcE, m - s, m + s, color=BAND, lw=0, zorder=0)
        ax.plot(gcE, m, color=INK, ls=(0, (3, 2)), lw=1.0, label='Human (mean ± s.d.)')
        ax.plot(gc('0'), mod[k], color=C0, label='Model, effort-minimising')
        ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xlabel('Gait cycle (%)')
        ax.set_title(titles[k], loc='left')
        if k == 0:
            ax.set_ylabel('Axial rotation (deg)')
            fig.legend(*ax.get_legend_handles_labels(), loc='upper center', ncol=2,
                       bbox_to_anchor=(0.5, 1.03))
        letter(ax, 'ABC'[k])
    # weight sweep
    sweep = [('61', 500), ('83', 1000), ('82', 2000), ('60', 5000), ('81', 10000),
             ('80', 25000), ('0', 50000), ('84', 100000)]
    sweep = [(c, w) for c, w in sweep if c in d]
    w = np.array([s[1] for s in sweep]); ms = [M(c) for c, _ in sweep]
    ax = fig.add_subplot(gs[1, 0:2])
    for key, col, mk, ls, lab in [('pel', C0, 'o', '-', 'Pelvis'), ('tho', CB, 's', '--', 'Thorax')]:
        ax.plot(w, [m[key] for m in ms], color=col, marker=mk, ls=ls, label=lab, zorder=3)
        ax.axhline(mE[key], color=col, lw=0.7, ls=':', zorder=1)
        ax.text(w[0], mE[key] + (-0.6 if key == 'tho' else 0.5), 'human ' + lab.lower(), color=col,
                fontsize=6, ha='left', va='bottom' if key == 'pel' else 'top')
    ax.set_xscale('log'); ax.axvline(50000, color=MUTED, lw=0.5, zorder=0)
    ax.text(50000, ax.get_ylim()[1] if False else 1.0, ' nominal', fontsize=6, color=MUTED, va='bottom',
            transform=ax.get_xaxis_transform())
    ax.set_xlabel(r'Joint-acceleration weight, $w_\mathrm{acc}$')
    ax.set_ylabel('Range of motion (deg)'); ax.set_ylim(0, None)
    ax.legend(loc='upper right', ncol=2)
    letter(ax, 'D', dx=-0.075)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(w, [m['cot'] for m in ms], color=C0, marker='o')
    ax.set_xscale('log'); ax.axvline(50000, color=MUTED, lw=0.5, zorder=0)
    ax.set_xlabel(r'$w_\mathrm{acc}$'); ax.set_ylabel(r'COT (J kg$^{-1}$ m$^{-1}$)')
    letter(ax, 'E', dx=-0.25)
    save(fig, 'fig2_overrotation')


# ═══ Fig. 3 — where the benefit of pelvic rotation comes from ═══════════
GROUPS = [('Gluteus maximus', ('glut_max',)),
          ('Hip abductors', ('glut_med', 'glut_min', 'tfl')),
          ('Hip adductors', ('add_', 'grac', 'pect')),
          ('Deep rotators', ('quad_fem', 'gem', 'peri')),
          ('Hamstrings', ('semimem', 'semiten', 'bifem')),
          ('Hip flexors', ('iliacus', 'psoas', 'sar')),
          ('Quadriceps', ('rect_fem', 'vas_')),
          ('Plantarflexors', ('med_gas', 'lat_gas', 'soleus', 'tib_post', 'flex_', 'per_')),
          ('Dorsiflexors', ('tib_ant', 'ext_')),
          ('Trunk', ('ercspn', 'intobl', 'extobl'))]


def group_cot(c):
    mus = list(d[c]['muscles']); v = np.asarray(d[c]['COT_perMuscle'], float).ravel()
    out, used = [], np.zeros(len(mus), bool)
    for _, pre in GROUPS:
        sel = np.array([any(m.startswith(p) for p in pre) for m in mus])
        used |= sel; out.append(v[sel].sum())
    out.append(v[~used].sum())
    return np.array(out)


def stance_work(c, joint):
    """Positive work of joint (right side) during right stance, per metre (J m-1)."""
    F = np.asarray(d[c]['GRF']); st = F[1] > 20
    P = T(c, joint) * np.radians(Qd(c, joint))        # coordinate speeds are stored in deg s-1
    dt = stride_time(c) / P.size
    return np.sum(np.clip(P[st], 0, None)) * dt / float(d[c]['stride_length'])


CURVES = [  # pelvisRotTerm continuation sweeps (w_pel: case)
    ('Nominal objective', C0, 'o', '-', [('0', 0), ('90', 100), ('275', 300), ('91', 1000), ('276', 3000),
                                         ('92', 10000), ('277', 30000)]),
    (r'Energy-weighted ($w_\mathrm{acc}$ 2000)', CA, 's', '--',
     [('82', 0), ('278', 100), ('279', 300), ('280', 1000), ('281', 3000), ('282', 10000)])]
HUMAN_RANGE = (6.0, 13.0)   # overground adult pelvis transverse ROM (Thompson et al. 2015; this data set)


def fig3():
    pairs = [('91', '0', r'$w_\mathrm{pel}$ 1000', CS, '--'),
             ('92', '0', r'$w_\mathrm{pel}$ 10 000', CV, ':'),
             ('281', '82', r'$w_\mathrm{pel}$ 3000, $w_\mathrm{acc}$ 2000', CC, '-.')]
    pairs = [p for p in pairs if have(p[0], p[1])]
    fig = plt.figure(figsize=(W2, 120 * MM))
    gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.55, width_ratios=[1, 1.15])
    # A: cost of restricting pelvic rotation
    ax = fig.add_subplot(gs[0, 0]); ax2 = fig.add_subplot(gs[0, 1])
    for lab, col, mk, ls, cs in CURVES:
        cs = [(c, w) for c, w in cs if c in d]
        if not cs:
            continue
        x = [M(c)['pel'] for c, _ in cs]; c0 = M(cs[0][0])['cot']
        ax.plot(x, [100 * (M(c)['cot'] / c0 - 1) for c, _ in cs], color=col, marker=mk, ls=ls, label=lab)
        ax2.plot(x, [stance_work(c, 'hip_adduction_r') for c, _ in cs], color=col, marker=mk, ls=ls, label=lab)
    for a_ in (ax, ax2):
        a_.axvspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
        a_.axvline(mE['pel'], color=INK, lw=0.8, ls=(0, (3, 2)), zorder=1)
        a_.set_xlabel('Pelvis range of motion (deg)'); a_.set_xlim(0, 30)
    ax.text(np.mean(HUMAN_RANGE), 0.03, 'human\nrange', transform=ax.get_xaxis_transform(), ha='center',
            va='bottom', fontsize=5.8, color=MUTED)
    ax.set_ylabel('Change in cost of transport (%)'); ax.set_ylim(bottom=-0.2)
    ax.legend(loc='upper right', fontsize=5.8)
    ax.set_title('Cost of restricting pelvic rotation', loc='left')
    letter(ax, 'A', dx=-0.2)
    ax2.set_ylabel('Hip ab/adduction positive\nstance work (J m$^{-1}$)')
    ax2.set_title('Stance hip frontal-plane work', loc='left')
    letter(ax2, 'B', dx=-0.2)
    # C: change in metabolic cost by muscle group
    ax = fig.add_subplot(gs[1, 0])
    names = [g[0] for g in GROUPS]
    y = np.arange(len(names)); hgt = 0.8 / len(pairs)
    for i, (c, r, lab, col, _) in enumerate(pairs):
        g0 = group_cot(r)
        dv = (100 * (group_cot(c) - g0) / g0.sum())[:len(names)]
        ax.barh(y + (i - (len(pairs) - 1) / 2) * hgt, dv, height=hgt * 0.9, color=col,
                label='%s: %.0f→%.0f deg' % (lab, M(r)['pel'], M(c)['pel']))
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=6); ax.invert_yaxis()
    ax.set_xlabel('Change in metabolic cost (% of reference total)')
    ax.legend(loc='upper center', bbox_to_anchor=(0.4, -0.22), fontsize=5.8)
    letter(ax, 'C', dx=-0.5)
    # D: hip abduction moment (nominal objective)
    ax = fig.add_subplot(gs[1, 1])
    tE = np.asarray(kinT['mean']['hip_adduction_r']); sE = np.asarray(kinT['std']['hip_adduction_r'])
    ax.fill_between(gcT, -(tE - sE), -(tE + sE), color=BAND, lw=0)
    ax.plot(gcT, -tE, color=INK, ls=(0, (3, 2)), lw=1.0, label='Human')
    ax.plot(gc('0'), -T('0', 'hip_adduction_r'), color=C0, label='Unrestricted')
    for c, r, lab, col, ls in pairs:
        if r == '0':
            ax.plot(gc(c), -T(c, 'hip_adduction_r'), color=col, ls=ls, label=lab)
    ax.set_xlim(0, 100); ax.set_xticks([0, 20, 40, 60, 80, 100]); ax.set_ylim(-20, 95)
    ax.set_xlabel('Gait cycle (%)'); ax.set_ylabel('Hip abduction moment (N m)')
    ax.set_title('Nominal objective', loc='left')
    ax.legend(loc='upper right', fontsize=5.8, handlelength=1.6, ncol=2, columnspacing=0.8,
              bbox_to_anchor=(1.03, 1.02))
    letter(ax, 'D', dx=-0.2)
    save(fig, 'fig3_mechanism')


# ═══ Fig. 4 — candidate factors (2x2x2: TR, C, AM) ══════════════════════
# Factor labels: TR passive torsional resistance (hip rotation + subtalar springs, 50 N m rad-1),
# C human stride time, AM vertical angular-momentum-rate cost, FM free-moment cost.
FACT = [('0', 'none'), ('203', 'TR'), ('212', 'C'), ('214', 'TR+C'),
        ('328', 'AM'), ('329', 'TR+AM'), ('330', 'C+AM'), ('302', 'TR+C+AM')]
SPEEDS = [0.8, 1.0, 1.33, 1.45, 1.6]
SP_BASE = ['294', '24', '0', '292', '296']          # effort-minimising solution
SP_TCA = ['316', '318', '302', '320', '322']        # TR + C + AM (main condition)
SP_TCFA = ['239', '240', '216', '245', '246']       # TR + FM + C + AM
SP_TFC = ['236', '237', '211', '244', '301']        # TR + FM + C (earlier factorial, Supplementary)
SP_TC = ['383', '384', '214', '385', '386']         # TR + C without AM (cross-speed check)
SPEEDS6 = [0.8, 1.0, 1.33, 1.45, 1.52, 1.6]
SP_TCA6 = ['316', '318', '302', '320', '391', '322']  # TR + C + AM incl. 1.52 m/s
CTC = '#E69F00'                                     # TR + C colour (orange)
FM_HUMAN = (3.4, 1.4)                               # peak free moment, Almosnino et al. (2009)
CT = '#009E73'                                      # TR + C + AM colour (= CB)


def _fact_bars(ax, key, ylab, ylim):
    f = [(c, l) for c, l in FACT if c in d]
    v = [M(c)[key] for c, _ in f]
    for i, (c, l) in enumerate(f):
        am = 'AM' in l
        col = CT if l == 'TR+C+AM' else (C0 if l == 'none' else ('#7fbfa9' if am else '#9db8cf'))
        ax.bar(i, v[i], width=0.72, color=col, edgecolor='white', lw=0, hatch='////' if am else None)
    ax.set_xticks(range(len(f)))
    ax.set_xticklabels([l.replace('+', '+\n') for _, l in f], fontsize=5.6)
    ax.set_ylabel(ylab); ax.set_ylim(*ylim)
    ax.axvline(3.5, color=MUTED, lw=0.5, ls=':')
    return f, v


def fig4():
    fig = plt.figure(figsize=(W2, 112 * MM))
    gs = fig.add_gridspec(2, 2, hspace=0.62, wspace=0.32)
    # A pelvis ROM
    ax = fig.add_subplot(gs[0, 0])
    f, v = _fact_bars(ax, 'pel', 'Pelvis range of motion (deg)', (0, 23))
    ax.axhspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    exp_line(ax, mE['pel'])
    cot0 = M('0')['cot']
    for i, (c, _) in enumerate(f):
        if c != '0':
            ax.text(i, v[i] + 0.4, '%+.1f%%' % (100 * (M(c)['cot'] / cot0 - 1)), ha='center',
                    fontsize=5.2, color=MUTED, rotation=90, va='bottom')
    ax.set_title('Bar labels: change in cost of transport', loc='right', fontsize=5.5, color=MUTED)
    letter(ax, 'A', dx=-0.1)
    # B thorax-pelvis phase
    ax = fig.add_subplot(gs[0, 1])
    _fact_bars(ax, 'tp', 'Thorax–pelvis phase (deg)', (0, 185))
    ax.set_yticks([0, 45, 90, 135, 180])
    exp_line(ax, mE['tp'])
    letter(ax, 'B', dx=-0.12)
    # C peak free moment
    ax = fig.add_subplot(gs[1, 0])
    _fact_bars(ax, 'fm_peak', 'Peak free moment (N m)', (0, 7))
    ax.axhspan(FM_HUMAN[0] - FM_HUMAN[1], FM_HUMAN[0] + FM_HUMAN[1], color=BAND, lw=0, zorder=0)
    exp_line(ax, FM_HUMAN[0])
    ax.text(7.45, FM_HUMAN[0] + FM_HUMAN[1] + 0.15, 'human: Almosnino et al. (2009)', ha='right', fontsize=5.3, color=MUTED)
    letter(ax, 'C', dx=-0.1)
    # D is a free-moment cost needed once AM is present? (five speeds)
    ax = fig.add_subplot(gs[1, 1])
    for cs, sp, col, mk, ls, lab in [(SP_BASE, SPEEDS, C0, 'o', '-', 'no factor'),
                                     (SP_TCFA, SPEEDS, CC, 's', ':', 'TR+FM+C+AM'),
                                     (SP_TCA6, SPEEDS6, CT, 'D', '--', 'TR+C+AM')]:
        pts = [(s_, M(c)['pel']) for s_, c in zip(sp, cs) if c in d]
        ax.plot(*zip(*pts), color=col, marker=mk, ls=ls, label=lab)
    ax.axhspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    ax.plot(1.33, mE['pel'], marker='*', ms=8, color=INK, ls='none', label='human (this data set)')
    ax.set_xlabel(r'Walking speed (m s$^{-1}$)'); ax.set_ylabel('Pelvis range of motion (deg)')
    ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6]); ax.set_ylim(0, 30)
    ax.legend(loc='upper left', fontsize=5.8, ncol=2, columnspacing=1.0)
    letter(ax, 'D', dx=-0.12)
    handles = [plt.Rectangle((0, 0), 1, 1, color='#9db8cf'), plt.Rectangle((0, 0), 1, 1, color='#7fbfa9', hatch='////', ec='white', lw=0),
               plt.Rectangle((0, 0), 1, 1, color=BAND), Line2D([], [], color=INK, lw=0.8, ls=(0, (3, 2)))]
    fig.legend(handles, ['without AM', 'with AM', 'human range', 'human (this data set)'], loc='upper center',
               ncol=4, bbox_to_anchor=(0.5, 1.02))
    save(fig, 'fig4_factors')


# ═══ Fig. 5 — trunk coordination ════════════════════════════════════════
AM_DOSE = [('214', 0), ('369', 1), ('302', 3), ('370', 10), ('371', 30)]
WACC_TCA = [('302', 50000), ('326', 10000), ('327', 1000)]
LOCKS = [('302', 'free'), ('303', 'arms\nlocked'), ('304', 'lumbar\nlocked'), ('305', 'both\nlocked')]


def fig5():
    fig = plt.figure(figsize=(W2, 100 * MM))
    gs = fig.add_gridspec(2, 3, hspace=0.62, wspace=0.45)
    sets = [('214', 'TR+C', CA, '-'), ('302', 'TR+C+AM', CT, '--')]
    for k, (key, title) in enumerate([('pel', 'Pelvis'), ('tho', 'Thorax')]):
        ax = fig.add_subplot(gs[0, k])
        m = pelE if key == 'pel' else choE
        if key == 'pel':
            ax.fill_between(gcE, m - sdP, m + sdP, color=BAND, lw=0)
        ax.plot(gcE, m, color=INK, ls=(0, (3, 2)), lw=1.0, label='Human')
        for c, lab, col, ls in sets:
            y = Q(c, 'pelvis_rotation') + (Q(c, 'lumbar_rotation') if key == 'tho' else 0)
            ax.plot(gc(c), y, color=col, ls=ls, label=lab)
        ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xlabel('Gait cycle (%)')
        ax.set_title(title, loc='left'); ax.set_ylabel('Axial rotation (deg)')
        letter(ax, 'AB'[k])
    ax = fig.add_subplot(gs[0, 2])
    tE = np.asarray(kinT['mean']['lumbar_rotation']); sE = np.asarray(kinT['std']['lumbar_rotation'])
    ax.fill_between(gcT, tE - sE, tE + sE, color=BAND, lw=0)
    ax.plot(gcT, tE, color=INK, ls=(0, (3, 2)), lw=1.0, label='Human (mean ± s.d.)')
    for c, lab, col, ls in sets:
        ax.plot(gc(c), T(c, 'lumbar_rotation'), color=col, ls=ls, label=lab)
    ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xlabel('Gait cycle (%)')
    ax.set_title('Lumbar axial moment', loc='left'); ax.set_ylabel('Moment (N m)')
    fig.legend(*ax.get_legend_handles_labels(), loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.02))
    letter(ax, 'C')
    # D AM weight dose (main condition)
    ax = fig.add_subplot(gs[1, 0])
    dd = [(c, w) for c, w in AM_DOSE if c in d]
    xs = [max(w, 0.3) for _, w in dd]
    ax.plot(xs, [M(c)['tp'] for c, _ in dd], color=CT, marker='D', ls='--', label='thorax–pelvis phase')
    exp_line(ax, mE['tp'])
    ax.set_xscale('log'); ax.set_xticks([0.3, 1, 3, 10, 30]); ax.set_xticklabels(['0', '1', '3', '10', '30'])
    ax.set_xlabel(r'$w_\mathrm{AM}$'); ax.set_ylabel('Thorax–pelvis phase (deg)')
    ax.set_ylim(-22, 185); ax.set_yticks([0, 45, 90, 135, 180])
    for x_, (c, _) in zip(xs, dd):   # pelvis ROM as labels (one y-axis only)
        ax.annotate('%.1f°' % M(c)['pel'], (x_, M(c)['tp']),
                    xytext=((8, -3) if M(c)['tp'] < 10 else (7, -3)) if M(c)['tp'] < 60 else (-4, 7), ha='left' if M(c)['tp'] < 60 else 'right',
                    textcoords='offset points', fontsize=5.3, color=MUTED)
    ax.set_title('Varying AM weight (TR+C)', loc='left')
    ax.minorticks_off()
    letter(ax, 'D')
    # E joint-acceleration weight
    ax = fig.add_subplot(gs[1, 1])
    for c, w in [(c, w) for c, w in WACC_TCA if c in d]:
        m = M(c)
        ax.plot(m['pel'], m['tp'], marker='D', color=CT, ls='none')
        ax.annotate(r'$w_\mathrm{acc}$ = %gk' % (w / 1000), (m['pel'], m['tp']),
                    xytext=(4, 3) if w >= 50000 else (-5, -9), ha='left' if w >= 50000 else 'right',
                    textcoords='offset points', fontsize=5.5)
    ax.plot(mE['pel'], mE['tp'], marker='*', ms=8, color=INK, ls='none')
    ax.annotate('human', (mE['pel'], mE['tp']), xytext=(-4, -10), ha='right', textcoords='offset points', fontsize=6)
    ax.set_xlabel('Pelvis range of motion (deg)'); ax.set_ylabel('Thorax–pelvis phase (deg)')
    ax.set_ylim(0, 185); ax.set_yticks([0, 45, 90, 135, 180]); ax.set_xlim(0, 16)
    ax.set_title(r'TR+C+AM, varying $w_\mathrm{acc}$', loc='left')
    letter(ax, 'E')
    # F locking arms / lumbar rotation
    ax = fig.add_subplot(gs[1, 2])
    lk = [(c, l) for c, l in LOCKS if c in d]
    x = np.arange(len(lk))
    ax.bar(x, [M(c)['tp'] for c, _ in lk], width=0.7, color=CT)
    exp_line(ax, mE['tp'])
    ax.set_xticks(x); ax.set_xticklabels([l for _, l in lk], fontsize=5.6)
    ax.set_ylabel('Thorax–pelvis phase (deg)'); ax.set_ylim(0, 185); ax.set_yticks([0, 45, 90, 135, 180])
    ax.set_title('TR+C+AM', loc='left')
    letter(ax, 'F')
    save(fig, 'fig5_coordination')


# ═══ Fig. 6 — speed dependence ══════════════════════════════════════════
SPEED_CURVES = [  # pelvisRotTerm continuation sweeps per speed (w_pel 0 ... 10 000)
    ('0.8 m s$^{-1}$', CS, 'v', ':', ['294', '283', '284', '285', '286']),
    ('1.33 m s$^{-1}$', C0, 'o', '-', ['0', '90', '275', '91', '276', '92']),
    ('1.6 m s$^{-1}$', CV, '^', '--', ['296', '297', '298', '299', '300'])]


def fig6():
    fig = plt.figure(figsize=(W2, 118 * MM))
    gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.4)
    series = [((SP_BASE, SPEEDS), C0, 'o', '-', 'none (effort-minimising)'),
              ((SP_TC, SPEEDS), CTC, 's', '-.', 'TR+C (without AM)'),
              ((SP_TCA6, SPEEDS6), CT, 'D', '--', 'TR+C+AM')]

    def pts(cs, key):
        cs, sp = cs
        return [(s_, M(c)[key]) for s_, c in zip(sp, cs) if c in d]

    def xfmt(ax):
        ax.set_xlabel(r'Walking speed (m s$^{-1}$)'); ax.set_xlim(0.2, 1.7)
        ax.set_xticks([0.4, 0.8, 1.2, 1.6])

    ax = fig.add_subplot(gs[0, 0])
    for cs, col, mk, ls, lab in series:
        ax.plot(*zip(*pts(cs, 'pel')), color=col, marker=mk, ls=ls, label=lab)
    ax.plot(1.33, mE['pel'], marker='*', ms=8, color=INK, ls='none', label='Human (this data set)')
    ax.axhspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    ax.set_ylabel('Pelvis range of motion (deg)'); ax.set_ylim(0, None); xfmt(ax)
    hA, lA = ax.get_legend_handles_labels()
    letter(ax, 'A')
    ax = fig.add_subplot(gs[0, 1])
    mu, sd = LAM.mean(0), LAM.std(0, ddof=1)
    ax.errorbar(LAM_V, mu, yerr=sd, color=MUTED, marker='o', mfc='white', ms=3.5, lw=0.8, capsize=1.5,
                ls=':', label='Lamoth et al. (2002), mean ± s.d.')
    for cs, col, mk, ls, lab in series:
        ax.plot(*zip(*pts(cs, 'tp')), color=col, marker=mk, ls=ls, label=lab)
    ax.plot(1.33, mE['tp'], marker='*', ms=8, color=INK, ls='none')
    ax.set_ylabel('Thorax–pelvis phase (deg)'); ax.set_ylim(0, 185); ax.set_yticks([0, 45, 90, 135, 180])
    xfmt(ax)
    hB, lB = ax.get_legend_handles_labels()
    k = lB.index('Lamoth et al. (2002), mean ± s.d.')
    fig.legend(hA + [hB[k]], lA + [lB[k]], loc='upper center', ncol=5, bbox_to_anchor=(0.5, 1.03),
               columnspacing=1.0)
    letter(ax, 'B')
    ax = fig.add_subplot(gs[1, 0])
    for cs, col, mk, ls, lab in series:
        ax.plot(*zip(*pts(cs, 'ph_hip')), color=col, marker=mk, ls=ls, label=lab)
    ax.axhline(0, color=MUTED, lw=0.5)
    ax.set_ylabel('Pelvis re hip flexion phase (deg)'); xfmt(ax)
    letter(ax, 'C')
    ax = fig.add_subplot(gs[1, 1])
    for lab, col, mk, ls, cs in SPEED_CURVES:
        cs = [c for c in cs if c in d]
        c0 = M(cs[0])['cot']
        ax.plot([M(c)['pel'] for c in cs], [100 * (M(c)['cot'] / c0 - 1) for c in cs], color=col, marker=mk,
                ls=ls, label=lab)
    ax.axvspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    ax.set_xlabel('Pelvis range of motion (deg)'); ax.set_ylabel('Change in cost of transport (%)')
    ax.set_xlim(0, 22); ax.set_ylim(bottom=-0.1)
    ax.set_title('Cost of restricting pelvic rotation', loc='left')
    ax.legend(loc='upper right', fontsize=5.8)
    letter(ax, 'D')
    save(fig, 'fig6_speed')


# ═══ Fig. S1 — earlier factorial with the free-moment cost (TR, FM, C) ═══
FACT_FM = [('0', 'none'), ('203', 'TR'), ('213', 'FM'), ('212', 'C'),
           ('198', 'TR+FM'), ('214', 'TR+C'), ('215', 'FM+C'), ('211', 'TR+FM+C')]
WSETS = {50000: ['0', '203', '213', '212', '211'], 10000: ['81', '232', '233', '234', '235'],
         1000: ['83', '228', '229', '230', '231']}


def figS1():
    fig = plt.figure(figsize=(W2, 58 * MM))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.35, 1, 1], wspace=0.42)
    ax = fig.add_subplot(gs[0, 0])
    f = [(c, l) for c, l in FACT_FM if c in d]
    v = [M(c)['pel'] for c, _ in f]
    ax.bar(range(len(f)), v, color=[C0 if l == 'none' else (CA if l == 'TR+FM+C' else '#9db8cf') for _, l in f],
           width=0.7)
    exp_line(ax, mE['pel']); ax.axhspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    ax.set_xticks(range(len(f))); ax.set_xticklabels([l.replace('+', '+\n') for _, l in f], fontsize=5.6)
    ax.set_ylabel('Pelvis range of motion (deg)'); ax.set_ylim(0, 23)
    letter(ax, 'A', dx=-0.13)
    ax = fig.add_subplot(gs[0, 1])
    labs = ['TR', 'FM', 'C', 'TR+FM+C']; fc = [CS, CV, CC, CA]
    ws = [w for w in (50000, 10000, 1000) if have(*WSETS[w])]
    x = np.arange(len(ws)); bw = 0.2
    for i, lab in enumerate(labs):
        r = [100 * (M(WSETS[w][i + 1])['pel'] / M(WSETS[w][0])['pel'] - 1) for w in ws]
        ax.bar(x + (i - 1.5) * bw, r, width=bw * 0.9, color=fc[i], label=lab,
               hatch='////' if i == 3 else None, edgecolor='white', lw=0)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xticks(x); ax.set_xticklabels(['%g' % w for w in ws])
    ax.set_xlabel(r'$w_\mathrm{acc}$'); ax.set_ylabel('Change in pelvis range of motion (%)')
    ax.set_ylim(-70, 5); ax.legend(ncol=2, loc='lower center', handlelength=1.0, columnspacing=0.8)
    letter(ax, 'B', dx=-0.22)
    ax = fig.add_subplot(gs[0, 2])
    for cs, col, mk, ls, lab in [(SP_TFC, CA, 's', '-', 'TR+FM+C'), (SP_TCA, CT, 'D', '--', 'TR+C+AM')]:
        pts = [(s_, 100 * (M(c)['pel'] / M(b)['pel'] - 1)) for s_, c, b in zip(SPEEDS, cs, SP_BASE) if have(c, b)]
        ax.plot(*zip(*pts), color=col, marker=mk, ls=ls, label=lab)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel(r'Walking speed (m s$^{-1}$)'); ax.set_ylabel('Change in pelvis range of motion (%)')
    ax.set_ylim(-85, 5); ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6]); ax.legend(loc='lower left')
    letter(ax, 'C', dx=-0.22)
    save(fig, 'figS1_factorial_FM')


# ═══ Fig. S2 — what sets the stride time (cadence) in the model ═════════
CAD = ['309', '310', '212', '311', '0', '312', '313', '314']     # imposed stride times, 1.33 m s-1
SP_STIFF = ['355', '352', '345', '353', '354']                   # contact stiffness x10, free stride time
SP_STAB = ['346', '347', '338', '348', '349']                    # TR+AM + proportional stability cost
HUMAN_T = [1.391, 1.222, 1.036, 0.985, 0.931]


def figS2():
    fig = plt.figure(figsize=(W2, 58 * MM))
    gs = fig.add_gridspec(1, 3, wspace=0.45)
    cs = [c for c in CAD if c in d]
    Ts = [M(c)['T'] for c in cs]
    ax = fig.add_subplot(gs[0, 0])
    c0 = M('0')['cot']
    ax.plot(Ts, [100 * (M(c)['cot'] / c0 - 1) for c in cs], color=C0, marker='o')
    ax.axvline(1.036, color=INK, lw=0.8, ls=(0, (3, 2)))
    ax.set_xlabel('Imposed stride time (s)'); ax.set_ylabel('Change in cost of transport (%)')
    ax.set_title('1.33 m s$^{-1}$, nominal model', loc='left')
    letter(ax, 'A')
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(Ts, [M(c)['pel'] for c in cs], color=C0, marker='o')
    ax.axvline(1.036, color=INK, lw=0.8, ls=(0, (3, 2))); ax.axhspan(*HUMAN_RANGE, color=BAND, lw=0, zorder=0)
    ax.set_xlabel('Imposed stride time (s)'); ax.set_ylabel('Pelvis range of motion (deg)')
    letter(ax, 'B')
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(SPEEDS, HUMAN_T, color=INK, ls=(0, (3, 2)), marker='*', ms=6, label='human (Grieve, 1968)')
    for cs_, col, mk, ls, lab in [(SP_BASE, C0, 'o', '-', 'nominal contact'),
                                  (SP_STIFF, CV, '^', '--', 'contact stiffness ×10'),
                                  (SP_STAB, CC, 's', ':', 'stability cost (TR+AM)')]:
        pts = [(s_, M(c)['T']) for s_, c in zip(SPEEDS, cs_) if c in d]
        if pts:
            ax.plot(*zip(*pts), color=col, marker=mk, ls=ls, label=lab)
    ax.set_xlabel(r'Walking speed (m s$^{-1}$)'); ax.set_ylabel('Free stride time (s)')
    ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6]); ax.legend(loc='upper right', fontsize=5.6)
    letter(ax, 'C')
    save(fig, 'figS2_stride_time')


if __name__ == '__main__':
    for f in (fig2, fig3, fig4, fig5, fig6, figS1, figS2):
        try:
            f()
        except Exception as ex:
            import traceback
            print(f.__name__, 'FAILED:', repr(ex)); traceback.print_exc()
