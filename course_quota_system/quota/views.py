from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, QuotaRequest
from django.contrib.auth.decorators import login_required

@login_required
def course_list(request):
    available_courses = Course.objects.filter(is_open=True)
    return render(request, 'quota/course_list.html', {'courses': available_courses})

def request_quota(request, course_id):
    course = Course.objects.get(id=course_id)
    if course.available_seats > 0:
        QuotaRequest.objects.create(student=request.user, course=course)
        course.available_seats -= 1
        course.save()
        return redirect('course_list')
    else:
        return render(request, 'quota/no_seats_available.html')

@login_required
def cancel_quota(request, quota_request_id):
    quota_request = get_object_or_404(QuotaRequest, id=quota_request_id, student=request.user)
    quota_request.course.available_seats += 1
    quota_request.course.save()
    quota_request.delete()
    
    return redirect('student_quota_list')

@login_required
def student_quota_list(request):
    # Get all quota requests for the logged-in student
    quota_requests = QuotaRequest.objects.filter(student=request.user)
    
    # Render the student's quota request page
    return render(request, 'quota/student_quota_list.html', {'quota_requests': quota_requests})
