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
    }

    return settings
