from django import forms
from .models import Mood


class MoodForm(forms.ModelForm):

    class Meta:

        model = Mood

        fields = [
            "mood",
            "notes",
        ]

        widgets = {

            "mood": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write how you're feeling today (optional)..."
                }
            ),

        }