from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, 'home.html', {
        'announcements': [],
        'forum_topics': [],
        'upcoming_events': [],
        'now': datetime.now()
    })


def home(request):
    context = {
        "announcements": [],
        "forum_topics": [],
        "materials": [],
        "portfolio": [],
        "upcoming_events": [],
        "poll": None,
        "vote": None,
        "diary": [],
        "gallery": [],
        "stats": {"members": 0, "events_this_month": 0, "new_posts": 0}
    }
    return render(request, "home.html", context)
