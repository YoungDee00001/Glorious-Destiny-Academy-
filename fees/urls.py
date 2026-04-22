# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Fee management
    path('fees/create/', views.create_fee_record, name='create_fee_record'),
    path('fees/paid/', views.paid_fees_list, name='paid_fees_list'),
    path('fees/unpaid/', views.unpaid_fees_list, name='unpaid_fees_list'),
    path('fees/mark-paid/<int:fee_id>/', views.mark_as_paid, name='mark_as_paid'),
    
    # Student fees
    path('student/<int:student_id>/fees/', views.student_fee_detail, name='student_fee_detail'),
    
    # Reminders
    path('reminders/', views.reminders_log, name='reminders_log'),
    path('reminders/resend/<int:fee_id>/', views.manual_resend_reminder, name='manual_resend_reminder'),
    path('reminders/run-check/', views.run_reminder_check, name='run_reminder_check'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),
    
    # Payment webhook (for payment gateway integration)
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
]