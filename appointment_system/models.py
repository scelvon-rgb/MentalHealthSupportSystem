from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "session_notes"

    def __str__(self):
        return f"Session Note - {self.appointment.student.username}"