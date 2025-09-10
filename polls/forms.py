from django import forms
from .models import Survey, Question, Choice

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ("title", "description")

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("text", "order", "question_type")

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ("text",)

class AnswerForm(forms.Form):
    def __init__(self, question: Question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        if question.question_type == "text":
            self.fields["text_answer"] = forms.CharField(widget=forms.Textarea, required=True)
        elif question.question_type == "radio":
            self.fields["choice"] = forms.ModelChoiceField(
                queryset=question.choices.all(),
                widget=forms.RadioSelect,
                required=True,
                empty_label=None,
            )
        elif question.question_type == "checkbox":
            self.fields["choices"] = forms.ModelMultipleChoiceField(
                queryset=question.choices.all(),
                widget=forms.CheckboxSelectMultiple,
                required=True,
            )