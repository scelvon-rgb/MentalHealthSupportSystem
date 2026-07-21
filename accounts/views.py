from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistrationForm, ProfileForm, AdminUserCreationForm
from .models import Role, UserProfile, Notification

from mood_tracker.models import Mood
from appointment_system.models import Appointment
from resources.models import Resource
from forum.models import ForumPost

from django.db.models import Count
def logout_view(request):
    logout(request)
    return redirect("login")
def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.save()

                # Every public registration becomes a Student
                student_role = Role.objects.get(role_name="Student")

                UserProfile.objects.create(
                    user=user,
                    role=student_role,
                    phone="",
                    student_reg_no=""
                )

                messages.success(
                    request,
                    "Registration successful. Please login."
                )

                return redirect("login")

            except Exception as e:
                print("REGISTRATION ERROR:", e)
                messages.error(
                    request,
                    "Registration failed."
                )

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password",
            },
        )

    return render(request, "accounts/login.html")

@login_required
def dashboard(request):

    profile = UserProfile.objects.get(user=request.user)
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

        moods = Mood.objects.filter(
            user=request.user
        ).order_by("created_at")

        mood_scale = {
            "Happy": 6,
            "Calm": 5,
            "Neutral": 4,
            "Sad": 3,
            "Stressed": 2,
            "Anxious": 1,
        }

        mood_labels = []
        mood_values = []

        for mood in moods:
            mood_labels.append(mood.created_at.strftime("%d %b"))
            mood_values.append(
                mood_scale.get(mood.mood, 0)
            )

        return render(
            request,
            "accounts/dashboard/student_dashboard.html",
            {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "role": role,
                "profile": profile,
                "active_page": "dashboard",
                "mood_labels": mood_labels,
                "mood_values": mood_values,
            },
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
                "role": role,
                "profile": profile,
                "active_page": "dashboard",
            },
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
                "Counselor",
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
                "role": role,
                "profile": profile,
                "active_page": "dashboard",
            },
        )

    return redirect("login")
@login_required
def view_students(request):

    students = UserProfile.objects.select_related(
        "user",
        "role"
    ).all()

    return render(
        request,
        "accounts/view_students.html",
        {
            "students": students,
        },
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
            "moods": moods,
        },
    )


@login_required
def profile(request):

    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "profile",
        },
    )


@login_required
def settings(request):

    profile = UserProfile.objects.get(user=request.user)

    return render(
        request,
        "accounts/dashboard/settings.html",
        {
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "settings",
        },
    )
@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": notifications,
            "profile": UserProfile.objects.get(user=request.user),
            "role": UserProfile.objects.get(user=request.user).role.role_name,
            "active_page": "notifications",
        },
    )


@login_required
def mark_notification_read(request, notification_id):

    notification = Notification.objects.get(
        notification_id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("notifications")


@login_required
def delete_notification(request, notification_id):

    notification = Notification.objects.get(
        notification_id=notification_id,
        user=request.user
    )

    notification.delete()

    return redirect("notifications")
@login_required
def add_user(request):

    profile = UserProfile.objects.get(user=request.user)

    # Only admins can add users
    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role_name = request.POST["role"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("add_user")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add_user")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        role = Role.objects.get(role_name=role_name)

        UserProfile.objects.create(
            user=user,
            role=role,
            phone="",
            student_reg_no=""
        )

        messages.success(request, "User created successfully.")

        return redirect("manage_users")

    roles = Role.objects.all()

    return render(
        request,
        "accounts/admin/add_user.html",
        {
            "roles": roles,
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "manage_users",
        },
    )
@login_required
def manage_users(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    users = UserProfile.objects.select_related(
        "user",
        "role"
    )

    search = request.GET.get("search")

    if search:
        users = users.filter(
            user__first_name__icontains=search
        ) | users.filter(
            user__last_name__icontains=search
        ) | users.filter(
            user__username__icontains=search
        ) | users.filter(
            user__email__icontains=search
        )

    return render(
        request,
        "accounts/admin/manage_users.html",
        {
            "users": users,
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "manage_users",
        },
    )
@login_required
def add_user(request):

    profile = UserProfile.objects.get(user=request.user)

    # Only Admins can access this page
    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":

        form = AdminUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                phone="",
                student_reg_no=""
            )

            messages.success(
                request,
                "User created successfully."
            )

            return redirect("manage_users")

    else:

        form = AdminUserCreationForm()

    return render(
        request,
        "accounts/admin/add_users.html",
        {
            "form": form,
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "manage_users",
        },
    )