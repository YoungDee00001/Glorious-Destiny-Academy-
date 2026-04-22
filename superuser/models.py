from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import User
from schoolevents.models import SchoolEvent, EventGallery


class Course(models.Model):
    course_name = models.CharField(max_length=130)
    registration_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    course_registration = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name
    