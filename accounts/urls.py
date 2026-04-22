from django.urls import path
from .views import (
    LoginView, RegisterView, LogoutView,
    choose_role, student_profile_create, staff_profile_create,home_page
)

urlpatterns = [
    path('', home_page, name='home_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("choose-role/", choose_role, name="choose_role"),

    # NEW
    
    path("student-profile/", student_profile_create, name="create_student"),
    path("staff-profile/", staff_profile_create, name="create_teacher"),
]
