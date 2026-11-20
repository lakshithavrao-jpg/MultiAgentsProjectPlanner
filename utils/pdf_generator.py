from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)


def generate_pdf(project, results):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "NexusTitle",
        parent=styles["Title"],
        fontSize=25,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6D28D9"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "NexusHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4F46E5"),
        spaceBefore=15,
        spaceAfter=10
    )

    body_style = styles["BodyText"]

    story = []

    story.append(
        Paragraph("NEXUS", title_style)
    )

    story.append(
        Paragraph(
            escape(project["name"]),
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            "Agentic AI Project Proposal",
            styles["Italic"]
        )
    )

    story.append(Spacer(1, 25))

    sections = [
        ("Project Requirements", results.get("requirements", "")),
        ("Software Architecture", results.get("architecture", "")),
        ("Project Management Plan", results.get("project_plan", "")),
        ("Final Project Proposal", results.get("proposal", ""))
    ]

    for heading, content in sections:

        story.append(
            Paragraph(escape(heading), heading_style)
        )

        for line in str(content).splitlines():

            line = line.strip()

            if not line:
                story.append(Spacer(1, 5))
                continue

            safe_line = escape(line)

            story.append(
                Paragraph(safe_line, body_style)
            )

            story.append(Spacer(1, 5))

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()