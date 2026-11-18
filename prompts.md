# Antigravity prompts — one per step

Paste **one** prompt at a time. Each starts from `scorecard_workflow.md` so you do not repeat the whole plan. Replace nothing except where noted.

---

**Setup prompt (Day 0, once)**

> Read `scorecard_workflow.md`, `README.md`, and `decisions.md`. Confirm you understand the 10 steps, the 9 non-negotiable rules, and the scorecard formula. Do not write any code yet. Summarise the rules back to me in 5 bullet points and list the files I must download before Step 1.

---

**Step 1 — EDA**

> Follow `scorecard_workflow.md`, Step 1 only. Load `data/raw/cs-training.csv`, show shape, dtypes, a missing-value table, summary statistics, target rate, histograms and boxplots, and a correlation heatmap. Flag any odd values. Save the notebook as `notebooks/01_eda.ipynb` and the missing-value table in `reports/tables/`. Use the exploratory-data-analysis skill. Do not start Step 2.

**Step 2 — Cleaning**

> Follow `scorecard_workflow.md`, Step 2 only. Using the findings from `01_eda.ipynb`, implement my cleaning rules from `decisions.md`: median-impute `MonthlyIncome`, impute `NumberOfDependents`, treat 96/98 codes in the past-due columns, fix age = 0, and cap extreme `DebtRatio` and `RevolvingUtilization`. Produce a cleaning log showing rows/columns affected before and after. Save as `notebooks/02_cleaning.ipynb`, write `data/processed/clean.csv`, and log to `reports/tables/cleaning_log.md`. Do not split or bin yet.

**Step 3 — Split**

> Follow `scorecard_workflow.md`, Step 3 only. Load `data/processed/clean.csv`. Do a stratified 70/30 train/test split with `random_state=42`, verify the target rate is nearly equal in both sets, and that row indices do not overlap. Save `notebooks/03_split.ipynb`, `data/processed/train.csv`, and `data/processed/test.csv`. Do not start binning.

**Step 4 — WoE / IV**

> Follow `scorecard_workflow.md`, Step 4 only. Using the training file only, bin every variable with `optbinning` (monotonic trend, max 6 bins), compute IV, save the WoE tables and an IV bar chart, and write a short markdown summary of which variables look strong, weak, or suspicious. Do not touch the test set. Use the credit-risk-model and scikit-learn skills. Save outputs in `notebooks/04_binning_iv.ipynb` and `reports/`.

**Step 5 — Logistic regression**

> Follow `scorecard_workflow.md`, Step 5 only. Fit a logistic regression on the WoE-transformed training data from Step 4. Report coefficients, p-values, and a VIF table. Flag any coefficient whose sign contradicts business sense. Save `notebooks/05_logistic_model.ipynb` and tables in `reports/tables/`. Use the statsmodels skill. Do not validate on test yet.

**Step 6 — Validation**

> Follow `scorecard_workflow.md`, Step 6 only. Evaluate the Step 5 model on the test set only: AUC, Gini, KS statistic, ROC curve, KS plot, and a calibration table/plot. Add an assertion that Gini equals 2·AUC − 1. Save `notebooks/06_validation.ipynb`, `reports/tables/metrics.csv`, and figures in `reports/figures/`. Do not build the scorecard yet.

**Step 7 — Scorecard points**

> Follow `scorecard_workflow.md`, Step 7 only. Using base score 600, base odds 50:1, PDO 20, convert the Step 5 coefficients into points using the formula in the master file. Build the scorecard table, score two example borrowers, and verify the points add up. Save `notebooks/07_scorecard_points.ipynb` and `reports/tables/scorecard.csv`. Do not start PSI.

**Step 8 — PSI**

> Follow `scorecard_workflow.md`, Step 8 only. Compute PSI by score band and by variable for train vs. test, plus a simulated "new period" made by randomly perturbing the test score distribution. Apply the <0.1 / 0.1–0.25 / >0.25 thresholds and interpret each result. Save `notebooks/08_psi.ipynb`, `reports/tables/psi.csv`, and `reports/figures/score_distribution.png`. Do not start SHAP.

**Step 9 — SHAP**

> Follow `scorecard_workflow.md`, Step 9 only. Fit XGBoost on the same WoE features, generate SHAP summary and dependence plots, and produce a table comparing its top drivers with the scorecard's variable importance. Explain any disagreement in 3–4 sentences. Save `notebooks/09_shap.ipynb` and outputs in `reports/`. Use the shap skill. Do not rewrite the README yet.

**Step 10 — Write-up**

> Follow `scorecard_workflow.md`, Step 10 only. Fill in `README.md` using its 6 required sections and complete `reports/one_page_summary.md`. Include the key numbers from `reports/tables/metrics.csv`, the scorecard, the PSI result, and a cut-off strategy showing approval rate vs. expected default rate. Add limitations and next steps. Every figure referenced must exist in `reports/figures/`. Do not invent results that are not in the tables.

---

**Weekly review prompt (end of each week)**

> Use the `scorecard-reviewer` skill in `.agents/skills/scorecard-reviewer/SKILL.md` to review this repo. Output the Issue | Severity | Where | Fix table. Do not change any code.
