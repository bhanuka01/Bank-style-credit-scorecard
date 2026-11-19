"""Steps 1–3: load, profile, clean, and split the data."""

from __future__ import annotations

import pandas as pd


def load_raw(path) -> pd.DataFrame:
    """Load cs-training.csv. Drop an unnamed index column if Kaggle added one."""
    raise NotImplementedError("Step 1: read CSV and drop unnamed index column")


def profile(df: pd.DataFrame) -> dict:
    """Return shape, dtypes, missing counts, describe(), and target rate.

    Also flag odd values: 96/98 in past-due columns, age == 0, negative values.
    """
    raise NotImplementedError("Step 1: build the EDA profile dictionary")


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """DEPRECATED — do not use. See scorecard_workflow.md sections 1 and 6.

    Cleaning is now implemented as `CreditCleaner` in src/pipeline.py, fitted
    inside each CV fold. Creating a full-data `clean.csv` before splitting is
    leakage, even if the split itself is stratified.
    """
    raise NotImplementedError("Use src.pipeline.CreditCleaner instead (Step 3)")


def split(df: pd.DataFrame, test_size=0.30, seed=42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratified 70/30 holdout (Step 2). Assert no overlap and similar target rates.

    Call this BEFORE any cleaning or binning. The test set is locked afterwards.
    """
    raise NotImplementedError("Step 2: stratified split with leakage assertions")
