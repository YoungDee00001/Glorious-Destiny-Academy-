import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.conf import settings  # to get EMAIL_HOST_USER
import mimetypes


from accounts.models import User
from .forms import (
    SuperUserUpdateForm,
    CourseForm,
    StudentRegistrationForm,
    TeacherForm,
    StaffDocumentForm,
    StaffFolderForm
)
from students.models import StudentRegistration
from staff.models import Teacher, StaffDocument, StaffFolder
from schoolevents.models import SchoolEvent, EventGallery, EventDocument
from schoolevents.forms import SchoolEventForm, EventGalleryForm, EventDocumentForm
from .models import Course
from django.contrib import messages

from threading import Thread
import time
from datetime import date
from django.core.mail import EmailMessage
from birthdays.utils import send_birthday_email, get_full_name


from django.contrib.admin.views.decorators import staff_member_required


import threading











User = get_user_model()


# =============================================
# SUPERUSER DASHBOARD
# =============================================
class SuperuserAdmin(LoginRequiredMixin, DetailView):
    template_name = 'superuser/superuser.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return render(self.request, "400.html", {})
        return super().dispatch(*args, **kwargs)
    
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
        context['pending_students'] = StudentRegistration.objects.filter(status='pending').count()
        context['pending_staff'] = Teacher.objects.filter(status='pending').count()

        context['staff_count'] = Teacher.objects.count()

        return context
        

        return context   # ✔ Correct


    # return render(request, 'superuser/dashboard.html', context)




# =============================================
# SUPERUSER LIST / DETAIL / UPDATE / DELETE
# =============================================
class SuperUserList(ListView):
    model = User
    template_name = "superuser/superuser_list.html"
    ordering = ['-date_joined']


class SuperUserDetailView(DetailView):
    model = User
    template_name = 'superuser/super-user-detail-view.html'
    context_object_name = 'superuser'


class SuperUserUpdateView(UpdateView):
    model = User
    form_class = SuperUserUpdateForm
    template_name = 'superuser/super-user-update.html'
    success_url = reverse_lazy('SuperUserList')


class SuperUserDeleteView(DeleteView):
    model = User
    template_name = 'superuser/super-user-confirm-delete.html'
    success_url = reverse_lazy('SuperUserList')


# =============================================
# STUDENT REGISTRATION
# =============================================
# class StudentRegisterView(CreateView):
#     form_class = StudentRegistrationForm
#     template_name = 'superuser/student_register.html'
#     success_url = reverse_lazy('super_user_student_list')




