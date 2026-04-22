# Gate 1 Proposal — Go/No-Go Submission

**Course:** Data Visualization & Analytics — Capstone 2
**Institute:** ADYPU
**Section:** *[fill in]*
**Team ID:** *[fill in]*
**Team Members:** *[list 5 members with roll numbers]*
**Submission date:** *[fill in]*

---

## 1. Sector

**Retail / E-commerce** — specifically, a mid-market online retailer selling giftware, homeware, and seasonal products primarily to UK consumers with a minor cross-border presence.

## 2. Business Context

Online retail businesses in this category (non-grocery, non-fashion-first, small-basket giftware) face three structural pressures:

1. **Revenue concentration risk** — a small fraction of repeat customers typically generates the majority of revenue. Losing this base is far costlier than losing casual guests.
2. **Rising acquisition costs** — paid channels (Google, Meta) have grown more expensive year-over-year, making retention of existing customers the cheaper growth lever.
3. **Seasonal volatility** — Q4 (Oct–Dec) drives a disproportionate share of annual revenue in giftware categories, concentrating operational and inventory risk.

These pressures make it critical for retailers to know precisely *which* customers drive the business, *which* products they buy, and *where* the budget for retention and promotion should be spent.

## 3. Problem Statement

> For a mid-market UK online retailer operating across ~40 countries between Dec 2009 and Dec 2011, identify **(a)** the customer segments and product categories that drive the top 20% of net revenue, **(b)** the magnitude and drivers of churn in the repeat-purchase base, and **(c)** a prioritized reallocation of retention and promotional budget that protects the revenue-concentration base while recovering at-risk customers.

### Sub-questions (the analysis will answer each explicitly)

1. What share of total net revenue comes from the top 20% of customers? (Pareto test)
2. Do registered customers have materially different average order values than guest checkouts? (Two-sample t-test)
3. Which product-category hints drive the highest return rates, and is the difference across categories statistically significant? (Chi-square / ANOVA)
4. Is there a statistically significant month-of-year effect on revenue after controlling for customer count? (Linear regression with month dummies)
5. Which RFM segments show the steepest churn (Recency decay) over the 24-month window, and how much revenue is at risk from them?
6. Among registered customers, what is the relationship between first-order basket size and 12-month lifetime value? (Correlation + simple linear regression)

## 4. Dataset — Primary

| Field | Value |
|---|---|
| Name | Online Retail II |
| Source | UCI Machine Learning Repository (approved source per guidelines) |
| URL | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| Row count | ~1,067,000 line-item rows |
| Column count | 8 raw analytical columns |
| Time range | 01-Dec-2009 to 09-Dec-2011 |
| Format | Excel `.xlsx`, two sheets |
| Raw data quality issues | ~25% missing `Customer ID`; negative `Quantity` and `Price` values for returns/adjustments; inconsistent country names (`EIRE` vs `Ireland`); non-product stock codes (`POST`, `M`, `D`); duplicate product descriptions across codes |

✔ Meets the ≥5,000 rows rule (exceeds by 200×)
✔ Meets the ≥8 meaningful columns rule (exactly 8 raw columns; cleaning adds 8 more)
✔ Meets the "raw, not pre-cleaned" rule (UCI original; no feature engineering applied)
✔ Contains the realistic issues the spec requires (missing values, mixed formats, category inconsistency)

## 5. Backup Datasets (same sector — ready if primary is rejected)

**Backup 1: Brazilian E-Commerce by Olist** (Kaggle)
- URL: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- 9 raw CSV tables: orders, customers, products, sellers, order items, reviews, payments, geolocation, category translations
- ~100,000 orders from 2016–2018
- Raw multi-table joins = strong ETL story; missing values in reviews; inconsistent seller geolocation
- Slightly different problem framing: *seller performance + logistics* rather than customer retention

**Backup 2: Retailrocket Ecommerce Events Dataset** (Kaggle)
- URL: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset
- ~2.7M events (view, add-to-cart, transaction) + item properties + category tree
- Raw transactional event log — clear clickstream
- Problem framing would pivot to: *funnel conversion + cart abandonment drivers*

Both backups satisfy the row/column/raw criteria independently.

## 6. Initial Data Dictionary

See [`data_dictionary.md`](data_dictionary.md) in the same folder. Covers all 8 raw columns, known data-quality issues per column, 8 engineered columns added during cleaning, and the 6-KPI framework.

## 7. KPI Framework (preview)

- **Net Revenue** (after returns) — primary P&L metric
- **Return Rate** — product quality signal
- **Repeat Purchase Rate** — retention health
- **Average Order Value** — pricing/basket signal
- **RFM Score** — customer-level segmentation
- **Top-20% Revenue Concentration** — dependence risk

Full formulas in the data dictionary.

## 8. Tech Stack & Repo

- Python 3.10 / pandas / scipy / statsmodels / scikit-learn
- Jupyter Notebooks (also runnable on Google Colab)
- Tableau Public for dashboard
- Public GitHub repo with PR-based workflow — folder structure follows the capstone spec exactly

Repo link: *[fill in after GitHub repo is created]*

## 9. Team & Roles

See `roles.md` in the `docs/` folder. Five ownership areas — ETL, Analysis, KPI/Final-load, Viz/Storytelling, Report/Business — each with a primary owner and a secondary reviewer so every member has visible PR activity.

## 10. Timeline Commitment

We commit to the 10-day execution schedule in the guidelines:
- Days 1–2: team setup, repo, dataset sourcing (complete at Gate 1)
- Day 3: Gate 1 submission (this document)
- Days 4–5: raw data committed, cleaning pipeline built
- Days 6–7: EDA + statistical analysis
- Days 8–9: Tableau dashboard published
- Day 10: final report + deck + audit
