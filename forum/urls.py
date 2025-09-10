from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
    path("thread/<int:thread_id>/", views.thread_detail, name="thread"),
    path("create-thread/", views.create_thread, name="create_thread"),

]


