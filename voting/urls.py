from django.urls import path
from . import views

app_name = "voting"


urlpatterns = [
    path("", views.poll_list, name="voting_list"),
    path("<int:poll_id>/", views.poll_detail, name="voting_detail"),
    path("<int:poll_id>/vote/<int:choice_id>/", views.vote, name="vote"),
    path("<int:poll_id>/results/", views.poll_results, name="voting_results"),
    path("create/", views.create_poll, name="create_voting"),
    path("delete/<int:poll_id>/", views.delete_poll, name="delete_voting"),
    path("edit/<int:poll_id>/", views.edit_poll, name="edit_voting"),
]
