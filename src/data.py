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
    """Apply the cleaning rules from decisions.md.

    Returns (clean_df, cleaning_log). Rules:
      - MonthlyIncome: median imputation
      - NumberOfDependents: 0 or median (record your choice)
      - 96/98 past-due codes: replace with NaN then impute/mode
      - age == 0: treat as missing
      - cap DebtRatio and RevolvingUtilization at a chosen percentile
    Fit all imputation statistics on TRAIN only in Step 3 — see notes there.
    """
    raise NotImplementedError("Step 2: implement cleaning and return a log")


def split(df: pd.DataFrame, test_size=0.30, seed=42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratified train/test split. Assert no index overlap and similar target rates."""
    raise NotImplementedError("Step 3: stratified split with leakage assertions")
