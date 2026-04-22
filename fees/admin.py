# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Student, FeeRecord, ReminderLog, PaymentNotification, SchoolSettings


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'class_name', 'parent_email', 'is_active', 'date_enrolled']
    list_filter = ['is_active', 'class_name', 'date_enrolled']
    search_fields = ['name', 'student_id', 'parent_email']
    ordering = ['name']


@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'fee_amount', 'amount_paid', 'balance_display', 
        'due_date', 'payment_status_display', 'days_status'
    ]
    list_filter = ['payment_status', 'due_date', 'fee_type', 'created_at']
    search_fields = ['student__name', 'student__student_id', 'transaction_id']
    date_hierarchy = 'due_date'
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Fee Details', {
            'fields': ('fee_type', 'fee_amount', 'due_date', 'academic_term', 'notes')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'amount_paid', 'payment_date', 'payment_method', 'transaction_id')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def balance_display(self, obj):
        balance = obj.balance
        if balance > 0:
            return format_html('<span style="color: red;">${}</span>', balance)
        return format_html('<span style="color: green;">$0.00</span>')
    balance_display.short_description = 'Balance'
    
    def payment_status_display(self, obj):
        colors = {
            'PAID': 'green',
            'UNPAID': 'red',
            'PARTIAL': 'orange'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.payment_status, 'black'),
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Status'
    
    def days_status(self, obj):
        if obj.payment_status == 'PAID':
            return format_html('<span style="color: green;">✓ Paid</span>')
        elif obj.is_overdue:
            return format_html(
                '<span style="color: red;">⚠ {} days overdue</span>',
                obj.days_overdue
            )
        elif obj.days_until_due == 0:
            return format_html('<span style="color: orange;">⏰ Due today</span>')
        elif obj.days_until_due < 7:
            return format_html(
                '<span style="color: orange;">{} days remaining</span>',
                obj.days_until_due
            )
        else:
            return format_html(
                '<span style="color: blue;">{} days remaining</span>',
                obj.days_until_due
            )
    days_status.short_description = 'Due Status'


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = [
        'fee_record', 'reminder_type', 'recipient_email', 
        'status_display', 'sent_at'
    ]
    list_filter = ['reminder_type', 'status', 'sent_at']
    search_fields = [
        'fee_record__student__name', 'recipient_email', 
        'email_subject'
    ]
    date_hierarchy = 'sent_at'
    readonly_fields = ['sent_at']
    
    def status_display(self, obj):
        if obj.status == 'SENT':
            return format_html('<span style="color: green;">✓ Sent</span>')
        else:
            return format_html('<span style="color: red;">✗ Failed</span>')
    status_display.short_description = 'Status'


@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'fee_record', 'admin_user', 'is_read', 'notified_at'
    ]
    list_filter = ['is_read', 'notified_at']
    search_fields = ['fee_record__student__name', 'admin_user__username']
    date_hierarchy = 'notified_at'
    readonly_fields = ['notified_at']


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('School Information', {
            'fields': (
                'school_name', 'school_email', 'school_phone', 
                'school_address'
            )
        }),
        ('Reminder Settings', {
            'fields': (
                'days_before_due_reminder',
                'enable_due_soon_reminder',
                'enable_due_today_reminder',
                'enable_overdue_reminder',
                'overdue_reminder_frequency_days',
            )
        }),
        ('Email Templates (Optional)', {
            'fields': (
                'due_soon_email_template',
                'due_today_email_template',
                'overdue_email_template',
                'payment_receipt_template',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one settings object
        return not SchoolSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False