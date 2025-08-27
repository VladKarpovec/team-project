from django.urls import path
from school_diary import views


app_name = "diary"

urlpatterns = [
    path("subjects/", views.subjects_list, name="subjects"),
    path("<int:subject_id>/classes/", views.classes_list, name="classes"),
    path("<int:subject_id>/<int:class_id>/", views.scores, name="scores"),
]
