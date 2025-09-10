from django import forms
from .models import Media

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'file']
