from django.urls import path
from . import views

urlpatterns = [
    path('', views.StaffAdmin.as_view(), name='StaffAdmin'),

]
