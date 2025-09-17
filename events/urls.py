from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('calendar/', views.event_calendar, name='event_calendar'),
    path('calendar/<int:year>/<int:month>/', views.event_calendar, name='event_calendar_month'),
]
