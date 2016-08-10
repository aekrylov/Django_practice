from django.contrib import admin

# Register your models here.
from exams_scheduler.models import Professor, Group

admin.site.register(Professor)
admin.site.register(Group)