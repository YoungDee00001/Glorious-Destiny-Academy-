from django.contrib import admin
from .models import SchoolEvent, EventGallery, EventDocument


class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 1
    readonly_fields = ('uploaded_at',)


class EventDocumentInline(admin.TabularInline):
    model = EventDocument
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'event_type',
        'academic_year',
        'start_date',
        'end_date',
        'is_published',
    )
    list_filter = (
        'event_type',
        'academic_year',
        'is_published',
        'start_date',
    )
    search_fields = (
        'title',
        'academic_year',
        'venue',
        'organizers',
    )
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Event Information', {
            'fields': (
                'event_type',
                'title',
                'description',
                'academic_year',
            )
        }),
        ('Event Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Venue & Organizers', {
            'fields': ('venue', 'organizers')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Publication', {
            'fields': ('is_published',)
        }),
    )
    


@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'uploaded_at')
    search_fields = ('event__title', 'caption')


@admin.register(EventDocument)
class EventDocumentAdmin(admin.ModelAdmin):
    list_display = ('event', 'document_title', 'uploaded_at')
    search_fields = ('event__title', 'document_title')
