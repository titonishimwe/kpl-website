"""PDF reports built with ReportLab."""
from collections import Counter
from io import BytesIO
from xml.sax.saxutils import escape

from django.conf import settings
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

INK = colors.HexColor("#0B1412")
ACCENT = colors.HexColor("#37675C")
MINT = colors.HexColor("#6DCDB8")
MUTED = colors.HexColor("#6C757D")
LINE = colors.HexColor("#DEE2E6")
ZEBRA = colors.HexColor("#F6F8F7")
STATUS_COLORS = {
    "pending": colors.HexColor("#B7791F"),
    "approved": colors.HexColor("#1F7A3E"),
    "confirmed": colors.HexColor("#1F7A3E"),
    "rejected": colors.HexColor("#8B1E1E"),
    "cancelled": MUTED,
}

LOGO = settings.BASE_DIR / "static" / "images" / "logos" / "logo.png"

_styles = getSampleStyleSheet()
TITLE = ParagraphStyle("t", parent=_styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22,
                       textColor=INK, alignment=0, spaceAfter=2)
SUB = ParagraphStyle("s", parent=_styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED)
H2 = ParagraphStyle("h2", parent=_styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14,
                    textColor=ACCENT, spaceBefore=10, spaceAfter=6)
CELL = ParagraphStyle("c", parent=_styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=INK)
CELL_B = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
HEAD = ParagraphStyle("hd", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)
RIGHT = ParagraphStyle("r", parent=SUB, alignment=TA_RIGHT)


def _p(text, style=CELL):
    # ReportLab's built-in fonts cover Latin-1; replace anything else instead of failing.
    text = str(text if text not in (None, "") else "—")
    text = text.encode("latin-1", "replace").decode("latin-1")
    return Paragraph(escape(text), style)


