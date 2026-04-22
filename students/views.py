from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User


User = get_user_model()

class StudentAdmin(LoginRequiredMixin, DetailView):
    template_name = 'student/student.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_students:
            return render(self.request, "400.html", {})
        return super(StudentAdmin, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(StudentAdmin, self).get_context_data(*args, **kwargs)
        return context





# class SuperUserStudentListView(ListView):
#     model = StudentRegistration
#     template_name = "superuser/superuser_student_list.html"
#     context_object_name = "students"
#     ordering = ['-created_at']


# class SuperUserStudentDetailView(DetailView):
#     model = StudentRegistration
#     template_name = "superuser/superuser_student_detail.html"
#     context_object_name = "student"


# class SuperUserStudentUpdateView(UpdateView):
#     model = StudentRegistration
#     form_class = StudentRegistrationForm
#     template_name = "superuser/superuser_student_Edit.html"
#     success_url = reverse_lazy("super_user_student_list")


# class SuperUserStudentDeleteView(DeleteView):
#     model = StudentRegistration
#     template_name = "superuser/superuser_student_confirm_delete.html"
#     success_url = reverse_lazy("super_user_student_list")




# # ------------------------------
# # Pending Students List View
# # ------------------------------
# def pending_students(request):
#     students = StudentRegistration.objects.filter(status='pending')
#     context = {
#         'students': students,
#         'pending_student_count': students.count()
#     }
#     return render(request, 'superuser/pending_students.html', context)




# def approve_student(request, student_id):
#     student = get_object_or_404(StudentRegistration, id=student_id)
#     student.status = 'approved'
#     student.save()

#     # Send approval email
#     email = EmailMessage(
#         subject="✅ Student Registration Approved",
#         body=f"Congratulations! {student.full_name} has been approved and is now registered successfully.",
#         to=[student.parent_email],  # assuming parent_email field exists
#     )
#     if student.child_picture:
#         email.attach(student.child_picture.name, student.child_picture.read(), 'image/jpeg')
#     email.send()

#     messages.success(request, f"{student.full_name} has been approved and email sent!")
#     return redirect('super_user_student_list')  # redirect to normal student list


# def reject_student(request, student_id):
#     student = get_object_or_404(StudentRegistration, id=student_id)
#     student.delete()
#     messages.warning(request, f"{student.full_name} has been rejected and deleted!")
#     return redirect('pending_students')

