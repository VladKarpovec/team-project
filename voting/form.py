# voting/forms.py
from django import forms
from .models import Poll, Choice


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question"]
        widgets = {
            "question": forms.TextInput(attrs={"class": "form-control", "placeholder": "Текст питання"}),
        }



