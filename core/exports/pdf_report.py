from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus.flowables import Flowable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import numpy as np
import tempfile
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# BRAND PALETTE
# ─────────────────────────────────────────────────────────────────
BRAND_BLUE   = colors.HexColor("#007AFF")
BRAND_INDIGO = colors.HexColor("#5856D6")
BRAND_DARK   = colors.HexColor("#0F1117")
BRAND_MID    = colors.HexColor("#3A4455")
BRAND_MUTED  = colors.HexColor("#6B7585")
BRAND_LIGHT  = colors.HexColor("#F3F5FB")
BRAND_LINE   = colors.HexColor("#E2E5F0")
WHITE        = colors.white
SUCCESS      = colors.HexColor("#1a7a36")
DANGER       = colors.HexColor("#c0392b")

PAGE_W, PAGE_H = A4
MARGIN = 38


# ─────────────────────────────────────────────────────────────────
# CUSTOM FLOWABLES
# ─────────────────────────────────────────────────────────────────
class ColorBar(Flowable):
    """Full-width accent bar — used as section dividers."""
    def __init__(self, height=2, color=BRAND_BLUE, width=None):
        super().__init__()
        self._h = height
        self._c = color
        self._w = width
    def wrap(self, available_width, available_height):
        self.width = self._w or available_width
        self.height = self._h
        return self.width, self.height
    def draw(self):
        self.canv.setFillColor(self._c)
        self.canv.rect(0, 0, self.width, self._h, stroke=0, fill=1)


