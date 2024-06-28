from django.contrib import admin
from .models import JobsDone, ClockIn

admin.site.register(JobsDone)


class ClockInAdmin(admin.ModelAdmin):
    list_display = ('worker', 'clock_in_time', 'clock_out_time')
    readonly_fields = ('clock_in_time', 'clock_out_time')
    search_fields = ('worker__username',)
    list_filter = ('clock_in_time', 'clock_out_time')

admin.site.register(ClockIn, ClockInAdmin)



