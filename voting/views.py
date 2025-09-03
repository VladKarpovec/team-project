from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Vote

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .form import PollForm
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, "voting/poll_list.html", {"voting": polls})


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "voting/poll_detail.html", {"poll": poll})


@login_required
def vote(request, poll_id, choice_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choice = get_object_or_404(Choice, id=choice_id, poll=poll)

    # або створюємо голос, або оновлюємо існуючий
    Vote.objects.update_or_create(
        poll=poll, user=request.user,
        defaults={"choice": choice}
    )
    return redirect("voting:poll_results", poll_id=poll.id)


def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    votes = Vote.objects.filter(poll=poll)
    results = {choice.text: votes.filter(choice=choice).count() for choice in poll.choices.all()}
    return render(request, "voting/poll_results.html", {"poll": poll, "results": results})


@staff_member_required
def create_poll(request):
    if request.method == "POST":
        question = request.POST.get("question")
        choices = request.POST.getlist("choices")

        if not question or not any(choices):
            messages.error(request, "Питання та хоча б один варіант обов'язкові.")
            return render(request, "voting/poll_create.html")

        poll = Poll.objects.create(
            question=question,
            created_by=request.user
        )
        for choice_text in choices:
            if choice_text.strip():
                Choice.objects.create(poll=poll, text=choice_text.strip())

        messages.success(request, "Опитування створено успішно.")
        return redirect("voting:poll_list")

    return render(request, "voting/poll_create.html")


@staff_member_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return redirect("voting:poll_list")


@staff_member_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = poll.choices.all()

    if request.method == "POST":
        form = PollForm(request.POST, instance=poll)
        new_choices = request.POST.getlist("choices")

        if form.is_valid():
            form.save()

            poll.choices.all().delete()

            for text in new_choices:
                text = text.strip()
                if text:
                    Choice.objects.create(poll=poll, text=text)

            return redirect("voting:poll_list")

    else:
        form = PollForm(instance=poll)

    return render(request, "voting/poll_edit.html", {
        "form": form,
        "choices": choices,
        "poll": poll,
    })