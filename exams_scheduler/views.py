from calendar import Calendar

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import generic

from exams_scheduler.forms import ProfessorDayForm
from .models import ProfessorDay

import datetime


def get_professor(request):
    return request.user.professor


def is_prof(user):
    try:
        is_prof = user.professor is not None
    except:
        is_prof = False

    return is_prof


def is_group(user):
    try:
        is_group = user.group is not None
    except:
        is_group = False
    return is_group


def get_calendar(professor, month=6):
    '''
    get calendar for given month
    :return:
    '''
    now = datetime.datetime.now().date().replace(month=month)

    events = ProfessorDay.objects.filter(professor=professor)

    calendar = Calendar(0)
    weeks = calendar.monthdayscalendar(month=month, year=now.year)
    days = dict(
        map(lambda entry: (entry.date.day, {'date': entry.date,
                                            'available': entry.available,
                                            'exam': entry.exam_group}
                           ), events)
    )

    weeks = map(lambda week: map(lambda day: days[day] if day in days else {}, week), weeks)
    return weeks


def get_professor_day(professor_id, date):
    return ProfessorDay.objects.get_or_create(professor_id=professor_id, date=date)

@login_required()
def redirect(request):
    url = 'exams_scheduler:professor_index' if is_prof(request) else 'exams_scheduler:student_index'
    return HttpResponseRedirect(reverse(url))


class ProfessorView(UserPassesTestMixin, generic.ListView):
    context_object_name = 'days'
    template_name = 'exams_scheduler/professor_index.html'
    model = ProfessorDay

    test_func = lambda x: is_prof(x.request.user)

    def get_queryset(self):
        return ProfessorDay.objects.filter(professor__user=self.request.user)


class ProfessorDayView(UserPassesTestMixin, generic.UpdateView):
    context_object_name = 'day'
    template_name = 'exams_scheduler/professor_day.html'
    form_class = ProfessorDayForm

    test_func = lambda x: is_prof(x.request.user)

    def get_success_url(self):
        return reverse('exams_scheduler:professor_index')

    def get_object(self, queryset=None):
        date = datetime.date(datetime.datetime.now().year, int(self.kwargs['month']), int(self.kwargs['day']))
        day, created = get_professor_day(self.request.user.professor.id, date)

        return day

    def get_context_data(self, **kwargs):
        context = super(ProfessorDayView, self).get_context_data(**kwargs)

        days = ProfessorDay.objects.filter(professor=self.request.user.professor)
        weeks = get_calendar(professor=self.request.user.professor)
        context['days'] = days
        context['weeks'] = weeks

        return context


class StudentDetailView(UserPassesTestMixin, generic.ListView):
    context_object_name = 'days'
    template_name = 'exams_scheduler/student_detail.html'

    test_func = lambda x: is_group(x.request.user)

    def get_queryset(self):
        return ProfessorDay.objects.filter(professor_id=self.kwargs['professor_id'])


@user_passes_test(is_group)
def student_add(request):
    professor_id = int(request.GET['professor_id'])
    group = request.user.group

    (day, created) = ProfessorDay.objects.get_or_create(professor_id=professor_id,
                                                        date=request.GET['date'],
                                                        exam_group=None)
    if day.exam_group is not None:
        return HttpResponseNotAllowed('This professor is already busy this day')
    if not day.available:
        return HttpResponseNotAllowed('This professor is not available')

    day.exam_group = group
    day.save()
    return HttpResponse('OK')


@user_passes_test(is_group)
def student_delete(request):
    professor_id = int(request.GET['professor_id'])
    date = request.GET['date']
    group = request.user.group

    day = get_object_or_404(ProfessorDay, professor_id=professor_id, date=date, exam_group=group)
    day.exam_group = None
    day.save()

    return HttpResponse('OK')
