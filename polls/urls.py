from django.urls import path
from .views import (
    survey_completed,
    survey_list,
    survey_detail,
    survey_results,
    response_detail,
    SurveyCreateView,
    SurveyUpdateView,
    SurveyDeleteView,
)


app_name = "polls"


urlpatterns = [
    path("", survey_list, name="survey_list"),
    path("<int:pk>/", survey_detail, name="survey_detail"),
    path("<int:pk>/results/", survey_results, name="survey_results"),
    path("<int:survey_id>/response/<int:user_id>/", response_detail, name="response_detail"),
    path("<int:pk>/completed/", survey_completed, name="survey_completed"),

    #
    path("create/", SurveyCreateView.as_view(), name="survey_create"),
    path("<int:pk>/edit/", SurveyUpdateView.as_view(), name="survey_edit"),
    path("<int:pk>/delete/", SurveyDeleteView.as_view(), name="survey_delete"),
]
