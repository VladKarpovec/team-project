from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Survey, Question, Answer, Response, Choice
from .forms import SurveyForm, QuestionForm, AnswerForm

from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Survey


def is_moderator_or_admin(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    profile = getattr(user, "profile", None)
    return profile and profile.role in ("admin", "manager")


def survey_list(request):
    surveys = Survey.objects.all()
    responded_ids = set()

    if request.user.is_authenticated:
        responses = Response.objects.filter(user=request.user)
        responded_ids = set(r.survey_id for r in responses)

    return render(request, "polls/survey_list.html", {
        "surveys": surveys,
        "responded_ids": responded_ids,
    })


@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.questions.all()

    # отримуємо відповідь, якщо користувач вже проходив
    response, created = Response.objects.get_or_create(
        user=request.user, survey=survey
    )

    if request.method == "POST":
        response.answers.all().delete()

        for question in questions:
            qid = str(question.id)

            if question.question_type == "text":
                answer_value = request.POST.get(qid)
                if answer_value:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        text_answer=answer_value
                    )

            elif question.question_type == "radio":
                choice_text = request.POST.get(qid)
                if choice_text:
                    choice = question.choices.filter(text=choice_text).first()
                    if choice:
                        Answer.objects.create(
                            response=response,
                            question=question,
                            choice=choice
                        )

            elif question.question_type == "checkbox":
                selected = [v for k, v in request.POST.items() if k.startswith(qid + "_")]
                for choice_text in selected:
                    choice = question.choices.filter(text=choice_text).first()
                    if choice:
                        Answer.objects.create(
                            response=response,
                            question=question,
                            choice=choice
                        )

        messages.success(request, "Ваші відповіді збережено.")
        return redirect("polls:survey_completed", pk=survey.id)

    return render(request, "polls/survey_detail.html", {
        "survey": survey,
        "questions": questions,
    })


@login_required
def survey_results(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not is_moderator_or_admin(request.user):
        messages.error(request, "У вас немає доступу до результатів.")
        return redirect("polls:survey_list")

    responses = Response.objects.filter(survey=survey).select_related("user")
    return render(request, "polls/survey_results.html", {
        "survey": survey,
        "responses": responses,
    })


@login_required
def survey_completed(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    return render(request, "polls/survey_completed.html", {"survey": survey})


@login_required
def response_detail(request, survey_id, user_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    if not is_moderator_or_admin(request.user):
        messages.error(request, "У вас немає доступу до перегляду відповідей.")
        return redirect("polls:survey_list")

    response = get_object_or_404(Response, survey=survey, user_id=user_id)
    answers = response.answers.select_related("question")

    return render(request, "polls/response_detail.html", {
        "survey": survey,
        "response": response,
        "answers": answers,
    })


# --- CRUD для адміністраторів і менеджерів ---
@method_decorator(login_required, name="dispatch")
class SurveyCreateView(CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = "polls/survey_form.html"
    success_url = reverse_lazy("polls:survey_list")

    def dispatch(self, request, *args, **kwargs):
        if not is_moderator_or_admin(request.user):
            messages.error(request, "У вас немає доступу.")
            return redirect("polls:survey_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.created_by = self.request.user
        survey.save()

        for key in self.request.POST:
            if key.startswith("question_") and key.endswith("_text"):
                index = key.split("_")[1]
                text = self.request.POST.get(f"question_{index}_text")
                qtype = self.request.POST.get(f"question_{index}_type", "text")
                question = Question.objects.create(
                    survey=survey,
                    text=text,
                    order=int(index),
                    question_type=qtype
                )

                if qtype in ["radio", "checkbox"]:
                    options_raw = self.request.POST.get(f"question_{index}_options", "")
                    for line in options_raw.strip().split("\n"):
                        if line.strip():
                            Choice.objects.create(question=question, text=line.strip())

        messages.success(self.request, "Опитування створено.")
        return redirect(self.success_url)


@method_decorator(login_required, name="dispatch")
class SurveyUpdateView(UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = "polls/survey_form.html"
    success_url = reverse_lazy("polls:survey_list")

    def dispatch(self, request, *args, **kwargs):
        if not is_moderator_or_admin(request.user):
            messages.error(request, "У вас немає доступу.")
            return redirect("polls:survey_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        survey = form.save()

        survey.questions.all().delete()

        for key in self.request.POST:
            if key.startswith("question_") and key.endswith("_text"):
                index = key.split("_")[1]
                text = self.request.POST.get(f"question_{index}_text")
                qtype = self.request.POST.get(f"question_{index}_type", "text")
                question = Question.objects.create(
                    survey=survey,
                    text=text,
                    order=int(index),
                    question_type=qtype
                )

                if qtype in ["radio", "checkbox"]:
                    options_raw = self.request.POST.get(f"question_{index}_options", "")
                    for line in options_raw.strip().split("\n"):
                        if line.strip():
                            Choice.objects.create(question=question, text=line.strip())

        messages.success(self.request, "Опитування оновлено.")
        return redirect(self.success_url)


@method_decorator(login_required, name="dispatch")
class SurveyDeleteView(View):
    def post(self, request, pk):
        if not is_moderator_or_admin(request.user):
            return JsonResponse({"error": "Недостатньо прав"}, status=403)

        survey = get_object_or_404(Survey, pk=pk)
        survey.delete()
        return JsonResponse({"status": "deleted"})

    def get(self, request, pk):
        # Якщо хтось випадково перейде GET-запитом — повертаємо 405
        return JsonResponse({"error": "GET-запит не підтримується"}, status=405)
