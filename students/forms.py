from django import forms
from .models import StudentFee, FeeReminder
from students.models import StudentRegistration






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

class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = StudentFee
        fields = ['student', 'amount', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show approved students
        self.fields['student'].queryset = StudentRegistration.objects.filter(status='approved')
        self.fields['student'].label_from_instance = lambda obj: obj.get_full_name()
        

class FeeReminderForm(forms.ModelForm):
    class Meta:
        model = FeeReminder
        fields = ['student_fee', 'reminder_type', 'message_sent']
        widgets = {
            'student_fee': forms.Select(attrs={'class': 'form-select'}),
            'reminder_type': forms.Select(attrs={'class': 'form-select'}),
            'message_sent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only student fee records
        self.fields['student_fee'].label_from_instance = lambda obj: f"{obj.student.get_full_name()} - ₦{obj.amount}"

