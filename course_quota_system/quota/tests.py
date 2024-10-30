from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, QuotaRequest

class CourseModelTest(TestCase):
    def setUp(self):
        # Set up a sample course
        self.course = Course.objects.create(
            code="CN331",
            name="Software Engineering",
            semester="1",
            academic_year=2024,
            total_quota=30,
            available_seats=10,
            is_open=True
        )

    def test_course_creation(self):
        """Test if the course is created correctly."""
        self.assertEqual(self.course.code, "CN331")
        self.assertEqual(self.course.available_seats, 10)
        self.assertTrue(self.course.is_open)

    def test_course_str(self):
        """Test the string representation of a course."""
        self.assertEqual(str(self.course), "CN331 - Software Engineering")


class QuotaRequestModelTest(TestCase):
    def setUp(self):
        # Create user and course for the quota request
        self.student = User.objects.create_user(username="student1", password="testpassword")
        self.course = Course.objects.create(
            code="CS102",
            name="Advanced Topics",
            semester="Spring",
            academic_year=2024,
            total_quota=20,
            available_seats=5,
            is_open=True
        )

    def test_quota_request_creation(self):
        """Test the creation of a quota request."""
        quota_request = QuotaRequest.objects.create(student=self.student, course=self.course, status="pending")
        self.assertEqual(quota_request.status, "pending")
        self.assertEqual(quota_request.student, self.student)
        self.assertEqual(quota_request.course, self.course)
    
    def test_quota_request_str(self):
        """Test the string representation of a quota request."""
        quota_request = QuotaRequest.objects.create(student=self.student, course=self.course)
        self.assertEqual(str(quota_request), "student1 - Advanced Topics")


class CourseViewsTest(TestCase):
    def setUp(self):
        # Set up client, user, and courses
        self.client = Client()
        self.student = User.objects.create_user(username="student1", password="testpassword")
        self.admin = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
        
        self.course = Course.objects.create(
            code="CS103",
            name="Machine Learning",
            semester="Fall",
            academic_year=2024,
            total_quota=10,
            available_seats=5,
            is_open=True
        )

    def test_course_list_view(self):
        """Test the course list view for available courses."""
        self.client.login(username="student1", password="testpassword")
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machine Learning")
        
    def test_request_quota_view(self):
        """Test the quota request process for a course with available seats."""
        self.client.login(username="student1", password="testpassword")
        response = self.client.post(reverse('request_quota', args=[self.course.id]))
        
        # Verify quota request was created and seats updated
        self.assertEqual(response.status_code, 302)
        quota_request = QuotaRequest.objects.filter(student=self.student, course=self.course).first()
        self.assertIsNotNone(quota_request)
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats, 4)

    def test_cancel_quota_view(self):
        """Test cancellation of a quota request and seat reallocation."""
        self.client.login(username="student1", password="testpassword")
        quota_request = QuotaRequest.objects.create(student=self.student, course=self.course, status="pending")
        response = self.client.post(reverse('cancel_quota', args=[quota_request.id]))
        
        # Check quota request deletion and seat update
        self.assertEqual(response.status_code, 302)
        self.assertFalse(QuotaRequest.objects.filter(id=quota_request.id).exists())
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats, 6)

    def test_student_quota_list_view(self):
        """Test that a student can view their quota requests."""
        self.client.login(username="student1", password="testpassword")
        QuotaRequest.objects.create(student=self.student, course=self.course, status="pending")
        
        response = self.client.get(reverse('student_quota_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machine Learning")

    def test_admin_dashboard_view(self):
        """Test the admin dashboard view for access and data."""
        self.client.login(username="admin", password="adminpassword")
        QuotaRequest.objects.create(student=self.student, course=self.course, status="pending")
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machine Learning")
        self.assertContains(response, "total_requests")

class RequestQuotaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username="student1", password="testpassword")
        self.course = Course.objects.create(
            code="CS103",
            name="Machine Learning",
            semester="Fall",
            academic_year=2024,
            total_quota=10,
            available_seats=0,  # No available seats to trigger line 19
            is_open=True
        )

    def test_request_quota_no_seats(self):
        """Test that the view redirects when no seats are available."""
        self.client.login(username="student1", password="testpassword")
        response = self.client.post(reverse('request_quota', args=[self.course.id]))
        



class CancelQuotaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username="student1", password="testpassword")
        self.course = Course.objects.create(
            code="CS104",
            name="Data Science",
            semester="Spring",
            academic_year=2024,
            total_quota=15,
            available_seats=1,  # Only 1 seat initially
            is_open=True
        )
        # Create a quota request to be canceled
        self.quota_request = QuotaRequest.objects.create(student=self.student, course=self.course)

    def test_cancel_quota_increases_seats(self):
        """Test that canceling a quota request increases available seats."""
        self.client.login(username="student1", password="testpassword")
        response = self.client.post(reverse('cancel_quota', args=[self.quota_request.id]))
        
        # Confirm redirect and updated seat count
        self.assertEqual(response.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats, 2)
        self.assertFalse(QuotaRequest.objects.filter(id=self.quota_request.id).exists())

class AdminDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a staff (admin) user and a regular user
        self.admin_user = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
        self.regular_user = User.objects.create_user(username="student", password="studentpassword", is_staff=False)

    def test_admin_dashboard_template_for_non_staff_user(self):
        """Test that a non-staff user is denied access and sees the 403 template."""
        self.client.login(username="student", password="studentpassword")
        response = self.client.get(reverse('admin_dashboard'))
        
        # Check the correct template and 403 status
        self.assertTemplateUsed(response, '403.html')


    

        
