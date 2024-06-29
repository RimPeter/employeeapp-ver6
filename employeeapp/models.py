from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    select_user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname
    
    # name = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.name

class ClockIn(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(default=timezone.now)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{Employee} - {self.clock_in_time} - {self.clock_out_time}"