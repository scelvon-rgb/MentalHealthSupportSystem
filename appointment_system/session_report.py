from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import SessionNote


def generate_session_note_report(note, file_path):

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Mental Health Support System",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            "Counselling Session Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Student:</b> {note.appointment.student.username}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Counsellor:</b> {note.counselor.username}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Date:</b> {note.appointment.appointment_date}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "<br/><b>Session Notes</b>",
            styles["Heading3"]
        )
    )

    elements.append(
        Paragraph(
            note.notes.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(elements)