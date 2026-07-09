from django import forms
from .models import Appointment
from .models import SessionNote


class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment

        fields = [
            "appointment_date",
            "appointment_time",
            "reason",
        ]

        widgets = {

            "appointment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "appointment_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control"
                }
            ),

        }


class SessionNoteForm(forms.ModelForm):

    class Meta:

        model = SessionNote

        fields = [
            "notes",
            "recommendations",
            "follow_up_date",
        ]

        widgets = {

            "notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control"
                }
            ),

            "recommendations": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control"
                }
            ),

            "follow_up_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

        }