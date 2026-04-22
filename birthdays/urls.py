from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:student_id>/', views.send_birthday_notification, name='send_birthday_notification'),
    path('', views.today_birthdays, name='today_birthdays'),
    path('notifications/', views.birthday_notifications_list, name='birthday_notifications_list'),
]