class SectionHeader(Flowable):
    """Pill-style numbered section header."""
    def __init__(self, number, title, available_width=None):
        super().__init__()
        self._num   = number
        self._title = title
        self._aw    = available_width or (PAGE_W - 2 * MARGIN)
    def wrap(self, aw, ah):
        self.width  = self._aw
        self.height = 28
        return self.width, self.height
    def draw(self):
        c = self.canv
        # pill background
        c.setFillColor(BRAND_BLUE)
        c.roundRect(0, 4, 28, 20, 4, stroke=0, fill=1)
        # number
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(14, 9, str(self._num))
        # title
        c.setFillColor(BRAND_DARK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(36, 8, self._title.upper())
        # underline
        c.setStrokeColor(BRAND_LINE)
        c.setLineWidth(0.75)
        c.line(0, 2, self.width, 2)


class KPIRow(Flowable):
    """Horizontal row of KPI boxes."""
    def __init__(self, kpis, available_width=None):
        super().__init__()
        self._kpis = kpis          # list of (label, value, sub) tuples
        self._aw   = available_width or (PAGE_W - 2 * MARGIN)
    def wrap(self, aw, ah):
        self.width  = self._aw
        self.height = 72
        return self.width, self.height
    def draw(self):
        c   = self.canv
        n   = len(self._kpis)
        gap = 8
        box_w = (self.width - gap * (n - 1)) / n
        for i, (label, value, sub) in enumerate(self._kpis):
            x = i * (box_w + gap)
            # card background
            c.setFillColor(BRAND_LIGHT)
            c.roundRect(x, 0, box_w, self.height - 4, 6, stroke=0, fill=1)
            # top accent line
            c.setFillColor(BRAND_BLUE)
            c.roundRect(x, self.height - 6, box_w, 2, 1, stroke=0, fill=1)
            # label
            c.setFillColor(BRAND_MUTED)
            c.setFont("Helvetica", 6.5)
            c.drawString(x + 10, self.height - 20, label.upper())
            # value
            c.setFillColor(BRAND_DARK)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(x + 10, self.height - 40, str(value))
            # sub
            if sub:
                c.setFillColor(BRAND_MUTED)
                c.setFont("Helvetica", 7)
                c.drawString(x + 10, self.height - 56, str(sub))


# ─────────────────────────────────────────────────────────────────
# MATPLOTLIB THEME
# ─────────────────────────────────────────────────────────────────
def apply_theme(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor("#F3F5FB")
    ax.figure.patch.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E2E5F0")
    ax.spines["bottom"].set_color("#E2E5F0")
    ax.tick_params(colors="#6B7585", labelsize=7)
    ax.xaxis.label.set_color("#6B7585")
    ax.yaxis.label.set_color("#6B7585")
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)
    if title:
        ax.set_title(title, color="#0F1117", fontsize=10, fontweight="bold", pad=10)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L" if x >= 1e5 else f"{x:.0f}"))


def save_fig(fig, suffix=".png"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    fig.savefig(tmp.name, dpi=180, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    return tmp.name


# ─────────────────────────────────────────────────────────────────
# PAGE TEMPLATE — header/footer on every page
# ─────────────────────────────────────────────────────────────────
class PageTemplate:
    def __init__(self, project_name="StructuraAI Report"):
        self.project = project_name
        self.generated = datetime.now().strftime("%d %b %Y · %H:%M")

    def __call__(self, canv, doc):
        canv.saveState()
        w, h = A4

        # ── TOP BAR ──────────────────────────────────────────────
        canv.setFillColor(BRAND_DARK)
        canv.rect(0, h - 38, w, 38, stroke=0, fill=1)

        # Logo mark
        canv.setFillColor(BRAND_BLUE)
        canv.roundRect(MARGIN, h - 29, 18, 18, 3, stroke=0, fill=1)
        canv.setFillColor(WHITE)
        canv.setFont("Helvetica-Bold", 8)
        canv.drawCentredString(MARGIN + 9, h - 22, "◈")

        # Brand name
        canv.setFillColor(WHITE)
        canv.setFont("Helvetica-Bold", 11)
        canv.drawString(MARGIN + 24, h - 22, "StructuraAI")
        canv.setFillColor(BRAND_MUTED)
        canv.setFont("Helvetica", 7.5)
        canv.drawString(MARGIN + 95, h - 22, "Construction Intelligence Platform")

        # Right — date
        canv.setFillColor(BRAND_MUTED)
        canv.setFont("Helvetica", 7)
        canv.drawRightString(w - MARGIN, h - 22, self.generated)

        # ── BOTTOM BAR ───────────────────────────────────────────
        canv.setFillColor(BRAND_LINE)
        canv.rect(0, 0, w, 22, stroke=0, fill=1)

        # Accent line above footer
        canv.setFillColor(BRAND_BLUE)
        canv.rect(0, 22, w, 1.5, stroke=0, fill=1)

        canv.setFillColor(BRAND_MUTED)
        canv.setFont("Helvetica", 6.5)
        canv.drawString(MARGIN, 8, "CONFIDENTIAL · StructuraAI Intelligence Report")
        canv.drawRightString(w - MARGIN, 8, f"Page {doc.page}")

        canv.restoreState()


# ─────────────────────────────────────────────────────────────────
# CHART GENERATORS
# ─────────────────────────────────────────────────────────────────
def chart_monte_carlo(base_cost, risk_score):
    sims = np.random.normal(base_cost, base_cost * (risk_score / 100), 3000)
    p10, p50, p90 = np.percentile(sims, [10, 50, 90])

    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    n, bins, patches = ax.hist(sims, bins=50, edgecolor="none")

    # Colour bins by percentile
    for patch, left in zip(patches, bins[:-1]):
        if left < p10:
            patch.set_facecolor("#FFD6D6")
        elif left < p90:
            patch.set_facecolor("#007AFF")
        else:
            patch.set_facecolor("#C0392B")

    for pct, val, lbl, clr in [(p10, p10, "P10", "#C0392B"),
                                 (p50, p50, "P50", "#0F1117"),
                                 (p90, p90, "P90", "#1a7a36")]:
        ax.axvline(val, color=clr, linewidth=1.2, linestyle="--", alpha=0.8)
        ax.text(val, ax.get_ylim()[1] * 0.85, f" {lbl}", color=clr,
                fontsize=6.5, fontweight="bold")

    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
    apply_theme(ax, xlabel="Projected Cost", ylabel="Frequency")
    ax.set_title("")
    fig.tight_layout()
    return save_fig(fig)


def chart_cashflow(base_cost):
    months = np.arange(1, 13)
    monthly = np.linspace(base_cost / 14, base_cost / 9, 12)
    cumulative = np.cumsum(monthly)
    planned = np.linspace(base_cost / 12, base_cost / 12, 12)
    plan_cum = np.cumsum(planned)

    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    ax.fill_between(months, cumulative, alpha=0.12, color="#007AFF")
    ax.plot(months, cumulative, color="#007AFF", linewidth=2, label="Actual Spend", marker="o", markersize=3.5)
    ax.plot(months, plan_cum, color="#5856D6", linewidth=1.5, linestyle="--", label="Planned Spend")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"M{int(x)}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L"))
    ax.legend(fontsize=7, framealpha=0, labelcolor="#3A4455")
    apply_theme(ax, xlabel="Month", ylabel="Cumulative (₹)")
    fig.tight_layout()
    return save_fig(fig)


def chart_risk_radar(risk_factors):
    labels = list(risk_factors.keys())[:6]
    values = [min(risk_factors[k], 100) for k in labels]
    N = len(labels)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(3.2, 3.2), subplot_kw=dict(polar=True))
    ax.set_facecolor("#F3F5FB")
    fig.patch.set_facecolor("white")
    ax.plot(angles, values, color="#007AFF", linewidth=2)
    ax.fill(angles, values, color="#007AFF", alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=7, color="#3A4455")
    ax.set_ylim(0, 100)
    ax.tick_params(colors="#6B7585", labelsize=6)
    ax.spines["polar"].set_color("#E2E5F0")
    ax.yaxis.set_ticklabels([])
    fig.tight_layout()
    return save_fig(fig)


