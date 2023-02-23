from django.contrib import admin

from .models import *


admin.site.register(Student)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(PrizeCategory)
admin.site.register(Prize)

class CustomAttendanceAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']

admin.site.register(Attendance, CustomAttendanceAdmin)