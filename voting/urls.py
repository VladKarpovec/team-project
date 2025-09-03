from django.urls import path
from . import views

app_name = "voting"


urlpatterns = [
    path("", views.poll_list, name="poll_list"),
    path("<int:poll_id>/", views.poll_detail, name="poll_detail"),
    path("<int:poll_id>/vote/<int:choice_id>/", views.vote, name="vote"),
    path("<int:poll_id>/results/", views.poll_results, name="poll_results"),
    path("create/", views.create_poll, name="create_poll"),
    path("delete/<int:poll_id>/", views.delete_poll, name="delete_poll"),
]
