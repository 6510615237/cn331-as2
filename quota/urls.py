from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('request_quota/<int:course_id>/', views.request_quota, name='request_quota'),
    path('cancel_quota/<int:quota_id>/', views.cancel_quota, name='cancel_quota'),
    path('quota/cancel/<int:quota_request_id>/', views.cancel_quota, name='cancel_quota'),
    path('quota/student_requests/', views.student_quota_list, name='student_quota_list'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
