# Scorecard Workflow — Master File

Single source of truth for this project. Every Antigravity prompt refers to a step number **here**, so you never paste the whole plan again.

- **Project:** Bank-style credit scorecard and PD model
- **Dataset:** *Give Me Some Credit* (Kaggle), `cs-training.csv`, ~150,000 borrowers, 10 features, target `SeriousDlqin2yrs`, **6.68% defaults** (1:14 imbalance)
- **Goal:** Predict 2-year serious delinquency, then convert the PD model into a points-based scorecard
- **Timeline:** ~3 weeks, one step per day

> The Kaggle `cs-test.csv` has **no target column**. Split `cs-training.csv` yourself in Step 2.

> **Order change (2026-11-19):** the validation design (holdout + Stratified 5-fold CV) is now defined in **Step 2, before any cleaning is applied**. Cleaning, WoE binning, and model fitting all happen **inside the pipeline, fitted per fold**. No full-data `clean.csv` is created.

---

## 1. Non-negotiable rules

1. **Define the validation scheme before touching the data.** Holdout split and `StratifiedKFold` are set up in Step 2 — before imputation, capping, or binning.
2. **No leakage.** Every learned quantity — medians, cap levels, WoE bins, IV-based feature selection, model coefficients — must be fitted on the **current fold's training data only**, inside a `Pipeline`. Never fit on the full dataset.
3. **Stratified 5-fold CV on the training set.** `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`. The holdout test set is **locked** and used **once**, at the end of Step 6.
4. **Stratification is for imbalance, NOT for leakage.** It keeps ~6.68% defaults in every fold. The Pipeline prevents leakage. Do not confuse the two.
5. **Monotonic WoE** where possible. If a variable is non-monotonic, justify it in `decisions.md`.
6. **IV filters:** drop IV < 0.02; flag IV > 0.5 as suspicious (possible leakage or proxy for target). IV must be computed inside the fold.
7. **Report on TEST:** AUC, Gini, KS, and calibration — not train only. Also report **Gini/KS mean ± std over the 5 folds** as stability evidence.
8. **No SMOTE** for logistic regression. Prefer leaving weights alone and moving the business cut-off; if you use `class_weight='balanced'`, document that it changes calibration.
9. **Every chart gets a one-sentence insight** — in the notebook and in `decisions.md`.
10. **Decision log:** after every step, write 2–3 lines in `decisions.md` (what you decided + why).
11. **Commit after each step:** `git add . && git commit -m "step NN: short description"`.

---

## 2. Daily loop (~4 hours)

| Time | Activity |
|---|---|
| 30–45 min | **Study** only the concept for today's step |
| 20 min | **Decide** — write your own expectation before coding |
| 60–90 min | **Vibe code** with one paragraph prompt from `prompts.md` |
| 45 min | **Verify** — recompute 1–2 numbers independently |
| 15 min | **Explain** — update `decisions.md` and `README.md` |

Writing your expectation first is the key habit. If the result differs from your guess, you learned something.

**Rule of thumb:** Antigravity writes the code. You make the decisions, verify the numbers, and explain the result. If you cannot explain a number in an interview, that step is not finished.

---

## 3. The 10 steps

### Step 1 — Data understanding ✅ DONE
- **Study:** class imbalance, meaning of each column
- **Think:** Is a 7% default rate plausible? Which 3 variables should matter most, and why?
- **Build:** load `data/raw/cs-training.csv`; show shape, dtypes, missing-value table, describe(), target rate, histograms, boxplots, correlation heatmap; flag odd values
- **Verify:** target rate = 6.68%; odd values confirmed
- **Save:** `notebooks/01_eda.ipynb`, `reports/tables/missing_values.csv`, `reports/tables/odd_values.csv`

