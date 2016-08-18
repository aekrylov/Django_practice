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
from django.views.generic.base import ContextMixin

from exams_scheduler.forms import ProfessorDayForm
from .models import ProfessorDay, Professor

import datetime


def is_prof(user):
    try:
        return user.professor is not None
    except:
        return False


def is_group(user):
    try:
        return user.group is not None
    except:
        return False


class UserIsProfessorMixin(UserPassesTestMixin):
    def test_func(self):
        return is_prof(self.request.user)


class UserIsStudentMixin(UserPassesTestMixin):
    def test_func(self):
        return is_group(self.request.user)


@login_required()
def redirect(request):
    url = 'exams_scheduler:professor_index' if is_prof(request.user) else 'exams_scheduler:student_index'
    return HttpResponseRedirect(reverse(url))


def get_calendar(professor, month=6):
    """
    get calendar for given month
    :return:
    """
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


class CalendarMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(CalendarMixin, self).get_context_data(**kwargs)
        professor = self.request.user.professor if is_prof(self.request.user) else\
            get_object_or_404(Professor, pk=self.kwargs['professor_id'])

        context['weeks'] = get_calendar(professor)

        return context


def get_professor_day(professor_id, date):
    return ProfessorDay.objects.get_or_create(professor_id=professor_id, date=date)


class ProfessorView(CalendarMixin, UserIsProfessorMixin, generic.TemplateView):
    template_name = 'exams_scheduler/professor_index.html'


class ProfessorDayView(CalendarMixin, UserIsProfessorMixin, generic.UpdateView):
    context_object_name = 'day'
    template_name = 'exams_scheduler/professor_day.html'
    form_class = ProfessorDayForm

    def get_success_url(self):
        return reverse('exams_scheduler:professor_index')

    def get_object(self, queryset=None):
        date = datetime.date.today().replace(month=int(self.kwargs['month']), day=int(self.kwargs['day']))
        day, created = get_professor_day(self.request.user.professor.id, date)

        return day


class StudentIndexView(UserIsStudentMixin, generic.ListView):
    context_object_name = 'professors'
    template_name = 'exams_scheduler/student_index.html'

    def get_queryset(self):
        return Professor.objects.all()


class StudentDetailView(CalendarMixin, UserIsStudentMixin, generic.ListView):
    context_object_name = 'days'
    template_name = 'exams_scheduler/student_detail.html'

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
