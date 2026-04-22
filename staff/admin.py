from django.contrib import admin
from accounts.models import User
from .models import Teacher, StaffDocument, StaffFolder


# -----------------------------------------------------
# Unregister User if already registered elsewhere
# -----------------------------------------------------
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


# -----------------------------------------------------
# Custom Admin for Custom User model
# -----------------------------------------------------
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "staff",
        "admin",
        "students",
        "active",
        "date_joined",
    )
    list_filter = ("staff", "admin", "students", "active")
    search_fields = ("email", "full_name")
    ordering = ("email",)


# -----------------------------------------------------
# Inlines for Teacher Admin
# -----------------------------------------------------
class StaffDocumentInline(admin.TabularInline):
    model = StaffDocument
    extra = 1


class StaffFolderInline(admin.TabularInline):
    model = StaffFolder
    extra = 1


# -----------------------------------------------------
# Teacher Admin
# -----------------------------------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "employment_status", "department", "designation")
    search_fields = ("employee_id", "user__email", "user__full_name")
    list_filter = ("employment_status", "employment_type", "department")
    # inlines = [StaffDocumentInline, StaffFolderInline]


# -----------------------------------------------------
# StaffDocument Admin
# -----------------------------------------------------
@admin.register(StaffDocument)
class StaffDocumentAdmin(admin.ModelAdmin):
    list_display = ("staff", "document_title", "document_type", "uploaded_at")
    search_fields = ("document_title", "staff__email", "staff__full_name")
    list_filter = ("document_type", "uploaded_at")



# -----------------------------------------------------
# StaffFolder Admin
# -----------------------------------------------------
@admin.register(StaffFolder)
class StaffFolderAdmin(admin.ModelAdmin):
    list_display = ("staff", "folder_name", "created_at")
    search_fields = ("folder_name", "staff__email", "staff__full_name")
