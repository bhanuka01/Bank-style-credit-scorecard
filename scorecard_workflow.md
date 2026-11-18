# Scorecard Workflow — Master File

Single source of truth for this project. Every Antigravity prompt refers to a step number **here**, so you never paste the whole plan again.

- **Project:** Bank-style credit scorecard and PD model
- **Dataset:** *Give Me Some Credit* (Kaggle), `cs-training.csv`, ~150,000 borrowers, 10 features, target `SeriousDlqin2yrs`, ~7% defaults
- **Goal:** Predict 2-year serious delinquency, then convert the PD model into a points-based scorecard
- **Timeline:** ~3 weeks, one step per day

> The Kaggle `cs-test.csv` has **no target column**. Split `cs-training.csv` yourself in Step 3.

---

## 1. Non-negotiable rules

1. **Split before binning.** Fit WoE/IV, imputation, and capping on **TRAIN only**.
2. **No leakage.** Never use test data to choose bins, thresholds, or hyperparameters.
3. **Monotonic WoE** where possible. If a variable is non-monotonic, justify it in `decisions.md`.
4. **IV filters:** drop IV < 0.02; flag IV > 0.5 as suspicious (possible leakage or proxy for target).
5. **Report on TEST:** AUC, Gini, KS, and calibration — not train only.
6. **No SMOTE** for logistic regression. Use class weights or leave as-is, and explain why.
7. **Every chart gets a one-sentence insight** — in the notebook and in `decisions.md`.
8. **Decision log:** after every step, write 2–3 lines in `decisions.md` (what you decided + why).
9. **Commit after each step:** `git add . && git commit -m "step NN: short description"`.

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

### Step 1 — Data understanding
- **Study:** class imbalance, meaning of each column
- **Think:** Is a 7% default rate plausible? Which 3 variables should matter most, and why? Write your guess in `decisions.md` **before** running code.
- **Build:** load `data/raw/cs-training.csv`; show shape, dtypes, missing-value table, describe(), target rate, histograms, boxplots, correlation heatmap; flag odd values
- **Verify:** does the target rate match ~7%? Are the flagged odd values real?
- **Save:** `notebooks/01_eda.ipynb`, `reports/tables/missing_values.csv`

### Step 2 — Cleaning
- **Study:** MCAR/MAR/MNAR, outlier capping
- **Think:** How do you treat 96/98 codes, age = 0, and missing income? Is each choice defensible to a reviewer?
- **Build:** impute `MonthlyIncome` (median) and `NumberOfDependents` (0 or median); treat 96/98 in past-due columns; fix age = 0; cap extreme `DebtRatio` and `RevolvingUtilization`; produce a cleaning log
- **Verify:** row count unchanged (or changes explained); no negatives/impossible values remain
- **Save:** `notebooks/02_cleaning.ipynb`, `reports/tables/cleaning_log.md`, `data/processed/clean.csv`

### Step 3 — Train/test split
- **Study:** data leakage
- **Think:** why split before binning? Which stratification and seed?
- **Build:** stratified 70/30 split with `random_state=42`; save train/test
- **Verify:** target rate nearly equal in both sets; no overlap of row indices
- **Save:** `notebooks/03_split.ipynb`, `data/processed/train.csv`, `data/processed/test.csv`

### Step 4 — WoE binning and IV
- **Study:** WoE and IV formulas, IV thresholds
- **Think:** are bins monotonic? Is any IV too high? Which variables to drop?
- **Build:** bin every feature on **train only**, monotonic trend, max 6 bins; compute WoE tables and IV; drop IV < 0.02 and flag suspicious IV
- **Verify:** calculate IV by hand for one variable and compare
- **Save:** `notebooks/04_binning_iv.ipynb`, `reports/tables/woe_tables.csv`, `reports/tables/iv_summary.csv`, `reports/figures/iv_bar.png`

### Step 5 — Logistic regression
- **Study:** logistic regression, multicollinearity, p-values
- **Think:** do coefficient signs make business sense? Any correlated variables?
- **Build:** fit on WoE-transformed features; print coefficients, p-values, VIF table
- **Verify:** higher-risk bins have coefficients in the expected direction
- **Save:** `notebooks/05_logistic_model.ipynb`, `reports/tables/model_summary.csv`, `reports/tables/vif.csv`

### Step 6 — Validation
- **Study:** Gini = 2·AUC − 1, KS statistic, calibration
- **Think:** does test performance match train? Is the model calibrated?
- **Build:** compute AUC, Gini, KS, ROC curve, KS plot, calibration table on **test**
- **Verify:** confirm Gini equals 2·AUC − 1
- **Save:** `notebooks/06_validation.ipynb`, `reports/tables/metrics.csv`, `reports/figures/roc.png`, `reports/figures/ks.png`, `reports/figures/calibration.png`

### Step 7 — Scorecard points
- **Study:** Factor / Offset scaling formula
- **Think:** are base score, base odds, and PDO sensible? Do points add up?
- **Build:** convert coefficients to points using the formula below; build scorecard table; score two example borrowers
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
- **Build:** fit XGBoost as a benchmark, make SHAP summary and dependence plots, compare variable importance with the scorecard
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

---

## 5. Prompt template (one paragraph)

> "Follow `scorecard_workflow.md`, **Step N only**. [Exact task]. [What NOT to do]. Use the installed [skill names]. Save outputs in [folder]. Update `decisions.md` with 2–3 lines. Do not start Step N+1."

Ready-to-paste prompts for all 10 steps are in `prompts.md`.

---

## 6. Verification recipes

| Number | Independent check |
|---|---|
| IV | Recompute by hand for one variable: `IV = Σ (good% − bad%) × WoE` |
| Gini | Assert `abs(gini - (2*auc - 1)) < 1e-6` |
| PSI | Recompute manually for one variable using 10 equal-width bands |
| Scorecard | Hand-score two borrowers from the WoE table and compare to code |

If hand result and AI result differ, you found a bug **or** a misunderstanding. Both are useful.

---

## 7. PSI interpretation

| PSI | Meaning | Action |
|---|---|---|
| < 0.10 | Stable | No action |
| 0.10 – 0.25 | Watch | Investigate, monitor closely |
| > 0.25 | Significant shift | Investigate cause, consider retraining |

---

## 8. Self-test (answer without notes)

1. Why split before WoE binning?
2. What does an IV of 0.4 tell you? Is it too good?
3. What does PSI = 0.3 mean?
4. Why a scorecard when XGBoost has higher AUC?
5. How do you choose the cut-off score?
