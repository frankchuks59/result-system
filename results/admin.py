# Register your models here.
from django.contrib import admin
from .models import StudentProfile, Subject, Result

admin.site.register(StudentProfile)
admin.site.register(Subject)
admin.site.register(Result)