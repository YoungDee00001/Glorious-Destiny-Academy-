
from django.urls import path
from .views import *


urlpatterns = [
    path('report-cards/', report_card_list, name='report_card_list'),
    path('report-cards/create/', create_report_card, name='create_report_card'),
    path('report-cards/<int:pk>/edit/', edit_report_card, name='edit_report_card'),
    path('report-cards/<int:pk>/view/', view_report_card, name='view_report_card'),
    path('report-cards/<int:pk>/delete/', delete_report_card, name='delete_report_card'),
]