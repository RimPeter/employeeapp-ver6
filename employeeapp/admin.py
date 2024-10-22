from django.contrib import admin
from .models import JobsDone, ClockIn, Employee, Profile

admin.site.register(JobsDone)

class ClockInInline(admin.TabularInline):
    model = ClockIn
    extra = 0
    readonly_fields = ('clock_in_time',)
    fields = ('clock_in_time', 'clock_out_time')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    inlines = [ClockInInline]

@admin.register(ClockIn)
class ClockInAdmin(admin.ModelAdmin):
    list_display = ['employee', 'clock_in_time', 'clock_out_time']
    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'phone_number')




