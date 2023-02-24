from django.contrib import admin

from .models import *


admin.site.register(Student)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(PrizeCategory)
admin.site.register(Prize)

class CustomAttendanceAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('event',)
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Attendance, CustomAttendanceAdmin)