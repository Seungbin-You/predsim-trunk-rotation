'''
    Simulation settings for:
    "Transverse-plane trunk kinematics in predictive gait simulation:
     evaluation and a test of the angular momentum hypothesis"

    Modified from settings.py of predsim_tutorial (A. Falisse, Apache-2.0).
    Case IDs correspond to the simulation IDs in the Supplementary Material
    (Tables S1 and S5). Unspecified settings take the defaults of main.py:
      weights  metabolicEnergyRateTerm 500, activationTerm 2000,
               jointAccelerationTerm 50000 (w_acc), armExcitationTerm 1e6,
               passiveTorqueTerm 1000, controls 0.001,
               GRMzTerm 0 (added term weight), pelvisRotTerm 0 (w_pel)
      targetSpeed 1.33 m/s, guessType 'hotStart' (guess from experimental data),
      gaitCycleSimulation 'half' (symmetric half cycle), d 3.
      NOTE: main.py defaults to N = 50; all cases here set N explicitly.

    GRMzMode (form of the added vertical-moment penalty):
      'pelvis_sum' : (M_P,y^r + M_P,y^l)^2, vertical ground reaction moment
                     about the pelvis origin (proxy for the rate of change of
                     whole-body vertical angular momentum) -- main text
      'free'       : T_r^2 + T_l^2, free moment of each foot
      'sum'/'each' : moment about the ground origin (origin-dependent; see
                     Supplementary Section S1). 'sum' is the default of main.py.

    Groups
      0-7      baseline and repository cases
      4        full gait cycle (no symmetry)
      6        lumbar passive-torque test: requires the lumbar_rotation
               passive-torque angle parameters (theta) in muscleData.py to be
               changed to +/-3 deg; with the distributed muscleData.py it
               reproduces case 0
      7        GRMzTerm = 0 stated explicitly (code-change check; = case 0)
      10-17    origin-referenced 'sum' penalty, weight sweep
      20-25    speed sweep with (20-22) and without (23-25) the 'sum' penalty
      33, 34   arm excitation weight x100
      40, 41   N = 50
      50-56    origin-referenced 'each' penalty, weight sweep
      60-64    objective terms (w_acc, arm excitation, metabolic weights)
      70, 71   reduced w_acc with 'each' penalty
      80-84    w_acc sweep
      90-92    pelvis-rotation penalty sweep (diagnostic, no physiological basis)
      93-113   combinations with the origin-referenced 'each' penalty
      114      reference condition (w_acc 15000, w_pel 3000, no added term)
      148-153  follow-up: proximal-distal activation gradient (activationGradient
               = lambda 0.5/1/2) without (148-150) and with (151-153) w_AM = 3
      154-156  follow-up: arm excitation weight 1e5/3e5 with w_AM = 3 (154, 155)
               and 1e5 without the added term (156)
      157-158  follow-up: w_AM = 3 with model variants (stiffer contacts,
               weaker gluteals) distributed with predsim_tutorial
      159-161  follow-up: tracking of human pelvis timing relative to the legs
               (pelvisTrackTerm 3e4 / 3e5 with w_AM = 3; 3e5 without)
      162-167  follow-up: lumbar torsional stiffness 10/20/40 N m/rad without
               (162-164) and with (165-167) w_AM = 3
      168-170  follow-up: 132 objective started from the 160 solution (168) or
               from its own solution (169, check); 160 with cold start (170)
      171-174  follow-up: penalty on the lumbar axial-rotation torque
               (lumbarTorqueTerm 0.3/1/3/10) with w_AM = 3
      175-181  pelvis rotation study, nominal objective, no pelvis penalty:
               hip rotation stiffness 25/50/100 N m/rad (175-177); hip
               abductors/extensors/deep rotators x0.5 (178) and x1.5 (179);
               all lower-limb muscles x0.7 (180); stride time 1.036 s (181)
      182-185  pelvis rotation study: hip rotation 100 + subtalar 50/100 N m/rad
               (182, 183); free-moment penalty 400 (184); all three (185)
      186-190  two of three routes (186 hip + free, 187 subtalar + free);
               weaker free-moment penalty 40/100 with both stiffnesses
               (188, 189); 185 + w_AM = 3 via freeMomentTerm (190)
      191-197  hip 100 + free-moment penalty 1/3/10 (191-193); hip 25/50 +
               free 400 (194, 195); 190 with w_acc 15000 (196) and cold start (197)
      198-202  physiological-range set: hip 50 + subtalar 50/100 + free-moment
               penalty 1 (198, 199); 198 with hip slack 5/10 deg (200, 201);
               198 + w_AM 3 + w_acc 15000 (202)
      115      free-moment penalty
      116-124  INTENDED as pelvis-referenced penalties, but RUN WITH THE
               ORIGIN-REFERENCED 'sum' PENALTY: main.py had no pelvis branch
               at the time (unknown modes then fell back to 'sum'). Re-running
               them with the current main.py gives pelvis-referenced results,
               not the results reported in Table S1.
      130-134  pelvis-referenced penalty ('pelvis_sum'), weight sweep
      135-137  pelvis-referenced penalty without the diagnostic modifications
      138      selected condition (w_AM = 3), generic initial guess
      139-141  selected condition at 0.8, 1.0 and 1.6 m/s
      142, 147 selected condition with N = 50 (experimental / generic guess)
      143-145  reference condition at 0.8, 1.0 and 1.6 m/s
      146      reference condition with N = 50
'''


