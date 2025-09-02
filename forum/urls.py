from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = "forum"

urlpatterns = [
    path("", views.thread_list, name="main"),
    path("thread/<int:thread_id>/", views.thread_detail, name="thread"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/create/", views.announcement_create, name="announcement_create"),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/upload/', views.media_upload_view, name='media_upload'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


