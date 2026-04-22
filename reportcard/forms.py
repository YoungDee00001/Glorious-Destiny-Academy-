from django import forms
from django.forms import inlineformset_factory
from .models import ReportCard, SubjectScore, AffectiveDisposition, PsychomotorSkill

# --------------------------
# ReportCard Form
# --------------------------
class ReportCardForm(forms.ModelForm):
    class Meta:
        model = ReportCard
        fields = [
            'student',
            'term',
            'times_school_opened',
            'times_present',
            'times_absent',
            'class_teacher_comment',
            'headmaster_comment',
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'term': forms.Select(attrs={'class': 'form-control'}),
            'times_school_opened': forms.NumberInput(attrs={'class': 'form-control'}),
            'times_present': forms.NumberInput(attrs={'class': 'form-control'}),
            'times_absent': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_teacher_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'headmaster_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# --------------------------
# SubjectScore Form
# --------------------------
class SubjectScoreForm(forms.ModelForm):
    class Meta:
        model = SubjectScore
        fields = ['subject', 'ca1', 'ca2', 'ca3', 'exam', 'remark']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ca1': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'ca2': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'ca3': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'exam': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'remark': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


# --------------------------
# AffectiveDisposition Form
# --------------------------
class AffectiveDispositionForm(forms.ModelForm):
    class Meta:
        model = AffectiveDisposition
        exclude = ['report_card']
        widgets = {
            'punctuality': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'attentiveness': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'politeness': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'neatness': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'initiative': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'perseverance': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'leadership': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'honesty': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'self_control': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'relationship_with_others': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'emotional_stability': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
        }


# --------------------------
# PsychomotorSkill Form
# --------------------------
class PsychomotorSkillForm(forms.ModelForm):
    class Meta:
        model = PsychomotorSkill
        exclude = ['report_card']
        widgets = {
            'handwriting': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'drawing_painting': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'craft_tools': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'sports_games': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'music': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
            'verbal_fluency': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 5}),
        }


# --------------------------
# SubjectScore Formset
# --------------------------
SubjectScoreFormSet = inlineformset_factory(
    ReportCard,
    SubjectScore,
    form=SubjectScoreForm,
    extra=16,
    can_delete=False
)
