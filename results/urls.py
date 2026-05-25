from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name='student_login'), # Default route
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/<int:student_id>/', views.student_report_slip, name='student_report_slip'), # New Line
]