# Tableau Dashboard — Design Specification

> This is the **design brief** the Viz Lead works against. It defines the dashboard structure, chart-by-chart, before any Tableau work starts. The rubric awards dashboards that are *decision-relevant*, not decorative, so every chart below exists to answer a specific question.

**Data source:** `data/processed/tableau_final_load.csv` (produced by `notebooks/05_final_load_prep.ipynb`).
**Target:** One published Tableau Public workbook with four connected dashboards + one story.
**Interactivity requirement:** At least one global filter (rubric mandatory), no hard-coded numbers anywhere.

---

## 1. Design principles (non-negotiable)

1. **Every view answers one business question.** Title the view as the question, not the chart type.
2. **No chart without a written takeaway.** Tableau captions are used for 1-line insights, not axis labels.
3. **One filter shelf for all dashboards.** Global filters (country, date range, segment) apply across all four views via dashboard-to-dashboard filter actions.
4. **Color discipline.** Two primary colors (brand + alert) plus neutral gray. Don't let each chart invent its own palette.
5. **Mobile afterthought.** Optimize for 1366×768 laptops — the rubric audit is done on a laptop, not a phone.

### Color palette (commit to this exactly)

| Role | Hex | Usage |
|---|---|---|
| Primary (brand) | `#1F4E79` (deep blue) | Main revenue bars, headline KPI fills |
| Secondary (growth) | `#2E8540` (forest green) | Positive deltas, retained customers |
| Alert (risk) | `#B33A3A` (muted red) | Negative deltas, at-risk segments, return-rate bars |
| Neutral | `#737373` (warm gray) | Non-selected categories, reference lines |
| Background | `#FAFAFA` (off-white) | Dashboard background |

### Typography
- Titles: Tableau default bold, 16pt
- Chart titles: 12pt semibold
- Axis/legend: 9pt regular

---

## 2. Dashboard structure — 4 connected views + 1 story

### View 1 — Revenue Overview ("Where did the money come from?")

**Purpose:** Open with macro context. Shows total revenue, monthly shape, geographic distribution, and the top-20% concentration — setting up every deeper dashboard.

| Layout position | Chart | Fields | Mark type |
|---|---|---|---|
| Top band (full width) | KPI tiles × 4 | Net Revenue, # Invoices, # Customers, Repeat-Purchase Rate | Text (big number) |
| Middle-left (60%) | Monthly revenue line chart | `invoice_year_month` × SUM(`line_revenue`) | Line + shaded area |
| Middle-right (40%) | Top-10 countries bar chart | `country_clean` × SUM(`line_revenue`) | Horizontal bar (sorted desc) |
| Bottom (full width) | Top-20% concentration gauge/Pareto | Cumulative % revenue vs cumulative % of customers | Dual-axis: line + bar |

**Filters visible on this dashboard:** Date range, Country, Registered-only toggle.

**Written insights to include (one per chart as caption):**
- Monthly line: seasonal peak identification (Oct–Dec giftware peak)
- Country bar: UK dominance % and implication for international growth
- Pareto gauge: X% of customers drive Y% of revenue → concentration-risk headline

---

### View 2 — Customer Segments ("Who are we actually serving?")

**Purpose:** Break customers into RFM segments, quantify each segment's revenue share and engagement, and highlight at-risk customers.

| Layout position | Chart | Fields | Mark type |
|---|---|---|---|
| Top | RFM segment treemap | `rfm_segment` sized by SUM(`monetary`), colored by count | Treemap |
| Middle-left | Segment KPI table | `rfm_segment` × [customers, avg recency, avg frequency, total revenue] | Text table |
| Middle-right | Recency vs Frequency scatter | `recency_days` × `frequency`, sized by `monetary`, colored by `rfm_segment` | Scatter |
| Bottom | Segment trend over time | `invoice_year_month` × SUM(`line_revenue`) split by `rfm_segment` | Stacked area |

**Filters:** Segment multi-select, Country, Top-20% customers only toggle.

**Insights to include:**
- Treemap: which 2 segments contribute most revenue
- Scatter: where the "At Risk" cluster sits — long recency, high historical monetary = priority win-back targets
- Stacked area: whether "Champions" share is growing, flat, or shrinking

---

### View 3 — Product Performance ("Which products work — and which hurt us?")

**Purpose:** Drill into products and category hints. Two sides: winners (revenue/velocity) and losers (high return rate, thin margin).

| Layout position | Chart | Fields | Mark type |
|---|---|---|---|
| Top-left | Top-20 products by revenue | `description` × SUM(`line_revenue`) | Horizontal bar |
| Top-right | Top-10 products by return rate (min 50 units sold) | `description` × `return_rate` | Horizontal bar, colored alert-red |
| Middle | Category-hint revenue vs return-rate scatter | `product_category_hint`: SUM(`line_revenue`) × return-rate, sized by volume | Scatter with quadrant labels |
| Bottom | Monthly category mix | `invoice_year_month` × `product_category_hint` SUM(`line_revenue`) | 100% stacked area |

