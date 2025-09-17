from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from announcements.models import Announcement
from forum.models import Thread, Post
from events.models import Event
from gallery.models import GalleryImage

def home(request):
    now = timezone.now()
    month_start = now.replace(day=1)

    # Дані для блоків
    announcements = Announcement.objects.order_by("-created_at")[:5]
    forum_topics = Thread.objects.order_by("-created_at")[:5]
    upcoming_events = Event.objects.filter(date__gte=now.date()).order_by("date")[:5]
    gallery_images = GalleryImage.objects.order_by("-uploaded_at")[:6]

    # Статистика
    stats = {
        "members": User.objects.count(),
        "events_this_month": Event.objects.filter(date__gte=month_start.date()).count(),
        "new_posts": Post.objects.filter(created_at__gte=month_start).count(),
    }

    context = {
        "announcements": announcements,
        "forum_topics": forum_topics,
        "upcoming_events": upcoming_events,
        "gallery_images": gallery_images,
        "stats": stats,
    }
    return render(request, "home.html", context)
