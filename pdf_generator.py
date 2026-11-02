import io
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def clean_for_pdf(text: str) -> str:
    """Escapes XML entities so reportlab Paragraph won't crash on <, >, &."""
    if not text:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert newlines to breaks
    text = text.replace("\n", "<br/>")
    return text

def generate_petition_pdf(
    category_title: str,
    draft_text: str,
    user_name: str = "",
    state: str = "",
    laws: list = None,
    evidence: list = None,
    resources: list = None,
    language: str = "English",
) -> bytes:
    """
    Generates an official, court-ready PDF legal petition and evidence dossier
    formatted on A4 with judicial styling, statutory citations, and signature blocks.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom Judicial Color Palette
    NAVY = colors.HexColor("#0A192F")
    GOLD = colors.HexColor("#C5A059")
    CHARCOAL = colors.HexColor("#2D3748")
    LIGHT_BG = colors.HexColor("#F8F9FA")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "JudicialTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        alignment=1,  # Center
    )

    subtitle_style = ParagraphStyle(
        "JudicialSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=GOLD,
        alignment=1,
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "JudicialBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=CHARCOAL,
    )

    body_bold = ParagraphStyle(
        "JudicialBodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=NAVY,
    )

    draft_box_style = ParagraphStyle(
        "DraftStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=CHARCOAL,
    )

    disclaimer_style = ParagraphStyle(
        "DisclaimerStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#718096"),
        alignment=1,
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("NYAYAMITRA AI | FORMAL CIVIC LEGAL PETITION", title_style))
    story.append(Paragraph("VERIFIED LEGAL AID DOSSIER & COMPLAINT RECORD", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=8, spaceBefore=2))

    # 2. Case Metadata Table
    today_str = datetime.now().strftime("%d-%B-%Y, %I:%M %p IST")
    meta_data = [
        [
            Paragraph("<b>Subject / Category:</b>", body_style),
            Paragraph(clean_for_pdf(category_title or "Civic Legal Dispute"), body_bold),
            Paragraph("<b>Date of Record:</b>", body_style),
            Paragraph(clean_for_pdf(today_str), body_style),
        ],
        [
            Paragraph("<b>Complainant / Citizen:</b>", body_style),
            Paragraph(clean_for_pdf(user_name or "Aggrieved Citizen"), body_bold),
            Paragraph("<b>State / Jurisdiction:</b>", body_style),
            Paragraph(clean_for_pdf(state or "National Jurisdiction / Pan-India"), body_style),
        ],
    ]

    meta_table = Table(meta_data, colWidths=[1.5 * inch, 2.3 * inch, 1.4 * inch, 2.1 * inch])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Applicable Statutory Provisions (if provided)
    if laws:
        story.append(Paragraph("I. APPLICABLE STATUTORY CITATIONS & LEGISLATION", section_heading))
        law_items = []
        for law in laws[:4]:
            law_items.append(Paragraph(f"• <b>{clean_for_pdf(law)}</b>", body_style))
        for item in law_items:
            story.append(item)
        story.append(Spacer(1, 8))

    # 4. Official Petition / Complaint Draft
    story.append(Paragraph("II. FORMAL COMPLAINT / GRIEVANCE PETITION", section_heading))
    
    # Process draft text cleanly
    cleaned_draft = clean_for_pdf(draft_text.strip())
    draft_table = Table([[Paragraph(cleaned_draft, draft_box_style)]], colWidths=[7.3 * inch])
    draft_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FCFCFC")),
                ("BOX", (0, 0), (-1, -1), 0.75, BORDER_COLOR),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(draft_table)
    story.append(Spacer(1, 10))

    # 5. Evidence Checklist (if provided)
    if evidence:
        story.append(Paragraph("III. PRESCRIBED EVIDENCE & ATTACHMENT CHECKLIST", section_heading))
        ev_data = []
        for ev in evidence:
            ev_data.append([
                Paragraph("[  ]", body_bold),
                Paragraph(clean_for_pdf(ev), body_style),
            ])
        ev_table = Table(ev_data, colWidths=[0.3 * inch, 7.0 * inch])
        ev_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        story.append(ev_table)
        story.append(Spacer(1, 8))

    # 6. Verification and Signature Block
    sig_block = [
        [
            Paragraph("<b>VERIFICATION & SIGNATURE:</b><br/>"
                      "I hereby declare that the facts stated above are true to the best of my knowledge, information, and belief.<br/><br/>"
                      "Place: ___________________________<br/>"
                      "Date: ____________________________", body_style),
            Paragraph("<br/><br/>_____________________________________<br/>"
                      "<b>Signature / Thumb Impression of Complainant</b><br/>"
                      f"Name: {clean_for_pdf(user_name or 'Aggrieved Citizen')}", body_style)
        ]
    ]
    sig_table = Table(sig_block, colWidths=[4.0 * inch, 3.3 * inch])
    sig_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(KeepTogether(sig_table))
    story.append(Spacer(1, 10))

    # 7. Official Resources and Statutory Helplines
    if resources:
        res_text = " | ".join([f"{r.get('name', '')}: {r.get('contact', '')}" for r in resources if r.get('contact')])
        if res_text:
            story.append(Paragraph(f"<b>Key Statutory Helplines:</b> {clean_for_pdf(res_text)}", body_style))
            story.append(Spacer(1, 4))

    # 8. Disclaimer Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=4, spaceBefore=4))
    story.append(
        Paragraph(
            "<b>Statutory Notice:</b> NyayaMitra AI provides structured procedural guidance and civic petition drafts based on verified Indian laws (BNS 2023, CPA 2019, RTI Act 2005). This document does not constitute an advocate-client relationship. For free legal aid, dial National Legal Services Authority (NALSA) Helpline 15100 or Tele-Law 14488.",
            disclaimer_style,
        )
    )

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

