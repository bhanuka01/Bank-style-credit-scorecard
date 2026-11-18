# Raw data

Download the dataset here before starting Step 1.

1. Go to Kaggle → **Give Me Some Credit** (competition/dataset).
   https://www.kaggle.com/c/GiveMeSomeCredit/data
2. Download `cs-training.csv`.
3. Place it in this folder as `cs-training.csv` (exact name used in `scorecard_workflow.md`).

**Do not commit it.** `.gitignore` excludes everything in `data/raw/` except this README, because the file is large and Kaggle's terms apply.

## What you should find

| Property | Expected value |
|---|---|
| Rows | ~150,000 |
| Features | 10 |
| Target | `SeriousDlqin2yrs` (1 = serious delinquency in 2 years) |
| Default rate | ~7% |

## Important

The Kaggle `cs-test.csv` has **no target column**, so it cannot be used for validation. You will create your own train/test split from `cs-training.csv` in **Step 3**.
