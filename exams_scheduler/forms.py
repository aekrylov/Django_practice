from django import forms

from exams_scheduler.models import ProfessorDay


class ProfessorDayForm(forms.ModelForm):
    class Meta:
        model = ProfessorDay
        fields = ['time', 'comment', 'available']
