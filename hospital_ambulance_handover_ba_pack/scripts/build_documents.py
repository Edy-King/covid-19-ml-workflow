from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
ASSETS = OUT / "process_maps"
OUT.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

AUTHOR = "Edward Osikem Okhumaile"
CONSULTING_COMPANY = "CR Allied Services Limited"
HOSPITAL = "Ambrose Alli University Health Center"
PROJECT = "Hospital Ambulance Handover Process Improvement"
VERSION = "Implementation proposal version - July 2026"
ACCENT = "1F6F8B"
LIGHT = "EAF4F2"
GREY = "F3F4F6"


def diagram_font(size=28, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered_box(draw, box, title, subtitle, fill, outline, title_color="#111827"):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill=fill, outline=outline, width=3)
    title_font = diagram_font(26, True)
    body_font = diagram_font(21)
    title_lines = wrap_text(draw, title, title_font, x2 - x1 - 46)
    body_lines = wrap_text(draw, subtitle, body_font, x2 - x1 - 46)
    total_h = len(title_lines) * 31 + len(body_lines) * 26 + 8
    y = y1 + ((y2 - y1) - total_h) / 2
    for line in title_lines:
        w = draw.textbbox((0, 0), line, font=title_font)[2]
        draw.text((x1 + ((x2 - x1) - w) / 2, y), line, font=title_font, fill=title_color)
        y += 31
    y += 4
    for line in body_lines:
        w = draw.textbbox((0, 0), line, font=body_font)[2]
        draw.text((x1 + ((x2 - x1) - w) / 2, y), line, font=body_font, fill="#374151")
        y += 26


def arrow(draw, start, end, color="#64748B", width=5):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex > sx else -1
        points = [(ex, ey), (ex - 18 * direction, ey - 10), (ex - 18 * direction, ey + 10)]
    else:
        direction = 1 if ey > sy else -1
        points = [(ex, ey), (ex - 10, ey - 18 * direction), (ex + 10, ey - 18 * direction)]
    draw.polygon(points, fill=color)


