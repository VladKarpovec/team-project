from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_surveys")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ("text", "Текст"),
        ("radio", "Один варіант"),
        ("checkbox", "Кілька варіантів"),
    ]

    survey = models.ForeignKey(Survey, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=800)
    order = models.PositiveIntegerField(default=0)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="text")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.survey.title} — {self.text[:50]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, related_name="responses", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="survey_responses", on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["survey", "user"], name="unique_survey_user")
        ]

    def __str__(self):
        return f"{self.user} → {self.survey}"

class Answer(models.Model):
    response = models.ForeignKey(Response, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.response.user} — {self.question.text[:40]}"