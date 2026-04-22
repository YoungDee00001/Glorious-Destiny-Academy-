from django import forms
from .models import SchoolEvent, EventGallery, EventDocument

class SchoolEventForm(forms.ModelForm):
    class Meta:
        model = SchoolEvent
        fields = [
            'event_type', 'title', 'description',
            'academic_year', 'start_date', 'end_date',
            'cover_image', 'venue', 'organizers',
            'is_published'
        ]


class EventGalleryForm(forms.ModelForm):
    class Meta:
        model = EventGallery
        fields = ['image', 'caption']


class EventDocumentForm(forms.ModelForm):
    class Meta:
        model = EventDocument
        fields = ['document_title', 'document_file']
