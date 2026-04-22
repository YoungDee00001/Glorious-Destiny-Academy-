from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class AcademicYear(models.Model):
    year = models.CharField(max_length=20, unique=True)  # e.g., "2024/2025"
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year
    
    class Meta:
        ordering = ['-year']


class Term(models.Model):
    TERM_CHOICES = [
        ('1', 'First Term'),
        ('2', 'Second Term'),
        ('3', 'Third Term'),
    ]
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=1, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_term_display()} - {self.academic_year.year}"
    
    class Meta:
        unique_together = ['academic_year', 'term']
        ordering = ['-academic_year', '-term']


class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., "JSS 1A", "Primary 3"
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <- dynamic reference
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['name']


class Student(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    parent_name = models.CharField(max_length=200)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField(blank=True)
    date_admitted = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.admission_number}"
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    
    # Attendance
    times_school_opened = models.IntegerField(default=0)
    times_present = models.IntegerField(default=0)
    times_absent = models.IntegerField(default=0)
    
    # Comments
    class_teacher_comment = models.TextField(blank=True)
    headmaster_comment = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.term}"
    
    class Meta:
        unique_together = ['student', 'term']
        ordering = ['-term', 'student']


class SubjectScore(models.Model):
    report_card = models.ForeignKey(ReportCard, on_delete=models.CASCADE, related_name='subject_scores')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    # Scores
    ca1 = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    ca2 = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    ca3 = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    exam = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                validators=[MinValueValidator(0), MaxValueValidator(70)])
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True)
    remark = models.CharField(max_length=50, blank=True)
    
    def save(self, *args, **kwargs):
        # Auto-calculate total
        self.total = self.ca1 + self.ca2 + self.ca3 + self.exam
        
        # Auto-assign grade
        if self.total >= 80:
            self.grade = 'A'
        elif self.total >= 70:
            self.grade = 'B'
        elif self.total >= 60:
            self.grade = 'C'
        elif self.total >= 50:
            self.grade = 'D'
        elif self.total >= 40:
            self.grade = 'E'
        else:
            self.grade = 'F'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.report_card.student.get_full_name()} - {self.subject.name}"
    
    class Meta:
        unique_together = ['report_card', 'subject']
        ordering = ['subject__name']


class AffectiveDisposition(models.Model):
    report_card = models.OneToOneField(ReportCard, on_delete=models.CASCADE, related_name='affective')
    
    punctuality = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    attentiveness = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    politeness = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    neatness = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    initiative = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    perseverance = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    leadership = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    honesty = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    self_control = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    relationship_with_others = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    emotional_stability = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return f"Affective - {self.report_card.student.get_full_name()}"


class PsychomotorSkill(models.Model):
    report_card = models.OneToOneField(ReportCard, on_delete=models.CASCADE, related_name='psychomotor')
    
    handwriting = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    drawing_painting = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    craft_tools = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    sports_games = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    music = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    verbal_fluency = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return f"Psychomotor - {self.report_card.student.get_full_name()}"

