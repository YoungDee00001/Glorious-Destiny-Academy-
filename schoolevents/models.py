from django.db import models

class SchoolEvent(models.Model):
    '''Events portal for different school activities'''
    EVENT_TYPE = (
        ('emit_week', 'EMIT Week'),
        ('professional_day', 'Professional Day'),
        ('cultural_day', 'Cultural Day'),
        ('graduation', 'Graduation Ceremony'),
        ('sports_day', 'Sports Day'),
        ('inter_house', 'Inter-House Sports'),
        ('excursion', 'Excursion'),
        ('parents_day', 'P.T.A Meeting'),
        ('fruit_week', 'Fruit Week'),
        ('other', 'Other Event'),
    )
    
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Year and session
    academic_year = models.CharField(max_length=20, help_text='e.g., 2024/2025')
    
    # Event dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Event media
    cover_image = models.ImageField(upload_to='events/%Y/', blank=True)
    
    # Event details
    venue = models.CharField(max_length=200)
    organizers = models.TextField(help_text='Names of organizing committee')
    
    # Gallery
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def _str_(self):
        return f"{self.get_event_type_display()} - {self.academic_year}"


class EventGallery(models.Model):
    '''Photo gallery for events'''
    event = models.ForeignKey(SchoolEvent, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='event_gallery/%Y/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Event Galleries'
    
    def _str_(self):
        return f"{self.event.title} - Photo"


class EventDocument(models.Model):
    '''Documents related to events (programs, reports, etc.)'''
    event = models.ForeignKey(SchoolEvent, on_delete=models.CASCADE, related_name='documents')
    document_title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='event_documents/%Y/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.event.title} - {self.document_title}"

