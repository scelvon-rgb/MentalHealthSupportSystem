from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import Mood


def generate_mood_report(user, file_path):

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        f"Mental Health Support System<br/>Mood History Report<br/>{user.username}",
        styles["Heading1"]
    )

    elements.append(title)

    data = [
        [
            "Mood",
            "Notes",
            "Date"
        ]
    ]

    moods = Mood.objects.filter(user=user).order_by("-created_at")

    for mood in moods:

        data.append([
            mood.mood,
            mood.notes if mood.notes else "-",
            mood.created_at.strftime("%Y-%m-%d %H:%M")
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