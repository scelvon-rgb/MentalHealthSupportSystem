from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("students/", views.view_students, name="view_students"),

    path(
        "students/<int:user_id>/",
        views.student_mood_history,
        name="student_mood_history"
    ),
]