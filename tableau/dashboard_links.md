# Tableau Public — Dashboard Links

> This file will hold the live public URL(s) for the dashboard. Faculty and reviewers access the dashboard through these links.

## Primary Dashboard

- **Title:** Online Retail II — Revenue, Segments & Retention
- **Public URL:** *[paste after publishing to Tableau Public]*
- **Published by:** *[Tableau Public username]*
- **Last updated:** *[YYYY-MM-DD]*

## Structure

The dashboard has four connected views:

1. **Revenue Overview** — Net revenue by month, country, top-20% concentration
2. **Customer Segments** — RFM segments, segment-level revenue + AOV
3. **Product Performance** — Top/bottom SKUs, return-rate by category hint
4. **Retention Health** — Repeat-purchase rate, cohort retention heatmap

## Filters (interactive — required by rubric)

- Country (multi-select)
- Date range (InvoiceDate)
- RFM segment (single-select)
- Registered vs Guest checkout

## Data Source

Source CSV: `data/processed/tableau_final_load.csv` (produced by `notebooks/05_final_load_prep.ipynb`).
Never hard-code numbers in the workbook — all values must come from the connected data source.

## Screenshots

See `tableau/screenshots/` for PNG exports of each view. Naming convention: `01_overview.png`, `02_segments.png`, `03_products.png`, `04_retention.png`.
