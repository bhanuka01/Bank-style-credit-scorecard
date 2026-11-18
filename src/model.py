"""Step 5: logistic regression on WoE features."""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression


def fit_logistic(x_woe: pd.DataFrame, y: pd.Series) -> LogisticRegression:
    """Fit logistic regression on WoE-transformed features.

    Use class_weight balanced only if you decide so in decisions.md;
    do NOT use SMOTE. Return the fitted estimator.
    """
    raise NotImplementedError("Step 5: fit the PD model")


def vif_report(x_woe: pd.DataFrame) -> pd.DataFrame:
    """Variance Inflation Factor for each feature (flag VIF > 5 or 10)."""
    raise NotImplementedError("Step 5: compute VIF table")


def coefficient_table(model, feature_names: list[str]) -> pd.DataFrame:
    """Coefficients, odds ratios, p-values (via statsmodels), and sign check."""
    raise NotImplementedError("Step 5: build coefficient / p-value table")
