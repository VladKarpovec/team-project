from django.urls import path
from school_diary import views


app_name = "diary"

urlpatterns = [
    path("subjects/", views.subjects_list, name="subjects"),
    path("<int:subject_id>/classes/", views.classes_list, name="classes"),
    path("<int:subject_id>/<int:class_id>/", views.scores, name="scores"),
    path("<int:subject_id>/<int:class_id>/<int:student_id>/add-grade/", views.add_grade, name="add_grade"),
]
