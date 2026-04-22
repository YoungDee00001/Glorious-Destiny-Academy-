# online_payments/models.py
from django.db import models
from parent.models import Parent  # correct import
# Make sure the students app exists with StudentRegistration model
# from students.models import StudentRegistration

class OnlinePayment(models.Model):
    """Online payment records using Paystack"""
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    payment_reference = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey('students.StudentRegistration', on_delete=models.CASCADE)
    parent = models.ForeignKey('parent.Parent', on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='paystack')
    
    # Paystack details
    paystack_reference = models.CharField(max_length=200, blank=True)
    authorization_url = models.URLField(blank=True)
    access_code = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Payment metadata
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Allocation (which fees this payment covers)
    fee_items = models.JSONField(default=list, help_text='List of fee items being paid')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']  # order by most recent first
        verbose_name = 'Online Payment'
        verbose_name_plural = 'Online Payments'
    
    def __str__(self):
        return f"{self.payment_reference} - ₦{self.amount}"
