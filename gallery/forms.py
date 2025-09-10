from django import forms

class MediaUploadForm(forms.Form):
    media_file = forms.FileField(required=True)


