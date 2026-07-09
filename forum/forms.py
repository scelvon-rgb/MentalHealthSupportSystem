from django import forms
from .models import ForumPost, ForumComment


class ForumPostForm(forms.ModelForm):

    class Meta:

        model = ForumPost

        fields = [
            "title",
            "content",
            "anonymous"
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your post..."
                }
            ),

            "anonymous": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }


class ForumCommentForm(forms.ModelForm):

    class Meta:

        model = ForumComment

        fields = [
            "comment"
        ]

        widgets = {

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write a comment..."
                }
            ),

        }