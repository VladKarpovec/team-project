from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Post


# Create your views here.
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, "forum/main.html", context={"threads": threads})


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == "GET":
        return render(request, "forum/thread.html", context={"thread": thread})
    elif request.method == "POST":
        text = request.POST.get("content")
        if text:
            post = Post.objects.create(
                thread=thread,
                content=text,
                author=request.user,
            )
        else:
            error = "Comment cannot be empty."
            return render(
                request,
                "forum/thread.html",
                context={"thread": thread, "error": error},
            )
        return redirect("forum:thread", thread_id=thread.id)


def create_thread(request):
    if request.method == "GET":
        return render(request, "forum/thread_create.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        thread = Thread.objects.create(title=title)
        post = Post.objects.create(
            thread=thread,
            content=content,
            author=request.user,
            is_first=True,
        )
        return redirect("forum:thread", thread_id=thread.id)
