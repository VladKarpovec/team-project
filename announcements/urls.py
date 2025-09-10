from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = "announcements"




urlpatterns = [
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/create/", views.announcement_create, name="announcement_create"),


]