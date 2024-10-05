from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    semester = models.CharField(max_length=50)
    academic_year = models.IntegerField()
    available_seats = models.IntegerField()
    is_open = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.code} - {self.name}"

class QuotaRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"