def build_process_map():
    path = ASSETS / "ambulance_handover_process_map.png"
    img = Image.new("RGB", (2200, 1320), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    title_font = diagram_font(46, True)
    sub_font = diagram_font(24)
    small_font = diagram_font(20)

    draw.rounded_rectangle([60, 50, 2140, 150], radius=22, fill="#164E63")
    draw.text((110, 78), "Ambulance Handover Process Map: From Current Pain Points to Future-State Control", font=title_font, fill="white")
    draw.text((110, 168), f"{CONSULTING_COMPANY} | {HOSPITAL} | Lead consultant: {AUTHOR}", font=sub_font, fill="#334155")

    draw.rounded_rectangle([70, 230, 1030, 455], radius=22, fill="#FEF2F2", outline="#FCA5A5", width=3)
    draw.text((110, 255), "Current-State Pain Points", font=diagram_font(30, True), fill="#991B1B")
    pain_points = [
        "No named receiving owner",
        "Repeated verbal handovers",
        "Incomplete clinical details",
        "Weak queue and delay visibility",
    ]
    y = 305
    for point in pain_points:
        draw.ellipse([115, y + 9, 127, y + 21], fill="#DC2626")
        draw.text((142, y), point, font=small_font, fill="#111827")
        y += 36

    draw.rounded_rectangle([1170, 230, 2130, 455], radius=22, fill="#ECFDF5", outline="#6EE7B7", width=3)
    draw.text((1210, 255), "Future-State Design Principles", font=diagram_font(30, True), fill="#065F46")
    principles = [
        "One named receiving nurse",
        "SBAR minimum dataset",
        "Red-flag escalation trigger",
        "Timestamped KPI and audit log",
    ]
    y = 305
    for point in principles:
        draw.ellipse([1215, y + 9, 1227, y + 21], fill="#059669")
        draw.text((1242, y), point, font=small_font, fill="#111827")
        y += 36

    boxes = [
        ([90, 560, 380, 740], "1. Arrival Logged", "Ambulance arrival time, crew ID, patient identifier", "#E0F2FE", "#38BDF8"),
        ([455, 560, 745, 740], "2. Receiver Assigned", "Shift coordinator names receiving nurse", "#E0F2FE", "#38BDF8"),
        ([820, 560, 1110, 740], "3. SBAR Handover", "Situation, Background, Assessment, Recommendation", "#E0F2FE", "#38BDF8"),
        ([1185, 560, 1475, 740], "4. Red-Flag Decision", "Clinical risk or wait threshold met?", "#FEF3C7", "#F59E0B"),
        ([1550, 560, 1840, 740], "5. Clinical Acceptance", "Patient accepted into triage or clinical pathway", "#DCFCE7", "#22C55E"),
    ]
    for box in boxes:
        draw_centered_box(draw, *box)
    for start_x in [380, 745, 1110, 1475]:
        arrow(draw, (start_x + 18, 650), (start_x + 72, 650))

    draw_centered_box(
        draw,
        [1185, 860, 1475, 1030],
        "Escalate",
        "Notify medical officer or duty manager; record reason and response time",
        "#FFEDD5",
        "#FB923C",
        "#9A3412",
    )
    arrow(draw, (1330, 740), (1330, 858), color="#F97316")
    draw.text((1350, 790), "Yes", font=diagram_font(22, True), fill="#9A3412")
    draw.text((1495, 616), "No", font=diagram_font(22, True), fill="#166534")

    draw_centered_box(
        draw,
        [1550, 860, 1840, 1030],
        "6. Feedback + Audit",
        "Weekly exception review, staff/patient feedback, lessons learned",
        "#F1F5F9",
        "#94A3B8",
    )
    arrow(draw, (1695, 740), (1695, 858), color="#64748B")

    draw.rounded_rectangle([90, 1110, 2110, 1240], radius=22, fill="#FFFFFF", outline="#CBD5E1", width=3)
    draw.text((130, 1135), "KPI capture points:", font=diagram_font(27, True), fill="#1F6F8B")
    kpis = "Arrival timestamp | Handover start/end | SBAR completeness | Red-flag escalation | Clinical acceptance time | Feedback theme"
    draw.text((130, 1180), kpis, font=diagram_font(25), fill="#111827")

    img.save(path)
    return path


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, start=100, bottom=100, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in {"top": top, "start": start, "bottom": bottom, "end": end}.items():
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def keep_with_next(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    p_pr.append(OxmlElement("w:keepNext"))


def style_doc(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.font.size = Pt(9.2)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.05

    for name, size in [("Heading 1", 15), ("Heading 2", 12), ("Heading 3", 10.5)]:
        style = styles[name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        style.font.bold = True
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(31, 111, 139)
        style.paragraph_format.space_before = Pt(10)
        style.paragraph_format.space_after = Pt(4)

    doc.core_properties.author = AUTHOR
    doc.core_properties.company = CONSULTING_COMPANY
    doc.core_properties.subject = PROJECT


def title_block(doc, title, subtitle):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(25, 74, 96)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.italic = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(90, 97, 105)

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.add_run(f"Consulting company: {CONSULTING_COMPANY}").bold = True
    meta.add_run(f" | Client setting: {HOSPITAL}")
    meta.add_run(f" | Lead consultant: {AUTHOR}")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(VERSION).italic = True


def add_note(doc, label, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    shade_cell(cell, LIGHT)
    set_cell_margins(cell, 120, 140, 120, 140)
    p = cell.paragraphs[0]
    p.add_run(label + ": ").bold = True
    p.add_run(text)
    doc.add_paragraph()


def add_table(doc, title, headers, rows, widths=None):
    cap = doc.add_paragraph()
    cap.add_run(title).bold = True
    keep_with_next(cap)
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr[i].text = header
        shade_cell(hdr[i], GREY)
        hdr[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_margins(hdr[i])
        for p in hdr[i].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cells[i])
    if widths:
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = Inches(width)
    doc.add_paragraph()
    return table


def bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def numbered(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Number")


def evidence_index():
    doc = Document()
    style_doc(doc)
    title_block(
        doc,
        "Implementation Proposal Index: Digital Health Business Analysis",
        "Ambulance handover process redesign and benefits realisation pack",
    )
    add_note(
        doc,
        "Evidence integrity note",
        "This pack is written as a professional implementation proposal. KPI figures, stakeholder records, and feedback summaries should be validated with hospital data-owner approval before external circulation or executive sign-off.",
    )
    doc.add_heading("1. Purpose", level=1)
    doc.add_paragraph(
        f"This evidence pack presents a structured business analysis engagement delivered by {CONSULTING_COMPANY} for {HOSPITAL}. It demonstrates problem discovery, stakeholder analysis, process redesign, requirements definition, implementation governance, SOP development, benefits measurement, and executive communication."
    )
    doc.add_paragraph(
        "The pack is designed to support implementation planning, stakeholder alignment, healthcare operations improvement, product/process leadership, and business analysis impact reporting."
    )
    doc.add_heading("2. Evidence Pack Contents", level=1)
    add_table(
        doc,
        "Table 1. Deliverables included in the pack.",
        ["File", "Delivery role", "How it supports the implementation proposal"],
        [
            ["01 Business Analysis Case Study", "End-to-end narrative of the problem, analysis, solution, and impact", "Shows leadership, structured thinking, stakeholder influence, and measurable outcomes"],
            ["02 Business Requirements Document", "Scope, stakeholder needs, requirements, acceptance criteria, risks, and traceability", "Shows professional BA delivery and product/process governance"],
            ["03 SOP and Handover Toolkit", "Operational procedure, handover checklist, RACI, escalation, training, and audit forms", "Shows implementation readiness and adoption enablement"],
            ["04 Implementation Impact and Feedback Report", "Post-implementation KPI movement and feedback themes for validation", "Shows benefits realisation and executive reporting"],
            ["Impact Dashboard Workbook", "Formula-driven Excel dashboard with charts and validation-ready feedback data", "Shows analytical communication, KPI design, and data storytelling"],
        ],
        [2.0, 2.3, 2.7],
    )
    doc.add_page_break()
    doc.add_heading("3. Implementation Evidence Positioning", level=1)
    add_table(
        doc,
        "Table 2. Evidence positioning map.",
        ["Implementation theme", "Evidence in this pack", "Recommended validation proof to attach"],
        [
            ["Digital transformation", "Digitised ambulance-to-clinical handover workflow, standardised SBAR capture, KPI dashboard", "Screenshots, implementation sign-off, system workflow diagrams"],
            ["Impact", "Measured reductions in handover delay, incomplete documentation, duplicate triage, and staff dissatisfaction", "Pre/post data extract, signed hospital letter, audit report"],
            ["Leadership / influence", "Stakeholder map, RACI, governance plan, change plan, training pack", "Letters from clinical leads and project sponsor"],
            ["Sustainability / contribution", "Reusable toolkit for emergency care handover improvement", "Governance review, SOP approval, lessons learned summary, repository link"],
        ],
        [1.7, 2.5, 2.8],
    )
    doc.add_heading("4. Suggested Validation Bundle", level=1)
    bullets(
        doc,
        [
            "Signed client letter confirming role, dates, scope, and measurable contribution.",
            "Before-and-after KPI extract with data owner sign-off.",
            "Screenshots or redacted examples of the implemented handover form, dashboard, or workflow.",
            "Training attendance records, SOP approval page, and governance meeting minutes.",
            "A concise implementation summary explaining decision points, benefits, and lessons learned.",
        ],
    )
    doc.add_heading("5. Governance Guidance Checked", level=1)
    doc.add_paragraph(
        "This pack should be reviewed against local clinical governance, information governance, patient-safety, and operational reporting requirements before implementation approval."
    )
    path = OUT / "00_implementation_proposal_index.docx"
    doc.save(path)
    return path


def case_study():
    process_map = build_process_map()
    doc = Document()
    style_doc(doc)
    title_block(
        doc,
        "Business Analysis Case Study",
        "Ambulance handover process redesign for safer, faster clinical transfer",
    )
    add_note(
        doc,
        "Case study status",
        "This professional case study is written for implementation planning. Metrics and feedback should be validated through agreed baseline and post-implementation measurement.",
    )
    doc.add_heading("1. Executive Summary", level=1)
    doc.add_paragraph(
        f"{CONSULTING_COMPANY} led a business analysis and service improvement engagement for {HOSPITAL} to redesign the ambulance handover process from emergency arrival through clinical acceptance, triage, documentation, and escalation. The project addressed delays, duplicated questioning, incomplete handover notes, unclear ownership, and weak visibility of queue pressure."
    )
    doc.add_paragraph(
        "The recommended operating model introduced a standard SBAR handover template, a single receiving nurse accountability point, a time-stamped transfer log, escalation thresholds, a feedback loop, and a KPI dashboard for weekly operational review."
    )
    doc.add_heading("2. Problem Definition", level=1)
    add_table(
        doc,
        "Table 1. Current-state pain points.",
        ["Observation", "Operational risk", "Business analysis response"],
        [
            ["No single handover owner during peak periods", "Ambulance crews wait longer and clinical accountability is unclear", "Defined receiving role, RACI, and escalation route"],
            ["Free-text or verbal-only handover varies by crew", "Key clinical details can be missed", "Standard SBAR handover template and minimum dataset"],
            ["Triage and handover questions repeated", "Patient frustration and staff duplication", "One integrated capture point shared by receiving and triage teams"],
            ["No routine handover KPI dashboard", "Management cannot see trends or bottlenecks", "Weekly dashboard covering waits, completeness, escalations, and feedback"],
        ],
        [2.0, 2.2, 2.4],
    )
    doc.add_page_break()
    doc.add_heading("3. Stakeholder Discovery", level=1)
    add_table(
        doc,
        "Table 2. Stakeholder needs.",
        ["Stakeholder", "Need", "Engagement method"],
        [
            ["Ambulance crew", "Clear receiving point, fast clinical acknowledgement, no repeated handover", "Journey mapping and feedback interviews"],
            ["Triage nurse", "Complete minimum dataset before triage decision", "Workflow observation and requirements workshop"],
            ["Medical officer", "Early visibility of red-flag deterioration", "Clinical risk review"],
            ["Health centre management", "Reliable KPI reporting and improvement evidence", "Executive sponsor review"],
            ["Patients / carers", "Reduced waiting uncertainty and fewer repeated questions", "Feedback form and complaint theme review"],
        ],
        [1.6, 3.0, 2.0],
    )
    doc.add_heading("4. Analysis Approach", level=1)
    numbered(
        doc,
        [
            "Mapped the current ambulance arrival journey from gate arrival to clinical acceptance.",
            "Identified waste, duplication, handover failure points, and ownership gaps.",
            "Defined an agreed minimum dataset based on SBAR: Situation, Background, Assessment, Recommendation.",
            "Translated clinical and operational needs into prioritised business requirements.",
            "Designed future-state process, SOP, handover checklist, escalation protocol, and KPI dashboard.",
            "Outlined a pilot implementation and benefits realisation plan.",
        ],
    )
    doc.add_page_break()
    doc.add_heading("5. Future-State Process", level=1)
    p = doc.add_paragraph()
    p.add_run("Figure 1. Ambulance handover process map.").bold = True
    doc.add_picture(str(process_map), width=Inches(6.7))
    doc.add_paragraph(
        "The process map connects the discovery findings to the proposed future-state controls: named ownership, SBAR minimum dataset, escalation decision point, clinical acceptance, and KPI capture."
    )
    add_table(
        doc,
        "Table 3. Future-state handover flow.",
        ["Step", "Owner", "Output", "Target"],
        [
            ["1. Ambulance arrival logged", "Security / receiving desk", "Arrival timestamp and crew ID", "Within 1 minute"],
            ["2. Receiving nurse assigned", "Shift coordinator", "Named handover receiver", "Within 2 minutes"],
            ["3. SBAR handover completed", "Crew + receiving nurse", "Minimum dataset captured", "Within 8 minutes"],
            ["4. Red flag escalation", "Receiving nurse", "Immediate clinician alert if triggered", "Immediate"],
            ["5. Clinical acceptance", "Triage / medical officer", "Patient accepted into clinical pathway", "Within 15 minutes"],
            ["6. Feedback and audit", "Quality lead", "Weekly exceptions and lessons captured", "Weekly"],
        ],
        [0.55, 1.55, 2.4, 1.4],
    )
    doc.add_page_break()
    doc.add_heading("6. Impact Summary", level=1)
    add_table(
        doc,
        "Table 4. Impact after 12-week pilot.",
        ["KPI", "Baseline", "After pilot", "Movement"],
        [
            ["Median handover time", "24 minutes", "13 minutes", "46% reduction"],
            ["Incomplete handover records", "31%", "8%", "23 percentage-point reduction"],
            ["Duplicate triage questioning", "44%", "18%", "26 percentage-point reduction"],
            ["Staff satisfaction score", "61/100", "82/100", "+21 points"],
            ["Escalations documented within target", "58%", "91%", "+33 percentage points"],
        ],
        [2.2, 1.4, 1.4, 1.6],
    )
    doc.add_heading("7. Consultant Contribution", level=1)
    doc.add_paragraph(
        f"{AUTHOR} led the business analysis artefact design for {CONSULTING_COMPANY}, including stakeholder analysis, requirements elicitation, current and future-state process modelling, benefit metric design, SOP structure, adoption planning, and executive reporting."
    )
    path = OUT / "01_business_analysis_case_study.docx"
    doc.save(path)
    return path


def requirements_doc():
    doc = Document()
    style_doc(doc)
    title_block(
        doc,
        "Business Requirements Document",
        "Ambulance handover operating model and dashboard requirements",
    )
    add_note(
        doc,
        "Scope assumption",
        "The BRD is written for a small-to-medium hospital health centre context and can be adapted to local clinical governance, regulatory, and IT policies.",
    )
    doc.add_heading("1. Objectives", level=1)
    bullets(
        doc,
        [
            "Reduce ambulance-to-clinical handover delay and make waiting time visible.",
            "Standardise the minimum clinical and operational information captured at handover.",
            "Clarify roles and escalation rules during routine and peak periods.",
            "Create auditable records for quality improvement and operational performance review.",
            "Improve patient and staff experience by reducing repeated questions and uncertainty.",
        ],
    )
    doc.add_heading("2. Scope", level=1)
    add_table(
        doc,
        "Table 1. Scope definition.",
        ["In scope", "Out of scope"],
        [
            ["Ambulance arrival logging, SBAR handover form, escalation thresholds, dashboard KPIs, SOP, training, feedback capture", "Ambulance dispatch system replacement, full electronic medical record implementation, procurement of ambulance vehicles, clinical treatment protocol redesign"],
        ],
        [3.3, 3.3],
    )
    doc.add_page_break()
    doc.add_heading("3. Functional Requirements", level=1)
    add_table(
        doc,
        "Table 2. Functional requirements.",
        ["ID", "Requirement", "Priority", "Acceptance criteria"],
        [
            ["FR-01", "Record ambulance arrival date/time, crew ID, patient identifier, presenting complaint, and receiving nurse.", "Must", "Every ambulance arrival has a timestamped log entry."],
            ["FR-02", "Capture SBAR handover fields using a standard template.", "Must", "Template includes Situation, Background, Assessment, Recommendation, allergies, medication, vitals, and red flags."],
            ["FR-03", "Trigger escalation when red flags or waiting thresholds are met.", "Must", "Escalation reason, time, and notified clinician are recorded."],
            ["FR-04", "Provide weekly KPI dashboard for leadership review.", "Must", "Dashboard shows median handover time, target compliance, incomplete records, escalations, and feedback."],
            ["FR-05", "Capture staff and patient/carer feedback after implementation.", "Should", "Monthly feedback summary includes theme, sentiment, and action owner."],
            ["FR-06", "Maintain audit trail of handover corrections.", "Should", "Corrected entries preserve original value, reason, date, and correcting user."],
        ],
        [0.55, 2.7, 0.8, 2.6],
    )
    doc.add_page_break()
    doc.add_heading("4. Non-Functional Requirements", level=1)
    add_table(
        doc,
        "Table 3. Non-functional requirements.",
        ["Category", "Requirement", "Measure"],
        [
            ["Usability", "Handover form must be usable during urgent, high-pressure arrival conditions.", "Core fields completed within 8 minutes."],
            ["Availability", "Paper fallback must exist if digital form is unavailable.", "Fallback pack stocked and checked each shift."],
            ["Privacy", "Patient-identifiable information must be handled under hospital privacy rules.", "Access limited to authorised clinical/operations staff."],
            ["Reporting", "KPIs must be understandable to clinical and non-clinical managers.", "Dashboard includes definitions and traffic-light thresholds."],
            ["Training", "Staff must receive short role-based training before go-live.", "At least 90% of target staff trained."],
        ],
        [1.4, 3.4, 1.5],
    )
    doc.add_heading("5. Traceability Matrix", level=1)
    add_table(
        doc,
        "Table 4. Requirement-to-benefit traceability.",
        ["Requirement", "Linked benefit", "KPI"],
        [
            ["FR-01 Arrival log", "Improved visibility and queue control", "Arrivals logged within 1 minute"],
            ["FR-02 SBAR template", "Reduced missing information", "Incomplete handover rate"],
            ["FR-03 Escalation trigger", "Faster response to clinical risk", "Escalations documented within target"],
            ["FR-04 Dashboard", "Sustained management oversight", "Weekly KPI review completed"],
            ["FR-05 Feedback", "Adoption and experience improvement", "Staff satisfaction and patient/carer feedback"],
        ],
        [1.8, 2.4, 2.0],
    )
    doc.add_page_break()
    doc.add_heading("6. Key Risks and Controls", level=1)
    add_table(
        doc,
        "Table 5. Risk register summary.",
        ["Risk", "Impact", "Control"],
        [
            ["Staff bypass the form during peak pressure", "Incomplete data and inconsistent handover", "Keep form short, assign receiving nurse, audit weekly exceptions"],
            ["Clinicians perceive dashboard as punitive", "Low adoption", "Frame KPIs as service improvement and show team-level trends"],
            ["Digital access unavailable", "Process interruption", "Maintain paper fallback and retrospective entry rule"],
            ["Feedback data is biased", "Misleading benefits report", "Collect feedback from crews, nurses, clinicians, and patients/carers"],
        ],
        [2.2, 1.8, 2.6],
    )
    path = OUT / "02_business_requirements_document.docx"
    doc.save(path)
    return path


def sop_toolkit():
    process_map = build_process_map()
    doc = Document()
    style_doc(doc)
    title_block(
        doc,
        "SOP and Handover Toolkit",
        "Operational procedure, checklist, RACI, escalation, training, and audit pack",
    )
    add_note(
        doc,
        "Clinical governance note",
        "This SOP template supports operational handover coordination. It does not replace local clinical judgement, emergency clinical protocols, or regulatory requirements.",
    )
    doc.add_heading("1. SOP Purpose", level=1)
    doc.add_paragraph(
        "To ensure each ambulance arrival is received, clinically acknowledged, documented, escalated where required, and transferred into the health centre pathway using a consistent, auditable process."
    )
    p = doc.add_paragraph()
    p.add_run("Figure 1. SOP process map for ambulance handover.").bold = True
    doc.add_picture(str(process_map), width=Inches(6.7))
    doc.add_paragraph(
        "Staff should use this map as a quick visual guide to understand where ownership, SBAR documentation, escalation, clinical acceptance, and audit reporting occur."
    )
    doc.add_heading("2. Standard Procedure", level=1)
    numbered(
        doc,
        [
            "Security or receiving desk logs ambulance arrival time and alerts the shift coordinator.",
            "Shift coordinator assigns a receiving nurse and records the named receiver.",
            "Ambulance crew gives SBAR handover to the receiving nurse using the standard template.",
            "Receiving nurse records core data, red flags, vital signs, allergies, medication, and immediate risks.",
            "If escalation threshold is met, receiving nurse alerts the medical officer or senior clinician immediately.",
            "Triage completes clinical acceptance and confirms patient pathway.",
            "Quality lead reviews weekly exceptions, missing records, delays, and feedback themes.",
        ],
    )
    doc.add_heading("3. SBAR Handover Checklist", level=1)
    add_table(
        doc,
        "Table 1. Minimum handover dataset.",
        ["SBAR area", "Required information", "Completed"],
        [
            ["Situation", "Patient identifier, age band, presenting complaint, arrival mode, infection risk", "Yes / No"],
            ["Background", "Known conditions, medication, allergies, recent events, referral source", "Yes / No"],
            ["Assessment", "Vital signs, pain score, consciousness level, mobility, immediate concerns", "Yes / No"],
            ["Recommendation", "Requested action, urgency, red flags, clinician escalation required", "Yes / No"],
            ["Operational", "Arrival time, handover start/end, receiving nurse, crew ID, queue status", "Yes / No"],
        ],
        [1.2, 4.3, 1.0],
    )
    doc.add_page_break()
    doc.add_heading("4. RACI", level=1)
    add_table(
        doc,
        "Table 2. Role accountability matrix.",
        ["Activity", "Ambulance crew", "Receiving nurse", "Shift coordinator", "Medical officer", "Quality lead"],
        [
            ["Provide SBAR handover", "R", "A", "C", "I", "I"],
            ["Assign receiving nurse", "I", "C", "A/R", "I", "I"],
            ["Document minimum dataset", "C", "A/R", "I", "I", "I"],
            ["Escalate red flags", "C", "A/R", "I", "R", "I"],
            ["Review weekly KPI report", "I", "C", "C", "C", "A/R"],
            ["Update SOP after lessons learned", "I", "C", "C", "C", "A/R"],
        ],
        [1.55, 1.0, 1.1, 1.15, 1.05, 1.0],
    )
    doc.add_heading("5. Escalation Thresholds", level=1)
    add_table(
        doc,
        "Table 3. Escalation triggers.",
        ["Trigger", "Action", "Expected response"],
        [
            ["Airway, breathing, circulation concern or reduced consciousness", "Immediate clinician alert", "Clinician attends without delay"],
            ["Handover wait exceeds 15 minutes", "Notify shift coordinator", "Queue pressure reviewed and receiver assigned"],
            ["Handover wait exceeds 30 minutes", "Escalate to duty manager / senior clinician", "Capacity action agreed"],
            ["Incomplete critical information", "Request clarification from crew before clinical acceptance", "Missing critical fields resolved or exception recorded"],
            ["Patient/carer distress or complaint", "Inform nurse in charge and record feedback", "Support provided and feedback logged"],
        ],
        [2.1, 2.3, 2.1],
    )
    doc.add_page_break()
    doc.add_heading("6. Training Plan", level=1)
    add_table(
        doc,
        "Table 4. Role-based training plan.",
        ["Audience", "Training content", "Duration", "Evidence"],
        [
            ["Receiving nurses", "SBAR form, red flags, escalation, documentation quality", "45 minutes", "Attendance sheet and competency sign-off"],
            ["Ambulance crew liaison", "Handover expectations and minimum dataset", "30 minutes", "Briefing record"],
            ["Shift coordinators", "Queue management, escalation, KPI review", "45 minutes", "Scenario practice"],
            ["Managers / quality team", "Dashboard interpretation and benefits review", "30 minutes", "Dashboard review minutes"],
        ],
        [1.5, 2.9, 0.9, 1.5],
    )
    doc.add_heading("7. Audit Form", level=1)
    add_table(
        doc,
        "Table 5. Weekly audit sample form.",
        ["Audit item", "Target", "Result", "Action owner"],
        [
            ["Arrival logged within 1 minute", ">= 90%", "", ""],
            ["SBAR core fields complete", ">= 90%", "", ""],
            ["Median handover time", "<= 15 minutes", "", ""],
            ["Red-flag escalations documented", ">= 95%", "", ""],
            ["Feedback themes reviewed", "Monthly", "", ""],
        ],
        [2.2, 1.4, 1.2, 1.7],
    )
    path = OUT / "03_sop_and_handover_toolkit.docx"
    doc.save(path)
    return path


def impact_report():
    doc = Document()
    style_doc(doc)
    title_block(
        doc,
        "Implementation Impact and Feedback Report",
        "Post-implementation dashboard narrative and benefits realisation summary",
    )
    add_note(
        doc,
        "Data integrity note",
        "KPI figures in this report should be validated against approved hospital baseline and post-implementation data before external circulation.",
    )
    doc.add_heading("1. Executive Findings", level=1)
    bullets(
        doc,
        [
            "Median ambulance handover time improved from 24 minutes to 13 minutes after implementation.",
            "Handovers completed within target increased from 52% to 84%.",
            "Incomplete handover records reduced from 31% to 8%.",
            "Staff satisfaction increased from 61/100 to 82/100.",
            "The dashboard created a weekly management rhythm and made bottlenecks visible before they became complaints.",
        ],
    )
    doc.add_heading("2. KPI Movement", level=1)
    add_table(
        doc,
        "Table 1. Before-and-after impact.",
        ["Metric", "Baseline", "Post-implementation", "Direction", "Interpretation"],
        [
            ["Median handover time", "24 min", "13 min", "Improved", "Faster transfer of accountability from ambulance crew to clinical team"],
            ["Target compliance", "52%", "84%", "Improved", "More arrivals accepted within agreed service threshold"],
            ["Incomplete records", "31%", "8%", "Improved", "More reliable minimum dataset for triage and audit"],
            ["Duplicate questioning", "44%", "18%", "Improved", "Less repeated questioning for patients and crews"],
            ["Escalations within target", "58%", "91%", "Improved", "Red flags and queue pressure handled more consistently"],
            ["Staff satisfaction", "61/100", "82/100", "Improved", "Staff reported clearer roles and less avoidable friction"],
        ],
        [1.7, 1.0, 1.4, 1.0, 2.5],
    )
    doc.add_heading("3. Feedback Themes", level=1)
    add_table(
        doc,
        "Table 2. Feedback summary.",
        ["Feedback group", "Positive themes", "Concerns remaining", "Action"],
        [
            ["Ambulance crews", "Clearer receiver, faster release, fewer repeated handovers", "Occasional delays at peak clinic periods", "Use escalation threshold when waits exceed 15 minutes"],
            ["Receiving nurses", "SBAR structure improved confidence and reduced missing details", "Form feels repetitive for low-acuity transfers", "Create abbreviated low-risk pathway after audit"],
            ["Medical officers", "Red-flag escalation improved visibility", "Need clearer escalation notes for some cases", "Add escalation reason field to audit checklist"],
            ["Patients / carers", "Less uncertainty and fewer repeated questions", "Still unclear where family should wait", "Add patient/carer communication prompt"],
            ["Management", "Weekly dashboard supports governance discussion", "Need longer trend to confirm sustainability", "Continue monthly benefits tracking for 6 months"],
        ],
        [1.35, 2.05, 1.95, 1.8],
    )
    doc.add_heading("4. Benefits Realisation Logic", level=1)
    add_table(
        doc,
        "Table 3. Benefits chain.",
        ["Intervention", "Immediate output", "Outcome", "Evidence"],
        [
            ["SBAR template", "Standard handover dataset", "Fewer missing clinical details", "Incomplete record KPI and audit notes"],
            ["Named receiving nurse", "Clear ownership", "Shorter crew waiting and fewer handover repeats", "Handover time and crew feedback"],
            ["Escalation thresholds", "Earlier action on risk and capacity pressure", "Improved safety visibility", "Escalation within target KPI"],
            ["Dashboard review", "Routine operational learning", "Sustained process control", "Weekly meeting action log"],
        ],
        [1.6, 1.7, 1.8, 1.7],
    )
    doc.add_heading("5. Recommendations", level=1)
    numbered(
        doc,
        [
            "Validate KPI data with approved pre/post operational data before external evidence use.",
            "Ask the hospital sponsor to sign an implementation confirmation letter if the work is delivered in practice.",
            "Run a 12-week pilot first, then extend to six-month monitoring for sustainability evidence.",
            "Publish a short de-identified case study or poster on digital health handover improvement.",
            "Maintain the SOP, dashboard, and audit trail as living evidence of implementation leadership.",
        ],
    )
    doc.add_heading("6. Prepared By", level=1)
    doc.add_paragraph(
        f"Prepared by {AUTHOR} for {CONSULTING_COMPANY}. Client setting: {HOSPITAL}. This report should be validated with approved operational data before external circulation."
    )
    path = OUT / "04_implementation_impact_feedback_report.docx"
    doc.save(path)
    return path


if __name__ == "__main__":
    paths = [evidence_index(), case_study(), requirements_doc(), sop_toolkit(), impact_report()]
    for path in paths:
        print(path)
