from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.db.models import F
from django.db.models.functions import Greatest
from django.db.models.signals import m2m_changed, pre_delete, pre_save, post_save
from django.dispatch import receiver


class Student(models.Model):
    """
    Data about a student.
    """
    last_name = models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    first_name = models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    number = models.PositiveIntegerField(unique=True, verbose_name='Student Number')
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    email = models.EmailField(max_length=180, validators=[MinLengthValidator(1)])
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.number}) - {self.grade}'

    def save(self, *args, **kwargs):
        self.points = max(self.points, 0)
        super(Student, self).save(*args, **kwargs)


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
        return f'{self.name} ({self.date}) {self.points}pts'

class Attendance(models.Model):
    """
    Tracks attendance for students in events
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    class Meta:
        verbose_name_plural = 'attendance'

    def __str__(self):
        return str(self.event)

@receiver(post_save, sender=Event)
def create_attendance(sender, instance, created, **kwargs):
    if created:
        Attendance.objects.create(event=instance).save()

@receiver(pre_save, sender=Event)
def update_event_points(sender, instance, **kwargs):
    if instance.pk is None:  # Object being created
        return
    try:
        old_inst = Event.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        return  # Object being imported
    diff = instance.points - old_inst.points
    instance.attendance.students.all().update(points=Greatest(F('points') + diff, 0))

@receiver(pre_delete, sender=Event)
def delete_event_points(sender, instance, **kwargs):
    instance.attendance.students.all().update(points=Greatest(F('points') - instance.points, 0))


@receiver(m2m_changed, sender=Attendance.students.through)
def update_attendance(sender, instance, action, pk_set, **kwargs):
    if action == "pre_add":
        s = Student.objects.filter(pk__in=pk_set)
        s.update(points=F('points') + instance.event.points)
    elif action == "pre_remove":
        s = Student.objects.filter(pk__in=pk_set)
        s.update(points=Greatest(F('points') - instance.event.points, 0))

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
        return f'{self.name} ({self.category}) {self.points}pts'