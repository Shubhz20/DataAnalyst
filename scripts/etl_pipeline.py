
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# LOGGING SETUP
# ---------------------------------------------------------------------------

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("etl_pipeline")

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

# Paths relative to project root (overridable via CLI)
DEFAULT_RAW_PATH = Path("data/raw/raw_dataset.csv")
DEFAULT_OUT_PATH = Path("data/processed/cleaned_dataset.csv")

# Columns that MUST be present in the raw file
REQUIRED_COLUMNS = {
    "Order No", "Order Date", "Customer Name", "City", "State",
    "Customer Type", "Order Priority", "Product Name", "Product Category",
    "Ship Mode", "Cost Price", "Retail Price", "Profit Margin",
    "Order Quantity",
}

# Columns whose values are stored as currency strings ("$1,234.56")
CURRENCY_COLUMNS = [
    "Cost Price", "Retail Price", "Profit Margin",
    "Sub Total", "Discount $", "Order Total", "Shipping Cost", "Total",
]

# Columns that must be non-negative after cleaning
NON_NEGATIVE_COLUMNS = ["Order Quantity", "Cost Price", "Retail Price", "Shipping Cost"]

# Numeric columns subject to outlier analysis
OUTLIER_COLUMNS = ["Order Quantity", "Cost Price", "Retail Price", "Profit Margin", "Order Total"]

# IQR multiplier for outlier fence
IQR_MULTIPLIER = 3.0


# ---------------------------------------------------------------------------
# PHASE 1 — EXTRACT
# ---------------------------------------------------------------------------

def extract(raw_path: Path) -> pd.DataFrame:
    """
    Read the raw CSV into a DataFrame.

    Validates:
      - File exists on disk
      - File is non-empty
      - All required columns are present
    """
    log.info("=" * 60)
    log.info("PHASE 1 — EXTRACT")
    log.info("=" * 60)

    # File existence check
    if not raw_path.exists():
        log.error("Raw file not found: %s", raw_path.resolve())
        raise FileNotFoundError(f"Raw file not found: {raw_path.resolve()}")

    log.info("Reading raw file: %s", raw_path.resolve())

    try:
        df = pd.read_csv(raw_path, dtype=str, encoding="utf-8")
    except UnicodeDecodeError:
        log.warning("UTF-8 decode failed — retrying with latin-1 encoding")
        df = pd.read_csv(raw_path, dtype=str, encoding="latin-1")
    except Exception as exc:
        log.error("Failed to read CSV: %s", exc)
        raise

    if df.empty:
        raise ValueError("Raw file is empty — nothing to process.")

    log.info("Raw extract complete: %d rows x %d columns", *df.shape)

    # Schema validation
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Required columns missing from raw file: {missing_cols}")
    log.info("Schema check passed — all required columns present")

    return df


# ---------------------------------------------------------------------------
# PHASE 2 — INITIAL VALIDATION
# ---------------------------------------------------------------------------

def validate_raw(df: pd.DataFrame) -> None:
    """
    Log a diagnostic summary of the raw DataFrame.
    Raises warnings on data quality issues but does NOT halt the pipeline.
    """
    log.info("=" * 60)
    log.info("PHASE 2 — INITIAL VALIDATION")
    log.info("=" * 60)

    log.info("Shape          : %d rows × %d columns", *df.shape)
    log.info("Columns        : %s", list(df.columns))

    # Missing values
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if null_cols.empty:
        log.info("Missing values : None found")
    else:
        log.warning("Missing values detected:")
        for col, cnt in null_cols.items():
            log.warning("  %-30s %d (%.1f%%)", col, cnt, cnt / len(df) * 100)

    # Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count:
        log.warning("Duplicate rows : %d found", dup_count)
    else:
        log.info("Duplicate rows : None found")

    # Data types (all str because we read with dtype=str)
    log.info("All columns loaded as object (string) — types assigned in Transform phase")
    log.info("Initial validation complete")


# ---------------------------------------------------------------------------
# PHASE 3 — TRANSFORM
# ---------------------------------------------------------------------------

# -- Helper utilities --------------------------------------------------------

def _strip_currency(series: pd.Series) -> pd.Series:
    """Remove '$' and ',' from currency strings and convert to float."""
    return (
        series.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .replace({"": np.nan, "nan": np.nan, "None": np.nan})
        .astype(float)
    )


def _strip_percent(series: pd.Series) -> pd.Series:
    """Remove '%' and convert to float (e.g. '2%' → 2.0)."""
    return (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "nan": np.nan, "None": np.nan})
        .astype(float)
    )


def _standardise_text(series: pd.Series) -> pd.Series:
    """Strip whitespace and apply title-case to a string column."""
    return series.astype(str).str.strip().str.title().replace({"Nan": np.nan, "None": np.nan})


