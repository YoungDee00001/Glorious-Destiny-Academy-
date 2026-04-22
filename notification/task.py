from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
from django.core.mail import send_mail
from django.conf import settings
from .models import BirthdayNotification, FeeReminder
from student.models import Student
from fees.models import StudentFee

@shared_task
def send_birthday_notifications():
    '''Send birthday notifications daily at 6:00 AM'''
    today = timezone.now().date()
    
    # Get students with birthday today
    birthday_students = Student.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        status='active'
    )
    
    for student in birthday_students:
        # Check if notification already sent today
        if not BirthdayNotification.objects.filter(
            student=student,
            notification_date=today
        ).exists():
            
            # Calculate age
            age = today.year - student.date_of_birth.year
            
            # Birthday message
            subject = f"🎉 Happy Birthday {student.first_name}!"
            message = f"""
Dear {student.parent.user.get_full_name()},

🎂 Happy Birthday to {student.get_full_name()}! 🎉

We are delighted to celebrate {student.first_name}'s {age}th birthday today!

May this special day bring joy, happiness, and wonderful memories. 
We wish {student.first_name} a fantastic year ahead filled with success and achievements.

The entire Glorious Destiny Academy family sends warm birthday wishes!

Best regards,
Glorious Destiny Academy
Excellence in Education
            """
            
            # Send email to parent
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[student.parent.user.email],
                    fail_silently=False,
                )
                
                # Create notification record
                BirthdayNotification.objects.create(
                    student=student,
                    message_sent=True
                )
                
                print(f"Birthday notification sent for {student.get_full_name()}")
            
            except Exception as e:
                print(f"Failed to send birthday notification: {str(e)}")
                BirthdayNotification.objects.create(
                    student=student,
                    message_sent=False
                )


@shared_task
def send_fee_reminders():
    '''Send fee payment reminders'''
    today = timezone.now().date()
    
    # 1. Due Soon Reminder (7 days before)
    due_soon_date = today + timedelta(days=7)
    fees_due_soon = StudentFee.objects.filter(
        due_date=due_soon_date,
        is_paid=False
    )
    
    for fee in fees_due_soon:
        subject = f"School Fee Payment Reminder - Due in 7 Days"
        message = f"""
Dear {fee.student.parent.user.get_full_name()},

This is a friendly reminder that school fees for {fee.student.get_full_name()} are due in 7 days.

Fee Details:
- Category: {fee.fee_structure.category.name}
- Amount: ₦{fee.amount:,.2f}
- Amount Paid: ₦{fee.amount_paid:,.2f}
- Balance: ₦{fee.balance:,.2f}
- Due Date: {fee.due_date.strftime('%B %d, %Y')}

Please ensure payment is made before the due date to avoid any inconvenience.

You can pay online through our portal: {settings.SITE_URL}/payments/

Thank you for your cooperation.

Best regards,
Glorious Destiny Academy
Accounts Department
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[fee.student.parent.user.email],
                fail_silently=False,
            )
            
            FeeReminder.objects.create(
                student_fee=fee,
                reminder_type='due_soon',
                message_sent=True
            )
        except Exception as e:
            print(f"Failed to send fee reminder: {str(e)}")
    
    
    # 2. Due Today Reminder
    fees_due_today = StudentFee.objects.filter(
        due_date=today,
        is_paid=False
    )
    
    for fee in fees_due_today:
        subject = f"URGENT: School Fee Payment Due Today"
        message = f"""
Dear {fee.student.parent.user.get_full_name()},

This is an urgent reminder that school fees for {fee.student.get_full_name()} are DUE TODAY.

Fee Details:
- Category: {fee.fee_structure.category.name}
- Amount Due: ₦{fee.balance:,.2f}
- Due Date: TODAY ({fee.due_date.strftime('%B %d, %Y')})

Please make payment immediately to avoid penalties.

Pay online: {settings.SITE_URL}/payments/

Best regards,
Glorious Destiny Academy
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[fee.student.parent.user.email],
                fail_silently=False,
            )
            
            FeeReminder.objects.create(
                student_fee=fee,
                reminder_type='due_today',
                message_sent=True
            )
        except Exception as e:
            print(f"Failed to send due today reminder: {str(e)}")
    
    
    # 3. Overdue Reminder
    overdue_fees = StudentFee.objects.filter(
        due_date__lt=today,
        is_paid=False
    )
    
    for fee in overdue_fees:
        days_overdue = (today - fee.due_date).days
        
        subject = f"OVERDUE: School Fee Payment - {days_overdue} Days Overdue"
        message = f"""
Dear {fee.student.parent.user.get_full_name()},

Your school fees payment for {fee.student.get_full_name()} is now {days_overdue} days OVERDUE.

Fee Details:
- Category: {fee.fee_structure.category.name}
- Outstanding Balance: ₦{fee.balance:,.2f}
- Due Date: {fee.due_date.strftime('%B %d, %Y')}
- Days Overdue: {days_overdue}

Please contact the school office immediately to resolve this matter.

Pay online: {settings.SITE_URL}/payments/

Best regards,
Glorious Destiny Academy
Accounts Department
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[fee.student.parent.user.email],
                fail_silently=False,
            )
            
            FeeReminder.objects.create(
                student_fee=fee,
                reminder_type='overdue',
                message_sent=True
            )
        except Exception as e:
            print(f"Failed to send overdue reminder: {str(e)}")
