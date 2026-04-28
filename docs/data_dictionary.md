# Data Dictionary — Retail Insights: A Comprehensive Sales Dataset

**Source:** Kaggle 
**URL:** https://www.kaggle.com/datasets/rajneesh231/retail-insights-a-comprehensive-sales-dataset
**Grain:** One row per customer order transaction
**Time range:** February 2013 – February 2017
**File format:** CSV (`data/raw/data.csv`) — 5,000 rows, 24 columns
**Geography:** Australian states (NSW, VIC, QLD, and others)
**Cleaned output:** `data/processed/cleaned_dataset.csv` — 4,995 rows, 34 columns

---

## Raw columns (as delivered by source)

| # | Raw Column | Cleaned Name | Type | Description | Known issues |
|---|---|---|---|---|---|
| 1 | `Order No` | `order_no` | string | Unique order identifier (e.g. `4293-1`) | None significant |
| 2 | `Order Date` | `order_date` | string → datetime | Date the order was placed (`DD-MM-YYYY`) | Non-standard date format — must be parsed with `dayfirst=True` |
| 3 | `Customer Name` | `customer_name` | string | Full name of the customer | Minor whitespace inconsistencies |
| 4 | `Address` | `address` | string | Customer street address | 1 missing value |
| 5 | `City` | `city` | string | City of the customer | Inconsistent casing in some rows |
| 6 | `State` | `state` | string | Australian state code (e.g. NSW, VIC) | Inconsistent casing in some rows |
| 7 | `Customer Type` | `customer_type` | string | Segment: Consumer, Corporate, Small Business, Home Office | None significant |
| 8 | `Account Manager` | `account_manager` | string | Name of the assigned account manager | None significant |
| 9 | `Order Priority` | `order_priority` | string | Critical / High / Medium / Low | Some rows missing — filled with `Not Specified` |
| 10 | `Product Name` | `product_name` | string | Full product description | Inconsistent casing |
| 11 | `Product Category` | `product_category` | string | Furniture / Office Supplies / Technology | None significant |
| 12 | `Product Container` | `product_container` | string | Packaging type (Small Box, Wrap Bag, Small Pack, etc.) | None significant |
| 13 | `Ship Mode` | `ship_mode` | string | Shipping method (Regular Air, Express Air, etc.) | None significant |
| 14 | `Ship Date` | `ship_date` | string → datetime | Date the order was shipped (`DD-MM-YYYY`) | Same format issue as `Order Date` |
| 15 | `Cost Price` | `cost_price` | string → float | Wholesale cost per unit (stored as `$156.50`) | Dollar sign and commas must be stripped; 4 rows where `Cost Price > Retail Price` — removed |
| 16 | `Retail Price` | `retail_price` | string → float | Selling price per unit (stored as `$300.97`) | Same formatting as `Cost Price` |
| 17 | `Profit Margin` | `profit_margin` | string → float | Raw margin value (`Retail Price − Cost Price`) stored as currency string | Recalculated cleanly as `profit_margin_calc` in ETL |
| 18 | `Order Quantity` | `order_quantity` | string → int | Number of units ordered | 1 missing value — row dropped; values must be ≥ 1 |
| 19 | `Sub Total` | `sub_total` | string → float | `Retail Price × Order Quantity` before discounts | Currency formatting |
| 20 | `Discount %` | `discount_pct` | string → float | Discount percentage (stored as `2%`) | Percent sign must be stripped |
| 21 | `Discount $` | `discount_amt` | string → float | Discount amount in dollars | Currency formatting |
| 22 | `Order Total` | `order_total` | string → float | Sub Total after discount | Currency formatting |
| 23 | `Shipping Cost` | `shipping_cost` | string → float | Cost of shipping the order | Currency formatting |
| 24 | `Total` | `total` | string → float | Final total including shipping | Currency formatting |

---

## Engineered columns (added by `scripts/etl_pipeline.py`)

| Column | Type | Definition | Computed in |
|---|---|---|---|
| `profit_margin_calc` | float | `retail_price − cost_price` — recalculated clean margin in dollars | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `profit_margin_pct` | float | `(retail_price − cost_price) / retail_price × 100` — margin as percentage, rounded to 2dp | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `line_revenue` | float | `retail_price × order_quantity` — total revenue for this line item | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_year` | int | Calendar year from `order_date` | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_month` | int | Month number (1–12) from `order_date` | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_month_name` | string | Full month name (January, February, …) | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_quarter` | string | Q1 / Q2 / Q3 / Q4 derived from `order_date` | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_day_of_week` | string | Day name (Monday, Tuesday, …) from `order_date` | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `order_year_month` | string (YYYY-MM) | Month bucket for time-series aggregation | `etl_pipeline.py` / `02_cleaning.ipynb` |
| `shipping_lead_days` | int | `ship_date − order_date` in calendar days; negative values (data errors) set to null | `etl_pipeline.py` / `02_cleaning.ipynb` |

---

## KPI layer (computed in `05_final_load_prep.ipynb`)

| KPI | Formula | Grain | Business meaning |
|---|---|---|---|
| **Line Revenue** | `retail_price × order_quantity` | per transaction | Total selling value of each order line — primary revenue metric |
| **Profit Margin %** | `(retail_price − cost_price) / retail_price × 100` | per transaction / category / segment | Profitability per unit sold — key for category and segment prioritisation |
| **Average Order Value (AOV)** | `Σ(order_total) / count(orders)` | month / segment | Basket size health — tracks pricing and upsell effectiveness |
| **Shipping Cost %** | `shipping_cost / order_total × 100` | ship mode / state | Logistics efficiency — high % signals margin erosion from shipping |
| **Top-20% Revenue Concentration** | `revenue from top 20% customers / total revenue` | overall / year | Pareto test — measures dependence risk on a small customer base |
| **Seasonal Revenue Index** | Quarter-over-quarter `Σ(line_revenue)` normalised to annual mean | quarter / year | Identifies peak seasons for inventory and promotional planning |

---

## Data cleaning decisions (must be disclosed in final report)

1. **4 rows dropped where `cost_price > retail_price`** — these are business-logic violations (selling below cost) likely caused by data entry errors. They represent 0.08% of the dataset and are excluded from all analysis.
2. **1 row dropped for missing `order_quantity`** — cannot impute a transaction quantity without introducing arbitrary revenue figures.
3. **`order_priority` null → `Not Specified`** — missing priority is a valid state (the order had no priority assigned), not a data error. Kept in dataset with explicit label.
4. **`shipping_cost` null → median imputed** — no nulls found in this dataset; logic retained as a pipeline safeguard for future data.
5. **Discount null → 0** — no discount is the correct interpretation when the field is absent.
6. **Negative `shipping_lead_days` → null** — ship date earlier than order date is a data entry error and cannot be imputed reliably.
7. **Currency and percentage strings** — all `$`/`,` stripped from price columns; `%` stripped from `discount_pct`. This is documented as a structural raw-data issue, not an imputation.

---


