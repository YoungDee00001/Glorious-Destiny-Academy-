from django.db.models import Count, Q
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from students.models import StudentRegistration, Class


class StaffAdmin(LoginRequiredMixin, DetailView):
    template_name = 'staff/staff.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "400.html")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aggregate student counts by class_applying
        from django.db.models import Value, CharField

        class_choices = dict(StudentRegistration.CLASS_CHOICES)

        # Build a list of dicts with counts per class_applying
        classes_data = []

        for class_key, class_name in class_choices.items():
            total_students = StudentRegistration.objects.filter(class_applying=class_key).count()
            boys_count = StudentRegistration.objects.filter(class_applying=class_key, gender='male').count()
            girls_count = StudentRegistration.objects.filter(class_applying=class_key, gender='female').count()

            classes_data.append({
                'class_key': class_key,
                'class_name': class_name,
                'total_students': total_students,
                'boys_count': boys_count,
                'girls_count': girls_count,
            })

        context['classes_data'] = classes_data
        context['total_classes'] = len(classes_data)

        # Optional: total students overall
        context['student_count'] = StudentRegistration.objects.count()

        return context
