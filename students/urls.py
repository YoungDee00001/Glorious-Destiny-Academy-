from django.urls import path
from . import views


urlpatterns = [
    path('', views.StudentAdmin.as_view(), name='StudentAdmin'),

    # # ===============================
    # #   STUDENT MANAGEMENT
    # # ===============================
    # path("students/", SuperUserStudentListView.as_view(), name="super_user_student_list"),
    # # path("students/register/", StudentRegisterView.as_view(), name="student_register"),
    # path("students/register/", StudentRegisterView, name="student_register"),
    # path("students/<int:pk>/", SuperUserStudentDetailView.as_view(), name="studentreg_detail"),
    # path("students/<int:pk>/update/", SuperUserStudentUpdateView.as_view(), name="student_update"),
    # path("students/<int:pk>/delete/", SuperUserStudentDeleteView.as_view(), name="student_delete"),


    # # Pending Students
    # path('students/pending/', pending_students, name='pending_students'),
    # path('students/approve/<int:student_id>/', approve_student, name='approve_student'),
    # path('students/reject/<int:student_id>/', reject_student, name='reject_student'),

]

 