def chart_resource_bar(quantities):
    if not quantities:
        quantities = {"Concrete": 450, "Steel": 180, "Formwork": 320, "Labour": 240, "MEP": 110}
    labels = list(quantities.keys())[:8]
    vals   = [float(quantities[k]) for k in labels]
    norm   = [v / max(vals) for v in vals]

    fig, ax = plt.subplots(figsize=(6.2, 2.4))
    bars = ax.barh(labels, vals, color=[
        "#007AFF" if n >= 0.75 else ("#5856D6" if n >= 0.45 else "#A0B4D6")
        for n in norm
    ], edgecolor="none", height=0.55)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.0f}", va="center", color="#3A4455", fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.15)
    ax.xaxis.set_visible(False)
    apply_theme(ax)
    fig.tight_layout()
    return save_fig(fig)


def chart_phase_gantt(schedule):
    if not schedule:
        schedule = [
            {"task": "Site Preparation", "start": "2024-01-01", "finish": "2024-01-15"},
            {"task": "Foundation",        "start": "2024-01-10", "finish": "2024-02-10"},
            {"task": "Structural Frame",  "start": "2024-02-01", "finish": "2024-04-01"},
            {"task": "MEP Rough-in",      "start": "2024-03-15", "finish": "2024-05-01"},
            {"task": "Facade & Roofing",  "start": "2024-04-01", "finish": "2024-05-15"},
            {"task": "Finishing",         "start": "2024-05-01", "finish": "2024-06-15"},
        ]
    import pandas as pd
    df = pd.DataFrame(schedule)
    df["start"]  = pd.to_datetime(df["start"])
    df["finish"] = pd.to_datetime(df["finish"])
    df["dur"]    = (df["finish"] - df["start"]).dt.days

    fig, ax = plt.subplots(figsize=(6.2, max(2.4, len(df) * 0.42)))
    colors_list = ["#007AFF", "#5856D6", "#34C759", "#FF9F0A", "#FF453A", "#64D2FF"]
    base = df["start"].min()
    for i, row in df.iterrows():
        start_d = (row["start"] - base).days
        ax.barh(i, row["dur"], left=start_d,
                color=colors_list[i % len(colors_list)],
                edgecolor="none", height=0.55, alpha=0.88)
        ax.text(start_d + row["dur"] / 2, i, row["task"],
                ha="center", va="center", color="white",
                fontsize=6.5, fontweight="bold")
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"D{int(x)}"))
    apply_theme(ax, xlabel="Project Day")
    ax.invert_yaxis()
    fig.tight_layout()
    return save_fig(fig)


