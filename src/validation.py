"""Step 6: discrimination and calibration on TEST data."""

from __future__ import annotations

import pandas as pd


def auc_gini_ks(y_true: pd.Series, y_score: pd.Series) -> dict:
    """Return AUC, Gini = 2*AUC - 1, and the KS statistic with its cut-off.

    Assert abs(gini - (2*auc - 1)) < 1e-6.
    """
    raise NotImplementedError("Step 6: compute AUC, Gini, KS")


def plot_roc(y_true, y_score, save_path) -> None:
    """ROC curve with AUC in the legend. Save to reports/figures/."""
    raise NotImplementedError("Step 6: ROC plot")


def plot_ks(y_true, y_score, save_path) -> None:
    """Cumulative good/bad distributions with the KS gap marked."""
    raise NotImplementedError("Step 6: KS plot")


def calibration_table(y_true, y_score, bins=10) -> pd.DataFrame:
    """Predicted vs. actual default rate by decile of predicted PD."""
    raise NotImplementedError("Step 6: calibration table and plot")
