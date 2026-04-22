from django.urls import path
from . import views

urlpatterns = [
    path('', views.Administration.as_view(), name='Administration'),

]
