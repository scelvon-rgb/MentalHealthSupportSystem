from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:

        model = Resource

        fields = [
            "title",
            "category",
            "description",
            "content",
            "resource_file",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "rows": 8,
                    "class": "form-control"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "resource_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }