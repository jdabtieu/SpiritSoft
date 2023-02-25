from django.db import models

from main.models import Student

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

class QuarterlyWinner(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    points = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Pick Quarterly Winners'
        default_permissions = []
        permissions = [
            ('can_view_winners', 'Can view quarterly winners'),
            ('can_pick_winners', 'Can pick quarterly winners'),
        ]