from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'exams_scheduler/login.html'

    def get_success_url(self):
        return reverse('exams_scheduler:redirect')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None and user.is_active:
            login(self.request, user)
            super(LoginView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
