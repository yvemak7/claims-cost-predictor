"""
Project-wide configuration.

Every knob here is read once from the environment so the same code produces a
different-but-reproducible project per student.

  HIGH_COST_THRESHOLD_USD  dollar threshold that defines the positive label.
                           Flows through the data generator (label assignment),
                           training (reporting), and the API (response metadata).
  STUDENT_SEED             random seed for the synthetic cohort. Set this to
                           your own assigned seed before generating data: your
                           prevalence, feature importances, and subgroup
                           disparities will differ from everyone else's, so your
                           numbers and your write-up have to be your own.
  N_MEMBERS                size of the synthetic member cohort.

Changing the seed or the threshold changes the *data*, so regenerate and
retrain after touching either one:

    STUDENT_SEED=2 python generate_claims_data.py
    STUDENT_SEED=2 python train.py
"""
import os

HIGH_COST_THRESHOLD_USD = int(os.environ.get("HIGH_COST_THRESHOLD_USD", 25_000))
HIGH_COST_THRESHOLD_CENTS = HIGH_COST_THRESHOLD_USD * 100

STUDENT_SEED = int(os.environ.get("STUDENT_SEED", 2))
N_MEMBERS = int(os.environ.get("N_MEMBERS", 2_000))
