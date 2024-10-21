from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class JobsDone(models.Model):
    
    JOB_DESCRIPTIONS = [
        ('painting', 'Painting'),
        ('drywall_installation', 'Drywall Installation'),
        ('flooring', 'Flooring'),
        ('plumbing', 'Plumbing'),
        ('electrical_work', 'Electrical Work'),
        ('carpentry', 'Carpentry'),
        ('hvac_installation', 'HVAC Installation'),
        ('tile_work', 'Tile Work'),
        ('cabinet_installation', 'Cabinet Installation'),
        ('insulation', 'Insulation'),
        ('lighting_installation', 'Lighting Installation'),
        ('window_installation', 'Window Installation'),
        ('door_installation', 'Door Installation'),
        ('bathroom_remodeling', 'Bathroom Remodeling'),
        ('kitchen_remodeling', 'Kitchen Remodeling'),
    ]
    worker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='jobs_done')
    job_title = models.CharField(max_length=50, choices=JOB_DESCRIPTIONS)
    job_done_in_hours = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title
    

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClockIn(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(default=timezone.now)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.clock_in_time} - {self.clock_out_time}"

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('You must be at least 18 years old.')

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(validators=[validate_age])
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'