def StudentRegisterView(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.status = "approved"  # Auto-approve
            student.save()

            # -----------------------------
            # Send registration email immediately
            # -----------------------------
            email = EmailMessage(
                subject="✅ Student Registration Successful",
                body=f"Congratulations! {student.full_name} has been registered successfully.",
                to=[student.parent_email],
            )
            if student.child_picture:
                email.attach(student.child_picture.name, student.child_picture.read(), 'image/jpeg')
            email.send(fail_silently=True)


            # -----------------------------
            # If today is birthday, send birthday email after 5 minutes
            # -----------------------------
            # check if birthday is today
            today = date.today()
            if student.date_of_birth.month == today.month and student.date_of_birth.day == today.day:

                def delayed():
                    time.sleep(300)  # wait 5 minutes
                    if student.last_birthday_email_sent != today:
                        photo_url = student.child_picture.url if student.child_picture else None
                        send_birthday_email(
                            get_full_name(student),
                            student.parent_email,
                            photo_url
                        )
                        student.last_birthday_email_sent = today
                        student.save(update_fields=["last_birthday_email_sent"])

                threading.Thread(target=delayed, daemon=True).start()

            # -----------------------------
            # Redirect after registration
            # -----------------------------
            return redirect("super_user_student_list")

    else:
        form = StudentRegistrationForm()

    return render(request, "superuser/student_register.html", {"form": form})





class SuperUserStudentListView(ListView):
    model = StudentRegistration
    template_name = "superuser/superuser_student_list.html"
    context_object_name = "students"
    ordering = ['-created_at']


class SuperUserStudentDetailView(DetailView):
    model = StudentRegistration
    template_name = "superuser/superuser_student_detail.html"
    context_object_name = "student"


class SuperUserStudentUpdateView(UpdateView):
    model = StudentRegistration
    form_class = StudentRegistrationForm
    template_name = "superuser/superuser_student_Edit.html"
    success_url = reverse_lazy("super_user_student_list")


class SuperUserStudentDeleteView(DeleteView):
    model = StudentRegistration
    template_name = "superuser/superuser_student_confirm_delete.html"
    success_url = reverse_lazy("super_user_student_list")


# =============================================
# STAFF REGISTRATION
# =============================================
class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "superuser/teacher_list.html"
    context_object_name = "teachers"


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "superuser/teacher_detail.html"
    context_object_name = "teacher"



class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "superuser/teacher_form.html"
    success_url = reverse_lazy("teacher_list")

    def form_valid(self, form):
        staff = form.save(commit=False)
        staff.status = "approved"  # Auto approve
        staff.save()

        # Compose full name
        full_name = get_full_name(staff)

        # Send registration email
        email = EmailMessage(
            subject="✅ Staff Registration Successful",
            body=(
                f"Hello {full_name},\n\n"
                f"Your staff account has been created successfully.\n"
                f"You can now log in and access your staff dashboard.\n\n"
                f"Thank you."
            ),
            to=[staff.user.email]
        )

        # Attach profile picture if exists
        if staff.profile_picture:
            try:
                email.attach(
                    staff.profile_picture.name,
                    staff.profile_picture.read(),
                    "image/jpeg"
                )
            except Exception as e:
                print("Attachment read error:", e)

        try:
            email.send()
        except Exception as e:
            print("Email Error:", e)

        messages.success(
            self.request,
            f"{full_name} has been created and email sent successfully!"
        )

        # --------------------------------------------------
        # 5-MINUTE DELAYED BIRTHDAY EMAIL (ONLY IF TODAY)
        # --------------------------------------------------
        try:
            today = date.today()

            if (
                staff.date_of_birth and
                staff.date_of_birth.month == today.month and
                staff.date_of_birth.day == today.day
            ):
                # do not send twice if already sent today
                if staff.last_birthday_email_sent != today:

                    def send_birthday_email_delayed():
                        time.sleep(300)  # wait 5 minutes

                        # Check again before sending
                        if staff.last_birthday_email_sent != today:
                            photo_url = (
                                staff.profile_picture.url 
                                if staff.profile_picture 
                                else None
                            )

                            send_birthday_email(
                                full_name,
                                staff.user.email,
                                photo_url
                            )

                            # update record so no double sending
                            staff.last_birthday_email_sent = today
                            staff.save(update_fields=["last_birthday_email_sent"])

                    Thread(target=send_birthday_email_delayed, daemon=True).start()

        except Exception as e:
            print("Birthday delay error:", e)

        return super().form_valid(form)



class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "superuser/teacher_form.html"
    success_url = reverse_lazy("teacher_list")
    permission_required = "Teacher.change_teacher"


class TeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Teacher
    template_name = "superuser/teacher_confirm_delete.html"
    success_url = reverse_lazy("teacher_list")
    permission_required = "Teacher.delete_teacher"


class StaffDocumentListView(LoginRequiredMixin, ListView):
    model = StaffDocument
    template_name = "superuser/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        return StaffDocument.objects.filter(staff=self.request.user)


class StaffDocumentCreateView(LoginRequiredMixin, CreateView):
    model = StaffDocument
    form_class = StaffDocumentForm
    template_name = "superuser/document_form.html"
    success_url = reverse_lazy("document_list")

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)


class StaffDocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = StaffDocument
    form_class = StaffDocumentForm
    template_name = "superuser/document_form.html"
    success_url = reverse_lazy("document_list")

    def get_queryset(self):
        return StaffDocument.objects.filter(staff=self.request.user)


class StaffDocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = StaffDocument
    template_name = "superuser/document_confirm_delete.html"
    success_url = reverse_lazy("document_list")

    def get_queryset(self):
        return StaffDocument.objects.filter(staff=self.request.user)


class StaffFolderListView(LoginRequiredMixin, ListView):
    model = StaffFolder
    template_name = "superuser/folder_list.html"
    context_object_name = "folders"

    def get_queryset(self):
        return StaffFolder.objects.filter(staff=self.request.user)


class StaffFolderCreateView(LoginRequiredMixin, CreateView):
    model = StaffFolder
    form_class = StaffFolderForm
    template_name = "superuser/folder_form.html"
    success_url = reverse_lazy("folder_list")

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)


class StaffFolderUpdateView(LoginRequiredMixin, UpdateView):
    model = StaffFolder
    form_class = StaffFolderForm
    template_name = "superuser/folder_form.html"
    success_url = reverse_lazy("folder_list")

    def get_queryset(self):
        return StaffFolder.objects.filter(staff=self.request.user)


class StaffFolderDeleteView(LoginRequiredMixin, DeleteView):
    model = StaffFolder
    template_name = "superuser/folder_confirm_delete.html"
    success_url = reverse_lazy("folder_list")

    def get_queryset(self):
        return StaffFolder.objects.filter(staff=self.request.user)


