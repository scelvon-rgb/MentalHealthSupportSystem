from django.urls import path
from . import views

urlpatterns = [

    path(
        "checkin/",
        views.mood_checkin,
        name="mood_checkin"
    ),

    path(
        "history/",
        views.mood_history,
        name="mood_history"
    ),

    path(
        "edit/<int:mood_id>/",
        views.edit_mood,
        name="edit_mood"
    ),

    path(
        "delete/<int:mood_id>/",
        views.delete_mood,
        name="delete_mood"
    ),

    path(
        "analytics/",
        views.mood_analytics,
        name="mood_analytics"
    ),

    path(
        "export-report/",
        views.export_mood_report,
        name="export_mood_report"
    ),

]