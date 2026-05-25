# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=20, unique=True)
    current_class = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.reg_number})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically calculates totals and grades before storing in database
        self.total_score = self.test_score + self.exam_score
        if self.total_score >= 70:
            self.grade = 'A'
        elif self.total_score >= 60:
            self.grade = 'B'
        elif self.total_score >= 50:
            self.grade = 'C'
        elif self.total_score >= 45:
            self.grade = 'D'
        elif self.total_score >= 40:
            self.grade = 'E'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.student.reg_number} - {self.subject.name}: {self.grade}"
