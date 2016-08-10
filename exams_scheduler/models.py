from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=50)
    name_short = models.CharField(max_length=16)
    subject_longname = models.CharField(max_length=50)
    subject_shortname = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name_short


class Exam(models.Model):
    date = models.DateField()
    group = models.ForeignKey(Group)
    professor = models.ForeignKey(Professor)

    def __unicode__(self):
        return "%s of %s" % (self.professor.subject_shortname, self.group)


class ProfessorDay(models.Model):
    date = models.DateField()
    professor = models.ForeignKey(Professor)
    available = models.BooleanField(default=True)
    time = models.TimeField(null=True)
    comment = models.TextField(null=True)

    def __unicode__(self):
        return "%s @ %s" % (self.professor, self.date)
