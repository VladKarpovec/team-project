from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Post


# Create your views here.
def thread_list(request):
    tag = request.GET.get("tag")
    if tag:
        threads = Thread.objects.filter(tag=tag)
    else:
        threads = Thread.objects.all()
    return render(request, "forum/main.html", context={"threads": threads})


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == "GET":
        context = {
            "thread": thread,
            "can_manage": can_manage_thread(request.user, thread),
        }
        return render(request, "forum/thread.html", context=context)
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


def can_manage_thread(user, thread):
    if not user.is_authenticated:
        return False
    if user.profile.role in ["admin", "manager"]:
        return True

    first_post = thread.posts.filter(is_first=True).first()
    if first_post and first_post.author == user:
        return True


def update_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if not can_manage_thread(request.user, thread):
        return redirect("forum:thread", thread_id=thread.id)

    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            thread.title = new_title
            thread.save()

    return redirect("forum:thread", thread_id=thread.id)


def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if not can_manage_thread(request.user, thread):
        return redirect("forum:thread", thread_id=thread.id)

    if request.method == "POST":
        thread.delete()
        return redirect("forum:main")

    return redirect("forum:thread", thread_id=thread.id)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    thread = post.thread

    if not (can_manage_thread(request.user, thread) or request.user == post.author):
        return redirect("forum:thread", thread_id=thread.id)

    if request.method == "POST":
        post.delete()
        return redirect("forum:thread", thread_id=thread.id)

    return redirect("forum:thread", thread_id=thread.id)