# -- Sub-steps ---------------------------------------------------------------

def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise column names to snake_case for downstream consistency."""
    rename_map = {
        "Order No":          "order_no",
        "Order Date":        "order_date",
        "Customer Name":     "customer_name",
        "Address":           "address",
        "City":              "city",
        "State":             "state",
        "Customer Type":     "customer_type",
        "Account Manager":   "account_manager",
        "Order Priority":    "order_priority",
        "Product Name":      "product_name",
        "Product Category":  "product_category",
        "Product Container": "product_container",
        "Ship Mode":         "ship_mode",
        "Ship Date":         "ship_date",
        "Cost Price":        "cost_price",
        "Retail Price":      "retail_price",
        "Profit Margin":     "profit_margin",
        "Order Quantity":    "order_quantity",
        "Sub Total":         "sub_total",
        "Discount %":        "discount_pct",
        "Discount $":        "discount_amt",
        "Order Total":       "order_total",
        "Shipping Cost":     "shipping_cost",
        "Total":             "total",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    log.info("Columns renamed to snake_case")
    return df


def _clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and normalise casing for all object columns."""
    text_cols = [
        "customer_name", "city", "state", "customer_type",
        "account_manager", "order_priority", "product_name",
        "product_category", "ship_mode",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = _standardise_text(df[col])

    # Optional columns that may not exist in all dataset versions
    for col in ["address", "product_container"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"Nan": np.nan, "None": np.nan})

    log.info("Text columns stripped and title-cased")
    return df


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Order Date and Ship Date from DD-MM-YYYY strings to datetime."""
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col], dayfirst=True, errors="coerce"
            )
            bad = df[col].isna().sum()
            if bad:
                log.warning("  %s: %d rows could not be parsed as date (set to NaT)", col, bad)
    log.info("Date columns parsed to datetime64")
    return df


def _parse_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Convert currency strings, percentages, and quantities to numeric types."""
    # Currency columns
    for col in CURRENCY_COLUMNS:
        snake = col.lower().replace(" ", "_").replace("%", "pct").replace("$", "amt")
        # handle the exact snake names we assigned
        mapped = {
            "Cost Price":    "cost_price",
            "Retail Price":  "retail_price",
            "Profit Margin": "profit_margin",
            "Sub Total":     "sub_total",
            "Discount $":    "discount_amt",
            "Order Total":   "order_total",
            "Shipping Cost": "shipping_cost",
            "Total":         "total",
        }
        target = mapped.get(col, snake)
        if target in df.columns:
            df[target] = _strip_currency(df[target])

    # Discount percentage
    if "discount_pct" in df.columns:
        df["discount_pct"] = _strip_percent(df["discount_pct"])

    # Order Quantity → integer
    if "order_quantity" in df.columns:
        df["order_quantity"] = pd.to_numeric(
            df["order_quantity"].astype(str).str.strip(), errors="coerce"
        )

    log.info("Numeric columns parsed (currency symbols and commas removed)")
    return df


