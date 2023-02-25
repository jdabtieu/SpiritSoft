from django.db import models

class ImportStudents(models.Model):
    class Meta:
        verbose_name_plural = 'Import Students'
        default_permissions = []
        permissions = [('can_import_students', 'Can import students')]

class CreateReport(models.Model):
    class Meta:
        verbose_name_plural = 'Create Report'
        default_permissions = []
        permissions = [('can_create_report', 'Can create report')]