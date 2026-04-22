from django.db import models
from accounts.models import User  # make sure this is your custom User model
from datetime import date
from django.core.validators import FileExtensionValidator


class Teacher(models.Model):
    """
    Teacher/Staff Profile
    Extended information for teaching and non-teaching staff
    """
    
    EMPLOYMENT_TYPE = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('volunteer', 'Volunteer'),
    )
    
    EMPLOYMENT_STATUS = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    QUALIFICATION_CHOICES = (
        ('ssce', 'SSCE/WAEC/NECO'),
        ('ond', 'OND'),
        ('nce', 'NCE'),
        ('hnd', 'HND'),
        ('bsc', 'B.Sc/B.A/B.Ed'),
        ('pgde', 'PGDE'),
        ('msc', 'M.Sc/M.A/M.Ed'),
        ('phd', 'Ph.D'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    
        # ----------------------------------------------------------
    # ⭐️ PERSONAL INFORMATION (ADDED BY CHATGPT)
    # ----------------------------------------------------------
    date_of_birth = models.DateField(null=True, blank=True)


    # NEW name fields (same as Student)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)



    profile_picture = models.ImageField(
        upload_to='teacher_photos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    # ----------------------------------------------------------

    # Employment Details
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, default='full_time')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # <--- ADDED
    
    # Job Information
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True, help_text='Job title')
    subject_specialization = models.CharField(max_length=200, blank=True)
    
    # Teaching Details
    is_class_teacher = models.BooleanField(default=False)
    teaching_experience_years = models.IntegerField(default=0)
    
    # Qualification
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, blank=True)
    qualification_details = models.TextField(blank=True, help_text='Details of qualifications obtained')
    
    # Professional Development
    certifications = models.TextField(blank=True, help_text='Professional certifications')
    training_attended = models.TextField(blank=True)
    
    # Salary & Benefits
    salary = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    account_name = models.CharField(max_length=200, blank=True)
    
    # Leave Management
    annual_leave_days = models.IntegerField(default=30)
    sick_leave_days = models.IntegerField(default=14)
    leave_days_taken = models.IntegerField(default=0)
    leave_balance = models.IntegerField(default=30)
    
    # ______________________________________________________
    last_birthday_email_sent = models.DateField(null=True, blank=True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Performance
    performance_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text='Out of 5.00')
    last_appraisal_date = models.DateField(null=True, blank=True)
    
    # Contract Details
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    
    # Exit Information
    exit_date = models.DateField(null=True, blank=True)
    exit_reason = models.TextField(blank=True)
    
    # Documents
    cv_file = models.FileField(upload_to='staff_cv/', blank=True)
    appointment_letter = models.FileField(upload_to='staff_letters/', blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Teacher/Staff'
        verbose_name_plural = 'Teachers/Staff'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    @property
    def is_contract_active(self):
        """Check if contract is still active"""
        if self.contract_end_date:
            return date.today() <= self.contract_end_date
        return True
    
    @property
    def years_of_service(self):
        """Calculate years of service"""
        if self.date_of_joining:
            today = date.today()
            return (today - self.date_of_joining).days // 365
        return 0


class StaffDocument(models.Model):
    '''Document storage for staff CV, letters, etc.'''
    DOCUMENT_TYPE = (
        ('cv', 'Curriculum Vitae (CV)'),
        ('cover_letter', 'Cover Letter'),
        ('application_letter', 'Application Letter'),
        ('certificate', 'Certificate'),
        ('recommendation', 'Recommendation Letter'),
        ('contract', 'Employment Contract'),
        ('other', 'Other Document'),
    )
    
    staff = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='documents')
    
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE)
    document_title = models.CharField(max_length=200)
    document_file = models.FileField(
        upload_to='staff_documents/%Y/%m/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    
    description = models.TextField(blank=True)
    
    # Folder organization
    folder_name = models.CharField(max_length=100, default='General')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.document_title}"


class StaffFolder(models.Model):
    '''Organize staff documents into folders'''
    staff = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='folders')
    folder_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['staff', 'folder_name']
        ordering = ['folder_name']
    
    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.folder_name}"
