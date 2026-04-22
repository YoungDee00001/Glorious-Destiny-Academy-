from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from twilio.rest import Client

from students.models import StudentRegistration
from .models import BirthdayNotification


# 🎉 SEND SMS FUNCTION
def send_sms_message(phone_number, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        print("SMS Error:", e)
        return False


# 🎂 1. List students whose birthday is today
def today_birthdays(request):
    today = timezone.now().date()
    
    students = StudentRegistration.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    return render(request, 'birthdays/today_birthdays.html', {
        'students': students,
        'today': today
    })


# ✉️📱 2. Send birthday notification (EMAIL + SMS)
def send_birthday_notification(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)

    parent_email = getattr(student, 'parent_email', None)
    parent_phone = getattr(student, 'parent_phone', None)

    # Birthday message
    subject = f"Happy Birthday to {student.first_name}!"
    email_message = (
        f"Dear Parent,\n\n"
        f"Wishing a very Happy Birthday to {student.first_name} {student.last_name}! 🎉🎂\n"
        f"May this year bring joy, growth, and success.\n\n"
        f"Warm regards,\nYour School Team"
    )

    sms_message = (
        f"🎉 Happy Birthday to {student.first_name}! 🎂 "
        f"Wishing them joy and success. - Your School"
    )

    # ⚠️ EMAIL SENDING
    if parent_email:
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [parent_email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Email sending failed: {e}")
    else:
        messages.warning(request, "No parent email found.")

    # ⚠️ SMS SENDING
    if parent_phone:
        sms_sent = send_sms_message(parent_phone, sms_message)
        if not sms_sent:
            messages.error(request, "SMS failed to send.")
    else:
        messages.warning(request, "No parent phone number found.")

    # Save notification record
    BirthdayNotification.objects.create(
        student=student,
        message_sent=True
    )

    messages.success(request, f"Birthday messages sent for {student.first_name}!")

    return redirect('today_birthdays')


# 📋 3. List notifications
def birthday_notifications_list(request):
    notifications = BirthdayNotification.objects.all().order_by('-notification_date')

    return render(request, 'birthdays/birthday_notifications_list.html', {
        'notifications': notifications
    })
