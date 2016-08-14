from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone

# Create your models here.


class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    name_short = models.CharField(max_length=16)
    subject_longname = models.CharField(max_length=50)
    subject_shortname = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name_short


class ProfessorDay(models.Model):
    date = models.DateField()
    professor = models.ForeignKey(Professor)
    available = models.BooleanField(default=True)
    time = models.TimeField(null=True, blank=True)
    comment = models.TextField(default='', blank=True)

    exam_group = models.ForeignKey(Group, null=True, blank=True, default=None)

    def __unicode__(self):
        return "%s @ %s (%s)" % (self.professor, self.date, self.exam_group)

    def clean(self):
        if self.exam_group is None:
            # Not scheduling an exam so nothing to check
            return

        if not self.available:
            raise ValidationError('Professor is not available this day')

        nearby_dates = ProfessorDay.objects.filter(date__gte=self.date + timezone.timedelta(days=-3),
                                           date__lte=self.date + timezone.timedelta(days=3)) \
            .exclude(pk=self.id)

        if nearby_dates.filter(exam_group=self.exam_group).count() > 0:
            raise ValidationError('Group must have at least 3 days between exams')

        if nearby_dates.filter(professor=self.professor, date=self.date).count() > 0:
            raise ValidationError('Professor can have only 1 exam per day')