### Step 2 — Holdout split + Stratified 5-fold CV  ← DO THIS BEFORE CLEANING
- **Study:** data leakage, stratified vs. plain K-fold, why a 1:14 imbalance needs stratification
- **Think:** why split before fitting anything? Why is plain `KFold` risky at 6.68% defaults? Which seed?
- **Build:**
  1. stratified 70/30 holdout (`random_state=42`) → `train.csv` (105,000) / `test.csv` (45,000). **Lock the test set.**
  2. on train only: `cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
  3. print default count and rate for each fold
- **Verify:** fold default rates within ±0.5pp of 6.68%; each fold has >100 defaults; train/test indices disjoint
- **Save:** `notebooks/02_split_cv.ipynb`, `data/processed/train.csv`, `data/processed/test.csv`, `reports/tables/fold_summary.csv`

### Step 3 — Cleaning rules (as a fitted transformer, NOT a full-data clean)
- **Study:** MCAR/MAR/MNAR, outlier capping, sklearn `TransformerMixin`
- **Think:** How do you treat 96/98 codes, age = 0, and missing income? Is each choice defensible to a reviewer?
- **Build:** write `CreditCleaner` in `src/pipeline.py`. Its `fit()` learns medians and cap levels **from the data it is given** (which will always be fold-train); its `transform()` applies them. Decide the `MonthlyIncome == 0` → `DebtRatio` rule here (see §6 note) and justify the `NumberOfDependents` / 96/98 imputation choices in `decisions.md`. **Do not create `data/processed/clean.csv` from the full dataset.**
- **Verify:** no statistic is computed outside `fit()`; the class inherits `BaseEstimator, TransformerMixin` and has no hard-coded numbers from Step 1
- **Save:** `notebooks/03_cleaning.ipynb`, `reports/tables/cleaning_log.md`, `src/pipeline.py`

### Step 4 — WoE binning and IV (inside the Pipeline)
- **Study:** WoE and IV formulas, IV thresholds, why binning must be refit per fold
- **Think:** are bins monotonic? Is any IV too high? Will the rules hold in a fold with fewer bad cases?
- **Build:** wrap `scorecardpy`/`optbinning` in `WoETransformer`. In each fold, fit bins on fold-train only (monotonic, max 6 bins) and transform fold-validation. Report IV, WoE tables, and bin stability per fold. Per-fold AUC/Gini/KS belong to **Step 6**, not here. IV-based selection must also happen inside the fold.
- **Verify:** calculate IV by hand for one variable; confirm fold WoE tables differ slightly (proof of refitting); confirm no test data entered
- **Save:** `notebooks/04_binning_iv.ipynb`, `reports/tables/woe_tables.csv` (exported from the final refit on all train rows), `reports/tables/iv_summary.csv`, `reports/figures/iv_bar.png`

### Step 5 — Logistic regression (inside the Pipeline)
- **Study:** logistic regression, multicollinearity, p-values
- **Think:** do coefficient signs make business sense? Any correlated variables?
- **Build:** the `('model', LogisticRegression(...))` stage; fit per fold with `cross_validate`, then refit on all 105,000 train rows for the final model. Report coefficients, p-values, and VIF from the final refit.
- **Verify:** higher-risk bins have coefficients in the expected direction; VIF < 5–10
- **Save:** `notebooks/05_logistic_model.ipynb`, `reports/tables/model_summary.csv`, `reports/tables/vif.csv`

### Step 6 — Validation (5-fold CV + one final holdout)
- **Study:** Gini = 2·AUC − 1, KS, calibration, mean ± std across folds
- **Think:** does fold-to-fold spread suggest an unstable model? Is it calibrated? Does the single holdout result agree with the CV mean?
- **Build:** `cross_validate` the full Pipeline on train with the 5 stratified folds; report AUC/Gini/KS as **mean ± std**. `Gini`/`KS` need **scalar** `make_scorer` helpers in `src/validation.py` (see §6). Then refit on all train and evaluate the locked test set **once** for ROC, KS, and calibration.
- **Verify:** Gini = 2·AUC − 1 for every fold; each fold default rate representative
- **Save:** `notebooks/06_validation.ipynb`, `reports/tables/cv_metrics.csv`, `reports/tables/metrics.csv`, `reports/figures/roc.png`, `ks.png`, `calibration.png`

### Step 7 — Scorecard points
- **Study:** Factor / Offset scaling formula
- **Think:** are base score, base odds, and PDO sensible? Do points add up?
- **Build:** use the final production pipeline refit in Step 6; convert coefficients to points; build the scorecard table; score two example borrowers
- **Verify:** hand-score two borrowers and compare
- **Save:** `notebooks/07_scorecard_points.ipynb`, `reports/tables/scorecard.csv`

### Step 8 — PSI drift check
- **Study:** PSI formula and thresholds
- **Think:** what does a PSI shift mean for the business? When would you retrain?
- **Build:** PSI by score band and by variable, train vs. test and a simulated "new period"
- **Verify:** compute PSI manually for one variable
- **Save:** `notebooks/08_psi.ipynb`, `reports/tables/psi.csv`, `reports/figures/score_distribution.png`

### Step 9 — SHAP / explainability
- **Study:** SHAP basics, global vs. local explanation
- **Think:** do SHAP drivers agree with the scorecard? If not, why?
- **Build:** fit XGBoost as a benchmark on the same pipeline-transformed features, make SHAP summary and dependence plots, compare importance with the scorecard
- **Verify:** top drivers broadly agree, or disagreement is explained
- **Save:** `notebooks/09_shap.ipynb`, `reports/figures/shap_summary.png`, `reports/tables/importance_comparison.csv`

### Step 10 — Write-up
- **Study:** cut-off strategy, approval rate vs. default rate
- **Think:** what is the one-sentence story? What are the limits?
- **Build:** fill in `README.md` using its 6 sections; complete `reports/one_page_summary.md`; clean the repo
- **Verify:** a stranger can answer "what did you build and why does it matter?" in 30 seconds
- **Save:** `README.md`, `reports/one_page_summary.md`

---

## 4. Scorecard formula

Scale: base score **600** at odds **50:1**, PDO (points to double the odds) = **20**.

```
Factor = PDO / ln(2)
Offset = Base score − Factor × ln(Base odds)
Score  = Offset − Factor × ln(odds of default)

