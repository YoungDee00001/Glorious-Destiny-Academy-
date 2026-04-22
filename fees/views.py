# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Student, FeeRecord, ReminderLog, PaymentNotification, SchoolSettings
from .services import PaymentService, FeeReminderService
from .forms import FeeRecordForm, StudentForm
from datetime import timedelta




def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard showing overview"""
    today = timezone.now().date()
    
    # Get statistics
    total_students = Student.objects.filter(is_active=True).count()
    
    # Paid fees
    paid_fees = FeeRecord.objects.filter(payment_status='PAID')
    total_paid = paid_fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    paid_count = paid_fees.count()
    
    # Unpaid fees
    unpaid_fees = FeeRecord.objects.filter(
        Q(payment_status='UNPAID') | Q(payment_status='PARTIAL')
    )
    total_unpaid = unpaid_fees.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    unpaid_count = unpaid_fees.count()
    
    # Overdue fees
    overdue_fees = unpaid_fees.filter(due_date__lt=today)
    overdue_count = overdue_fees.count()
    
    # Due today
    due_today = unpaid_fees.filter(due_date=today).count()
    
    # Due this week
    week_end = today + timedelta(days=7)
    due_this_week = unpaid_fees.filter(due_date__range=[today, week_end]).count()
    
    # Recent payments (last 10)
    recent_payments = FeeRecord.objects.filter(
        payment_status='PAID'
    ).order_by('-payment_date')[:10]
    
    # Unread notifications
    unread_notifications = PaymentNotification.objects.filter(
        admin_user=request.user,
        is_read=False
    ).count()
    
    context = {
        'total_students': total_students,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'overdue_count': overdue_count,
        'due_today': due_today,
        'due_this_week': due_this_week,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'recent_payments': recent_payments,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'fees/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def paid_fees_list(request):
    """List all paid fees"""
    paid_fees = FeeRecord.objects.filter(
        payment_status='PAID'
    ).select_related('student').order_by('-payment_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        paid_fees = paid_fees.filter(
            Q(student__name__icontains=search_query) |
            Q(student__student_id__icontains=search_query) |
            Q(transaction_id__icontains=search_query)
        )
    
    context = {
        'paid_fees': paid_fees,
        'search_query': search_query,
    }
    
    return render(request, 'fees/paid_fees_list.html', context)


@login_required
@user_passes_test(is_admin)
def unpaid_fees_list(request):
    """List all unpaid fees with action buttons"""
    unpaid_fees = FeeRecord.objects.filter(
        Q(payment_status='UNPAID') | Q(payment_status='PARTIAL')
    ).select_related('student').order_by('due_date')
    
    # Filter options
    filter_type = request.GET.get('filter', 'all')
    today = timezone.now().date()
    
    if filter_type == 'overdue':
        unpaid_fees = unpaid_fees.filter(due_date__lt=today)
    elif filter_type == 'due_today':
        unpaid_fees = unpaid_fees.filter(due_date=today)
    elif filter_type == 'due_soon':
        week_end = today + timedelta(days=7)
        unpaid_fees = unpaid_fees.filter(due_date__range=[today, week_end])
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        unpaid_fees = unpaid_fees.filter(
            Q(student__name__icontains=search_query) |
            Q(student__student_id__icontains=search_query)
        )
    
    context = {
        'unpaid_fees': unpaid_fees,
        'filter_type': filter_type,
        'search_query': search_query,
    }
    
    return render(request, 'fees/unpaid_fees_list.html', context)


@login_required
@user_passes_test(is_admin)
def reminders_log(request):
    """View all sent reminders"""
    reminders = ReminderLog.objects.select_related(
        'fee_record__student'
    ).order_by('-sent_at')
    
    # Filter by type
    reminder_type = request.GET.get('type', '')
    if reminder_type:
        reminders = reminders.filter(reminder_type=reminder_type)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        reminders = reminders.filter(status=status)
    
    # Search by student
    search_query = request.GET.get('search', '')
    if search_query:
        reminders = reminders.filter(
            Q(fee_record__student__name__icontains=search_query) |
            Q(recipient_email__icontains=search_query)
        )
    
    # Pagination could be added here
    reminders = reminders[:100]  # Limit to latest 100
    
    context = {
        'reminders': reminders,
        'reminder_type': reminder_type,
        'status': status,
        'search_query': search_query,
    }
    
    return render(request, 'fees/reminders_log.html', context)


@login_required
@user_passes_test(is_admin)
def create_fee_record(request):
    """Create new fee record for student"""
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            fee_record = form.save(commit=False)
            fee_record.created_by = request.user
            fee_record.save()
            messages.success(request, f'Fee record created for {fee_record.student.name}')
            return redirect('admin_dashboard')
    else:
        form = FeeRecordForm()
    
    context = {'form': form}
    return render(request, 'fees/create_fee_record.html', context)


@login_required
@user_passes_test(is_admin)
def manual_resend_reminder(request, fee_id):
    """Manually resend reminder for a specific fee"""
    fee_record = get_object_or_404(FeeRecord, id=fee_id)
    
    success, message = PaymentService.manual_resend_reminder(fee_record)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect(request.META.get('HTTP_REFERER', 'unpaid_fees_list'))


@login_required
@user_passes_test(is_admin)
def mark_as_paid(request, fee_id):
    """Manually mark fee as paid"""
    if request.method == 'POST':
        fee_record = get_object_or_404(FeeRecord, id=fee_id)
        
        amount = float(request.POST.get('amount', fee_record.fee_amount))
        payment_method = request.POST.get('payment_method', 'Cash')
        transaction_id = request.POST.get('transaction_id', '')
        
        PaymentService.process_payment(
            fee_record,
            amount,
            payment_method,
            transaction_id
        )
        
        messages.success(request, f'Payment recorded for {fee_record.student.name}')
        return redirect('unpaid_fees_list')
    
    return redirect('unpaid_fees_list')


@login_required
@user_passes_test(is_admin)
def notifications_list(request):
    """View payment notifications"""
    notifications = PaymentNotification.objects.filter(
        admin_user=request.user
    ).select_related('fee_record__student').order_by('-notified_at')
    
    # Mark as read if requested
    if request.GET.get('mark_read'):
        notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'fees/notifications_list.html', context)


@login_required
@user_passes_test(is_admin)
def run_reminder_check(request):
    """Manually trigger reminder check"""
    results = FeeReminderService.check_and_send_reminders()
    
    message = f"Reminders sent: {results['due_soon']} due soon, {results['due_today']} due today, {results['overdue']} overdue"
    
    if results['errors']:
        message += f". Errors: {len(results['errors'])}"
        messages.warning(request, message)
    else:
        messages.success(request, message)
    
    return redirect('admin_dashboard')


# API endpoint for payment webhook (for online payment gateway integration)
@login_required
def payment_webhook(request):
    """Handle payment webhook from payment gateway"""
    if request.method == 'POST':
        # This is a simplified example - actual implementation depends on payment gateway
        try:
            # Parse payment data from gateway
            transaction_id = request.POST.get('transaction_id')
            amount = float(request.POST.get('amount'))
            fee_record_id = request.POST.get('fee_record_id')
            payment_method = request.POST.get('payment_method', 'Online')
            
            # Verify transaction with payment gateway here
            # ... gateway verification code ...
            
            # Process payment
            fee_record = FeeRecord.objects.get(id=fee_record_id)
            PaymentService.process_payment(
                fee_record,
                amount,
                payment_method,
                transaction_id
            )
            
            return JsonResponse({'status': 'success', 'message': 'Payment processed'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
@user_passes_test(is_admin)
def student_fee_detail(request, student_id):
    """View all fees for a specific student"""
    student = get_object_or_404(Student, id=student_id)
    fees = FeeRecord.objects.filter(student=student).order_by('-due_date')
    
    # Calculate totals
    total_fees = fees.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    total_paid = fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_balance = total_fees - total_paid
    
    context = {
        'student': student,
        'fees': fees,
        'total_fees': total_fees,
        'total_paid': total_paid,
        'total_balance': total_balance,
    }
    
    return render(request, 'fees/student_fee_detail.html', context)