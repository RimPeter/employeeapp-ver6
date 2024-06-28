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
    
class ClockIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField(null=True, blank=True)
    worked_hours = models.DurationField(null=True, blank=True)

    def clock_out(self):
        if not self.clocked_out:
            self.clocked_out = timezone.now()
            self.worked_hours = self.clocked_out - self.clocked_in
            self.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.clocked_in} to {self.clocked_out}"