class _NumberedCanvas(rl_canvas.Canvas):
    """Adds 'Page X of Y' and the footer once the total page count is known."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            w, _ = self._pagesize
            self.setStrokeColor(LINE)
            self.line(15 * mm, 12 * mm, w - 15 * mm, 12 * mm)
            self.setFont("Helvetica", 7.5)
            self.setFillColor(MUTED)
            self.drawString(15 * mm, 8 * mm, "Kigali Public Library · Confidential: contains personal data")
            self.drawRightString(w - 15 * mm, 8 * mm, f"Page {self._pageNumber} of {total}")
            super().showPage()
        super().save()


def _header(title, subtitle_lines, width):
    logo = Image(str(LOGO), width=24 * mm, height=24 * mm * 703 / 967) if LOGO.exists() else Spacer(1, 1)
    text = [Paragraph(escape(title), TITLE)] + [Paragraph(escape(line), SUB) for line in subtitle_lines]
    t = Table([[text, logo]], colWidths=[width - 30 * mm, 30 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, 0), 2, MINT),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [t, Spacer(1, 8)]


def _summary_tiles(pairs, width):
    """A row of 'big number + label' tiles."""
    tile = ParagraphStyle("tile", parent=CELL, leading=19)
    cells = [[Paragraph(f'<font size="16"><b>{value}</b></font><br/><font color="#6C757D">{escape(label)}</font>', tile)
              for label, value in pairs]]
    t = Table(cells, colWidths=[width / len(pairs)] * len(pairs))
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (-1, -1), ZEBRA),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def _data_table(header, rows, col_widths, status_col=None):
    data = [[_p(h, HEAD) for h in header]] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(style))
    return t


def _status_cell(obj):
    color = STATUS_COLORS.get(obj.status, MUTED).hexval()[2:]
    return Paragraph(f'<font color="#{color}"><b>{escape(obj.get_status_display())}</b></font>', CELL)


def _build(story, pagesize):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=pagesize, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=14 * mm, bottomMargin=18 * mm,
                            title="Kigali Public Library report", author="Kigali Public Library")
    doc.build(story, canvasmaker=_NumberedCanvas)
    return buf.getvalue()


def _generated_line(user):
    who = (user.get_full_name() or user.username) if user else "system"
    return f"Generated {timezone.localtime():%d %B %Y at %H:%M} by {who}"


def membership_report(applications, filter_summary, user):
    """Landscape table of membership applications, with status and category totals."""
    applications = list(applications)
    width = landscape(A4)[0] - 30 * mm
    story = _header(
        "Membership Applications Report",
        [filter_summary, _generated_line(user)],
        width,
    )

    by_status = Counter(a.status for a in applications)
    story.append(_summary_tiles([
        ("Applications", len(applications)),
        ("Pending", by_status.get("pending", 0)),
        ("Approved", by_status.get("approved", 0)),
        ("Rejected", by_status.get("rejected", 0)),
    ], width))

    by_type = Counter(a.get_membership_type_display() for a in applications)
    if by_type:
        story.append(Paragraph("By membership category", H2))
        rows = [[_p(k), _p(v)] for k, v in by_type.most_common()]
        story.append(_data_table(["Category", "Applications"], rows, [width * 0.6, width * 0.4]))

    story.append(Paragraph("Applications", H2))
    if not applications:
        story.append(Paragraph("No applications match these filters.", SUB))
    else:
        rows = []
        for i, a in enumerate(applications, 1):
            rows.append([
                _p(i), _p(f"{a.first_name} {a.last_name}", CELL_B), _p(a.get_membership_type_display()),
                _p(a.phone), _p(a.email), _p(a.district), _p(a.get_payment_method_display().split(" (")[0]),
                _p(timezone.localtime(a.created_at).strftime("%d %b %Y")), _status_cell(a),
            ])
        story.append(_data_table(
            ["#", "Applicant", "Membership", "Phone", "Email", "District", "Payment", "Submitted", "Status"],
            rows,
            [w * width for w in (0.04, 0.15, 0.19, 0.11, 0.17, 0.09, 0.08, 0.09, 0.08)],
        ))
    return _build(story, landscape(A4))


def application_detail_pdf(app, user):
    """One application on a printable A4 page, with signature lines for card issuance."""
    width = A4[0] - 30 * mm
    story = _header(
        "Membership Card Application",
        [f"Application #{app.pk} · submitted {timezone.localtime(app.created_at):%d %B %Y}", _generated_line(user)],
        width,
    )

    def section(title, pairs):
        rows = [[_p(label, CELL_B), _p(value)] for label, value in pairs]
        t = Table(rows, colWidths=[width * 0.32, width * 0.68])
        t.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
            ("BACKGROUND", (0, 0), (0, -1), ZEBRA),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return KeepTogether([Paragraph(title, H2), t])

    story.append(section("Applicant", [
        ("Full name", f"{app.first_name} {app.last_name}"),
        ("Date of birth", app.dob.strftime("%d %B %Y")),
        ("Gender", app.get_gender_display()),
        ("National ID / Passport", app.id_passport),
    ]))
    story.append(section("Contact", [
        ("Phone", app.phone), ("Alternative phone", app.alt_phone),
        ("Email", app.email), ("Alternative email", app.alt_email),
    ]))
    story.append(section("Address", [
        ("Village", app.village), ("Sector", app.sector), ("District", app.district), ("Province", app.province),
    ]))
    if app.guardian_name:
        story.append(section("Parent / guardian", [
            ("Name", app.guardian_name), ("Relationship", app.guardian_relationship),
            ("ID", app.guardian_id), ("Phone", app.guardian_phone),
        ]))
    reviewer = app.reviewed_by.get_full_name() or app.reviewed_by.username if app.reviewed_by else ""
    story.append(section("Membership", [
        ("Membership type", app.get_membership_type_display()),
        ("Payment method", app.get_payment_method_display()),
        ("Supporting document", "Attached (see dashboard)" if app.document else "None"),
        ("Status", app.get_status_display()),
        ("Reviewed by", reviewer),
        ("Reviewed on", timezone.localtime(app.reviewed_at).strftime("%d %B %Y") if app.reviewed_at else ""),
        ("Staff notes", app.staff_notes),
    ]))

    story.append(Spacer(1, 18))
    sig = Table(
        [[_p("Card number:"), _p("Issued by (name & signature):"), _p("Date issued:")],
         [_p(" "), _p(" "), _p(" ")]],
        colWidths=[width / 3] * 3, rowHeights=[14, 26],
    )
    sig.setStyle(TableStyle([("LINEBELOW", (0, 1), (-1, 1), 0.6, INK), ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))
    story.append(KeepTogether([Paragraph("For library use", H2), sig]))
    return _build(story, A4)


def reservations_report(reservations, filter_summary, user):
    reservations = list(reservations)
    width = landscape(A4)[0] - 30 * mm
    story = _header("Room & Space Reservations Report", [filter_summary, _generated_line(user)], width)
    by_status = Counter(r.status for r in reservations)
    story.append(_summary_tiles([
        ("Reservations", len(reservations)),
        ("Pending", by_status.get("pending", 0)),
        ("Confirmed", by_status.get("confirmed", 0)),
        ("Cancelled", by_status.get("cancelled", 0)),
    ], width))
    story.append(Paragraph("Reservations", H2))
    if not reservations:
        story.append(Paragraph("No reservations match these filters.", SUB))
    else:
        rows = [[
            _p(r.reservation_date.strftime("%d %b %Y"), CELL_B), _p(r.space_type), _p(r.name),
            _p(r.organization), _p(r.phone), _p(r.get_duration_display()), _p(r.attendees_count), _status_cell(r),
        ] for r in reservations]
        story.append(_data_table(
            ["Date", "Space", "Booked by", "Organization", "Phone", "Duration", "People", "Status"],
            rows,
            [w * width for w in (0.1, 0.22, 0.15, 0.15, 0.12, 0.09, 0.07, 0.1)],
        ))
    return _build(story, landscape(A4))
