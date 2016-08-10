from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views import generic

from exams_scheduler.forms import ProfessorDayForm
from .models import Professor, ProfessorDay, Exam, Group

import datetime


def get_professor(request):
    #TODO
    id = 2 #request.user.id
    return Professor.objects.get()


def professor_index(request):
    professor = get_professor(request)
    days = ProfessorDay.objects.filter(professor=professor)
    exams = Exam.objects.filter(professor=professor)

    context = {
        'days': days,
        'exams': exams
    }
    return render(request, 'exams_scheduler/professor_index.html', context=context)


class ProfessorDayView(generic.UpdateView):

    context_object_name = 'day'
    template_name = 'exams_scheduler/professor_day.html'
    model = ProfessorDay
    form_class = ProfessorDayForm

    def get_success_url(self):
        return reverse('exams_scheduler:professor_index')

    def get_object(self, queryset=None):
        professor = get_professor(self.request)
        date = datetime.date(datetime.datetime.now().year, int(self.kwargs['month']), int(self.kwargs['day']))

        defaults = {
            'professor': professor,
            'date': date
        }
        day, created = ProfessorDay.objects.get_or_create(defaults=defaults, professor=professor, date=date)

        return day

    def get_context_data(self, **kwargs):
        context = super(ProfessorDayView, self).get_context_data(**kwargs)

        professor = get_professor(self.request)
        days = ProfessorDay.objects.filter(professor=professor)
        exams = Exam.objects.filter(professor=professor)

        context['days'] = days
        context['exams'] = exams

        return context


def student_detail(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    group = Group.objects.get(pk=request.user.id)

    context = {
        'busy': ProfessorDay.objects.filter(professor=professor, available=False),
        'exam': Exam.objects.filter(group=group, professor=professor)
    }
    return render(request, 'exams_scheduler/student_detail.html', context=context)


def student_add(request):
    #TODO student add
    pass


def student_delete(request):
    #TODO student delete
    pass
