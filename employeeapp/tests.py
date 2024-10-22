from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import JobsDone, ClockIn, Employee, Profile
from .forms import CustomUserCreationForm, LoginForm, JobsDoneForm, UpdateJobForm, ProfileForm

class EmployeeAppViewsTestCase(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        # Create a profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            date_of_birth='1990-01-01',  # Add a valid date of birth
            address='123 Test Street',
            phone_number='1234567890',
            email_address='testuser@example.com'
        )

        # Create an employee linked to the user
        self.employee = Employee.objects.create(
            user=self.user,
            name='Test Employee'
        )

        # Log the user in
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/index.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/register.html')

        # Test POST request with valid data
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        # Access login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/login.html')

        # Test POST request with valid credentials
        self.client.logout()  # Ensure no user is logged in
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/dashboard.html')

    def test_add_job_view(self):
        response = self.client.get(reverse('add-job'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/create-record.html')

        # Test POST request with valid data
        response = self.client.post(reverse('add-job'), {
            'job_title': 'painting',
            'job_done_in_hours': 5,
        })
        print("Response status code:", response.status_code)
        if response.status_code == 200 and response.context:
            # Form did not validate, print errors
            print("Form errors:", response.context['form'].errors)
            # Optionally, fail the test if form validation failed unexpectedly
            self.fail("Form did not validate as expected.")
        elif response.status_code == 302:
            # Form submitted successfully, proceed with assertions
            self.assertRedirects(response, reverse('dashboard'))
            # Verify that the job was created
            self.assertTrue(JobsDone.objects.filter(job_title='painting').exists())
        else:
            # Unexpected status code
            self.fail(f"Unexpected status code: {response.status_code}")

    def test_update_job_view(self):
        # Create a job to update
        job = JobsDone.objects.create(
        job_title='painting',  # Must be one of the choices in JOB_DESCRIPTIONS
        job_done_in_hours=5,
        worker=self.user
        )
        response = self.client.get(reverse('update-job', kwargs={'pk': job.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/update-record.html')

        # Test POST request to update job
        response = self.client.post(reverse('update-job', kwargs={'pk': job.pk}), {
            'job_title': 'flooring',
            'job_done_in_hours': 8,
        })
        self.assertEqual(response.status_code, 302)
        job.refresh_from_db()
        self.assertEqual(job.job_title, 'flooring')

    def test_delete_job_view(self):
        # Create a job to delete
        job = JobsDone.objects.create(
            job_title='painting',
            job_done_in_hours=5,
            worker=self.user
        )
        response = self.client.get(reverse('delete-job', kwargs={'pk': job.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(JobsDone.objects.filter(pk=job.pk).exists())

    def test_clock_in_view(self):
        response = self.client.get(reverse('employee-clockin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeeapp/clockin.html')

        # Test clocking in
        response = self.client.post(reverse('employee-clockin'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ClockIn.objects.filter(employee=self.employee).exists())


    def test_clock_out_view(self):
        # First, clock in
        ClockIn.objects.create(employee=self.employee)

        response = self.client.post(reverse('employee-clockin'))
        self.assertEqual(response.status_code, 302)
        clock_in_instance = ClockIn.objects.get(employee=self.employee)
        self.assertIsNotNone(clock_in_instance.clock_out_time)

    def test_create_profile_view(self):
        # Delete existing profile
        self.profile.delete()

        response = self.client.post(reverse('create_profile'), {
            'first_name': 'New',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',  # Required field
            'address': '456 New Street',     # Required field
            'phone_number': '0987654321',    # Required field
            'email_address': 'newuser@example.com',  # Required field
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())


    def test_edit_profile_view(self):
        response = self.client.post(reverse('edit_profile', kwargs={'pk': self.profile.pk}), {
            'first_name': 'Updated',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'address': '789 Updated Street',
            'phone_number': '1122334455',
            'email_address': 'updateduser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')


    def test_delete_profile_view(self):
        response = self.client.post(reverse('delete_profile', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())
