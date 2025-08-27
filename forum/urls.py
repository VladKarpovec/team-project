from django.urls import path
from forum import views
from .views import announcement_list

app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
    path("thread/<int:thread_id>/", views.thread_detail, name="thread"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path('announcements/', announcement_list, name='announcement_list'),
]
