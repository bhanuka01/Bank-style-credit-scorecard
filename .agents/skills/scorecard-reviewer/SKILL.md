---
name: scorecard-reviewer
description: Reviews a credit scorecard/PD project. Use when the user asks to review, validate, or check a WoE/logistic scorecard notebook or repo.
---

# Scorecard Reviewer

Review the project and report problems in this order:

1. **Leakage**: split happens before binning/WoE; no test data used in fitting.
2. **Cleaning**: special codes (e.g. 96/98), impossible values (age 0), missing-value handling documented.
3. **Binning**: WoE trends monotonic or justified; IV thresholds applied (drop < 0.02); suspiciously high IV flagged (> 0.5).
4. **Model**: coefficient signs make business sense; VIF/correlation checked.
5. **Validation**: AUC, Gini, KS, and calibration reported on test data, not only train. Check Gini = 2·AUC − 1.
6. **Scorecard**: scaling parameters stated (base score, base odds, PDO); points add up.
7. **PSI**: computed correctly, with interpretation (< 0.1 stable, 0.1–0.25 watch, > 0.25 shift).
8. **Business story**: cut-off strategy with approval rate vs. default rate.
9. **README**: problem, method, results, limitations all present; no placeholder `TODO` left in a finished project.

## Output format

| # | Issue | Severity (High/Med/Low) | Where (file / cell) | Fix |
|---|---|---|---|---|
| 1 | | | | |

Then a short paragraph: **Verdict** — ready for GitHub / needs work before sharing.

## Rules

- Never change the user's code unless asked.
- Cite the exact notebook cell or table where each issue appears.
- Prefer concrete fixes over general advice.
