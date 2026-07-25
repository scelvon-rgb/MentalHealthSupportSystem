from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ("Online", "Online"),
        ("Physical", "Physical"),
    ]

    appointment_id = models.AutoField(primary_key=True)

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_appointments"
    )

    counselor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="counselor_appointments",
        blank=True,
        null=True
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField()

    # NEW FIELD
    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES,
        default="Physical"
    )

    # For online appointments
    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    # For physical appointments
    meeting_location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "appointments"

    def __str__(self):
        return f"{self.student.username} - {self.appointment_date}"


class SessionNote(models.Model):

    note_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="session_note"
    )

    counselor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    notes = models.TextField()

    recommendations = models.TextField(
        blank=True,
        null=True
    )

    follow_up_date = models.DateField(
        blank=True,
        null=True
    )
    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    meeting_location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "session_notes"

    def __str__(self):
        return f"Session Note - {self.appointment.student.username}"
    rejection_reason = models.TextField(
    blank=True,
    null=True
)