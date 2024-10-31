from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
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

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    if not request.user.is_staff:
        return render(request, '403.html')  # Handle unauthorized access

    courses = Course.objects.all()
    quota_requests = QuotaRequest.objects.all()

    # Calculate statistics
    stats = {
        'total_courses': courses.count(),
        'total_requests': quota_requests.count(),
        'approved_requests': quota_requests.filter(status='approved').count(),
        'pending_requests': quota_requests.filter(status='pending').count(),
        'canceled_requests': quota_requests.filter(status='canceled').count(),
    }

    context = {
        'courses': courses,
        'stats': stats,
        'quota_requests': quota_requests,
    }
    return render(request, 'admin/dashboard.html', context)