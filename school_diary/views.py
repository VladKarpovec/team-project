from django.shortcuts import render, get_object_or_404, redirect
from .models import Classroom, Subject


# Create your views here.
def subjects_list(request):
    subjects = Subject.objects.all()
    return render(request, "school_diary/subjects.html", context={"subjects": subjects})


def classes_list(request, subject_id):
    classes = Classroom.objects.all().filter(subjects__id=subject_id)
    return render(
        request,
        "school_diary/classes.html",
        context={"classes": classes, "subject_id": subject_id},
    )


def scores(request, subject_id, class_id):
    classroom = get_object_or_404(Classroom, id=class_id)
    subject = get_object_or_404(Subject, id=subject_id)
    students = classroom.students.all()
    return redirect("diary:classes", subject_id=subject.id)
