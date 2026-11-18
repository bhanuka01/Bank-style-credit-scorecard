"""Step 9: XGBoost benchmark and SHAP explainability."""

from __future__ import annotations

import pandas as pd


def fit_xgboost(x_train: pd.DataFrame, y_train: pd.Series, seed=42):
    """Fit a benchmark gradient-boosted model on the same WoE features."""
    raise NotImplementedError("Step 9: fit the XGBoost benchmark")


def shap_summary(model, x_sample: pd.DataFrame, save_path) -> None:
    """Global SHAP summary (beeswarm or bar) saved to reports/figures/."""
    raise NotImplementedError("Step 9: SHAP summary plot")


def importance_comparison(scorecard: pd.DataFrame, shap_importance: pd.Series) -> pd.DataFrame:
    """Rank features by scorecard |points| range vs. SHAP mean |value|.

    Return a side-by-side table with rank columns for discussion.
    """
    raise NotImplementedError("Step 9: compare the two importance rankings")
