# parents/models.py
from django.db import models
from accounts.models import User  # make sure this is your custom User model

class Parent(models.Model):
    """
    Parent/Guardian Profile
    Extended information for parents/guardians
    """
    
    RELATIONSHIP_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Legal Guardian'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('grandparent', 'Grandparent'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    
    # Relationship to Children
    relationship_to_children = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='father')
    
    # Occupation & Employment
    occupation = models.CharField(max_length=200, blank=True)
    employer_name = models.CharField(max_length=200, blank=True)
    employer_address = models.TextField(blank=True)
    office_phone = models.CharField(max_length=17, blank=True)
    
    # Financial Information
    monthly_income_range = models.CharField(max_length=50, blank=True)
    
    # Spouse Information
    spouse_name = models.CharField(max_length=200, blank=True)
    spouse_phone = models.CharField(max_length=17, blank=True)
    spouse_occupation = models.CharField(max_length=200, blank=True)
    
    # Additional Details
    number_of_children = models.IntegerField(default=0)
    number_of_children_in_school = models.IntegerField(default=0)
    
    # Preferences
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=(
            ('email', 'Email'),
            ('phone', 'Phone Call'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
        ),
        default='email'
    )
    
    # PTA Membership
    is_pta_member = models.BooleanField(default=False, verbose_name='PTA Member')
    pta_membership_date = models.DateField(null=True, blank=True)
    pta_position = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True, help_text='Additional notes about parent/guardian')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user']  # ✅ fixed
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Parent"
    
    @property
    def total_children(self):
        """Count total children registered"""
        return self.children.count()  # assumes a related_name 'children' from a Student model