def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute or drop missing values with documented business logic.

    Strategy
    --------
    - order_priority  : fill with 'Not Specified' (categorical, low impact)
    - ship_mode       : fill with mode (most common shipping method)
    - account_manager : fill with 'Unknown'
    - product_container: fill with 'Unknown'
    - discount_pct/amt: fill with 0 (no discount assumed when absent)
    - shipping_cost   : fill with median (reasonable cost estimate)
    - Rows missing order_date, product_name, cost_price, retail_price dropped.
    """
    before = len(df)

    # Drop rows where critical fields are missing
    critical = ["order_date", "product_name", "cost_price", "retail_price", "order_quantity"]
    df = df.dropna(subset=[c for c in critical if c in df.columns]).copy()
    dropped = before - len(df)
    if dropped:
        log.warning("Dropped %d rows missing critical fields", dropped)

    # Categorical fills
    if "order_priority" in df.columns:
        df["order_priority"] = df["order_priority"].fillna("Not Specified")

    if "ship_mode" in df.columns:
        mode_val = df["ship_mode"].mode(dropna=True)
        fill_mode: str = str(mode_val.iloc[0]) if not mode_val.empty else "Unknown"
        df["ship_mode"] = df["ship_mode"].fillna(fill_mode)

    for col in ["account_manager", "product_container", "customer_type"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Numeric fills
    for col in ["discount_pct", "discount_amt"]:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)

    if "shipping_cost" in df.columns:
        df["shipping_cost"] = df["shipping_cost"].fillna(df["shipping_cost"].median())

    log.info("Missing values handled — %d rows remaining", len(df))
    return df


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicate rows, keeping the first occurrence."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    log.info("Duplicate rows removed: %d (%.2f%%)", removed, removed / before * 100 if before else 0)
    return df


def _remove_impossible_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that violate business constraints:
      - order_quantity must be ≥ 1
      - cost_price and retail_price must be > 0
      - cost_price must be ≤ retail_price (no selling below cost)
    """
    before = len(df)

    if "order_quantity" in df.columns:
        df = df[df["order_quantity"] >= 1]

    for col in ["cost_price", "retail_price"]:
        if col in df.columns:
            df = df[df[col] > 0]

    if {"cost_price", "retail_price"}.issubset(df.columns):
        invalid_margin = df["cost_price"] > df["retail_price"]
        n_invalid = invalid_margin.sum()
        if n_invalid:
            log.warning(
                "Removing %d rows where cost_price > retail_price (business logic violation)",
                n_invalid,
            )
            df = df[~invalid_margin]

    removed = before - len(df)
    log.info("Impossible-value rows removed: %d", removed)
    return df


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived columns useful for analysis and Tableau dashboards."""

    # Recalculate profit margin cleanly from source columns
    if {"retail_price", "cost_price"}.issubset(df.columns):
        df["profit_margin_calc"] = df["retail_price"] - df["cost_price"]
        df["profit_margin_pct"] = (
            df["profit_margin_calc"] / df["retail_price"] * 100
        ).round(2)

    # Revenue per line item
    if {"retail_price", "order_quantity"}.issubset(df.columns):
        df["line_revenue"] = (df["retail_price"] * df["order_quantity"]).round(2)

    # Order date features
    if "order_date" in df.columns:
        df["order_year"]        = df["order_date"].dt.year
        df["order_month"]       = df["order_date"].dt.month
        df["order_month_name"]  = df["order_date"].dt.strftime("%B")
        df["order_quarter"]     = df["order_date"].dt.quarter.map(
            {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
        )
        df["order_day_of_week"] = df["order_date"].dt.day_name()
        df["order_year_month"]  = df["order_date"].dt.to_period("M").astype(str)

    # Shipping lead time (days)
    if {"order_date", "ship_date"}.issubset(df.columns):
        df["shipping_lead_days"] = (df["ship_date"] - df["order_date"]).dt.days
        # Negative lead times are data errors — nullify them
        df.loc[df["shipping_lead_days"] < 0, "shipping_lead_days"] = np.nan

    log.info("Derived features engineered")
    return df


# -- Master transform --------------------------------------------------------

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute all transformation steps in order and return the cleaned DataFrame.
    """
    log.info("=" * 60)
    log.info("PHASE 3 — TRANSFORM")
    log.info("=" * 60)

    df = _rename_columns(df)
    df = _clean_text_columns(df)
    df = _parse_dates(df)
    df = _parse_numerics(df)
    df = _handle_missing_values(df)
    df = _remove_duplicates(df)
    df = _remove_impossible_values(df)
    df = _engineer_features(df)

    log.info("Transform complete: %d rows × %d columns", *df.shape)
    return df


# ---------------------------------------------------------------------------
# PHASE 4 — OUTLIER HANDLING
# ---------------------------------------------------------------------------

