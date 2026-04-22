from django.urls import path
from .views import (
    SuperuserAdmin,

    # Superuser Controls
    SuperUserList,
    SuperUserDetailView,
    SuperUserUpdateView,
    SuperUserDeleteView,

    # Students
    StudentRegisterView,
    SuperUserStudentListView,
    SuperUserStudentDetailView,
    SuperUserStudentUpdateView,
    SuperUserStudentDeleteView,

    # Courses
    CourseRegistration,
    courselistview,
    pendingcourselistview,
    CourseListUpdateView,
    CourseListDeleteView,

    TeacherListView, TeacherDetailView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView,
    StaffDocumentListView, StaffDocumentCreateView, StaffDocumentUpdateView, StaffDocumentDeleteView,
    StaffFolderListView, StaffFolderCreateView, StaffFolderUpdateView, StaffFolderDeleteView,


    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventGalleryUploadView,
    EventDocumentUploadView,

    pending_students,
    approve_student,
    reject_student,
    pending_staff,
    approve_staff,
    reject_staff,
)


urlpatterns = [

    # ===============================
    #   SUPERUSER DASHBOARD
    # ===============================
    path("", SuperuserAdmin.as_view(), name="SuperuserAdmin"),

    # ===============================
    #   SUPERUSER MANAGEMENT
    # ===============================
    path("users/", SuperUserList.as_view(), name="SuperUserList"),
    path("users/<int:pk>/", SuperUserDetailView.as_view(), name="superuser_detail"),
    path("users/<int:pk>/update/", SuperUserUpdateView.as_view(), name="superuser_update"),
    path("users/<int:pk>/delete/", SuperUserDeleteView.as_view(), name="superuser_delete"),

    # ===============================
    #   STUDENT MANAGEMENT
    # ===============================
    path("students/", SuperUserStudentListView.as_view(), name="super_user_student_list"),
    # path("students/register/", StudentRegisterView.as_view(), name="student_register"),
    path("students/register/", StudentRegisterView, name="student_register"),
    path("students/<int:pk>/", SuperUserStudentDetailView.as_view(), name="studentreg_detail"),
    path("students/<int:pk>/update/", SuperUserStudentUpdateView.as_view(), name="student_update"),
    path("students/<int:pk>/delete/", SuperUserStudentDeleteView.as_view(), name="student_delete"),

    # ===============================
    #   STAFF MANAGEMENT
    # ===============================
    
     # Teacher
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("teachers/add/", TeacherCreateView.as_view(), name="teacher_add"),
    path("teachers/<int:pk>/edit/", TeacherUpdateView.as_view(), name="teacher_edit"),
    path("teachers/<int:pk>/delete/", TeacherDeleteView.as_view(), name="teacher_delete"),

    # Documents
    path("documents/", StaffDocumentListView.as_view(), name="document_list"),
    path("documents/add/", StaffDocumentCreateView.as_view(), name="document_add"),
    path("documents/<int:pk>/edit/", StaffDocumentUpdateView.as_view(), name="document_edit"),
    path("documents/<int:pk>/delete/", StaffDocumentDeleteView.as_view(), name="document_delete"),

    # Folders
    path("folders/", StaffFolderListView.as_view(), name="folder_list"),
    path("folders/add/", StaffFolderCreateView.as_view(), name="folder_add"),
    path("folders/<int:pk>/edit/", StaffFolderUpdateView.as_view(), name="folder_edit"),
    path("folders/<int:pk>/delete/", StaffFolderDeleteView.as_view(), name="folder_delete"),



     # ===============================================================
    # EVENT LIST & DETAIL
    # ===============================================================
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="superuser_event_detail"),

    # ===============================================================
    # CREATE / UPDATE / DELETE EVENT
    # ===============================================================
    path("events/create/", EventCreateView.as_view(), name="superuser_event_create"),
    path("events/<int:pk>/update/", EventUpdateView.as_view(), name="superuser_event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="superuser_event_delete"),

    # ===============================================================
    # EVENT GALLERY UPLOAD
    # ===============================================================
    path("events/<int:event_id>/gallery/upload/",EventGalleryUploadView.as_view(),name="superuser_event_gallery_upload",),

    # ===============================================================
    # EVENT DOCUMENT UPLOAD
    # ===============================================================
    path("events/<int:event_id>/documents/upload/",EventDocumentUploadView.as_view(),name="superuser_event_document_upload",),


    # ===============================
    #   COURSE MANAGEMENT
    # ===============================
    path("courses/register/", CourseRegistration.as_view(), name="course_register"),
    path("courses/", courselistview, name="CourseListView"),
    path("courses/pending/", pendingcourselistview, name="pending_course_list"),
    path("courses/<int:pk>/update/", CourseListUpdateView.as_view(), name="course_update"),
    path("courses/<int:pk>/delete/", CourseListDeleteView.as_view(), name="course_delete"),



    # Pending Students
    path('students/pending/', pending_students, name='pending_students'),
    path('students/approve/<int:student_id>/', approve_student, name='approve_student'),
    path('students/reject/<int:student_id>/', reject_student, name='reject_student'),

    # Pending Staff
    path('staff/pending/', pending_staff, name='pending_staff'),
    path('staff/approve/<int:staff_id>/', approve_staff, name='approve_staff'),
    path('staff/reject/<int:staff_id>/', reject_staff, name='reject_staff'),

]
