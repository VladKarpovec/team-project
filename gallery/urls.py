from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('gallery/upload/', views.media_upload_view, name='media_upload'),
    path('delete/<int:media_id>/', views.delete_media_view, name='delete_media'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








