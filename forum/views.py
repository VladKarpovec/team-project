from django.shortcuts import render
from .models import Thread


# Create your views here.
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, "forum/main.html", context={"threads": threads})


def thread_detail(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    return render(request, "forum/thread.html", context={"thread": thread})
