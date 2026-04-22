from django.contrib import admin
from .models import BirthdayNotification


@admin.register(BirthdayNotification)
class BirthdayNotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'notification_date', 'message_sent')
    list_filter = ('notification_date', 'message_sent')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__parent_email',
    )
    ordering = ('-notification_date',)
    list_per_page = 25
