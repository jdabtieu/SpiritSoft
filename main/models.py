from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    """
    Data about a student.
    """
    last_name = models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    first_name = models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    number = models.PositiveIntegerField(unique=True)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    email = models.EmailField(max_length=180, validators=[MinLengthValidator(1)])
    points = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.number}) - {self.grade}'


class EventCategory(models.Model):
    """
    Event categories, such as Athletic and School Spirit
    """
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])

    class Meta:
        verbose_name_plural = 'event categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Data about an event
    """
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    date = models.DateField()
    points = models.PositiveIntegerField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.date})'

class Attendance(models.Model):
    """
    Tracks attendance for students in events
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    class Meta:
        verbose_name_plural = 'attendance'

    def __str__(self):
        return str(self.event)

@receiver(post_save, sender=Event)
def update_attendance(sender, instance, created, **kwargs):
    if created:
        Attendance.objects.create(event=instance).save()

class PrizeCategory(models.Model):
    """
    Prize categories, such as Pizza and Clothing
    """
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])

    class Meta:
        verbose_name_plural = 'prize categories'

    def __str__(self):
        return self.name


class Prize(models.Model):
    """
    Data about an event
    """
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    points = models.PositiveIntegerField()
    category = models.ForeignKey(PrizeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.category})'