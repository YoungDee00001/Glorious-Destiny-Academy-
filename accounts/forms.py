from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from .models import User

from students.models import StudentRegistration
from staff.models import Teacher

User = get_user_model()


# -----------------------------------------------------
# ADMIN USER CREATION FORM
# -----------------------------------------------------
class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# -----------------------------------------------------
# ADMIN USER UPDATE FORM
# -----------------------------------------------------
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


# -----------------------------------------------------
# LOGIN FORM
# -----------------------------------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


# -----------------------------------------------------
# REGISTER FORM
# -----------------------------------------------------
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# -----------------------------------------------------
# STUDENT PROFILE FORM (FIXED)
# -----------------------------------------------------
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        exclude = ["user", "status", "created_at", "updated_at"]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }


# -----------------------------------------------------
# STAFF PROFILE FORM
# -----------------------------------------------------
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ["user", "status", "created_at", "updated_at"]
