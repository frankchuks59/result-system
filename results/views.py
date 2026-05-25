from django.shortcuts import render, redirect
from .models import StudentProfile, Subject, Result
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect, get_object_or_404

def teacher_dashboard(request):
    if request.method == "POST":
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')

        #convert text inputs to numbers for model fields
        test_score = float(request.POST.get('test_score', 0))
        exam_score = float(request.POST.get('exam_score', 0))
        
        # Pull model objects
        student_obj = StudentProfile.objects.get(id=student_id)
        subject_obj = Subject.objects.get(id=subject_id)
        
        # Save new record; logic triggers automated grade calculation internally
        Result.objects.create(
            student=student_obj,
            subject=subject_obj,
            test_score=test_score,
            exam_score=exam_score
        )
        return redirect('teacher_dashboard')

    # Data queries to build dropdown fields and results logs
    context = {
        'students': StudentProfile.objects.all(),
        'subjects': Subject.objects.all(),
        'results': Result.objects.all().order_by('-id')
    }
    return render(request, 'results/teacher_dashboard.html', context)

def student_report_slip(request, student_id):
    # Fetch the exact student matching the ID parameter in the URL route
    student = get_object_or_404(StudentProfile, id=student_id)
    
    # Filter only results belonging to this single student
    results = Result.objects.filter(student=student)
    
    return render(request, 'results/student_report.html', {
        'student': student,
        'results': results
    })

def student_login(request):
    error_msg = None
    if request.method == "POST":
        user_in = request.POST.get('username')
        pass_in = request.POST.get('password')
        
        # Django checks credentials against database records
        user = authenticate(request, username=user_in, password=pass_in)
        
        if user is not None:
            try:
                # Find the profile linked to this user account
                student_profile = StudentProfile.objects.get(user=user)
                login(request, user)
                # Redirect directly to their print slip page!
                return redirect('student_report_slip', student_id=student_profile.id)
            except StudentProfile.DoesNotExist:
                error_msg = "Account authenticated but no student record found."
        else:
            error_msg = "Invalid username or password. Please try again."

    return render(request, 'results/student_login.html', {'error': error_msg})