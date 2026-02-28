# core/exports/pdf_report.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(project_data, output_path="project_report.pdf"):

    doc = SimpleDocTemplate(output_path)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("StructuraAI Project Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    for section, content in project_data.items():
        elements.append(Paragraph(f"<b>{section}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        if isinstance(content, dict):
            table_data = [["Key", "Value"]]
            for k, v in content.items():
                table_data.append([str(k), str(v)])

            table = Table(table_data)
            elements.append(table)

        elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)

    return output_path