def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and cap outliers in key numeric columns using the IQR method.

    Business rationale
    ------------------
    We CAP (Winsorise) rather than DROP outliers because extreme but valid
    bulk orders should influence aggregates only mildly.  A multiplier of
    IQR_MULTIPLIER=3.0 is deliberately conservative to preserve real large
    orders while removing data-entry errors.

    A companion column `<col>_is_outlier` (bool) is added for transparency,
    so analysts can filter outliers in Tableau if needed.
    """
    log.info("=" * 60)
    log.info("PHASE 4 — OUTLIER HANDLING")
    log.info("=" * 60)

    for col in OUTLIER_COLUMNS:
        if col not in df.columns:
            continue

        series = df[col].dropna()
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - IQR_MULTIPLIER * iqr
        upper = q3 + IQR_MULTIPLIER * iqr

        outlier_mask = (df[col] < lower) | (df[col] > upper)
        n_out = int(outlier_mask.sum())

        df[f"{col}_is_outlier"] = outlier_mask

        if n_out:
            log.warning(
                "%-20s  outliers: %4d  fence: [%.2f, %.2f]  → capped",
                col, n_out, lower, upper,
            )
            df[col] = df[col].clip(lower=lower, upper=upper)
        else:
            log.info("%-20s  outliers: none detected", col)

    log.info("Outlier handling complete")
    return df


# ---------------------------------------------------------------------------
# PHASE 5 — FINAL VALIDATION
# ---------------------------------------------------------------------------

def validate_clean(df: pd.DataFrame) -> None:
    """
    Run post-transform checks and log a clean data summary.
    Raises RuntimeError if any critical assertion fails.
    """
    log.info("=" * 60)
    log.info("PHASE 5 — FINAL VALIDATION")
    log.info("=" * 60)

    # Duplicate check
    dup = df.duplicated().sum()
    if dup:
        raise RuntimeError(f"Final dataset still contains {dup} duplicate rows — investigate.")
    log.info("Duplicates check   : PASSED (0 duplicates)")

    # Null check on critical columns
    critical_clean = ["order_date", "product_name", "cost_price", "retail_price", "order_quantity"]
    for col in critical_clean:
        if col not in df.columns:
            continue
        nulls = df[col].isna().sum()
        if nulls:
            raise RuntimeError(f"Critical column '{col}' still has {nulls} nulls after cleaning.")
    log.info("Null check         : PASSED (critical columns are complete)")

    # Cost ≤ Retail check
    if {"cost_price", "retail_price"}.issubset(df.columns):
        violations = (df["cost_price"] > df["retail_price"]).sum()
        if violations:
            raise RuntimeError(f"{violations} rows still have cost_price > retail_price.")
    log.info("Margin logic check : PASSED (cost_price ≤ retail_price everywhere)")

    # Non-negative check
    for col in NON_NEGATIVE_COLUMNS:
        if col not in df.columns:
            continue
        neg = (df[col] < 0).sum()
        if neg:
            raise RuntimeError(f"Column '{col}' has {neg} negative values after cleaning.")
    log.info("Non-negative check : PASSED")

    # Summary statistics
    log.info("-" * 60)
    log.info("CLEAN DATASET SUMMARY")
    log.info("-" * 60)
    log.info("Final shape        : %d rows × %d columns", *df.shape)
    log.info("Date range         : %s  →  %s",
             df["order_date"].min().date() if "order_date" in df.columns else "N/A",
             df["order_date"].max().date() if "order_date" in df.columns else "N/A")

    if "product_category" in df.columns:
        log.info("Product categories : %s", sorted(df["product_category"].dropna().unique().tolist()))

    if "customer_type" in df.columns:
        log.info("Customer types     : %s", sorted(df["customer_type"].dropna().unique().tolist()))

    if "order_priority" in df.columns:
        log.info("Order priorities   : %s", sorted(df["order_priority"].dropna().unique().tolist()))

    for col in ["order_quantity", "cost_price", "retail_price", "profit_margin_pct", "line_revenue"]:
        if col in df.columns:
            log.info(
                "%-25s  mean=%-10.2f  min=%-10.2f  max=%.2f",
                col, df[col].mean(), df[col].min(), df[col].max(),
            )

    log.info("Final validation   : ALL CHECKS PASSED")


# ---------------------------------------------------------------------------
# PHASE 6 — LOAD
# ---------------------------------------------------------------------------

def load(df: pd.DataFrame, out_path: Path) -> None:
    """
    Write the cleaned DataFrame to CSV.
    Creates the output directory if it does not already exist.
    """
    log.info("=" * 60)
    log.info("PHASE 6 — LOAD")
    log.info("=" * 60)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    log.info("Saved cleaned dataset: %s", out_path.resolve())
    log.info("File size          : %.1f KB", size_kb)
    log.info("Rows written       : %d", len(df))
    log.info("Columns written    : %d", len(df.columns))
    log.info("=" * 60)
    log.info("ETL PIPELINE COMPLETE — READY FOR ANALYSIS & TABLEAU")
    log.info("=" * 60)


# ---------------------------------------------------------------------------
# ARGUMENT PARSING
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retail Sales ETL Pipeline — Capstone 2, ADYPU",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--raw",
        type=Path,
        default=DEFAULT_RAW_PATH,
        help="Path to raw input CSV file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_PATH,
        help="Path for cleaned output CSV file",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def run_pipeline(raw_path: Path, out_path: Path) -> pd.DataFrame:
    """
    Orchestrate all ETL phases and return the final clean DataFrame.
    Can be imported and called directly from notebooks for testing.
    """
    log.info("=" * 60)
    log.info("RETAIL SALES ETL PIPELINE — START")
    log.info("=" * 60)
    log.info("Raw path : %s", raw_path)
    log.info("Out path : %s", out_path)

    df_raw   = extract(raw_path)
    validate_raw(df_raw)
    df_clean = transform(df_raw)
    df_clean = handle_outliers(df_clean)
    validate_clean(df_clean)
    load(df_clean, out_path)

    return df_clean


if __name__ == "__main__":
    args = _parse_args()

    # Fallback: if default raw path doesn't exist, try the actual filename
    raw_path = args.raw
    if not raw_path.exists() and raw_path == DEFAULT_RAW_PATH:
        alt = raw_path.parent / "data.csv"
        if alt.exists():
            log.info("Default raw file not found — falling back to: %s", alt)
            raw_path = alt

    try:
        run_pipeline(raw_path, args.out)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        log.error("Pipeline failed: %s", exc)
        sys.exit(1)
