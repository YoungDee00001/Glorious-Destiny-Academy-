from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import User
import uuid


class StudentRegistration(models.Model):
    """Student Registration for New Intake"""

    # -------------------------
    # CLASS CHOICES
    # -------------------------
    CLASS_CHOICES = (
        ('creche', 'Creche'),
        ('kindergarten', 'Kindergarten'),
        ('nursery_1', 'Nursery 1'),
        ('nursery_2', 'Nursery 2'),
        ('primary_1', 'Primary 1'),
        ('primary_2', 'Primary 2'),
        ('primary_3', 'Primary 3'),
        ('primary_4', 'Primary 4'),
        ('primary_5', 'Primary 5'),
        ('primary_6', 'Primary 6'),
        ('jss_1', 'JSS 1'),
        ('jss_2', 'JSS 2'),
        ('jss_3', 'JSS 3'),
        ('sss_1', 'SSS 1'),
        ('sss_2', 'SSS 2'),
        ('sss_3', 'SSS 3'),
    )

    # -------------------------
    # NIGERIAN STATES
    # -------------------------
    NIGERIAN_STATES = (
        ('abia', 'Abia'),
        ('adamawa', 'Adamawa'),
        ('akwa_ibom', 'Akwa Ibom'),
        ('anambra', 'Anambra'),
        ('bauchi', 'Bauchi'),
        ('bayelsa', 'Bayelsa'),
        ('benue', 'Benue'),
        ('borno', 'Borno'),
        ('cross_river', 'Cross River'),
        ('delta', 'Delta'),
        ('ebonyi', 'Ebonyi'),
        ('edo', 'Edo'),
        ('ekiti', 'Ekiti'),
        ('enugu', 'Enugu'),
        ('fct', 'FCT Abuja'),
        ('gombe', 'Gombe'),
        ('imo', 'Imo'),
        ('jigawa', 'Jigawa'),
        ('kaduna', 'Kaduna'),
        ('kano', 'Kano'),
        ('katsina', 'Katsina'),
        ('kebbi', 'Kebbi'),
        ('kogi', 'Kogi'),
        ('kwara', 'Kwara'),
        ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'),
        ('niger', 'Niger'),
        ('ogun', 'Ogun'),
        ('ondo', 'Ondo'),
        ('osun', 'Osun'),
        ('oyo', 'Oyo'),
        ('plateau', 'Plateau'),
        ('rivers', 'Rivers'),
        ('sokoto', 'Sokoto'),
        ('taraba', 'Taraba'),
        ('yobe', 'Yobe'),
        ('zamfara', 'Zamfara'),
    )

    # -------------------------
    # GENDER CHOICES (NEW)
    # -------------------------
    GENDER_CHOICES = (
        ('male', 'Boy'),
        ('female', 'Girl'),
    )

    # -------------------------
    # USER RELATION
    # -------------------------
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # -------------------------
    # REGISTRATION DETAILS
    # -------------------------
    registration_number = models.CharField(max_length=50, unique=True, blank=True)

    # -------------------------
    # STUDENT PERSONAL INFO
    # -------------------------
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)

    @property
    def full_name(self):
        name = f"{self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        name += f" {self.surname}"
        return name

    date_of_birth = models.DateField()
    
    # -------------------------
    # GENDER FIELD (NEW)
    # -------------------------
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    
    state_of_origin = models.CharField(max_length=50, choices=NIGERIAN_STATES)
    address = models.TextField()

    # Class applying for
    class_applying = models.CharField(max_length=20, choices=CLASS_CHOICES)
    
    # -------------------------
    # ASSIGNED CLASS (NEW) - For admitted students
    # -------------------------
    assigned_class = models.ForeignKey(
        'Class', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students',
        help_text='Class assigned after admission'
    )

    # Child passport
    child_picture = models.ImageField(
        upload_to='student_registration/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    # -------------------------
    # PARENT DETAILS
    # -------------------------
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    parent_email = models.EmailField(max_length=200, blank=True, null=True)

    # __________________________________________________
    last_birthday_email_sent = models.DateField(null=True, blank=True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # -------------------------
    # EXTRA INFORMATION
    # -------------------------
    previous_school = models.CharField(max_length=200, blank=True)
    medical_conditions = models.TextField(blank=True)

    # -------------------------
    # APPROVAL STATUS
    # -------------------------
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('admitted', 'Admitted'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # -------------------------
    # TIMESTAMPS
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.registration_number} - {self.full_name}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.surname} {self.first_name} {self.middle_name}"
        return f"{self.surname} {self.first_name}"

    # Auto-generate unique registration number
    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = f"REG-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


# =========================================================
# NEW CLASS MODEL
# =========================================================
class Class(models.Model):
    """
    Class/Grade Model to organize students and assign teachers
    """
    CLASS_LEVEL_CHOICES = (
        ('creche', 'Creche'),
        ('kindergarten', 'Kindergarten'),
        ('nursery_1', 'Nursery 1'),
        ('nursery_2', 'Nursery 2'),
        ('primary_1', 'Primary 1'),
        ('primary_2', 'Primary 2'),
        ('primary_3', 'Primary 3'),
        ('primary_4', 'Primary 4'),
        ('primary_5', 'Primary 5'),
        ('primary_6', 'Primary 6'),
        ('jss_1', 'JSS 1'),
        ('jss_2', 'JSS 2'),
        ('jss_3', 'JSS 3'),
        ('sss_1', 'SSS 1'),
        ('sss_2', 'SSS 2'),
        ('sss_3', 'SSS 3'),
    )
    
    class_name = models.CharField(
        max_length=100, 
        help_text='e.g., Primary 1A, JSS 2B'
    )
    class_level = models.CharField(
        max_length=20, 
        choices=CLASS_LEVEL_CHOICES,
        help_text='Grade/Level of the class'
    )
    
    # Class Teacher (one main teacher per class)
    class_teacher = models.ForeignKey(
        'staff.Teacher',  # This references the Teacher model in staff app
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_taught',
        help_text='Main class teacher'
    )

    subject_teachers = models.ManyToManyField(
        'staff.Teacher',  # This references the Teacher model in staff app
        blank=True,
        related_name='classes_teaching',
        help_text='Teachers who teach subjects in this class'
    )
    
    # Academic year
    academic_year = models.CharField(
        max_length=20,
        help_text='e.g., 2024/2025'
    )
    
    # Class capacity
    max_capacity = models.IntegerField(default=30)
    
    # Classroom details
    classroom_location = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['class_level', 'class_name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        unique_together = ['class_name', 'academic_year']
    
    def __str__(self):
        return f"{self.class_name} ({self.academic_year})"