from django.contrib import admin
from .models import Subject, Classroom, Student, Grade


# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "classroom")


@admin.register(Grade)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score", "date")
