# Gate 1 Proposal — Go/No-Go Submission

**Course:** Data Visualization & Analytics — Capstone 2
**Institute:** ADYPU
**Team Members:**
- Harshit Aggarwal — Team Lead & Data Extraction
- Shibaditya Deb — Statistical Analysis & ETL Engineer
- Arohi Jadhav — EDA, Data Cleaning & Tableau
- Jeet Srivastav — Documentation & Reports
- Jay Patil — Tableau & Final Load

**Submission date:** 2026-04-28

---

## 1. Sector

**Retail / E-commerce** — specifically, a multi-category retailer operating across Australian states, selling Office Supplies, Furniture, and Technology products to Consumer, Corporate, Small Business, and Home Office customer segments.

## 2. Business Context

Mid-market retail businesses across product categories face three structural pressures:

1. **Revenue concentration risk** — a small fraction of customers and product categories typically generates the majority of revenue. Identifying and protecting this base is more cost-effective than broad acquisition.
2. **Margin pressure by segment** — different customer types (Corporate vs Consumer vs Small Business) negotiate different terms. Understanding which segments are most profitable per order is essential for sales strategy.
3. **Logistics cost inefficiency** — shipping mode, order priority, and geography all interact to drive shipping cost as a percentage of order value, creating a hidden margin drain that most retailers underestimate.

These pressures make it critical to know precisely *which* customers, *which* product categories, and *which* geographic clusters drive profitability — and where to reallocate retention and promotional spend.

## 3. Problem Statement

> For a multi-state Australian retailer operating across Consumer, Corporate, Small Business, and Home Office segments between 2013 and 2017, identify **(a)** the customer segments and product categories that drive the top 20% of revenue, **(b)** the magnitude and drivers of profit margin variation across segments and shipping modes, and **(c)** a prioritized reallocation of retention and promotional budget that protects the high-margin base while recovering at-risk customer segments.

### Sub-questions (the analysis will answer each explicitly)

1. What share of total revenue comes from the top 20% of customers by order total? (Pareto test)
2. Do Corporate customers have materially higher Average Order Values than Consumer or Small Business customers? (One-way ANOVA / two-sample t-test)
3. Which product category drives the highest profit margin percentage, and is the difference statistically significant across categories? (ANOVA)
4. Is there a statistically significant seasonal (month/quarter) effect on revenue after controlling for customer type? (Linear regression with time dummies)
5. Which shipping mode has the highest shipping cost as a percentage of order total, and how does this interact with order priority? (Cross-tab + chi-square)
6. Among repeat-order states, what is the relationship between average order quantity and profit margin? (Correlation + simple linear regression)

## 4. Dataset — Primary

| Field | Value |
|---|---|
| Name | Retail Insights: A Comprehensive Sales Dataset |
| Source | Kaggle |
| URL | https://www.kaggle.com/datasets/rajneesh231/retail-insights-a-comprehensive-sales-dataset |
| Row count | 5,000 transactions |
| Column count | 24 raw columns |
| Time range | February 2013 – February 2017 |
| Format | CSV |
| Geography | Australian states (NSW, VIC, QLD, and others) |
| Raw data quality issues | 1 missing `Order Quantity` row; 1 missing `Address`; 4 rows where `Cost Price > Retail Price` (business logic violation); currency values stored as strings with `$` and `,`; discount stored as percentage string (`2%`); dates in non-standard `DD-MM-YYYY` format |

**Columns:** `Order No`, `Order Date`, `Customer Name`, `Address`, `City`, `State`, `Customer Type`, `Account Manager`, `Order Priority`, `Product Name`, `Product Category`, `Product Container`, `Ship Mode`, `Ship Date`, `Cost Price`, `Retail Price`, `Profit Margin`, `Order Quantity`, `Sub Total`, `Discount %`, `Discount $`, `Order Total`, `Shipping Cost`, `Total`

**Product categories:** Furniture, Office Supplies, Technology
**Customer types:** Consumer, Corporate, Home Office, Small Business
**Order priorities:** Critical, High, Medium, Low

✔ Meets the ≥5,000 rows rule (exactly 5,000 raw rows)
✔ Meets the ≥8 meaningful columns rule (24 raw columns; ETL adds 10 engineered columns)
✔ Meets the "raw, not pre-cleaned" rule (currency formatting, string dates, logic violations intact)
✔ Contains the realistic issues the spec requires (missing values, mixed formats, business logic errors)

## 5. Backup Dataset (same sector — ready if primary is rejected)

**Backup: Retail Sales Dataset by Mohammad Talib** (Kaggle)
- URL: https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset
- 1,000 rows, 9 columns: Transaction ID, Date, Customer ID, Gender, Age, Product Category, Quantity, Price per Unit, Total Amount
- Synthetic dataset simulating a retail environment — useful for EDA and demographic analysis
- Smaller but cleaner; primarily useful as a validation or supplementary dataset

## 6. Initial Data Dictionary

See [`data_dictionary.md`](data_dictionary.md) in the same folder. Covers all 24 raw columns, known data-quality issues per column, 10 engineered columns added during ETL, and the KPI framework.

## 7. KPI Framework (preview)

- **Line Revenue** (`Retail Price × Order Quantity`) — primary revenue metric per transaction
- **Profit Margin %** (`(Retail Price − Cost Price) / Retail Price × 100`) — profitability signal
- **Average Order Value** — basket size health per segment
- **Shipping Cost %** (`Shipping Cost / Order Total × 100`) — logistics efficiency signal
- **Top-20% Revenue Concentration** — customer dependence risk (Pareto)
- **Seasonal Revenue Index** — quarter-over-quarter revenue trend

Full formulas in the data dictionary.

## 8. Tech Stack & Repo

- Python 3.10 / pandas / numpy / scipy / statsmodels / scikit-learn / matplotlib / seaborn
- Jupyter Notebooks (also runnable on Google Colab)
- Tableau Public for dashboard
- Public GitHub repo with PR-based workflow — folder structure follows the capstone spec exactly

## 9. Team & Roles

See `roles.md` in the `docs/` folder. Five ownership areas — Team Lead/Extraction, Statistical Analysis/ETL, EDA/Cleaning/Tableau, Docs/Reports, Tableau/Final Load — each with a primary owner and a secondary reviewer so every member has visible PR activity.

## 10. Timeline Commitment

We commit to the 10-day execution schedule in the guidelines:

- Days 1–2: team setup, repo, dataset sourcing (complete at Gate 1)
- Day 3: Gate 1 submission (this document)
- Days 4–5: raw data committed, extraction and cleaning pipeline built (`01_extraction.ipynb`, `02_cleaning.ipynb`, `scripts/etl_pipeline.py`)
- Days 6–7: EDA + statistical analysis (`03_eda.ipynb`, `04_statistical_analysis.ipynb`)
- Days 8–9: Tableau dashboard published, final load prep (`05_final_load_prep.ipynb`)
- Day 10: final report + presentation deck + contribution audit
