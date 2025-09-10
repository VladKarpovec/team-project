from django.shortcuts import render, redirect
from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'forum/announcement_list.html', {'announcements': announcements})

def announcement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Announcement.objects.create(title=title, description=description)
            return redirect('announcement_list')
        else:
            error = "Будь ласка, заповніть усі поля."
            return render(request, 'announcement_create.html', {'error': error})

    return render(request, 'announcements/announcement_create.html')


