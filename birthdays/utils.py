from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date

from students.models import StudentRegistration
from staff.models import Teacher


def get_full_name(person):
    return f"{person.first_name} {person.middle_name or ''} {person.surname}".strip()


def send_birthday_email(full_name, email, photo_url=None, gif_url=None):
    subject = f"🎉 Happy Birthday, {full_name}! 🎂"

    html_content = render_to_string(
        "birthdays/birthday_email.html",
        {
            "name": full_name,
            "photo_url": photo_url,
            "gif_url": gif_url or "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Happy Birthday, {full_name}!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def check_and_send_birthday_emails(test_mode=False):
    today = date.today()

    students = StudentRegistration.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
    )

    teachers = Teacher.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
    )

    people = list(students) + list(teachers)

    for person in people:

        # Prevent double sending
        if person.last_birthday_email_sent == today:
            continue

        # --------------------------
        # Get Email + Photo for Student
        # --------------------------
        if isinstance(person, StudentRegistration):
            email = person.parent_email
            photo_url = person.child_picture.url if person.child_picture else None
