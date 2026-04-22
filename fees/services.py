# services.py
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import FeeRecord, ReminderLog, PaymentNotification, SchoolSettings, Student
from django.contrib.auth.models import User


class EmailService:
    @staticmethod
    def get_school_settings():
        settings, created = SchoolSettings.objects.get_or_create(
            pk=1,
            defaults={
                'school_name': 'Your School Name',
                'school_email': 'admin@school.com',
                'school_phone': '+1234567890',
                'school_address': 'School Address',
            }
        )
        return settings
    
    @staticmethod
    def send_reminder_email(fee_record, reminder_type):
        settings = EmailService.get_school_settings()
        student = fee_record.student
        
        if reminder_type == 'DUE_SOON':
            subject = f"Fee Payment Reminder - Due in {abs(fee_record.days_until_due)} days"
            message = EmailService._create_due_soon_message(fee_record, settings)
        elif reminder_type == 'DUE_TODAY':
            subject = f"Fee Payment Due Today - {student.name}"
            message = EmailService._create_due_today_message(fee_record, settings)
        elif reminder_type == 'OVERDUE':
            subject = f"URGENT: Overdue Fee Payment - {student.name}"
            message = EmailService._create_overdue_message(fee_record, settings)
        else:
            return False
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.school_email,
                recipient_list=[student.parent_email],
                fail_silently=False,
            )
            
            ReminderLog.objects.create(
                fee_record=fee_record,
                reminder_type=reminder_type,
                recipient_email=student.parent_email,
                email_subject=subject,
                email_body=message,
                status='SENT'
            )
            
            return True
        except Exception as e:
            ReminderLog.objects.create(
                fee_record=fee_record,
                reminder_type=reminder_type,
                recipient_email=student.parent_email,
                email_subject=subject,
                email_body=message,
                status='FAILED',
                error_message=str(e)
            )
            return False
    
    @staticmethod
    def _create_due_soon_message(fee_record, settings):
        student = fee_record.student
        return f"""
Dear Parent/Guardian of {student.name},

This is a friendly reminder that your child's fee payment is due soon.

Student Details:
-----------------
Student Name: {student.name}
Student ID: {student.student_id}
Class: {student.class_name}

Fee Details:
-----------------
Fee Type: {fee_record.fee_type}
Amount: ${fee_record.fee_amount}
Due Date: {fee_record.due_date.strftime('%B %d, %Y')}
Days Until Due: {abs(fee_record.days_until_due)} days

Please ensure payment is made before the due date to avoid any late fees.

School Contact Information:
-----------------
{settings.school_name}
Phone: {settings.school_phone}
Email: {settings.school_email}
Address: {settings.school_address}

Thank you for your cooperation.

Best regards,
{settings.school_name}
        """
    
    @staticmethod
    def _create_due_today_message(fee_record, settings):
        student = fee_record.student
        return f"""
Dear Parent/Guardian of {student.name},

This is a reminder that your child's fee payment is DUE TODAY.

Student Details:
-----------------
Student Name: {student.name}
Student ID: {student.student_id}
Class: {student.class_name}

Fee Details:
-----------------
Fee Type: {fee_record.fee_type}
Amount: ${fee_record.fee_amount}
Due Date: {fee_record.due_date.strftime('%B %d, %Y')} (TODAY)
Payment Status: {fee_record.payment_status}

Please make the payment today to avoid late fees.

School Contact Information:
-----------------
{settings.school_name}
Phone: {settings.school_phone}
Email: {settings.school_email}
Address: {settings.school_address}

Thank you for your prompt attention.

Best regards,
{settings.school_name}
        """
    
    @staticmethod
    def _create_overdue_message(fee_record, settings):
        student = fee_record.student
        return f"""
Dear Parent/Guardian of {student.name},

URGENT: Your child's fee payment is now OVERDUE.

Student Details:
-----------------
Student Name: {student.name}
Student ID: {student.student_id}
Class: {student.class_name}

Fee Details:
-----------------
Fee Type: {fee_record.fee_type}
Amount: ${fee_record.fee_amount}
Due Date: {fee_record.due_date.strftime('%B %d, %Y')}
Days Overdue: {fee_record.days_overdue} days
Payment Status: OVERDUE

Please make the payment immediately.

School Contact Information:
-----------------
{settings.school_name}
Phone: {settings.school_phone}
Email: {settings.school_email}
Address: {settings.school_address}

Best regards,
{settings.school_name}
        """
    
    @staticmethod
    def send_payment_receipt(fee_record):
        settings = EmailService.get_school_settings()
        student = fee_record.student
        
        subject = f"Payment Receipt - {student.name}"
        message = f"""
Dear Parent/Guardian of {student.name},

Thank you for your payment. This email serves as your receipt.

Student Details:
-----------------
Student Name: {student.name}
Student ID: {student.student_id}
Class: {student.class_name}

Payment Details:
-----------------
Fee Type: {fee_record.fee_type}
Amount Paid: ${fee_record.amount_paid}
Payment Date: {fee_record.payment_date.strftime('%B %d, %Y %I:%M %p') if fee_record.payment_date else 'N/A'}
Payment Method: {fee_record.payment_method}
Transaction ID: {fee_record.transaction_id}

School Contact Information:
-----------------
{settings.school_name}
Phone: {settings.school_phone}
Email: {settings.school_email}

Thank you for your payment.

Best regards,
{settings.school_name}
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.school_email,
                recipient_list=[student.parent_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Failed to send receipt: {e}")
            return False


class FeeReminderService:
    @staticmethod
    def check_and_send_reminders():
        settings = EmailService.get_school_settings()
        today = timezone.now().date()
        
        results = {
            'due_soon': 0,
            'due_today': 0,
            'overdue': 0,
            'errors': []
        }
        
        unpaid_fees = FeeRecord.objects.filter(
            Q(payment_status='UNPAID') | Q(payment_status='PARTIAL')
        )
        
        for fee in unpaid_fees:
            try:
                if settings.enable_due_soon_reminder:
                    if fee.days_until_due == settings.days_before_due_reminder:
                        if not FeeReminderService._reminder_sent_today(fee, 'DUE_SOON'):
                            if EmailService.send_reminder_email(fee, 'DUE_SOON'):
                                results['due_soon'] += 1
                
                if settings.enable_due_today_reminder:
                    if fee.days_until_due == 0:
                        if not FeeReminderService._reminder_sent_today(fee, 'DUE_TODAY'):
                            if EmailService.send_reminder_email(fee, 'DUE_TODAY'):
                                results['due_today'] += 1
                
                if settings.enable_overdue_reminder:
                    if fee.is_overdue:
                        if FeeReminderService._should_send_overdue_reminder(fee, settings):
                            if EmailService.send_reminder_email(fee, 'OVERDUE'):
                                results['overdue'] += 1
            
            except Exception as e:
                results['errors'].append(f"Error processing fee {fee.id}: {str(e)}")
        
        return results
    
    @staticmethod
    def _reminder_sent_today(fee_record, reminder_type):
        today = timezone.now().date()
        return ReminderLog.objects.filter(
            fee_record=fee_record,
            reminder_type=reminder_type,
            sent_at__date=today,
            status='SENT'
        ).exists()
    
    @staticmethod
    def _should_send_overdue_reminder(fee_record, settings):
        last_reminder = ReminderLog.objects.filter(
            fee_record=fee_record,
            reminder_type='OVERDUE',
            status='SENT'
        ).order_by('-sent_at').first()
        
        if not last_reminder:
            return True
        
        days_since_last = (timezone.now().date() - last_reminder.sent_at.date()).days
        return days_since_last >= settings.overdue_reminder_frequency_days


class PaymentService:
    @staticmethod
    def process_payment(fee_record, amount_paid, payment_method, transaction_id=None):
        fee_record.amount_paid += amount_paid
        fee_record.payment_date = timezone.now()
        fee_record.payment_method = payment_method
        
        if transaction_id:
            fee_record.transaction_id = transaction_id
        
        if fee_record.amount_paid >= fee_record.fee_amount:
            fee_record.payment_status = 'PAID'
        elif fee_record.amount_paid > 0:
            fee_record.payment_status = 'PARTIAL'
        
        fee_record.save()
        
        EmailService.send_payment_receipt(fee_record)
        PaymentService._notify_admin(fee_record)
        
        return fee_record
    
    @staticmethod
    def _notify_admin(fee_record):
        admin_users = User.objects.filter(is_staff=True)
        
        message = f"""
Payment received for {fee_record.student.name}.
Amount: ${fee_record.amount_paid}
Fee Type: {fee_record.fee_type}
Payment Date: {fee_record.payment_date.strftime('%B %d, %Y %I:%M %p')}
Payment Status: {fee_record.payment_status}
        """
        
        for admin in admin_users:
            PaymentNotification.objects.create(
                fee_record=fee_record,
                admin_user=admin,
                message=message
            )
    
    @staticmethod
    def manual_resend_reminder(fee_record):
        if fee_record.payment_status == 'PAID':
            return False, "Fee is already paid"
        
        if fee_record.is_overdue:
            reminder_type = 'OVERDUE'
        elif fee_record.days_until_due == 0:
            reminder_type = 'DUE_TODAY'
        else:
            reminder_type = 'DUE_SOON'
        
        success = EmailService.send_reminder_email(fee_record, reminder_type)
        
        if success:
            return True, "Reminder sent successfully"
        else:
            return False, "Failed to send reminder"