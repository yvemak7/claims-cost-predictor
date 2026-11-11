"""
WEEK 6 STARTER — audit the model across demographic groups.

The model is one number per member. A fairness audit asks whether that number
is equally wrong for everybody, and "equally wrong" turns out to have several
mutually incompatible definitions.

Fill in every section marked TODO. When you run this file it should:
  1. Score every member with the trained model
  2. Report per-group rates for sex and age_bucket
  3. Apply the 80% rule
  4. Compare against a model retrained without the demographic columns
  5. Write reports/fairness_report.md

Run:
    python fairness.py

Check your work:
    pytest tests/test_fairness.py -v
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn import clone
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import HIGH_COST_THRESHOLD_USD
from train import TEST_SIZE, RANDOM_STATE, CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET, load_data

DATA_PATH = Path("data/member_summary.csv")
MODEL_PATH = Path("model.joblib")
REPORT_PATH = Path("reports/fairness_report.md")

PROTECTED_COLUMNS = ["sex", "age_bucket"]
DECISION_THRESHOLD = 0.1  # swap in the threshold you defended in Week 5

# ---------------------------------------------------------------------------
# TODO 6 — your written assessment.
#
# After you have the numbers, fill this in. It is graded on whether the claim
# follows from your own cohort's numbers, not on whether it is reassuring.
# Reference specific rates. Name the group that is worse off. If a subgroup is
# too small to conclude anything, say that instead of reporting a ratio to two
# decimal places as if it meant something.
# ---------------------------------------------------------------------------
ASSESSMENT = """
"The fairness audit shows that sex passes the 80% rule (ratio 0.815), with females flagged slightly 
more often than males (13.02% vs. 10.60%). Age shows a larger disparity (ratio 0.293), with members 
aged 18–29 flagged least often (5.28%) compared to ages 60–64 (18.04%). However, the youngest group 
also has a much lower actual high-cost rate (1.76% vs. 8.76%) and only five high-cost members, 
limiting conclusions. Ages 40–49 have the highest false negative rate (6.12%). Removing demographic 
features improves the ratios for sex (0.815 to 0.931) and age (0.293 to 0.352), but age disparity 
remains, possibly due to other features acting as demographic proxies. Since the audit includes 
training data, these findings should be interpreted cautiously.
"""

def confusion_counts(y_true, y_pred) -> dict[str, int]:
    """
    TODO 1 — return {"tp": .., "fp": .., "fn": .., "tn": ..}.

    Write it with vectorized comparisons rather than a loop. Both inputs are
    0/1 arrays or Series.
    """

    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def group_metrics(df: pd.DataFrame, group_col: str,
                  y_true_col: str = "y_true", y_pred_col: str = "y_pred") -> pd.DataFrame:
    """
    TODO 2 — one row per group value, with these columns:

        group, n, base_rate, positive_rate, tpr, fpr, fnr, precision

        n              members in the group
        base_rate      share of the group that is actually high-cost
        positive_rate  share of the group the model flags   (demographic parity)
        tpr            of the actually-high-cost, share flagged
        fpr            of the actually-normal, share flagged (equalized odds)
        fnr            1 - tpr; the members the model misses
        precision      of the flagged, share actually high-cost

    Build it on top of confusion_counts(). Sort by group so the output is stable
    across runs. Guard the divisions: a group with zero actual positives has no
    TPR, and reporting 0.0 there is a lie — use np.nan.
    """
    rows = []
    for group, group_df in df.groupby(group_col):
        counts = confusion_counts(group_df[y_true_col], group_df[y_pred_col])
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        tn = counts["tn"]

        n = tp + fp + fn + tn
        base_rate = (tp+fn) / n if n > 0 else np.nan
        positive_rate = (tp+fp) / n if n > 0 else np.nan
        tpr = tp/(tp+fn) if (tp+fn) > 0 else np.nan
        fpr = fp/(fp+tn) if (fp+tn) > 0 else np.nan
        fnr = 1-tpr if not np.isnan(tpr) else np.nan
        precision = tp/(tp+fp) if (tp+fp) > 0 else np.nan

        rows.append({
            "group": group,
            "n": n,
            "base_rate": base_rate,
            "positive_rate": positive_rate,
            "tpr": tpr,
            "fpr": fpr,
            "fnr": fnr,
            "precision": precision
        })
    
    return pd.DataFrame(rows).sort_values("group").reset_index(drop=True)



def disparate_impact_ratio(rates: pd.Series) -> float:
    """
    TODO 3 — the four-fifths ratio: the lowest rate divided by the highest.

    Ignore nan rates. Returns a number in [0, 1], where 1.0 is exact parity.
    """
    rates = rates.dropna()
    if len(rates) == 0:
        return np.nan
    highest = rates.max()
    lowest = rates.min()

    return lowest / highest if highest > 0 else np.nan


def passes_80_percent_rule(ratio: float) -> bool:
    """
    TODO 4 — True when the ratio clears the EEOC four-fifths guideline.

    Careful with the boundary: exactly 0.80 passes.
    """
    return bool(ratio >= 0.80)


def blind_model_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO 5 — retrain without the demographic columns and re-audit.

    `df` arrives with y_true / y_pred already on it from the full model. Score
    the blind model yourself rather than reusing those columns, so the two
    numbers you compare come from two actual models.

    Steps:
      - take the fitted pipeline's feature list, drop PROTECTED_COLUMNS
      - build and fit a pipeline of the same shape on the same training split
      - score, threshold, and run group_metrics() again per protected column
      - return a DataFrame with one row per protected column and the disparate
        impact ratio with the demographic features and without, side by side

    Predict the result before you run it, in one sentence: ____________________

    Most students expect the disparity to disappear. Whatever you find, the
    interesting question is *why*. Which remaining columns carry the same
    information the demographic columns did? Check with:
        df.groupby("sex")[numeric_cols].mean()
    """
    pipeline = joblib.load(MODEL_PATH)
    full_df = load_data()

    original_features = list(pipeline["preprocessor"].feature_names_in_)
    blind_features = [col for col in original_features if col not in PROTECTED_COLUMNS]

    cat_cols = [col for col in blind_features if full_df[col].dtype == "object"]
    num_cols = [col for col in blind_features if col not in cat_cols]

    processor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
        ]
    )
    
    X = full_df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = full_df[TARGET].astype(int)


    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE
)
    blind_pipeline = Pipeline([('preprocessor', processor), ('classifier', clone(pipeline.steps[-1][1]))])

    blind_pipeline.fit(
        X_train[blind_features],
        y_train
    )

    blind_y_proba = blind_pipeline.predict_proba(df[blind_features])[:, 1]

    threshold = DECISION_THRESHOLD

    blind_y_pred = (blind_y_proba >= threshold).astype(int)

    blind_df = df.copy()
    blind_df["y_pred"] = blind_y_pred

    row = []
    for col in PROTECTED_COLUMNS:
        table = group_metrics(blind_df, col)
        ratio = disparate_impact_ratio(table.set_index("group")["positive_rate"])
        row.append({
            "protected_column": col,
            "disparate_impact_with_demo": disparate_impact_ratio(group_metrics(df, col).set_index("group")["positive_rate"]),
            "disparate_impact_without_demo": ratio
        })
    return pd.DataFrame(row).sort_values("protected_column").reset_index(drop=True)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    pipeline = joblib.load(MODEL_PATH)

    features = list(pipeline["preprocessor"].feature_names_in_)
    scored = df.assign(
        y_true=df["is_high_cost"].astype(int),
        y_proba=pipeline.predict_proba(df[features])[:, 1],
    )
    scored["y_pred"] = (scored["y_proba"] >= DECISION_THRESHOLD).astype(int)

    print(f"Auditing at threshold {DECISION_THRESHOLD} "
          f"(label: >${HIGH_COST_THRESHOLD_USD:,} plan-paid)")

    lines = [f"# Fairness audit\n", f"Decision threshold: {DECISION_THRESHOLD}\n"]
    for col in PROTECTED_COLUMNS:
        table = group_metrics(scored, col)
        ratio = disparate_impact_ratio(table.set_index("group")["positive_rate"])
        verdict = "PASS" if passes_80_percent_rule(ratio) else "FAIL"

        print(f"\n=== {col} ===")
        print(table.to_string(index=False))
        print(f"disparate impact ratio (positive rate): {ratio:.3f} → {verdict}")

        lines += [f"\n## {col}\n", table.to_markdown(index=False),
                  f"\n\nDisparate impact ratio: {ratio:.3f} ({verdict})\n"]

    print("\n=== Blind model comparison ===")
    comparison = blind_model_comparison(scored)
    print(comparison.to_string(index=False))
    lines += ["\n## Blind model comparison\n", comparison.to_markdown(index=False),
              f"\n\n## Assessment\n\n{ASSESSMENT}\n"]

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines))
    print(f"\nReport written to {REPORT_PATH}")


if __name__ == "__main__":
    main()
