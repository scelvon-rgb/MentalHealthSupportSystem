from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import RegistrationForm, ProfileForm, AdminUserCreationForm
from .models import UserProfile, Role, Notification

from mood_tracker.models import Mood
from appointment_system.models import Appointment
from resources.models import Resource
from forum.models import ForumPost
from django.core.mail import send_mail
from django.conf import settings

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

            selected_role = form.cleaned_data["role"]

            approved = True

            if selected_role.role_name == "Counsellor":
                approved = False

            UserProfile.objects.create(
                user=user,
                role=selected_role,
                phone="",
                student_reg_no="",
                is_approved=approved,
            )
            print("Sending email to:", user.email)

            # ==========================
            # STUDENT EMAIL
            # ==========================
            if approved:

                send_mail(
                    subject="Welcome to the Mental Health Support System",
                    message=f"""
Hello {user.first_name},

Thank you for registering for the Mental Health Support System.

Your account has been created successfully and is now active.

You can now log in using your username and password.

Regards,
Mental Health Support System Team
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                messages.success(
                    request,
                    "Registration successful. Please log in."
                )

            # ==========================
            # COUNSELLOR EMAIL
            # ==========================
            else:

                send_mail(
                    subject="Counsellor Registration Received",
                    message=f"""
Hello {user.first_name},

Thank you for registering as a counsellor.

Your registration has been received successfully.

Your account is currently awaiting administrator approval.

You will receive another email immediately after your account has been approved.

Regards,
Mental Health Support System Team
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                messages.success(
                    request,
                    "Thank you for registering as a counsellor. Please wait for administrator approval."
                )

            return redirect("login")

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

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            profile = UserProfile.objects.get(user=user)

            if (
                profile.role.role_name in ["Counsellor", "Counselor"]
                and not profile.is_approved
            ):

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "waiting_for_approval": True
                    }
                )

            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
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
def settings_view(request):

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

    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":

        form = AdminUserCreationForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                phone="",
                student_reg_no="",
            )

            messages.success(request, "User created successfully.")
            return redirect("manage_users")

    else:
        form = AdminUserCreationForm()

    return render(
        request,
        "accounts/admin/add_user.html",
        {
            "form": form,
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "manage_users",
        },
    )
@login_required
def manage_users(request):

    profile = UserProfile.objects.get(user=request.user)

    # Only admins can access
    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    users = UserProfile.objects.select_related(
        "user",
        "role"
    ).order_by("user__first_name")

    search = request.GET.get("search")

    if search:
        users = users.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search)
        )

    # DEBUG
    for u in users:
        print(
            f"ID={u.profile_id}, "
            f"User={u.user.username}, "
            f"Role={u.role.role_name}, "
            f"Approved={u.is_approved}, "
            f"Reason={u.rejection_reason}"
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
def approve_counsellor(request, profile_id):

    admin = UserProfile.objects.get(user=request.user)

    if admin.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    profile = UserProfile.objects.get(profile_id=profile_id)

    profile.is_approved = True
    profile.save()

    Notification.objects.create(
        user=profile.user,
        title="Account Approved",
        message="Your counsellor account has been approved. You can now log in."
    )

    messages.success(request, "Counsellor approved successfully.")

    return redirect("manage_users")
@login_required
def reject_counsellor(request, profile_id):

    admin = UserProfile.objects.get(user=request.user)

    if admin.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    profile = UserProfile.objects.get(profile_id=profile_id)

    if request.method == "POST":

        reason = request.POST.get("reason")

        print("========== REJECT DEBUG ==========")
        print("Profile ID:", profile.profile_id)
        print("Before:", profile.is_approved, profile.rejection_reason)

        profile.is_approved = False

        # Remove these two lines if you have NOT added the status field yet
        profile.status = "Rejected"

        profile.rejection_reason = reason
        profile.save()

        profile.refresh_from_db()

        print("After:", profile.is_approved, profile.rejection_reason)

        Notification.objects.create(
            user=profile.user,
            title="Counsellor Registration Rejected",
            message=(
                f"Your counsellor registration has been rejected.\n\n"
                f"Reason:\n{reason}"
            )
        )

        messages.success(request, "Counsellor rejected successfully.")
        return redirect("manage_users")

    return render(
        request,
        "accounts/admin/reject_counsellor.html",
        {
            "profile": profile,
        },
    )
@login_required
def add_user(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name not in ["Admin", "Administrator"]:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":

        form = AdminUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            selected_role = form.cleaned_data["role"]

            approved = True

            if selected_role.role_name == "Counsellor":
                approved = False

            UserProfile.objects.create(
                user=user,
                role=selected_role,
                phone="",
                student_reg_no="",
                is_approved=approved,
            )

            if not approved:

                Notification.objects.create(
                    user=user,
                    title="Registration Submitted",
                    message="Your counsellor account is waiting for administrator approval."
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
@login_required
def counsellor_availability(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name != "Counsellor":
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":

        profile.availability = request.POST.get("availability")
        profile.save()

        messages.success(
            request,
            "Availability updated successfully."
        )

        return redirect("counsellor_availability")

    return render(
        request,
        "accounts/counsellor_availability.html",
        {
            "profile": profile,
            "role": profile.role.role_name,
            "active_page": "availability",
        },
    )

@login_required
def available_counsellors(request):

    counsellors = UserProfile.objects.filter(
        role__role_name="Counsellor",
        is_approved=True
    ).select_related("user")

    return render(
        request,
        "accounts/available_counsellors.html",
        {
            "counsellors": counsellors,
        },
    )
