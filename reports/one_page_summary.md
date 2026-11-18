# One-page business summary

> Fill this in at Step 10. One page maximum. A loan manager should be able to read it in 60 seconds.

## The problem

TODO — one paragraph: why the bank needs a PD model and a scorecard.

## What was built

TODO — dataset, sample size, method (WoE binning → logistic regression → points), benchmark model (XGBoost + SHAP).

## Headline numbers

| Metric | Value |
|---|---|
| Test AUC | TODO |
| Gini | TODO |
| KS | TODO |
| PSI | TODO |
| Scorecard scale | 600 base / PDO 20 |

## The business decision

TODO — recommended cut-off score, approval rate at that cut-off, expected default rate at that cut-off.

## What the model says

TODO — top 3 risk drivers and the direction of effect.

## Limitations

TODO — no out-of-time validation, reject inference absent, single dataset.

## Next steps

TODO — Home Credit v2, reject inference, Streamlit demo, PSI monitoring dashboard.
