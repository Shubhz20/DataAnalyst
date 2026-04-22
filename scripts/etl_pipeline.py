"""
etl_pipeline.py — Parameterized ETL for the Online Retail II dataset.

This script mirrors the logic in notebooks/01_extraction.ipynb and
notebooks/02_cleaning.ipynb so the pipeline is reproducible from the command line:

    python scripts/etl_pipeline.py \
        --raw data/raw/online_retail_II.xlsx \
        --out data/processed/online_retail_II_clean.csv

The notebooks are the source of truth for exploration and analysis; this script
is the productionized / reproducible version used for re-running the pipeline.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("etl")


# ---------------------------------------------------------------------------
# EXTRACT
# ---------------------------------------------------------------------------

def extract(raw_path: Path) -> pd.DataFrame:
    """Load both sheets from the Online Retail II Excel file and concatenate."""
    log.info("Extracting from %s", raw_path)
    xl = pd.ExcelFile(raw_path)
    log.info("Sheets found: %s", xl.sheet_names)
    dfs = [xl.parse(sheet_name=s) for s in xl.sheet_names]
    df = pd.concat(dfs, ignore_index=True)
    log.info("Extracted %d rows, %d columns", *df.shape)
    return df


# ---------------------------------------------------------------------------
# CLEAN
# ---------------------------------------------------------------------------

NON_PRODUCT_STOCK_CODES = {"POST", "D", "M", "BANK CHARGES", "AMAZONFEE", "DOT", "CRUK", "PADS", "S"}

COUNTRY_STANDARDIZATION = {
    "EIRE": "Ireland",
    "RSA": "South Africa",
    "USA": "United States",
    "Channel Islands": "United Kingdom",  # crown dependency — fold into UK for analysis
}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the documented cleaning steps. Each step logged for auditability."""
    df = df.copy()
    n0 = len(df)
    log.info("Cleaning start: %d rows", n0)

    # 1. Standardize column names (space → snake_case)
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.lower()
    )

    # 2. Parse types
    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["customer_id"] = df["customer_id"].astype("Int64")  # nullable int

    # 3. Drop rows missing critical fields (InvoiceDate / StockCode)
    crit = df["invoicedate"].isna() | df["stockcode"].isna()
    log.info("Dropping %d rows missing InvoiceDate or StockCode", int(crit.sum()))
    df = df[~crit]

    # 4. Flag returns (invoice starts with 'C' OR negative quantity)
    df["is_return"] = (
        df["invoice"].astype(str).str.startswith("C")
        | (df["quantity"] < 0)
    )
    log.info("Flagged %d return rows (%.1f%%)", int(df["is_return"].sum()), df["is_return"].mean() * 100)

    # 5. Flag registered customers
    df["is_registered"] = df["customer_id"].notna()
    log.info("Registered customers cover %.1f%% of rows", df["is_registered"].mean() * 100)

    # 6. Flag non-product stock codes
    df["is_product"] = ~df["stockcode"].astype(str).str.upper().isin(NON_PRODUCT_STOCK_CODES)

    # 7. Compute line revenue (can be negative — that's OK for net-revenue KPIs)
    df["line_revenue"] = df["quantity"] * df["price"]

    # 8. Clean description (strip, title case the common ones)
    df["description"] = df["description"].astype(str).str.strip()
    df.loc[df["description"].isin(["", "nan", "None"]), "description"] = np.nan

    # 9. Standardize country
    df["country_clean"] = df["country"].replace(COUNTRY_STANDARDIZATION)

    # 10. Time features
    df["invoice_year_month"] = df["invoicedate"].dt.to_period("M").astype(str)
    df["invoice_hour"] = df["invoicedate"].dt.hour
    df["invoice_day_of_week"] = df["invoicedate"].dt.day_name()

    # 11. Coarse category hint (keyword-based — best-effort only; not authoritative)
    df["product_category_hint"] = df["description"].apply(_category_hint)

    # 12. Drop exact duplicate rows (same invoice + stockcode + quantity + price)
    before = len(df)
    df = df.drop_duplicates(subset=["invoice", "stockcode", "quantity", "price", "invoicedate"])
    log.info("Dropped %d exact duplicate rows", before - len(df))

    log.info("Cleaning complete: %d rows (from %d, %.1f%% retained)", len(df), n0, len(df) / n0 * 100)
    return df


def _category_hint(desc: str | float) -> str:
    """Very coarse category mapping based on keyword presence in the description."""
    if not isinstance(desc, str):
        return "unknown"
    d = desc.lower()
    keywords = {
        "christmas": ["christmas", "xmas", "advent"],
        "bag": ["bag", "jumbo", "lunch box"],
        "mug_cup": ["mug", "cup", "teacup"],
        "candle_light": ["candle", "t-light", "lantern"],
        "decor": ["decoration", "ornament", "hanging"],
        "paper": ["paper", "napkin", "card"],
        "kitchen": ["cake", "bake", "kitchen", "apron"],
        "garden": ["garden", "plant", "flower"],
        "kids_toys": ["toy", "kids", "children", "doll"],
    }
    for cat, kws in keywords.items():
        if any(kw in d for kw in kws):
            return cat
    return "other"


# ---------------------------------------------------------------------------
# LOAD
# ---------------------------------------------------------------------------

def load(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    log.info("Wrote %d rows to %s", len(df), out_path)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, required=True, help="Path to raw xlsx")
    ap.add_argument("--out", type=Path, required=True, help="Output CSV path")
    args = ap.parse_args()

    df = extract(args.raw)
    df = clean(df)
    load(df, args.out)


if __name__ == "__main__":
    main()
