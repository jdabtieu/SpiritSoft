from django.db import models

# Create your models here.
class ImportStudents(models.Model):
    class Meta:
        verbose_name_plural = 'Import Students'
        default_permissions = []
        permissions = [('can_import_students', 'Can import students')]