# Healthcare Claims Cost Predictor — Student Starter

Over eight weeks you will build a machine learning system that predicts which health-plan members are likely to become high-cost and deploy it as a public REST API that anyone can call.



The data is entirely synthetic. It is generated on your own machine, no real patients, no PHI. That is exactly why this repo can be public. When you work with real claims data in a job, none of it goes anywhere near GitHub.

---

## Table of contents

1. [Start here: environment setup](#start-here-environment-setup)
2. [How this repo works](#how-this-repo-works)
3. [Your own cohort](#your-own-cohort)
4. [The weekly rhythm](#the-weekly-rhythm)
5. [Git workflow](#git-workflow)
6. [Running the API locally](#running-the-api-locally)
7. [What to commit](#what-to-commit)
8. [Getting help](#getting-help)

---

## Start here: environment setup

**→ [SETUP.md](SETUP.md)**

Week 1 is getting a working local environment: claiming the GitHub Student Developer Pack, installing Python 3.11, making your own copy of this repo, creating a virtual environment, setting your assigned seed, and running your first tests. It is a separate guide so you can follow it start to finish without scrolling past things you do not need yet.

Come back here when `python check_env.py` passes.

---

## How this repo works

Every week has a **starter file** with `TODO`s and a **test file** that tells you
whether what you wrote is correct. You never have to wait for a session to find
out if you are on the right track.

| Week | Topic | You fill in | You check with |
|---|---|---|---|
| 1 | Setup ([SETUP.md](SETUP.md)) | — | `python check_env.py` |
| 2 | The claims domain, EDA | a notebook in `notebooks/` | `pytest tests/test_data.py` |
| 3 | Features & target leakage | `features.py` | `pytest tests/test_features.py` |
| 4 | Train a baseline | `train.py` | `pytest tests/test_leakage.py tests/test_model.py` |
| 5 | Evaluation & thresholds | `evaluate.py` | `pytest tests/test_evaluation.py` |
| 6 | Fairness audit | `fairness.py` | `pytest tests/test_fairness.py` |
| 7 | Deploy with FastAPI | `app/schemas.py`, `app/main.py` | `pytest tests/test_api.py` |
| 8 | Presentations | your slides | your peers |

Three things to know about the tests:

- **A test for code you have not written yet skips — it does not fail.** Early on, most of the suite skips. That is expected. Skips turn into passes as you go.
- **The failure message is the point.** Each one says what is wrong and where to look. If a message is ever unhelpful,  please call it out. That is a bug in the test and it's not on you.

One deliberate exception: `tests/test_leakage.py` fails from day one. Finding out why is the Week 4 exercise. Leave it alone until then.

---

## Your own cohort

`STUDENT_SEED` controls which synthetic members you get. Everything downstream is specific to your data: prevalence, feature importances, which demographic group the model treats worse, the fairness story you end up writing.

Same seed, same data, byte for byte — reproducibility you can verify: `pytest tests/test_data.py -k seed`. Different seed, genuinely different project.

This means your results will not match your neighbour's, and that is the point. Comparing them ("why is your disparity bigger than mine?") is a real conversation instead of a copying check. Put your seed on your title slide in Week 8.

Changing the seed changes the label, so regenerate **and** retrain afterwards:

```bash
export STUDENT_SEED=2
python generate_claims_data.py
python train.py
```

---

## The weekly rhythm

1. `git checkout main && git pull origin main`
2. `git checkout -b week-04` (see [Git workflow](#git-workflow))
3. Open the week's starter file and work through the `TODO`s
4. Run that week's tests until they pass
5. Commit, push, open a PR in your own repo
6. Get a peer review, address the comments, merge
7. Pull `main` back down before starting the next week

Weeks build on each other — Week 5 needs the model your Week 4 code saved — so
merge each week before branching for the next one.

---

## Git workflow

### One branch per week

```bash
git checkout main
git pull origin main               # make sure you have last week's merged work
git checkout -b week-04

# ... work, in small commits ...
git add -A
git commit -m "Week 4: stratified split and baseline pipeline"
git push origin week-04
```

Then open a pull request into your own `main`. Both sides of the PR should show your username. 

`main` is protected, so this is the only way in: pushing to it directly is rejected, and merging asks for one approval. See [SETUP.md → Step 4](SETUP.md#step-4-protect-your-main-branch).

### If last week's PR is not merged yet

Branch off the previous week's branch instead of `main`, so you keep your own
work:

```bash
git checkout week-04
git checkout -b week-05
```

### Peer review

You will be paired to review each other's PRs.

> **Open your own PR for a week before you read anyone else's.** This is the
> one rule that matters. It means nobody sees a solution to a problem they have
> not already worked through, so there is no reason to go looking early and
> nothing lost by sharing once you have.
>
> Note it is *open*, not *merge*. Merging needs your partner's approval, and if
> you each waited for your own merge before reviewing the other, neither of you
> could ever merge. Push your work, open the PR, then go and review theirs.

Your reviewer needs to be able to see your repo. If yours is public, they
already can. If it is private, add them under **Settings → Collaborators**, and
remove them at the end of the course if you like.

Your seeds are different, so their numbers will never match yours. Do not treat
a different ROC-AUC or a different disadvantaged group as a mistake — ask how
they got there.

A useful review is specific. Things worth commenting on:

- Does the relevant test suite pass? Check the green tick on the PR.
- Any leaky features? Would you defend every column in the feature list?
- Is the chosen threshold justified with a trade-off, or just asserted?
- Do the numbers in the write-up come from this person's own seed?
- Is anything in a notebook that should be in a `.py` file so it can be tested?

"Looks good 👍" is not a review. Ask one real question per PR. It's also great to complement the work done if you think they have a good solution.

### Pulling in course updates

When your Fellow announces an update:

```bash
git checkout main
git pull upstream main --no-rebase
git push origin main
```

Course updates only touch files you do not edit (`tests/`, docs), so this should be conflict-free. If git does report a conflict, stop and ask rather thanguessing — resolving one badly can lose your work.

---

## Running the API locally

From Week 7, once `app/main.py` is implemented:

```bash
uvicorn app.main:app --reload --port 8000
```

- Interactive docs: http://localhost:8000/docs
- Liveness check: http://localhost:8000/health

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age_bucket": "50-59",
    "sex": "F",
    "region": "Northeast",
    "total_claims": 18,
    "medical_claims": 14,
    "pharmacy_claims": 4,
    "specialty_drug_fills": 2,
    "total_billed_cents": 2400000,
    "unique_diagnosis_codes": 7,
    "inpatient_claims": 1,
    "has_specialty_drug": true
  }'
```

Send the fields **your** model was trained on — if you settled on a different feature list in Week 4, adjust the payload to match. To see the exact list:

```bash
python -c "import joblib; print(list(joblib.load('model.joblib')['preprocessor'].feature_names_in_))"
```

### Deploying to Render (Week 7)

`render.yaml` is already set up. In Render: **New → Blueprint**, connect your repo, and set `STUDENT_SEED` to your seed in the dashboard. Render reruns data generation and training on every deploy, so your local `model.joblib` is never uploaded — the cloud service trains its own copy from your code.

The free tier sleeps after 15 minutes of inactivity; the first request after that takes 30–60 seconds. Warm it up before you demo.

---

## What to commit

**Commit:** your starter files, your notebooks, your reports.

**Do not commit:** `data/`, `model.joblib`, `.venv/`, `reports/` output, `__pycache__/`. All of these are already in `.gitignore` — they are generated artifacts, and anyone with your code and your seed can reproduce them exactly. That is the point of a reproducible pipeline.

If `git status` ever shows a 700 KB `.joblib` file as untracked-and-about-to-be-added, something is wrong with your `.gitignore`.

---

## Getting help

Bring three things and you will almost always get unstuck fast:

1. What you expected to happen
2. What actually happened — the **full** error message, copied as text
3. The output of `python check_env.py`

Asking well is a professional skill. 