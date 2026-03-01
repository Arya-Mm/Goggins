# core/exports/pdf_report.py

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime


def generate_pdf_report(data, filename="structuraai_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    # =====================================================
    # SAFE EXTRACTION
    # =====================================================

    quantities = data.get("Material Quantities", {}) or {}
    cost_data = data.get("Cost Breakdown", {}) or {}
    risk_data = data.get("Risk Summary", {}) or {}
    build_data = data.get("Buildability Summary", {}) or {}
    schedule_data = data.get("Schedule Summary", {}) or {}

    base_cost = float(cost_data.get("total_project_cost", 0) or 0)

    # =====================================================
    # COVER PAGE
    # =====================================================

    elements.append(Paragraph("<b>STRUCTURAAI PROJECT REPORT</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        f"Risk Score: {risk_data.get('risk_score', 0)}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Buildability Score: {build_data.get('final_score', 0)}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Total Duration: {schedule_data.get('Total Duration', 0)} days",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Total Project Cost: ₹{base_cost:,.0f}",
        styles["Normal"]
    ))

    elements.append(PageBreak())

    # =====================================================
    # COST BREAKDOWN (SAFE)
    # =====================================================

    elements.append(Paragraph("<b>Cost Breakdown</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    breakdown = cost_data.get("cost_breakdown", {}) \
        or cost_data.get("breakdown", {}) \
        or {}

    cost_rows = [["Category", "Amount (₹)", "Percentage"]]

    if breakdown:
        for k, v in breakdown.items():

            try:
                amount = float(v)
            except Exception:
                amount = 0

            if base_cost > 0:
                percent = (amount / base_cost) * 100
            else:
                percent = 0

            cost_rows.append([
                str(k),
                f"₹{amount:,.0f}",
                f"{percent:.1f}%"
            ])
    else:
        cost_rows.append(["No cost data available", "-", "-"])

    total_percent = "100.0%" if base_cost > 0 else "0.0%"

    cost_rows.append([
        "TOTAL",
        f"₹{base_cost:,.0f}",
        total_percent
    ])

    cost_table = Table(cost_rows, colWidths=[2.5*inch, 2*inch, 1.5*inch])

    cost_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(cost_table)

    elements.append(PageBreak())

    # =====================================================
    # MATERIAL QUANTITIES
    # =====================================================

    elements.append(Paragraph("<b>Material Quantities</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    quantity_rows = [["Material", "Quantity"]]

    if quantities:
        for k, v in quantities.items():
            quantity_rows.append([str(k), str(v)])
    else:
        quantity_rows.append(["No quantity data available", "-"])

    quantity_table = Table(quantity_rows, colWidths=[3*inch, 2*inch])

    quantity_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(quantity_table)

    elements.append(PageBreak())

    # =====================================================
    # SCHEDULE SUMMARY
    # =====================================================

    elements.append(Paragraph("<b>Execution Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"Critical Path: {schedule_data.get('Critical Path', [])}",
        styles["Normal"]
    ))

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(elements)

    return filename