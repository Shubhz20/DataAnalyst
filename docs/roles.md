# Team Roles & Ownership Map

Every member owns one primary area and reviews a secondary area. The secondary review guarantees every member has **visible PR activity** — the audit the faculty explicitly warns about. Nobody should be merging their own PRs.

## 5-Member Split

| # | Name | Role | Primary Owns | Reviews (Secondary) | Notebooks / Files |
|---|---|---|---|---|---|
| 1 | **Harshit Aggarwal** | Team Lead & Data Extraction | Repo setup, raw data commit, extraction pipeline, reproducibility, team coordination | Shibaditya's ETL output schema and statistical notebook | `01_extraction.ipynb`, `.gitignore`, `requirements.txt`, raw data commit |
| 2 | **Shibaditya Deb** | Statistical Analysis & ETL Engineer | Cleaning pipeline, ETL script, statistical methods, interpretation | Harshit's extraction notebook for schema consistency | `02_cleaning.ipynb`, `04_statistical_analysis.ipynb`, `scripts/etl_pipeline.py` |
| 3 | **Arohi Jadhav** | EDA, Data Cleaning & Tableau | Exploratory analysis, cleaning validation, Tableau workbook and dashboard design | Jay's Tableau output for chart accuracy | `03_eda.ipynb`, `02_cleaning.ipynb` (cleaning section), `tableau/`, `tableau/screenshots/` |
| 4 | **Jeet Srivastav** | Documentation & Reports | Final report PDF, presentation deck, all docs, data dictionary maintenance | Shibaditya's statistical narrative for business clarity | `docs/gate1_proposal.md`, `docs/data_dictionary.md`, `docs/roles.md`, `docs/contribution_matrix.md`, `reports/project_report.pdf`, `reports/presentation.pdf` |
| 5 | **Jay Patil** | Tableau & Final Load | Tableau public dashboard, dashboard links, KPI-ready flat file prep | Arohi's EDA charts for dashboard relevance | `05_final_load_prep.ipynb`, `tableau/dashboard_links.md`, `tableau/screenshots/` |

## Why this split works for the rubric

| Rubric area | Marks | Primary owner | Why |
|---|---|---|---|
| Problem Framing | 10 | Jeet Srivastav | Owns the framing document and refines it with the team |
| Data Quality & ETL | 15 | Harshit Aggarwal + Shibaditya Deb | Harshit owns extraction; Shibaditya owns cleaning and the reusable ETL script |
| Analysis Depth | 25 | Shibaditya Deb + Arohi Jadhav | Shibaditya owns statistical analysis (04); Arohi owns EDA (03); highest rubric weight |
| Dashboard & Viz | 20 | Jay Patil + Arohi Jadhav | Jay owns Tableau publication and interactivity; Arohi owns chart design in EDA |
| Business Recommendations | 20 | Jeet Srivastav (with Shibaditya Deb) | Recommendations must come from analysis, not intuition |
| Storytelling & Clarity | 10 | Jeet Srivastav | Owns report and deck coherence |

## Rules of engagement

1. **Never merge your own PR.** The secondary reviewer on the table above is the minimum — pick anyone else on the team.
2. **One PR per logical change.** Do not batch a week of work into one PR; reviewers cannot evaluate that and faculty will see only one PR per member.
3. **Commit messages use prefixes:** `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
4. **Branch naming:** `feat/cleaning-pipeline`, `docs/data-dictionary`, etc.
5. **Everyone commits to the final report.** Jeet owns structure and cohesion, but the analysis, KPI, and viz leads write their own sections as PRs against `reports/`. This also ensures PR diversity per member.
6. **Daily standup on GitHub Issues.** Use issue comments to check off daily tasks — creates a visible audit trail.

## Contribution matrix snapshot

The final report includes a contribution matrix that must match GitHub Insights. See `docs/contribution_matrix.md`.
