# Reproducing "What limits pelvic rotation in human walking? A predictive simulation study"

Simulation framework: Falisse et al. (2019) predictive simulation (OpenSimAD, CasADi, IPOPT), Python 3.9, OpenSim 4.4, NumPy 1.x.
Analyses: OpenSim 4.6 (segment angular momentum), matplotlib.

## Running a condition
```
python main.py <case>  > Results\log_<case>.txt 2>&1
```
One case per process (pandas insert conflict in bounds.py). All settings are in `settings.py`; case numbers below are those keys.
Results accumulate in `Results/optimaltrajectories.npy`. `analysis/export_cases.py <cases>` writes a subset to `Results/export_cases.npy`.

## Additions to the original implementation (main.py, settings keys)
| key | meaning |
|---|---|
| `hipRotStiffness`, `subtalarStiffness` | linear springs (N m rad-1) on hip rotation / subtalar, both legs (factor TR) |
| `fixedStrideTime` | stride time imposed within +-0.1% (factor C) |
| `GRMzTerm` + `GRMzMode: 'pelvis_sum'` | cost on the net external vertical moment about the pelvis origin, both feet (factor AM) |
| `freeMomentTerm` | cost on the free moment of each foot (factor FM) |
| `pelvisRotTerm` | diagnostic penalty on pelvic rotation (energetic cost curves only) |
| `jointAccelerationTerm` | joint-acceleration weight w_acc (nominal 50 000) |
| `armExcitationTerm` | weight w_4 of the arm actuator excitations (nominal 1e6; arm-matched model 2e6) |
| `lumbarRotStiffness` | linear spring (N m rad-1) on lumbar rotation (robustness test) |
| `lockJoints`, `lockTolDeg` | bound coordinates to +-tol around the guess mean |
| `polynomialTag` | load refitted muscle-geometry polynomials (abductor moment arm; analysis/glut_poly.py) |
| `stepStabTerm`, `stepStabLength` | lateral-stability (step-time) cost (Supplementary S1) |
| `initialGuessFromCase` | warm start from a stored solution |
| model `Hamner_modified_stifferContacts` | contact stiffness x10 (variant of the original repository) |

Bug fixes to the original code: bounds.py (pandas duplicate insert above 1.33 m s-1), guesses.py (DataFrame.append removed in pandas 2).

## Figures and supplementary tables
```
python analysis\make_fig1.py                 # Fig. 1 (needs figures/fig1a_model.png)
python analysis\make_figures_paper.py figures  # Figs 2-6, S1, S2
python analysis\make_tables_paper.py           # Tables S10-S13 and additions to Table S4 (analysis/out)
```
`Results/optimaltrajectories.npy` contains every solution listed below, so figures and tables can be regenerated without re-running the simulations.

## Case map (main text)
| content | cases |
|---|---|
| effort-minimising solution, 0.8/1.0/1.33/1.45/1.6 m s-1 | 294, 24, 0, 292, 296 |
| joint-acceleration weight 500 ... 100 000 | 61, 83, 82, 60, 81, 80, 0, 84; metabolic x10: 64 |
| cost of limiting pelvic rotation (w_pel continuation) | 1.33: 0, 90, 275, 91, 276, 92, 277; w_acc 2000: 82, 278-282; 0.8: 294, 283-286; 1.6: 296, 297-300 |
| factorial TR / C / AM (1.33) | 0, 203, 212, 214, 328, 329, 330, 302 |
| AM weight 0/1/3/10/30 (TR+C) | 214, 369, 302, 370, 371 |
| TR+C+AM, w_acc 10 000 / 1000 | 326, 327 |
| TR+C+AM speeds | 316, 318, 302, 320, 322 |
| TR+FM+C+AM speeds | 239, 240, 216, 245, 246 |
| TR+FM+C speeds (Supplementary) | 236, 237, 211, 244, 301 |
| earlier factorial TR / FM / C (Supplementary) | 0, 203, 213, 212, 198, 214, 215, 211; w_acc 10 000: 81, 232-235; 1000: 83, 228-231; TR stiffness 10/20: 226, 227 |
| initial guess / mesh | 269, 272; 270, 273; 323, 324, 325; 271, 274 |
| abductor moment arm | 262, 263, 258; 266, 267, 261 |
| locking arms / lumbar / both | 306-308; 303-305 |
| imposed stride time | 309, 310, 212, 311, 312, 313, 314 |
| lateral-stability cost | 331-342, 346-349 |
| contact stiffness x10 | 343-345, 351-358 (selected: 355, 352, 345, 353, 354); with TR+AM 344, 350, 359-368 |
| TR+C without AM, speeds (Fig. 6) | 383, 384, 214, 385, 386 |
| TR+C+AM at 1.52 m s-1 (Figs 4D, 6) | 391 |
| C only, speeds | 252, 253, 212, 254, 255 |
| C+AM / TR+AM at 1.0 and 1.45 m s-1 | 387, 388, 389, 390 |
| speed diagnostics, 1.6 m s-1 (Table S10) | C from 296: 372; stride-time sweep: 372, 378, 373, 374; scaled w_acc: 375, 376, 377 (1.45); other guess: 321; scaled w_AM: 379-382 |
| TR at one joint; lumbar spring (Table S11) | 392 (hip), 393 (subtalar); 397 (20), 398 (50 N m rad-1) |
| arm actuator weight (Table 1, Table S11) | TR+C+AM: 394 (x0.1), 302 (x1), 399 (x2), 400 (x4), 395/401/402 (x10, three guesses); TR+C: 396 (x0.1), 403 (x10) |

## Case map (arm-matched model, w_4 x2; Table 2, Tables S12-S13)
| content | cases |
|---|---|
| factorial TR / C / AM (1.33) | 404 (none), 405 (TR), 406 (C), 407 (TR+C), 408 (AM), 409 (TR+AM), 410 (C+AM), 399 (TR+C+AM) |
| AM weight 0/1/3/10/30 (TR+C) | 407, 429, 399, 430, 431 |
| free moment: TR+FM+C+AM, TR+FM+C | 432, 433 |
| cost of limiting pelvic rotation (w_pel 0/1000/3000/10 000/30 000) | 404, 434, 435, 436, 437 |
| effort-minimising, 0.8/1.0/1.33/1.45/1.6 | 411, 412, 404, 413, 414 |
| TR+C, 0.8/1.0/1.33/1.45/1.6 | 425, 426, 407, 427, 428 |
| C+AM, 0.8/1.0/1.33/1.45/1.52/1.6 | 420, 421, 410, 422, 423, 424 |
| TR+C+AM, 0.8/1.0/1.33/1.45/1.52/1.6 | 415, 416, 399, 417, 418, 419 |

Cases not listed are exploratory runs from earlier stages of the project and are kept in `settings.py` for completeness; they are not used in the manuscript.

Note: the Windows external function (OpenSimModel/*/Model/*.dll) is the one distributed with the original implementation. If it fails to load on your system, regenerate it from the .osim model with OpenSimAD; the simulations in this study used a local rebuild of the same, unmodified model.
