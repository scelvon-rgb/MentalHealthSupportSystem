from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path("accounts/", include("accounts.urls")),

    path("mood/", include("mood_tracker.urls")),

    path("appointments/", include("appointment_system.urls")),

    path("resources/", include("resources.urls")),

    path("forum/", include("forum.urls")),

]