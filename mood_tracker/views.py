from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings
import os

from .forms import MoodForm
from .models import Mood
from .reports import generate_mood_report


@login_required
def mood_checkin(request):

    if request.method == "POST":

        form = MoodForm(request.POST)

        if form.is_valid():

            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()

            return redirect("mood_history")

    else:

        form = MoodForm()

    return render(
        request,
        "mood_tracker/checkin.html",
        {
            "form": form
        }
    )


@login_required
def mood_history(request):

    moods = Mood.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "mood_tracker/history.html",
        {
            "moods": moods
        }
    )


@login_required
def edit_mood(request, mood_id):

    mood = get_object_or_404(
        Mood,
        mood_id=mood_id,
        user=request.user
    )

    if request.method == "POST":

        form = MoodForm(
            request.POST,
            instance=mood
        )

        if form.is_valid():

            form.save()

            return redirect("mood_history")

    else:

        form = MoodForm(instance=mood)

    return render(
        request,
        "mood_tracker/edit_mood.html",
        {
            "form": form
        }
    )


@login_required
def delete_mood(request, mood_id):

    mood = get_object_or_404(
        Mood,
        mood_id=mood_id,
        user=request.user
    )

    mood.delete()

    return redirect("mood_history")


@login_required
def mood_analytics(request):

    moods = Mood.objects.filter(
        user=request.user
    ).order_by("created_at")

    mood_scores = {
        "Happy": 5,
        "Calm": 4,
        "Neutral": 3,
        "Sad": 2,
        "Stressed": 1,
        "Anxious": 0,
    }

    labels = []
    values = []

    for mood in moods:

        labels.append(
            mood.created_at.strftime("%d %b")
        )

        values.append(
            mood_scores.get(
                mood.mood,
                0
            )
        )

    total_entries = moods.count()

    if values:

        average_score = round(
            sum(values) / len(values),
            2
        )

        highest_score = max(values)
        lowest_score = min(values)

    else:

        average_score = 0
        highest_score = 0
        lowest_score = 0

    return render(
        request,
        "mood_tracker/analytics.html",
        {
            "labels": labels,
            "values": values,
            "moods": moods,
            "total_entries": total_entries,
            "average_score": average_score,
            "highest_score": highest_score,
            "lowest_score": lowest_score,
        }
    )


@login_required
def export_mood_report(request):

    reports_folder = os.path.join(
        settings.BASE_DIR,
        "reports"
    )

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    pdf_path = os.path.join(
        reports_folder,
        f"mood_report_{request.user.username}.pdf"
    )

    generate_mood_report(
        request.user,
        pdf_path
    )

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename="Mood_History_Report.pdf"
    )