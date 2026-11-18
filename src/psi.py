"""Step 8: population stability index."""

from __future__ import annotations

import pandas as pd


def psi(expected: pd.Series, actual: pd.Series, buckets=10) -> float:
    """PSI = sum((actual% - expected%) * ln(actual% / expected%)).

    Use equal-width bands of `expected` (or deciles for scores).
    Interpretation: < 0.1 stable, 0.1–0.25 watch, > 0.25 shift.
    """
    raise NotImplementedError("Step 8: compute PSI for two distributions")


def psi_report(train: pd.DataFrame, test: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """PSI per variable plus PSI of the final score distribution."""
    raise NotImplementedError("Step 8: full PSI table")
