from django import forms
from .models import Staff
from staff.models import Teacher





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