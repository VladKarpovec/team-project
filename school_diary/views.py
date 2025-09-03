from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Classroom, Subject, Grade


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

    grades = Grade.objects.filter(subject=subject, student__in=students).order_by(
        "date"
    )
    dates = grades.values_list("date", flat=True).distinct()  # Extract unique dates

    grade_dict = {}
    for student in students:
        grade_dict[student] = {g.date: g.score for g in grades.filter(student=student)}

    context = {
        "subject": subject,
        "classroom": classroom,
        "students": students,
        "dates": dates,
        "grade_dict": grade_dict,
        "grade_choices": [str(i) for i in range(1, 13)] + ["H"],
    }

    return render(request, "school_diary/scores_table.html", context=context)


def add_grade(request, subject_id, class_id, student_id):
    if request.method == "POST":
        subject = get_object_or_404(Subject, id=subject_id)
        classroom = get_object_or_404(Classroom, id=class_id)
        student = get_object_or_404(classroom.students, id=student_id)

        score = request.POST.get("score")
        date_str = request.POST.get("date")

        if score and date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            Grade.objects.create(
                student=student,
                subject=subject,
                score=score,
                date=date,
            )

        return redirect("diary:scores", subject_id=subject_id, class_id=class_id)
