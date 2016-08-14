from django.conf.urls import url, include
from django.contrib.auth.views import auth_login
from django.views.generic import TemplateView
from .views import *

app_name = 'exams_scheduler'

urlpatterns = [
    url(r'^$', redirect, name='redirect'),

    url(r'^student/', include([
        url(r'^$', TemplateView.as_view(template_name='exams_scheduler/student_index.html'), name='student_index'),
        url(r'^(?P<professor_id>[0-9]+)/$', StudentDetailView.as_view(), name='student_detail'),
        url(r'^add/$', student_add),
        url(r'^delete/$', student_delete)
    ])),

    url(r'^professor/', include([
        url(r'^$', ProfessorView.as_view(), name='professor_index'),
        url(r'^(?P<day>[0-9]{2})-(?P<month>[0-9]{2})/$', ProfessorDayView.as_view(), name='professor_day')
    ]))
]