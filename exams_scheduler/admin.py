from django.contrib import admin

# Register your models here.
from exams_scheduler.models import Professor, Group, ProfessorDay

admin.site.register(Professor)
admin.site.register(Group)
admin.site.register(ProfessorDay)