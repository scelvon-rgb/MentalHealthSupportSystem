from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import UserProfile
from .forms import AppointmentForm, SessionNoteForm
from .models import Appointment, SessionNote
from .reports import generate_appointment_report
from .session_report import generate_session_note_report

import os


@login_required
def book_appointment(request):

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)
            appointment.student = request.user
            appointment.save()

            # Send confirmation email
            if request.user.email:
                send_mail(
                    subject="Appointment Request Received",
                    message=f"""
Hello {request.user.username},

Your counselling appointment request has been received successfully.

You will receive another email once the counsellor approves or rejects your appointment.

Thank you for using the Mental Health Support System.
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

            return redirect("dashboard")

    else:

        form = AppointmentForm()

    return render(
        request,
        "appointment_system/book_appointment.html",
        {
            "form": form
        }
    )


@login_required
def appointment_list(request):

    profile = UserProfile.objects.get(user=request.user)
    role = profile.role.role_name

    if role == "Student":

        appointments = Appointment.objects.filter(
            student=request.user
        ).order_by("-created_at")

    else:

        appointments = Appointment.objects.all().order_by("-created_at")

    for appointment in appointments:
        appointment.has_session_note = SessionNote.objects.filter(
            appointment=appointment
        ).exists()

    return render(
        request,
        "appointment_system/appointment_list.html",
        {
            "appointments": appointments,
            "role": role,
        }
    )


@login_required
def approve_appointment(request, appointment_id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name != "Counsellor":
        return redirect("dashboard")

    appointment = get_object_or_404(
        Appointment,
        appointment_id=appointment_id
    )

    appointment.status = "Approved"
    appointment.counselor = request.user
    appointment.save()

    # Send approval email to the student
    if appointment.student.email:
        send_mail(
            subject="Appointment Approved",
            message=f"""
Hello {appointment.student.first_name},

Good news!

Your counselling appointment has been approved.

Appointment Details

Date: {appointment.appointment_date}
Time: {appointment.appointment_time}

Please log in to the Mental Health Support System to view your appointment.

Thank you.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.student.email],
            fail_silently=False,
        )

    return redirect("appointment_list")

@login_required
def reject_appointment(request, appointment_id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name != "Counsellor":
        return redirect("dashboard")

    appointment = get_object_or_404(
        Appointment,
        appointment_id=appointment_id
    )

    appointment.status = "Rejected"
    appointment.counselor = request.user
    appointment.save()

    

@login_required
def add_session_note(request, appointment_id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name != "Counsellor":
        return redirect("dashboard")

    appointment = get_object_or_404(
        Appointment,
        appointment_id=appointment_id
    )

    if hasattr(appointment, "session_note"):
        return redirect(
            "view_session_note",
            appointment_id=appointment.appointment_id
        )

    if request.method == "POST":

        form = SessionNoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)

            note.appointment = appointment
            note.counselor = request.user

            note.save()

            return redirect(
                "view_session_note",
                appointment_id=appointment.appointment_id
            )

    else:

        form = SessionNoteForm()

    return render(
        request,
        "appointment_system/add_session_note.html",
        {
            "form": form,
            "appointment": appointment,
        }
    )


@login_required
def view_session_note(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        appointment_id=appointment_id
    )

    note = get_object_or_404(
        SessionNote,
        appointment=appointment
    )

    return render(
        request,
        "appointment_system/view_session_note.html",
        {
            "appointment": appointment,
            "note": note,
        }
    )


@login_required
def export_appointment_report(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name not in [
        "Admin",
        "Administrator",
        "Counsellor",
        "Counselor",
    ]:
        return redirect("dashboard")

    reports_folder = os.path.join(settings.BASE_DIR, "reports")
    os.makedirs(reports_folder, exist_ok=True)

    pdf_path = os.path.join(
        reports_folder,
        "appointment_report.pdf"
    )

    generate_appointment_report(pdf_path)

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename="Appointment_Report.pdf"
    )


@login_required
def export_session_report(request, appointment_id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role.role_name not in [
        "Counsellor",
        "Counselor",
        "Admin",
        "Administrator",
    ]:
        return redirect("dashboard")

    appointment = get_object_or_404(
        Appointment,
        appointment_id=appointment_id
    )

    note = get_object_or_404(
        SessionNote,
        appointment=appointment
    )

    reports_folder = os.path.join(settings.BASE_DIR, "reports")
    os.makedirs(reports_folder, exist_ok=True)

    pdf_path = os.path.join(
        reports_folder,
        f"session_report_{appointment.appointment_id}.pdf"
    )

    generate_session_note_report(
        note,
        pdf_path
    )

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename=f"Session_Report_{appointment.appointment_id}.pdf"
    )