from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

# SpiritSoft doesn't use Django groups
admin.site.unregister(Group)

# Register all the models with appropriate titles
class CustomEventCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Event Categories'}
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(EventCategory, CustomEventCategoryAdmin)

class CustomEventAdmin(admin.ModelAdmin):
    list_filter = ['points']
    search_fields = ['name']
    ordering = ['date', 'name']
    list_display = ['name', 'date', 'category', 'points']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Events'}
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Event, CustomEventAdmin)

class CustomPrizeCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Prize Categories'}
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(PrizeCategory, CustomPrizeCategoryAdmin)

class CustomPrizeAdmin(admin.ModelAdmin):
    list_filter = ['points', 'category__name']
    search_fields = ['name']
    ordering = ['category__name', 'name']
    list_display = ['name', 'category', 'points']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Prizes'}
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Prize, CustomPrizeAdmin)

class CustomAttendanceAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
    list_filter = ['event__points']
    search_fields = ['event__name']
    ordering = ['event__date', 'event__name']

    @admin.display(description='Date', ordering='event__date')
    def get_date(self, obj):
        return obj.event.date
    
    @admin.display(description='Name', ordering='event__name')
    def get_name(self, obj):
        return obj.event.name
    
    @admin.display(description='Category', ordering='event__category')
    def get_category(self, obj):
        return obj.event.category

    @admin.display(description='Points', ordering='event__points')
    def get_points(self, obj):
        return obj.event.points
    
    list_display = ['get_name', 'get_date', 'get_category', 'get_points']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Event Attendance'}
        return super().changelist_view(request, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('event',)
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj:
            return f"{obj._meta.app_label}/{obj._meta.model_name}" not in request.path
        else:
            return False
admin.site.register(Attendance, CustomAttendanceAdmin)


class CustomStudentAdmin(admin.ModelAdmin):
    list_filter = ['grade']
    search_fields = ['first_name', 'last_name', 'number']
    ordering = ['last_name', 'first_name']
    list_display = ['last_name', 'first_name', 'number', 'grade', 'points']

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Students'}
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Student, CustomStudentAdmin)