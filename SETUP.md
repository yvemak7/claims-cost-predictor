# Week 1 — Set up your environment

Work through this before the Week 2 session. It takes about 20 minutes when nothing goes wrong, and [Troubleshooting](#troubleshooting) covers it when something does.

When `python check_env.py` passes, you are done — go back to [README.md](README.md) for how the project works week to week.

---

## Contents

- [Accounts you need](#accounts-you-need)
- [Step 0: claim the GitHub Student Developer Pack](#step-0-claim-the-github-student-developer-pack)
- [Step 1: install Python 3.11](#step-1-install-python-311)
- [Step 2: create an empty repo on GitHub](#step-2-create-an-empty-repo-on-github)
- [Step 3: clone the course repo and point it at yours](#step-3-clone-the-course-repo-and-point-it-at-yours)
- [Step 4: protect your `main` branch](#step-4-protect-your-main-branch)
- [Step 5: create a virtual environment](#step-5-create-a-virtual-environment)
- [Step 6: install the dependencies](#step-6-install-the-dependencies)
- [Step 7: set your assigned seed](#step-7-set-your-assigned-seed)
- [Step 8: check your setup](#step-8-check-your-setup)
- [Step 9: generate your data and run your first tests](#step-9-generate-your-data-and-run-your-first-tests)
- [Step 10: rehearse the git workflow](#step-10-rehearse-the-git-workflow)
- [Troubleshooting](#troubleshooting)

---

## Accounts you need

| Account | Cost | When you need it | Why |
|---|---|---|---|
| **GitHub** | free | Week 1 | Your copy of this repo is where all your work lives |
| **Render** | free tier | Week 7 | Hosts your deployed API. Sign in with GitHub; no card required |
| **GitHub Student Developer Pack** | free | Week 1 (verification takes time) | See [Step 0](#step-0-claim-the-github-student-developer-pack) |

You also need **git** installed, and a terminal you are comfortable in.

---

## Step 0: claim the GitHub Student Developer Pack

**→ https://education.github.com/pack**

Do this first if you have not already done so, before anything else in this guide. Verification can take anywhere from a few minutes to a few days, so start it now and carry on with the rest of the setup while it processes.

The pack is free for enrolled students and gives you paid developer tools at no cost for as long as you are studying. The ones that matter for this project:

| Offer | What you get | Why it is useful here |
|---|---|---|
| **GitHub Pro** | Free while you are a student | Unlimited private repos with collaborators, and better insights on your own repo |
| **GitHub Copilot** | Free for verified students | An AI pair programmer in your editor. |
| **JetBrains** | Free PyCharm Professional (and the rest of the suite) | A full Python IDE with a real debugger, if you would rather not use VS Code |
| **Microsoft Azure** | $100 credit | An alternative place to deploy if you outgrow Render's free tier |
| **Heroku** | $13/month credit for 24 months | Another deployment target worth knowing |
| **DataCamp / Educative / Frontend Masters** | Several months free | Structured courses on pandas, SQL, and ML if you want more depth than eight weeks allows |
| **Namecheap / Name.com** | A free domain + SSL certificate | Put your deployed API on a real domain for your portfolio |
| **Notion, Microsoft 365** | Education plans | Notes, slides for your Week 8 presentation |

### How to apply

1. Go to https://education.github.com/pack and click **Sign up for Student Developer Pack**
2. Sign in with the GitHub account you will use for this course
3. Verify you are a student. The fastest route is adding your **school-issued email address** to your GitHub account. If you do not have one, GitHub will ask you to upload dated proof of enrollment (a student ID with a current date, a transcript, or an enrollment letter)
4. Wait for the approval email, then claim individual offers from the pack page as required. Each offer is redeemed separately. (Being approved does not automatically turn them all on)

### A note on Copilot and AI assistants

Copilot is in the pack and you are welcome to use it or any other AI tool of your choice. Knowing how to work with these tools is part of the job now. Two things worth being deliberate about:

- **You will be asked to explain your code.** In peer review and in your final week activity, "Copilot wrote it" is not an answer to "why did you choose this threshold?" Use it to go faster on things you understand, and to explain things you don't.
- **It will happily hand you a leaky feature.** An autocomplete has no idea which of your columns are observable at prediction time. That judgment is the whole point of Weeks 3 and 4, and it is exactly what the tests check.

---

## Step 1: install Python 3.11

This project pins its dependencies to versions that work on **Python 3.11**
(3.12 also works). **Python 3.13 does not** — the pinned numpy and scikit-learn
have no prebuilt packages for it, and `pip install` will fail.

### macOS

```bash
brew install python@3.11          # install Homebrew first from brew.sh
python3.11 --version              # should print Python 3.11.x
```

### Ubuntu / Debian

```bash
sudo apt update && sudo apt install python3.11 python3.11-venv
python3.11 --version              # should print Python 3.11.x
```

The `python3.11-venv` package matters — without it, Step 5 fails with an error
about `ensurepip`.

### Windows

1. Download the **Windows installer (64-bit)** from [python.org](https://www.python.org/downloads/release/python-3119/) Scroll to the bottom of that page, under *Files*.

   - Do **not** install Python from the Microsoft Store. It sandboxes file access in ways that cause confusing failures later.

2. Run the installer. On the very first screen, before clicking anything else:

   - **Tick "Add python.exe to PATH"** at the bottom of the window. It is easy
     to miss, and missing it is the single most common cause of
     `python: command not found` later on.
   - Then click **Install Now**.

3. **Close every terminal window you already had open.** A running terminal will
   not pick up the new PATH. Open a fresh **PowerShell**.

4. Check it worked:

   ```powershell
   py --version              # should print Python 3.11.x
   py -0                     # lists every Python the launcher can see
   ```

`py` is the Python launcher that ships with the Windows installer, and it is the
reliable way to reach a specific version. **Wherever this guide says
`python3.11`, type `py -3.11` instead.**

<details>
<summary>Typing <code>python</code> opens the Microsoft Store instead of Python</summary>

Windows ships a placeholder that hijacks the `python` command. Either use `py`
everywhere instead, or switch the placeholder off:

**Settings** → **Apps** → **Advanced app settings** → **App execution aliases**,
then turn off both **python.exe** and **python3.exe**.

</details>

<details>
<summary>Which terminal should I use on Windows?</summary>

**PowerShell** is what this guide assumes. It comes with Windows — search for it
in the Start menu.

**Windows Terminal** (free, from the Microsoft Store) is a nicer host that runs PowerShell inside it. Optional, but worth it if you are spending eight weeks here.

**Git Bash** comes with Git for Windows and behaves like a macOS/Linux shell. It works fine, but the environment activation command differs — see Step 5.

Avoid the old **cmd.exe** unless you have a reason to use it.

</details>

---

## Step 2: create an empty repo on GitHub

On GitHub, click **+** → **New repository**.

- **Owner:** your own account
- **Repository name:** `claims-cost-predictor`
- **Visibility:** **Public**. The data is synthetic, so there is nothing to protect, and a finished project is worth showing people. It also matters practically: branch protection (Step 4) is free on public repos but needs GitHub Pro on private ones, and your Student Pack approval may not have come through yet.
- **Do not tick** "Add a README file", "Add .gitignore", or "Choose a license".

> **The repo has to be completely empty.** Any of those three tick-boxes creates a commit, and the push in Step 3 will then be rejected. If you have already made one with a README, delete it and make another.

GitHub will show you a "quick setup" page with some suggested commands. Ignore it — Step 3 is different, and better.

---

## Step 3: clone the course repo and point it at yours

You are about to make a copy of the course repo that belongs to you. Four commands, and the third is the interesting one.

```bash
git clone --single-branch --branch main \
  https://github.com/sivakarthik51/claims-cost-predictor-starter.git \
  claims-cost-predictor

cd claims-cost-predictor

git remote rename origin upstream
git remote add origin https://github.com/YOUR-USERNAME/claims-cost-predictor.git

git push -u origin main
```

Use **your** username on the `git remote add origin` line.

What just happened, because this is worth understanding rather than pasting:

- **`git clone`** copied the course repo, full history included, onto your
  machine. `--single-branch` takes only `main`, so nothing else the course repo
  holds comes with it.
- **`git remote rename origin upstream`** renames where it came from. By
  convention `origin` is *your* repo and `upstream` is the one you track, and
  right now they are the wrong way round.
- **`git remote add origin ...`** points `origin` at the empty repo you just
  made, so pushes go to you.
- **`git push -u origin main`** uploads everything and sets `main` to track
  your repo from now on.

Check it looks right:

```bash
git remote -v
```

`origin` should have **your** username and `upstream` should have the course's.
If they are swapped, redo the two `git remote` lines.

> **Why not just fork it?** A fork stays permanently linked to the repo it came
> from, and GitHub uses that link in a way that will bite you: when you open a
> pull request, it points at the *course* repo by default, not yours. Miss that
> dropdown once and your solution is a public PR that the whole class can read.
> This way there is no link, so your PRs can only go where they belong.
>
> Keeping the history matters too — that is what makes course updates merge
> cleanly instead of conflicting on every file you have touched.

---

## Step 4: protect your `main` branch

Set this up now, before there is anything to lose. It makes `main` behave the way a shared branch behaves on a real team: nothing lands on it except through a reviewed pull request.

**Settings → Rules → Rulesets → New ruleset → New branch ruleset**

1. **Ruleset name:** `protect main`
2. **Enforcement status:** Active
3. **Bypass list** → *Add bypass* → **Repository admin**, then change its mode
   from *Always* to **For pull requests only**
4. **Target branches** → *Add target* → **Include default branch**
5. Under **Rules**, tick:
   - **Restrict deletions**
   - **Block force pushes**
   - **Require a pull request before merging**, and set **Required approvals** to **1**
6. **Create**

From now on `git push origin main` is rejected outright. You will have to branch, open a PR and get it reviewed. That is the point.

The bypass in step 3 is a deliberate escape hatch, and it is narrow. You cannot push to `main` directly no matter what, but if your review partner is ill the week your work is due, you can merge your own PR without their approval rather than being stuck. Use it when you have to, not by default: the review is the part you are here for.

> **You can never approve your own pull request.** GitHub does not allow it, on any plan. Without the bypass above, one unavailable partner would block your whole week.

---

## Step 5: create a virtual environment

A virtual environment keeps this project's packages separate from everything else on your machine. Create it once, inside the repo folder. Activate it in every terminal you work in.

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

If the second line fails with **"running scripts is disabled on this system"**,
PowerShell is blocking the activation script. Allow locally-created scripts for
your own account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Answer `Y`, then run the activate line again. This is a one-time fix, and it
does not weaken anything you download from the internet — those stay blocked.

<details>
<summary>Activating in cmd.exe or Git Bash instead</summary>

The environment is the same; only the activation script differs:

| Shell | Command |
|---|---|
| PowerShell | `.venv\Scripts\Activate.ps1` |
| cmd.exe | `.venv\Scripts\activate.bat` |
| Git Bash | `source .venv/Scripts/activate` |

Note that Git Bash uses `Scripts`, not `bin` — it is still a Windows
environment even though the shell looks like Linux.

</details>

### Check it worked

Your prompt should now start with `(.venv)`:

```
(.venv) PS C:\Users\you\claims-cost-predictor>      # Windows
(.venv) you@laptop claims-cost-predictor %          # macOS
```

If it doesn't, the environment is not active and the next step will install into
the wrong Python. Confirm which one you are on:

```bash
python --version            # should say 3.11.x
```

> **Every new terminal starts deactivated.** Activating is not permanent. When  something fails tomorrow morning with `ModuleNotFoundError`, check whether your prompt still says `(.venv)` before you check anything else.

---

## Step 6: install the dependencies

With `(.venv)` active, from inside the repo folder:

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

`requirements.txt` is what the deployed service needs. `requirements-dev.txt` is that plus the tools for the weekly exercises (pytest, matplotlib, jupyter), so install the `-dev` one locally.

Inside an active environment, plain `python` and `pip` already point at the right 3.11 — the `py -3.11` form is only needed to *create* the environment.

If `pip` appears to install things but `python` then cannot import them, one of the two ran outside the environment. Check where each resolves to:

```powershell
where.exe python            # Windows — first hit should be inside .venv\Scripts
```

```bash
which python                # macOS / Linux — should be .../.venv/bin/python
```

---

## Step 7: set your assigned seed

Your Fellow will give you a number. It decides which synthetic members you get,
and therefore every result you report for eight weeks.

### macOS / Linux

```bash
export STUDENT_SEED=2             # use YOUR number
```

`export` only lasts for the current terminal. To make it stick, add that line to `~/.zshrc` (macOS default) or `~/.bashrc` (most Linux), then open a new terminal.

### Windows

```powershell
setx STUDENT_SEED 2
```

`setx` saves the value permanently — but **it does not apply to the terminal you
typed it in**. Close that window and open a new one. To also set it for the
session you are in right now:

```powershell
$env:STUDENT_SEED = "2"            # PowerShell
```

```
set STUDENT_SEED=2                # cmd.exe
```

### Confirm it took, on any platform

```bash
python -c "import os; print(os.environ.get('STUDENT_SEED'))"
```

If that prints `None`, the seed is not set *in this terminal* and you will generate the wrong cohort. There is more on why this matters in
[README.md → Your own cohort](README.md#your-own-cohort).

---

## Step 8: check your setup

```bash
python check_env.py
```

This prints one line per check: Python version, packages, git remotes, seed, data. Fix anything marked `FAIL`. Lines marked `warn` are worth tidying but will not block you.

---

## Step 9: generate your data and run your first tests

```bash
python generate_claims_data.py
pytest tests/test_data.py
```

You should see three CSVs written to `data/`, a prevalence figure printed (somewhere around 5–8%), and **nine passing tests**. That is a working environment.

Run the whole suite if you are curious — `pytest` — and expect a screen full of skips. Tests for code you have not written yet skip rather than fail. One test in `tests/test_leakage.py` fails from day one; finding out why is the Week 4 exercise, so leave it alone until then.

---

## Step 10: rehearse the git workflow

Do this now, while there is nothing to lose. The full weekly workflow is in [README.md → Git workflow](README.md#git-workflow).

```bash
git checkout -b week-01-setup
# make a small change — write your assigned seed into notebooks/README.md, say
git add -A
git commit -m "Week 1: environment set up"
git push origin week-01-setup
```

Then open a pull request on GitHub. Because your repo is not a fork, the base will already be your own `main` — both sides of the PR should show your username.

GitHub will tell you **"Review required"** and grey out the merge button. That is the ruleset from Step 2 doing its job. For this rehearsal only, use the bypass: click **Merge without waiting for requirements to be met**. From Week 2 on, that button is for emergencies — the normal path is a partner's approval.

Then come back to `main`:

```bash
git checkout main
git pull origin main
```

That is the loop you will repeat every week. You are set up.

---

## Troubleshooting

| Symptom | What is going on | Fix |
|---|---|---|
| `pip install` fails building numpy or scikit-learn from source | You are on Python 3.13+. The pinned versions have no wheels for it. | Install Python 3.11, delete `.venv`, recreate it with `python3.11 -m venv .venv` (`py -3.11 -m venv .venv` on Windows) |
| `python: command not found` | Some systems only have `python3` | Use `python3` (macOS/Linux) or `py -3.11` (Windows) |
| Windows: typing `python` opens the Microsoft Store | Windows' placeholder app is intercepting the command | Use `py` instead, or turn off the aliases — see [Step 1](#step-1-install-python-311) |
| Windows: `py` is not recognised either | "Add python.exe to PATH" was unticked during install | Re-run the python.org installer, choose **Modify**, and tick it — or just reinstall |
| Windows: *"running scripts is disabled on this system"* | PowerShell blocks the activation script by default | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again |
| Windows: `.venv\Scripts\activate` does nothing in Git Bash | Wrong activation script for that shell | `source .venv/Scripts/activate` |
| Windows: git or pip errors about locked or permission-denied files | The repo is inside a OneDrive- or Dropbox-synced folder | Clone to a plain local path such as `C:\Users\you\code\` |
| `ModuleNotFoundError: No module named 'pandas'` | The virtual environment is not active, or you installed before activating | `source .venv/bin/activate` (`.venv\Scripts\Activate.ps1` on Windows), then `pip install -r requirements-dev.txt` |
| Prompt has no `(.venv)` | Environment not activated in this terminal | Activate it again — every new terminal needs it |
| `pytest: command not found` | Same cause as above | Activate the venv, or run `python -m pytest` |
| `pip` installs fine but `python` cannot import it | pip and python are resolving to different installs | `where.exe python` (Windows) or `which python` — it should point inside `.venv` |
| Windows: `STUDENT_SEED` is empty in a new terminal | `setx` does not affect already-open terminals | Open a new terminal, or `$env:STUDENT_SEED = "7"` for this session |
| Tests error with "not a git repository" | You downloaded a zip instead of cloning | Clone your repo with `git clone` |
| `model.joblib exists but will not load` | The file was saved by a different scikit-learn version | Delete it and retrain: `python train.py` |
| Your numbers match nobody else's, wildly | `STUDENT_SEED` unset or different from your assigned one | `echo $STUDENT_SEED`, fix it, then regenerate data **and** retrain |
| `python generate_claims_data.py` prints a different prevalence than last week | You changed the seed or the threshold | Expected — the label is baked into the data at generation time |
| Student Pack application still pending | Verification can take a few days | Nothing in Weeks 1–7 depends on it. Carry on |

Still stuck? Run `python check_env.py` and bring its full output — see
[README.md → Getting help](README.md#getting-help).
