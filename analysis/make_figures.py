"""
Data figures for the manuscript (Fig 2-5). Fig 1 (model schematic) is drawn separately.

Run from project root:  python analysis\\make_figures.py
Output: figures\\fig2_waveforms.(pdf|png), fig3_wacc.(...), fig4_dose.(...), fig5_speed.(...)

Case numbers (see handover.md):
  baseline 0 | reference 114 | angular-momentum (AM) final 138 (w=3, cold start)
  w_acc sweep (no added terms): 61, 83, 82, 60, 81, 80, 0, 84
  AM sweep (hot start, w_acc 15000, w_pel 3000): 114, 130, 131, 132, 133, 134
  diagnostics (w_AM = 10): 135 (no pelvis penalty), 136 (nominal w_acc), 137 (nominal + AM only)
  speed: reference 143/144/114/145, AM 139/140/132/141
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── data ────────────────────────────────────────────────────────────────
RES = 'Results/optimaltrajectories.npy'
EXP = 'OpenSimModel/Hamner_modified/experimentalData.npy'
OUT = 'figures'
os.makedirs(OUT, exist_ok=True)
d = np.load(RES, allow_pickle=True).item()
e = np.load(EXP, allow_pickle=True).item()['Hamner_modified']['kinematics']['positions']

# ── style (validated 3-slot categorical palette; experiment in neutral gray) ──
C_BASE, C_REF, C_AM = '#2a78d6', '#eb6834', '#1baf7a'
C_EXP, C_EXPBAND, INK, MUTED, GRID = '#52514e', '#e1e0d9', '#0b0b0b', '#898781', '#e1e0d9'
MM = 1 / 25.4
W1, W2 = 90 * MM, 190 * MM          # single / double column width
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7, 'axes.titlesize': 7.5, 'axes.labelsize': 7,
    'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'legend.fontsize': 6.5,
    'axes.edgecolor': '#c3c2b7', 'axes.linewidth': 0.6,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.labelcolor': INK,
    'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.4,
    'lines.linewidth': 1.4, 'lines.markersize': 4.5,
    'legend.frameon': False, 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'savefig.dpi': 600,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(OUT, name + '.png'), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print('saved', name)


# ── helpers ─────────────────────────────────────────────────────────────
def periodic(x, gc=None):
    x = np.asarray(x, float).ravel()
    if gc is not None:
        gc = np.asarray(gc, float).ravel()
        if gc.size == x.size and gc[-1] >= 99.999 and gc[0] <= 0.001:
            x = x[:-1]
    return x


def h1(x):
    n = x.size
    return np.sum((x - x.mean()) * np.exp(-2j * np.pi * np.arange(n) / n))


def model_rot(c):
    J = list(d[c]['joints']); Q = np.asarray(d[c]['coordinate_values'])
    pel, lum = Q[J.index('pelvis_rotation')], Q[J.index('lumbar_rotation')]
    gc = np.asarray(d[c].get('GC_percent', np.linspace(0, 100, pel.size))).ravel()
    return gc, pel, lum, pel + lum


def metrics(pel, lum):
    tho = pel + lum
    cp, ct, cl = h1(pel), h1(tho), h1(lum)
    return dict(rom_pel=np.ptp(pel), rom_tho=np.ptp(tho), rom_lum=np.ptp(lum),
                ph_tp=abs(np.degrees(np.angle(ct / cp))),
                ph_lp=abs(np.degrees(np.angle(cl / cp))),
                amp_tho=4 * np.abs(ct) / tho.size)   # peak-to-peak of 1st harmonic


def M(c):
    _, pel, lum, _ = model_rot(c)
    m = metrics(pel, lum); m['cot'] = float(d[c]['COT']); return m


gcE = np.asarray(e.get('GC_percent', np.linspace(0, 100, len(e['mean']['pelvis_rotation'])))).ravel()
pelE, lumE = np.asarray(e['mean']['pelvis_rotation']), np.asarray(e['mean']['lumbar_rotation'])
sdP, sdL = np.asarray(e['std']['pelvis_rotation']), np.asarray(e['std']['lumbar_rotation'])
mE = metrics(periodic(pelE, gcE), periodic(lumE, gcE))
print('EXP check: ph_tp %.1f (95.8), ph_lp %.1f (112.6), ROM %.2f/%.2f/%.2f (6.38/11.70/14.78)'
      % (mE['ph_tp'], mE['ph_lp'], mE['rom_pel'], mE['rom_tho'], mE['rom_lum']))


def hline_exp(ax, y, label='Experiment'):
    ax.axhline(y, color=C_EXP, lw=0.9, ls=(0, (4, 2)), zorder=1, label=label)


# ── Fig 2: waveforms ────────────────────────────────────────────────────
def fig2():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 52 * MM), sharex=True)
    titles = ['Pelvis rotation', 'Thorax rotation (pelvis + lumbar)', 'Lumbar rotation']
    expm = [pelE, pelE + lumE, lumE]
    exps = [sdP, None, sdL]
    for k, ax in enumerate(axs):
        if exps[k] is not None:
            ax.fill_between(gcE, expm[k] - 2 * exps[k], expm[k] + 2 * exps[k],
                            color=C_EXPBAND, lw=0, zorder=0, label='Experiment ±2 s.d.')
        ax.plot(gcE, expm[k], color=C_EXP, lw=1.0, ls=(0, (4, 2)), zorder=1, label='Experiment mean')
        for c, col, ls, lab in [('0', C_BASE, '-', 'Baseline'),
                                ('114', C_REF, (0, (1.5, 1.2)), 'Reference'),
                                ('138', C_AM, '-', r'Angular momentum ($w_\mathrm{AM}=3$)')]:
            gc, pel, lum, tho = model_rot(c)
            ax.plot(gc, [pel, tho, lum][k], color=col, ls=ls, zorder=3, label=lab)
        ax.set_title(titles[k], loc='left', color=INK)
        ax.set_xlabel('Gait cycle (%)'); ax.set_xlim(0, 100)
    axs[0].set_ylabel('Angle (°)')
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, 'fig2_waveforms')


# ── Fig 3: w_acc sweep ──────────────────────────────────────────────────
def fig3():
    cases = {'61': 500, '83': 1000, '82': 2000, '60': 5000, '81': 10000,
             '80': 25000, '0': 50000, '84': 100000}
    cs = [c for c in cases if c in d]
    w = np.array([cases[c] for c in cs]); ms = [M(c) for c in cs]
    fig, axs = plt.subplots(2, 1, figsize=(W1, 95 * MM), sharex=True)
    ax = axs[0]
    for key, col, mk, lab in [('rom_pel', C_BASE, 'o', 'Pelvis'), ('rom_lum', C_REF, 's', 'Lumbar'),
                              ('rom_tho', C_AM, '^', 'Thorax')]:
        ax.plot(w, [m[key] for m in ms], color=col, marker=mk, label=lab, zorder=3)
        ax.axhline(mE[key], color=col, lw=0.8, ls=(0, (4, 2)), zorder=1)
    ax.set_ylabel('Range of motion (°)')
    ax.set_title('(a) Range of motion', loc='left')
    ax.legend(ncol=3, loc='lower right', bbox_to_anchor=(1.0, 1.0), handlelength=1.6, columnspacing=1.0)
    ax = axs[1]
    ax.plot(w, [m['ph_tp'] for m in ms], color=INK, marker='o', label='Model', zorder=3)
    hline_exp(ax, mE['ph_tp'])
    ax.set_ylim(0, 180); ax.set_yticks([0, 45, 90, 135, 180])
    ax.set_ylabel('Thorax–pelvis phase (°)')
    ax.set_title('(b) Relative phase', loc='left')
    ax.legend(loc='upper left', ncol=2)
    for a in axs:
        a.set_xscale('log'); a.axvline(50000, color=MUTED, lw=0.6, zorder=0)
    axs[1].set_xlabel(r'Joint acceleration weight $w_\mathrm{acc}$ (nominal 50 000)')
    fig.tight_layout()
    save(fig, 'fig3_wacc')


# ── Fig 4: angular-momentum penalty dose-response ──────────────────────
def fig4():
    sweep = [('114', 0), ('130', 0.3), ('131', 1), ('132', 3), ('133', 10), ('134', 30)]
    sweep = [(c, w) for c, w in sweep if c in d]
    X0 = 0.1                                   # plotting position for w = 0
    x = np.array([X0 if w == 0 else w for _, w in sweep]); ms = [M(c) for c, _ in sweep]
    diag = [('135', 'Without pelvis penalty', 'v'), ('136', r'Nominal $w_\mathrm{acc}$', 'D'),
            ('137', 'Nominal objective + AM term', 'P')]
    diag = [t for t in diag if t[0] in d]
    panels = [('ph_tp', 'Thorax–pelvis phase (°)', mE['ph_tp'], (0, 185)),
              ('ph_lp', 'Lumbar–pelvis phase (°)', mE['ph_lp'], (90, 185)),
              ('amp_tho', 'Thorax amplitude (°)', mE['amp_tho'], (0, None)),
              ('cot', r'COT (J kg$^{-1}$ m$^{-1}$)', None, (None, None))]
    fig, axs = plt.subplots(1, 4, figsize=(W2, 55 * MM))
    for k, (key, lab, ex, yl) in enumerate(panels):
        ax = axs[k]
        ax.plot(x, [m[key] for m in ms], color=C_AM, marker='o', label='Sweep', zorder=3)
        if ex is not None:
            hline_exp(ax, ex)
        if key != 'cot':
            for c, dl, mk in diag:
                ax.plot(10, M(c)[key], marker=mk, ls='none', mfc='white', mec=INK,
                        mew=0.8, label=dl, zorder=4)
        ax.set_xscale('log'); ax.set_xticks([X0, 0.3, 1, 3, 10, 30])
        ax.set_xticklabels(['0', '0.3', '1', '3', '10', '30'])
        ax.minorticks_off(); ax.set_xlabel(r'$w_\mathrm{AM}$')
        ax.set_title('(%s) %s' % ('abcd'[k], lab), loc='left', fontsize=6.8)
        if key in ('ph_tp', 'ph_lp'):
            ax.set_yticks(np.arange(0, 181, 45))
        ax.set_ylim(*yl)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, 'fig4_dose')


# ── Fig 5: walking speed ────────────────────────────────────────────────
def fig5():
    ref = [('143', 0.8), ('144', 1.0), ('114', 1.33), ('145', 1.6)]
    am = [('139', 0.8), ('140', 1.0), ('132', 1.33), ('141', 1.6)]
    # literature values read from the papers (approximate; different phase measures)
    lamoth = np.array([[1.4, 15], [2.2, 17], [3.0, 37], [3.8, 100], [4.6, 149], [5.4, 149]])
    bruijn = np.array([[2.0, 44], [4.8, 110], [5.2, 126]])
    fig, ax = plt.subplots(figsize=(W1, 65 * MM))
    ax.plot(lamoth[:, 0] / 3.6, lamoth[:, 1], color=MUTED, marker='s', mfc='white', lw=0.8,
            ls=':', label='Lamoth et al. (2002)', zorder=2)
    ax.plot(bruijn[:, 0] / 3.6, bruijn[:, 1], color=MUTED, marker='^', mfc='white', lw=0.8,
            ls=':', label='Bruijn et al. (2008)', zorder=2)
    for cases, col, lab in [(ref, C_REF, 'Reference (no AM term)'),
                            (am, C_AM, r'Angular momentum ($w_\mathrm{AM}=3$)')]:
        cases = [(c, v) for c, v in cases if c in d]
        mm = [M(c) for c, _ in cases]; v = [s for _, s in cases]
        ax.plot(v, [m['ph_tp'] for m in mm], color=col, marker='o', label=lab, zorder=3)
        for (c, s), m in zip(cases, mm):       # flag poorly defined phase
            if m['amp_tho'] < 2.0:
                ax.plot(s, m['ph_tp'], marker='o', mfc='white', mec=col, mew=1.0, zorder=4)
    ax.plot(1.33, mE['ph_tp'], marker='*', ms=8, color=INK, ls='none',
            label='Experiment (this data set)', zorder=5)
    ax.set_xlabel(r'Walking speed (m s$^{-1}$)'); ax.set_ylabel('Thorax–pelvis phase (°)')
    ax.set_ylim(0, 180); ax.set_yticks([0, 45, 90, 135, 180]); ax.set_xlim(0.3, 1.7)
    ax.legend(loc='upper left', fontsize=6)
    fig.tight_layout()
    save(fig, 'fig5_speed')


for f in (fig2, fig3, fig4, fig5):
    try:
        f()
    except Exception as ex:
        print(f.__name__, 'FAILED:', repr(ex))
