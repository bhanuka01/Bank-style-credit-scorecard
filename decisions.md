# Decision log

Two to three lines after **every** step: what you decided and why. This is your critical-thinking record and your interview revision sheet.

## Day 0 — Initial guess (write BEFORE Step 1)

My top 3 variables expected to have the highest IV:

1. _(RevolvingUtilizationOfUnsecuredLines)_ — How much use credit card Until now
2. _(DebtRatio)_ — This is Income and credit ratio. So it's more effect for
3. _(NumberOfTimes90DaysLate)_ — This is late its mean more Them can't pay for last payment.

My expected default rate: 7%

---

## Step 1 — Data understanding

- **Date:** 2026-11-19
- **Expectation vs. result:** Expected default rate ~7%; actual 10,026 / 150,000 = 6.68% (1:14 imbalance). Expected past-due counts to lead; raw correlation supports this (30-59d r=0.126, 90d r=0.117, age r=0.115, 60-89d r=0.102). Compare with the Day 0 guess above.
- **Decision / why:** Dropped the Kaggle `Unnamed: 0` index column (schema fix, not cleaning). Read raw data read-only, no sampling, no imputation, no row deletion. Saved `missing_values.csv`, `odd_values.csv`, and 3 EDA figures. Key flags for Step 3: MonthlyIncome 19.82% missing, Dependents 2.62% missing, 269 rows with 96/98 codes, 1 age=0, 13 age>100, extreme DebtRatio/utilization tails. Nothing cleaned yet — decisions come in Step 3.

## Step 2 — Holdout split + Stratified 5-fold CV

- **Date:** 2026-11-19
- **Expectation vs. result:** Expected folds to sit near 6.68% with small deviations; actual fold rates 6.681–6.686% (max deviation 0.003pp), each with 1,403–1,404 defaults out of 21,000 validation rows. Train 105,000 (70%) / test 45,000 (30%); train default rate 6.684%, identical to the full file.
- **Decision / why:** Defined the validation scheme before any cleaning: stratified holdout (`seed=42`) plus `StratifiedKFold(5, shuffle=True, seed=42)` on train only. Locked the test set — wrote it to disk but computed no statistic on it. Asserted train/test index disjoint, fold train/val disjoint, >100 defaults per fold, and ±0.5pp rate tolerance. No imputation, capping, or binning performed.

## Step 3 — Cleaning rules (fitted transformer)

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 4 — WoE / IV

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 5 — Logistic regression

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 6 — Validation

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 7 — Scorecard points

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 8 — PSI

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 9 — SHAP

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**

## Step 10 — Write-up

- **Date:**
- **Expectation vs. result:**
- **Decision / why:**
