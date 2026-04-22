# SectionX_TeamY_OnlineRetailInsights

> **TODO — rename this folder, the repo, and this heading.** Use the convention `SectionName_TeamID_ProjectName`. Example: `B_Team04_RetailPulse`. You also need to pick a real `ProjectName` your team agrees on — "OnlineRetailInsights" is a placeholder.

Capstone 2 analytics project for the Data Visualization & Analytics course at ADYPU. We analyze a UK online retailer's transactional data (Dec 2009 – Dec 2011) to identify revenue-driving customer segments, at-risk repeat buyers, and product-level profitability — ultimately recommending where the retailer should reallocate retention and promotional spend.

## Problem Statement

For a mid-market UK e-commerce retailer operating across ~40 countries, identify **(a)** the customer segments and product categories that drive the top 20% of revenue, **(b)** the magnitude and drivers of churn in the repeat-purchase base, and **(c)** a prioritized reallocation of retention and promotional budget that protects the revenue-concentration base while recovering at-risk customers.

Full problem framing, business context, and sub-questions: see [`docs/gate1_proposal.md`](docs/gate1_proposal.md).

## Sector

Retail / E-commerce.

## Dataset

| | Source | Rows | Columns | Link |
|---|---|---|---|---|
| **Primary** | Online Retail II (UCI ML Repository) | ~1,067,000 | 8 | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| **Backup 1** | Brazilian E-Commerce by Olist (Kaggle) | ~100,000 orders across 9 raw tables | 50+ (joined) | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| **Backup 2** | Retailrocket recommender system dataset (Kaggle) | ~2.7M events | 8 (raw) | https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset |

Column-level definitions: see [`docs/data_dictionary.md`](docs/data_dictionary.md).

## Repository Structure

```
SectionX_TeamY_OnlineRetailInsights/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/              ← Original dataset (never edited after commit)
│   └── processed/        ← Cleaned output from pipeline
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── scripts/
│   └── etl_pipeline.py   ← Parameterized version of notebook logic
├── tableau/
│   ├── screenshots/
│   └── dashboard_links.md
├── reports/
│   ├── project_report.pdf
│   └── presentation.pdf
└── docs/
    ├── data_dictionary.md
    ├── gate1_proposal.md
    ├── roles.md
    └── contribution_matrix.md
```

## Tech Stack

- **Language:** Python 3.10+
- **Core libs:** pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn
- **Notebooks:** Jupyter (or Google Colab; commit `.ipynb` either way)
- **Visualization:** Tableau Public
- **Version control:** GitHub — PR-based workflow, every member commits

## How to Run

```bash
# 1. Clone
git clone <repo-url>
cd SectionX_TeamY_OnlineRetailInsights

# 2. Set up env
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Place raw dataset
# Download Online Retail II from UCI, save to data/raw/online_retail_II.xlsx

# 4. Run notebooks in order
jupyter notebook notebooks/
# Execute 01 → 02 → 03 → 04 → 05

# 5. Outputs
# - Cleaned CSV: data/processed/online_retail_II_clean.csv
# - Tableau-ready flat file: data/processed/tableau_final_load.csv
```

## Dashboard

Live Tableau Public link: see [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

## Team & Roles

See [`docs/roles.md`](docs/roles.md) for the 5-member role split and ownership map.

## Contribution Matrix

See [`docs/contribution_matrix.md`](docs/contribution_matrix.md). This must match GitHub Insights at submission time — faculty audits commit + PR history per member.

## Git Workflow (mandatory)

1. `main` is protected — no direct pushes
2. Every change goes through a **feature branch** and a **pull request**
3. Branch naming: `feat/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`
4. At least one teammate reviews each PR before merge
5. Commit messages use conventional prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

This ensures every member has visible PR activity — the audit rule the faculty explicitly warns about.

## License

MIT — see `LICENSE`.
