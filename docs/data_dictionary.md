# Data Dictionary — Online Retail II

**Source:** UCI Machine Learning Repository, dataset 502
**URL:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
**Grain:** One row per line item on an invoice (a single invoice contains multiple rows — one per product)
**Time range:** 01-Dec-2009 to 09-Dec-2011
**File format:** Two Excel sheets (`Year 2009-2010` and `Year 2010-2011`), concatenated during extraction

## Raw columns (as delivered by UCI)

| # | Column | Type | Description | Known issues |
|---|---|---|---|---|
| 1 | `Invoice` | string | Invoice number. Prefixed with `C` for cancellations/returns (e.g. `C536379`). | Mixed prefix encoding — must be parsed to identify returns |
| 2 | `StockCode` | string | 5-digit product code. Some service/admin codes are non-numeric (e.g. `POST`, `D`, `M`, `BANK CHARGES`). | Non-product codes inflate row counts — filter for analysis |
| 3 | `Description` | string | Free-text product name. | Missing for ~4,000 rows. Inconsistent casing. Duplicate descriptions across stock codes. |
| 4 | `Quantity` | integer | Units sold on this line. | **Negative** values indicate returns/cancellations — must be handled explicitly |
| 5 | `InvoiceDate` | datetime | Timestamp of invoice, minute precision. | None significant |
| 6 | `Price` | float | Unit price in GBP (£). | Zero and negative values present (bad debt adjustments, samples) — filter or flag |
| 7 | `Customer ID` | float | Unique customer ID. | **~25% missing** — these are guest/non-registered checkouts; they are real transactions but cannot be attributed to a customer for segmentation |
| 8 | `Country` | string | Country of customer. | Mostly "United Kingdom" (~90%). Some inconsistencies like `EIRE` vs `Ireland`, `Unspecified`, `European Community` |

## Engineered columns (added during cleaning — defined by us)

| Column | Type | Definition | Computed in |
|---|---|---|---|
| `LineRevenue` | float | `Quantity × Price` (GBP) | `02_cleaning.ipynb` |
| `IsReturn` | bool | `True` if `Invoice` starts with "C" OR `Quantity < 0` | `02_cleaning.ipynb` |
| `IsRegistered` | bool | `True` if `Customer ID` is not null | `02_cleaning.ipynb` |
| `InvoiceYearMonth` | string (YYYY-MM) | Month bucket of `InvoiceDate` | `02_cleaning.ipynb` |
| `InvoiceHour` | int | Hour of day from `InvoiceDate` | `02_cleaning.ipynb` |
| `InvoiceDayOfWeek` | string | Day name from `InvoiceDate` | `02_cleaning.ipynb` |
| `CountryClean` | string | Standardized country (EIRE → Ireland, etc.) | `02_cleaning.ipynb` |
| `ProductCategoryHint` | string | Coarse category from Description keyword tokens (Christmas, bag, mug, etc.) — best-effort, not authoritative | `02_cleaning.ipynb` |

## KPI layer (computed in `05_final_load_prep.ipynb`)

| KPI | Formula | Grain | Business meaning |
|---|---|---|---|
| Net Revenue | `Σ(LineRevenue where not IsReturn) − Σ(|LineRevenue| where IsReturn)` | month / country / segment | Revenue after returns — the KPI that actually matters to the P&L |
| Return Rate | `rows(IsReturn) / rows(all)` | product / country / month | Quality signal; high return rate flags supply-chain or listing-accuracy issues |
| Repeat Purchase Rate | `customers with ≥2 invoices / total registered customers` | month | Health of the retention engine |
| Avg Order Value (AOV) | `Net Revenue per invoice` | month / segment | Pricing + basket composition health |
| RFM Score | Recency (days since last purchase), Frequency (invoices), Monetary (net rev) — quintiled and concatenated | customer | Customer segmentation for retention prioritization |
| Top-20% Revenue Concentration | `rev from top 20% of customers / total rev` | month | Pareto — measures dependence risk on a small customer base |

All KPIs are computed over the **registered-customer subset** unless noted; guest-checkout rows are excluded from customer-level KPIs but included in product-level KPIs.

## Known data-quality caveats (must be disclosed in final report)

1. **Guest checkouts (~25% of rows)** cannot be attributed to a customer — customer-level analysis covers ~75% of revenue only.
2. **Non-product stock codes** (`POST`, `M`, `D`, `BANK CHARGES`, `AMAZONFEE`, `DOT`, `CRUK`) are adjustments/services — excluded from product analysis, retained for revenue totals with a flag.
3. **Returns create negative rows** — need to be netted against the matching original invoice where possible; otherwise treated as standalone revenue adjustments.
4. **Heavy UK skew** (~90% of rows) — international analysis is directional only, not statistically powerful for small-country segments.
