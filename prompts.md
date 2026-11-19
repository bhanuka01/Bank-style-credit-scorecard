# Antigravity prompts — one per step

Paste **one** prompt at a time. Each starts from `scorecard_workflow.md` so you do not repeat the whole plan. Steps 2 and 3 are reordered: **validation design comes before cleaning**.

---

**Setup prompt (Day 0, once)**

> Read `scorecard_workflow.md`, `README.md`, and `decisions.md`. Confirm you understand the 10 steps, the 11 non-negotiable rules, the Stratified 5-fold design, and the pipeline specification in section 6. Do not write any code yet. Summarise back to me: (1) the 11 rules in 5 bullets, (2) the difference between stratification and leakage prevention, (3) why the holdout test set is locked.

---

**Step 1 — EDA** ✅ DONE

> Follow `scorecard_workflow.md`, Step 1 only. Load `data/raw/cs-training.csv`, show shape, dtypes, a missing-value table, summary statistics, target rate, histograms and boxplots, and a correlation heatmap. Flag any odd values. Save the notebook as `notebooks/01_eda.ipynb` and the missing-value table in `reports/tables/`. Use the exploratory-data-analysis skill. Do not start Step 2.

**Step 2 — Holdout split + Stratified 5-fold CV (do this BEFORE cleaning)**

> Follow `scorecard_workflow.md`, Step 2 only. Load `data/raw/cs-training.csv`, drop the `Unnamed: 0` column, and make a stratified 70/30 holdout split with `random_state=42` → `data/processed/train.csv` and `test.csv`. Lock the test set; do not compute any statistic on it. On the training set only, create `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` and print the default count and default rate for each fold. Assert every fold is within ±0.5 percentage points of 6.684% and has more than 100 defaults. Save `notebooks/02_split_cv.ipynb` and `reports/tables/fold_summary.csv`. **Do not clean, impute, cap, or bin anything yet — Step 3 only writes the cleaning rules as a transformer. Do not start Step 3.**

**Step 3 — Cleaning rules as a fitted transformer**

> Follow `scorecard_workflow.md`, Step 3 only. Implement `CreditCleaner(BaseEstimator, TransformerMixin)` in `src/pipeline.py` using the EDA findings from `01_eda.ipynb`: median-impute `MonthlyIncome`, impute `NumberOfDependents`, treat 96/98 in past-due columns, fix age 0, and cap `DebtRatio` / `RevolvingUtilization`. All statistics must be learned in `fit()` from whatever data it is given; none may be hard-coded from Step 1. Compute the age median after excluding age 0. Decide and justify the `MonthlyIncome == 0` → `DebtRatio` rule (1,634 rows have income 0; their DebtRatio median is 930 vs 0.3 for income > 0 — a p99 cap does not fix this) and the 96/98 treatment; record both in `decisions.md`. Do NOT create a full-data `clean.csv`. Save `notebooks/03_cleaning.ipynb`, `reports/tables/cleaning_log.md`, and `src/pipeline.py`. Do not fit a model yet.

**Step 4 — WoE / IV inside the pipeline**

> Follow `scorecard_workflow.md`, Step 4 only. Implement `WoETransformer(BaseEstimator, TransformerMixin)` in `src/pipeline.py` wrapping `scorecardpy` (or `optbinning`) with monotonic bins, max 6 bins. Use the convention `WoE = ln(good% / bad%)`. If `scorecardpy` will not install on this environment, implement WoE/IV manually in pandas and say so. Using the training file and the 5 stratified folds from Step 2, fit the bins on fold-train only, transform fold-validation, and report IV, WoE tables, and bin stability per fold. Leave per-fold AUC/Gini/KS to Step 6. Drop IV < 0.02 and flag IV > 0.5. Export `woe_tables.csv` from the final refit on all training rows. Never touch the locked test set. Save `notebooks/04_binning_iv.ipynb` and outputs in `reports/`. Use the credit-risk-model and scikit-learn skills. Do not start Step 5.

**Step 5 — Logistic regression inside the pipeline**

> Follow `scorecard_workflow.md`, Step 5 only. Complete `make_pipeline()` in `src/pipeline.py` with the `LogisticRegression` stage. Use `cross_validate` with the 5 stratified folds from Step 2; then refit on all training rows for the final model. Report coefficients, p-values (statsmodels), and VIF from the final refit. No SMOTE and no class weights unless I approve it in `decisions.md`. Save `notebooks/05_logistic_model.ipynb` and tables in `reports/tables/`. Use the statsmodels skill.

**Step 6 — Validation: 5-fold CV + one final holdout**

> Follow `scorecard_workflow.md`, Step 6 only. Add scalar scorer helpers (`gini_score`, `ks_score`) to `src/validation.py` and register them with `make_scorer`. Run `cross_validate` on the full pipeline using the 5 stratified folds; report AUC, Gini, and KS as mean ± std and save to `reports/tables/cv_metrics.csv`. Add an assertion that Gini = 2·AUC − 1 for every fold. Then, and only then, evaluate the locked `test.csv` once for ROC, KS, and calibration → `reports/tables/metrics.csv` and figures in `reports/figures/`. Save `notebooks/06_validation.ipynb`. Do not start Step 7.

**Step 7 — Scorecard points**

> Follow `scorecard_workflow.md`, Step 7 only. Using the final production pipeline refit on all training rows, convert coefficients to points with base score 600, base odds 50:1, PDO 20. Build the scorecard table, score two example borrowers, and verify the points add up. Save `notebooks/07_scorecard_points.ipynb` and `reports/tables/scorecard.csv`.

**Step 8 — PSI**

> Follow `scorecard_workflow.md`, Step 8 only. Compute PSI by score band and by variable for train vs. test, plus a simulated "new period" made by randomly perturbing the test score distribution. Apply the <0.1 / 0.1–0.25 / >0.25 thresholds and interpret each result. Save `notebooks/08_psi.ipynb`, `reports/tables/psi.csv`, and `reports/figures/score_distribution.png`.

**Step 9 — SHAP**

> Follow `scorecard_workflow.md`, Step 9 only. Fit XGBoost on the same pipeline-transformed WoE features, generate SHAP summary and dependence plots, and produce a table comparing its top drivers with the scorecard's variable importance. Explain any disagreement in 3–4 sentences. Save `notebooks/09_shap.ipynb` and outputs in `reports/`. Use the shap skill.

**Step 10 — Write-up**

> Follow `scorecard_workflow.md`, Step 10 only. Fill in `README.md` using its 6 required sections and complete `reports/one_page_summary.md`. Include the CV mean ± std, the single holdout result, the scorecard, the PSI result, and a cut-off strategy showing approval rate vs. expected default rate. Add limitations and next steps. Every figure referenced must exist in `reports/figures/`. Do not invent results that are not in the tables.

---

**Weekly review prompt (end of each week)**

> Use the `scorecard-reviewer` skill in `.agents/skills/scorecard-reviewer/SKILL.md` to review this repo, with special attention to rules 1–4 on leakage and stratification. Output the Issue | Severity | Where | Fix table. Do not change any code.
