# forms.py
from django import forms
from .models import FeeRecord, Student




class StudentForm(forms.ModelForm):
    """Form for creating/editing students"""
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'class_name', 'parent_email', 'parent_phone', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FeeRecordForm(forms.ModelForm):
    """Form for creating fee records"""
    class Meta:
        model = FeeRecord
        fields = [
            'student', 'fee_amount', 'due_date', 'fee_type', 
            'academic_term', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fee_type': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_term': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PaymentForm(forms.Form):
    """Form for recording manual payments"""
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('Cash', 'Cash'),
            ('Check', 'Check'),
            ('Bank Transfer', 'Bank Transfer'),
            ('Online', 'Online Payment'),
            ('Card', 'Credit/Debit Card'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    transaction_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )