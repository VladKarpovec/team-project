from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=4)
    subjects = models.ManyToManyField(Subject, related_name="classrooms")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    classroom = models.ForeignKey(
        Classroom, related_name="students", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Grade(models.Model):
    SCORE_CHOICES = [(i, i) for i in range(1, 13)] + [("H", "H")]

    student = models.ForeignKey(
        Student, related_name="grades", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="grades", on_delete=models.CASCADE
    )
    score = models.CharField(max_length=2, choices=SCORE_CHOICES)
    date = models.DateField(auto_now_add=True)
