from django import forms
from .models import Appointment, SessionNote


class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment

        fields = [
            "appointment_date",
            "appointment_time",
            "appointment_type",
            "reason",
        ]

        widgets = {

            "appointment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "appointment_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "appointment_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Briefly explain why you need the appointment.",
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
                    "class": "form-control",
                }
            ),

            "recommendations": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                }
            ),

            "follow_up_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

        }


class RejectAppointmentForm(forms.Form):

    rejection_reason = forms.CharField(
        label="Reason for rejection",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter the reason for rejecting this appointment..."
            }
        )
    )