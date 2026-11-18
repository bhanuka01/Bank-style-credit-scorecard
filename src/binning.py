"""Step 4: WoE binning and Information Value.

Fit on TRAIN only. Never call fit_binning on the test set.
"""

from __future__ import annotations

import pandas as pd


def fit_binning(x_train: pd.DataFrame, y_train: pd.Series, max_bins=6):
    """Fit monotonic WoE bins for every feature.

    Returns a dict {feature: DataFrame with columns [bin, n, good, bad,
    good_pct, bad_pct, woe, iv]}. Use scorecardpy or optbinning.
    """
    raise NotImplementedError("Step 4: fit WoE bins on training data only")


def transform(df: pd.DataFrame, binning_tables: dict) -> pd.DataFrame:
    """Replace raw feature values with their WoE values using fitted bins."""
    raise NotImplementedError("Step 4: map raw values to WoE")


def iv_summary(binning_tables: dict) -> pd.DataFrame:
    """One row per feature with total IV, sorted descending.

    Drop IV < 0.02; flag IV > 0.5 as suspicious.
    """
    raise NotImplementedError("Step 4: summarise IV per feature")
