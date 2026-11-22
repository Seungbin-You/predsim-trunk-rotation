"""
Fig 1 — overview: (a) model snapshot, (b) pelvis-referenced vertical moment (top view),
(c) objective function, (d) coordination measures.

Panel (a) is an OpenSim GUI snapshot saved as  figures/fig1a_model.png  (see handover).
If the file is missing, a labelled placeholder box is drawn instead.

Run from project root:  python analysis\\make_fig1.py   ->  figures/fig1_overview.(pdf|png)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse, Circle, FancyBboxPatch, Arc

OUT = 'figures'; os.makedirs(OUT, exist_ok=True)
IMG = os.path.join(OUT, 'fig1a_model.png')
C_BASE, C_REF, C_AM = '#0072B2', '#E69F00', '#009E73'   # Okabe-Ito, as in Figs 2-6
C_TR, C_C, C_FM = '#56B4E9', '#CC79A7', '#6b6b6b'
INK, MUTED, GRID, EXP = '#000000', '#6b6b6b', '#d9d9d9', '#3a3a3a'
MM = 1 / 25.4
plt.rcParams.update({'font.family': 'sans-serif',
                     'font.sans-serif': ['Arial', 'Liberation Sans', 'Helvetica', 'DejaVu Sans'],
                     'font.size': 7, 'mathtext.default': 'regular',
                     'pdf.fonttype': 42, 'savefig.dpi': 600})


def arrow(ax, p0, p1, col=INK, lw=1.0, ms=7, ls='-', z=3):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=ms, color=col,
                                 lw=lw, ls=ls, zorder=z, shrinkA=0, shrinkB=0))


def title(ax, s):
    # bold upper-case panel letter, plain title
    letter, name = s.split(' ', 1)
    ax.text(0.0, 1.0, letter, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8, fontweight='bold', color=INK)
    ax.annotate(name, (0.0, 1.0), xycoords='axes fraction', xytext=(9, 0), textcoords='offset points',
                ha='left', va='bottom', fontsize=7, color=INK)


fig = plt.figure(figsize=(180 * MM, 64 * MM))
gs = fig.add_gridspec(1, 4, width_ratios=[0.62, 1.55, 1.45, 0.92], wspace=0.42)

# ── (a) model snapshot ──────────────────────────────────────────────────
REMOVE_THIN_LINES = True   # drop 1-2 px lines (floor outline, light helper)
KEY_TO_WHITE = True   # replace the (solid) snapshot background colour with white
CROP = None   # manual crop as fractions (left, top, right, bottom), e.g. (0.3, 0.05, 0.7, 0.95); None = auto


def autocrop(img, tol=0.08, pad=0.03, line_px=2):
    """Trim a uniform background (colour estimated from the image border).
    Thin 1-2 px lines (WebGL helper/floor outlines) are removed before the bounding box is taken:
    a binary opening keeps only structures wider than ~2*line_px+1 px (bones, muscles, spheres)."""
    rgb = img[..., :3].astype(float)
    if rgb.max() > 1.5: rgb /= 255.0
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    bg = np.median(border, axis=0)
    mask = np.abs(rgb - bg).max(axis=2) > tol
    if REMOVE_THIN_LINES:
        try:
            from scipy import ndimage as ndi
            k = np.ones((2 * line_px + 1, 2 * line_px + 1), bool)
            core = ndi.binary_opening(mask, structure=k)
            keep = ndi.binary_dilation(core, structure=k, iterations=2)   # keep anti-aliased edges
            rgb[mask & ~keep] = bg; mask &= keep
        except ImportError:
            print('scipy not found: thin-line removal skipped')
    if not mask.any(): return img
    r = np.where(mask.any(1))[0]; c = np.where(mask.any(0))[0]
    ph, pw = int(pad * img.shape[0]), int(pad * img.shape[1])
    sl = (slice(max(r[0] - ph, 0), r[-1] + ph + 1), slice(max(c[0] - pw, 0), c[-1] + pw + 1))
    rgb, mask = rgb[sl].copy(), mask[sl]
    if KEY_TO_WHITE:   # any solid background colour -> white
        rgb[~mask] = 1.0
    return rgb


ax = fig.add_subplot(gs[0]); ax.axis('off'); title(ax, 'A Model')
iax = ax.inset_axes([0.0, 0.24, 1.0, 0.70]); iax.axis('off')
if os.path.exists(IMG):
    img = plt.imread(IMG)
    if CROP is not None:
        h, w = img.shape[:2]; l, t, r_, b = CROP
        img = img[int(t * h):int(b * h), int(l * w):int(r_ * w)]
    else:
        img = autocrop(img)
    iax.imshow(img, interpolation='lanczos')
else:
    iax.set_xlim(0, 1); iax.set_ylim(0, 1)
    iax.add_patch(FancyBboxPatch((0.05, 0.02), 0.9, 0.96, boxstyle='round,pad=0.01',
                                 fc='#f4f3f0', ec=GRID))
    iax.text(0.5, 0.5, 'OpenSim\nsnapshot', ha='center', va='center', color=MUTED, fontsize=6.5)
ax.text(0.5, 0.20, '31 degrees of freedom, 92 muscles\n3-DOF lumbar joint, oblique subtalar axis\ntorque-driven arms\n6 contact spheres per foot',
        transform=ax.transAxes, ha='center', va='top', fontsize=5.6, color=EXP, linespacing=1.3)

# ── (b) pelvis-referenced vertical moment, top view ─────────────────────
# right-handed frame seen from above: x forward (right on page), y vertical (out of page),
# z = x × y  ->  points DOWN on the page (subject's right side)
host_b = fig.add_subplot(gs[1]); host_b.axis('off')
title(host_b, 'B Vertical moment about the pelvis')
ax = host_b.inset_axes([0.0, 0.0, 1.0, 0.97]); ax.axis('off')
ax.set_xlim(-0.15, 1.85); ax.set_ylim(-2.15, 0.30); ax.set_aspect('equal', adjustable='box')
ax.text(-0.15, 0.28, 'top view (y vertical, out of the page)', fontsize=5.6, color=MUTED, va='top')
O = np.array([0.0, -0.10]); P = np.array([0.95, -0.55]); G = P + np.array([-0.20, 0.0])
cop = np.array([1.38, -1.08])
# ground frame at O
arrow(ax, O, O + [0.26, 0], col=MUTED, lw=0.8, ms=5)
ax.text(O[0] + 0.29, O[1], 'x (forward)', va='center', color=MUTED, fontsize=5.6)
arrow(ax, O, O + [0, -0.26], col=MUTED, lw=0.8, ms=5)
ax.text(O[0] + 0.04, O[1] - 0.27, 'z (right)', ha='left', va='top', color=MUTED, fontsize=5.6)
ax.add_patch(Circle(O, 0.045, fc='white', ec=MUTED, lw=0.7, zorder=4))
ax.plot(*O, 'o', color=MUTED, ms=1.6, zorder=5)
ax.text(O[0] - 0.07, O[1] + 0.02, 'O', ha='right', va='center', color=MUTED, fontsize=6.8)
# r_P
arrow(ax, O + [0.05, -0.02], P + [-0.04, 0.02], col=MUTED, lw=0.6, ls=(0, (3, 2)), ms=5)
ax.text(0.46, -0.27, r'$\mathbf{r}_P$', color=MUTED, fontsize=6.6, va='bottom', ha='center')
# moment about P
ax.add_patch(Arc(P, 0.34, 0.34, theta1=200, theta2=500, color=C_AM, lw=1.4, zorder=3))
a1 = np.radians(500); a0 = np.radians(485)
arrow(ax, P + 0.17 * np.array([np.cos(a0), np.sin(a0)]), P + 0.17 * np.array([np.cos(a1), np.sin(a1)]),
      col=C_AM, lw=1.4, ms=6)
ax.add_patch(Circle(P, 0.03, fc=C_AM, ec='white', lw=0.8, zorder=4))
ax.text(P[0] + 0.22, P[1] + 0.10, 'M$_{P,y}$', color=C_AM, fontsize=7.2, va='center')
ax.text(P[0] + 0.02, P[1] + 0.24, 'pelvis origin P', fontsize=5.8, color=INK, ha='center', va='bottom')
# COM
ax.add_patch(Circle(G, 0.022, fc='white', ec=INK, lw=0.7, zorder=4))
ax.plot([G[0], G[0] - 0.10], [G[1] - 0.03, G[1] - 0.16], color=INK, lw=0.4)
ax.text(G[0] - 0.12, G[1] - 0.17, 'COM\n(about 7 cm posterior to P)', fontsize=5.4, ha='center', va='top',
        color=INK, linespacing=1.15)
# stance foot and ground reaction force components
ax.add_patch(Ellipse(cop + [0.02, 0], 0.40, 0.14, fc='#f2f2f2', ec=MUTED, lw=0.6))
ax.plot(*cop, 'o', color=INK, ms=2.4, zorder=5)
arrow(ax, cop, cop + [-0.28, 0], col=EXP, lw=1.2, ms=6)
ax.text(cop[0] - 0.31, cop[1], 'F$_x$', color=EXP, ha='right', va='center', fontsize=6.4)
arrow(ax, cop, cop + [0, 0.22], col=EXP, lw=1.2, ms=6)
ax.text(cop[0] + 0.04, cop[1] + 0.20, 'F$_z$', color=EXP, fontsize=6.4, va='center')
ax.text(cop[0] + 0.02, cop[1] - 0.10, 'stance foot', fontsize=5.6, color=EXP, ha='center', va='top')
# equations, separated from the drawing
ax.plot([-0.15, 1.85], [-1.40, -1.40], color=GRID, lw=0.6)
ax.text(0.85, -1.50, r'M$_{P,y}$ = $\Sigma_\mathrm{feet}$ (M$_{O,y}$ $-$ z$_P$F$_x$ + x$_P$F$_z$)',
        ha='center', va='top', fontsize=6.4, color=INK)
ax.text(0.85, -1.74, r'cost: w$_\mathrm{AM}$ (M$_{P,y}$)$^2$',
        ha='center', va='top', fontsize=6.4, color=INK)
ax.text(0.85, -1.98, r'(about the COM: dH$_{G,y}$/dt)',
        ha='center', va='top', fontsize=5.6, color=MUTED)

# ── (c) objective ───────────────────────────────────────────────────────
ax = fig.add_subplot(gs[2]); ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
title(ax, 'C Objective and factors')
rows = [(r'w$_1$ $\dot{E}$', 'metabolic rate', INK, ''),
        ('w$_2$ a', 'activation', INK, ''),
        (r'w$_\mathrm{acc}$ $\ddot{q}$', 'joint acceleration', C_REF, 'varied'),
        (r'w$_4$ e$_\mathrm{arm}$', 'arm excitation', INK, ''),
        (r'w$_5$ $\tau_\mathrm{pass}$', 'passive torque', INK, ''),
        ('w$_6$ u', 'control derivatives', INK, ''),
        ('TR', r'hip rotation and subtalar springs', C_TR, ''),
        ('C', 'human stride time imposed', C_C, ''),
        ('AM', r'w$_\mathrm{AM}$ (M$_{P,y}$)$^2$, angular momentum rate', C_AM, ''),
        ('FM', r'w$_\mathrm{FM}$ T$^2$, free moment', C_FM, '')]
ax.text(0.0, 0.93, r'J = (1/d) $\int$ $\Sigma_i$ w$_i$ (x$_i$)$^2$ dt', fontsize=7, va='top')
ax.text(0.0, 0.765, 'nominal (Falisse et al., 2019)', fontsize=5.3, color=MUTED)
ys = [0.70, 0.635, 0.57, 0.505, 0.44, 0.375, 0.24, 0.175, 0.11, 0.045]
ax.plot([0, 1], [0.32, 0.32], color=GRID, lw=0.6)
ax.text(0.0, 0.295, 'candidate factors', fontsize=5.3, color=MUTED, va='top')
for (eq, desc, col, tag), y in zip(rows, ys):
    if y < 0.3: y -= 0.02
    ax.text(0.0, y, eq, color=col, fontsize=6.3, va='center', fontweight='bold' if y < 0.3 else 'normal')
    ax.text(0.30 if y > 0.3 else 0.14, y, desc + (f' ({tag})' if tag else ''), color=col if col != INK else EXP, fontsize=5.4, va='center')
    if tag:
        pass

# ── (d) coordination measures ───────────────────────────────────────────
host = fig.add_subplot(gs[3]); host.axis('off')
host.text(-0.30, 1.0, 'D', transform=host.transAxes, ha='left', va='bottom',
          fontsize=8, fontweight='bold', color=INK)
host.annotate('Coordination measure', (-0.30, 1.0), xycoords='axes fraction', xytext=(9, 0),
              textcoords='offset points', ha='left', va='bottom', fontsize=7, color=INK)
D_BOTTOM, D_HEIGHT = 0.27, 0.69          # plot box inside the panel (fractions of panel height)
ax = host.inset_axes([0.0, D_BOTTOM, 1.0, D_HEIGHT])
t = np.linspace(0, 100, 400); dphi = 96
pel = 3.2 * np.sin(2 * np.pi * t / 100)
tho = 6.0 * np.sin(2 * np.pi * t / 100 - np.radians(dphi))
ax.plot(t, pel, color=MUTED, lw=1.1)
ax.plot(t, tho, color=INK, lw=1.3)
tp, tt = 25.0, 25.0 + dphi / 360 * 100
ax.plot([tp, tp], [3.2, 7.6], color=INK, lw=0.4, ls=':')
ax.plot([tt, tt], [6.0, 7.6], color=INK, lw=0.4, ls=':')
ax.annotate('', xy=(tt, 7.6), xytext=(tp, 7.6), arrowprops=dict(arrowstyle='<->', lw=0.6, color=INK,
            shrinkA=0, shrinkB=0))
ax.text((tp + tt) / 2, 8.1, r'$\Delta\varphi_\mathrm{th\text{-}pel}$', ha='center', va='bottom',
        color=INK, fontsize=6.2)
ax.text(12, 3.9, 'pelvis', ha='center', va='bottom', color=MUTED, fontsize=5.6)
ax.text(tt + 9, 5.9, 'thorax', ha='left', va='center', color=INK, fontsize=5.6)
ax.set_xlim(0, 100); ax.set_ylim(-7.5, 10.5); ax.set_xticks([0, 50, 100]); ax.set_yticks([-6, -3, 0, 3, 6])
ax.set_xlabel('Gait cycle (%)', fontsize=6, labelpad=1); ax.set_ylabel('Rotation (°)', fontsize=6, labelpad=1)
for s_ in ('top', 'right'):
    ax.spines[s_].set_visible(False)
for s_ in ('left', 'bottom'):
    ax.spines[s_].set_color('#c3c2b7'); ax.spines[s_].set_linewidth(0.6)
ax.tick_params(colors=MUTED, labelsize=5.6, width=0.6)
host.text(-0.30, 0.06, 'thorax = pelvis + lumbar;\nphase from the first harmonic',
          transform=host.transAxes, ha='left', va='top', fontsize=5.2, color=MUTED)

fig.savefig(os.path.join(OUT, 'fig1_overview.pdf'), bbox_inches='tight')
fig.savefig(os.path.join(OUT, 'fig1_overview.png'), bbox_inches='tight', dpi=300)
print('saved fig1_overview')
