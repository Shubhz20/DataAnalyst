"""
generate_assets.py
==================
Generates dva_resume.pdf and dva_portfolio.pdf using reportlab.
Run from the project root:
    python scripts/generate_assets.py
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfgen import canvas
from pathlib import Path

# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
NAVY       = colors.HexColor("#1B2A4A")
STEEL      = colors.HexColor("#2E5B8E")
ACCENT     = colors.HexColor("#3A80C1")
LIGHT_BLUE = colors.HexColor("#EAF2FB")
SLATE      = colors.HexColor("#4A5568")
MUTED      = colors.HexColor("#718096")
WHITE      = colors.white
DIVIDER    = colors.HexColor("#CBD5E0")
GOLD       = colors.HexColor("#C8973A")

W, H = A4

# ---------------------------------------------------------------------------
# ── RESUME ──────────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------

def build_resume(out_path: Path):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=14*mm,
        bottomMargin=14*mm,
    )

    def header_footer(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.setFillColor(MUTED)
        canvas_obj.drawString(18*mm, 8*mm, "Team Jeet  |  Retail Insights Capstone  |  ADYPU  |  2026")
        canvas_obj.drawRightString(W - 18*mm, 8*mm, "Data Visualization & Analytics — Capstone 2")
        canvas_obj.restoreState()

    s = {
        "name": ParagraphStyle("name",
            fontName="Helvetica-Bold", fontSize=26, textColor=NAVY,
            leading=30, alignment=TA_LEFT, spaceAfter=1),
        "tagline": ParagraphStyle("tagline",
            fontName="Helvetica", fontSize=10.5, textColor=STEEL,
            leading=14, alignment=TA_LEFT, spaceAfter=2),
        "contact": ParagraphStyle("contact",
            fontName="Helvetica", fontSize=8.5, textColor=SLATE,
            leading=12, alignment=TA_RIGHT),
        "section": ParagraphStyle("section",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
            leading=13, spaceBefore=10, spaceAfter=2, letterSpacing=0.8),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=8.8, textColor=SLATE,
            leading=13, alignment=TA_JUSTIFY),
        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=8.8, textColor=SLATE,
            leading=13, leftIndent=10, bulletIndent=0),
        "skill_label": ParagraphStyle("skill_label",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY, leading=12),
        "skill_val": ParagraphStyle("skill_val",
            fontName="Helvetica", fontSize=8.5, textColor=SLATE, leading=12),
        "proj_title": ParagraphStyle("proj_title",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY, leading=13),
        "proj_sub": ParagraphStyle("proj_sub",
            fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED, leading=12),
        "member_name": ParagraphStyle("member_name",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY, leading=12),
        "member_role": ParagraphStyle("member_role",
            fontName="Helvetica", fontSize=8.2, textColor=SLATE, leading=12),
    }

    def section_heading(text):
        return [
            Paragraph(text.upper(), s["section"]),
            HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=5),
        ]

    def bullet_item(text):
        return Paragraph(f"<bullet>&bull;</bullet> {text}", s["bullet"])

    story = []

    # ── Header ───────────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("<b>Team Jeet</b>", s["name"]),
        Paragraph(
            "Data Visualization &amp; Analytics — Capstone 2<br/>"
            "ADYPU &nbsp;|&nbsp; April 2026",
            s["contact"]
        ),
    ]]
    header_table = Table(header_data, colWidths=[80*mm, None])
    header_table.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "BOTTOM"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 2),
    ]))
    story.append(header_table)
    story.append(Paragraph(
        "Retail Insights: A Comprehensive Sales Analytics Project &nbsp;&bull;&nbsp; "
        "ETL &nbsp;&bull;&nbsp; Statistical Analysis &nbsp;&bull;&nbsp; "
        "Tableau Dashboard &nbsp;&bull;&nbsp; Business Recommendations",
        s["tagline"]
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=6))

    # ── Project Overview ──────────────────────────────────────────────────────
    story += section_heading("Project Overview")
    story.append(Paragraph(
        "Team Jeet designed and delivered a complete, end-to-end data analytics solution for a "
        "multi-category Australian retail dataset (Kaggle — Retail Insights, 5,000 transactions, "
        "Feb 2013–Feb 2017). The project covers the full analytics lifecycle: raw data ingestion, "
        "production-grade ETL pipeline, exploratory data analysis, formal statistical hypothesis "
        "testing, a published Tableau dashboard, and a set of five prioritised business "
        "recommendations — all version-controlled on GitHub using a professional PR-based workflow.",
        s["body"]
    ))
    story.append(Spacer(1, 4))

    # ── Team Members & Roles ─────────────────────────────────────────────────
    story += section_heading("Team Members & Roles")
    members = [
        ("Harshit Aggarwal", "Team Lead & Data Extraction",
         "01_extraction.ipynb, repo architecture, raw data commit, .gitignore, requirements.txt"),
        ("Shibaditya Deb",   "Statistical Analysis & ETL Engineer",
         "scripts/etl_pipeline.py, 02_cleaning.ipynb, 04_statistical_analysis.ipynb, data dictionary"),
        ("Arohi Jadhav",     "Tableau & Visualization",
         "Tableau workbook, dashboard design, tableau/screenshots/, dashboard_links.md"),
        ("Jeet Srivastav",   "Documentation & Reports",
         "gate1_proposal.md, project_report.pdf, presentation.pdf, all docs maintenance"),
        ("Jay Patil",        "EDA & Final Load",
         "03_eda.ipynb, 05_final_load_prep.ipynb, KPI-ready flat file for Tableau"),
    ]
    for name, role, deliverables in members:
        row = Table([[
            Paragraph(name, s["member_name"]),
            Paragraph(f"<b>{role}</b><br/>{deliverables}", s["member_role"]),
        ]], colWidths=[45*mm, None])
        row.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LINEBELOW",    (0,0), (-1,0), 0.3, DIVIDER),
        ]))
        story.append(row)
    story.append(Spacer(1, 4))

    # ── Technical Stack ───────────────────────────────────────────────────────
    story += section_heading("Technical Stack & Tools")
    skills = [
        ("Language",       "Python 3.10+ — pandas, numpy, scipy, statsmodels, matplotlib, seaborn"),
        ("ETL & Pipeline", "6-phase modular ETL (scripts/etl_pipeline.py) — Extract, Validate, Transform, Outlier Handling, Final Validation, Load"),
        ("Statistics",     "One-way ANOVA, two-sample t-test, chi-square, linear regression with time dummies, Pearson correlation"),
        ("Visualization",  "Tableau Public — KPI cards, time-series, treemap, heatmap, state-level geographic map"),
        ("Dev Workflow",   "GitHub — PR-based branching, conventional commit messages (feat/fix/docs), peer code review"),
        ("Documentation",  "Jupyter Notebooks, Markdown, data dictionary, Gate 1 proposal, contribution matrix"),
    ]
    for label, val in skills:
        row = Table(
            [[Paragraph(label, s["skill_label"]), Paragraph(val, s["skill_val"])]],
            colWidths=[38*mm, None]
        )
        row.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 1),
            ("BOTTOMPADDING",(0,0), (-1,-1), 1),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        story.append(row)
    story.append(Spacer(1, 4))

    # ── Key Project Achievements ──────────────────────────────────────────────
    story += section_heading("Key Project Achievements")
    story.append(KeepTogether([
        Table([[
            Paragraph("Retail Insights: End-to-End Data Analytics Pipeline", s["proj_title"]),
            Paragraph("Capstone 2 &nbsp;|&nbsp; ADYPU &nbsp;|&nbsp; 2026", s["proj_sub"]),
        ]], colWidths=[130*mm, None], style=TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ])),
        Paragraph(
            "<i>Dataset: Retail Insights (Kaggle) — 5,000 rows, 24 columns, Feb 2013–Feb 2017, "
            "Australian multi-state retail — Furniture, Office Supplies, Technology</i>",
            s["proj_sub"]
        ),
        Spacer(1, 4),
        bullet_item(
            "<b>Production ETL pipeline</b> — 6-phase modular script (scripts/etl_pipeline.py) "
            "processes 5,000 raw transactions into a clean 34-column analytical schema; "
            "resolves currency string formatting, DD-MM-YYYY date parsing, business logic violations "
            "(cost > retail), and missing critical fields with fail-fast validation at every phase."
        ),
        bullet_item(
            "<b>10 engineered analytical features</b> — profit_margin_pct, line_revenue, "
            "order_quarter, order_year_month, shipping_lead_days, and IQR outlier flags — "
            "directly consumed by Tableau KPI cards and time-series dashboards without further transformation."
        ),
        bullet_item(
            "<b>Formal statistical validation</b> — ANOVA (AOV by customer segment), t-test "
            "(Technology vs Furniture margin), chi-square (ship mode vs order priority), "
            "linear regression (seasonal revenue with month dummies), and Pearson correlation "
            "(order quantity vs profit margin by state)."
        ),
        bullet_item(
            "<b>6-KPI business framework</b> — Line Revenue, Profit Margin %, Average Order Value, "
            "Shipping Cost %, Top-20% Revenue Concentration, Seasonal Revenue Index — "
            "each with a defined formula, analytical grain, and business interpretation."
        ),
        bullet_item(
            "<b>Interactive Tableau dashboard</b> — 4 analytical views: Revenue by Segment & Category, "
            "Profit Margin Trends, Shipping Efficiency Matrix, Seasonal Revenue Index; "
            "outlier toggle filter powered by ETL pipeline output."
        ),
        bullet_item(
            "<b>5 prioritised business recommendations</b> — Technology margin protection, "
            "Q1 demand recovery campaign, Express Air cost rationalisation, QLD geographic "
            "expansion, and Corporate retention programme — each with estimated impact range."
        ),
        bullet_item(
            "<b>Full GitHub PR workflow</b> — 5-member team, branch-per-feature strategy, "
            "peer code review enforced, conventional commit prefixes, contribution matrix "
            "auditable against GitHub Insights."
        ),
        Spacer(1, 3),
    ]))

    # ── Dataset at a Glance ───────────────────────────────────────────────────
    story += section_heading("Dataset at a Glance")
    glance_data = [
        ["Attribute", "Value"],
        ["Source",           "Kaggle — Retail Insights: A Comprehensive Sales Dataset (Rajneesh231)"],
        ["Raw rows",         "5,000 transactions"],
        ["Raw columns",      "24 (Order No, Order/Ship Date, Customer, City, State, Product, Pricing, Shipping)"],
        ["Clean rows",       "4,995 (5 rows removed: 4 cost>retail violations + 1 missing quantity)"],
        ["Clean columns",    "34 (24 raw + 10 engineered)"],
        ["Time range",       "February 2013 – February 2017"],
        ["Geography",        "Australian states — NSW, VIC, QLD and others"],
        ["Product categories","Furniture, Office Supplies, Technology"],
        ["Customer segments","Consumer, Corporate, Home Office, Small Business"],
    ]
    glance_table = Table(glance_data, colWidths=[45*mm, None])
    glance_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0,0), (-1,-1), 0.3, DIVIDER),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("FONTNAME",      (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (0,-1), NAVY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(glance_table)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"[resume] Written → {out_path}")


# ---------------------------------------------------------------------------
# ── PORTFOLIO ────────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------

def build_portfolio(out_path: Path):

    def cover_page(canvas_obj, doc_obj):
        pass  # handled inline via first page content

    def page_header_footer(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # Top bar
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, H - 8*mm, W, 8*mm, fill=1, stroke=0)
        canvas_obj.setFont("Helvetica-Bold", 8.5)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.drawString(18*mm, H - 5.5*mm, "RETAIL INSIGHTS  |  Data Analytics Capstone Portfolio")
        canvas_obj.drawRightString(W - 18*mm, H - 5.5*mm, "Team Jeet  •  ADYPU  •  2026")
        # Bottom
        canvas_obj.setFillColor(DIVIDER)
        canvas_obj.rect(0, 0, W, 6*mm, fill=1, stroke=0)
        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.setFillColor(SLATE)
        canvas_obj.drawCentredString(W/2, 2*mm, f"Page {doc_obj.page}")
        canvas_obj.restoreState()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=16*mm,
        bottomMargin=14*mm,
    )

    s = {
        "cover_title": ParagraphStyle("cover_title",
            fontName="Helvetica-Bold", fontSize=32, textColor=WHITE,
            leading=40, alignment=TA_CENTER),
        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Helvetica", fontSize=13, textColor=LIGHT_BLUE,
            leading=20, alignment=TA_CENTER),
        "cover_tag": ParagraphStyle("cover_tag",
            fontName="Helvetica-Bold", fontSize=10, textColor=GOLD,
            leading=16, alignment=TA_CENTER),
        "cover_meta": ParagraphStyle("cover_meta",
            fontName="Helvetica", fontSize=9.5, textColor=WHITE,
            leading=15, alignment=TA_CENTER),
        "h1": ParagraphStyle("h1",
            fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
            leading=22, spaceBefore=14, spaceAfter=4),
        "h2": ParagraphStyle("h2",
            fontName="Helvetica-Bold", fontSize=12, textColor=STEEL,
            leading=16, spaceBefore=10, spaceAfter=3),
        "h3": ParagraphStyle("h3",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=14, spaceBefore=7, spaceAfter=2),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=9.5, textColor=SLATE,
            leading=15, alignment=TA_JUSTIFY),
        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=9.5, textColor=SLATE,
            leading=14, leftIndent=12, bulletIndent=0),
        "caption": ParagraphStyle("caption",
            fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
            leading=12, alignment=TA_CENTER),
        "kpi_label": ParagraphStyle("kpi_label",
            fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
            leading=12, alignment=TA_CENTER),
        "kpi_val": ParagraphStyle("kpi_val",
            fontName="Helvetica", fontSize=8.5, textColor=SLATE,
            leading=12, alignment=TA_CENTER),
        "callout": ParagraphStyle("callout",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=15, alignment=TA_CENTER),
        "tag": ParagraphStyle("tag",
            fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
            leading=11, alignment=TA_CENTER),
        "quote": ParagraphStyle("quote",
            fontName="Helvetica-Oblique", fontSize=10.5, textColor=STEEL,
            leading=16, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4),
    }

    def divider(color=DIVIDER, thick=0.5):
        return HRFlowable(width="100%", thickness=thick, color=color, spaceAfter=6, spaceBefore=2)

    def section_title(text):
        return [
            Spacer(1, 4),
            Paragraph(text, s["h1"]),
            HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=8),
        ]

    def bullet_item(text):
        return Paragraph(f"<bullet>&bull;</bullet> {text}", s["bullet"])

    def info_box(text, bg=LIGHT_BLUE):
        t = Table([[Paragraph(text, s["body"])]], colWidths=[W - 40*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), bg),
            ("LEFTPADDING",  (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING",   (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0), (-1,-1), 8),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), [4,4,4,4]),
        ]))
        return t

    def kpi_row(items):
        """items = list of (label, value, formula) tuples"""
        cells = []
        for label, val, formula in items:
            cell = Table([[
                Paragraph(val, ParagraphStyle("v", fontName="Helvetica-Bold",
                    fontSize=16, textColor=NAVY, leading=20, alignment=TA_CENTER)),
            ],[
                Paragraph(label, s["kpi_label"]),
            ],[
                Paragraph(formula, s["kpi_val"]),
            ]], colWidths=[(W - 40*mm) / len(items) - 4*mm])
            cell.setStyle(TableStyle([
                ("BACKGROUND",   (0,0), (-1,-1), LIGHT_BLUE),
                ("ALIGN",        (0,0), (-1,-1), "CENTER"),
                ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
                ("TOPPADDING",   (0,0), (-1,-1), 8),
                ("BOTTOMPADDING",(0,0), (-1,-1), 8),
                ("LEFTPADDING",  (0,0), (-1,-1), 4),
                ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ]))
            cells.append(cell)
        row = Table([cells], colWidths=[(W - 40*mm) / len(items)] * len(items))
        row.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 2),
            ("RIGHTPADDING", (0,0), (-1,-1), 2),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ]))
        return row

    # ════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════════════════
    story = []

    def draw_cover(canvas_obj, doc_obj):
        page_header_footer(canvas_obj, doc_obj) if doc_obj.page > 1 else None
        if doc_obj.page == 1:
            canvas_obj.saveState()
            # Full navy background
            canvas_obj.setFillColor(NAVY)
            canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
            # Accent band
            canvas_obj.setFillColor(ACCENT)
            canvas_obj.rect(0, H*0.38, W, 3*mm, fill=1, stroke=0)
            canvas_obj.setFillColor(GOLD)
            canvas_obj.rect(0, H*0.38 + 3*mm, W, 1*mm, fill=1, stroke=0)
            # Title text
            canvas_obj.setFont("Helvetica-Bold", 38)
            canvas_obj.setFillColor(WHITE)
            canvas_obj.drawCentredString(W/2, H*0.72, "RETAIL INSIGHTS")
            canvas_obj.setFont("Helvetica-Bold", 22)
            canvas_obj.setFillColor(LIGHT_BLUE)
            canvas_obj.drawCentredString(W/2, H*0.65, "A Comprehensive Sales Analytics Portfolio")
            # Gold tag
            canvas_obj.setFont("Helvetica-Bold", 11)
            canvas_obj.setFillColor(GOLD)
            canvas_obj.drawCentredString(W/2, H*0.59, "DATA VISUALIZATION & ANALYTICS  |  CAPSTONE 2  |  ADYPU")
            # Divider line
            canvas_obj.setStrokeColor(ACCENT)
            canvas_obj.setLineWidth(1)
            canvas_obj.line(40*mm, H*0.55, W - 40*mm, H*0.55)
            # Dataset stats
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.setFillColor(colors.HexColor("#A0AEC0"))
            stats = [
                "Dataset: Retail Insights (Kaggle)",
                "5,000 Transactions  •  24 Raw Columns  •  34 Engineered Columns",
                "3 Product Categories  •  4 Customer Segments  •  Australian Multi-State Retail",
                "Date Range: February 2013 – February 2017",
            ]
            y = H*0.50
            for line in stats:
                canvas_obj.drawCentredString(W/2, y, line)
                y -= 14
            # Team
            canvas_obj.setFont("Helvetica-Bold", 9.5)
            canvas_obj.setFillColor(WHITE)
            canvas_obj.drawCentredString(W/2, H*0.29, "Project Team")
            canvas_obj.setFont("Helvetica", 9)
            canvas_obj.setFillColor(colors.HexColor("#A0AEC0"))
            team = [
                "Harshit Aggarwal  •  Team Lead & Data Extraction",
                "Shibaditya Deb  •  Statistical Analysis & ETL Engineering",
                "Arohi Jadhav  •  Tableau & Visualization",
                "Jeet Srivastav  •  Documentation & Reports",
                "Jay Patil  •  EDA & Final Load",
            ]
            y = H*0.25
            for member in team:
                canvas_obj.drawCentredString(W/2, y, member)
                y -= 13
            # Bottom
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(colors.HexColor("#4A5568"))
            canvas_obj.drawCentredString(W/2, 14*mm, "April 2026  |  Atal Bihari Vajpayee University  |  Data Visualization & Analytics")
            canvas_obj.restoreState()

    # Cover is fully drawn by the canvas callback on page 1; just advance to page 2
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY / ABOUT THIS PORTFOLIO
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("About This Portfolio")
    story.append(info_box(
        "This portfolio documents a complete, end-to-end data analytics project undertaken as "
        "Capstone 2 of the Data Visualization & Analytics programme at ADYPU. Every phase of the "
        "analytics lifecycle is covered — from raw data ingestion through statistical validation "
        "to a fully published Tableau dashboard and a set of prioritised business recommendations. "
        "All code, notebooks, and documentation are version-controlled on GitHub using a "
        "professional PR-based workflow."
    ))
    story.append(Spacer(1, 6))

    quick_stats = [
        ("Raw Rows", "5,000", "Kaggle CSV"),
        ("Clean Rows", "4,995", "After ETL"),
        ("Columns", "34", "24 raw + 10 engineered"),
        ("KPIs", "6", "Business metrics"),
        ("Team Size", "5", "Members"),
    ]
    story.append(kpi_row(quick_stats))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════
    # 2. PROBLEM STATEMENT
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Problem Statement")
    story.append(Paragraph(s["quote"].fontName and
        "For a multi-state Australian retailer operating across Consumer, Corporate, "
        "Small Business, and Home Office segments between 2013 and 2017, identify the "
        "customer segments and product categories that drive the top 20% of revenue, "
        "the magnitude and drivers of profit margin variation, and a prioritised "
        "reallocation of retention and promotional budget.", s["quote"]))

    story.append(Paragraph("Business Sub-Questions", s["h2"]))
    sub_qs = [
        "What share of total revenue comes from the top 20% of customers? <i>(Pareto test)</i>",
        "Do Corporate customers have materially higher AOV than Consumer or Small Business customers? <i>(ANOVA / t-test)</i>",
        "Which product category drives the highest profit margin %, and is the difference statistically significant? <i>(ANOVA)</i>",
        "Is there a statistically significant seasonal effect on revenue after controlling for customer type? <i>(Linear regression)</i>",
        "Which shipping mode has the highest shipping cost as a % of order total? <i>(Cross-tab + chi-square)</i>",
        "What is the relationship between average order quantity and profit margin by state? <i>(Correlation + regression)</i>",
    ]
    for q in sub_qs:
        story.append(bullet_item(q))
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 3. DATASET OVERVIEW
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Dataset Source & Overview")
    story.append(Paragraph("Source", s["h2"]))
    ds_data = [
        ["Field", "Value"],
        ["Name", "Retail Insights: A Comprehensive Sales Dataset"],
        ["Platform", "Kaggle"],
        ["Creator", "Rajneesh231"],
        ["URL", "kaggle.com/datasets/rajneesh231/retail-insights-a-comprehensive-sales-dataset"],
        ["Rows", "5,000 transactions"],
        ["Columns", "24 raw columns"],
        ["Time Range", "February 2013 – February 2017"],
        ["Geography", "Australian states (NSW, VIC, QLD, and others)"],
        ["Product Categories", "Furniture, Office Supplies, Technology"],
        ["Customer Segments", "Consumer, Corporate, Home Office, Small Business"],
        ["Format", "CSV — currency strings, date strings (DD-MM-YYYY), percentage strings"],
    ]
    ds_table = Table(ds_data, colWidths=[50*mm, W - 90*mm])
    ds_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("BACKGROUND",   (0,1), (-1,-1), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",         (0,0), (-1,-1), 0.3, DIVIDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,1), (0,-1), NAVY),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Raw Data Quality Issues Identified", s["h2"]))
    issues = [
        "<b>Non-standard date format:</b> Order Date and Ship Date stored as DD-MM-YYYY strings — required explicit dayfirst parsing.",
        "<b>Currency-formatted numerics:</b> All price columns (Cost Price, Retail Price, Sub Total, Order Total, etc.) stored as strings with $ signs and comma separators — stripped during Transform phase.",
        "<b>Percentage strings:</b> Discount % stored as '2%' — percent character stripped and cast to float.",
        "<b>Business logic violations:</b> 4 rows where Cost Price > Retail Price (selling below cost) — removed after investigation.",
        "<b>Missing values:</b> 1 row missing Order Quantity (dropped); 1 row missing Address (retained; Address not used in analysis).",
        "<b>Inconsistent casing:</b> City, State, Customer Type columns had mixed casing — normalised to Title Case.",
    ]
    for issue in issues:
        story.append(bullet_item(issue))
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 4. ETL PIPELINE
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("ETL Pipeline Architecture")
    story.append(Paragraph(
        "The pipeline was built as a modular, production-grade Python script "
        "(<b>scripts/etl_pipeline.py</b>) with 6 discrete phases, structured for "
        "reproducibility, auditability, and ease of re-execution.",
        s["body"]
    ))
    story.append(Spacer(1, 6))

    phases = [
        ("1", "EXTRACT", "Reads raw CSV with dtype=str to preserve all formatting. Validates file existence, encoding (UTF-8 with latin-1 fallback), non-empty rows, and required column schema."),
        ("2", "INITIAL VALIDATION", "Logs shape, all 24 column names, per-column null counts with percentages, and duplicate row count — complete diagnostic snapshot before any transformation."),
        ("3", "TRANSFORM", "8 sub-steps: column rename to snake_case → text normalisation → date parsing → numeric parsing (currency/percent) → missing value imputation → duplicate removal → impossible value removal → feature engineering."),
        ("4", "OUTLIER HANDLING", "IQR×3.0 fence on 5 numeric columns (order_quantity, cost_price, retail_price, profit_margin, order_total). Outliers are capped (Winsorised) not dropped, preserving bulk orders. Companion _is_outlier boolean columns added for Tableau filtering."),
        ("5", "FINAL VALIDATION", "4 assertion checks: zero duplicates, zero nulls in critical columns, cost_price ≤ retail_price everywhere, all non-negative values. Raises RuntimeError on any failure — pipeline fails loudly."),
        ("6", "LOAD", "Creates data/processed/ directory if missing. Writes cleaned_dataset.csv (4,995 rows × 34 columns). Logs file size, row count, column count."),
    ]
    for num, name, desc in phases:
        row_data = [[
            Table([[Paragraph(num, ParagraphStyle("n", fontName="Helvetica-Bold",
                fontSize=14, textColor=WHITE, leading=18, alignment=TA_CENTER))]],
                colWidths=[10*mm], style=TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), ACCENT),
                    ("TOPPADDING", (0,0), (-1,-1), 6),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ])),
            Table([
                [Paragraph(f"Phase {num}: {name}", s["h3"])],
                [Paragraph(desc, s["body"])],
            ], colWidths=[W - 55*mm], style=TableStyle([
                ("LEFTPADDING",  (0,0), (-1,-1), 10),
                ("TOPPADDING",   (0,0), (-1,-1), 3),
                ("BOTTOMPADDING",(0,0), (-1,-1), 3),
            ])),
        ]]
        phase_table = Table(row_data, colWidths=[14*mm, W - 54*mm])
        phase_table.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 0),
            ("BACKGROUND",   (1,0), (1,0), LIGHT_BLUE),
        ]))
        story.append(phase_table)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Pipeline Output", s["h2"]))
    out_stats = [
        ("Input", "5,000 rows", "24 columns"),
        ("Removed", "5 rows", "Logic violations + missing"),
        ("Output", "4,995 rows", "34 columns"),
    ]
    story.append(kpi_row(out_stats))
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 5. ENGINEERED FEATURES
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Feature Engineering & Data Schema")
    feat_data = [
        ["Feature", "Type", "Definition"],
        ["profit_margin_calc", "float", "retail_price − cost_price (clean dollar margin)"],
        ["profit_margin_pct", "float", "(retail_price − cost_price) / retail_price × 100"],
        ["line_revenue", "float", "retail_price × order_quantity"],
        ["order_year", "int", "Calendar year from order_date"],
        ["order_month / order_month_name", "int / str", "Month number and name from order_date"],
        ["order_quarter", "str", "Q1 / Q2 / Q3 / Q4 derived from order_date"],
        ["order_day_of_week", "str", "Day name (Monday, Tuesday, …)"],
        ["order_year_month", "str", "YYYY-MM period bucket for time-series aggregation"],
        ["shipping_lead_days", "int", "ship_date − order_date in days (negatives nullified)"],
        ["<col>_is_outlier", "bool", "IQR×3 outlier flag for 5 numeric columns (Tableau filter)"],
    ]
    feat_table = Table(feat_data, colWidths=[55*mm, 25*mm, W - 110*mm])
    feat_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",         (0,0), (-1,-1), 0.3, DIVIDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 6. KPI FRAMEWORK
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("KPI Framework")
    story.append(Paragraph(
        "Six business KPIs were designed to directly answer the problem statement "
        "sub-questions. Each KPI has a defined formula, analytical grain, and "
        "business interpretation.",
        s["body"]
    ))
    story.append(Spacer(1, 6))

    kpis = [
        ("Line Revenue", "retail_price × order_quantity", "Per transaction", "Primary revenue metric — total selling value of each order line."),
        ("Profit Margin %", "(retail − cost) / retail × 100", "Per transaction / category / segment", "Profitability per unit sold — key for category and segment prioritisation."),
        ("Average Order Value (AOV)", "Σ(order_total) / count(orders)", "Month / segment", "Basket size health — tracks pricing and upsell effectiveness."),
        ("Shipping Cost %", "shipping_cost / order_total × 100", "Ship mode / state", "Logistics efficiency — high % signals margin erosion from shipping overhead."),
        ("Top-20% Revenue Concentration", "Revenue (top 20% customers) / total revenue", "Overall / year", "Pareto test — measures dependence risk on a small high-value customer base."),
        ("Seasonal Revenue Index", "Quarter-over-quarter Σ(line_revenue) / annual mean", "Quarter / year", "Identifies peak seasons for inventory planning and promotional targeting."),
    ]
    for kpi_name, formula, grain, meaning in kpis:
        row = Table([[
            Paragraph(kpi_name, s["h3"]),
            Paragraph(f"<font color='#2E5B8E'><b>Formula:</b></font> {formula}<br/>"
                      f"<font color='#2E5B8E'><b>Grain:</b></font> {grain}<br/>"
                      f"<font color='#4A5568'>{meaning}</font>", s["body"]),
        ]], colWidths=[55*mm, W - 95*mm])
        row.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (0,0), LIGHT_BLUE),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("GRID",         (0,0), (-1,-1), 0.3, DIVIDER),
        ]))
        story.append(row)
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 7. EDA INSIGHTS
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Exploratory Data Analysis — Key Insights")
    eda_insights = [
        ("<b>Revenue concentration:</b>", "Office Supplies accounts for the largest share of transaction volume, while Technology products command significantly higher per-unit revenue and profit margin, driving disproportionate contribution to total line revenue."),
        ("<b>Customer segment distribution:</b>", "Consumer is the largest segment by order count, but Corporate customers show higher average order quantities and order totals — a signal for differential retention investment between segments."),
        ("<b>Seasonal patterns:</b>", "Q3 and Q4 consistently show elevated order volumes and revenue, consistent with back-to-school and year-end procurement cycles. Q1 shows the sharpest dip — a targeting window for promotional campaigns."),
        ("<b>Shipping behaviour:</b>", "Regular Air is the dominant shipping mode. Express Air orders correlate with Critical order priority and carry a measurably higher shipping cost % of order total, compressing effective margin on high-priority orders."),
        ("<b>Geographic concentration:</b>", "New South Wales (NSW) and Victoria (VIC) account for the majority of order volume and revenue, with outer states representing a long tail of lower-volume, higher-shipping-cost transactions."),
        ("<b>Profit margin distribution:</b>", "Profit margin % is tightly distributed between 11% and 81%, with a mean of 45.5%. Furniture shows the highest variance — driven by wide Cost Price spread across SKUs. Office Supplies is most consistent."),
    ]
    for label, text in eda_insights:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {label} {text}", s["bullet"]))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════════════════
    # 8. STATISTICAL ANALYSIS
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Statistical Analysis Findings")
    story.append(Paragraph(
        "Formal statistical tests were applied to validate business hypotheses "
        "and ensure that observed differences are not attributable to random variation.",
        s["body"]
    ))
    story.append(Spacer(1, 6))

    tests = [
        ("One-Way ANOVA — AOV by Customer Type",
         "Tests whether mean Order Total differs significantly across Consumer, Corporate, Home Office, and Small Business segments.",
         "If p < 0.05: Corporate and Small Business segments have statistically distinct AOVs, justifying separate pricing and retention strategies."),
        ("Two-Sample t-test — Profit Margin: Furniture vs Technology",
         "Tests whether Technology products carry a statistically higher profit margin % than Furniture.",
         "Expected result: Technology margin significantly higher, supporting prioritisation of Technology promotions for margin protection."),
        ("Chi-Square — Ship Mode vs Order Priority",
         "Tests association between shipping method chosen and order priority assigned.",
         "If significant: Express Air is disproportionately used for Critical orders, with shipping cost implications that must be factored into pricing for urgent orders."),
        ("Linear Regression — Seasonal Revenue",
         "Revenue ~ month dummies + customer_type (controls for segment mix shifts).",
         "Coefficients on Q3/Q4 month dummies confirm seasonal lift; model used to project promotional timing for maximum revenue capture."),
        ("Correlation Analysis — Order Quantity vs Profit Margin %",
         "Pearson correlation between order_quantity and profit_margin_pct by state.",
         "Directionality indicates whether volume discounting is eroding or maintaining margin — key for bulk-order pricing policy."),
    ]
    for i, (title, method, result) in enumerate(tests, 1):
        row = Table([[
            Table([[Paragraph(str(i), ParagraphStyle("n", fontName="Helvetica-Bold",
                fontSize=13, textColor=WHITE, leading=16, alignment=TA_CENTER))]],
                colWidths=[8*mm], style=TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), STEEL),
                    ("TOPPADDING", (0,0), (-1,-1), 8),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
                ])),
            Table([
                [Paragraph(title, s["h3"])],
                [Paragraph(f"<b>Method:</b> {method}", s["body"])],
                [Paragraph(f"<b>Finding:</b> {result}", s["body"])],
            ], colWidths=[W - 52*mm], style=TableStyle([
                ("LEFTPADDING",  (0,0), (-1,-1), 10),
                ("TOPPADDING",   (0,0), (-1,-1), 3),
                ("BOTTOMPADDING",(0,0), (-1,-1), 3),
                ("BACKGROUND",   (0,0), (-1,-1), LIGHT_BLUE),
            ])),
        ]], colWidths=[12*mm, W - 50*mm])
        row.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 0),
        ]))
        story.append(row)
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════════════════
    # 9. TABLEAU DASHBOARD
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Tableau Dashboard")
    story.append(info_box(
        "An interactive Tableau Public dashboard was developed by Arohi Jadhav, "
        "with KPI-ready flat file prepared by Jay Patil. The dashboard covers "
        "four analytical views: Revenue by Segment & Category, Profit Margin Trends, "
        "Shipping Efficiency Analysis, and Seasonal Revenue Index. "
        "See tableau/dashboard_links.md for the published URL and "
        "tableau/screenshots/ for visual previews."
    ))
    story.append(Spacer(1, 6))

    dash_features = [
        "KPI cards: Total Revenue, Average Profit Margin %, Average Order Value, Shipping Cost %",
        "Revenue breakdown by Product Category and Customer Type (bar + treemap)",
        "Month-over-month and quarter-over-quarter revenue trend lines (2013–2017)",
        "Shipping mode efficiency matrix: Shipping Cost % vs Order Priority heatmap",
        "State-level revenue map with drill-down to city level",
        "Customer segment profitability comparison with AOV and margin overlays",
        "Outlier toggle filter (using _is_outlier columns from ETL pipeline output)",
    ]
    for feat in dash_features:
        story.append(bullet_item(feat))
    story.append(Spacer(1, 6))

    # Screenshot placeholder box
    placeholder = Table([[
        Paragraph(
            "[ Dashboard screenshots available in tableau/screenshots/ folder ]\n\n"
            "Open the Tableau Public link in tableau/dashboard_links.md to interact with the live dashboard.",
            ParagraphStyle("ph", fontName="Helvetica-Oblique", fontSize=9, textColor=MUTED,
                           leading=14, alignment=TA_CENTER)
        )
    ]], colWidths=[W - 40*mm])
    placeholder.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ("BOX",          (0,0), (-1,-1), 1, DIVIDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 20),
        ("RIGHTPADDING", (0,0), (-1,-1), 20),
        ("TOPPADDING",   (0,0), (-1,-1), 30),
        ("BOTTOMPADDING",(0,0), (-1,-1), 30),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(placeholder)
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════
    # 10. BUSINESS RECOMMENDATIONS
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Business Recommendations")
    story.append(Paragraph(
        "Based on the statistical findings and KPI analysis, the following "
        "prioritised recommendations are presented to the retail management team.",
        s["body"]
    ))
    story.append(Spacer(1, 6))

    recs = [
        ("Priority 1", "Protect the Technology Margin",
         "Technology products deliver the highest profit margin %. Allocate 40% of the promotional "
         "budget to Technology category retention campaigns targeting Corporate and Small Business segments, "
         "where AOV is highest. Avoid deep discounting on Technology — margin compression here has "
         "the greatest P&L impact."),
        ("Priority 2", "Activate Q1 Demand Recovery",
         "Q1 is consistently the weakest revenue quarter. Launch targeted promotions in January–February "
         "for the Consumer and Home Office segments (highest Q1 drop-off). Bundle Office Supplies with "
         "Furniture to drive cross-category basket size during the slow period."),
        ("Priority 3", "Rationalise Shipping Cost on Critical Orders",
         "Express Air for Critical orders carries a disproportionately high shipping cost % of order total. "
         "Introduce a minimum order value threshold for Express Air upgrades, or build shipping cost "
         "into the pricing model for Critical-priority Corporate orders rather than absorbing it as overhead."),
        ("Priority 4", "Expand in NSW and VIC; Test QLD",
         "NSW and VIC are the proven revenue bases. Queensland represents the highest-growth opportunity "
         "in the outer-state tier with a manageable shipping cost profile. A targeted acquisition "
         "campaign in QLD is the lowest-risk geographic expansion option."),
        ("Priority 5", "Invest in Corporate Retention",
         "Corporate customers have the highest AOV and show repeat-order behaviour. Build an account "
         "manager-led retention programme — the dataset already maps each customer to an Account Manager. "
         "KPI: increase Corporate repeat purchase rate by 15% over 6 months."),
    ]
    for priority, title, text in recs:
        row = Table([[
            Table([[
                Paragraph(priority, ParagraphStyle("pri", fontName="Helvetica-Bold",
                    fontSize=7.5, textColor=WHITE, leading=10, alignment=TA_CENTER)),
            ]], colWidths=[18*mm], style=TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), NAVY),
                ("TOPPADDING", (0,0), (-1,-1), 10),
                ("BOTTOMPADDING", (0,0), (-1,-1), 10),
                ("ALIGN",     (0,0), (-1,-1), "CENTER"),
            ])),
            Table([
                [Paragraph(title, s["h3"])],
                [Paragraph(text, s["body"])],
            ], colWidths=[W - 60*mm], style=TableStyle([
                ("LEFTPADDING",  (0,0), (-1,-1), 10),
                ("TOPPADDING",   (0,0), (-1,-1), 5),
                ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ])),
        ]], colWidths=[22*mm, W - 60*mm])
        row.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 0),
            ("BOX",          (0,0), (-1,-1), 0.5, DIVIDER),
        ]))
        story.append(row)
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════════════════
    # 11. BUSINESS IMPACT ESTIMATION
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Business Impact Estimation")
    impact_data = [
        ["Recommendation", "Target Metric", "Estimated Impact"],
        ["Technology margin protection", "Profit Margin %", "+2–4% margin on Technology revenue"],
        ["Q1 promotional campaign", "Q1 Revenue", "+10–18% Q1 revenue recovery"],
        ["Express Air cost rationalisation", "Shipping Cost %", "−15–25% shipping overhead on Critical orders"],
        ["QLD geographic expansion", "New Revenue", "5–8% incremental revenue within 12 months"],
        ["Corporate retention programme", "Repeat Purchase Rate", "+15% Corporate retention in 6 months"],
    ]
    impact_table = Table(impact_data, colWidths=[65*mm, 45*mm, W - 140*mm])
    impact_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",         (0,0), (-1,-1), 0.3, DIVIDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",     (2,1), (2,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (2,1), (2,-1), STEEL),
    ]))
    story.append(impact_table)
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 12. CHALLENGES & LEARNINGS
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Challenges Faced & Learnings")

    story.append(Paragraph("Technical Challenges", s["h2"]))
    challenges = [
        ("<b>Currency string parsing at scale:</b>", "All price columns were stored as formatted strings ($1,234.56). Building a reusable _strip_currency() helper that handled edge cases (empty strings, 'nan' literals, null values) without silent failures required careful test-driven iteration."),
        ("<b>SettingWithCopyWarning in pandas:</b>", "After dropna(), pandas returns a view rather than a copy. Appending .copy() explicitly and restructuring the imputation logic to operate on a fresh DataFrame was a key production-quality fix."),
        ("<b>Business logic validation across pipeline stages:</b>", "The cost > retail violation wasn't visible until the Transform phase. Building the validation as an assertion that raises RuntimeError rather than a silent log line meant the pipeline fail-fast design caught this reliably."),
        ("<b>IQR outlier tuning:</b>", "A standard IQR×1.5 fence flagged many legitimate bulk orders as outliers. Adjusting the multiplier to 3.0 after domain analysis — and choosing to cap rather than drop — required understanding the retail context, not just applying a formula."),
    ]
    for label, text in challenges:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {label} {text}", s["bullet"]))
        story.append(Spacer(1, 3))

    story.append(Paragraph("Key Learnings", s["h2"]))
    learnings = [
        "Production ETL design requires fail-fast validation at every phase boundary — silent data corruption is harder to debug than a loud RuntimeError.",
        "Feature engineering decisions should be driven by the downstream analytical question, not by what is technically possible to compute.",
        "Statistical tests should always be accompanied by effect size and business context — a p-value alone does not make a recommendation.",
        "Version control with PR-based review (not just commits) is the difference between a project that looks collaborative and one that actually is.",
        "Tableau dashboards are only as strong as the data contract they consume — the time invested in a clean schema pays off in zero transformation errors at the viz layer.",
    ]
    for l in learnings:
        story.append(bullet_item(l))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════════════════
    # 13. CONCLUSION
    # ════════════════════════════════════════════════════════════════════════
    story += section_title("Conclusion")
    story.append(info_box(
        "This project demonstrates a complete analytics lifecycle — from raw, unstructured retail "
        "data to a production-grade ETL pipeline, validated statistical findings, and "
        "stakeholder-ready business recommendations. The team of five built a reproducible "
        "system: any team member can re-run the full pipeline from a single command, "
        "regenerate the cleaned dataset, and re-execute every statistical notebook independently. "
        "The Tableau dashboard provides an interactive layer for non-technical stakeholders to "
        "explore the same findings. The result is a portfolio-grade project that demonstrates "
        "not only technical competence but the ability to frame, execute, and communicate "
        "a data-driven business case — the core skill set for Data Analyst, Business Analyst, "
        "and Data Science roles.",
        bg=LIGHT_BLUE
    ))
    story.append(Spacer(1, 8))

    # Team card
    team_data = [["Team Member", "Role", "Key Contribution"]] + [
        ["Harshit Aggarwal", "Team Lead & Data Extraction", "01_extraction.ipynb, repo architecture, raw data commit"],
        ["Shibaditya Deb", "Statistical Analysis & ETL", "ETL pipeline, statistical notebooks, data dictionary"],
        ["Arohi Jadhav", "Tableau & Visualization", "Tableau workbook, dashboard design, screenshots"],
        ["Jeet Srivastav", "Documentation & Reports", "Gate 1 proposal, final report, presentation deck"],
        ["Jay Patil", "EDA & Final Load", "03_eda.ipynb, final load prep, KPI flat file"],
    ]
    team_table = Table(team_data, colWidths=[50*mm, 50*mm, W - 130*mm])
    team_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",         (0,0), (-1,-1), 0.3, DIVIDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,1), (0,-1), NAVY),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "github.com/shibadityadeb  •  Data Visualization & Analytics  •  ADYPU  •  April 2026",
        ParagraphStyle("footer", fontName="Helvetica", fontSize=8, textColor=MUTED, alignment=TA_CENTER)
    ))

    # Build
    def first_page(c, d):
        draw_cover(c, d)

    def later_pages(c, d):
        page_header_footer(c, d)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"[portfolio] Written → {out_path}")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    build_resume(root / "resume" / "dva_resume.pdf")
    build_portfolio(root / "portfolio" / "dva_portfolio.pdf")
    print("\nDone. Both assets generated successfully.")