Points per bin = −(coefficient × WoE + intercept / n) × Factor + Offset / n
```

where `n` = number of model features. Odds = p / (1 − p).

**WoE convention used here:** `WoE = ln(good% / bad%)` per bin, so a **higher** WoE means a **lower** default risk. The points formula above assumes this convention — if you switch to `ln(bad% / good%)`, flip the sign of every points column. Assert that the highest-risk bin of a strong variable receives the most points.

---

## 5. Why Stratified 5-Fold for a 6.68% default rate

**What stratification does.** With 6.68% defaults (~1:14), the sampling standard error of a fold default rate is √(p(1−p)/n) ≈ **0.17pp** at n = 21,000. So plain `KFold` would not produce "one fold 5%, another 9%" — but it *can* drift by ~0.2–0.4pp between folds purely by chance. That small noise still matters because WoE needs enough "bad" cases per bin: a bin that lands in a bad-poor fold can have very few defaults and produce unstable (sometimes infinite) WoE. `StratifiedKFold` allocates defaults to folds **exactly in proportion**, pinning every fold at ~6.68%, so:

- every fold is representative of the applicant population;
- fold-to-fold spread reflects **model stability**, not the luck of the split;
- WoE bins in each fold have enough bad cases to estimate;
- you can report **Gini/KS mean ± std over 5 folds** — far stronger evidence than a single number.

**What it does NOT do.** Stratification does not rebalance the classes and it does not stop leakage. It only makes validation reliable under imbalance. Leakage is prevented by fitting everything inside the fold (the Pipeline). The imbalance itself is handled by using AUC/Gini/KS instead of accuracy, choosing a business cut-off, and optionally `class_weight='balanced'` — though class weights change calibration, so for a scorecard prefer leaving them alone and moving the cut-off.

**Design chosen here (keep both):**

```
cs-training.csv (150,000)
│
├── Stratified 70/30 holdout, seed 42 → train 105,000 / test 45,000
│     test set is LOCKED — used once, at the end of Step 6
│
├── on train only: StratifiedKFold(5, shuffle=True, random_state=42)
│     folds 1–5: fit Pipeline on fold-train (84,000)
│                → score fold-validation (21,000)
│     → mean ± std of AUC / Gini / KS
│
└── refit Pipeline on all 105,000 train rows
      → final scorecard → single evaluation on the locked test set
