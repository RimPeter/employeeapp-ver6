from django.contrib import admin
from .models import JobsDone, ClockIn, Employee

admin.site.register(JobsDone)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(ClockIn)
class ClockInAdmin(admin.ModelAdmin):
    list_display = ['employee', 'clock_in_time', 'clock_out_time']
    




