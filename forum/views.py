from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Post
from .forms import ThreadForm, PostForm


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

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect("forum:thread", thread_id=thread.id)
        else:
            return render(
                request,
                "forum/thread.html",
                context={"thread": thread, "post_form": post_form},
            )

    else:
        post_form = PostForm()
        return render(
            request,
            "forum/thread.html",
            context={"thread": thread, "post_form": post_form},
        )


def create_thread(request):
    if request.method == "POST":
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save()
            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.is_first = True
            post.save()
            return redirect("forum:thread", thread_id=thread.id)
        else:
            return render(
                request,
                "forum/thread_create.html",
                context={"thread_form": thread_form, "post_form": post_form},
            )
    else:
        thread_form = ThreadForm()
        post_form = PostForm()
        return render(
            request,
            "forum/thread_create.html",
            context={"thread_form": thread_form, "post_form": post_form},
        )


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
