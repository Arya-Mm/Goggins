from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

import matplotlib.pyplot as plt
import tempfile
import os


def generate_chart_image(fig_func):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig_func()
    plt.savefig(tmp.name, bbox_inches="tight", dpi=200)
    plt.close()
    return tmp.name


def generate_pdf_report(data, filename="structuraai_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # ─────────────────────────────────────────
    # LOGO HEADER
    # ─────────────────────────────────────────
    try:
        logo = Image("core/assets/structura_logo.png", width=1.5 * inch, height=0.6 * inch)
        elements.append(logo)
    except:
        pass

    elements.append(Spacer(1, 0.3 * inch))

    # ─────────────────────────────────────────
    # EXECUTIVE SUMMARY PAGE
    # ─────────────────────────────────────────
    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    risk = data.get("Risk Summary", {})
    build = data.get("Buildability Summary", {})

    risk_level = risk.get("risk_level", "Unknown")

    # Risk Badge Color
    if risk_level.lower() == "high":
        badge_color = colors.red
    elif risk_level.lower() == "medium":
        badge_color = colors.orange
    else:
        badge_color = colors.green

    badge = Table(
        [[f"RISK LEVEL: {risk_level.upper()}"]],
        colWidths=[4 * inch]
    )
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), badge_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('INNERPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(badge)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        f"Buildability Score: <b>{build.get('final_score')}</b>",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Total Risk Score: <b>{risk.get('risk_score')}</b>",
        styles["Normal"]
    ))

    elements.append(PageBreak())

    # ─────────────────────────────────────────
    # QUANTITY & COST
    # ─────────────────────────────────────────
    elements.append(Paragraph("<b>Material Quantities</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    q = data.get("Material Quantities", {})
    if q:
        table_data = [["Item", "Value"]]
        for k, v in q.items():
            table_data.append([k, str(v)])

        table = Table(table_data, colWidths=[3 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("<b>Cost Breakdown</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    cost = data.get("Cost Breakdown", {})
    if cost:
        table_data = [["Component", "₹"]]
        for k, v in cost.items():
            table_data.append([k, f"{v:,.2f}"])

        table = Table(table_data, colWidths=[3 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))

        elements.append(table)

    elements.append(PageBreak())

    # ─────────────────────────────────────────
    # RISK CHART
    # ─────────────────────────────────────────
    def risk_chart():
        phases = [x["phase"] for x in risk.get("breakdown", {}).items()]
        values = list(risk.get("breakdown", {}).values())
        plt.bar(phases, values)
        plt.title("Risk Breakdown")
        plt.xticks(rotation=45)

    chart_path = generate_chart_image(risk_chart)
    elements.append(Paragraph("<b>Risk Breakdown Chart</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(chart_path, width=6 * inch, height=3 * inch))

    elements.append(PageBreak())

    # ─────────────────────────────────────────
    # GANTT CHART
    # ─────────────────────────────────────────
    if "gantt_path" in data:
        elements.append(Paragraph("<b>Project Gantt Chart</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Image(data["gantt_path"], width=6 * inch, height=3.5 * inch))

    doc.build(elements)

    return filename