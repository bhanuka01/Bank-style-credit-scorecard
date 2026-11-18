"""Step 7: convert the logistic model into scorecard points."""

from __future__ import annotations

import pandas as pd


def factor_offset(base_score=600, base_odds=50.0, pdo=20) -> tuple[float, float]:
    """Factor = PDO / ln(2); Offset = base_score - Factor * ln(base_odds)."""
    raise NotImplementedError("Step 7: compute Factor and Offset")


def build_scorecard(model, binning_tables: dict, n_features: int) -> pd.DataFrame:
    """Points per bin = -(coef * WoE + intercept/n) * Factor + Offset/n.

    Returns a long table: feature, bin, WoE, coefficient, points.
    """
    raise NotImplementedError("Step 7: build the scorecard table")


def score_borrower(row: dict, scorecard: pd.DataFrame, base_score: float) -> float:
    """Sum the points for one borrower and return their total score."""
    raise NotImplementedError("Step 7: score one borrower (for the hand-check)")