# =============================================
# SCHOOL EVENTS
# =============================================
class EventListView(LoginRequiredMixin, ListView):
    model = SchoolEvent
    template_name = "superuser/event_list.html"
    context_object_name = "events"
    ordering = ['-start_date']


class EventDetailView(LoginRequiredMixin, DetailView):
    model = SchoolEvent
    template_name = "superuser/event_detail.html"
    context_object_name = "event"


class EventCreateView(LoginRequiredMixin, CreateView):
    model = SchoolEvent
    form_class = SchoolEventForm
    template_name = "superuser/event_form.html"
    success_url = reverse_lazy("event_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, "400.html")
        return super().dispatch(request, *args, **kwargs)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = SchoolEvent
    form_class = SchoolEventForm
    template_name = "superuser/event_form.html"
    success_url = reverse_lazy("event_list")


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = SchoolEvent
    template_name = "superuser/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")


# =============================================
# EVENT GALLERY / DOCUMENT UPLOAD
# =============================================
class EventGalleryUploadView(LoginRequiredMixin, CreateView):
    model = EventGallery
    form_class = EventGalleryForm
    template_name = "superuser/event_gallery_form.html"

    def form_valid(self, form):
        event = SchoolEvent.objects.get(pk=self.kwargs['pk'])
        form.instance.event = event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event_detail", kwargs={'pk': self.kwargs['pk']})


class EventDocumentUploadView(LoginRequiredMixin, CreateView):
    model = EventDocument
    form_class = EventDocumentForm
    template_name = "superuser/event_document_form.html"

    def form_valid(self, form):
        event = SchoolEvent.objects.get(pk=self.kwargs['pk'])
        form.instance.event = event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event_detail", kwargs={'pk': self.kwargs['pk']})


# =============================================
# COURSE MANAGEMENT
# =============================================
class CourseRegistration(CreateView):
    form_class = CourseForm
    template_name = 'superuser/course.html'
    success_url = reverse_lazy('pending_course_list')


def courselistview(request):
    courses = Course.objects.filter(course_registration=True)
    return render(request, 'superuser/course_list_view.html', {"course": courses})


def pendingcourselistview(request):
    courses = Course.objects.filter(course_registration=False)
    return render(request, 'superuser/pending_course_list_view.html', {"course": courses})


class CourseListUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'superuser/CourseListUpdateView.html'
    success_url = reverse_lazy('CourseListView')


class CourseListDeleteView(DeleteView):
    model = Course
    template_name = 'superuser/CourseListDeleteView.html'
    success_url = reverse_lazy('CourseListView')




# ------------------------------
# Pending Students List View
# ------------------------------
def pending_students(request):
    students = StudentRegistration.objects.filter(status='pending')
    context = {
        'students': students,
        'pending_student_count': students.count()
    }
    return render(request, 'superuser/pending_students.html', context)




def approve_student(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)
    student.status = 'approved'
    student.save()

    # Send approval email
    email = EmailMessage(
        subject="✅ Student Registration Approved",
        body=f"Congratulations! {student.full_name} has been approved and is now registered successfully.",
        to=[student.parent_email],  # assuming parent_email field exists
    )
    if student.child_picture:
        email.attach(student.child_picture.name, student.child_picture.read(), 'image/jpeg')
    email.send()

    messages.success(request, f"{student.full_name} has been approved and email sent!")
    return redirect('super_user_student_list')  # redirect to normal student list


def reject_student(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)
    student.delete()
    messages.warning(request, f"{student.full_name} has been rejected and deleted!")
    return redirect('pending_students')


# ------------------------------
# Pending Staff List View
# ------------------------------
def pending_staff(request):
    staffs = Teacher.objects.filter(status='pending')
    context = {
        'staffs': staffs,
        'pending_staff_count': staffs.count()
    }
    return render(request, 'superuser/pending_staff.html', context)


def approve_staff(request, staff_id):
    staff = get_object_or_404(Teacher, id=staff_id)
    staff.status = 'approved'
    staff.save()

    # Send approval email
    email = EmailMessage(
        subject="✅ Staff Registration Approved",
        body=f"Congratulations! {staff.user.get_full_name()} has been approved and is now officially a staff member.",
        to=[staff.user.email],  # assuming user email field
    )
    email.send()

    messages.success(request, f"{staff.user.get_full_name()} has been approved and email sent!")
    return redirect('teacher_list')  # redirect to normal staff list


def reject_staff(request, staff_id):
    staff = get_object_or_404(Teacher, id=staff_id)
    staff.delete()
    messages.warning(request, f"{staff.full_name} has been rejected and deleted!")
    return redirect('pending_staff')