def getSettings():

    settings = {

        # ── Baseline and repository cases ───────────────────────────────
        '0': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25},
        '1': {'model': 'Hamner_modified', 'targetSpeed': 1.00, 'N': 25},
        '2': {'model': 'Hamner_modified_weakerGluts', 'targetSpeed': 1.33,
              'N': 25},
        '3': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33,
              'N': 25},
        '4': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50,
              'gaitCycleSimulation': 'full'},
        '5': {'model': 'Hamner_modified_weakerRightGluts', 'targetSpeed': 1.33,
              'N': 50, 'gaitCycleSimulation': 'full'},
        '6': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25},
        '7': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
              'GRMzTerm': 0},

        # ── Origin-referenced 'sum' penalty ─────────────────────────────
        '10': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 1},
        '11': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 10},
        '12': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 100},
        '13': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 1000},
        '14': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 3},
        '15': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 20},
        '16': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 30},
        '17': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 50},

        # ── Speed sweep with / without the 'sum' penalty ────────────────
        '20': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25,
               'GRMzTerm': 30},
        '21': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25,
               'GRMzTerm': 30},
        '22': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25,
               'GRMzTerm': 30},
        '23': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25},
        '24': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25},
        '25': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25},

        # ── Arm excitation weight x100 ──────────────────────────────────
        '33': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 30, 'armExcitationTerm': 100000000},
        '34': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'armExcitationTerm': 100000000},

        # ── N = 50 ──────────────────────────────────────────────────────
        '40': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50,
               'GRMzTerm': 30},
        '41': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50},

        # ── Origin-referenced 'each' penalty ────────────────────────────
        '50': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 30,  'GRMzMode': 'each'},
        '51': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 1,   'GRMzMode': 'each'},
        '52': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 3,   'GRMzMode': 'each'},
        '53': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 10,  'GRMzMode': 'each'},
        '54': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 20,  'GRMzMode': 'each'},
        '55': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 50,  'GRMzMode': 'each'},
        '56': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'GRMzTerm': 100, 'GRMzMode': 'each'},

        # ── Objective terms ─────────────────────────────────────────────
        '60': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 5000},
        '61': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 500},
        '62': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'armExcitationTerm': 100000},
        '63': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 500, 'armExcitationTerm': 100000},
        '64': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'metabolicEnergyRateTerm': 5000},

        # ── Reduced w_acc with 'each' penalty ───────────────────────────
        '70': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 500, 'armExcitationTerm': 100000,
               'GRMzTerm': 50, 'GRMzMode': 'each'},
        '71': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 5000,
               'GRMzTerm': 50, 'GRMzMode': 'each'},

        # ── w_acc sweep ─────────────────────────────────────────────────
        '80': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 25000},
        '81': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 10000},
        '82': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 2000},
        '83': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 1000},
        '84': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 100000},

        # ── Pelvis-rotation penalty sweep (diagnostic) ──────────────────
        '90': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'pelvisRotTerm': 100},
        '91': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'pelvisRotTerm': 1000},
        '92': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'pelvisRotTerm': 10000},

        # ── Combinations with the origin-referenced 'each' penalty ──────
        '93': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 2000, 'pelvisRotTerm': 3000},
        '94': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 2000, 'pelvisRotTerm': 3000,
               'GRMzTerm': 50, 'GRMzMode': 'each'},
        '95': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'pelvisRotTerm': 3000},
        '96': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
               'jointAccelerationTerm': 5000, 'pelvisRotTerm': 3000,
               'GRMzTerm': 50, 'GRMzMode': 'each'},
        '100': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 5000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20,  'GRMzMode': 'each'},
        '101': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 5000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 100, 'GRMzMode': 'each'},
        '102': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 10000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 50,  'GRMzMode': 'each'},
        '103': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 5000, 'pelvisRotTerm': 2000,
                'GRMzTerm': 50,  'GRMzMode': 'each'},
        '104': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 5000, 'pelvisRotTerm': 5000,
                'GRMzTerm': 50,  'GRMzMode': 'each'},
        '105': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 50000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 50, 'GRMzMode': 'each'},
        '106': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 25000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 50, 'GRMzMode': 'each'},
        '107': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 10000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '108': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 10000, 'pelvisRotTerm': 4000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '109': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 25000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '110': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '111': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '112': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},
        '113': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 20, 'GRMzMode': 'each'},

        # ── Reference condition and free moment ─────────────────────────
        '114': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 0},
        '115': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 400, 'GRMzMode': 'free'},

        # ── 116-124: see header -- these ran with the origin 'sum' penalty
        '116': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 184, 'GRMzMode': 'pelvis_each'},
        '117': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 144, 'GRMzMode': 'pelvis_sum'},
        '118': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 72, 'GRMzMode': 'pelvis_sum'},
        '119': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 144, 'GRMzMode': 'pelvis_sum',
                'guessType': 'coldStart'},
        '120': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 92, 'GRMzMode': 'pelvis_each'},
        '121': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 184, 'GRMzMode': 'pelvis_each',
                'guessType': 'coldStart'},
        '122': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 36, 'GRMzMode': 'pelvis_sum'},
        '123': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 108, 'GRMzMode': 'pelvis_sum'},
        '124': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 0,
                'GRMzTerm': 72, 'GRMzMode': 'pelvis_sum'},

        # ── Pelvis-referenced penalty: weight sweep (main text) ─────────
        '130': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 0.3, 'GRMzMode': 'pelvis_sum'},
        '131': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 1, 'GRMzMode': 'pelvis_sum'},
        '132': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '133': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 10, 'GRMzMode': 'pelvis_sum'},
        '134': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 30, 'GRMzMode': 'pelvis_sum'},

        # ── Without the diagnostic modifications ────────────────────────
        '135': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 0,
                'GRMzTerm': 10, 'GRMzMode': 'pelvis_sum'},   # no pelvis penalty
        '136': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'pelvisRotTerm': 3000,
                'GRMzTerm': 10, 'GRMzMode': 'pelvis_sum'},   # nominal w_acc
        '137': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'GRMzTerm': 10, 'GRMzMode': 'pelvis_sum'},   # nominal + new term

        # ── Selected condition (w_AM = 3): guess, speed and mesh checks ─
        '138': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'guessType': 'coldStart'},
        '139': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '140': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '141': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '142': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},

        # ── Reference condition: speed and mesh ─────────────────────────
        '143': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000},
        '144': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000},
        '145': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000},
        '146': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000},
        '147': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'guessType': 'coldStart'},

        # ---- Follow-up (2026-10): proximal-distal activation gradient ----
        # activationGradient = lambda; lambda = 0 equals cases 114 / 132.
        '148': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'activationGradient': 0.5},
        '149': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'activationGradient': 1},
        '150': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'activationGradient': 2},
        '151': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'activationGradient': 0.5},
        '152': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'activationGradient': 1},
        '153': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'activationGradient': 2},
        # ---- Follow-up (2026-10): cheaper arms + angular-momentum term ----
        # armExcitationTerm default 1e6; 156 is the control without the term.
        '154': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'armExcitationTerm': 100000},
        '155': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'armExcitationTerm': 300000},
        '156': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'armExcitationTerm': 100000},
        # ---- Follow-up (2026-10): pelvis timing — model variants (A) ----
        '157': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '158': {'model': 'Hamner_modified_weakerGluts', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        # ---- Follow-up (2026-10): track human pelvis timing (B) ----
        '159': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'pelvisTrackTerm': 30000},
        '160': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'pelvisTrackTerm': 300000},
        '161': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'pelvisTrackTerm': 300000},
        # ---- Follow-up (2026-10): lumbar torsional stiffness (C) ----
        '162': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'lumbarRotStiffness': 10},
        '163': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'lumbarRotStiffness': 20},
        '164': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'lumbarRotStiffness': 40},
        '165': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'lumbarRotStiffness': 10},
        '166': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'lumbarRotStiffness': 20},
        '167': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'lumbarRotStiffness': 40},
        # ---- Follow-up (2026-10): is the human-like solution a local optimum? ----
        # 168: objective of 132 (no tracking) started from the solution of 160
        # 169: objective of 132 started from its own solution (warm-start check)
        # 170: case 160 with the generic (cold-start) guess
        '168': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'initialGuessFromCase': 160},
        '169': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'initialGuessFromCase': 132},
        '170': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'pelvisTrackTerm': 300000, 'guessType': 'coldStart'},
        # ---- Follow-up (2026-11): lumbar torsional load penalty, w_AM = 3 ----
        '171': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'lumbarTorqueTerm': 0.3},
        '172': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'lumbarTorqueTerm': 1},
        '173': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'lumbarTorqueTerm': 3},
        '174': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'jointAccelerationTerm': 15000, 'pelvisRotTerm': 3000,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'lumbarTorqueTerm': 10},
        # ---- Pelvis rotation study (2026-11): nominal objective, no pelvis
        # penalty; one candidate physiological factor at a time ----
        # A: hip rotation passive stiffness (N m/rad)
        '175': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 25},
        '176': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50},
        '177': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100},
        # B: muscle strength (max isometric force scale)
        '178': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'muscleStrengthScale': {'glut_med': 0.5, 'glut_min': 0.5, 'glut_max': 0.5, 'quad_fem': 0.5, 'gem': 0.5, 'peri': 0.5}},
        '179': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'muscleStrengthScale': {'glut_med': 1.5, 'glut_min': 1.5, 'glut_max': 1.5, 'quad_fem': 1.5, 'gem': 1.5, 'peri': 1.5}},
        '180': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25,
                'muscleStrengthScale': {'glut_med': 0.7, 'glut_min': 0.7, 'semimem': 0.7, 'semiten': 0.7, 'bifemlh': 0.7, 'bifemsh': 0.7, 'sar': 0.7, 'add_long': 0.7, 'add_brev': 0.7, 'add_mag': 0.7, 'tfl': 0.7, 'pect': 0.7, 'grac': 0.7, 'glut_max': 0.7, 'iliacus': 0.7, 'psoas': 0.7, 'quad_fem': 0.7, 'gem': 0.7, 'peri': 0.7, 'rect_fem': 0.7, 'vas_med': 0.7, 'vas_int': 0.7, 'vas_lat': 0.7, 'med_gas': 0.7, 'lat_gas': 0.7, 'soleus': 0.7, 'tib_post': 0.7, 'flex_dig': 0.7, 'flex_hal': 0.7, 'tib_ant': 0.7, 'per_brev': 0.7, 'per_long': 0.7, 'per_tert': 0.7, 'ext_dig': 0.7, 'ext_hal': 0.7}},
        # C: stride time fixed to the experimental value (1.036 s)
        '181': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.036},
        # D: hip rotation + subtalar stiffness (block the detour through the ankle)
        '182': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 50},
        '183': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100},
        # E: foot-ground twisting (free moment) penalty, no pelvis penalty
        '184': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'GRMzTerm': 400, 'GRMzMode': 'free'},
        # D + E: all three routes restrained
        '185': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'GRMzTerm': 400, 'GRMzMode': 'free'},
        # Which routes are necessary: two of three
        '186': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'GRMzTerm': 400, 'GRMzMode': 'free'},
        '187': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'subtalarStiffness': 100, 'GRMzTerm': 400, 'GRMzMode': 'free'},
        # Weaker foot-ground restraint (keep a realistic free moment)
        '188': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'GRMzTerm': 40, 'GRMzMode': 'free'},
        '189': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'GRMzTerm': 100, 'GRMzMode': 'free'},
        # 185 + angular-momentum term (free moment via freeMomentTerm)
        '190': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'freeMomentTerm': 400, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        # Weak free-moment penalty (keep a human-like free moment), hip 100
        '191': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'GRMzTerm': 1, 'GRMzMode': 'free'},
        '192': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'GRMzTerm': 3, 'GRMzMode': 'free'},
        '193': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'GRMzTerm': 10, 'GRMzMode': 'free'},
        # Minimal hip stiffness with free-moment penalty 400
        '194': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 25, 'GRMzTerm': 400, 'GRMzMode': 'free'},
        '195': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'GRMzTerm': 400, 'GRMzMode': 'free'},
        # 190 with reduced joint-acceleration weight; 190 with cold start
        '196': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'freeMomentTerm': 400, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'jointAccelerationTerm': 15000},
        '197': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 100,
                'freeMomentTerm': 400, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'guessType': 'coldStart'},
        # Physiological-range combination: hip ~ capsule stiffness (50),
        # subtalar 50/100, free-moment penalty 1 (human-like free moment)
        '198': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free'},
        '199': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 100,
                'GRMzTerm': 1, 'GRMzMode': 'free'},
        # 198 with a slack region in the hip rotation spring (5 / 10 deg)
        '200': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'hipRotSlack': 5,
                'subtalarStiffness': 50, 'GRMzTerm': 1, 'GRMzMode': 'free'},
        '201': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'hipRotSlack': 10,
                'subtalarStiffness': 50, 'GRMzTerm': 1, 'GRMzMode': 'free'},
        # 198 + angular-momentum term + reduced joint-acceleration weight (as 196)
        '202': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum',
                'jointAccelerationTerm': 15000},
        # --- 11-09: dose-response around 198 (hip 50 + subtalar 50 + free moment 1) ---
        # (A) free-moment weight sweep at physiological hip/subtalar springs
        '203': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50},
        '204': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 0.3, 'GRMzMode': 'free'},
        '205': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 3, 'GRMzMode': 'free'},
        '206': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 10, 'GRMzMode': 'free'},
        # (B) hip rotation stiffness dose (linear, no slack) at subtalar 50 + free moment 1
        '207': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 100, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free'},
        '208': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 200, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free'},
        '209': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 400, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free'},
        # (C) all physiological-range factors combined + human stride time (1.036 s, as 181)
        '210': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 3, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},
        '211': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},
        # (D) 2x2x2 factorial: A = springs (hip 50 + subtalar 50), B = free moment 1, C = stride time 1.036 s
        #     existing: none=0, A=203, AB=198, ABC=211 ; new below (C uses the 11-09 band code)
        '212': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.036},  # C  (= 181 rerun)
        '213': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'GRMzTerm': 1, 'GRMzMode': 'free'},  # B
        '214': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'fixedStrideTime': 1.036},  # AC
        '215': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'GRMzTerm': 1, 'GRMzMode': 'free',
                'fixedStrideTime': 1.036},  # BC
        # (E) stage 2 (timing/coordination) on top of 211 (physiological springs + human stride time)
        '216': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036},  # + AM term
        '217': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 15000},  # + AM term + lower w_acc
        '218': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'torsoYawAccTerm': 10},  # torso yaw stabilisation
        '219': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'torsoYawAccTerm': 100},
        # (F) 216 + w_acc sweep (amplitude-phase balance) ; 222 = 220 without free-moment term
        '220': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 30000},
        '221': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 22000},
        '222': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 30000},
        # (G) free-moment weight sweep on 221 (AM 3, w_acc 22000): 0 / [1 = 221] / 10 / 100
        '223': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 22000},
        '224': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 10, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 22000},
        '225': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 100, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'jointAccelerationTerm': 22000},
        # (H) robustness, 11-13
        # H1: factor A at in-vivo passive stiffness (Leite 2012: 10.1 +/- 3.9 Nm/rad), with B and C (cf. 211 = 50/50)
        '226': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 10, 'subtalarStiffness': 10, 'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},
        '227': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 20, 'subtalarStiffness': 20, 'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},
        # H2: factor main effects under an energy-dominated objective (w_acc 1000; baseline = case 83, pelvis 29.7 deg)
        '228': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 1000, 'hipRotStiffness': 50, 'subtalarStiffness': 50},  # A
        '229': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 1000, 'GRMzTerm': 1, 'GRMzMode': 'free'},  # B
        '230': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 1000, 'fixedStrideTime': 1.036},  # C
        '231': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 1000, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},  # ABC
        # H3: factor main effects at intermediate w_acc 10000 (baseline = case 81, pelvis 25.1 deg)
        '232': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 10000, 'hipRotStiffness': 50, 'subtalarStiffness': 50},  # A
        '233': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 10000, 'GRMzTerm': 1, 'GRMzMode': 'free'},  # B
        '234': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 10000, 'fixedStrideTime': 1.036},  # C
        '235': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 10000, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},  # ABC
        # (I) stage 3: multiple speeds, nominal weights. Baselines: 23 (0.8), 24 (1.0), 0 (1.33), 25 (1.6).
        #     C = human stride time from preferred step length ~ v^0.42 (Kuo 2001), anchored at 1.036 s @ 1.33 m/s:
        #     0.8 -> 1.391 s, 1.0 -> 1.222 s, 1.6 -> 0.931 s.  1.33 m/s counterparts: ABC = 211, ABC+AM = 216.
        '236': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.391},  # ABC
        '237': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.222},  # ABC
        '238': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 0.931},  # ABC
        '239': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.391},  # ABC + AM
        '240': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.222},  # ABC + AM
        '241': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.931},  # ABC + AM
        # (J) 11-16: check of the 1.33 -> 1.6 m/s drop in pelvis ROM. 242 = rerun of baseline 25 with current code;
        #     1.45 m/s: baseline / ABC / ABC+AM (C stride time 0.985 s, step length ~ v^0.42, Grieve 1968)
        '242': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25},
        '243': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25},
        '244': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 0.985},  # ABC
        '245': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.985},  # ABC + AM
        # (K) 11-16: warm-start checks at 1.6 m/s (is the drop above 1.45 m/s a different local optimum?)
        '246': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.931,
                'initialGuessFromCase': '245'},  # = 241, warm start from 1.45 m/s ABC+AM
        '247': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'initialGuessFromCase': '243'},  # = 25/242, warm start from 1.45 m/s baseline
        # (L) 11-16 speed-trend hypotheses. H1: w_acc 10000 baseline (1.33 = case 81). H2: C only (1.33 = case 212).
        '248': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'jointAccelerationTerm': 10000},  # H1
        '249': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'jointAccelerationTerm': 10000},  # H1
        '250': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'jointAccelerationTerm': 10000},  # H1
        '251': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'jointAccelerationTerm': 10000},  # H1
        '252': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'fixedStrideTime': 1.391},  # H2 C only
        '253': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'fixedStrideTime': 1.222},  # H2 C only
        '254': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'fixedStrideTime': 0.985},  # H2 C only
        '255': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'fixedStrideTime': 0.931},  # H2 C only
        # (M) 11-16 abductor lever arm (evolutionary test, Lovejoy 2005): glut_med1-3 / glut_min1-3 femoral
        #     insertion moved laterally (z x k, femur frame), MTU length offset to keep neutral length; leg
        #     polynomials refitted (analysis/glut_poly.py) -> {modelName}_abdXXX_polynomial_{r,l}.json.
        #     k 0.8 / 1.2 / 1.4 -> mean gluteal hip-abduction moment arm -15% / +12% / +22% (dummy motion).
        '256': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd080'},
        '257': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd120'},
        '258': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd140'},
        '259': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd080'},  # ABC
        '260': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd120'},  # ABC
        '261': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd140'},  # ABC
        # (N) 11-16 warm-start checks for (M): 256/257 landed on a shorter-stride optimum (stride 1.40 vs 1.49 m).
        #     k=1.0 refit reproduces the baseline polynomials to 1e-16, so the pipeline itself is exact.
        '262': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd080', 'initialGuessFromCase': '0'},
        '263': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd120', 'initialGuessFromCase': '0'},
        '264': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'polynomialTag': 'abd140', 'initialGuessFromCase': '0'},
        '265': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'initialGuessFromCase': '257'},  # = 0, from short-stride basin
        '266': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd080',
                'initialGuessFromCase': '211'},
        '267': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd120',
                'initialGuessFromCase': '211'},
        '268': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'polynomialTag': 'abd140',
                'initialGuessFromCase': '211'},
        # (O) 11-16 robustness of the key conditions: cold start (N=25) and mesh refinement (N=50, hot start)
        #     baseline 0, ABC 211, ABC+AM 216.
        '269': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'guessType': 'coldStart'},
        '270': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036, 'guessType': 'coldStart'},
        '271': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036,
                'guessType': 'coldStart'},
        '272': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50},
        '273': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 1.036},
        '274': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'freeMomentTerm': 1, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036},
        # (P) 11-16 energy cost of restricting pelvic rotation: pelvisRotTerm continuation sweeps (warm start from
        #     the neighbouring solution; 95 = w_pel 3000 from IK landed on a short-stride local optimum).
        #     Nominal w_acc 50000: 0 / 90 (100) / 275 (300) / 91 (1000) / 276 (3000) / 92 (10000) / 277 (30000).
        '275': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'pelvisRotTerm': 300, 'initialGuessFromCase': '90'},
        '276': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'pelvisRotTerm': 3000, 'initialGuessFromCase': '91'},
        '277': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'pelvisRotTerm': 30000, 'initialGuessFromCase': '92'},
        #     Energy-dominated w_acc 2000: 82 / 278 (100) / 279 (300) / 280 (1000) / 281 (3000; cf. 93) / 282 (10000).
        '278': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 2000,
                'pelvisRotTerm': 100, 'initialGuessFromCase': '82'},
        '279': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 2000,
                'pelvisRotTerm': 300, 'initialGuessFromCase': '278'},
        '280': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 2000,
                'pelvisRotTerm': 1000, 'initialGuessFromCase': '279'},
        '281': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 2000,
                'pelvisRotTerm': 3000, 'initialGuessFromCase': '280'},
        '282': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'jointAccelerationTerm': 2000,
                'pelvisRotTerm': 10000, 'initialGuessFromCase': '281'},
        # (Q) 11-17 speed dependence of the cost of restricting pelvic rotation (nominal objective, continuation):
        #     0.8 m/s: 23 / 283 (300) / 284 (1000) / 285 (3000) / 286 (10000)
        #     1.6 m/s: 242 / 287 (300) / 288 (1000) / 289 (3000) / 290 (10000)
        '283': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'pelvisRotTerm': 300, 'initialGuessFromCase': '23'},
        '284': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'pelvisRotTerm': 1000, 'initialGuessFromCase': '283'},
        '285': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'pelvisRotTerm': 3000, 'initialGuessFromCase': '284'},
        '286': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'pelvisRotTerm': 10000, 'initialGuessFromCase': '285'},
        '287': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 300, 'initialGuessFromCase': '242'},
        '288': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 1000, 'initialGuessFromCase': '287'},
        '289': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 3000, 'initialGuessFromCase': '288'},
        '290': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 10000, 'initialGuessFromCase': '289'},
        # 287 (w_pel 300) reached a longer-stride basin with LOWER effort than the 1.6 baseline 242 -> rerun the
        # unrestricted 1.6 m/s case from that basin.
        '291': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'initialGuessFromCase': '287'},
        # 291 = lowest-cost 1.6 m/s baseline (pelvis 17.8 deg, stride 1.62 m). Check neighbouring speeds from it.
        '292': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'initialGuessFromCase': '291'},
        '293': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'initialGuessFromCase': '291'},
        # 293 == case 0 (same basin, obj 371.58 vs 371.71); 292 (1.45) beat 243 by 4.5% (pelvis 19.3 deg).
        # Complete the baseline speed series with cross-speed warm starts.
        '294': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'initialGuessFromCase': '24'},
        '295': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'initialGuessFromCase': '0'},
        '296': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'initialGuessFromCase': '292'},
        # 296 = lowest-cost 1.6 m/s baseline (pelvis 20.8 deg, COT 4.373); 294 ~ 23 (0.8 confirmed); 295 worse than 24.
        # Redo the 1.6 m/s pelvis-restriction curve from 296 (287-290 sat in the worse 291 basin).
        '297': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 300, 'initialGuessFromCase': '296'},
        '298': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 1000, 'initialGuessFromCase': '297'},
        '299': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 3000, 'initialGuessFromCase': '298'},
        '300': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'pelvisRotTerm': 10000, 'initialGuessFromCase': '299'},
        # ABC at 1.6 m/s warm-started from the 1.45 m/s ABC solution
        '301': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50,
                'GRMzTerm': 1, 'GRMzMode': 'free', 'fixedStrideTime': 0.931, 'initialGuessFromCase': '244'},
        # (S1) 11-17 'chimpanzee-like upper body': arms held and/or rigid waist (lockJoints, +/-1 deg about IK mean).
        #      With A + C + angular-momentum cost but NO free-moment cost, so the free moment is an outcome.
        '302': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036},  # AC+AM reference
        '303': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'lockJoints': ['arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l']},  # arms held
        '304': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'lockJoints': ['lumbar_rotation']},  # rigid waist
        '305': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'lockJoints': ['arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l'] + ['lumbar_rotation']},  # both
        #      Effort-only objective (no constraints, no AM cost):
        '306': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'lockJoints': ['arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l']},
        '307': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'lockJoints': ['lumbar_rotation']},
        '308': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'lockJoints': ['arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l'] + ['lumbar_rotation']},
        # (S2) 11-17 cadence landscape at 1.33 m/s, effort-only objective (free optimum: case 0, T = 1.124 s;
        #      212: T = 1.036 s). Warm start from case 0.
        '309': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 0.950, 'initialGuessFromCase': '0'},
        '310': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.000, 'initialGuessFromCase': '0'},
        '311': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.080, 'initialGuessFromCase': '0'},
        '312': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.170, 'initialGuessFromCase': '0'},
        '313': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.220, 'initialGuessFromCase': '0'},
        '314': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'fixedStrideTime': 1.280, 'initialGuessFromCase': '0'},
        # (T) 11-17 verification of A + C + AM without the free-moment cost (case 302) as the main condition
        #     speeds (C = human stride time, Grieve scaling), IK start vs warm start from ABC+AM at that speed
        '315': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.391},
        '316': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.391, 'initialGuessFromCase': '239'},
        '317': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.222},
        '318': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.222, 'initialGuessFromCase': '240'},
        '319': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.985},
        '320': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.985, 'initialGuessFromCase': '245'},
        '321': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.931},
        '322': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 0.931, 'initialGuessFromCase': '246'},
        #     1.33 m/s robustness: cold start, N = 50, warm start from 216 (ABC+AM)
        '323': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'guessType': 'coldStart'},
        '324': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 50, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036},
        '325': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'initialGuessFromCase': '216'},
        #     objective-weight sensitivity (w_acc 10 000 / 1000)
        '326': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'jointAccelerationTerm': 10000},
        '327': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'jointAccelerationTerm': 1000},
        #     decomposition given AM: AM only / A + AM / C + AM (302 = A + C + AM)
        '328': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '329': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '330': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036},
        # (U) 11-17 lateral-stability step-time cost (LIP noise amplification), free cadence.
        # stepStabTerm 1.66/3.49/7.26/14.5 = 5.7/12/25/50% of the metabolic term at the human step time (1.33 m/s).
        '331': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'stepStabTerm': 1.66, 'initialGuessFromCase': '0'},
        '332': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'stepStabTerm': 3.49, 'initialGuessFromCase': '0'},
        '333': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'stepStabTerm': 7.26, 'initialGuessFromCase': '0'},
        '334': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'stepStabTerm': 14.5, 'initialGuessFromCase': '0'},
        '335': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 1.66, 'initialGuessFromCase': '329'},
        '336': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 3.49, 'initialGuessFromCase': '329'},
        '337': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 7.26, 'initialGuessFromCase': '329'},
        '338': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 14.5, 'initialGuessFromCase': '329'},
        # A + AM + stepStabTerm 7.26 at other speeds (free cadence).
        '339': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 7.26, 'initialGuessFromCase': '316'},
        '340': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 7.26, 'initialGuessFromCase': '318'},
        '341': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 7.26, 'initialGuessFromCase': '320'},
        '342': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 7.26, 'initialGuessFromCase': '322'},
        # (V) 11-18 model-bias check: contact sphere stiffness x10 (repo variant), free cadence.
        '343': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25, 'initialGuessFromCase': '0'},
        '344': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '329'},
        '345': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25},
        # (W) 11-18 proportional stability cost: stepStabTerm set per speed so that it is 45% of the metabolic term
        # at the human step time (same fraction as case 338 at 1.33 m/s), A + AM, free cadence.
        '346': {'model': 'Hamner_modified', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 2.284, 'initialGuessFromCase': '316'},
        '347': {'model': 'Hamner_modified', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 5.005, 'initialGuessFromCase': '318'},
        '348': {'model': 'Hamner_modified', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 19.726, 'initialGuessFromCase': '320'},
        '349': {'model': 'Hamner_modified', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'stepStabTerm': 30.739, 'initialGuessFromCase': '322'},
        # (X) 11-18 stiffer contacts (x10): A+AM from IK guess; speed series of the baseline objective (IK guess / warm start).
        '350': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum'},
        '351': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 0.8, 'N': 25},
        '352': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.0, 'N': 25},
        '353': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.45, 'N': 25},
        '354': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.6, 'N': 25},
        '355': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 0.8, 'N': 25, 'initialGuessFromCase': '294'},
        '356': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.0, 'N': 25, 'initialGuessFromCase': '24'},
        '357': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.45, 'N': 25, 'initialGuessFromCase': '292'},
        '358': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.6, 'N': 25, 'initialGuessFromCase': '296'},
        # (Y) 11-18 stiffer contacts + A + AM, free cadence (no C): warm starts from A+C+AM solutions and from stiff baseline.
        '359': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '316'},
        '360': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '318'},
        '361': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '302'},
        '362': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '320'},
        '363': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '322'},
        '364': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 0.8, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '355'},
        '365': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.0, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '352'},
        '366': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '345'},
        '367': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.45, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '353'},
        '368': {'model': 'Hamner_modified_stifferContacts', 'targetSpeed': 1.6, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 3, 'GRMzMode': 'pelvis_sum', 'initialGuessFromCase': '354'},
        # (Z) 11-18 AM weight dose-response in the main condition A+C+AM (302 = weight 3; 214 = weight 0), warm start from 302.
        '369': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 1, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'initialGuessFromCase': '302'},
        '370': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 10, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'initialGuessFromCase': '302'},
        '371': {'model': 'Hamner_modified', 'targetSpeed': 1.33, 'N': 25, 'hipRotStiffness': 50, 'subtalarStiffness': 50, 'GRMzTerm': 30, 'GRMzMode': 'pelvis_sum', 'fixedStrideTime': 1.036, 'initialGuessFromCase': '302'},
    }

    return settings
