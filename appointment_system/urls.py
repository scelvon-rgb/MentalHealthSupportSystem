from django.urls import path
from . import views

urlpatterns = [

    path(
        "book/",
        views.book_appointment,
        name="book_appointment"
    ),

    path(
        "list/",
        views.appointment_list,
        name="appointment_list"
    ),

    path(
        "approve/<int:appointment_id>/",
        views.approve_appointment,
        name="approve_appointment"
    ),

    path(
        "reject/<int:appointment_id>/",
        views.reject_appointment,
        name="reject_appointment"
    ),

    path(
        "session-note/add/<int:appointment_id>/",
        views.add_session_note,
        name="add_session_note"
    ),

    path(
        "session-note/view/<int:appointment_id>/",
        views.view_session_note,
        name="view_session_note"
    ),
    path(
    "export-report/",
    views.export_appointment_report,
    name="export_appointment_report"
),
path(
    "session-report/<int:appointment_id>/",
    views.export_session_report,
    name="export_session_report"
),
]