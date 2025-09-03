from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project


# portfolio/forms.py
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "screenshot", "link", "file"]
        labels = {
            "title": "Назва проєкту",
            "description": "Опис",
            "screenshot": "Скріншот",
            "link": "Посилання",
            "file": "Файл",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        self.fields["screenshot"].widget.attrs.update({"class": "form-control-file"})
        self.fields["file"].widget.attrs.update({"class": "form-control-file"})