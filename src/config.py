"""Paths, constants, and scaling parameters shared by all notebooks."""

from pathlib import Path

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"

RAW_FILE = DATA_RAW / "cs-training.csv"
CLEAN_FILE = DATA_PROCESSED / "clean.csv"
TRAIN_FILE = DATA_PROCESSED / "train.csv"
TEST_FILE = DATA_PROCESSED / "test.csv"

# --- Columns -----------------------------------------------------------------
TARGET = "SeriousDlqin2yrs"
PAST_DUE_COLS = [
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate",
]
SPECIAL_PAST_DUE_CODES = (96, 98)  # treat as missing / erroneous
CAP_COLS = ["DebtRatio", "RevolvingUtilizationOfUnsecuredLines"]

# --- Split / model -----------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.30
MAX_BINS = 6
IV_MIN = 0.02       # drop below this
IV_SUSPICIOUS = 0.5  # flag above this

# --- Scorecard scaling (Step 7) ---------------------------------------------
BASE_SCORE = 600
BASE_ODDS = 50.0    # 50:1
PDO = 20            # points to double the odds