# ─────────────────────────────────────────────────────────────────
# STYLE DEFINITIONS
# ─────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    styles = {
        "cover_title": ps("cover_title",
            fontName="Helvetica-Bold", fontSize=28,
            textColor=BRAND_DARK, leading=34, spaceAfter=6),
        "cover_sub": ps("cover_sub",
            fontName="Helvetica", fontSize=12,
            textColor=BRAND_MUTED, leading=18),
        "cover_meta": ps("cover_meta",
            fontName="Helvetica", fontSize=8.5,
            textColor=BRAND_MUTED, leading=14),
        "body": ps("body",
            fontName="Helvetica", fontSize=8.5,
            textColor=BRAND_MID, leading=14, spaceAfter=4),
        "body_bold": ps("body_bold",
            fontName="Helvetica-Bold", fontSize=8.5,
            textColor=BRAND_DARK, leading=14),
        "caption": ps("caption",
            fontName="Helvetica", fontSize=7,
            textColor=BRAND_MUTED, leading=11, spaceAfter=8, alignment=TA_CENTER),
        "table_head": ps("table_head",
            fontName="Helvetica-Bold", fontSize=7.5,
            textColor=WHITE, leading=10),
        "table_cell": ps("table_cell",
            fontName="Helvetica", fontSize=8,
            textColor=BRAND_MID, leading=12),
        "insight": ps("insight",
            fontName="Helvetica", fontSize=8,
            textColor=BRAND_DARK, leading=13,
            leftIndent=10, borderPad=8,
            backColor=colors.HexColor("#EEF3FF"),
            borderColor=BRAND_BLUE, borderWidth=0,
            spaceAfter=6),
    }
    return styles


# ─────────────────────────────────────────────────────────────────
# TABLE HELPERS
# ─────────────────────────────────────────────────────────────────
def styled_table(data_rows, col_widths, header=True):
    """Create a clean, professionally styled table."""
    s = make_styles()
    table_data = []
    for r_idx, row in enumerate(data_rows):
        styled_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0 and header:
                styled_row.append(Paragraph(str(cell), s["table_head"]))
            else:
                styled_row.append(Paragraph(str(cell), s["table_cell"]))
        table_data.append(styled_row)

    t = Table(table_data, colWidths=col_widths, repeatRows=1 if header else 0)

    style = [
        # Header row
        ("BACKGROUND",    (0, 0), (-1, 0),  BRAND_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  7.5),
        ("TOPPADDING",    (0, 0), (-1, 0),  7),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  7),
        # Body rows
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("TEXTCOLOR",     (0, 1), (-1, -1), BRAND_MID),
        ("TOPPADDING",    (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 9),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
        # Alternating rows
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, BRAND_LIGHT]),
        # Grid
        ("GRID",          (0, 0), (-1, -1), 0.4, BRAND_LINE),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.2, BRAND_BLUE),
        ("LINEBELOW",     (0, -1),(-1, -1), 0.8, BRAND_LINE),
        ("ROUNDEDCORNERS",[4]),
    ]
    t.setStyle(TableStyle(style))
    return t


def insight_box(text, s):
    """Blue-left-border insight/callout paragraph."""
    return Table(
        [[Paragraph(f"<b>Insight:</b> {text}", s["body"])]],
        colWidths=[PAGE_W - 2 * MARGIN],
        style=TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#EEF3FF")),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LINEAFTER",     (0, 0), (0, -1),  0, WHITE),     # suppress right border
            ("LINEBEFORE",    (0, 0), (0, -1),  3, BRAND_BLUE),
            ("ROUNDEDCORNERS",[4]),
        ])
    )


