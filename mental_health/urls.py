from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path("accounts/", include("accounts.urls")),

    path("mood/", include("mood_tracker.urls")),

    path("appointments/", include("appointment_system.urls")),

    path("resources/", include("resources.urls")),

    path("forum/", include("forum.urls")),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
    ),
    name="password_reset",
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),

]