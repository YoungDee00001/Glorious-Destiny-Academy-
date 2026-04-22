from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Course
from students.models import StudentRegistration
from staff.models import Teacher, StaffDocument, StaffFolder
from django.core.exceptions import ValidationError
import re

User = get_user_model()



class SuperUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'active',
            'staff',
            'admin',
            'superuser',
            'students',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }


# ======== StudentRegistrationForm ==========
# ======== StudentRegistrationForm ==========
class StudentRegistrationForm(forms.ModelForm):
    # Override the gender field to add empty option
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + list(StudentRegistration.GENDER_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = StudentRegistration
        fields = [
            'surname',
            'first_name',
            'middle_name',
            'date_of_birth',
            'gender',
            'state_of_origin',
            'address',
            'class_applying',
            'child_picture',
            'previous_school',
            'medical_conditions',
            'parent_phone',
            'parent_email',
        ]

        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),

            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            # Gender is now defined above as a field override
            
            'state_of_origin': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'class_applying': forms.Select(attrs={'class': 'form-control'}),

            'child_picture': forms.FileInput(attrs={'class': 'form-control'}),

            'previous_school': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Parent Phone Number'
            }),

            'parent_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Parent Email'
            }),
        }
        
        labels = {
            'gender': 'Gender',
            'child_picture': 'Child Passport Photo',
            'class_applying': 'Class Applying For',
        }




# staff Registration Form
class DateInput(forms.DateInput):
    input_type = 'date'
    

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),  # Use nice date picker
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary', '')
        if not re.match(r'^[0-9,]*$', salary):
            raise ValidationError("Salary can only contain digits and commas.")
        return salary



# staff document
class StaffDocumentForm(forms.ModelForm):
    class Meta:
        model = StaffDocument
        fields = [
            'staff', 'document_type', 'document_title',
            'document_file', 'description', 'folder_name'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'folder_name': forms.TextInput(attrs={'placeholder': 'e.g. Certificates'}),
        }


# staff folder
class StaffFolderForm(forms.ModelForm):
    class Meta:
        model = StaffFolder
        fields = ['staff', 'folder_name', 'description']

        widgets = {
            'folder_name': forms.TextInput(attrs={'placeholder': 'Folder Name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }





# Course Form
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course_name', 'registration_date', 'course_registration',) 

