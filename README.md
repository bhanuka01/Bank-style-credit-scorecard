# Bank-style Credit Scorecard and PD Model

> **Status: Steps 1–2 complete** (EDA + holdout/5-fold CV). Steps 3–10 pending. Numbers below are placeholders marked `TODO` until the corresponding step finishes.

Predict the probability that a borrower will experience serious delinquency within 2 years, then convert the model into a points-based scorecard that a credit team could actually use.

## One chart, one conclusion

> TODO — add the ROC/KS chart from `reports/figures/` and one sentence:
> "At a cut-off of X points we approve Y% of applicants while the default rate falls from 7% to Z%."

## Repository structure

```
.
├── data/
│   ├── raw/          # cs-training.csv goes here (never committed)
│   └── processed/    # train.csv, test.csv (never committed; generated in Step 2)
├── notebooks/        # 01_eda → 09_shap, numbered by workflow step
├── src/              # reusable functions imported by the notebooks
├── reports/
│   ├── figures/      # charts (committed — portfolio evidence)
│   ├── tables/       # metrics, WoE, scorecard, PSI (committed)
│   └── one_page_summary.md
├── scorecard_workflow.md   # master plan — start here
├── prompts.md              # one paste-ready prompt per step
├── decisions.md            # your critical-thinking log
├── requirements.txt
└── .agents/skills/scorecard-reviewer/   # weekly self-review skill
```

## Quickstart

```powershell
# 1. environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. data — download cs-training.csv from Kaggle "Give Me Some Credit"
#    and place it in data/raw/ (see data/raw/README.md)

# 3. work through steps 1–10 in scorecard_workflow.md, one prompt at a time
# 4. after each step:
git add . && git commit -m "step NN: short description"
```

## 1. Business problem

Banks must decide who to lend to. A good PD model estimates the chance a borrower defaults; a **scorecard** turns that estimate into transparent points that a loan officer can explain to a customer and a regulator. This project balances predictive power (XGBoost benchmark) with explainability (WoE + logistic regression + SHAP).

## 2. Data and cleaning decisions

- **Source:** Give Me Some Credit (Kaggle), 150,000 borrowers, 10 features, target `SeriousDlqin2yrs`, **6.68% default rate** (1:14 imbalance). Column meanings confirmed against `data/raw/Data Dictionary.xls` (needs `xlrd`).
- **Dataset choice:** cleaner than Home Credit, so it fits a 2–3 week build; Home Credit is a planned "version 2".
- **Cleaning:** TODO — implemented as a fitted transformer (`CreditCleaner`) inside the pipeline, not as a full-data clean. Planned: median-impute `MonthlyIncome`, impute `NumberOfDependents`, treat 96/98 past-due codes, fix age = 0, handle the `MonthlyIncome == 0` → `DebtRatio` artifact (1,634 rows; DebtRatio median 930 vs 0.3 for income > 0), cap extreme ratios. Full log: `reports/tables/cleaning_log.md`.
- **Leakage control:** stratified 70/30 holdout (`seed=42`) locked first, then Stratified 5-fold CV on the training set only. Imputation, capping, WoE binning, IV selection and the model are all fitted **inside each fold** via a sklearn `Pipeline`.

## 3. Key results

| Metric | 5-fold CV (mean ± std) | Locked test | Source |
|---|---|---|---|
| AUC | TODO | TODO | `reports/tables/cv_metrics.csv`, `metrics.csv` |
| Gini (2·AUC − 1) | TODO | TODO | same |
| KS | TODO | TODO | same |
| PSI (train vs. test) | — | TODO | `reports/tables/psi.csv` |

**Scorecard:** base score 600, base odds 50:1, PDO 20. Full points table: `reports/tables/scorecard.csv`.

## 4. Business insight — cut-off strategy

TODO — table of cut-off score vs. approval rate vs. expected default rate. Example framing: "approve the top 70% and the default rate drops from 7% to X%".

## 5. Scorecard vs. XGBoost + SHAP

TODO — what the comparison teaches: the scorecard loses a little AUC but wins on transparency and regulatory acceptability; SHAP confirms / challenges the same drivers.

## 6. Limitations and next steps

- Single public dataset, one point in time — no true out-of-time validation.
- Reject inference is not applied (training data contains only accepted borrowers).
- Next: Home Credit dataset, reject inference, a Streamlit scoring demo, and a monitored PSI dashboard.

## Interview talking points

- **"Why logistic regression and WoE when XGBoost is more accurate?"** Banks need explainability and regulatory transparency — WoE bins read directly as "riskier band → more points", which connects to my XAI work.
- **"What does IV tell you?"** Predictive strength of a single variable; < 0.02 is weak, > 0.5 is suspicious.
- **"What does PSI < 0.1 mean?"** Population is stable; no retraining needed.
- **"How would you set the cut-off score?"** From the business trade-off between approval rate and expected loss, not from maximising AUC.
