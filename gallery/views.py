from django.shortcuts import render, redirect
from .forms import MediaUploadForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect
from .models import Media

def gallery_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('media_file')
            for f in files:
                fs = FileSystemStorage()
                file_path = fs.save(f.name, f)
                Media.objects.create(
                    file=file_path,
                    title=f.name,
                    is_image=f.content_type.startswith('image'),
                    is_video=f.content_type.startswith('video')
                )
            return redirect('gallery:gallery')

    else:
        form = MediaUploadForm()
    media_items = Media.objects.all().order_by('-id')
    return render(request, 'gallery/gallery.html', {
        'form': form,
        'media_items': media_items
    })


def media_upload_view(request):
    form = MediaUploadForm()
    return render(request, 'gallery/upload.html', {'form': form})


def delete_media_view(request, media_id):
    if request.method == 'POST':
        media = get_object_or_404(Media, id=media_id)
        media.delete()
    return redirect('gallery:gallery')
