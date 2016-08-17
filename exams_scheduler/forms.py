from django import forms
from django.forms import HiddenInput

from exams_scheduler.models import ProfessorDay


class ProfessorDayForm(forms.ModelForm):
    exam_group = HiddenInput(attrs={'disabled': True})

    class Meta:
        model = ProfessorDay
        fields = ['time', 'comment', 'available', 'exam_group']

    def clean_exam_group(self):
        # if professor sets day to unavailable, we clean the exam and notificate group
        # TODO notifications
        if not self.cleaned_data['available']:
            return None

        return self.cleaned_data['exam_group']


class AddExamForm(forms.ModelForm):
    class Meta:
        model = ProfessorDay
        fields = ['exam_group', 'date', 'professor']

