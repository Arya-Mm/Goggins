from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os


def generate_pdf_report(data, filename="structuraai_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # ─────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────
    elements.append(Paragraph("<b>StructuraAI — Project Intelligence Report</b>", title_style))
    elements.append(Spacer(1, 0.25 * inch))

    # ─────────────────────────────────────────
    # BASIC SUMMARY
    # ─────────────────────────────────────────
    risk = data.get("Risk Summary", {})
    build = data.get("Buildability Summary", {})
    cost_data = data.get("Cost Breakdown", {})
    quantities = data.get("Material Quantities", {})

    elements.append(Paragraph(f"Overall Risk Score: {risk.get('risk_score', 0)}", normal_style))
    elements.append(Paragraph(f"Buildability Score: {build.get('final_score', 0)}", normal_style))
    elements.append(Paragraph(f"Estimated Total Cost: ₹{cost_data.get('total_project_cost', 0):,.0f}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # ─────────────────────────────────────────
    # MONTE CARLO SIMULATION
    # ─────────────────────────────────────────
    base_cost = cost_data.get("total_project_cost", 1000000)
    risk_score = risk.get("risk_score", 40)

    simulations = np.random.normal(
        base_cost,
        base_cost * (risk_score / 100),
        1000
    )

    def monte_chart():
        plt.hist(simulations, bins=35)
        plt.title("Cost Risk Simulation")
        plt.xlabel("Projected Cost")
        plt.ylabel("Probability")

    tmp1 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    monte_chart()
    plt.savefig(tmp1.name, dpi=200, bbox_inches="tight")
    plt.close()

    elements.append(Paragraph("<b>Cost Risk Simulation (Monte Carlo)</b>", subtitle_style))
    elements.append(Image(tmp1.name, width=5.5 * inch, height=2.5 * inch))
    elements.append(Spacer(1, 0.3 * inch))

    # ─────────────────────────────────────────
    # CASHFLOW CURVE
    # ─────────────────────────────────────────
    months = np.arange(1, 13)
    cashflow = np.cumsum(np.linspace(base_cost/12, base_cost/8, 12))

    def cashflow_chart():
        plt.plot(months, cashflow)
        plt.title("Projected Cashflow")
        plt.xlabel("Month")
        plt.ylabel("Cumulative Spend")

    tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    cashflow_chart()
    plt.savefig(tmp2.name, dpi=200, bbox_inches="tight")
    plt.close()

    elements.append(Paragraph("<b>Projected Cashflow</b>", subtitle_style))
    elements.append(Image(tmp2.name, width=5.5 * inch, height=2.5 * inch))
    elements.append(Spacer(1, 0.3 * inch))

    # ─────────────────────────────────────────
    # IRR / NPV
    # ─────────────────────────────────────────
    discount_rate = 0.1
    projected_return = base_cost * 1.25

    npv = projected_return / (1 + discount_rate) - base_cost
    irr = (projected_return / base_cost) - 1

    finance_table = [
        ["Metric", "Value"],
        ["NPV (10% discount rate)", f"₹{npv:,.0f}"],
        ["Internal Rate of Return (IRR)", f"{irr*100:.2f}%"],
    ]

    table = Table(finance_table, colWidths=[3 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))

    elements.append(Paragraph("<b>Financial Snapshot</b>", subtitle_style))
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # ─────────────────────────────────────────
    # RESOURCE HEATMAP
    # ─────────────────────────────────────────
    resource_vals = list(quantities.values()) if quantities else np.random.rand(5)

    def heatmap_chart():
        plt.imshow([resource_vals], aspect="auto")
        plt.title("Resource Utilization")
        plt.yticks([])
        plt.colorbar()

    tmp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    heatmap_chart()
    plt.savefig(tmp3.name, dpi=200, bbox_inches="tight")
    plt.close()

    elements.append(Paragraph("<b>Resource Utilization</b>", subtitle_style))
    elements.append(Image(tmp3.name, width=5.5 * inch, height=1.5 * inch))

    doc.build(elements)

    for tmp in [tmp1.name, tmp2.name, tmp3.name]:
        try:
            os.remove(tmp)
        except:
            pass

    return filename