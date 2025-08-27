from django.urls import path
from forum import views


app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
    path("thread/<int:thread_id>/", views.thread_detail, name="thread"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("thread/<int:thread_id>/edit/", views.update_thread, name="thread_edit"),
    path("thread/<int:thread_id>/delete/", views.delete_thread, name="thread_delete"),
]
