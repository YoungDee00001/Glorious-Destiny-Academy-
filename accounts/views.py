from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import (
    LoginForm,
    RegisterForm,
    StudentProfileForm,
    StaffProfileForm
)

from students.models import StudentRegistration
from staff.models import Teacher


# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------
def home_page(request):
    context = {
        "content": "Welcome to Home Page, by David Thomas",
        "superuser": "davidthomasinimforn@gmail.com",
        "personnal": "Personal Information"
    }
    return render(request, 'accounts/home_page.html', context)


# ----------------------------------------------------
# LOGIN VIEW
# ----------------------------------------------------
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/choose-role/'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("choose_role")

        messages.error(request, "Invalid email or password.")
        return super().form_invalid(form)


# ----------------------------------------------------
# USER ACCOUNT REGISTER (BASIC ACCOUNT)
# ----------------------------------------------------
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created successfully! Please log in.")
        return super().form_valid(form)


# ----------------------------------------------------
# LOGOUT
# ----------------------------------------------------
class LogoutView(View):
    def get(self, request):
        return render(request, 'accounts/logout.html')

    def post(self, request):
        logout(request)
        messages.success(request, 'Logout Successful')
        return redirect('/')


# ----------------------------------------------------
# CHOOSE ROLE PAGE
# ----------------------------------------------------
def choose_role(request):
    return render(request, "accounts/choose_role.html")



# ----------------------------------------------------
# STUDENT REGISTRATION (NO LOGIN NEEDED)
# ----------------------------------------------------
def student_profile_create(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.status = "pending"   # superuser must approve
            student.save()

            messages.warning(
                request,
                "Registration submitted successfully! Pending approval from admin."
            )
            return redirect("home_page")

    else:
        form = StudentProfileForm()

    return render(request, "accounts/student_register.html", {"form": form})



# ----------------------------------------------------
# STAFF PROFILE CREATION (LOGIN REQUIRED)
# ----------------------------------------------------
@login_required
def staff_profile_create(request):
    if request.method == "POST":
        form = StaffProfileForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user = request.user
            staff.status = "pending"   # superadmin must approve
            staff.save()

            messages.warning(
                request,
                "Staff profile created! Waiting for admin approval."
            )
            return redirect("dashboard")
    else:
        form = StaffProfileForm()

    return render(request, "accounts/teacher_form.html", {"form": form})



# =====================================================================
#                     SUPERUSER APPROVAL SECTION
# =====================================================================

# ----------------------------------------------------
# ADMIN – VIEW PENDING STUDENTS
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def admin_pending_students(request):
    students = StudentRegistration.objects.filter(status="pending")
    return render(request, "accounts/admin_pending_students.html", {"students": students})


# ----------------------------------------------------
# ADMIN – APPROVE STUDENT
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def approve_student(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)
    student.status = "approved"
    student.save()

    messages.success(request, f"{student.full_name} has been APPROVED.")
    return redirect("admin_pending_students")


# ----------------------------------------------------
# ADMIN – REJECT STUDENT
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def reject_student(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)
    student.status = "rejected"
    student.save()

    messages.error(request, f"{student.full_name} has been REJECTED.")
    return redirect("admin_pending_students")



# ----------------------------------------------------
# ADMIN – VIEW PENDING STAFF
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def admin_pending_staff(request):
    staff_list = Teacher.objects.filter(status="pending")
    return render(request, "accounts/admin_pending_staff.html", {"staff_list": staff_list})


# ----------------------------------------------------
# ADMIN – APPROVE STAFF
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def approve_staff(request, pk):
    staff = get_object_or_404(Teacher, pk=pk)
    staff.status = "approved"
    staff.save()

    messages.success(request, f"{staff.full_name} has been APPROVED as staff.")
    return redirect("admin_pending_staff")


# ----------------------------------------------------
# ADMIN – REJECT STAFF
# ----------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def reject_staff(request, pk):
    staff = get_object_or_404(Teacher, pk=pk)
    staff.status = "rejected"
    staff.save()

    messages.error(request, f"{staff.full_name} has been REJECTED.")
    return redirect("admin_pending_staff")
