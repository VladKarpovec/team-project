
from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
    path("thread/<int:thread_id>/", views.thread_detail, name="thread"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/create/", views.announcement_create, name="announcement_create"),
]
