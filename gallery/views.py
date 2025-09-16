from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MediaUploadForm
from .models import Media

def gallery_view(request):
    form = MediaUploadForm()
    media_items = Media.objects.all().order_by('-id')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Щоб додати медіа, увійдіть або зареєструйтесь.")
            return redirect('gallery:gallery')

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
            messages.success(request, "Медіа успішно додано.")
            return redirect('gallery:gallery')
        else:
            messages.error(request, "Форма недійсна. Перевірте дані.")

    return render(request, 'gallery/gallery.html', {
        'form': form,
        'media_items': media_items
    })


@login_required
def media_upload_view(request):
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
            messages.success(request, "Медіа успішно додано.")
            return redirect('gallery:gallery')
        else:
            messages.error(request, "Форма недійсна.")
    else:
        form = MediaUploadForm()

    return render(request, 'gallery/upload.html', {'form': form})


@login_required
def delete_media_view(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if request.method == 'POST':
        media.delete()
        messages.success(request, "Медіа видалено.")
    return redirect('gallery:gallery')