```

---

## 6. Leakage-safe pipeline (specification)

Implement in `src/pipeline.py`. `cross_validate` calls `fit()` on fold-train and `transform()` on both fold-train and fold-validation — that isolation is the leakage barrier.

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import make_scorer

PAST_DUE = ['NumberOfTime30-59DaysPastDueNotWorse',
            'NumberOfTime60-89DaysPastDueNotWorse',
            'NumberOfTimes90DaysLate']
CAP_COLS = ['DebtRatio', 'RevolvingUtilizationOfUnsecuredLines']

class CreditCleaner(BaseEstimator, TransformerMixin):
    """Cleaning rules as a fitted transformer — no statistics from full data.

    NOTE (decide in Step 3, record in decisions.md):
    - DebtRatio is unreliable when MonthlyIncome is 0 or missing. 1,634 rows
      have income == 0; their DebtRatio median is 930 vs 0.3 for income > 0.
      A p99 cap (~4,979) does not fix this. Decide a rule, e.g. set DebtRatio
      to NaN when income <= 0 and let WoE place those rows in their own bin.
    - 96/98 are "no data" codes; filling with 0 asserts "no delinquency".
      Consider a separate missing bin or an indicator instead.
    """
    def fit(self, X, y=None):
        self.income_median_ = X['MonthlyIncome'].median()
        self.age_median_ = X.loc[X['age'] > 0, 'age'].median()   # exclude age 0
        self.cap_ = {c: X[c].quantile(0.99) for c in CAP_COLS}
        return self

    def transform(self, X):
        X = X.copy()
        X['MonthlyIncome'] = X['MonthlyIncome'].fillna(self.income_median_)
        X['NumberOfDependents'] = X['NumberOfDependents'].fillna(0)
        X['age'] = X['age'].replace(0, np.nan).fillna(self.age_median_)
        # TODO Step 3: apply the income <= 0 -> DebtRatio rule decided above.
        for c in PAST_DUE:
            X[c] = X[c].mask(X[c].isin([96, 98])).fillna(0)
        for c, v in self.cap_.items():
            X[c] = X[c].clip(upper=v)
        return X

class WoETransformer(BaseEstimator, TransformerMixin):
    """Wrap scorecardpy / optbinning as a sklearn transformer."""
    def fit(self, X, y):        # learns bins + WoE from fold-train only
        ...
    def transform(self, X):     # maps values to WoE, unseen → default bin
        ...

def make_pipeline():
    return Pipeline([
        ('clean', CreditCleaner()),
        ('woe', WoETransformer(max_bins=6)),
        ('model', LogisticRegression(max_iter=1000, random_state=42)),
    ])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
result = cross_validate(
    make_pipeline(), X_train, y_train, cv=cv,
    scoring=['roc_auc', 'neg_log_loss']   # add make_scorer(gini/ks) here
)
```

`Gini` and `KS` are not built-in sklearn scorers. Add **scalar** helpers in `src/validation.py` — e.g. `gini_score(y_true, y_score)` and `ks_score(y_true, y_score)` that each return a single float — and register them with `make_scorer(...)`. (`auc_gini_ks()` returns a dict, which `make_scorer` cannot use.) Alternatively, compute them from out-of-fold predictions via `cross_val_predict(..., method='predict_proba')`.

**Pipeline rules:**
- `fit()` may only see fold-train data; `transform()` may see fold-train and fold-validation.
- Never call `fit()` on concatenated train+test, and never create a full-data `clean.csv` that is split afterwards.
- Drop the `Unnamed: 0` index column **before** the pipeline (Step 2 does this when saving `train.csv`); add a defensive `drop(columns=...)` if the pipeline is ever run on the raw file.
- IV-based feature selection must also be fitted per fold (or fixed from Step 1 EDA and documented). If it drops different features per fold, `n` varies — the **final refit on all 105,000 train rows** fixes the `n` used in the scorecard formula.
- After the final refit on all train rows, save the production pipeline with `joblib.dump` (ignored by `.gitignore`).

---

## 7. Prompt template (one paragraph)

> "Follow `scorecard_workflow.md`, **Step N only**. [Exact task]. [What NOT to do]. Use the installed [skill names]. Save outputs in [folder]. Update `decisions.md` with 2–3 lines. Do not start Step N+1."

Ready-to-paste prompts for all 10 steps are in `prompts.md`.

---

## 8. Verification recipes

| Number | Independent check |
|---|---|
| IV | Recompute by hand for one variable: `IV = Σ (good% − bad%) × WoE` |
| Gini | Assert `abs(gini - (2*auc - 1)) < 1e-6` for every fold |
| PSI | Recompute manually for one variable using 10 equal-width bands |
| Scorecard | Hand-score two borrowers from the WoE table and compare to code |
| Stratification | Each fold has ~6.68% defaults (±0.5pp) and >100 defaults |
| Leakage | Fit the pipeline on one fold twice → identical output; change one fold-train row → fold-validation scores change. If they do not, a statistic escaped the fold. |

If hand result and AI result differ, you found a bug **or** a misunderstanding. Both are useful.

---

## 9. PSI interpretation

| PSI | Meaning | Action |
|---|---|---|
| < 0.10 | Stable | No action |
| 0.10 – 0.25 | Watch | Investigate, monitor closely |
| > 0.25 | Significant shift | Investigate cause, consider retraining |

---

## 10. Self-test (answer without notes)

1. Why split before WoE binning?
2. Does `StratifiedKFold` prevent leakage? (No — fitting inside the fold does.)
3. What does `StratifiedKFold` guarantee, and what does it not guarantee?
4. What does an IV of 0.4 tell you? Is it too good?
5. What does PSI = 0.3 mean?
6. Why report Gini mean ± std instead of one number?
7. Why a scorecard when XGBoost has higher AUC?
8. How do you choose the cut-off score?
