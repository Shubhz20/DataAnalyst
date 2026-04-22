# Team Roles & Ownership Map

Every member owns one primary area and reviews a secondary area. The secondary review is what guarantees every member has **visible PR activity** — the audit the faculty explicitly warns about. Nobody should be merging their own PRs.

## 5-Member Split

| # | Role | Primary Owns | Reviews (Secondary) | Notebooks / Files |
|---|---|---|---|---|
| 1 | **Tech Lead / ETL Owner** | Repo setup, raw data commit, cleaning pipeline, reproducibility | Viz lead's commits (sanity-check CSVs used by Tableau) | `01_extraction.ipynb`, `02_cleaning.ipynb`, `scripts/etl_pipeline.py`, `.gitignore`, `requirements.txt` |
| 2 | **Analytics Lead** | EDA, statistical methods, interpretation | KPI owner's metric definitions | `03_eda.ipynb`, `04_statistical_analysis.ipynb` |
| 3 | **KPI & Final Load Owner** | KPI framework, Tableau-ready flat file | ETL owner's cleaning output schema | `05_final_load_prep.ipynb`, KPI section of `data_dictionary.md` |
| 4 | **Viz & Storytelling Lead** | Tableau workbook, dashboard design, screenshots, public URL | Analytics lead's chart choices | `tableau/`, `tableau/dashboard_links.md`, `tableau/screenshots/` |
| 5 | **Business & Report Lead** | Problem framing, business context, recommendations, final report PDF, presentation deck | Everyone's narrative language (insights vs chart descriptions) | `docs/gate1_proposal.md`, `reports/project_report.pdf`, `reports/presentation.pdf`, README.md |

## Why this split works for the rubric

| Rubric area | Marks | Primary owner | Why |
|---|---|---|---|
| Problem Framing | 10 | Business & Report Lead | Owns the framing document and refines it with the team |
| Data Quality & ETL | 15 | Tech Lead | Owns notebooks 01–02 and the reusable script |
| Analysis Depth | 25 | Analytics Lead | Owns 03–04; highest rubric weight, so this role must be the strongest Python/stats person |
| Dashboard & Viz | 20 | Viz Lead | Owns Tableau publication + interactivity |
| Business Recommendations | 20 | Business & Report Lead (collaborates with Analytics Lead) | Recommendations must come from analysis, not intuition |
| Storytelling & Clarity | 10 | Business & Report Lead | Owns report + deck coherence |

## Rules of engagement

1. **Never merge your own PR.** The secondary reviewer on the table above is the minimum — pick anyone else on the team.
2. **One PR per logical change.** Don't batch a week of work into one PR; reviewers can't evaluate that and faculty will see only one PR per member.
3. **Commit messages use prefixes:** `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
4. **Branch naming:** `feat/cleaning-pipeline`, `docs/data-dictionary`, etc.
5. **Everyone commits to the final report.** The report lead owns structure and cohesion, but the analysis/KPI/viz leads write their own sections as PRs against `reports/`. This also ensures PR diversity per member.
6. **Daily standup on GitHub Issues.** Use issue comments to check off daily tasks — creates a visible audit trail.

## Contribution matrix snapshot

The final report includes a contribution matrix that must match GitHub Insights. Template in `docs/contribution_matrix.md`.
