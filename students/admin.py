# from django.contrib import admin
# from .models import StudentRegistration


# @admin.register(StudentRegistration)
# class StudentRegistrationAdmin(admin.ModelAdmin):
#     list_display = ('registration_number', 'get_full_name', 'class_applying', 'status', 'created_at')
#     list_filter = ('status', 'class_applying', 'state_of_origin')
#     search_fields = ('surname', 'first_name', 'middle_name', 'registration_number')
#     ordering = ('-created_at',)

#     readonly_fields = ('registration_number', 'created_at', 'updated_at')



from django.contrib import admin
from .models import StudentRegistration


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    # list all fields automatically (no missing field errors)
    list_display = [field.name for field in StudentRegistration._meta.fields]
    search_fields = [field.name for field in StudentRegistration._meta.fields if 'name' in field.name or 'email' in field.name]
    list_filter = [field.name for field in StudentRegistration._meta.fields if field.get_internal_type() in ['CharField', 'DateField']]
    list_per_page = 25

