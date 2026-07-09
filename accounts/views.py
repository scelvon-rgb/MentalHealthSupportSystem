from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .models import Role, UserProfile

from mood_tracker.models import Mood
from appointment_system.models import Appointment
from resources.models import Resource
from forum.models import ForumPost


def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            student_role = Role.objects.get(
                role_name="Student"
            )

            UserProfile.objects.create(
                user=user,
                role=student_role,
                phone="",
                student_reg_no=""
            )

            return redirect("login")

    else:

        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


@login_required
def dashboard(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    role = profile.role.role_name

    # ==========================
    # STUDENT DASHBOARD
    # ==========================

    if role == "Student":

        total = Appointment.objects.filter(
            student=request.user
        ).count()

        pending = Appointment.objects.filter(
            student=request.user,
            status="Pending"
        ).count()

        approved = Appointment.objects.filter(
            student=request.user,
            status="Approved"
        ).count()

        rejected = Appointment.objects.filter(
            student=request.user,
            status="Rejected"
        ).count()

        return render(
            request,
            "accounts/dashboard/student_dashboard.html",
            {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
            }
        )

    # ==========================
    # COUNSELLOR DASHBOARD
    # ==========================

    elif role in ["Counsellor", "Counselor"]:

        total = Appointment.objects.count()

        pending = Appointment.objects.filter(
            status="Pending"
        ).count()

        approved = Appointment.objects.filter(
            status="Approved"
        ).count()

        rejected = Appointment.objects.filter(
            status="Rejected"
        ).count()

        return render(
            request,
            "accounts/dashboard/counselor_dashboard.html",
            {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
            }
        )

    # ==========================
    # ADMIN DASHBOARD
    # ==========================

    elif role in ["Admin", "Administrator"]:

        total_students = UserProfile.objects.filter(
            role__role_name="Student"
        ).count()

        total_counsellors = UserProfile.objects.filter(
            role__role_name__in=[
                "Counsellor",
                "Counselor"
            ]
        ).count()

        total_appointments = Appointment.objects.count()

        total_moods = Mood.objects.count()

        total_resources = Resource.objects.count()

        total_forum_posts = ForumPost.objects.count()

        pending = Appointment.objects.filter(
            status="Pending"
        ).count()

        approved = Appointment.objects.filter(
            status="Approved"
        ).count()

        rejected = Appointment.objects.filter(
            status="Rejected"
        ).count()

        return render(
            request,
            "accounts/dashboard/admin_dashboard.html",
            {
                "total_students": total_students,
                "total_counsellors": total_counsellors,
                "total": total_appointments,
                "total_moods": total_moods,
                "total_resources": total_resources,
                "total_forum_posts": total_forum_posts,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
            }
        )

    return redirect("login")

@login_required
def view_students(request):

    students = UserProfile.objects.filter(
        role__role_name="Student"
    )

    return render(
        request,
        "accounts/view_students.html",
        {
            "students": students
        }
    )


@login_required
def student_mood_history(request, user_id):

    student = UserProfile.objects.get(
        user__id=user_id
    )

    moods = Mood.objects.filter(
        user__id=user_id
    ).order_by("-created_at")

    return render(
        request,
        "accounts/student_mood_history.html",
        {
            "student": student,
            "moods": moods
        }
    )