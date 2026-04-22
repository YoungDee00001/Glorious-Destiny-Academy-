from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
# from django.contrib.auth.decorators import login_required
from students.models import StudentRegistration
from staff.models import Teacher



User = get_user_model()

class Administration(LoginRequiredMixin, DetailView):
    template_name = 'administration/administration.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_admin:
            return render(self.request, "400.html", {})
        return super(Administration, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Administration, self).get_context_data(*args, **kwargs)
        return context

    def get_context_data(self, *args, **kwargs):
        context = super(Administration, self).get_context_data(*args, **kwargs)
        context['student_count'] = StudentRegistration.objects.count()
        context['staff_count'] = Teacher.objects.count()
        context['pending_students'] = StudentRegistration.objects.filter(status='pending').count()
        context['pending_staff'] = Teacher.objects.filter(status='pending').count()
        return context
