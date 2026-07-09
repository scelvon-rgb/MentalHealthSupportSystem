from django.db import models
from django.contrib.auth.models import User


class Mood(models.Model):

    MOOD_CHOICES = [
        ("Happy", "Happy"),
        ("Calm", "Calm"),
        ("Neutral", "Neutral"),
        ("Sad", "Sad"),
        ("Stressed", "Stressed"),
        ("Anxious", "Anxious"),
    ]

    mood_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "moods"

    def __str__(self):
        return f"{self.user.username} - {self.mood}"