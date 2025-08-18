from django.urls import path
from forum import views


app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
]
