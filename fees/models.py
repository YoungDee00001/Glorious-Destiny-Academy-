# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from students.models import StudentRegistration

class Student(models.Model):
    """Student model with basic information"""
    name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50, unique=True)
    class_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20, blank=True)
    date_enrolled = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"


class FeeRecord(models.Model):
    """Individual fee record for each student"""
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
    ]
    
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name='fees')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')
    
    # Payment details
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Metadata - FIXED: Changed from User to settings.AUTH_USER_MODEL
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Fee description
    fee_type = models.CharField(max_length=100, default='Tuition Fee')
    academic_term = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['payment_status', 'due_date']),
        ]
    
    def __str__(self):
        return f"{self.student.name} - {self.fee_amount} - {self.due_date}"
    
    @property
    def balance(self):
        """Remaining balance to be paid"""
        return self.fee_amount - self.amount_paid
    
    @property
    def is_overdue(self):
        """Check if fee is overdue"""
        return self.due_date < timezone.now().date() and self.payment_status != 'PAID'
    
    @property
    def days_until_due(self):
        """Calculate days until due date"""
        delta = self.due_date - timezone.now().date()
        return delta.days
    
    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue:
            delta = timezone.now().date() - self.due_date
            return delta.days
        return 0


class ReminderLog(models.Model):
    """Log of all reminder emails sent"""
    REMINDER_TYPES = [
        ('DUE_SOON', 'Due Soon'),
        ('DUE_TODAY', 'Due Today'),
        ('OVERDUE', 'Overdue'),
    ]
    
    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)
    recipient_email = models.EmailField()
    email_subject = models.CharField(max_length=200)
    email_body = models.TextField()
    status = models.CharField(max_length=20, default='SENT')
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['fee_record', 'reminder_type', 'sent_at']),
        ]
    
    def __str__(self):
        return f"{self.reminder_type} - {self.fee_record.student.name} - {self.sent_at}"


class PaymentNotification(models.Model):
    """Notifications sent to admin when payment is made"""
    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE)
    notified_at = models.DateTimeField(auto_now_add=True)
    # FIXED: Changed from User to settings.AUTH_USER_MODEL
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    
    class Meta:
        ordering = ['-notified_at']
    
    def __str__(self):
        return f"Payment notification - {self.fee_record.student.name}"


class SchoolSettings(models.Model):
    """School configuration for emails and reminders"""
    school_name = models.CharField(max_length=200)
    school_email = models.EmailField()
    school_phone = models.CharField(max_length=20)
    school_address = models.TextField()
    
    # Reminder settings
    days_before_due_reminder = models.IntegerField(default=7)
    enable_due_soon_reminder = models.BooleanField(default=True)
    enable_due_today_reminder = models.BooleanField(default=True)
    enable_overdue_reminder = models.BooleanField(default=True)
    overdue_reminder_frequency_days = models.IntegerField(default=3)
    
    # Email templatesq
    due_soon_email_template = models.TextField(blank=True)
    due_today_email_template = models.TextField(blank=True)
    overdue_email_template = models.TextField(blank=True)
    payment_receipt_template = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "School Settings"
        verbose_name_plural = "School Settings"
    
    def __str__(self):
        return self.school_name