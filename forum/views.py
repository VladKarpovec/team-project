from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Post
from .models import Announcement
from .models import GalleryImage
from .models import MediaItem
from .forms import MediaUploadForm
from django.shortcuts import render
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




def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'forum/announcement_list.html', {'announcements': announcements})

def announcement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Announcement.objects.create(title=title, description=description)
            return redirect('forum:announcement_list')
        else:
            error = "Будь ласка, заповніть усі поля."
            return render(request, 'forum/announcement_create.html', {'error': error})

    return render(request, 'forum/announcement_create.html')



def gallery_view(request):
    images = GalleryImage.objects.order_by('-uploaded_at')
    return render(request, 'forum/gallery.html', {'images': images})


def gallery_view(request):
    media_items = [
        {'is_image': True, 'file': {'url': '/media/image1.jpg'}, 'title': 'Image 1'},
        {'is_video': True, 'file': {'url': '/media/video1.mp4'}, 'title': 'Video 1'},
    ]
    return render(request, 'forum/gallery.html', {'media_items': media_items})

def media_upload_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = MediaUploadForm()
    return render(request, 'forum/upload.html', {'form': form})