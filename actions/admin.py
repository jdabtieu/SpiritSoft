from django.contrib import admin

from .models import *

# Register all the models with appropriate titles
# Remove the add and delete buttons for these custom pages
class CustomImportStudentsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ImportStudents, CustomImportStudentsAdmin)

class CustomCreateReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(CreateReport, CustomCreateReportAdmin)

class CustomQuarterlyWinnerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(QuarterlyWinner, CustomQuarterlyWinnerAdmin)

class CustomImportBackupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ImportBackup, CustomImportBackupAdmin)