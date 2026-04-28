# Unity_TeamJeet_OnlineRetailInsights

> **Newton School of Technology | Data Visualization & Analytics**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

| Field | Details |
|---|---|
| **Project Title** | Online Retail Insights |
| **Sector** | Retail / E-commerce |
| **Team ID** | TeamJeet |
| **Section** | Unity |
| **Faculty Mentor** | _To be filled by team_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _To be filled by team_ |

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Shibaditya | `github-handle` |
| Data Lead | Harshit Agrawal | `github-handle` |
| ETL Lead | Harshit Agrawal | `github-handle` |
| Analysis Lead | Jeet Shrivastav | `github-handle` |
| Visualization Lead | Jay Patil | `github-handle` |
| Strategy Lead | Arohi Jadhav | `github-handle` |
| PPT and Quality Lead | Shibaditya | `github-handle` |

---

## Business Problem
For a mid-market UK e-commerce retailer operating across ~40 countries, the core challenge is to identify revenue-driving customer segments, at-risk repeat buyers, and product-level profitability to ultimately recommend where the retailer should reallocate retention and promotional spend.

**Core Business Question**
> What are the key customer segments and product categories that drive the top 20% of revenue, and what are the drivers of churn in the repeat-purchase base?

**Decision Supported**
> Reallocation of retention and promotional budget that protects the revenue-concentration base while recovering at-risk customers.

---

## Dataset
| Attribute | Details |
|---|---|
| **Source Name** | Retail Sales Dataset (Kaggle) |
| **Direct Access Link** | [Kaggle Dataset](https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset) |
| **Row Count** | 1,000 |
| **Column Count** | 9 |
| **Time Period Covered** | Dec 2009 – Dec 2011 |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| Transaction ID | Unique identifier for each transaction | Unique ID |
| Date | Date the transaction occurred | Time series analysis |
| Customer ID | Unique identifier for each customer | Customer segmentation |
| Gender | Customer gender | Demographic split |
| Age | Customer age | Demographic split |
| Product Category | Category of the purchased product | Product analysis |
| Quantity | Number of items purchased | Volume metrics |
| Price per Unit | Unit price of the product | Value metrics |
| Total Amount | Total transaction value (Quantity × Price per Unit) | Revenue calculation |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework
| KPI | Definition | Formula / Computation |
|---|---|---|
| _To be filled by team_ | _What business outcome this tracks_ | _Show the exact formula or notebook reference_ |

---

## Tableau Dashboard
| Item | Details |
|---|---|
| **Dashboard URL** | _Paste Tableau Public link here_ |
| **Executive View** | _Describe the high-level KPI summary view_ |
| **Operational View** | _Describe the detailed drill-down view_ |
| **Main Filters** | _List the interactive filters used_ |

---

## Key Insights
1. _Insight 1_
2. _Insight 2_
3. _Insight 3_
4. _Insight 4_
5. _Insight 5_
6. _Insight 6_
7. _Insight 7_
8. _Insight 8_

---

## Recommendations
| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 2 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 3 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |

---

## Repository Structure
```text
Unity_TeamJeet_OnlineRetailInsights/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   |-- 04_statistical_analysis.ipynb
|   `-- 05_final_load_prep.ipynb
|
|-- scripts/
|   `-- etl_pipeline.py
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- README.md
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline
The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Tech Stack
| Tool | Purpose |
|---|---|
| Python + Jupyter Notebooks | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Cloud notebook execution environment |
| Tableau Public | Dashboard design, publishing, and sharing |
| GitHub | Version control, collaboration, contribution audit |
| SQL | Initial data extraction only, if documented |

**Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Contribution Matrix
| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| Harshit Agrawal | Owner | Owner | Support | Support | Support | Support | Support |
| Jeet Shrivastav | Support | Support | Owner | Owner | Support | Support | Support |
| Arohi Jadhav | Support | Support | Support | Support | Owner | Support | Support |
| Jay Patil | Support | Support | Support | Support | Owner | Support | Support |
| Shibaditya | Support | Support | Support | Support | Support | Owner | Owner |

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
