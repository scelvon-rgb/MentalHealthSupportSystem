from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from .models import Appointment


def generate_appointment_report(file_path):

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Mental Health Support System<br/>Appointment Report",
        styles["Heading1"]
    )

    elements.append(title)

    data = [
        [
            "Student",
            "Date",
            "Time",
            "Status"
        ]
    ]

    appointments = Appointment.objects.all().order_by("-appointment_date")

    for appointment in appointments:

        data.append([
            appointment.student.username,
            str(appointment.appointment_date),
            str(appointment.appointment_time),
            appointment.status
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

    ]))

    elements.append(table)

    doc.build(elements)