**Filters:** Category hint multi-select, Country, Date range.

**Insights:**
- Top revenue bar: is there a long tail or a hero-product dependence?
- Return-rate bar: specific SKUs that need supplier conversation
- Quadrant scatter: "high-volume / high-return" = urgent fix vs "high-volume / low-return" = protect

---

### View 4 — Retention Health ("Are we keeping the customers we win?")

**Purpose:** The rubric rewards statistical depth. This view surfaces retention analytics — cohort heatmap, repeat-purchase rate trend, and first-order-size → LTV relationship.

| Layout position | Chart | Fields | Mark type |
|---|---|---|---|
| Top-left | Cohort retention heatmap | `cohort_month` × `cohort_index`, color by % retained | Heatmap |
| Top-right | Monthly repeat-purchase rate | `invoice_year_month` × RPR | Line |
| Bottom-left | First-order revenue vs 12-month LTV scatter | `first_order_rev` × `ltv_12m`, trend line | Scatter + trend |
| Bottom-right | Segment-level churn funnel | RFM segments: customers → active this quarter → dormant | Funnel |

**Filters:** Cohort month range, Registered-only (always true here).

**Insights:**
- Cohort heatmap: which cohort months onboarded stickier customers (acquisition-channel hypothesis)
- LTV scatter: r value + what that means for first-order incentive budget
- Funnel: quantified at-risk base to target in Q-next retention push

---

### Story — "From Data to Decision" (6 slides, published with dashboards)

A Tableau Story that walks the reader through the narrative the reviewer will see first. Each slide pins one of the dashboards above, filtered to tell the one key point.

1. **The business** — UK online retailer, £X annual revenue, 40 countries
2. **The headline risk** — top 20% of customers drive Y% of revenue (concentration)
3. **The segments** — who the Champions are vs At-Risk; their £ value
4. **The product angle** — one hero category, one problem category
5. **The retention gap** — cohort retention curve shape
6. **The recommendation** — 3 specific actions tied to the analysis

This story is what's embedded in the PPT presentation.

---

## 3. Filters + parameters

**Global filters (applied to all 4 dashboards via "Apply to worksheets"):**
- Country (multi-select)
- Date range (`invoicedate`)
- RFM segment (multi-select)
- Registered-only toggle

**Parameters (user-controlled knobs):**
- "Top N products" — integer, default 20, used in Product view
- "Cohort retention threshold %" — used to color heatmap

**Filter actions:**
- View 1 Top-10 countries bar → clicking a country filters all other views to that country
- View 2 RFM treemap → clicking a segment filters Views 3 and 4 to that segment's customers

---

## 4. KPIs — exact calculated fields in Tableau

All KPIs are pre-computed in `05_final_load_prep.ipynb`; Tableau-side calculations stay thin. But some aggregates are expressed as Tableau calculated fields for filter reactivity:

```
Net Revenue =
  SUM([line_revenue]) - ABS(SUM(IIF([is_return], [line_revenue], 0)))

Repeat Purchase Rate =
  COUNTD(IF [frequency] >= 2 THEN [customer_id] END) / COUNTD([customer_id])

Return Rate =
  SUM(IIF([is_return], 1, 0)) / COUNT([invoice])

Top 20% Revenue Share =
  SUM(IIF([is_top_20pct_customer], [line_revenue], 0)) / SUM([line_revenue])
```

---

## 5. Build order (recommended for Viz Lead)

1. Connect data source, verify all columns from the final-load CSV are present with correct types
2. Build individual worksheets (one per chart above) — don't assemble dashboards yet
3. Verify each worksheet renders correctly with full data
4. Assemble each of the 4 dashboards
5. Add filter actions between dashboards
6. Apply color palette and typography consistently
7. Build the Story
8. Publish to Tableau Public, copy the URL, paste into `tableau/dashboard_links.md`
9. Export each dashboard as PNG (File → Export → Image), commit to `tableau/screenshots/` with naming: `01_overview.png`, `02_segments.png`, `03_products.png`, `04_retention.png`, `story.png`

---

## 6. Acceptance criteria (self-check before publishing)

- [ ] All 4 dashboards load without "null" or error tiles
- [ ] Global filters update every chart on every dashboard
- [ ] Filter actions between dashboards work (click a country → others filter)
- [ ] Every chart has a written caption (the insight)
- [ ] No hard-coded numbers anywhere (search all title/subtitle text)
- [ ] Color palette applied consistently (use the 4 hex values above only)
- [ ] Story has exactly 6 slides with dashboards pinned
- [ ] Published URL works when opened in incognito window (i.e., truly public)
- [ ] Screenshots at 1366×768 resolution (rubric audit resolution)
- [ ] `tableau/dashboard_links.md` has the final URL
