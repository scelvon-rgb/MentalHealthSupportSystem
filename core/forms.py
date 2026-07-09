from django import forms

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    ROLE_CHOICES = [
        (2, "Student"),
        (3, "Counsellor"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)