# ─────────────────────────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────────────────────────
def generate_pdf_report(data, filename="structuraai_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=55,
        bottomMargin=38,
    )

    pt  = PageTemplate()
    s   = make_styles()
    el  = []          # story elements
    aw  = PAGE_W - 2 * MARGIN   # available width

    # ── pull data ────────────────────────────────────────────────
    risk_data  = data.get("Risk Summary", {})
    build_data = data.get("Buildability Summary", {})
    cost_data  = data.get("Cost Breakdown", {})
    quantities = data.get("Material Quantities", {})
    schedule   = data.get("Schedule", [])
    risk_factors = data.get("Risk Factors", {
        "Structural": 45, "Schedule": 60, "Cost": 35,
        "Environmental": 25, "Labour": 55, "Regulatory": 20
    })

    risk_score  = risk_data.get("risk_score", 40)
    build_score = build_data.get("final_score", 72)
    base_cost   = cost_data.get("total_project_cost", 1_000_000)

    # ─────────────────────────────────────────────────────────────
    # PAGE 1 — COVER
    # ─────────────────────────────────────────────────────────────
    # Large accent block (rendered via canvas call)
    el.append(Spacer(1, 0.15 * inch))

    el.append(ColorBar(height=3, color=BRAND_BLUE, width=aw))
    el.append(Spacer(1, 18))

    el.append(Paragraph("PROJECT INTELLIGENCE", s["cover_meta"]))
    el.append(Spacer(1, 4))
    el.append(Paragraph("Structural Analysis<br/>& Construction Report", s["cover_title"]))
    el.append(Spacer(1, 8))
    el.append(Paragraph("Comprehensive risk, cost, and schedule assessment generated<br/>"
                         "by StructuraAI's automated analysis pipeline.", s["cover_sub"]))
    el.append(Spacer(1, 22))

    # Cover KPI strip
    el.append(KPIRow([
        ("Risk Score",       f"{risk_score}",          f"{'Low' if risk_score<40 else 'Medium' if risk_score<65 else 'High'} Risk"),
        ("Buildability",     f"{build_score}/100",      "Constructability Index"),
        ("Project Budget",   f"₹{base_cost/1e5:.1f}L", "Total Estimated Cost"),
        ("Report Date",      datetime.now().strftime("%d %b %Y"), datetime.now().strftime("%H:%M IST")),
    ], available_width=aw))

    el.append(Spacer(1, 22))
    el.append(ColorBar(height=1, color=BRAND_LINE, width=aw))
    el.append(Spacer(1, 10))

    # Report scope table
    scope_rows = [
        ["Report Section", "Description"],
        ["01 — Executive Summary",   "Key metrics, risk classification, buildability overview"],
        ["02 — Cost Intelligence",   "Budget breakdown, Monte Carlo simulation, NPV/IRR"],
        ["03 — Schedule Analysis",   "Phase Gantt, cashflow projection, critical timeline"],
        ["04 — Risk Assessment",     "Risk radar, phase-level risk matrix, mitigations"],
        ["05 — Resource Utilisation","Material quantities and crew allocation"],
    ]
    el.append(styled_table(scope_rows, [2.2*inch, aw - 2.2*inch]))
    el.append(Spacer(1, 10))

    el.append(Paragraph(
        f"<b>Prepared by:</b> StructuraAI Automated Analysis Engine &nbsp;·&nbsp; "
        f"<b>Classification:</b> Confidential &nbsp;·&nbsp; "
        f"<b>Valid Until:</b> 30 days from generation",
        s["body"]
    ))

    el.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # PAGE 2 — EXECUTIVE SUMMARY
    # ─────────────────────────────────────────────────────────────
    el.append(SectionHeader(1, "Executive Summary", aw))
    el.append(Spacer(1, 12))

    # Risk classification badge (text-based)
    risk_level = "LOW" if risk_score < 40 else "MEDIUM" if risk_score < 65 else "HIGH"
    risk_color = SUCCESS if risk_score < 40 else colors.HexColor("#B8600A") if risk_score < 65 else DANGER

    summary_rows = [
        ["Metric",                  "Value",                         "Status"],
        ["Overall Risk Score",      f"{risk_score} / 100",           risk_level],
        ["Buildability Score",      f"{build_score} / 100",          "ACCEPTABLE" if build_score >= 60 else "REVIEW"],
        ["Total Project Cost",      f"₹{base_cost:,.0f}",            "BASELINE"],
        ["Cost Contingency (P90)",  f"₹{base_cost*1.25:,.0f}",      "+25% BUFFER"],
        ["Expected Duration",       f"{data.get('Duration', 120)} days", "SCHEDULED"],
    ]
    el.append(styled_table(summary_rows, [2.5*inch, 2.1*inch, aw - 4.6*inch]))
    el.append(Spacer(1, 10))

    el.append(insight_box(
        f"The project carries a <b>{risk_level.title()} risk profile</b> with a score of {risk_score}/100. "
        f"Buildability index of {build_score}/100 indicates "
        f"{'strong constructability — proceed with standard protocols.' if build_score >= 70 else 'moderate complexity — enhanced supervision recommended.'}", s))
    el.append(Spacer(1, 14))

    # Cost breakdown table
    el.append(Paragraph("<b>Cost Breakdown by Category</b>", s["body_bold"]))
    el.append(Spacer(1, 6))

    cb = cost_data.get("breakdown", {
        "Foundation & Substructure": base_cost * 0.18,
        "Structural Frame":          base_cost * 0.22,
        "External Envelope":         base_cost * 0.14,
        "MEP Services":              base_cost * 0.20,
        "Internal Fit-out":          base_cost * 0.12,
        "Preliminaries":             base_cost * 0.08,
        "Contingency":               base_cost * 0.06,
    })
    cost_rows = [["Category", "Amount (₹)", "% of Total"]]
    for k, v in cb.items():
        cost_rows.append([k, f"₹{float(v):,.0f}", f"{float(v)/base_cost*100:.1f}%"])
    cost_rows.append(["<b>TOTAL</b>", f"<b>₹{base_cost:,.0f}</b>", "<b>100.0%</b>"])
    el.append(styled_table(cost_rows, [3.0*inch, 2.0*inch, aw - 5.0*inch]))

    el.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # PAGE 3 — COST INTELLIGENCE
    # ─────────────────────────────────────────────────────────────
    el.append(SectionHeader(2, "Cost Intelligence", aw))
    el.append(Spacer(1, 12))

    # Financial snapshot KPIs
    discount_rate     = 0.10
    projected_return  = base_cost * 1.25
    npv  = projected_return / (1 + discount_rate) - base_cost
    irr  = (projected_return / base_cost) - 1
    roi  = (projected_return - base_cost) / base_cost * 100

    el.append(KPIRow([
        ("NPV (10% discount)", f"₹{npv/1e5:.1f}L", "Net Present Value"),
        ("IRR",                f"{irr*100:.1f}%",   "Internal Rate of Return"),
        ("ROI",                f"{roi:.1f}%",       "Return on Investment"),
        ("Payback",            f"{base_cost/projected_return*12:.0f} mo", "Estimated Payback"),
    ], available_width=aw))

    el.append(Spacer(1, 14))

    # Monte Carlo
    el.append(Paragraph("<b>Cost Risk Simulation — Monte Carlo (3,000 runs)</b>", s["body_bold"]))
    el.append(Spacer(1, 4))
    mc_path = chart_monte_carlo(base_cost, risk_score)
    el.append(Image(mc_path, width=aw, height=2.5*inch))
    el.append(Paragraph(
        "Distribution of projected costs across 3,000 simulated scenarios. "
        "Red = P10 (best case), Blue = P50 (median), Green = P90 (worst case).",
        s["caption"]))
    el.append(Spacer(1, 10))

    # Percentile table
    sims = np.random.normal(base_cost, base_cost * (risk_score / 100), 3000)
    p10, p50, p90 = np.percentile(sims, [10, 50, 90])
    pct_rows = [
        ["Percentile", "Projected Cost", "Delta vs Baseline", "Recommendation"],
        ["P10 (Optimistic)",  f"₹{p10:,.0f}", f"{(p10-base_cost)/base_cost*100:+.1f}%", "Best-case scenario"],
        ["P50 (Median)",      f"₹{p50:,.0f}", f"{(p50-base_cost)/base_cost*100:+.1f}%", "Planning baseline"],
        ["P90 (Pessimistic)", f"₹{p90:,.0f}", f"{(p90-base_cost)/base_cost*100:+.1f}%", "Reserve funding buffer"],
    ]
    el.append(styled_table(pct_rows, [1.8*inch, 1.7*inch, 1.6*inch, aw - 5.1*inch]))

    el.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # PAGE 4 — SCHEDULE & CASHFLOW
    # ─────────────────────────────────────────────────────────────
    el.append(SectionHeader(3, "Schedule Analysis", aw))
    el.append(Spacer(1, 12))

    el.append(Paragraph("<b>Phase Execution Timeline</b>", s["body_bold"]))
    el.append(Spacer(1, 4))
    gantt_path = chart_phase_gantt(schedule)
    el.append(Image(gantt_path, width=aw, height=2.6*inch))
    el.append(Paragraph("Colour-coded Gantt: each bar represents a construction phase with duration in project days.", s["caption"]))
    el.append(Spacer(1, 14))

    el.append(Paragraph("<b>Cumulative Cashflow Projection (12 Months)</b>", s["body_bold"]))
    el.append(Spacer(1, 4))
    cf_path = chart_cashflow(base_cost)
    el.append(Image(cf_path, width=aw, height=2.6*inch))
    el.append(Paragraph("Solid line = projected spend. Dashed line = planned baseline. "
                         "Divergence indicates schedule variance.", s["caption"]))
    el.append(Spacer(1, 10))

    el.append(insight_box(
        "Peak cashflow demand occurs in months 4–8. Ensure draw schedules and credit facilities "
        "are arranged at least 6 weeks in advance of each phase milestone.", s))

    el.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # PAGE 5 — RISK ASSESSMENT
    # ─────────────────────────────────────────────────────────────
    el.append(SectionHeader(4, "Risk Assessment", aw))
    el.append(Spacer(1, 12))

    # Risk radar + table side by side
    radar_path = chart_risk_radar(risk_factors)

    risk_rows = [["Risk Category", "Score", "Level", "Mitigation"]]
    for cat, score in risk_factors.items():
        level = "Low" if score < 35 else "Medium" if score < 65 else "High"
        mit   = {
            "Structural":    "Peer review all structural calcs",
            "Schedule":      "Buffer 15% on critical path",
            "Cost":          "Maintain P90 contingency reserve",
            "Environmental": "Pre-construction site audit",
            "Labour":        "Secure subcontracts early",
            "Regulatory":    "Pre-application authority meeting",
        }.get(cat, "Monitor and review")
        risk_rows.append([cat, f"{score}/100", level, mit])

    risk_tbl = styled_table(risk_rows, [1.1*inch, 0.7*inch, 0.75*inch, 2.5*inch])
    radar_img = Image(radar_path, width=2.2*inch, height=2.2*inch)

    combo = Table(
        [[radar_img, risk_tbl]],
        colWidths=[2.4*inch, aw - 2.4*inch],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ])
    )
    el.append(combo)
    el.append(Spacer(1, 14))

    # Risk matrix heat table
    el.append(Paragraph("<b>Risk Impact Matrix</b>", s["body_bold"]))
    el.append(Spacer(1, 6))
    matrix_rows = [
        ["",           "LOW Impact",      "MEDIUM Impact",    "HIGH Impact"],
        ["HIGH Prob",  "Monitor",         "Mitigate Actively","Critical — Escalate"],
        ["MED Prob",   "Accept",          "Mitigate",         "Mitigate Actively"],
        ["LOW Prob",   "Accept",          "Accept/Monitor",   "Mitigate"],
    ]
    heat_tbl = Table(matrix_rows, colWidths=[1.2*inch, (aw-1.2*inch)/3]*3)
    heat_style = TableStyle([
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID",          (0, 0), (-1, -1), 0.4, BRAND_LINE),
        ("BACKGROUND",    (0, 0), (-1, 0),  BRAND_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("BACKGROUND",    (0, 1), (0, -1),  BRAND_DARK),
        ("TEXTCOLOR",     (0, 1), (0, -1),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        # Heat colours
        ("BACKGROUND",    (3, 1), (3, 1),   colors.HexColor("#FFD6D6")),
        ("TEXTCOLOR",     (3, 1), (3, 1),   DANGER),
        ("BACKGROUND",    (2, 1), (2, 1),   colors.HexColor("#FFE8C8")),
        ("BACKGROUND",    (1, 1), (1, 1),   colors.HexColor("#D6FFE4")),
        ("BACKGROUND",    (3, 2), (3, 2),   colors.HexColor("#FFE8C8")),
        ("BACKGROUND",    (2, 2), (2, 2),   colors.HexColor("#FFE8C8")),
        ("BACKGROUND",    (1, 3), (1, 3),   colors.HexColor("#D6FFE4")),
    ])
    heat_tbl.setStyle(heat_style)
    el.append(heat_tbl)

    el.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # PAGE 6 — RESOURCE UTILISATION
    # ─────────────────────────────────────────────────────────────
    el.append(SectionHeader(5, "Resource Utilisation", aw))
    el.append(Spacer(1, 12))

    el.append(Paragraph("<b>Material Quantity Summary</b>", s["body_bold"]))
    el.append(Spacer(1, 4))
    res_path = chart_resource_bar(quantities)
    el.append(Image(res_path, width=aw, height=2.3*inch))
    el.append(Paragraph("Bars coloured by utilisation intensity: dark blue = high, medium = moderate, light = low.", s["caption"]))
    el.append(Spacer(1, 12))

    # Material quantities table
    if quantities:
        qty_rows = [["Material / Resource", "Quantity", "Unit", "Estimated Cost (₹)"]]
        for mat, qty in quantities.items():
            unit_cost = base_cost / sum(quantities.values()) * float(qty)
            qty_rows.append([mat, f"{float(qty):,.1f}", "units", f"₹{unit_cost:,.0f}"])
        el.append(styled_table(qty_rows, [2.4*inch, 1.2*inch, 0.8*inch, aw - 4.4*inch]))
        el.append(Spacer(1, 10))

    # Final notes
    el.append(ColorBar(height=1, color=BRAND_LINE, width=aw))
    el.append(Spacer(1, 10))
    el.append(Paragraph("<b>Report Notes &amp; Disclaimer</b>", s["body_bold"]))
    el.append(Spacer(1, 4))
    el.append(Paragraph(
        "This report was generated automatically by the StructuraAI analysis pipeline from submitted "
        "structural drawings. All cost estimates are indicative and subject to market conditions, "
        "site-specific factors, and contractor quotes. Monte Carlo simulations are based on "
        "statistical modelling and do not guarantee outcomes. Engage a qualified QS for final "
        "cost planning. Risk scores are computed from drawing metadata and should be validated "
        "by a structural engineer before project mobilisation.",
        s["body"]
    ))

    # ─────────────────────────────────────────────────────────────
    # BUILD PDF
    # ─────────────────────────────────────────────────────────────
    tmp_files = [mc_path, cf_path, radar_path, res_path, gantt_path]

    doc.build(el, onFirstPage=pt, onLaterPages=pt)

    for f in tmp_files:
        try: os.remove(f)
        except: pass

    return filename


# ─────────────────────────────────────────────────────────────────
# TEST HARNESS
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample_data = {
        "Risk Summary":        {"risk_score": 52},
        "Buildability Summary":{"final_score": 74},
        "Cost Breakdown": {
            "total_project_cost": 4_850_000,
            "breakdown": {
                "Foundation & Substructure": 873_000,
                "Structural Frame":          1_067_000,
                "External Envelope":         679_000,
                "MEP Services":              970_000,
                "Internal Fit-out":          582_000,
                "Preliminaries":             388_000,
                "Contingency":               291_000,
            }
        },
        "Material Quantities": {
            "Concrete (m³)":    450,
            "Steel (tonnes)":   38,
            "Formwork (m²)":    1200,
            "Brickwork (m²)":   620,
            "Glazing (m²)":     310,
            "Insulation (m²)":  890,
        },
        "Risk Factors": {
            "Structural":    45,
            "Schedule":      62,
            "Cost":          38,
            "Environmental": 28,
            "Labour":        57,
            "Regulatory":    22,
        },
        "Duration": 148,
        "Schedule": [
            {"task": "Site Preparation", "start": "2024-01-01", "finish": "2024-01-18"},
            {"task": "Foundation",       "start": "2024-01-12", "finish": "2024-02-20"},
            {"task": "Structural Frame", "start": "2024-02-10", "finish": "2024-04-15"},
            {"task": "MEP Rough-in",     "start": "2024-03-20", "finish": "2024-05-10"},
            {"task": "Facade & Roofing", "start": "2024-04-10", "finish": "2024-05-28"},
            {"task": "Finishing",        "start": "2024-05-15", "finish": "2024-06-28"},
        ],
    }
    out = generate_pdf_report(sample_data, "/home/claude/structuraai_report.pdf")
    print(f"Generated: {out}")