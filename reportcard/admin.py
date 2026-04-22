
from django.contrib import admin
from .models import AcademicYear, Term, Class, Student, Subject, ReportCard, SubjectScore, AffectiveDisposition, PsychomotorSkill 





@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_current']
    list_filter = ['is_current']


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['term', 'academic_year', 'start_date', 'end_date', 'is_current']
    list_filter = ['academic_year', 'term', 'is_current']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_teacher']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'first_name', 'last_name', 'student_class', 'is_active']
    list_filter = ['student_class', 'is_active', 'gender']
    search_fields = ['admission_number', 'first_name', 'last_name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


class SubjectScoreInline(admin.TabularInline):
    model = SubjectScore
    extra = 0


class AffectiveDispositionInline(admin.StackedInline):
    model = AffectiveDisposition


class PsychomotorSkillInline(admin.StackedInline):
    model = PsychomotorSkill


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'term', 'times_present', 'times_absent', 'created_at']
    list_filter = ['term']
    search_fields = ['student__first_name', 'student__last_name', 'student__admission_number']
    inlines = [SubjectScoreInline, AffectiveDispositionInline, PsychomotorSkillInline]