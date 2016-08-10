from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20)


class Professor(models.Model):
    name = models.CharField(max_length=50)
    subject_longname = models.CharField(max_length=50)
    subject_shortname = models.CharField(max_length=15)


class Exam(models.Model):
    date = models.DateField()
    group = models.ForeignKey(Group)
    professor = models.ForeignKey(Professor)


class ProfessorDay(models.Model):
    date = models.DateField()
    available = models.BooleanField(default=True)
    time = models.TimeField()
    
