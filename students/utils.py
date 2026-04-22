# students/utils.py
from datetime import date
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from students.models import StudentRegistration
from staff.models import Teacher


def get_full_name(person):
    """
    Returns the full name of a person from first, middle, surname.
    """
    return f"{person.first_name} {person.middle_name or ''} {person.surname}".strip()


def check_and_send_birthday_emails(test_mode=True):
    """
    Sends birthday emails to all students and teachers whose birthday is today.
    If test_mode=True, it only prints who would get the email.
    """
    today = date.today()

    # Get students with birthday today
    students = StudentRegistration.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    # Get teachers with birthday today
    teachers = Teacher.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    # Combine both lists
    people = list(students) + list(teachers)

    if not people:
        print("No birthdays today.")
        return

    for person in people:
        # Determine email and photo
        if isinstance(person, StudentRegistration):
            email = getattr(person, "parent_email", None)
            photo_url = getattr(person, "child_picture", None) and person.child_picture.url
        else:  # Teacher
            email = getattr(person, "email", None)
            photo_url = getattr(person, "photo", None) and person.photo.url

        full_name = get_full_name(person)

        if not email:
            print(f"⚠️ Skipping {full_name}, no email found.")
            continue

        if test_mode:
            print(f"🎉 Would send email to {full_name} ({email})")
        else:
            send_birthday_email(full_name, email, photo_url)


def send_birthday_email(full_name, email, photo_url=None):
    """
    Sends an actual birthday email to the person.
    """
    subject = f"🎉 Happy Birthday, {full_name}! 🎂"

    html_content = render_to_string("birthdays/birthday_email.html", {
        "name": full_name,
        "photo_url": photo_url
    })

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=f"Happy Birthday, {full_name}!",  # plain text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email_message.attach_alternative(html_content, "text/html")

    try:
        email_message.send(fail_silently=False)
        print(f"✅ Sent birthday email to {full_name} ({email})")
    except Exception as e:
        print(f"❌ Failed to send email to {full_name}: {e}")
